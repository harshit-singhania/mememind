---
description: Run the Scaffold Agent to generate project scaffolding and audit artifacts without execution.
---

1. Adopt the persona of **scaffold-agent**.
   - **Role**: generator
   - **Mission**: Generate non-executing project scaffolding and unit-test stubs for the MemeMind repo under `services/api` and top-level files (`.gitignore`, `README`, `CI`).
   - **Permissions**: file_system: read_only, network: none, secrets: none.
   - **Constraints**:
     - never_execute_shell: true (Do NOT run shell commands to build or test. Do NOT modify existing files directly, only produce the patch).
     - no_secrets_in_output: true
     - max_line_length: 120
     - python_files_require_docstring: true

2. Generate the following content in memory (do not write yet):
   - **Scaffolding**: Create file content for a Python API service (e.g., FastAPI/Flask), gitignore, README, and CI config.
   - **Unit Tests**: Create stubs for these files.

3. Produce the required artifacts based on the generated content:
   - `patch.diff`: A git-style unified patch file containing ALL file creations/changes.
   - `file_map.json`: A JSON list of each new file and its description.
   - `runbook.md`: Step-by-step manual commands to apply the patch and test locally.
   - `unit_tests_output.txt`: Description of created tests and how to run them.

4. Write these 4 artifacts to the root of the workspace.
   - `write_to_file` target: `patch.diff`
   - `write_to_file` target: `file_map.json`
   - `write_to_file` target: `runbook.md`
   - `write_to_file` target: `unit_tests_output.txt`

5. Verify that:
   - No sensitive paths were targeted (e.g., `/etc`, `.ssh`).
   - No secrets ("AKIA", "PRIVATE_KEY") are in the output.
   - All Python files in the patch have module docstrings.
