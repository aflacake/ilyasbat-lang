# helpers/gema.py

import sys

def gema(teks: str, env=None):
    """Cetak ulang teks ke layar (fungsi gema)."""
    if env is None:
        print(teks)
        return

    try:
        teks = teks.format(**env)
    except Exception:
        pass

    print(teks)

if __name__ == "__main__":
    teks = " ".join(sys.argv[1:])
    gema(teks)
