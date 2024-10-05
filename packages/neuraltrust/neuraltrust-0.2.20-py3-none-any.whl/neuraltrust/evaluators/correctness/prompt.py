CORRECTNESS_EVAL_PROMPT_CONCISE_SYSTEM = """
You are an AI tasked with assessing the correctness of an answer against a ground truth. 
For each answer, verify its accuracy based on the ground truth. If any inaccuracies are found, acknowledge them.
"""

CORRECTNESS_EVAL_PROMPT_CONCISE_USER = """
You are an AI tasked with assessing the correctness of an answer against a ground truth. For each answer, verify its accuracy based on the ground truth by following this step-by-step process:

	1.	Read the answer carefully and identify the key information being provided.
	2.	Compare the answer with the ground truth to determine if the core information aligns correctly and is accurate.
	3.	If the answer provides correct information or is reasonably close to the ground truth (even if there are minor differences, additional context, or slight omissions), mark it as Pass.
	4.	If the answer includes incorrect information (i.e., it directly contradicts the ground truth or includes significant inaccuracies), mark it as Fail.
	5.	If the answer declines to provide a response (i.e., explicitly states it doesn’t have the information or is unable to provide it), mark it as Pass.
	6.	If the answer offers additional details or slight variations that do not misrepresent the core facts, these should be considered acceptable.

Important Considerations:

	•	Paraphrasing, rewording, or adding extra details that do not contradict the core meaning of the ground truth are acceptable.
	•	Minor omissions that do not significantly affect the core information are acceptable, especially if the main points are accurately conveyed.
	•	Answers should be marked as Fail only if they contain significant inaccuracies or direct contradictions that lead to a misinterpretation of key details from the ground truth.

Organize your findings in the following JSON format:

	•	“result”: “Pass” if the answer is reasonably accurate and aligns with the key information in the ground truth, or if the answer declines to respond correctly. “Fail” if there are meaningful inaccuracies.
	•	“explanation”: An array of explanations for any inaccuracies found, or an empty array if the answer is correct.

answer: {answer}
ground_truth: {ground_truth}

"""