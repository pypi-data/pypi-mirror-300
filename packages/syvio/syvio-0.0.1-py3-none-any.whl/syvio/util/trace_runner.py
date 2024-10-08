import asyncio
from datetime import datetime
from pathlib import Path
import abc

from syvio.util import bpftrace
from syvio.util import perfetto
from syvio.util.perfetto import PerfettoEvent
from syvio.util.bpftrace import BPFTraceResult
import syvio.util.upload as upload_utils


class BaseTraceRunner(abc.ABC):
    def __init__(self, name: str, script: str | Path, args: list[str]):
        self._name = name
        self._script = script
        self._args = args
        self._start_time = datetime.now()
        self._user_command_pid: int | None = None

    async def __run_user_command(self, command: list[str]) -> int:
        print("---\n")
        proc = await asyncio.create_subprocess_exec(*command)
        await proc.wait()
        self._user_command_pid = proc.pid
        print("\n---")
        return proc.pid

    async def _start_tracing(
        self,
        script: str | Path,
        args: list[str],
        user_command: list[str] | None = None,
    ):
        wait = 1 if user_command else 0
        proc = await bpftrace.run_async(script, args=args, wait=wait)
        if user_command:
            await self.__run_user_command(command=user_command)
            await proc.kill()
        result = await proc.communicate()
        return result

    @abc.abstractmethod
    def process(self, result: BPFTraceResult) -> list[PerfettoEvent]:
        raise NotImplementedError()

    def plot_graphs(self):
        pass

    async def __trace_impl(self, user_command: list[str] | None, upload: bool):
        script = self._script
        args = self._args
        print("Start recording ...")
        raw_result = await self._start_tracing(
            script, args=args, user_command=user_command
        )
        print(f"Finished recording. Processing ...")
        perfetto_events = self.process(result=raw_result)
        filename = perfetto.dump_trace_events(
            self._name, self._start_time, perfetto_events
        )
        print(f"Recorded {len(perfetto_events)} events to {filename}")
        if upload:
            upload_utils.upload(Path(filename))

        self.plot_graphs()

    def trace(self, user_command: list[str] | None = None, upload: bool = False):
        asyncio.run(self.__trace_impl(user_command=user_command, upload=upload))
