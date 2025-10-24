# tests/test_melompat.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.melompat import resolve_jump

print("=== Menjalankan Pengujian IlyasBat (melompat) ===\n")

def test_jump_forward():
    buffer = [
        "gema Halo",
        "label tujuan:",
        "gema Dunia"
    ]
    idx = resolve_jump(buffer, "tujuan", current_index=0)
    assert idx == 2, f"Seharusnya lompat ke baris 2, tapi dapat {idx}"
    print("[OKE] test_jump_forward -> lompat ke baris benar")


def test_jump_not_found():
    buffer = ["gema Halo"]
    try:
        resolve_jump(buffer, "tidak_ada")
    except RuntimeError as e:
        assert "tidak ditemukan" in str(e)
        print("[OKE] test_jump_not_found -> pesan error sesuai")
    else:
        raise AssertionError("Harusnya raise RuntimeError jika label tidak ditemukan")


def test_jump_backward_disallowed():
    buffer = [
        "label awal:",
        "gema Halo",
        "melompat awal"
    ]
    try:
        resolve_jump(buffer, "awal", current_index=2, allow_backward=False)
    except RuntimeError as e:
        assert "tidak diizinkan" in str(e)
        print("[OKE] test_jump_backward_disallowed -> lompatan mundur diblokir")
    else:
        raise AssertionError("Harusnya raise RuntimeError untuk lompatan mundur")


def test_jump_backward_allowed():
    buffer = [
        "label awal:",
        "gema Halo",
        "melompat awal"
    ]
    idx = resolve_jump(buffer, "awal", current_index=2, allow_backward=True)
    assert idx == 1, f"Harusnya lompat ke baris 1, tapi dapat {idx}"
    print("[OKE] test_jump_backward_allowed -> lompatan mundur diizinkan")

# Jalankan semua tes
if __name__ == "__main__":
    test_jump_forward()
    test_jump_not_found()
    test_jump_backward_disallowed()
    test_jump_backward_allowed()
    print("\nSemua pengujian melompat selesai")
