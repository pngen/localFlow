import unittest
from unittest.mock import patch
from localflow.activities.runner import ActivityRunner, ActivityResult


class TestActivityRunner(unittest.TestCase):
    def setUp(self):
        self.runner = ActivityRunner()

    def test_register_and_run_activity(self):
        def sample_activity():
            return "activity result"
        
        self.runner.register_activity("sample", sample_activity)
        result = self.runner.run_activity("sample")
        
        self.assertTrue(result.success)
        self.assertEqual(result.output, "activity result")

    def test_run_nonexistent_activity(self):
        with self.assertRaises(ValueError):
            self.runner.run_activity("nonexistent")

    @patch('subprocess.run')
    def test_run_activity_subprocess_success(self, mock_run):
        mock_run.return_value = type('MockResult', (), {
            'returncode': 0,
            'stdout': 'output',
            'stderr': ''
        })()
        
        result = self.runner.run_activity_subprocess("test_activity")
        self.assertTrue(result.success)
        self.assertEqual(result.output, "output")

    @patch('subprocess.run')
    def test_run_activity_subprocess_failure(self, mock_run):
        mock_run.return_value = type('MockResult', (), {
            'returncode': 1,
            'stdout': '',
            'stderr': 'error'
        })()
        
        result = self.runner.run_activity_subprocess("test_activity")
        self.assertFalse(result.success)
        self.assertEqual(result.error, "error")


if __name__ == '__main__':
    unittest.main()