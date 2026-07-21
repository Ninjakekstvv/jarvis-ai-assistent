from pathlib import Path


class PromptLoader:

    def __init__(self):

        self.prompt_path = (
            Path(__file__).parent.parent
            / "prompts"
        )

    def load(self, name: str, **kwargs):

        file = self.prompt_path / f"{name}.txt"

        prompt = file.read_text(
            encoding="utf-8"
        )

        for key, value in kwargs.items():

            placeholder = f"[[{key.upper()}]]"

            prompt = prompt.replace(
                placeholder,
                str(value)
            )

        return prompt