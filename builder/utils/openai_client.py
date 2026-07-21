import json

from openai import OpenAI


class OpenAIClient:

    def __init__(self):

        self.client = OpenAI(
            base_url="http://127.0.0.1:1234/v1",
            api_key="lm-studio"
        )

        self.model = "qwen3.5-9b"

    def ask(self, prompt: str):

        response = self.client.chat.completions.create(

            model=self.model,

            temperature=0.2,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ein erfahrener Softwarearchitekt. "
                        "Wenn JSON verlangt wird, antworte ausschließlich mit gültigem JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()

    def ask_json(self, prompt: str):

        text = self.ask(prompt)

        print("\n========== KI ==========")
        print(text)
        print("========================\n")

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Die KI hat kein gültiges JSON zurückgegeben.")

        text = text[start:end + 1]

        return json.loads(text)