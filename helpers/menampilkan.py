# helpers/menampilkan.py

import os
import sys

if len(sys.argv) != 2:
    print("[argumen tidak valid]")
    sys.exit(1)

key = sys.argv[1]
val = os.environ.get(key)

if val is None:
    print(f"[{key} tidak ditemukan]")
    sys.exit(1)
else:
    print(val)
