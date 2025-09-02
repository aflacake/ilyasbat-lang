# helpers/menyimpan.py

import sys
import json
import os
import re

if len(sys.argv) < 3:
    print("Kesalahan: Format menyimpan salah (butuh kunci dan nilai).")
    sys.exit(1)

raw_key = sys.argv[1]
raw_value = sys.argv[2]

try:
    value = json.loads(raw_value)
except:
    value = raw_value

store_file = "penyimpanan.json"

if os.path.exists(store_file):
    with open(store_file, "r") as f:
        data = json.load(f)
else:
    data = {}

def assign_nested(d, keys, value):
    for i, key in enumerate(keys):
        if re.match(r"^[a-zA-Z_]\w*\[\d+\]$", key):
            arr_name, idx = re.match(r"^([a-zA-Z_]\w*)\[(\d+)\]$", key).groups()
            idx = int(idx)
            d.setdefault(arr_name, [])
            while len(d[arr_name]) <= idx:
                d[arr_name].append(None)
            if i == len(keys) - 1:
                d[arr_name][idx] = value
            else:
                if d[arr_name][idx] is None:
                    d[arr_name][idx] = {}
                d = d[arr_name][idx]
        else:
            if i == len(keys) - 1:
                d[key] = value
            else:
                d = d.setdefault(key, {})

def parse_key_path(raw_key):
    parts = []
    tokens = re.split(r"(?<!\[\d{1,10})\.", raw_key)
    for token in tokens:
        parts.append(token)
    return parts

key_path = parse_key_path(raw_key)
assign_nested(data, key_path, value)

with open(store_file, "w") as f:
    json.dump(data, f, indent=2)

sys.exit(0)
