import json
from llm_client import LLMClient

class VerificationResult:
    def __init__(self, label, score, explanation):
        self.label = label
        self.score = score
        self.explanation = explanation

class SupportChecker:
    def __init__(self):
        self.llm = LLMClient()

    def verify(self, answer, retrieved_context):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a strict verification module. Evaluate if the Answer is fully supported "
                    "by the Retrieved Context. Do not use outside knowledge. "
                    "Respond strictly in JSON format: {\"label\": \"SUPPORTED\" or \"HALLUCINATED\", "
                    "\"score\": 0.0 to 1.0, \"explanation\": \"short reasoning\"}"
                )
            },
            {
                "role": "user",
                "content": f"Context: {retrieved_context}\n\nAnswer: {answer}"
            }
        ]
        
        try:
            response_text = self.llm.chat(messages, temperature=0.0)
            
            # Clean markdown JSON blocks if the model adds them
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].strip()
                
            data = json.loads(response_text)
            return VerificationResult(
                label=data.get("label", "UNKNOWN"),
                score=float(data.get("score", 0.0)),
                explanation=data.get("explanation", "No explanation provided.")
            )
        except Exception as e:
            return VerificationResult("ERROR", 0.0, f"Verification parsing failed: {str(e)}")