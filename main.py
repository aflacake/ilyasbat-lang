# main.py

import sys
import os
from helpers import fungsi

def jalankan_file_ibat(nama_file):
    if not os.path.exists(nama_file):
        print(f"[Kesalahan] File '{nama_file}' tidak ditemukan.")
        return

    with open(nama_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    env = {}
    hasil = fungsi.execute_fungsi(lines, env)
    if hasil is not None:
        print("[Hasil]", hasil)

def main():
    if len(sys.argv) < 2:
        print("Pemakaian: ilyasbat <file.ibat>")
        sys.exit(1)

    nama_file = sys.argv[1]
    jalankan_file_ibat(nama_file)

if __name__ == "__main__":
    main()
