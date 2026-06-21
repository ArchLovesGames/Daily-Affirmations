# Contributing

Thank you for contributing to Daily Affirmations. While this is a hackathon project, contributions are welcome

## How to Contribute

1. Fork or clone the repository.
2. Create a new branch.
3. Make your changes.
4. Test the app locally.
5. Submit a merge request or pull request.

## Local Testing

Please refer to README.md for local run testing.

## Local Git Hooks

Install the repository hooks once after cloning:

```bash
git config core.hooksPath .githooks
```

Install development check tools:

```bash
python -m pip install -r requirements-dev.txt
```

The pre-commit hook runs formatting, linting, Python compilation, unit tests,
secret scanning, and affirmation data compliance checks. The pre-push hook also
runs type checking, dead code checking, security scanning, and package audits
when the development tools are installed.
