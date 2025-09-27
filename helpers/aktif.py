# helpers/aktif.py

registry = {}

def hidup_block(name: str, code: str):
    """Aktifkan blok perintah dengan nama tertentu."""
    registry[name] = {"aktif": True, "code": code}
    return f"[hidup] {name} aktif"

def mati_block(name: str):
    """Nonaktifkan blok tertentu."""
    if name in registry:
        registry[name]["aktif"] = False
        return f"[mati] {name} nonaktif"
    return f"[mati] {name} tidak ditemukan"

def jalankan_block(name: str, env: dict, executor):
    """Jalankan blok jika aktif."""
    if name not in registry:
        return f"[jalankan] {name} tidak ditemukan"
    if not registry[name]["aktif"]:
        return f"[jalankan] {name} nonaktif"

    code = registry[name]["code"]
    for line in code.splitlines():
        executor(line.strip(), env)
    return f"[jalankan] {name} selesai"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("[aktif] argumen kurang")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "hidup":
        if len(sys.argv) < 4:
            print("[aktif] format: hidup <nama> <kode>")
            sys.exit(1)
        name = sys.argv[2]
        code_block = " ".join(sys.argv[3:])
        print(hidup_block(name, code_block))

    elif cmd == "mati":
        if len(sys.argv) < 3:
            print("[aktif] format: mati <nama>")
            sys.exit(1)
        print(mati_block(sys.argv[2]))

    elif cmd == "jalankan":
        if len(sys.argv) < 3:
            print("[aktif] format: jalankan <nama>")
            sys.exit(1)
        def fake_exec(line, env=None):
            print(">>>", line)
        print(jalankan_block(sys.argv[2], {}, fake_exec))

    else:
        print(f"[aktif] perintah {cmd} tidak dikenali")
        sys.exit(1)
