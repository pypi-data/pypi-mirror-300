import math
import os
from typing import Dict, Optional, Sequence, List, Union, Any, Tuple
import logging
import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN
from upstash_vector import Index
from upstash_vector.types import RangeResult, QueryResult
from .base_knowledge_base import BaseKnowledgeBase
from ..llm.client import ChatMessage, LLMClient, get_judge_client
from ..llm.embeddings import get_default_embedding
from ..errors.exceptions import ImportError
from ..utils.language_detection import detect_lang
import upstash_vector

try:
    import umap
except ImportError as err:
    raise ImportError(missing_package="umap") from err

logger = logging.getLogger("neuraltrust.generators")

LANGDETECT_MAX_TEXT_LENGTH = 300
LANGDETECT_DOCUMENTS = 10

TOPIC_SUMMARIZATION_PROMPT = """
Your task is to name a cluster of documents by giving them a title which represents the topic a set of documents.

Your are given below a list of documents and you must extract the topic best representing ALL contents.
- Provide the topic in this language: {language}
- The topic should be as specific as possible.
- Do not use the airline name in a topic name

Make sure to only return the topic name between quotes, and nothing else.

For example, given these documents:

<documents>
Camembert is a moist, soft, creamy, surface-ripened cow's milk cheese.
----------
Bleu d'Auvergne is a French blue cheese, named for its place of origin in the Auvergne region.
----------
Roquefort is a sheep milk cheese from the south of France.
</documents>

The topic is:
"French Cheese"

Now it's your turn. Here is the list of documents:

<documents>
{topics_elements}
</documents>

The topic is:
"""


class Document:
    """A class to wrap the elements of the knowledge base into a unified format."""

    def __init__(
            self,
            id_vector: str,
            metadata: Dict[str, str],
            vector: List[float],
            topic: Optional[str] = None
    ):
        self.content = metadata.get('text', '')
        self.question = metadata.get('url', '')
        self.id = id_vector
        self.embeddings = vector
        self.topic = topic
        self.reduced_embeddings = None

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content


