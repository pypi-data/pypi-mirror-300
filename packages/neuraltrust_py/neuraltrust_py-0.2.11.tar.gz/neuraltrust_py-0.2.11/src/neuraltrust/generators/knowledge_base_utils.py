import os
import uuid
from typing import List
import re

from upstash_vector import Index
import numpy as np

from neuraltrust.llm.embeddings import get_default_embedding


def compute_embeddings(text_chunks: List[str]) -> List[List[float]]:
    embedding_model = get_default_embedding()
    embeddings = []
    for chunk in text_chunks:
        seed_embedding = np.array(embedding_model.embed(texts=[chunk]))
        seed_embedding_list = seed_embedding.flatten().tolist() if isinstance(seed_embedding,
                                                                              np.ndarray) else seed_embedding
        embeddings.append(seed_embedding_list)

    return embeddings


def reset_index():
    url_upstash = os.getenv("UPSTASH_URL")
    token = os.getenv("UPSTASH_TOKEN")

    index = Index(url=url_upstash, token=token)
    index.reset()


def get_index():
    url_upstash = os.getenv("UPSTASH_URL")
    token = os.getenv("UPSTASH_TOKEN")

    index = Index(url=url_upstash, token=token)
    return index


def index_from_pdf(index, path: str):
    pdf_files = []
    if os.path.isdir(path):
        # If path is a directory, get all PDF files
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
    elif os.path.isfile(path) and path.lower().endswith('.pdf'):
        # If path is a single PDF file
        pdf_files.append(path)
    else:
        raise ValueError("The provided path is neither a PDF file nor a directory containing PDF files.")

    for pdf_path in pdf_files:
        # Extract text from PDF
        text_chunks = extract_text_from_pdf(pdf_path)

        # Compute embeddings using Azure OpenAI
        embeddings = compute_embeddings(text_chunks)

        # Write to vector store
        ids = [str(uuid.uuid4())[:8] for doc in text_chunks]
        write_to_vector_store(index, ids, text_chunks, embeddings, pdf_path)


def write_to_vector_store(index,
                          ids: List[str],
                          text_chunks: List[str],
                          embeddings: List[List[float]],
                          pdf_path: str):
    index.upsert(
        vectors=[
            (
                id,
                embedding,
                {
                    "text": document,
                    "url": pdf_path
                }
            )
            for id, embedding, document
            in zip(ids, embeddings, text_chunks)
        ]
    )

    print(f"Uploaded {len(text_chunks)} documents to Upstash index.")


def extract_text_from_pdf(pdf_path: str) -> List[str]:
    try:
        import PyPDF2
    except ImportError:
        raise ImportError(
            "PyPDF2 is required to extract text from PDF files. Install it using 'pip install PyPDF2'.")

    def split_into_sentences(text):
        # Normalize line breaks and spaces
        text = re.sub(r'\s+', ' ', text)

        # Split text into lines first
        lines = text.split('\n')

        sentences = []
        current_sentence = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if the line is a list item or table-like content
            if re.match(r'^[o•]\s|^\w+\s*\.{3,}', line):
                if current_sentence:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                sentences.append(line)
            else:
                # Split regular text into sentences
                line_sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', line)
                for s in line_sentences:
                    if s:
                        if current_sentence:
                            current_sentence += " " + s
                        else:
                            current_sentence = s
                        if s[-1] in '.!?':
                            sentences.append(current_sentence.strip())
                            current_sentence = ""

        if current_sentence:
            sentences.append(current_sentence.strip())

        return [s for s in sentences if s.strip()]

    def create_chunks(sentences, max_chunk_size=1000):
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0

            current_chunk.append(sentence)
            current_length += sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    text_chunks = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            sentences = split_into_sentences(text)
            chunks = create_chunks(sentences)
            text_chunks.extend(chunks)

    return text_chunks
