# Routpost Plugin: Example Transformer

A standalone transformer plugin for [Routpost](https://github.com/DionisiuBrovka/routpost). Platform: Routpost post text. It implements JSON-RPC protocol v1 over newline-delimited stdio.

## Capabilities

| Source | Transformer | Destination |
| --- | --- | --- |
| No | Yes | No |

## Requirements

Python 3.11+, uv, and Git. No social network account is required.

## Install in Routpost

In **Plugins**, inspect and install `https://github.com/DionisiuBrovka/routpost-plugin-example-transformer` from a reviewed branch or tag. The public HTTPS URL must match `plugin.repository` exactly. Routpost clones the package and runs `uv sync --locked --no-dev`; no sibling core checkout is required. The small Routpost Python SDK v1 helper is bundled under `src/routpost_sdk/` and sourced from [the core SDK](https://github.com/DionisiuBrovka/routpost/tree/main/sdk/python).

## Configure and use

Add a transformer step with an optional `suffix` string. The plugin returns a new post with that suffix appended to its text.

For a post containing `Hello` and suffix `!`, `transform.run` returns text `Hello!`. The input post is not mutated.

Configuration JSON Schemas live in `schemas/`. Do not put credentials in a repository, logs, or a public Issue.

## Develop and test

```bash
uv sync --locked --no-dev
python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
```

With a Routpost core checkout, run `python3 ../routpost/tests/plugin_conformance.py .` from this directory to validate the manifest, schemas, process startup, handshake, capabilities, and shutdown. Tests mock network calls; they require no live credentials. stdout is reserved for JSON-RPC; diagnostics go to stderr. See [CONTRIBUTING.md](CONTRIBUTING.md) and [the protocol](https://github.com/DionisiuBrovka/routpost/blob/main/specs/plugin-rpc.md).

## License

[GNU GPL version 3 or later](LICENSE), SPDX `GPL-3.0-or-later`. The bundled SDK helper is covered by the same license. Third-party dependencies keep their own copyrights and licenses.
