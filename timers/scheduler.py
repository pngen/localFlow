import heapq
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from ..core.workflow import WorkflowEngine


@dataclass
class Timer:
    id: str
    workflow_id: str
    fire_time: float
    duration: int  # seconds


class TimerScheduler:
    def __init__(self, workflow_engine: WorkflowEngine):
        self.workflow_engine = workflow_engine
        self.timers: List[Timer] = []
        self.timer_heap: List[float] = []

    def schedule_timer(self, workflow_id: str, duration_seconds: int) -> Timer:
        fire_time = time.time() + duration_seconds
        timer = Timer(
            id=str(time.time()),
            workflow_id=workflow_id,
            fire_time=fire_time,
            duration=duration_seconds
        )
        heapq.heappush(self.timer_heap, fire_time)
        self.timers.append(timer)
        return timer

    def get_ready_timers(self) -> List[Timer]:
        now = time.time()
        ready = []
        for timer in self.timers:
            if timer.fire_time <= now:
                ready.append(timer)
        return ready

    def remove_timer(self, timer_id: str):
        self.timers = [t for t in self.timers if t.id != timer_id]
        # Rebuild heap
        self.timer_heap = [t.fire_time for t in self.timers]
        heapq.heapify(self.timer_heap)