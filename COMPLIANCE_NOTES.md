# Compliance Notes

This is a beginner-level Streamlit project created for learning and hackathon practice.

## Included

- AGPLv3 license
- README
- Contributing guide
- User manual
- Security notes
- Code of conduct
- Changelog
- Environment example
- Docker readiness files
- Spec Kit documentation

## Not Included

### Secret Scanning

Not included because the app does not use API keys, passwords, tokens, databases, or external services.

### Dependency Audit

Not included because the app has only one dependency: Streamlit. This can be added later using `pip-audit`.

### Test Framework

Not included because the current app has minimal UI logic and no separate business logic functions. Manual testing is documented in the README.

### Coverage Reporting

Not included because no automated test suite exists yet.

### GitLab CI Pipeline

Not included because the app is deployed through Streamlit Cloud and does not currently require a CI/CD pipeline.

### Pre-commit Hooks

Not included to keep the beginner setup simple. This can be added later for formatting and linting.

### Automated Changelog

Not included because the project currently has a manually maintained `CHANGELOG.md`.

## Future Improvements

- Add basic Python tests.
- Add GitLab CI.
- Add `pip-audit`.
- Add pre-commit hooks.
- Add automated changelog generation.