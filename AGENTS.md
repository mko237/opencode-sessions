# Skill tool usage:
  - skills often recommend using a workflow.. if a task can be accomplished via the workflow perfer following the relevant steps instead of solving a task another way
  - skills are written for you the agent/assistant and also meant to be performed by you, not the user. 
## Python Usage in skills:
  - some skills may have and recommend python script usage.. always use `uv run python` instead of just calling python directly
  - prioritize built in scripts from skills over tools liek grep / glob / read (unless specified or no alternatives exist)

# Python:
  - always use uv to execute and manage python projects. 
  - do not modify pyproject.toml directly. use `uv init` to create and `uv add/remove` to modify package requirements
