# Contributing

Open an Issue for a reproducible bug or a small feature proposal before making broad changes. Do not include credentials or personal data. Small fixes can go directly to a pull request.

Keep modules focused, preserve the JSON-RPC v1 contract, and document user-visible changes. Include a short rationale, relevant tests, and any limitation in the pull request. Avoid platform-specific behavior in the core. Plugin integrations belong in separate repositories.

Run the checks in [README.md](README.md) before submitting. Tests must use mocks for external APIs and must not need live credentials. Update documentation and schemas when behavior or configuration changes. Source contributions are under GPL-3.0-or-later; retain third-party notices.
