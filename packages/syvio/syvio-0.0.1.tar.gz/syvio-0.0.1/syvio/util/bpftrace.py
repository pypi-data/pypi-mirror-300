from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
import asyncio
import time


def installed():
    """Check if bpftrace is installed"""
    result = subprocess.run(
        ["bpftrace", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.returncode == 0


def __bpftrace_requires_sudo():
    """Check if bpftrace is in sudoers"""
    # Run a test command and collect ret code, stderr, and stdout
    result = subprocess.run(
        ["bpftrace", "-l", "tracepoint:sched:sched_switch"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stderr = result.stderr.decode()
    return result.returncode == 1 and "ERROR:" in stderr and "root" in stderr


__BPFTRACE_BIN = "bpftrace"
__BPFTRACE_REQUIRES_SUDO = __bpftrace_requires_sudo()


@dataclass
class HistogramEntry:
    min: int
    max: int
    count: int


@dataclass
class Histogram:
    name: str
    entries: list[HistogramEntry]


@dataclass
class BPFTraceResult:
    maps: dict[str, dict[str, Any]]
    hists: dict[str, Histogram]


def run(script: str | Path, args: list[str]):
    from . import panic

    if not Path(script).exists():
        panic(f"bpftrace script does not exist: {script}")

    command: list[str] = [__BPFTRACE_BIN, "-f", "json", str(script), *args]
    if __BPFTRACE_REQUIRES_SUDO:
        command.insert(0, "sudo")
    with tempfile.NamedTemporaryFile() as out:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            panic("Failed to run bpftrace")
    return parse_result(result.stdout)


def parse_result(output: str) -> BPFTraceResult:
    result = BPFTraceResult(maps={}, hists={})
    for row in output.split("\n"):
        if not row.strip():
            continue
        data = json.loads(row.strip())
        if data["type"] == "lhist":
            for key, value in data["data"].items():
                if len(value) > 0:
                    result.hists[key] = Histogram(
                        name=key,
                        entries=[
                            HistogramEntry(
                                min=item["min"], max=item["max"], count=item["count"]
                            )
                            for item in value
                        ],
                    )
        if data["type"] == "map":
            for key, value in data["data"].items():
                result.maps[key] = value
    return result


class AsyncBPFTraceProcess:
    def __init__(self, proc: asyncio.subprocess.Process):
        self.__proc = proc
        self.__killed = False
        self.__created = time.time_ns()

    async def kill(self):
        assert not self.__killed
        # if process is already terminated, return
        if self.__proc.returncode is not None:
            return
        # don't terminate too early
        while time.time_ns() - self.__created < 1e9:
            await asyncio.sleep(0.1)
        # terminate the process
        self.__proc.send_signal(2)  # SIGINT
        self.__killed = True

    async def communicate(self):
        from . import panic

        stdout, _ = await self.__proc.communicate()

        ret = None if self.__killed else self.__proc.returncode
        if ret != 0 and ret is not None:
            panic(f"Failed to run bpftrace: {self.__proc.returncode}")

        stdout = stdout.decode()
        return parse_result(stdout)


async def __get_sudo_permission():
    from . import panic

    proc = await asyncio.create_subprocess_exec(
        "sudo", "ls", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()
    if proc.returncode != 0:
        panic("Failed to acquire sudo permission")


async def run_async(script: str | Path, args: list[str], wait: float = 1):
    from . import panic

    if not Path(script).exists():
        panic(f"bpftrace script does not exist: {script}")

    command: list[str] = [__BPFTRACE_BIN, "-f", "json", str(script), *args]
    if __BPFTRACE_REQUIRES_SUDO:
        command.insert(0, "sudo")
        # Get sudo permission once
        await __get_sudo_permission()
    proc = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE
    )
    # wait for 1s to make sure the process is running
    await asyncio.sleep(wait)
    return AsyncBPFTraceProcess(proc)
