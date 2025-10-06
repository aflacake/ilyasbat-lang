# helpers/gema.py

import sys

def gema(teks: str, env=None):
    """
    Cetak ulang teks ke layar (fungsi gema).
    Mendukung format variabel seperti {nama} dari environment.
    """
    if env is None:
        print(teks)
        return

    try:
        teks = teks.format(**env)
    except Exception:
        pass

    print(teks)


def gema_dari_args(args, env=None):
    """
    Versi gema untuk dipakai di interpreter (pakai list args).
    Misalnya: gema_dari_args(["Halo,", "{nama}!"], env)
    """
    if not args:
        print("[Kesalahan] Tidak ada teks untuk gema.")
        return

    teks = " ".join(args)
    gema(teks, env)


if __name__ == "__main__":
    teks = " ".join(sys.argv[1:])
    gema(teks)
