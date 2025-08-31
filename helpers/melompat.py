# helpers/melompat.py

import sys

if len(sys.argv) < 2:
    print("[Python] Kesalahan: Label tujuan tidak diberikan.")
    sys.exit(1)

label = sys.argv[1]

print(label)
sys.exit(0)
