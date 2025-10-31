# tests/test_fungsi.py

"""
Pengujian mandiri untuk fitur fungsi di IlyasBat:
- registrasi fungsi
- eksekusi baris (gema)
- eksekusi fungsi
- ekspresi 'kembalikan'
- daftar & pembersihan registry
"""

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers import fungsi_registry
from helpers import fungsi
from helpers import gema, masukkan

print("=== Menjalankan Pengujian IlyasBat (fungsi) ===")

fungsi_registry.clear_fungsi()
fungsi_registry.register_fungsi("tambah", ["a", "b"], ["kembalikan a + b"])
args, body = fungsi_registry.load_fungsi_def("tambah")

if args == ["a", "b"] and body == ["kembalikan a + b"]:
    print("[OKE] test_register_load_fungsi -> berhasil register dan ambil kembali")
else:
    print("[GAGAL] test_register_load_fungsi -> hasil tidak sesuai")

env = {}
fungsi.execute_line("gema Halo Dunia", env)
print("[OKE] test_execute_line -> gema berhasil dijalankan")

fungsi_registry.register_fungsi("halo", ["nama"], ["gema Halo, {nama}"])
env = {}
fungsi.execute_fungsi("halo", ["Ilyas"], env)
print("[OKE] test_execute_fungsi -> fungsi halo berhasil dijalankan")

fungsi_registry.register_fungsi("jumlah", ["x", "y"], ["kembalikan x + y"])
env = {"x": 2, "y": 3}
hasil = fungsi.call_fungsi_inline("jumlah", ["5", "7"], env)
if hasil == 12:
    print("[OKE] test_call_fungsi_inline -> hasil benar (5+7=12)")
else:
    print(f"[GAGAL] test_call_fungsi_inline -> hasil salah ({hasil})")

fungsi_registry.register_fungsi("kali", ["a", "b"], ["kembalikan a * b"])
env = {}
hasil_kali = fungsi.call_fungsi_inline("kali", ["4", "6"], env)
if hasil_kali == 24:
    print("[OKE] test_kembalikan -> ekspresi 'kembalikan' berhasil (4*6=24)")
else:
    print(f"[GAGAL] test_kembalikan -> hasil salah ({hasil_kali})")

daftar = fungsi_registry.list_fungsi()
if "jumlah" in daftar and "halo" in daftar and "kali" in daftar:
    print("[OKE] test_list_fungsi -> daftar fungsi terisi benar")

fungsi_registry.clear_fungsi()
if not fungsi_registry.list_fungsi():
    print("[OKE] test_clear_fungsi -> registry berhasil dikosongkan")

print("=== Semua pengujian fungsi selesai ===")
