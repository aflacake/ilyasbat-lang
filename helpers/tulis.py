# helpers/tulis.py

import sys
from simpleeval import simple_eval


def tulis(args, env=None, return_only=False):
    """
    Print atau kembalikan hasil gabungan argumen.
    - args: list of string token
    - env: dict variabel
    - return_only: kalau True, tidak print tapi return string
    """
    if not args:
        msg = "[Tidak ada teks untuk ditulis]"
        if return_only:
            return msg
        print(msg)
        return msg

    hasil = []
    for arg in args:
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            hasil.append(arg[1:-1])
        elif env:
            try:
                val = simple_eval(arg, names=env)
                hasil.append(str(val))
            except Exception:
                if arg in env:
                    hasil.append(str(env[arg]))
                else:
                    hasil.append(arg)
        else:
            hasil.append(arg)

    output = " ".join(hasil)

    if return_only:
        return output
    print(output)
    return output


if __name__ == "__main__":
    tulis(sys.argv[1:])
