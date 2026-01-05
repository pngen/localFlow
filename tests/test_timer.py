import unittest
from unittest.mock import patch
import time
from localflow.timers.scheduler import TimerScheduler
from localflow.core.workflow import WorkflowEngine


class TestTimerScheduler(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine()
        self.scheduler = TimerScheduler(self.engine)

    def test_schedule_timer(self):
        timer = self.scheduler.schedule_timer("test_workflow", 10)
        self.assertIsNotNone(timer.id)
        self.assertEqual(timer.workflow_id, "test_workflow")
        self.assertEqual(timer.duration, 10)

    @patch('time.time')
    def test_get_ready_timers(self, mock_time):
        # Set up a timer that should be ready
        mock_time.return_value = 100
        timer1 = self.scheduler.schedule_timer("workflow1", 5)
        
        # Set time so timer is ready
        mock_time.return_value = 106
        
        ready_timers = self.scheduler.get_ready_timers()
        self.assertEqual(len(ready_timers), 1)
        self.assertEqual(ready_timers[0].id, timer1.id)

    def test_remove_timer(self):
        timer = self.scheduler.schedule_timer("test_workflow", 10)
        self.scheduler.remove_timer(timer.id)
        ready_timers = self.scheduler.get_ready_timers()
        self.assertEqual(len(ready_timers), 0)


if __name__ == '__main__':
    unittest.main()