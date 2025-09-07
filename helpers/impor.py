# helpers/impor.py

import sys
import os

def impor_modul(modul_name: str):
    if os.path.exists(modul_name):
        return modul_name

    if not modul_name.endswith(".ibat"):
        modul_name = modul_name + ".ibat"

    candidate = os.path.join("modules", modul_name)
    if os.path.exists(candidate):
        return candidate

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Python] Kesalahan: Nama file modul tidak diberikan.")
        sys.exit(1)

    modul_name = sys.argv[1]
    modul_path = impor_modul(modul_name)

    if modul_path is None:
        print(f"[Python] Kesalahan: Modul '{modul_name}' tidak ditemukan.")
        sys.exit(2)

    print(f"[Python] Modul berhasil diimpor: {modul_path}")
    sys.exit(0)
