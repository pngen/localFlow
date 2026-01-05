import json
import os
from typing import List, Dict, Any
from ..core.workflow import WorkflowInstance, WorkflowEvent


class StatePersistence:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def save_workflow(self, workflow: WorkflowInstance):
        path = os.path.join(self.storage_path, f"{workflow.id}.json")
        with open(path, 'w') as f:
            json.dump({
                "id": workflow.id,
                "name": workflow.name,
                "status": workflow.status.value,
                "events": [
                    {
                        "id": e.id,
                        "timestamp": e.timestamp,
                        "type": e.type,
                        "data": e.data
                    } for e in workflow.events
                ],
                "last_replay_index": workflow.last_replay_index
            }, f)

    def load_workflow(self, workflow_id: str) -> WorkflowInstance:
        path = os.path.join(self.storage_path, f"{workflow_id}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Workflow {workflow_id} not found")

        with open(path, 'r') as f:
            data = json.load(f)
            
        events = [
            WorkflowEvent(
                id=e["id"],
                timestamp=e["timestamp"],
                type=e["type"],
                data=e["data"]
            ) for e in data["events"]
        ]
        
        return WorkflowInstance(
            id=data["id"],
            name=data["name"],
            status=WorkflowStatus(data["status"]),
            events=events,
            last_replay_index=data["last_replay_index"]
        )

    def save_event_log(self, events: List[WorkflowEvent]):
        path = os.path.join(self.storage_path, "event_log.json")
        with open(path, 'w') as f:
            json.dump([
                {
                    "id": e.id,
                    "timestamp": e.timestamp,
                    "type": e.type,
                    "data": e.data
                } for e in events
            ], f)

    def load_event_log(self) -> List[WorkflowEvent]:
        path = os.path.join(self.storage_path, "event_log.json")
        if not os.path.exists(path):
            return []
            
        with open(path, 'r') as f:
            data = json.load(f)
            
        return [
            WorkflowEvent(
                id=e["id"],
                timestamp=e["timestamp"],
                type=e["type"],
                data=e["data"]
            ) for e in data
        ]