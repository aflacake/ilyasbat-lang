# helpers/mengembalikan.py

import sys
import json
import os
import re

if len(sys.argv) < 2:
    print("[Python] Kesalahan: Kunci tidak diberikan.")
    sys.exit(1)

key_path_raw = sys.argv[1]

store_file = "penyimpanan.json"

if not os.path.exists(store_file):
    print("[Python] Kesalahan: Tidak ada data tersimpan.")
    sys.exit(1)

with open(store_file, "r") as f:
    data = json.load(f)

def parse_key_path(raw_key):
    return re.split(r"(?<!\[\d{1,10})\.", raw_key)

def resolve_nested(d, keys):
    for key in keys:
        if re.match(r"^[a-zA-Z_]\w*\[\d+\]$", key):
            arr_name, idx = re.match(r"^([a-zA-Z_]\w*)\[(\d+)\]$", key).groups()
            d = d[arr_name][int(idx)]
        else:
            d = d[key]
    return d

try:
    keys = parse_key_path(key_path_raw)
    value = resolve_nested(data, keys)
    print(value)
except Exception as e:
    print(f"[Python] Kesalahan: Tidak dapat mengambil nilai '{key_path_raw}'.")
    sys.exit(1)
