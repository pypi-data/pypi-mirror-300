from pathlib import Path
import typer
from typing_extensions import Annotated

from syvio.util.cli import APP
import syvio.util.upload as upload_utils


@APP.command(
    "upload",
    help="Upload a file to the a cloudfetto server. Please see https://github.com/wenyuzhao/cloudfetto for more information.",
)
def main(
    file: Annotated[
        Path,
        typer.Argument(
            help="The file to upload.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    remote: Annotated[
        str,
        typer.Option(
            envvar="SYVIO_UPLOAD_REMOTE",
            help="The remote server hostname or a complete url with endpoint.",
        ),
    ],
    cloudflare: Annotated[
        bool,
        typer.Option(
            envvar="SYVIO_UPLOAD_CLOUDFLARE",
            help="Enable cloudflare access",
        ),
    ] = True,
):
    upload_utils.upload(file, remote, cloudflare)
