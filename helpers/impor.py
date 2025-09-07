# helpers/impor.py

import sys
import os

def impor_modul(modul_path: str):
    print(f"Mengimpor modul: {modul_path}")

    if not os.path.exists(modul_path):
        print(f"[Python] Kesalahan: File tidak ditemukan -> {modul_path}")
        return 2

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kesalahan: Nama file modul tidak diberikan.")
        sys.exit(1)

    modul_path = sys.argv[1]
    code = impor_modul(modul_path)
    sys.exit(code)
