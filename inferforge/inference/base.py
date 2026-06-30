from typing import Protocol


class InferenceBackend(Protocol):
    name: str

    async def generate(self, prompt: str) -> str:
        """Generate output for a prompt."""
