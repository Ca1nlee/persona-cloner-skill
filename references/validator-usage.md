# Persona package validator

Run:

```bash
python scripts/validate_persona_package.py <package-dir>
python scripts/validate_persona_package.py <package-dir> --report <package-dir>/eval/validation-report.md
```

Pass gate:
- **pass**: no errors, no warnings
- **pass_with_warnings**: no errors, but cleanup still recommended
- **fail**: one or more structural or truthfulness-critical errors

The validator checks:
- required root files
- required reference files
- examples and evaluation prompts
- identity-boundary language
- source IDs / evidence trace
- eval track structure
- memory versioning structure
- placeholder-heavy scaffold residue

Use the validator for package completeness.
Use `scripts/eval_runtime_behavior.py` for post-build answer-behavior checks.
They solve different problems.
