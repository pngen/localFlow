import unittest
import tempfile
import os
from localflow.core.workflow import WorkflowEngine, WorkflowStatus, WorkflowEvent
from localflow.state.persistence import StatePersistence


class TestStatePersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = StatePersistence(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_workflow(self):
        engine = WorkflowEngine()
        workflow = engine.create_workflow("test_workflow")
        
        # Add some events
        engine.record_event(workflow.id, "TestEvent", {"key": "value"})
        
        # Save and reload
        self.persistence.save_workflow(workflow)
        loaded_workflow = self.persistence.load_workflow(workflow.id)
        
        self.assertEqual(loaded_workflow.name, "test_workflow")
        self.assertEqual(len(loaded_workflow.events), 1)
        self.assertEqual(loaded_workflow.events[0].type, "TestEvent")

    def test_save_and_load_event_log(self):
        engine = WorkflowEngine()
        workflow = engine.create_workflow("test_workflow")
        
        # Add some events
        engine.record_event(workflow.id, "Event1", {"key": "value1"})
        engine.record_event(workflow.id, "Event2", {"key": "value2"})
        
        # Save event log
        self.persistence.save_event_log(engine.event_log)
        
        # Load event log
        loaded_events = self.persistence.load_event_log()
        self.assertEqual(len(loaded_events), 2)
        self.assertEqual(loaded_events[0].type, "Event1")
        self.assertEqual(loaded_events[1].type, "Event2")


if __name__ == '__main__':
    unittest.main()