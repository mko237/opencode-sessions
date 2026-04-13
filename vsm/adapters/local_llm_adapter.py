"""Very simple LLM adapter used for early development.

It satisfies the ``LLMPort`` protocol.  The implementation just echoes the prompt
or returns a canned response – real adapters can replace this later.
"""

from ..ports.llm_port import LLMPort


class LocalLLMAdapter(LLMPort):
    def generate(self, prompt: str) -> str:
        # Echo the prompt for now – replace with an actual model call later.
        return f"generated: {prompt}"

    def chat(self, messages):
        # Concatenate messages for a deterministic stub response.
        combined = " ".join(m.get("content", "") for m in messages)
        return f"chat: {combined}"
