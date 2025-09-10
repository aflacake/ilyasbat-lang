# helpers/impor.py

import sys
import os

KEYWORDS = {
    "fungsi": "[FUNGSI]",
    "kalku": "[KALKU]",
    "jika": "[JIKA]",
    "menampilkan": "[MENAMPILKAN]",
}

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
