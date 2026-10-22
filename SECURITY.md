# Security policy

Only the current `main` branch is maintained; no stable release series has been declared.

Report vulnerabilities through [GitHub private vulnerability reporting](https://github.com/DionisiuBrovka/routpost-plugin-example-transformer/security/advisories/new). Do not put exploit details, tokens, app passwords, session cookies, encryption keys, or personal data in public Issues. If private reporting is unavailable, open a public Issue requesting a private reporting channel without disclosing the vulnerability.

Keep social network credentials in Routpost's encrypted connection storage. Never put them in plugin settings, source control, logs, or examples. Plugins execute with the server process's privileges; review their source and pin revisions before installing. Rotate any credential that may have leaked.
