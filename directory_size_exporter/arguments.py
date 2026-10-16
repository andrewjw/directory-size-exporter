import argparse

parser = argparse.ArgumentParser(
    description="Export directory sizes as Prometheus metrics. Uses eventual consistency to efficiently handle large directory structures."
)
parser.add_argument(
    "-q", "--quiet", action="store_true", help="don't log HTTP requests"
)
parser.add_argument(
    "--bind",
    type=str,
    nargs="?",
    default="0.0.0.0:9100",
    help="the ip address and port to bind to. Default: *:9100",
)
parser.add_argument(
    "--level",
    type=int,
    nargs="?",
    default=0,
    help="which level of directories to report on. Files above this level are ignored.",
)
parser.add_argument("directories", action="append")


def get_arguments(args):
    return parser.parse_args(args)
