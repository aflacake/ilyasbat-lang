# repl.py

import os
import subprocess

TMP_FILE = ".tmp_repl.ibat"

def run_ibat(code_lines):
    TMP_FILE = ".tmp_repl.ibat"
    ENV_FILE = ".env.bat"

    with open(TMP_FILE, "w", encoding="utf-8") as f:
        for line in code_lines:
            f.write(line + "\n")

        f.write("set > .env.bat\n")

    result = subprocess.run(["cmd", "/c", "main.bat", TMP_FILE], capture_output=True, text=True)

    output = result.stdout.strip()
    if output:
        print(output)
    err = result.stderr.strip()
    if err:
        print(f"[stderr] {err}")

    os.remove(TMP_FILE)

def main():
    print("== IlyasBat Mode REPL ==")
    print("Ketik 'keluar' untuk mengakhiri.")
    print("Ketik 'reset' untuk menghapus buffer.")
    print("Ketik 'lihat variabel' untuk melihat semua variabel.")
    print("Ketik 'jalan' untuk menjalankan skrip.")

    buffer = []

    while True:
        try:
            inp = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if inp.lower() == "keluar":
            print("Keluar!")
            break
        elif inp.lower() == "reset":
            buffer.clear()
            print("[buffer dikosongkan]")
        elif inp.lower() == "lihat variabel":
            if os.path.exists(".env.bat"):
                with open(".env.bat", encoding="utf-8") as f:
                    for line in f:
                        print(line.strip())
            else:
                print("[belum ada variabel]")
        elif inp.lower() == "jalan":
            if buffer:
                run_ibat(buffer)
            else:
                print("[buffer kosong]")
        elif inp == "":
            continue
        else:
            buffer.append(inp)

if __name__ == "__main__":
    main()
