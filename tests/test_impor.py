# tests/test_impor.py

import os
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.impor import (
    load_file,
    analyze_code,
    register_functions_from_code,
    run_module_code,
    pretty_print,
)

print("=== Menjalankan Pengujian IlyasBat (impor) ===")


class DummyEnv(dict):
    pass


REGISTERED_FUNCS = {}

def dummy_register_fungsi(name, args, body):
    REGISTERED_FUNCS[name] = {"args": args, "body": body}


def test_load_file():
    test_path = "tests/tmp_modul.ibat"
    test_code = "fungsi halo()\n    menampilkan Halo Dunia\nselesai"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    result = load_file(test_path)
    assert "fungsi halo()" in result, "load_file gagal membaca isi file"
    os.remove(test_path)
    print("[OKE] test_load_file -> file berhasil dibaca dan cocok")


def test_analyze_code():
    code = """fungsi hitung(x)
    kalku hasil = x + 1
selesai
"""
    funcs, vars_ = analyze_code(code)
    assert funcs == ["hitung(x)"] or "hitung" in funcs[0], "analisis fungsi gagal"
    assert "hasil" in vars_[0], "analisis variabel gagal"
    print("[OKE] test_analyze_code -> analisis fungsi & variabel berhasil")


def test_register_functions_from_code(monkeypatch=None):
    global REGISTERED_FUNCS
    REGISTERED_FUNCS.clear()

    code = """fungsi tambah(a, b)
    kalku hasil = a + b
selesai
"""
    import helpers.impor as impor
    impor.register_fungsi = dummy_register_fungsi

    register_functions_from_code(code)
    assert "tambah" in REGISTERED_FUNCS, "fungsi tidak terdaftar"
    assert REGISTERED_FUNCS["tambah"]["args"] == ["a", "b"], "argumen tidak sesuai"
    print("[OKE] test_register_functions_from_code -> pendaftaran fungsi berhasil")


def test_run_module_code():
    code = """menampilkan Halo Dunia"""
    logs = []

    import helpers.impor as impor
    def fake_execute_line(line, env):
        logs.append(line)
    impor.execute_line = fake_execute_line

    env = DummyEnv()
    run_module_code(code, env)
    assert logs == ["menampilkan Halo Dunia"], f"run_module_code gagal: {logs}"
    print("[OKE] test_run_module_code -> eksekusi baris kode berhasil")


def test_pretty_print():
    code = """fungsi halo()
    menampilkan Halo Dunia
selesai"""
    buffer = io.StringIO()
    sys_stdout_backup = sys.stdout
    sys.stdout = buffer
    pretty_print(code)
    sys.stdout = sys_stdout_backup

    out = buffer.getvalue()
    assert ">>> fungsi halo()" in out, "highlight fungsi gagal"
    assert "menampilkan Halo Dunia" in out, "highlight menampilkan gagal"
    print("[OKE] test_pretty_print -> pewarnaan keyword berhasil")


if __name__ == "__main__":
    test_load_file()
    test_analyze_code()
    test_register_functions_from_code()
    test_run_module_code()
    test_pretty_print()

    print("\nSemua pengujian impor selesai dengan sukses")
