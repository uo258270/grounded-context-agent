import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("MODEL_NAME")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

        if not self.model:
            raise ValueError("MODEL_NAME is missing. Add it to your .env file.")

        if base_url:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            self.client = OpenAI(api_key=api_key)

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=600,
        )

        return response.choices[0].message.content