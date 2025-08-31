# helpers/menyimpan.py

import sys
import json
import os

if len(sys.argv) < 3:
    print("[Python] Kesalahan: Format menyimpan salah (butuh kunci dan nilai).")
    sys.exit(1)

key = sys.argv[1]
value = sys.argv[2]

store_file = "penyimpanan.json"

if os.path.exists(store_file):
    with open(store_file, "r") as f:
        data = json.load(f)
else:
    data = {}

data[key] = value

with open(store_file, "w") as f:
    json.dump(data, f)

sys.exit(0)
