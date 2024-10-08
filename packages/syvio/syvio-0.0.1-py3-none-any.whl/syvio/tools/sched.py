from pathlib import Path
from typing import override
import typer
from typing_extensions import Annotated
from dataclasses import dataclass

from syvio.util import cli
from syvio.util.cli import APP
from syvio.util.trace_runner import BaseTraceRunner, PerfettoEvent, BPFTraceResult
import shortuuid


SCRIPT_PATH = Path(__file__).parent / "sched.bt"


@dataclass
class SwitchEvent:
    nsec: int
    prev_tid: int
    next_tid: int
    queue_cpu: int
    queue_nsec: int


@dataclass
class TaskInfo:
    tid: int
    pid: int
    uid: int
    gid: int
    comm: str

    def __post_init__(self):
        if self.tid == 0 and self.comm.startswith("swapper/"):
            self.comm = "swapper"

    def is_swapper(self):
        return self.comm == "swapper" and self.tid == 0


class Sched(BaseTraceRunner):
    def __init__(
        self,
        duration: int | None,
        no_swapper: bool = True,
        plot_runqlat: bool = False,
        plot_timeslice: bool = False,
    ):
        super().__init__(
            name="sched",
            script=SCRIPT_PATH,
            args=[f"{0 if  no_swapper else 1}", f"{ duration or 0}"],
        )
        self.no_swapper = no_swapper
        self.plot_runqlat = plot_runqlat
        self.plot_timeslice = plot_timeslice

    def __process_output(self, result: BPFTraceResult):
        switch_events: dict[int, list[SwitchEvent]] = {}
        task_info: dict[int, TaskInfo] = {}
        for key, value in result.maps.items():
            if key == "@sched":
                for k, v in value.items():
                    [cpu, nsec] = [int(x) for x in k.split(",")]
                    [prev_tid, next_tid, qcpu, qtime] = v
                    switch_events.setdefault(cpu, []).append(
                        SwitchEvent(
                            nsec=nsec,
                            prev_tid=prev_tid,
                            next_tid=next_tid,
                            queue_cpu=qcpu,
                            queue_nsec=qtime,
                        )
                    )
            elif key == "@tasks":
                for k, v in value.items():
                    tid = int(k)
                    [_, pid, uid, gid, comm] = v
                    task_info[tid] = TaskInfo(
                        tid=tid, pid=pid, uid=uid, gid=gid, comm=comm
                    )
        return switch_events, task_info

    def __generate_perfetto_events(
        self,
        switch_events: dict[int, list[SwitchEvent]],
        task_info: dict[int, TaskInfo],
    ):
        perfetto_events: list[PerfettoEvent] = []

        # intervals: cpu -> (tid, start, end)
        @dataclass
        class Interval:
            tid: int
            start: int
            end: int
            qcpu: int | None
            qtime: int | None

        intervals: dict[int, list[Interval]] = {}
        for cpu, events in switch_events.items():
            ivals = intervals.setdefault(cpu, [])
            for e in events:
                # Update previous interval
                if len(ivals) > 0 and ivals[-1].tid == e.prev_tid:
                    ivals[-1].end = e.nsec
                # Create new interval
                qtime = e.queue_nsec if e.queue_nsec != 0 else None
                qcpu = e.queue_cpu if e.queue_cpu != 0 else None
                ivals.append(
                    Interval(
                        tid=e.next_tid, start=e.nsec, end=-1, qcpu=qcpu, qtime=qtime
                    )
                )
        # Remove incomplete intervals or swapper intervals
        for cpu in list(intervals.keys()):
            intervals[cpu] = [
                i
                for i in intervals[cpu]
                if i.end != -1
                and i.tid in task_info
                and (not self.no_swapper or not task_info[i.tid].is_swapper())
            ]
        # Create TraceEvents
        for cpu, ivals in intervals.items():
            for ival in ivals:
                task = task_info[ival.tid]
                dur = ival.end - ival.start
                lat = (
                    (ival.start - ival.qtime)
                    if ival.qtime is not None and ival.qtime != 0
                    else None
                )
                meta = {
                    "uid": task.uid,
                    "pid": task.pid,
                    "tid": task.tid,
                    "gid": task.gid,
                    "qlat_ns": lat,
                    "uuid": shortuuid.ShortUUID().random(length=12),
                }
                if self._user_command_pid and task.pid == self._user_command_pid:
                    meta["primary"] = True
                if lat is not None and ival.qtime is not None and ival.qcpu is not None:
                    perfetto_events.append(
                        PerfettoEvent(
                            name=task.comm + ":queue",
                            ph="X",
                            id=meta["uuid"],
                            tid=ival.qcpu,
                            pid=0,
                            ts=float(ival.qtime) / 1000.0,
                            dur=float(lat) / 1000.0,
                            args=meta,
                        )
                    )
                perfetto_events.append(
                    PerfettoEvent(
                        name=task.comm,
                        ph="X",
                        id=meta["uuid"],
                        tid=cpu,
                        pid=0,
                        ts=float(ival.start) / 1000.0,
                        dur=float(dur) / 1000.0,
                        args=meta,
                    )
                )
        # Inject processor names
        perfetto_events.append(
            PerfettoEvent(
                ph="M",
                name="process_name",
                pid=0,
                ts=0,
                tid=0,
                args={"name": "Task Scheduling"},
            )
        )
        for cpu in list(intervals.keys()):
            perfetto_events.append(
                PerfettoEvent(
                    ph="M",
                    name="thread_name",
                    pid=0,
                    ts=0,
                    tid=cpu,
                    args={"name": f"CPU"},
                )
            )
        return perfetto_events

    @override
    def process(self, result: BPFTraceResult) -> list[PerfettoEvent]:
        switch_events, task_info = self.__process_output(result)
        perfetto_events = self.__generate_perfetto_events(switch_events, task_info)
        self.perfetto_events = perfetto_events
        return perfetto_events

    @override
    def plot_graphs(self):
        if self.plot_runqlat:
            runqlat = [
                float(e.args["qlat_ns"])
                for e in self.perfetto_events
                if e.args.get("qlat_ns") and not e.name.endswith(":queue")
            ]
            cli.plot_hist("runqlat (ns)", runqlat)
        if self.plot_timeslice:
            slice_time = [
                float(e.dur * 1000)
                for e in self.perfetto_events
                if not e.name.endswith(":queue") and e.dur is not None
            ]
            cli.plot_hist("timeslice (ns)", slice_time)


@APP.command("sched", help="Trace task scheduling events.")
def main(
    # pid: Annotated[int | None, typer.Argument(help="The target process PID.")] = None,
    duration: Annotated[
        int,
        typer.Option(
            "-D", "--duration", help="The duration to trace, in milliseconds."
        ),
    ] = 1000,
    command: Annotated[
        list[str] | None,
        typer.Argument(
            metavar="[-- COMMAND [ARG] ...]", help="The optional command to run."
        ),
    ] = None,
    upload: Annotated[
        bool,
        typer.Option(
            "-U",
            "--upload",
            help="Upload the trace to a cloudfetto server.",
            is_flag=True,
        ),
    ] = False,
    runqlat: Annotated[
        bool,
        typer.Option(
            "--runqlat",
            help="Plot the runqlat histogram.",
            is_flag=True,
        ),
    ] = False,
    timeslice: Annotated[
        bool,
        typer.Option(
            "--timeslice",
            help="Plot the timeslice histogram.",
            is_flag=True,
        ),
    ] = False,
):
    runner = Sched(
        duration=None if command else duration,
        plot_runqlat=runqlat,
        plot_timeslice=timeslice,
    )
    runner.trace(user_command=command, upload=upload)
