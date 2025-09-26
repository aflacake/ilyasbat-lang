# helpers/menampilkan.py

import sys

def try_print_literal(expr: str) -> bool:
    """Coba tampilkan literal string/angka secara langsung."""
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        print(expr[1:-1])
        return True
    try:
        num = int(expr)
        print(num)
        return True
    except ValueError:
        try:
            num = float(expr)
            print(num)
            return True
        except ValueError:
            return False

def menampilkan_inline(exprs, env):
    """Digunakan REPL: tampilkan dari literal atau env dict, bukan os.environ."""
    for expr in exprs:
        if try_print_literal(expr):
            continue
        if expr in env:
            print(env[expr])
        else:
            print(f"[{expr} tidak ditemukan]")

def main():
    if len(sys.argv) < 2:
        print("[argumen tidak cukup]")
        return

    exprs = sys.argv[1:]
    menampilkan_inline(exprs, {})

if __name__ == "__main__":
    main()


    val = os.environ.get(expr)
    if val is not None:
        print(val)
    else:
        print(f"[{expr} tidak ditemukan]")

if __name__ == "__main__":
    main()
