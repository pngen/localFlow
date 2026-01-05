from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
import time


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowEvent:
    id: str
    timestamp: float
    type: str
    data: Dict[str, Any]


@dataclass
class WorkflowInstance:
    id: str
    name: str
    status: WorkflowStatus
    events: List[WorkflowEvent]
    last_replay_index: int

    def __post_init__(self):
        if not self.events:
            self.events = []
        self.last_replay_index = 0


class WorkflowEngine:
    def __init__(self):
        self.instances: Dict[str, WorkflowInstance] = {}
        self.event_log: List[WorkflowEvent] = []

    def create_workflow(self, name: str) -> WorkflowInstance:
        workflow_id = str(uuid.uuid4())
        instance = WorkflowInstance(
            id=workflow_id,
            name=name,
            status=WorkflowStatus.PENDING,
            events=[],
            last_replay_index=0
        )
        self.instances[workflow_id] = instance
        return instance

    def record_event(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> WorkflowEvent:
        instance = self.instances.get(workflow_id)
        if not instance:
            raise ValueError(f"Workflow {workflow_id} not found")

        event = WorkflowEvent(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            type=event_type,
            data=data
        )
        
        instance.events.append(event)
        self.event_log.append(event)
        return event

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        return self.instances.get(workflow_id)

    def update_status(self, workflow_id: str, status: WorkflowStatus):
        instance = self.instances.get(workflow_id)
        if not instance:
            raise ValueError(f"Workflow {workflow_id} not found")
        instance.status = status