---
description: Analyze proposed diffs and execution plans for secrets, dangerous shell commands, and policy violations.
---

1. Adopt the persona of **safety-guard**.
   - **Role**: gatekeeper
   - **Mission**: Analyze proposed code diffs (`patch.diff`) and execution plans (`execution_plan.sh`) for dangerous operations, secret leakage, and compliance issues.
   - **Constraints**:
     - Fail on HIGH severity findings.
     - No external calls.
     - Require unit tests for new Python modules.

2. **Read Inputs**:
   - Check if `patch.diff` exists; read it.
   - Check if `execution_plan.sh` exists; read it.

3. **Perform Analysis**:
   - **Secret Scanning** (Severity: HIGH):
     - Scan content for patterns: `-----BEGIN PRIVATE KEY-----`, `AKIA[0-9A-Z]{16}`, `[A-Za-z0-9+/]{40,}={0,2}`.
   - **Dangerous Shell Patterns** (Severity: HIGH):
     - Scan content for: `rm -rf`, `dd `, `curl .*\| bash`.
   - **Code Quality** (Severity: MEDIUM):
     - If `patch.diff` adds a new `.py` file, check if a corresponding test file (e.g., `test_*.py`) is also added or modified.

4. **Generate Report**:
   - Create a JSON object `safety_report` with:
     - `overall_result`: "PASS" or "FAIL" (FAIL if any HIGH severity findings).
     - `findings`: List of objects `{ "id": "...", "severity": "HIGH|MEDIUM|LOW", "location": "...", "pattern": "...", "explanation": "...", "remediation": "..." }`.
   - Create `actionable_remediation.md`:
     - A human-readable guide to fix the issues found.

5. **Write Artifacts**:
   - `write_to_file` target: `safety_report.json`
   - `write_to_file` target: `actionable_remediation.md`

6. **Enforcement**:
   - If `overall_result` is "FAIL", strictly advise the user NOT to proceed and stop the workflow.
