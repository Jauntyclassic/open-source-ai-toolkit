import unittest
from promptcheck import inspect_prompt

class InspectPromptTests(unittest.TestCase):
    def test_counts_basic_text(self):
        result = inspect_prompt("hello world")
        self.assertEqual(result["characters"], 11)
        self.assertEqual(result["words"], 2)
        self.assertEqual(result["estimated_tokens"], 3)
        self.assertFalse(result["empty"])

    def test_empty_and_whitespace(self):
        self.assertTrue(inspect_prompt(" \n\t")["empty"])

    def test_flags_key_like_value(self):
        result = inspect_prompt("key: sk-" + "A" * 24)
        self.assertTrue(any(x["type"] == "OpenAI-style key"
                            for x in result["possible_credentials"]))

    def test_no_finding_for_ordinary_text(self):
        self.assertEqual(inspect_prompt("Write a helpful summary")["possible_credentials"], [])

if __name__ == "__main__":
    unittest.main()
