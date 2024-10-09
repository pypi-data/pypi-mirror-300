from typing import List, Dict
from .interfaces.data import DataPoint
from .generators import KnowledgeBase, generate_testset
from .utils import _generate_id
from .testset import Testset
from .services.api_service import NeuralTrustApiService

class GenerateTestset:
    def __init__(self, evaluation_set_id, name=None, description=None, knowledge_base: KnowledgeBase = None, num_questions: int = None):
        self.evaluation_set_id = evaluation_set_id
        self.name = name
        self.description = description
        self.knowledge_base = knowledge_base
        self.num_questions = num_questions
        self._load_existing_evaluation_set()

    def _load_existing_evaluation_set(self):
        evalset_data = NeuralTrustApiService.load_evaluation_set(self.evaluation_set_id)
        if evalset_data:
            self.name = evalset_data['name']
            self.description = evalset_data['description']

    def _generate_testset(self, type: str) -> str:
        if self.knowledge_base is None:
            raise ValueError("Knowledge base is not set.")

        testset_id = _generate_id(f"{self.name}_testset")

        try:
            testset = generate_testset(
                knowledge_base=self.knowledge_base,
                test_type=type,
                num_questions=self.num_questions,
                agent_description=self.description,
            )
        except ValueError as e:
            raise ValueError(f"Failed to generate testset: {str(e)}")

        self._load_testset_to_neuraltrust(testset_id, testset.samples)
        self._update({'testsetId': testset_id, 'numQuestions': self.num_questions})
        return testset_id

    def generate_adversarial(self):
        return self._generate_testset("adversarial")

    def generate_functional(self):
        return self._generate_testset("functional")

    def _load_testset_to_neuraltrust(self, testset_id: str, data: List[DataPoint]):
        try:
            Testset.create(
                id=self.evaluation_set_id,
                testset_id=testset_id,
                rows=data
            )
        except Exception as e:
            raise ValueError(f"Failed to load testset to NeuralTrust: {e}")

    def _update(self, eval_set: Dict):
        try:
            NeuralTrustApiService.update_evaluation_set(self.evaluation_set_id, eval_set)
        except Exception as e:
            raise