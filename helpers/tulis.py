# helpers/tulis.py

import sys

def tulis(args):
    if not args:
        print("[Tidak ada teks untuk ditulis]")
        return

    cleaned = []
    for arg in args:
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            cleaned.append(arg[1:-1])
        else:
            cleaned.append(arg)

    output = " ".join(cleaned)
    print(output)

if __name__ == "__main__":
    tulis(sys.argv[1:])
