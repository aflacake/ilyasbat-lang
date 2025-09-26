# helpers/masukkan.py

import sys

def masukkan_inline(varname: str, env: dict):
    """Digunakan REPL: masukkan nilai dari input() langsung ke env."""
    try:
        value = input(f"Masukkan nilai untuk {varname}: ")
        env[varname] = value
        return value
    except Exception as e:
        print(f"[Kesalahan masukkan: {e}]")
        return None

def main():
    varname = sys.argv[1] if len(sys.argv) > 1 else None
    if not varname:
        print("[Kesalahan: varname tidak diberikan]")
        sys.exit(1)

    val = masukkan_inline(varname, {})
    if val is not None:
        print(f"{varname}={val}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
