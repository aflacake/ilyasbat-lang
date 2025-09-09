# helpers/impor.py

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("[Kesalahan: Nama file modul tidak diberikan.]")
        sys.exit(1)

    modul_path = sys.argv[1]

    if not os.path.exists(modul_path):
        print(f"[Kesalahan: File tidak ditemukan -> {modul_path}]")
        sys.exit(2)

    with open(modul_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(content)

if __name__ == "__main__":
    main()
