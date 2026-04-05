
import unittest
from core.agents.vibeski_agent import VibeskiAgent, VIBESKI_SYSTEM_PROMPT

class TestVibeskiAgent(unittest.TestCase):
    def test_initialization(self):
        # Mocking tools if they require heavy initialization or external dependencies
        # Assuming BASIC_SECURITY_TOOLS don't crash on import/init without config
        agent = VibeskiAgent()
        self.assertEqual(agent.name, "Vibeski")
        self.assertEqual(agent.system_prompt, VIBESKI_SYSTEM_PROMPT)
        self.assertTrue(agent.auto_execute)
        self.assertGreater(len(agent.security_tools), 0)
        
        # Verify tools are loaded
        # tools list contains tool instances
        self.assertTrue(any(t for t in agent.security_tools))

if __name__ == "__main__":
    unittest.main()
