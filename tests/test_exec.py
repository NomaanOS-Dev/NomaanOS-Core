import unittest
from src.engine import NoseExec

class TestNoseExec(unittest.TestCase):
    def test_allowed_command(self):
        engine = NoseExec(["echo"])
        result = engine.execute(["echo", "test"])
        self.assertEqual(result["status"], "SUCCESS")

    def test_blocked_command(self):
        engine = NoseExec(["echo"])
        result = engine.execute(["rm", "-rf", "/"])
        self.assertEqual(result["status"], "BLOCKED")

if __name__ == "__main__":
   unittest.main()
