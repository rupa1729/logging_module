import os
import unittest
from datetime import datetime
from unittest.mock import patch
from log_component import LogComponent

class TestLogComponent(unittest.TestCase):
    def setUp(self):
        self.log_directory = "./logs"
        os.makedirs(self.log_directory, exist_ok=True)
        self.log_component = LogComponent(self.log_directory)

    def tearDown(self):
        self.log_component.stop(wait=True)
        log_files = os.listdir(self.log_directory)
        for file in log_files:
            os.remove(os.path.join(self.log_directory, file))
        os.rmdir(self.log_directory)

    def test_write_logs(self):
        message = "This is a dummy message"
        self.log_component.write(message)
        self.log_component.stop(wait=True)

        log_files = os.listdir(self.log_directory)
        self.assertEqual(len(log_files), 1)

        with open(os.path.join(self.log_directory, log_files[0]), "r") as file:
            log_contents = file.read()
            self.assertIn(message, log_contents)

    def test_midnight_rollover(self):
        # Patching datetime.now to simulate midnight rollover
        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 23, 59, 59)
            self.log_component.write("Log before midnight -1")

            mock_datetime.now.return_value = datetime(2023, 1, 2, 0, 0, 1)
            self.log_component.write("Log after midnight -1")

            self.log_component.stop(wait=True)

        log_files = os.listdir(self.log_directory)
        self.assertEqual(len(log_files), 2)

    def test_stop_behavior(self):
        self.log_component.write("Log 1")
        self.log_component.write("Log 2")
        self.log_component.stop(wait=False)

        log_files = os.listdir(self.log_directory)
        self.assertEqual(len(log_files), 1)

        self.log_component.write("Log 3")
        self.log_component.stop(wait=True)

        with open(os.path.join(self.log_directory, log_files[0]), "r") as file:
            log_contents = file.read()
            self.assertIn("Log 1", log_contents)
            self.assertIn("Log 2", log_contents)
            self.assertIn("Log 3", log_contents)

if __name__ == "__main__":
    unittest.main()
