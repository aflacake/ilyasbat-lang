# helpers/melompat.py

def resolve_jump(buffer, target_label):
    """
    Cari label dalam buffer, format: 'label <nama>:'
    Kembalikan indeks baris setelah label ditemukan, 
    atau None jika tidak ada.
    """
    label_syntax = f"label {target_label}:"
    for idx, line in enumerate(buffer):
        if line.strip().lower() == label_syntax.lower():
            return idx + 1
    return None
