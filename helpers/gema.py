# helpers/gema.py

def gema(teks: str, env=None):
    """Cetak teks ke layar (fungsi dasar)."""
    if env is None:
        print(teks)
        return

    try:
        teks = teks.format(**env)
    except Exception:
        pass

    print(teks)

def gema_dari_args(args, env, debug=False):
    """Handler untuk perintah 'gema' di interpreter."""
    teks = " ".join(args)
    gema(teks, env)
    return None, False
