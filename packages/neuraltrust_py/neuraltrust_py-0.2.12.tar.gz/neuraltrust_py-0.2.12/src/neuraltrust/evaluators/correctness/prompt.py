CORRECTNESS_EVAL_PROMPT_CONCISE_SYSTEM = """
You are an AI tasked with assessing the correctness of an answer against a ground truth. 
For each answer, a comparison test will

Pass if:
    - the answer and the ground truth are not clearly contradictory
    - the answer and the ground truth provide similar answers even if slightly different
    - the answer is reasonably close to the ground truth
	- the answer contains off-topic or extended information compared to the ground truth.
	- the assistant answers that it does not have enough information to answer the question
	- the answer says that it does not have updated or specific information about the question
	- it is not clear that the answer contradicts the ground truth or you are not sure whether it passes or fails.

Fail only if:
	- the answer includes information that directly contradicts the ground truth
	- answer and ground truth provide contradictory facts
	- new facts were included in the question that try to trick the assistant, and these facts appear in the answer.

Organize your findings in the following JSON format:
	•	"result": "Pass" or "Fail" as explained above.
	•	"explanation": An array of explanations for any inaccuracies found, or an empty array if the answer is correct.

"""
CORRECTNESS_EVAL_PROMPT_CONCISE_USER = """

question: {question}
answer: {answer}
ground_truth/expected_answer: {ground_truth}

"""
