# tests/test_berakhir.py

import os
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.berakhir import berakhir

print("=== Menjalankan Pengujian IlyasBat (berakhir) ===")

def test_berakhir_exit():
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        berakhir()
    except SystemExit as e:
        assert e.code == 0, f"Kode keluar salah: {e.code}"
    else:
        raise AssertionError("Fungsi berakhir() tidak memanggil sys.exit()!")

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "[Program dihentikan melalui perintah 'berakhir']" in output, f"Pesan salah: {output}"
    print("[OKE] test_berakhir_exit -> pesan dan exit code benar")

if __name__ == "__main__":
    test_berakhir_exit()
    print("\nSemua pengujian selesai.")
