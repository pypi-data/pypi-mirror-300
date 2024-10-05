from enum import Enum
from typing import Callable, Coroutine, Any

from diamond_shovel.plugins import PluginInitContext


class WorkerScope(Enum):
    INFO_COLLECTION = "info_collection"
    VULNERABILITY_SCAN = "vulnerability_scan"
    REPORT_GENERATION = "report_generation"


TaskContext = {}


class WorkerPool:
    def register_worker(self, plugin_ctx: PluginInitContext, worker: Callable[[TaskContext], Coroutine[Any, Any, Any]]):
        ...

pools: dict[str, WorkerPool] = {}
