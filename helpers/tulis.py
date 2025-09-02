# helpers/tulis.py

def tulis(args):
    if not args:
        print("[Tidak ada teks untuk ditulis]")
        return

    output = " ".join(args)
    print(output)
