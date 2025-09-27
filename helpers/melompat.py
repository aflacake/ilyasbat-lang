# helpers/melompat.py

def resolve_jump(buffer, target_label, current_index=0, allow_backward=False):
    """
    Cari label dalam buffer, format: 'label <nama>:'.
    - buffer: daftar baris script
    - target_label: string nama label
    - current_index: posisi baris saat ini
    - allow_backward: kalau False, cegah lompat ke atas (infinite loop)

    Return indeks baris setelah label ditemukan, atau None jika tidak ada.
    """
    label_syntax = f"label {target_label}:"
    for idx, line in enumerate(buffer):
        if line.strip().lower() == label_syntax.lower():
            if not allow_backward and idx < current_index:
                raise RuntimeError(
                    f"Lompatan mundur ke label '{target_label}' tidak diizinkan."
                )
            return idx + 1
    raise RuntimeError(f"Label '{target_label}' tidak ditemukan dalam buffer.")
