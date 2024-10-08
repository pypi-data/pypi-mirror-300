import dotenv

dotenv.load_dotenv()

from syvio import util
from syvio.util.cli import APP


# Import all tools
from . import tools


@APP.callback()
def callback():
    if not util.bpftrace.installed():
        util.panic("bpftrace is not installed")


def main():
    APP()
