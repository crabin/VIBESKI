import unittest
import tempfile
import os
from datetime import datetime
from database.manager import DatabaseManager
from database.models import Conversation, UserConfig


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for the database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.manager = DatabaseManager(db_path=self.db_path)

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.db_path):
            try:
                os.unlink(self.db_path)
            except PermissionError:
                pass

    def test_init_database(self):
        # Verify tables are created
        with self.manager._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("conversations", tables)
            self.assertIn("user_configs", tables)
            # Domain tables should NOT exist
            self.assertNotIn("crawler_tasks", tables)
            self.assertNotIn("attack_tasks", tables)
            self.assertNotIn("scan_results", tables)

    def test_conversation_operations(self):
        # Create a conversation
        conv = Conversation(
            agent_type="test_agent",
            user_message="Hello",
            assistant_message="Hi",
            session_id="session_1"
        )

        # Save
        conv_id = self.manager.save_conversation(conv)
        self.assertIsNotNone(conv_id)

        # Get
        conversations = self.manager.get_conversations(session_id="session_1")
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0].user_message, "Hello")

        # Delete
        count = self.manager.delete_conversations(session_id="session_1")
        self.assertEqual(count, 1)
        conversations = self.manager.get_conversations(session_id="session_1")
        self.assertEqual(len(conversations), 0)

    def test_config_operations(self):
        config = UserConfig(key="test_key", value="test_value")

        # Save
        self.manager.save_config(config)

        # Get
        saved_config = self.manager.get_config("test_key")
        self.assertIsNotNone(saved_config)
        self.assertEqual(saved_config.value, "test_value")

        # Update
        config.value = "new_value"
        self.manager.save_config(config)
        updated_config = self.manager.get_config("test_key")
        self.assertEqual(updated_config.value, "new_value")

        # Delete
        self.manager.delete_config("test_key")
        self.assertIsNone(self.manager.get_config("test_key"))

    def test_stats_no_domain_tables(self):
        """Verify get_stats doesn't include domain-specific tables."""
        stats = self.manager.get_stats()
        self.assertIn("conversations", stats)
        # Domain stats should NOT exist
        self.assertNotIn("crawler_tasks", stats)


if __name__ == "__main__":
    unittest.main()
