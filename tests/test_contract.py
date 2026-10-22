"""Standalone manifest, schema, and process contract checks."""
import json
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_manifest_schemas_and_rpc(self):
        manifest = tomllib.loads((ROOT / "plugin.toml").read_text())
        info = manifest["plugin"]
        self.assertEqual(info["protocol"], 1)
        self.assertEqual(info["license"], "GPL-3.0-or-later")
        self.assertTrue(info["repository"].startswith("https://github.com/"))
        capabilities = {key for key, enabled in manifest["capabilities"].items() if enabled}
        self.assertTrue(capabilities)
        for key, relative in manifest.get("config", {}).items():
            if key.endswith("_schema"):
                path = (ROOT / relative).resolve()
                self.assertTrue(path.is_relative_to(ROOT))
                schema = json.loads(path.read_text())
                self.assertEqual(schema["type"], "object")
        entry = (ROOT / manifest["runtime"]["entrypoint"]).resolve()
        self.assertTrue(entry.is_relative_to(ROOT))
        process = subprocess.Popen([sys.executable, str(entry)], cwd=ROOT, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            def call(method, params=None):
                process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": method, "method": method,
                                                "params": params or {}}) + "\n")
                process.stdin.flush()
                return json.loads(process.stdout.readline())
            initialized = call("plugin.initialize", {"protocol_version": 1})["result"]
            self.assertEqual(initialized["plugin_id"], info["id"])
            self.assertEqual(set(initialized["capabilities"]), capabilities)
            self.assertEqual(call("plugin.describe")["result"]["plugin_id"], info["id"])
            self.assertEqual(call("plugin.health")["result"]["status"], "ok")
            self.assertEqual(call("unknown.method")["error"]["code"], -32601)
            self.assertTrue(call("plugin.shutdown")["result"]["ok"])
            self.assertEqual(process.wait(timeout=5), 0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()
