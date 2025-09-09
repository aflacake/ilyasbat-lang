# helpers/impor.py

import sys
import os

def load_file(modul_path: str) -> str:
    """Kembalikan isi file .ibat sebagai string."""
    if not os.path.exists(modul_path):
        raise FileNotFoundError(f"File tidak ditemukan: {modul_path}")

    with open(modul_path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("[Kesalahan: Nama file modul tidak diberikan.]")
        sys.exit(1)

    modul_path = sys.argv[1]

    try:
        print(load_file(modul_path))
    except FileNotFoundError as e:
        print(e)
        sys.exit(2)

if __name__ == "__main__":
    main()
