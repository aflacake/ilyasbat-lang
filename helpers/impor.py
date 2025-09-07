# helpers/impor.py

import sys
import os
import subprocess

def jalankan_baris(line):
    """Jalankan satu baris perintah dari modul ibat."""
    line = line.strip()
    if not line or line.strip().startswith("KOM"):
        return

    parts = line.split()
    cmd = parts[0]
    args = parts[1:]

    subprocess.run(
        ["python", "repl.py", "--inline", cmd] + args,
        check=False
    )

def main():
    if len(sys.argv) < 2:
        print("Kesalahan: Nama file modul tidak diberikan.")
        sys.exit(1)

    modul_path = sys.argv[1]

    if not os.path.exists(modul_path):
        print(f"Kesalahan: File tidak ditemukan -> {modul_path}")
        sys.exit(2)

    print(f"Mengimpor modul: {modul_path}")

    with open(modul_path, "r", encoding="utf-8") as f:
        for line in f:
            jalankan_baris(line)

    sys.exit(0)

if __name__ == "__main__":
    main()