class KnowledgeBase(BaseKnowledgeBase):

    def __init__(
            self,
            url_upstash: str = None,
            token: str = None,
            seed: int = None,
            llm_client: Optional[LLMClient] = None,
            seed_topics: Optional[List[str]] = None,
    ) -> None:

        self._topics = None
        self._index_inst = None
        self._embeddings_inst = None
        self._reduced_embeddings_inst = None

        if not url_upstash:
            url_upstash = os.getenv("UPSTASH_URL")

        if not token:
            token = os.getenv("UPSTASH_TOKEN")

        self.index = Index(url=url_upstash, token=token)
        logger.warning("Created index connector")

        self._rng = np.random.default_rng(seed=seed)
        self._llm_client = llm_client or get_judge_client()
        self._embedding_model = get_default_embedding()

        (self._documents_per_topic,
         self._documents,
         self._scores,
         self._scores_per_topic) = self.load_data(seed_topics=seed_topics)

        self._documents_index = {doc.id: doc for doc in self._documents}

    def _set_lang(self, docs):
        document_languages = [
            detect_lang(doc.content[:LANGDETECT_MAX_TEXT_LENGTH])
            for doc in self._rng.choice(docs, size=LANGDETECT_DOCUMENTS)
        ]
        languages, occurences = np.unique(
            ["en" if (pd.isna(lang) or lang == "unknown") else lang for lang in document_languages], return_counts=True
        )
        self._language = languages[np.argmax(occurences)]

    def _get_documents(self, res: Union[RangeResult, QueryResult]) -> List[Document]:
        data = []
        vectors = res.vectors if isinstance(res, RangeResult) else res
        for vector_info in vectors:
            doc = self._get_document(vector_info)
            data.append(doc)
        return data

    def _get_document(self, vector_info: QueryResult, topic: Optional[str] = None):
        doc = Document(id_vector=vector_info.id,
                       metadata=vector_info.metadata,
                       vector=vector_info.vector,
                       topic=topic)
        return doc

    def reduce_embeddings(self, docs, embeddings):
        n_neighbors = min(15, max(2, len(docs) - 1))

        # Adjust n_components to be at most the number of samples minus 1
        n_components = min(2, len(docs) - 1)

        try:
            reducer = umap.UMAP(
                n_neighbors=n_neighbors,
                n_components=n_components,
                random_state=1234,
                n_jobs=1,
                metric='cosine'
            )
            reduced_vectors = reducer.fit_transform(embeddings)
        except ValueError as e:
            print(f"UMAP reduction failed: {e}")
            print("Falling back to original embeddings")
            reduced_vectors = embeddings

        for doc, reduced_vector in zip(docs, reduced_vectors):
            doc.reduced_embeddings = reduced_vector

        return reduced_vectors

    def _load_data_without_seed_topic(self):
        all_docs = self._load_all_data()
        scores = []
        scores_per_topic = {}

        self._set_lang(all_docs)

        embeddings = np.array([doc.embeddings for doc in all_docs])
        reduced_vectors = self.reduce_embeddings(docs=all_docs, embeddings=embeddings)

        logger.info("Finding topics in the knowledge base.")
        hdbscan = HDBSCAN(
            metric="cosine",
            cluster_selection_epsilon=0.0,
            allow_single_cluster=True
        )
        clustering = hdbscan.fit(reduced_vectors)

        docs_per_topic = {}
        for i, doc in enumerate(all_docs):
            topic_idx = clustering.labels_[i]
            if topic_idx == -1:
                continue

            score = clustering.probabilities_[i]

            if topic_idx not in docs_per_topic:
                docs_per_topic[topic_idx] = []
            if topic_idx not in scores_per_topic:
                scores_per_topic[topic_idx] = []

            docs_per_topic[topic_idx].append(doc)
            scores_per_topic[topic_idx].append(score)

        topics = set()
        topic_name_to_content = {}
        scores_per_topic_name = {}
        all_docs = []
        for topic_idx, docs in docs_per_topic.items():
            topic_name = self._get_topic_name(docs_per_topic[topic_idx])
            topic_name_to_content[topic_name] = docs_per_topic[topic_idx]
            scores_per_topic_name[topic_name] = scores_per_topic[topic_idx]

            for doc in docs_per_topic[topic_idx]:
                doc.topic = topic_name
                all_docs.append(doc)
            for score in scores_per_topic[topic_idx]:
                scores.append(score)

            topics.add(topic_name)

        logger.info(f"Found {len(topics)} topics in the knowledge base.")
        return topic_name_to_content, all_docs, list(topics), scores, scores_per_topic_name

    def _normalize_scores_per_topic(self, scores):
        for topic, scores_per_topic in scores.items():
            normalized = np.array(scores_per_topic) / sum(scores_per_topic)
            scores[topic] = normalized
        return scores

    def load_data(self, seed_topics: List[str] = None):
        logger.warning("Retrieving documents ...")
        if seed_topics is None:
            docs_per_topic, docs, seed_topics, scores, scores_per_topic = self._load_data_without_seed_topic()
            scores_per_topic = self._normalize_scores_per_topic(scores_per_topic)
            self._topics = seed_topics
            return docs_per_topic, docs, scores, scores_per_topic
        else:
            self._topics = seed_topics
            docs_per_topic, docs, scores, scores_per_topic = self._load_data_with_seed_topic(seed_topics)
            scores_per_topic = self._normalize_scores_per_topic(scores_per_topic)
            return docs_per_topic, docs, scores, scores_per_topic

    def filter_by_topic(self, topic: str):
        self._documents = self.documents_per_topic.get(topic, None)
        self._scores = self.scores_per_topic.get(topic, None)
        self._embeddings_inst = None
        self._reduced_embeddings_inst = None
        self._index_inst = None

        if self._documents is None or self._scores is None:
            raise ValueError("Wrong topic")

    def _load_all_data(self) -> List[Document]:
        res = self.index.range(cursor="", limit=5, include_vectors=True, include_metadata=True)
        data = self._get_documents(res)

        while res.next_cursor != "":
            res = self.index.range(cursor=res.next_cursor, limit=10, include_vectors=True, include_metadata=True)
            docs = self._get_documents(res)
            data.extend(docs)

        return data

    def _load_data_with_seed_topic(self, seed_topics: List[str]):
        doc_count = min([1000, self.index.info().vector_count])
        THRESHOLD = 0.60

        relevant_docs_per_topic = {}
        docs = []
        scores = []
        scores_per_topic = {}

        for seed_topic in seed_topics:
            relevant_docs_per_topic[seed_topic] = []
            scores_per_topic[seed_topic] = []

            seed_embedding = self._embedding_model.embed(seed_topic)
            seed_embedding_list = seed_embedding.flatten().tolist() if isinstance(seed_embedding,
                                                                                  np.ndarray) else seed_embedding
            try:
                res = self.index.query(vector=seed_embedding_list,
                                       top_k=doc_count,
                                       include_metadata=True,
                                       include_vectors=True)
                for result in res:
                    if result.score > THRESHOLD:
                        doc = self._get_document(vector_info=result, topic=seed_topic)
                        relevant_docs_per_topic[seed_topic].append(doc)
                        scores_per_topic[seed_topic].append(result.score)

                        docs.append(doc)
                        scores.append(result.score)

            except upstash_vector.errors.UpstashError as e:
                logger.error(f"Error querying Upstash: {e}")
                logger.error(f"Full embedding: {seed_embedding_list}")
                raise

        self._set_lang(docs)
        return relevant_docs_per_topic, docs, scores, scores_per_topic

    def get_savable_data(self):
        return {
            "columns": self._columns,
            "min_topic_size": self._min_topic_size,
            "topics": {int(k): topic for k, topic in self.topics.items()},
            "documents_topics": [int(doc.topic_id) for doc in self._documents],
        }

    def _get_topic_name(self, topic_documents):
        self._rng.shuffle(topic_documents)
        topics_str = "\n\n".join(["----------" + doc.content[:500] for doc in topic_documents[:10]])

        topics_str = topics_str[: 3 * 8192]
        prompt = TOPIC_SUMMARIZATION_PROMPT.format(language=self._language, topics_elements=topics_str)

        raw_output = self._llm_client.complete([ChatMessage(role="user", content=prompt)], temperature=0.0).content

        return raw_output.strip().strip('"')

    def get_random_document(self):
        return self._rng.choice(self._documents, p=self._scores)

    def get_neighbors(self, seed_document: Document, n_neighbors: int = 4, similarity_threshold: float = 0.2):
        seed_embedding = seed_document.embeddings

        relevant_documents = [
            doc
            for (doc, score) in self.vector_similarity_search_with_score(seed_embedding, k=n_neighbors)
            if score < similarity_threshold
        ]

        return relevant_documents

    def similarity_search_with_score(self, query: str, k: int) -> Sequence:
        query_emb = np.array(self._embedding_model.embed(query), dtype="float32")
        return self.vector_similarity_search_with_score(query_emb, k)

    def vector_similarity_search_with_score(self, query_emb: np.ndarray, k: int) -> Sequence:
        query_emb = np.atleast_2d(query_emb)
        distances, indices = self._index.search(query_emb, k)
        return [(self._documents[i], d) for d, i in zip(distances[0], indices[0])]

    @property
    def topics(self):
        return self._topics

    @property
    def documents_per_topic(self):
        return self._documents_per_topic

    @property
    def scores_per_topic(self):
        return self._scores_per_topic

    @property
    def _index(self):
        if self._index_inst is None:
            try:
                from faiss import IndexFlatL2
            except ImportError as err:
                raise ImportError(missing_package="faiss") from err

            self._index_inst = IndexFlatL2(self._dimension)
            self._index_inst.add(self._embeddings)
        return self._index_inst

    @property
    def language(self):
        return self._language

    @property
    def _embeddings(self):
        if self._embeddings_inst is None:
            self._embeddings_inst = np.array([doc.embeddings for doc in self._documents])

        return self._embeddings_inst

    @property
    def _reduced_embeddings(self):
        if self._reduced_embeddings_inst is None:
            self._reduced_embeddings_inst = np.array([doc.reduced_embeddings for doc in self._documents])

        return self._reduced_embeddings_inst

    @property
    def _dimension(self):
        return self._embeddings[0].shape[0]

    def __len__(self):
        return len(self._documents)

    def __getitem__(self, doc_id: str):
        return self._documents_index[doc_id]