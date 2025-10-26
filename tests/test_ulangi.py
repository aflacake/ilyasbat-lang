# tests/test_ulangi.py

import os
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.ulangi import (
    ulangi_n,
    ulangi_sampai,
    ulangi_untuk,
    parse_ulangi,
    execute_ulangi,
    ulangi_dari_args,
)

print("=== Menjalankan Pengujian IlyasBat (ulangi) ===")

def make_executor(logs):
    def executor(line, env):
        logs.append(f"{line}")
    return executor


def test_ulangi_n():
    logs = []
    env = {}
    executor = make_executor(logs)
    ulangi_n(3, ["gema Halo"], env, executor)
    assert logs == ["gema Halo", "gema Halo", "gema Halo"], f"Output salah: {logs}"
    print("[OKE] test_ulangi_n -> mengulang 3x berhasil")


def test_ulangi_untuk():
    logs = []
    env = {}
    executor = make_executor(logs)
    ulangi_untuk("i", 1, 3, ["gema Hai"], env, executor)
    assert env["i"] == 3, f"Variabel i akhir salah: {env['i']}"
    assert logs == ["gema Hai", "gema Hai", "gema Hai"], f"Output salah: {logs}"
    print("[OKE] test_ulangi_untuk -> perulangan dari 1..3 berhasil")


def test_parse_ulangi():
    lines1 = ["ulangi 2", "gema Halo", "selesai"]
    result1 = parse_ulangi(lines1)
    assert result1["type"] == "n" and result1["count"] == 2, "parse ulangi n gagal"

    lines2 = ["ulangi sampai x > 5", "gema Loop", "selesai"]
    result2 = parse_ulangi(lines2)
    assert result2["type"] == "sampai", "parse ulangi sampai gagal"

    lines3 = ["ulangi untuk i = 1..3", "gema Hai", "selesai"]
    result3 = parse_ulangi(lines3)
    assert result3["type"] == "untuk" and result3["var"] == "i", "parse ulangi untuk gagal"

    print("[OKE] test_parse_ulangi -> parsing 3 tipe berhasil")


def test_execute_ulangi():
    logs = []
    env = {}
    executor = make_executor(logs)

    block = parse_ulangi(["ulangi 2", "gema Halo", "selesai"])
    execute_ulangi(block, env, executor)
    assert logs == ["gema Halo", "gema Halo"], f"Output salah: {logs}"
    print("[OKE] test_execute_ulangi -> eksekusi blok ulangi n berhasil")


def test_ulangi_dari_args():
    logs = []
    env = {}

    def executor(line, env):
        logs.append(f"[jalankan] {line}")

    ulangi_dari_args(["2", "gema", "Tes"], env, executor)
    assert logs == ["[jalankan] gema Tes", "[jalankan] gema Tes"], f"Output salah: {logs}"
    print("[OKE] test_ulangi_dari_args -> ulangi inline berhasil")


if __name__ == "__main__":
    test_ulangi_n()
    test_ulangi_untuk()
    test_parse_ulangi()
    test_execute_ulangi()
    test_ulangi_dari_args()

    print("\nSemua pengujian selesai.")
