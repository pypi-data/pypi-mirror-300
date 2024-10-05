import time
from typing import List, Tuple, Optional

from ...interfaces.result import EvalResult, EvalResultMetric
from ...metrics.passed import Passed
from ...utils.logger import logger
from ...metrics.metric_type import MetricType
from ..llm_evaluator import LlmEvaluator
from .prompt import CORRECTNESS_EVAL_PROMPT_CONCISE_SYSTEM, CORRECTNESS_EVAL_PROMPT_CONCISE_USER

class Correctness(LlmEvaluator):

    def __init__(
            self,
            **kwargs
        ):
        super().__init__(
            system_message_template=CORRECTNESS_EVAL_PROMPT_CONCISE_SYSTEM,
            user_message_template=CORRECTNESS_EVAL_PROMPT_CONCISE_USER,
            **kwargs
        )
        
    @property
    def name(self) -> str:
        return "Correctness"

    @property
    def display_name(self) -> str:
        return "Correctness"
    
    @property
    def default_model(self) -> str:
        return "gpt-4o-mini"

    @property
    def metric_ids(self) -> List[str]:
        return [MetricType.CORRECTNESS.value]

    @property
    def required_args(self) -> List[str]:
        return ["question", "answer", "ground_truth"]

    @property
    def examples(self):
        return []
    
    def is_failure(self, score) -> Optional[bool]:
        return bool(score)
        
    def reason(self, explanation: List[str]) -> str:
        if (len(explanation) > 0):
            explanation_str = "\n- ".join(explanation)
            return f"The following sentences don't have sufficient supporting evidence in the context:\n- {explanation_str}"
        else:
            return f"All sentences have sufficient supporting evidence in the context. The answer is grounded."

    def _evaluate(self, **kwargs) -> EvalResult:
        """
        Run the LLM evaluator.
        """
        start_time = time.perf_counter()
        # Validate that correct args were passed
        self.validate_args(**kwargs)

        # Construct Prompt  
        messages = self._prompt_messages(**kwargs)

        # Run the LLM Completion
        chat_completion_response_json: dict = self.llm_service.json_completion(
            model=self._model,
            messages=messages,
            temperature=self.TEMPERATURE,
        )
        metrics = []
        try:
            result = chat_completion_response_json["result"]
            explanation = chat_completion_response_json["explanation"]
            correctness_score = Passed.compute(result == "Pass")
            failure = self.is_failure(correctness_score)
            metrics.append(EvalResultMetric(id=MetricType.CORRECTNESS.value, value=correctness_score))
            reason = self.reason(explanation)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Error occurred during correctness evaluation: {e}")
            raise e

        end_time = time.perf_counter()
        eval_runtime_ms = int((end_time - start_time) * 1000)
        llm_eval_result = EvalResult(
            name=self.name,
            display_name=self.display_name,
            data=kwargs,
            failure=failure,
            reason=reason,
            runtime=eval_runtime_ms,
            model=self._model,
            metrics=metrics,
        )
        return {k: v for k, v in llm_eval_result.items() if v is not None}
    
    def _user_message(
        self,
        question: str,
        answer: str,
        ground_truth: str,
        **kwargs,
    ) -> str:
            """
            Generates data for evaluation.

            :param question: user query
            :param answer: llm response
            :param ground_truth: expected output
            :return: A dictionary with formatted data for evaluation
            """
            return self._user_message_template.format(
                question=question,
                answer=answer,
                ground_truth=ground_truth
            )