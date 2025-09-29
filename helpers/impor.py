# helpers/impor.py

import sys
import os

from helpers.fungsi_registry import register_fungsi
from helpers.parser import parse
from helpers.fungsi import execute_line

KEYWORDS = {
    "fungsi": "[FUNGSI]",
    "kalku": "[KALKU]",
    "jika": "[JIKA]",
    "menampilkan": "[MENAMPILKAN]",
}

def register_functions_from_code(code: str):
    """
    Cari definisi fungsi dalam kode .ibat dan simpan ke registry.
    """
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("fungsi "):
            header = line[len("fungsi "):].strip()
            if "(" in header and header.endswith(")"):
                name, params = header.split("(", 1)
                name = name.strip()
                arg_names = [p.strip() for p in params[:-1].split(",") if p.strip()]
            else:
                name = header
                arg_names = []

            body_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != "selesai":
                body_lines.append(lines[i])
                i += 1

            register_fungsi(name, arg_names, body_lines)
        i += 1

def run_module_code(code: str, env):
    """Eksekusi isi kode .ibat agar fungsi terdaftar."""
    lines = code.splitlines()
    tree = parse(lines)
    for node in tree:
        if isinstance(node, dict) and node.get("type") == "fungsi":
            pass
        else:
            if isinstance(node, str):
                execute_line(node, env)

def load_file(modul_path: str) -> str:
    """Kembalikan isi file .ibat sebagai string."""
    if not os.path.exists(modul_path):
        raise FileNotFoundError(f"File tidak ditemukan: {modul_path}")

    with open(modul_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_code(code: str):
    """Analisis sederhana: hitung fungsi, variabel, dll."""
    functions = []
    variables = []
    for line in code.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "fungsi" and len(parts) > 1:
            functions.append(parts[1])
        elif parts[0] == "kalku" and len(parts) > 1:
            variables.append(parts[1])
    return functions, variables

def pretty_print(code: str):
    """Cetak kode dengan highlight sederhana."""
    for line in code.splitlines():
        parts = line.strip().split()
        if not parts:
            print()
            continue
        if parts[0] in KEYWORDS:
            print(f">>> {line}")
        else:
            print(f"    {line}")

def main():
    register_functions_from_code(code)
    from repl import env
    run_module_code(code, env)

    if len(sys.argv) < 2:
        print("[Kesalahan: Nama file modul tidak diberikan.]")
        sys.exit(1)

    modul_path = sys.argv[1]

    try:
        code = load_file(modul_path)
        functions, variables = analyze_code(code)

        print(f"[Mengimpor {modul_path}]")
        print(f" - {len(code.splitlines())} baris kode dimuat")
        if functions:
            print(f" - Fungsi terdeteksi: {', '.join(functions)}")
        if variables:
            print(f" - Variabel awal: {', '.join(variables)}")

        print("\n[Isi modul]")
        pretty_print(code)

    except FileNotFoundError as e:
        print(e)
        sys.exit(2)

if __name__ == "__main__":
    main()
