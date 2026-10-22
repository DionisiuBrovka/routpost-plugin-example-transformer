import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
spec = importlib.util.spec_from_file_location("plugin_main", ROOT / "src/main.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TransformerTests(unittest.TestCase):
    def test_adds_suffix_without_mutating_input(self):
        post = {"text": "hello", "attachments": []}
        result = module.transform({"post": post, "settings": {"suffix": "!"}})
        self.assertEqual(result["post"]["text"], "hello!")
        self.assertEqual(post["text"], "hello")
