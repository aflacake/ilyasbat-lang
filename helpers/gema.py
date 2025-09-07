# helpers/gema.py

import sys

def gema(teks: str):
    """Cetak ulang teks ke layar (fungsi gema)."""
    print(teks)

if __name__ == "__main__":
    teks = " ".join(sys.argv[1:])
    gema(teks)
