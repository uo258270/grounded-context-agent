import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.berget.ai/v1",
            api_key=os.getenv("BERGET_API_KEY")
        )
        # Using the model recommended in the course materials
        self.model = "google/gemma-4-31b-it"

    def chat(self, messages, temperature=0.1):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"