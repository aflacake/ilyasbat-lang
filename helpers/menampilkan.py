# helpers/menampilkan.py

def tampilkan_handler(env, args):
    if not args:
        print("[Tidak ada argumen untuk menampilkan]")
        return

    key = args[0]
    if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
        print(key[1:-1])
    else:
        if key in env:
            print(env[key])
        else:
            print(f"[{key} tidak ditemukan]")
