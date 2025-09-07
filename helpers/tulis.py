# helpers/tulis.py

import sys

def tulis(args):
    if not args:
        print("[Tidak ada teks untuk ditulis]")
        return
    output = " ".join(args)
    print(output)

if __name__ == "__main__":
    tulis(sys.argv[1:])
