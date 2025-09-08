# helpers/ulangi.py

import sys
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Kesalahan: Format ulangi salah (butuh jumlah dan perintah).")
        sys.exit(1)

    try:
        count = int(sys.argv[1])
        command = sys.argv[2:]

        for i in range(count):
            result = subprocess.run(
                ["cmd", "/c", "main.bat"] + command,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip(), file=sys.stderr)

            if result.returncode != 0:
                sys.exit(result.returncode)

    except Exception as e:
        print("Kesalahan:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
