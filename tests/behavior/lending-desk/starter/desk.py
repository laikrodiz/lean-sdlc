import csv
import sys

def labels(path):
    with open(path, newline="") as src:
        for row in csv.DictReader(src):
            print(row["tool_id"] + "|" + row["label"])

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "labels":
        labels(sys.argv[2])
    else:
        sys.exit("usage: desk.py labels catalog.csv")
