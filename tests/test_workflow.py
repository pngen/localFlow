import unittest
from unittest.mock import Mock, patch
from localflow.core.workflow import WorkflowEngine, WorkflowStatus, WorkflowEvent
from localflow.dsl.parser import WorkflowParser, WorkflowStep


class TestWorkflowEngine(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine()

    def test_create_workflow(self):
        workflow = self.engine.create_workflow("test_workflow")
        self.assertEqual(workflow.name, "test_workflow")
        self.assertEqual(workflow.status, WorkflowStatus.PENDING)
        self.assertEqual(len(workflow.events), 0)

    def test_record_event(self):
        workflow = self.engine.create_workflow("test_workflow")
        event = self.engine.record_event(
            workflow.id,
            "TestEvent",
            {"key": "value"}
        )
        
        self.assertEqual(len(workflow.events), 1)
        self.assertEqual(event.type, "TestEvent")
        self.assertEqual(event.data["key"], "value")

    def test_update_status(self):
        workflow = self.engine.create_workflow("test_workflow")
        self.engine.update_status(workflow.id, WorkflowStatus.RUNNING)
        self.assertEqual(workflow.status, WorkflowStatus.RUNNING)

    def test_get_workflow(self):
        workflow = self.engine.create_workflow("test_workflow")
        retrieved = self.engine.get_workflow(workflow.id)
        self.assertEqual(retrieved, workflow)

        non_existent = self.engine.get_workflow("non-existent")
        self.assertIsNone(non_existent)


class TestWorkflowParser(unittest.TestCase):
    def setUp(self):
        self.parser = WorkflowParser()

    def test_parse_simple_workflow(self):
        source = """
workflow PurchaseFlow {
    step charge_card;
    step send_email;
}
"""
        name, steps = self.parser.parse(source)
        self.assertEqual(name, "PurchaseFlow")
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0].type, "step")
        self.assertEqual(steps[0].name, "charge_card")
        self.assertEqual(steps[1].type, "step")
        self.assertEqual(steps[1].name, "send_email")

    def test_parse_workflow_with_wait(self):
        source = """
workflow PurchaseFlow {
    step charge_card;
    wait 1h;
    step send_email;
}
"""
        name, steps = self.parser.parse(source)
        self.assertEqual(name, "PurchaseFlow")
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[0].type, "step")
        self.assertEqual(steps[1].type, "wait")
        self.assertEqual(steps[1].duration, 3600)
        self.assertEqual(steps[2].type, "step")

    def test_parse_duration_units(self):
        # Test hours
        duration = self.parser._parse_duration("1h")
        self.assertEqual(duration, 3600)

        # Test minutes
        duration = self.parser._parse_duration("5m")
        self.assertEqual(duration, 300)

        # Test seconds
        duration = self.parser._parse_duration("30s")
        self.assertEqual(duration, 30)


if __name__ == '__main__':
    unittest.main()