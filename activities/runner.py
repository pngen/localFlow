import subprocess
import time
import json
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ActivityResult:
    success: bool
    output: str
    error: str
    duration: float


class ActivityRunner:
    def __init__(self):
        self.activities = {}

    def register_activity(self, name: str, func):
        self.activities[name] = func

    def run_activity(self, activity_name: str, timeout_seconds: int = 30) -> ActivityResult:
        if activity_name not in self.activities:
            raise ValueError(f"Activity {activity_name} not registered")

        start_time = time.time()
        try:
            result = self.activities[activity_name]()
            duration = time.time() - start_time
            return ActivityResult(
                success=True,
                output=str(result),
                error="",
                duration=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            return ActivityResult(
                success=False,
                output="",
                error=str(e),
                duration=duration
            )

    def run_activity_subprocess(self, activity_name: str, timeout_seconds: int = 30) -> ActivityResult:
        try:
            # In a real implementation, this would call an external process
            # For now, simulate with a subprocess call
            start_time = time.time()
            
            # Simulate activity execution
            result = subprocess.run(
                ["echo", f"executed: {activity_name}"],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            
            duration = time.time() - start_time
            return ActivityResult(
                success=result.returncode == 0,
                output=result.stdout.strip(),
                error=result.stderr.strip(),
                duration=duration
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return ActivityResult(
                success=False,
                output="",
                error=f"Activity timed out after {timeout_seconds} seconds",
                duration=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            return ActivityResult(
                success=False,
                output="",
                error=str(e),
                duration=duration
            )