# tests/test_menampilkan.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
import io
from contextlib import redirect_stdout
from helpers.menampilkan import try_print_literal, menampilkan_inline

print("=== Menjalankan Pengujian IlyasBat (menampilkan) ===\n")

def test_try_print_literal():
    buf = io.StringIO()
    with redirect_stdout(buf):
        try_print_literal('"Halo Dunia"')
    output = buf.getvalue().strip()
    assert output == "Halo Dunia", f"Output salah: {output!r}"
    print("[OKE] test_try_print_literal ->", output)


def test_menampilkan_inline_literal():
    buf = io.StringIO()
    with redirect_stdout(buf):
        menampilkan_inline(['"Selamat Datang"'], {})
    output = buf.getvalue().strip()
    assert output == "Selamat Datang", f"Output salah: {output!r}"
    print("[OKE] test_menampilkan_inline_literal ->", output)


def test_menampilkan_inline_env():
    buf = io.StringIO()
    with redirect_stdout(buf):
        menampilkan_inline(["nama"], {"nama": "Nazwa"})
    output = buf.getvalue().strip()
    assert output == "Nazwa", f"Output salah: {output!r}"
    print("[OKE] test_menampilkan_inline_env ->", output)


def test_menampilkan_inline_not_found():
    buf = io.StringIO()
    with redirect_stdout(buf):
        menampilkan_inline(["tidak_ada"], {})
    output = buf.getvalue().strip()
    assert "[tidak_ada tidak ditemukan]" in output, f"Output salah: {output!r}"
    print("[OKE] test_menampilkan_inline_not_found ->", output)


def test_menampilkan_cli():
    result = subprocess.run(
        ["python", "helpers/menampilkan.py", '"Halo dari CLI!"'],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    assert output == "Halo dari CLI!", f"Output salah: {output!r}"
    print("[OKE] test_menampilkan_cli ->", output)


if __name__ == "__main__":
    test_try_print_literal()
    test_menampilkan_inline_literal()
    test_menampilkan_inline_env()
    test_menampilkan_inline_not_found()
    test_menampilkan_cli()
    print("\nSemua pengujian 'menampilkan' berhasil.")
