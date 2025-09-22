# helpers/fungsi_registry.py

"""
Registry untuk menyimpan definisi fungsi bahasa .ibat
Fungsi disimpan dalam dictionary global agar bisa dipanggil dari REPL atau CLI.
"""

_fungsi_registry = {}


def register_fungsi(name, arg_names, body_lines):
    """
    Daftarkan fungsi baru ke registry.
    :param name: nama fungsi (string)
    :param arg_names: list nama parameter
    :param body_lines: list baris isi fungsi
    """
    if not isinstance(arg_names, list):
        raise TypeError("arg_names harus berupa list")
    if not isinstance(body_lines, list):
        raise TypeError("body_lines harus berupa list")

    _fungsi_registry[name] = (arg_names, body_lines)


def load_fungsi_def(name):
    """
    Ambil definisi fungsi dari registry.
    :param name: nama fungsi
    :return: tuple (arg_names, body_lines)
    """
    if name not in _fungsi_registry:
        raise ValueError(f"Fungsi '{name}' tidak ditemukan di registry.")
    return _fungsi_registry[name]


def has_fungsi(name):
    """Cek apakah fungsi sudah ada di registry."""
    return name in _fungsi_registry


def list_fungsi():
    """Kembalikan daftar nama fungsi yang sudah terdaftar."""
    return list(_fungsi_registry.keys())


def clear_fungsi():
    """Hapus semua fungsi di registry (berguna untuk testing/refresh)."""
    _fungsi_registry.clear()


if __name__ == "__main__":
    # Registrasi contoh fungsi
    register_fungsi("tambah", ["a", "b"], ["kembalikan a + b"])
    register_fungsi("halo", ["nama"], ["gema 'Halo', nama"])

    # Debug print
    print("Daftar fungsi:", list_fungsi())
    print("Definisi 'tambah':", load_fungsi_def("tambah"))
    print("Definisi 'halo':", load_fungsi_def("halo"))
