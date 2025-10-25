# helpers/menyimpan.py

import json
import os
import re

STORE_FILE = "penyimpanan.json"


def load_store(store_file=STORE_FILE):
    """Muat isi penyimpanan.json (atau buat baru jika tidak ada)."""
    if os.path.exists(store_file):
        try:
            with open(store_file, "r") as f:
                return json.load(f)
        except Exception:
            print(f"[Kesalahan] File {store_file} rusak, buat baru.")
            return {}
    return {}


def save_store(data, store_file=STORE_FILE):
    """Simpan dictionary ke penyimpanan.json."""
    with open(store_file, "w") as f:
        json.dump(data, f, indent=2)


def assign_nested(d, keys, value):
    """Set nilai di dictionary nested (mendukung arr[0] dan dot)."""
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
    """
    Pisahkan path seperti 'user.name' atau 'arr[0].field' tanpa regex lookbehind.
    """
    parts = []
    current = ""
    in_bracket = False

    for ch in raw_key:
        if ch == '.' and not in_bracket:
            parts.append(current)
            current = ""
        else:
            current += ch
            if ch == '[':
                in_bracket = True
            elif ch == ']':
                in_bracket = False

    if current:
        parts.append(current)

    return parts


def simpan(raw_key, raw_value, store_file=STORE_FILE):
    """Simpan pasangan key-value ke storage."""
    try:
        value = json.loads(raw_value)
    except Exception:
        value = raw_value

    data = load_store(store_file)
    key_path = parse_key_path(raw_key)
    assign_nested(data, key_path, value)
    save_store(data, store_file)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Kesalahan: Format menyimpan salah (butuh kunci dan nilai).")
        sys.exit(1)

    raw_key = sys.argv[1]
    raw_value = sys.argv[2]
    simpan(raw_key, raw_value)
    sys.exit(0)
