import configparser

from diamond_shovel.function.task import WorkerPool


class Event:
    ...

class DiamondShovelInitEvent(Event):
    config: configparser.ConfigParser
    daemon: bool
    ...

class WorkerPoolInitEvent(Event):
    pool: WorkerPool
    ...

def register_event(init_ctx, evt_class, handler):
    ...

def call_event(evt):
    ...
