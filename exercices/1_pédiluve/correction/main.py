from cowpy.cow import Cowacter
import argparse

parser = argparse.ArgumentParser(description="Display a cow saying a message.")
parser.add_argument("message", type=str, help="The message for the cow to say.")
args = parser.parse_args()

message = Cowacter().milk(args.message)
print(message)