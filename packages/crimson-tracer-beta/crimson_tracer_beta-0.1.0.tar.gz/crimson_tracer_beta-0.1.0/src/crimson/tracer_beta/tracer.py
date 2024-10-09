import sys
from types import FrameType
from typing import Optional, Callable, Any, List, Dict, Literal
from dataclasses import dataclass, field


@dataclass
class TraceEvent:
    function: str
    filename: str
    lineno: int
    event: Literal["call", "line", "return"]
    arg: Any | None
    level: int
    locals: Dict[str, Any] = field(default_factory=dict)


class TraceManager:
    traces: Dict[str, List[TraceEvent]] = {}
    current_trace_name: Optional[str] = None
    stack_count: int = -1
    frame_filter: Callable[[FrameType], bool] = lambda frame: True

    @classmethod
    def set_frame_filter(cls, filter_func: Callable[[FrameType], bool]):
        cls.frame_filter = filter_func

    @classmethod
    def tracer(cls, frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
        if cls.frame_filter(frame):
            if event == "call":
                cls.stack_count += 1
                trace_event = cls.generate_trace_event(frame, event, arg)
                cls.traces[cls.current_trace_name].append(trace_event)
            elif event == "line":
                trace_event = cls.generate_trace_event(frame, event, arg)
                cls.traces[cls.current_trace_name].append(trace_event)
            elif event == "return":
                trace_event = cls.generate_trace_event(frame, event, arg)
                cls.traces[cls.current_trace_name].append(trace_event)
                cls.stack_count -= 1
        return cls.tracer

    @classmethod
    def run_trace(cls, func: Callable, name: Optional[str] = None):
        if name is None:
            name = func.__name__

        cls.current_trace_name = name
        cls.traces[name] = []
        cls.stack_count = -1

        sys.settrace(cls.tracer)
        result = func()
        sys.settrace(None)

        cls.current_trace_name = None
        return result

    @classmethod
    def get_trace(cls, name: str) -> List[TraceEvent]:
        return cls.traces.get(name, [])

    @classmethod
    def generate_trace_event(cls, frame: FrameType, event: str, arg: Any):
        trace_event = TraceEvent(
            function=frame.f_code.co_name,
            filename=frame.f_code.co_filename,
            lineno=frame.f_lineno,
            event=event,
            arg=arg,
            level=cls.stack_count,
            locals=frame.f_locals if event == "call" else {},
        )
        return trace_event
