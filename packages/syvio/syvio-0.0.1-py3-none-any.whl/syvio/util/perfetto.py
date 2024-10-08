from dataclasses import asdict, dataclass, field
from datetime import datetime
import gzip
import json
from typing import Any, Literal


@dataclass
class PerfettoEvent:
    name: str
    """The name of the event, as displayed in Trace Viewer"""
    ph: Literal[
        "B", "E", "X", "i", "C", "b", "s", "P", "N", "M", "V", "R", "c", "(", ")"
    ]
    """
    The event type. This is a single character which changes depending on the type of event being output.

    The following table lists all event types and their associated phases:

    * **B** (begin), **E** (end): Duration events
    * **X**: Complete events
    * **i**: Instant events
    * **C**: Counter events
    * **b** (nestable start), **n** (nestable instant), **e** (nestable end): Async events
    * **s** (start), **t** (step), **f** (end): Flow events
    * **P**: Sample events
    * **N** (created), **O** (snapshot), **D** (destroyed): Object events
    * **M**: Metadata events
    * **V** (global), **v** (process): Memory dump events
    * **R**: Mark events
    * **c**: Clock sync events
    * **(**, **(**: Context events
    """
    ts: float | int
    """The tracing clock timestamp of the event. The timestamps are provided at microsecond granularity."""
    tid: int
    """The thread ID for the thread that output this event."""
    pid: int
    """The process ID for the process that output this event."""
    cat: str | None = None
    """The event categories. This is a comma separated list of categories for the event. The categories can be used to hide events in the Trace Viewer UI."""
    cname: (
        Literal[
            "black",
            "grey",
            "white",
            "yellow",
            "olive",
            "generic_work",
            "good",
            "bad",
            "terrible",
            "thread_state_uninterruptible",
            "thread_state_iowait",
            "thread_state_running",
            "thread_state_runnable",
            "thread_state_sleeping",
            "thread_state_unknown",
            "background_memory_dump",
            "light_memory_dump",
            "detailed_memory_dump",
            "vsync_highlight_color",
            "rail_response",
            "rail_animation",
            "rail_idle",
            "rail_load",
            "startup",
            "heap_dump_stack_frame",
            "heap_dump_object_type",
            "heap_dump_child_node_arrow",
            "cq_build_running",
            "cq_build_passed",
            "cq_build_failed",
            "cq_build_abandoned",
            "cq_build_attempt_runnig",
            "cq_build_attempt_passed",
            "cq_build_attempt_failed",
        ]
        | None
    ) = None
    """A fixed color name to associate with the event."""
    args: dict[str, Any] = field(default_factory=dict)
    """Any arguments provided for the event. Some of the event types have required argument fields, otherwise, you can put any information you wish in here. The arguments are displayed in Trace Viewer when you view an event in the analysis section."""

    dur: float | int | None = None
    """The duration of the event in microseconds. Required for **X** events."""
    s: Literal["g", "p", "t"] | None = None
    """The scope of the event. Required for **i** events. Possible values: global (g), process (p) and thread (t)"""
    id: str | None = None
    """Event ID"""


def dump_trace_events(name: str, time: datetime, events: list[PerfettoEvent]) -> str:
    if not name.startswith("syvio-"):
        name = f"syvio-{name}"
    if name.endswith(".json.gz"):
        name = name[:-8]
    time_str = time.strftime("%Y-%m-%d-%H%M%S")
    name = f"{name}-{time_str}.json.gz"
    trace_events = [asdict(x) for x in events]
    with gzip.open(name, "wt") as f:
        json.dump({"traceEvents": trace_events}, f)
    return name
