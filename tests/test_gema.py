# tests/test_gema.py

import os
import sys
import subprocess
import io
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from helpers.gema import gema_dari_args

def test_gema_function():
    env = {"nama": "Nazwa", "nilai": 1.76322}
    buf = io.StringIO()
    with redirect_stdout(buf):
        gema_dari_args(["Halo", "{nama},", "nilai", "Phie", "=", "{nilai}"], env)
    output = buf.getvalue().strip()
    expected = "Halo Nazwa, nilai Phie = 1.76322"
    assert output == expected, f"Output salah: {output!r}"
    print("[OKE] test_gema_function ->", output)


def test_gema_cli():
    test_file = "test_cli_gema.ibat"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("gema Halo dari CLI IlyasBat!\n")

    result = subprocess.run(
        [sys.executable, "cli.py", test_file],
        capture_output=True,
        text=True
    )

    os.remove(test_file)

    output = result.stdout.strip()
    assert "Halo dari CLI IlyasBat!" in output, f"Output salah: {output!r}"
    print("[OKE] test_gema_cli ->", output)


def test_gema_repl():
    cmd = 'print("\\ngema Halo dari REPL!")\nexit()\n'
    result = subprocess.run(
        [sys.executable, "repl.py"],
        input="gema Halo dari REPL!\nkeluar\n",
        capture_output=True,
        text=True
    )

    assert "Halo dari REPL!" in result.stdout, f"Output salah: {result.stdout!r}"
    print("[OKE] test_gema_repl ->", result.stdout.strip().splitlines()[-1])


def test_gema_repl_advanced():
    result = subprocess.run(
        [sys.executable, "repl_advanced.py"],
        input="gema Halo dari REPL Advanced!\nkeluar\n",
        capture_output=True,
        text=True
    )

    assert "Halo dari REPL Advanced!" in result.stdout, f"Output salah: {result.stdout!r}"
    print("[OKE] test_gema_repl_advanced ->", result.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    print("=== Menjalankan Pengujian IlyasBat (gema) ===\n")
    test_gema_function()
    test_gema_cli()
    test_gema_repl()
    test_gema_repl_advanced()
    print("\nSemua pengujian gema berhasil.")
