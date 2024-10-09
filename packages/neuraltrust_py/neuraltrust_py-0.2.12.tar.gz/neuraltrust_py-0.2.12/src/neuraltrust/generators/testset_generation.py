from random import randint
from typing import Optional, Sequence, Union

import itertools
import numpy as np

from neuraltrust.generators.knowledge_base import KnowledgeBase
from src.neuraltrust.generators.question_generators import (
    QuestionGenerator,
    complex_questions,
    simple_questions,
    roleplay_questions,
    hypothetical_questions,
    storytelling_questions,
    obfuscation_questions,
    special_token_questions,
)
from src.neuraltrust.generators.question_generators.utils import maybe_tqdm
from src.neuraltrust.generators.testset import QATestset

question_types = {
    "functional": [
        simple_questions,
        complex_questions
    ],
    "adversarial": [
        roleplay_questions,
        hypothetical_questions,
        # storytelling_questions,
        obfuscation_questions,
        special_token_questions
    ]
}


def generate_testset(
        knowledge_base: KnowledgeBase,
        test_type: str,
        num_questions: Optional[int] = 50,
        question_generators: Optional[Union[QuestionGenerator, Sequence[QuestionGenerator]]] = None,
        agent_description: Optional[str] = "This agent is a chatbot that answers question from users.",
) -> QATestset:

    if question_generators is None:
        question_generators = question_types.get(test_type, None)
        if not question_generators:
            raise ValueError("Wrong test type, accepted types are 'functional' and 'adversarial'")

    docs_per_topic = knowledge_base.documents_per_topic
    total_elems = sum(len(docs) for docs in docs_per_topic.values())

    if total_elems == 0:
        raise ValueError("The knowledge base is empty. Please add documents before generating a testset.")

    questions_per_topic = {}
    for topic, docs in docs_per_topic.items():
        num_docs = len(docs)
        num_questions_per_topic = round((num_docs / total_elems) * num_questions)
        questions_per_topic[topic] = num_questions_per_topic

    # add extra questions to the topics with highest value
    total = sum(questions_per_topic.values())
    topics = list(docs_per_topic.keys())
    if total != num_questions and topics:
        remaining = num_questions - total
        sorted_topics = sorted(questions_per_topic.items(), key=lambda x: x[1], reverse=True)
        for i in range(remaining):
            questions_per_topic[sorted_topics[i % len(sorted_topics)][0]] += 1

    questions_per_topic_and_type = {}
    shuffler = np.random.default_rng()
    for topic, num_questions_per_topic in questions_per_topic.items():
        questions_per_topic_and_type[topic] = {}
        shuffler.shuffle(question_generators)

        for i in range(len(question_generators)):
            num_questions_per_type = num_questions_per_topic // len(question_generators) + (1 if i < num_questions_per_topic % len(question_generators) else 0)
            if num_questions_per_type > 0:
                questions_per_topic_and_type[topic][question_generators[i]] = num_questions_per_type

    lang = knowledge_base.language
    question_list = []
    for topic, dict_generator in questions_per_topic_and_type.items():
        knowledge_base.filter_by_topic(topic)
        total_loading_bar = sum(dict_generator.values())

        if total_loading_bar == 0:
            print(f"We don't have any questions for {topic}, skipping ...")
            continue

        main_generator = itertools.chain.from_iterable(
            [
                generator.generate_questions(
                    knowledge_base,
                    num_questions=n,
                    agent_description=agent_description,
                    language=lang,
                )
                for generator, n in dict_generator.items()
            ]
        )
        questions = list(maybe_tqdm(main_generator, total=total_loading_bar, desc=f"Generating questions for topic {topic}"))

        for question in questions:
            question.metadata["topic"] = knowledge_base[question.metadata["seed_document_id"]].topic
            question_list.append(question)

    return QATestset(question_list)
