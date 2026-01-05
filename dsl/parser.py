import re
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class WorkflowStep:
    type: str  # "step", "wait"
    name: str
    duration: Optional[int] = None  # for wait steps


class WorkflowParser:
    def __init__(self):
        self.workflow_pattern = re.compile(
            r"workflow\s+(\w+)\s*{([^}]*)}",
            re.DOTALL
        )
        self.step_pattern = re.compile(r"step\s+(\w+);")
        self.wait_pattern = re.compile(r"wait\s+(\d+h|\d+m|\d+s)")

    def parse(self, source: str) -> Tuple[str, List[WorkflowStep]]:
        match = self.workflow_pattern.search(source)
        if not match:
            raise ValueError("Invalid workflow syntax")

        name = match.group(1)
        body = match.group(2)

        steps = []
        step_matches = self.step_pattern.findall(body)
        for step_name in step_matches:
            steps.append(WorkflowStep(type="step", name=step_name))

        wait_matches = self.wait_pattern.findall(body)
        for wait_str in wait_matches:
            duration = self._parse_duration(wait_str)
            steps.append(WorkflowStep(type="wait", name="", duration=duration))

        return name, steps

    def _parse_duration(self, duration_str: str) -> int:
        if duration_str.endswith('h'):
            return int(duration_str[:-1]) * 3600
        elif duration_str.endswith('m'):
            return int(duration_str[:-1]) * 60
        elif duration_str.endswith('s'):
            return int(duration_str[:-1])
        else:
            raise ValueError(f"Unknown duration format: {duration_str}")