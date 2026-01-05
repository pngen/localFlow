from typing import List, Dict, Any, Callable
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ..core.workflow import WorkflowEngine, WorkflowInstance, WorkflowStatus
from ..dsl.parser import WorkflowParser, WorkflowStep


class ActivityExecutionError(Exception):
    pass


class WorkflowExecutor:
    def __init__(self, workflow_engine: WorkflowEngine, activity_runner: Callable):
        self.workflow_engine = workflow_engine
        self.activity_runner = activity_runner
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def execute_workflow(self, workflow_id: str, steps: List[WorkflowStep]):
        instance = self.workflow_engine.get_workflow(workflow_id)
        if not instance:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Mark as running
        self.workflow_engine.update_status(workflow_id, WorkflowStatus.RUNNING)

        for step in steps:
            try:
                if step.type == "step":
                    await self._execute_activity(workflow_id, step.name)
                elif step.type == "wait":
                    await self._schedule_timer(workflow_id, step.duration)
            except Exception as e:
                self.workflow_engine.update_status(workflow_id, WorkflowStatus.FAILED)
                raise ActivityExecutionError(f"Failed to execute step {step.name}: {str(e)}")

        self.workflow_engine.update_status(workflow_id, WorkflowStatus.COMPLETED)

    async def _execute_activity(self, workflow_id: str, activity_name: str):
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self.activity_runner,
                activity_name
            )
            self.workflow_engine.record_event(
                workflow_id,
                "ActivityCompleted",
                {"activity": activity_name, "result": result}
            )
        except Exception as e:
            self.workflow_engine.record_event(
                workflow_id,
                "ActivityFailed",
                {"activity": activity_name, "error": str(e)}
            )
            raise

    async def _schedule_timer(self, workflow_id: str, duration_seconds: int):
        # Simulate timer scheduling
        await asyncio.sleep(duration_seconds)
        self.workflow_engine.record_event(
            workflow_id,
            "TimerFired",
            {"duration": duration_seconds}
        )