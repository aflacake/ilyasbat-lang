# tests/test_masukkan.py

import os
import sys
import io
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.masukkan import masukkan_inline, masukkan_dari_args, main

print("=== Menjalankan Pengujian IlyasBat (masukkan) ===")


def test_masukkan_inline():
    env = {}
    with patch("builtins.input", return_value="42"):
        val = masukkan_inline("angka", env)
    assert env["angka"] == "42", f"Nilai env salah: {env}"
    assert val == "42", f"Nilai kembalian salah: {val}"
    print("[OKE] test_masukkan_inline -> input palsu berhasil")


def test_masukkan_dari_args():
    env = {}
    with patch("builtins.input", return_value="Nazwa"):
        masukkan_dari_args(["nama"], env)
    assert env["nama"] == "Nazwa", f"Nilai env salah: {env}"
    print("[OKE] test_masukkan_dari_args -> handler masukkan berhasil")


def test_main_cli_simulasi():
    """Simulasi pemanggilan helpers/masukkan.py sebagai skrip CLI."""
    import subprocess

    result = subprocess.run(
        [sys.executable, "helpers/masukkan.py", "kota"],
        input="Bandung\n",
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, f"Kode keluar salah: {result.returncode}"
    assert "kota=Bandung" in result.stdout, f"Output salah: {result.stdout!r}"
    print("[OKE] test_main_cli_simulasi -> CLI masukkan berjalan baik")


if __name__ == "__main__":
    test_masukkan_inline()
    test_masukkan_dari_args()
    test_main_cli_simulasi()
    print("\nSemua pengujian selesai.")
