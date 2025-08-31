# helpers/ulangi.py

import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        cmd = sys.argv[2:]
        for _ in range(n):
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip(), file=sys.stderr)
            if result.returncode != 0:
                sys.exit(result.returncode)
    except:
        sys.exit(1)
