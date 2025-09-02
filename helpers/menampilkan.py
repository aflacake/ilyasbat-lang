# helpers/menampilkan.py

def menampilkan_handler(env, args):
    expr = " ".join(args)

    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        print(expr[1:-1])
        return

    try:
        val = int(expr)
        print(val)
        return
    except ValueError:
        try:
            val = float(expr)
            print(val)
            return
        except ValueError:
            pass

    val = env.get(expr)
    if val is not None:
        print(val)
    else:
        print(f"[{expr} tidak ditemukan]")
