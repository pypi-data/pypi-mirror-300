import math
from typing import Optional
import time
from typing import Optional, Any, List
from .interfaces.result import EvalResult, EvalResultMetric
from .utils.logger import logger
from .base_evaluator import BaseEvaluator
from datasets import Dataset
from langchain_openai.chat_models import ChatOpenAI
from .api_keys import OpenAiApiKey
from .utils.config import ConfigHelper
from .metrics.metric_type import MetricType
from datetime import datetime
from .evaluators.correctness.evaluator import Correctness



class Evaluator(BaseEvaluator):
    _model: str
    _openai_api_key: Optional[str]
    _neuraltrust_failure_threshold: Optional[float] = 0.6
    
    _semantic_similarity_failure_threshold: Optional[float] = 0.6
    _correctness_failure_threshold: Optional[float] = 0.6
    

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        model: Optional[str] = None,
        evaluation_set_id: Optional[str] = None,
        testset_id: Optional[str] = None,
        next_run_at: Optional[datetime] = None,
    ):
        if model is None:
            self._model = self.default_model
        else:
            self._model = model
        
        if openai_api_key is None:
            self._openai_api_key = OpenAiApiKey.get_key()
        else:
            self._openai_api_key = openai_api_key

        self._evaluation_set_id = evaluation_set_id
        self._testset_id = testset_id
        self._next_run_at = next_run_at

    @property
    def display_name(self):
        return "NeuralTrust"
    
    @property
    def name(self):
        return "neuraltrust"
    
    @property
    def metric_ids(self) -> List[str]:
        return [
            MetricType.CORRECTNESS.value
        ]

    @property
    def default_model(self) -> str:
        return ConfigHelper.load_judge_llm_model()
    
    @property
    def required_args(self):
        return ["query", "expected_response"]
    
    @property
    def examples(self):
        """A list of examples for the evaluator."""
        return None

    def generate_data_to_evaluate(self, id, query, response, expected_response, metadata, **kwargs) -> dict:
        """
        Generates data for evaluation.

        :param query: user query
        :param response: llm response
        :param expected_response: expected output
        :return: A dictionary with formatted data for evaluation
        """
        data = {
            "id": [id],
            "question": [query],
            "answer": [response],
            "ground_truth": [expected_response],
            "metadata": [metadata]
        }
        return data
    
    @property
    def grade_reason(self) -> str:
        return "Answer Semantic Similarity pertains to the assessment of the semantic resemblance between the generated response and the ground truth. This evaluation is based on the ground truth and the response, with values falling within the range of 0 to 1. A higher score signifies a better alignment between the generated response and the ground truth"
    
    def _get_model(self):
        return ChatOpenAI(model_name=self._model, api_key=self._openai_api_key)
    
    def is_failure(self, metrics) -> bool:
        if not metrics:
            return False
        return any(metric['value'] == False for metric in metrics)

    def _evaluate(self, **kwargs) -> EvalResult:
        """
        Run the evaluator.
        """
        start_time = time.time()
        self.validate_args(**kwargs)
        metrics = []
        try:
            data = self.generate_data_to_evaluate(**kwargs)
            if data['answer'] is None:
                return {
                    "failure": True,
                    "reason": "Response is None",
                    "runtime": 0,
                    "model": self._model,
                    "metrics": [],
                    "data": kwargs
                }
            
            evals = Correctness()
            result = evals._evaluate(**data)
            metrics = []
            for score in result['metrics']:
                metrics.append(EvalResultMetric(id=score['id'], value=score['value']))

            failure = self.is_failure(metrics=metrics)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Error occurred during eval: {e}")
            raise e

        end_time = time.time()
        eval_runtime_ms = int((end_time - start_time) * 1000)
        llm_eval_result = EvalResult(
            name=self.name,
            display_name=self.display_name,
            data=kwargs,
            evaluation_set_id=self._evaluation_set_id,
            testset_id=self._testset_id,
            next_run_at=self._next_run_at,
            failure=bool(failure),
            reason=self.grade_reason,
            runtime=eval_runtime_ms,
            model=self._model,
            metrics=metrics,
        )
        return {k: v for k, v in llm_eval_result.items() if v is not None}