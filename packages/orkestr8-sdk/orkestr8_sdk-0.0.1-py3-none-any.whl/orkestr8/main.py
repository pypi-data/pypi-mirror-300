from argparse import ArgumentParser
import os
import dotenv 
from enum import Enum
from orkestr8.commands import update 

class Dispatch(Enum):
    TRAIN = "train"
    RUN = "run"
    UPDATE = "update"

dotenv.load_dotenv()

def parse_args():
    parser = ArgumentParser(prog="Orchkestr8 ML train runner")
    subparsers = parser.add_subparsers(dest="command",help="Invocation commands")
    train_parser = subparsers.add_parser("train" ,help="Runs the training logic only")
    train_parser.add_argument("model_module", action="store", help="The module that contains the model to run. Module MUST have a `run` method defined")
    subparsers.add_parser("run", help="Runs the data update and training logic")
    subparsers.add_parser("update", help="Runs the data update function.")
    subparsers.add_parser("stop", help="Writes to a file")
    parser.add_argument("--aws-access-key")
    parser.add_argument("--aws-secret-key")
    parser.add_argument("--aws-bucket-name")

    return parser.parse_args()

def check_env_variables():
    required_variables = ["AWS_ACCESS_KEY", "AWS_SECRET_KEY"]

    for v in required_variables:
        if not os.environ.get(v):
            raise RuntimeError(f"Improper configuration. '{v}' is not set")
        
def run(raw_command:Dispatch):
    command  = Dispatch(raw_command)
    if command == Dispatch.TRAIN:
        pass
    elif command == Dispatch.UPDATE:
        update.run()
         
def main():
    args = parse_args()
    check_env_variables()
    print("Ye args => ", args)
    run(args.command)

if __name__ == "__main__":
    main()