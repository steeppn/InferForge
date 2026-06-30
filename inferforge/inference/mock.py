class MockInferenceBackend:
    name = "mock"

    async def generate(self, prompt: str) -> str:
        return f"Mock response for: {prompt}"
