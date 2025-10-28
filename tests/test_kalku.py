# tests/test_kalku.py

import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.kalku import (
    tambah, kurang, kali, bagi, pangkat, maks, min,
    try_parse_number, kalkulasi
)

print("=== Menjalankan Pengujian IlyasBat (kalku) ===")


def test_operasi_dasar():
    assert tambah(2, 3) == 5
    assert kurang(5, 2) == 3
    assert kali(3, 4) == 12
    assert bagi(8, 2) == 4
    assert bagi(5, 0) == float("inf")
    assert pangkat(2, 3) == 8
    assert maks(7, 4) == 7
    assert min(7, 4) == 4
    print("[OKE] test_operasi_dasar -> operasi aritmetika dasar berfungsi")


def test_try_parse_number():
    assert try_parse_number("42") == 42
    assert try_parse_number("3.14") == 3.14
    assert try_parse_number("abc") is None
    assert try_parse_number(10) == 10
    print("[OKE] test_try_parse_number -> parsing angka berhasil")


def test_kalkulasi_sederhana():
    env = {"x": 5}
    var, hasil = kalkulasi("y = tambah(x, 3)", env)
    assert var == "y" and hasil == 8
    print("[OKE] test_kalkulasi_sederhana -> tambah() berjalan baik")


def test_kalkulasi_pangkat_dan_bagi():
    env = {}
    var, hasil = kalkulasi("z = pangkat(2, 3) + bagi(10, 2)", env)
    assert var == "z" and hasil == 13
    print("[OKE] test_kalkulasi_pangkat_dan_bagi -> ekspresi majemuk sukses")


def test_kalkulasi_dengan_variabel_env():
    env = {"a": 10, "b": 2}
    var, hasil = kalkulasi("c = a / b", env)
    assert var == "c" and hasil == 5
    print("[OKE] test_kalkulasi_dengan_variabel_env -> env bekerja benar")


def test_kalkulasi_tanpa_assignment():
    var, hasil = kalkulasi("pangkat(2,3)", {})
    assert var is None and hasil is None
    print("[OKE] test_kalkulasi_tanpa_assignment -> deteksi format salah valid")


def test_kalkulasi_simbol_tidak_dikenal():
    env = {}
    var, result = kalkulasi("x = abc + 3", env)
    assert var is None and result is None
    print("[OKE] test_kalkulasi_simbol_tidak_dikenal -> deteksi simbol tidak dikenal valid")

def test_kalkulasi_kesalahan_sintaks():
    var, hasil = kalkulasi("x = tambah(2, )", {})
    assert var is None and hasil is None
    print("[OKE] test_kalkulasi_kesalahan_sintaks -> tangani error dengan aman")

def test_kalkulasi_bagi_nol():
    env = {"a": 5, "b": 0}
    var, hasil = kalkulasi("r = bagi(a, b)", env)
    assert var == "r" and hasil == float("inf")
    print("[OKE] test_kalkulasi_bagi_nol -> pembagian nol aman")


def test_cli_kalku_simulasi():
    """Simulasi jalankan helpers/kalku.py via CLI — tampilkan debug jika gagal."""
    import subprocess, os
    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    result = subprocess.run(
        [sys.executable, "helpers/kalku.py", "hasil=tambah(3,4)"],
        capture_output=True,
        text=True,
        cwd=proj_root,
        timeout=10
    )

    if result.returncode != 0:
        print("---- DEBUG: CLI kalku gagal ----")
        print("returncode:", result.returncode)
        print("stdout:")
        print(result.stdout)
        print("stderr:")
        print(result.stderr)
        print("---- END DEBUG ----")

    assert result.returncode == 0, f"CLI kalku gagal, returncode={result.returncode}"
    assert "hasil" in result.stdout or "Selesai" in result.stdout or "Kalkulasi" in result.stdout
    print("[OKE] test_cli_kalku_simulasi -> mode CLI kalku berjalan baik")


if __name__ == "__main__":
    test_operasi_dasar()
    test_try_parse_number()
    test_kalkulasi_sederhana()
    test_kalkulasi_pangkat_dan_bagi()
    test_kalkulasi_dengan_variabel_env()
    test_kalkulasi_tanpa_assignment()
    test_kalkulasi_simbol_tidak_dikenal()
    test_kalkulasi_kesalahan_sintaks()
    test_kalkulasi_bagi_nol()
    test_cli_kalku_simulasi()
    print("\nSemua pengujian selesai dengan sukses.")
