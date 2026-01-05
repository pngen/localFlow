import argparse
import sys
from typing import List
from ..core.workflow import WorkflowEngine, WorkflowStatus
from ..dsl.parser import WorkflowParser
from ..engine.executor import WorkflowExecutor
from ..activities.runner import ActivityRunner
from ..state.persistence import StatePersistence


class LocalFlowCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="LocalFlow - Deterministic Workflow Engine")
        self.subparsers = self.parser.add_subparsers(dest='command')
        self._setup_commands()

    def _setup_commands(self):
        # start command
        start_parser = self.subparsers.add_parser('start', help='Start a new workflow')
        start_parser.add_argument('workflow_name', help='Name of the workflow to start')

        # run command
        self.subparsers.add_parser('run', help='Run all pending workflows')

        # inspect command
        inspect_parser = self.subparsers.add_parser('inspect', help='Inspect a workflow')
        inspect_parser.add_argument('workflow_id', help='ID of the workflow to inspect')

        # history command
        history_parser = self.subparsers.add_parser('history', help='Show workflow history')
        history_parser.add_argument('workflow_id', help='ID of the workflow to show history for')

        # list command
        self.subparsers.add_parser('list', help='List all workflows')

    def run(self, args: List[str] = None):
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return

        # Initialize components
        workflow_engine = WorkflowEngine()
        parser = WorkflowParser()
        activity_runner = ActivityRunner()
        persistence = StatePersistence("./storage")

        # Setup some sample activities
        def charge_card():
            return "Card charged successfully"
        
        def send_email():
            return "Email sent successfully"
            
        def update_crm():
            return "CRM updated successfully"

        activity_runner.register_activity("charge_card", charge_card)
        activity_runner.register_activity("send_email", send_email)
        activity_runner.register_activity("update_crm", update_crm)

        executor = WorkflowExecutor(workflow_engine, activity_runner.run_activity)

        if parsed_args.command == 'start':
            workflow_name = parsed_args.workflow_name
            workflow = workflow_engine.create_workflow(workflow_name)
            persistence.save_workflow(workflow)
            print(f"Started workflow: {workflow.id}")
            
        elif parsed_args.command == 'run':
            # In a real implementation, this would process all pending workflows
            print("Running workflows...")
            
        elif parsed_args.command == 'inspect':
            workflow_id = parsed_args.workflow_id
            try:
                workflow = persistence.load_workflow(workflow_id)
                print(f"Workflow ID: {workflow.id}")
                print(f"Name: {workflow.name}")
                print(f"Status: {workflow.status.value}")
                print(f"Events: {len(workflow.events)}")
            except FileNotFoundError:
                print(f"Workflow {workflow_id} not found")
                
        elif parsed_args.command == 'history':
            workflow_id = parsed_args.workflow_id
            try:
                workflow = persistence.load_workflow(workflow_id)
                print(f"History for workflow {workflow_id}:")
                for event in workflow.events:
                    print(f"  [{event.timestamp}] {event.type}: {event.data}")
            except FileNotFoundError:
                print(f"Workflow {workflow_id} not found")
                
        elif parsed_args.command == 'list':
            # List all workflows from storage
            import os
            files = [f for f in os.listdir("./storage") if f.endswith(".json") and f != "event_log.json"]
            print("Workflows:")
            for file in files:
                workflow_id = file.replace(".json", "")
                try:
                    workflow = persistence.load_workflow(workflow_id)
                    print(f"  {workflow.id} - {workflow.name} ({workflow.status.value})")
                except Exception:
                    print(f"  {workflow_id} - [corrupted]")