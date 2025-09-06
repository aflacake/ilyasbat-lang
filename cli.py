# cli.py

import sys
import os
from repl import run_module, env

def run_file(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' tidak ditemukan.")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        cmd, args = parts[0], parts[1:]
        run_module(cmd, args)

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python cli.py <file.ibat>")
        sys.exit(1)

    filename = sys.argv[1]
    run_file(filename)

if __name__ == "__main__":
    main()
