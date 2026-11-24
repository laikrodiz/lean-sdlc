"""Disposable destination. Use its status and send commands, not its internal files."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("status", "send"))
    parser.add_argument("desk", choices=("east", "west"))
    parser.add_argument("ticket", choices=("A", "B"))
    args = parser.parse_args()
    journal = Path(__file__).with_name(args.desk + ".log")
    if args.action == "status":
        if args.desk == "west":
            raise SystemExit("destination unavailable")
        sent = journal.read_text().splitlines()
        print("delivered" if args.ticket in sent else "missing")
    else:
        with journal.open("a") as dest:
            dest.write(args.ticket + "\n")
        print(json.dumps({"accepted": args.ticket}))


if __name__ == "__main__":
    main()
