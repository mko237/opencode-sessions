# Step 2.4 LLM Agents & Memory (uses ports)

## Items

- [X] 15) Examine LLMPort prompt construction (f‑string) for readability and future templating needs.
- [x] 16) Verify the Determinism note (seed handling) is captured in the LLMPort API. (Undeeded)
- [x] 17) Review MemoryPort API (`append`, `load_all`, `query`) for completeness; consider bulk‑load or delete ops.
      - note: MemoryPort has been documented in `step_2_2_item_8_1.md`
- [x] 18) Check observation‑memory log format (YAML entries) for consistency and easy parsing. (skipped)
- [x] 19) Ensure ToolPort registration/discovery does not create circular imports with agents. (skipped)


## Item 15

---
**LLMPort Prompt Construction Design**

The current design defines `LLMPort` with a single `generate(prompt: str, **kwargs) -> str` method and builds prompts directly with f‑strings, e.g.:
```python
prompt = f"System 1 context: {ctx}\nMessages:{msg_log}"
```

### Observations
- **Readability** – f‑strings are concise but mix formatting logic with call sites.
- **Re‑use** – Repeating the same pattern across agents makes changes error‑prone.
- **Flexibility** – f‑strings cannot be edited at runtime; conditional sections require extra code.
- **Determinism** – The port logs a seed, but the prompt builder does not expose it.

### Suggested Minimal Change
Add a small helper in the `LLMPort` module to centralise prompt layout:
```python
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class PromptTemplate:
    """Simple template that can be formatted with a dict."""
    template: str

    def render(self, **ctx) -> str:
        return self.template.format(**ctx)

class LLMPort(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        ...

    def build_prompt(self, *, system: str = "", messages: str = "", **extra) -> str:
        """Create a default prompt layout.

        Callers can pass a custom ``PromptTemplate`` via ``extra['template']``.
        """
        default = PromptTemplate(
            "System context:\n{system}\n\nMessages:\n{messages}"
        )
        tmpl = extra.get("template", default)
        return tmpl.render(system=system, messages=messages, **extra)
```

#### Benefits
- **Single source of truth** for prompt formatting.
- **Readability** – call sites become `prompt = llm_port.build_prompt(system=ctx, messages=msg_log)`.
- **Extensibility** – custom templates can be loaded from YAML or other files.
- **Determinism hook** – the helper can automatically embed the current seed.
- **Testable** – template rendering can be unit‑tested.

#### Adoption Steps
1. Add the helper to the file that defines `LLMPort`.
2. Update any existing f‑string usages to `llm_port.build_prompt(...)` (one‑line change per caller).
3. Optionally expose a default template file for non‑Python edits.

---
*(End of design note)*
