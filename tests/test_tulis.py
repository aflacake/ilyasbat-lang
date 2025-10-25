# tests/test_tulis.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.tulis import tulis

print("=== Menjalankan Pengujian IlyasBat (tulis) ===\n")

def test_tulis_literal():
    result = tulis(['"Halo"', '"Dunia"'], return_only=True)
    assert result == "Halo Dunia", f"Output salah: {result}"
    print("[OKE] test_tulis_literal -> literal string ditulis benar")


def test_tulis_numerik():
    result = tulis(['123', '456'], return_only=True)
    assert result == "123 456", f"Output salah: {result}"
    print("[OKE] test_tulis_numerik -> angka ditulis benar")


def test_tulis_ekspresi_dengan_env():
    env = {'x': 10, 'y': 5}
    result = tulis(['x', '+', 'y'], env, return_only=True)
    assert result == "x + y", f"Output salah: {result}"
    print("[OKE] test_tulis_ekspresi_dengan_env -> gabungan ekspresi sesuai")


def test_tulis_eval_langsung():
    env = {'x': 10, 'y': 5}
    result = tulis(['x+y'], env, return_only=True)
    assert result == "15", f"Output salah: {result}"
    print("[OKE] test_tulis_eval_langsung -> ekspresi dievaluasi benar")


def test_tulis_var_dari_env():
    env = {'nama': 'Nazwa'}
    result = tulis(['nama'], env, return_only=True)
    assert result == "Nazwa", f"Output salah: {result}"
    print("[OKE] test_tulis_var_dari_env -> variabel dari env berhasil ditulis")


def test_tulis_kosong():
    result = tulis([], return_only=True)
    assert "[Tidak ada teks untuk ditulis]" in result
    print("[OKE] test_tulis_kosong -> pesan kosong sesuai")

if __name__ == "__main__":
    test_tulis_literal()
    test_tulis_numerik()
    test_tulis_ekspresi_dengan_env()
    test_tulis_eval_langsung()
    test_tulis_var_dari_env()
    test_tulis_kosong()
    print("\nSemua pengujian tulis selesai")
