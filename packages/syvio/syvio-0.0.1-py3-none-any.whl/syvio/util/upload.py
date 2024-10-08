import json
import os
from pathlib import Path
import subprocess
import typer
from typing_extensions import Annotated

from syvio.util import panic
from syvio.util.cli import APP


def upload(
    file: Path,
    remote: str | None = None,
    cloudflare: bool = True,
):
    if remote is None:
        remote = os.environ.get("SYVIO_UPLOAD_REMOTE")
    if remote is None:
        panic("Failed to upload trace file: Env var SYVIO_UPLOAD_REMOTE is not set")

    remote = remote.strip()
    host = (
        remote.removeprefix("http://").removeprefix("https://").rstrip("/").lstrip("/")
    )
    # Add default endpoint
    if "?" not in host and not host.endswith("/"):
        # remote only contains the hostname, append the default endpoint
        remote = remote.rstrip("/") + "/api/trace"
    # Add scheme if missing
    if not remote.startswith("http://") and not remote.startswith("https://"):
        remote = f"https://{remote}"
    # Construct command
    command = ["curl", remote, "-F", f"file=@{file}"]
    if cloudflare:
        command = ["cloudflared", "access", *command]
    # Run command
    result = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        panic(f"Failed to upload file")
    data = json.loads(result.stdout)
    url = data.get("url")
    print(f"Uploaded {file} to {url}")
