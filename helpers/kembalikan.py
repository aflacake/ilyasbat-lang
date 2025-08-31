# helpers/kembalikan.py

import sys

if len(sys.argv) < 2:
    print("[Python] Kesalahan: Nilai tidak diberikan.")
    sys.exit(1)

nilai = sys.argv[1]

print(nilai)
sys.exit(0)
