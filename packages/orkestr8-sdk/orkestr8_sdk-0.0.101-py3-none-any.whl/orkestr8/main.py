import os
from enum import Enum

import dotenv

from orkestr8.cli import parse_args
from orkestr8.commands.update import UpdateCommand


class Dispatch(Enum):
    TRAIN = "train"
    RUN = "run"
    UPDATE = "update"


dotenv.load_dotenv()


def check_env_variables(args):
    required_variables = ["AWS_ACCESS_KEY", "AWS_SECRET_KEY"]

    for v in required_variables:
        if not os.environ.get(v):
            attr = getattr(args, v.lower(), None)
            if attr is None:
                raise RuntimeError(f"Improper configuration. '{v}' is not set")
            else:
                os.environ[v] = attr


def run(args):
    command = Dispatch(args.command)
    if command == Dispatch.TRAIN:
        pass
    elif command == Dispatch.UPDATE:
        UpdateCommand.run(args)


def main():
    args = parse_args()
    check_env_variables(args)
    run(args)


if __name__ == "__main__":
    main()
