import os
from openai import OpenAI


class Model:
    def __init__(self, model_name):
        self.model_name = model_name

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{os.getenv('OPENROUTER_API_KEY')}",
        )


    def generate_text(self, instruction, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "developer",
                        "content": instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred: {e}"