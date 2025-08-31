# helpers/impor.py

import sys
import os

if len(sys.argv) < 2:
    print("[Python] Kesalahan: Nama file modul tidak diberikan.")
    sys.exit(1)

modul_path = sys.argv[1]
print(f"[Python] Mengimpor modul: {modul_path}")

if not os.path.exists(modul_path):
    print(f"[Python] Kesalahan: File tidak ditemukan -> {modul_path}")
    sys.exit(2)

sys.exit(0)
