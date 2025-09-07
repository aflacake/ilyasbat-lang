# helpers/tulis.py

import sys
import os

def tulis(args, env=None):
    if not args:
        print("[Tidak ada teks untuk ditulis]")
        return

    hasil = []
    for arg in args:
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            hasil.append(arg[1:-1])
        elif env and arg in env:
            hasil.append(str(env[arg]))
        else:
            hasil.append(arg)

    output = " ".join(hasil)
    print(output)

if __name__ == "__main__":
    import sys
    tulis(sys.argv[1:])

