# tests/test_menyimpan.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import json
import tempfile
from helpers.menyimpan import load_store, save_store, assign_nested, parse_key_path, simpan

print("=== Menjalankan Pengujian IlyasBat (menyimpan) ===")

TEMP_FILE = os.path.join(tempfile.gettempdir(), "test_penyimpanan.json")
if os.path.exists(TEMP_FILE):
    os.remove(TEMP_FILE)


def test_load_and_save_store():
    data = {"nama": "Nazwa", "nilai": 95}
    save_store(data, TEMP_FILE)
    hasil = load_store(TEMP_FILE)
    assert hasil == data, f"Data tidak sama: {hasil}"
    print("[OKE] test_load_and_save_store -> simpan & muat berhasil")


def test_assign_nested_dot():
    d = {}
    assign_nested(d, ["user", "name"], "Shabrina")
    assert d == {"user": {"name": "Shabrina"}}, f"Salah: {d}"
    print("[OKE] test_assign_nested_dot -> akses bertingkat titik")


def test_assign_nested_array():
    d = {}
    assign_nested(d, ["data[0]", "nama"], "Zain")
    assert d == {"data": [{"nama": "Zain"}]}, f"Salah: {d}"
    print("[OKE] test_assign_nested_array -> akses indeks array")


def test_parse_key_path():
    key = "user.profile[0].name"
    tokens = parse_key_path(key)
    assert tokens == ["user", "profile[0]", "name"], f"Salah: {tokens}"
    print("[OKE] test_parse_key_path -> tokenisasi key path benar")


def test_simpan_dan_load():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
    simpan("user.name", '"Nazwa"', TEMP_FILE)
    simpan("user.umur", "17", TEMP_FILE)
    hasil = load_store(TEMP_FILE)
    assert hasil["user"]["name"] == "Nazwa", f"Salah: {hasil}"
    assert hasil["user"]["umur"] == 17, f"Salah: {hasil}"
    print("[OKE] test_simpan_dan_load -> menyimpan dan memuat data berhasil")


def test_simpan_array_bertahap():
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
    simpan("arr[0].nilai", "100", TEMP_FILE)
    simpan("arr[1].nilai", "95", TEMP_FILE)
    hasil = load_store(TEMP_FILE)
    assert hasil["arr"][0]["nilai"] == 100, f"Salah: {hasil}"
    assert hasil["arr"][1]["nilai"] == 95, f"Salah: {hasil}"
    print("[OKE] test_simpan_array_bertahap -> array dengan indeks ganda berhasil")


if __name__ == "__main__":
    test_load_and_save_store()
    test_assign_nested_dot()
    test_assign_nested_array()
    test_parse_key_path()
    test_simpan_dan_load()
    test_simpan_array_bertahap()
    print("\nSemua pengujian selesai tanpa error")
