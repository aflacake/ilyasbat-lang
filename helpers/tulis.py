# helpers/tulis.py

import sys
import os

def tulis(args):
    if not args:
        print("[Tidak ada teks untuk ditulis]")
        return

    hasil = []
    for arg in args:
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            hasil.append(arg[1:-1])
        else:
            if arg in os.environ:
                hasil.append(os.environ[arg])
            else:
                hasil.append(arg)

    output = " ".join(hasil)
    print(output)

if __name__ == "__main__":
    tulis(sys.argv[1:])
