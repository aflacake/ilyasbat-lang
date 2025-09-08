# helpers/mengembalikan.py

import sys
import json
import os
import re

STORE_FILE = "penyimpanan.json"

def parse_key_path(raw_key: str):
    """
    Memecah key path seperti: user.profil[0].nama
    Menjadi list: ["user", "profil[0]", "nama"]
    """
    return re.split(r"(?<!\[\d{1,10})\.", raw_key)

def resolve_nested(d, keys):
    """
    Menelusuri dictionary/array dengan key path.
    """
    for key in keys:
        if re.match(r"^[a-zA-Z_]\w*\[\d+\]$", key):
            arr_name, idx = re.match(r"^([a-zA-Z_]\w*)\[(\d+)\]$", key).groups()
            d = d[arr_name][int(idx)]
        else:
            d = d[key]
    return d

def main():
    if len(sys.argv) < 2:
        print("Kesalahan: Kunci tidak diberikan.")
        sys.exit(1)

    key_path_raw = sys.argv[1]

    if not os.path.exists(STORE_FILE):
        print("Kesalahan: Tidak ada data tersimpan.")
        sys.exit(1)

    try:
        with open(STORE_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Kesalahan: File penyimpanan korup.")
        sys.exit(1)

    try:
        keys = parse_key_path(key_path_raw)
        value = resolve_nested(data, keys)
        print(value)
    except KeyError:
        print(f"Kesalahan: Kunci '{key_path_raw}' tidak ditemukan.")
        sys.exit(1)
    except Exception as e:
        print(f"Kesalahan: Tidak dapat mengambil nilai '{key_path_raw}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
