# tests/test_mengembalikan.py

import os
import json
import sys

print("=== Menjalankan Pengujian IlyasBat (mengembalikan) ===")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.mengembalikan import parse_key_path, resolve_nested, STORE_FILE, main

dummy_data = {
    "user": {
        "profil": [
            {"nama": "Nazwa", "umur": 17},
            {"nama": "Shabrina", "umur": 16}
        ]
    },
    "konfigurasi": {"mode": "aktif"}
}

with open(STORE_FILE, "w") as f:
    json.dump(dummy_data, f)


def test_parse_key_path():
    hasil = parse_key_path("user.profil[0].nama")
    assert hasil == ["user", "profil[0]", "nama"], f"Salah parse: {hasil}"
    print("[OKE] test_parse_key_path -> path terurai dengan benar")


def test_resolve_nested():
    keys = ["user", "profil[1]", "nama"]
    hasil = resolve_nested(dummy_data, keys)
    assert hasil == "Shabrina", f"Hasil salah: {hasil}"
    print("[OKE] test_resolve_nested -> akses bertingkat berhasil")


def test_main_cli_berhasil():
    sys.argv = ["mengembalikan.py", "user.profil[0].umur"]

    from io import StringIO
    backup_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        main()
        output = sys.stdout.getvalue().strip()
        assert output == "17", f"Output salah: {output}"
        print("[OKE] test_main_cli_berhasil -> CLI menampilkan nilai dengan benar")
    finally:
        sys.stdout = backup_stdout


def test_main_cli_kunci_tidak_ada():
    sys.argv = ["mengembalikan.py", "user.alamat"]

    from io import StringIO
    backup_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        try:
            main()
        except SystemExit:
            pass
        output = sys.stdout.getvalue()
        assert "tidak ditemukan" in output, "Pesan kesalahan tidak sesuai"
        print("[OKE] test_main_cli_kunci_tidak_ada -> tangani kunci tidak ditemukan")
    finally:
        sys.stdout = backup_stdout


if __name__ == "__main__":
    test_parse_key_path()
    test_resolve_nested()
    test_main_cli_berhasil()
    test_main_cli_kunci_tidak_ada()

    if os.path.exists(STORE_FILE):
        os.remove(STORE_FILE)

    print("\nSemua pengujian selesai.")
