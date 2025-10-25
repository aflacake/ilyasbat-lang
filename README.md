<p align="right">Bahasa: Indonesia</p>

![IlyasBat.png](https://raw.githubusercontent.com/aflacake/ilyasbat-lang/main/img/Logo%20IlyasBat%20New.png)
# IlyasBat – Bahasa Prosedural Mini

> Beberapa pengerjaan proyek ini dibantu oleh generative AI.

Sudah menjadi bahasa pemrograman prosedural sederhana, ide karya turanan dari Earl. Memanfaatkan perintah-perintah mirip dengan bahasa pemrograman modern.

Kemampuan sederhananya dengan mengimpor modul, mengambil _input_, melakukan perhitungan, menangani percabangan dasar, dan mengakhiri program.

# Instalasi
## Diperlukan
- **Python versi terbaru**. Karena menggunakan teknologi ini. Jika belum terinstal, unduh Python [disini](https://www.python.org/downloads/).

### Paket Pihak Ketiga
- Pasang `simpleeval`
  ```
  pip install simpleeval
  ```
- Pasang `colorama`, untuk warna teks cross-platform
  ```
  pip install colorama
  ```
- Pasang `pygments`, untuk syntax highlighting
  ```
  pip install pygments
  ```
- Pasang `prompt_toolkit`, buat REPL yang lebih interaktif
  ```
  pip install prompt_toolkit
  ```

## _Package_ Resmi
- Mendaftarkan paket resmi bagi helpers/impor.py
  ```
  cd ilyasbat-lang
  python -m helpers.impor testing/sapa.ibat
  ```

## 1. Manual via _Registry_ (Permanen, untuk seluruh sistem)
Hati-hati! Ini mengubah registry. Cadangkan dulu kalau perlu.
1. Jalankan CMD sebagai Administrator
2. Tambahkan file _association_:
   ```
   assoc .ibat=IbatScript
   ftype IbatScript="C:\jalur\ke\main.bat" "%%1"
   ```
   Ganti path ke lokasi `main.bat` milik Anda. Contoh:
   ```
   ftype IbatScript="C:\Users\anda\proyek\main.bat" "%%1"
   ```
## 2. Sementara (khusus satu sesi CMD)
Kalau hanya ingin sementara (tanpa ubah _registry_), di CMD:
```
assoc .ibat=IbatScript
ftype IbatScript="C:\jalur\ke\main.bat" "%%1"
```
Setelah tutup CMD, asosisasi ini hilang.

# Tutorial
## Pengujian Daftar Perintah di Jalur `tests/`
Cara menjalankan:
1. Direkomendasikan\
   Dari root proyek `ilyasbat-lang`,
   ```
   python -m tests.test_[NAMA_FILE]
   ```
2. Langsung\
   Kalau mau langsung jalan,
   ```
   python tests/test_[NAMA_FILE].py
   ```
   dengan syarat baris `sys.path.append(...)` tetap ada di atas.

# Lisensi
[Apache-2.0 license](https://github.com/aflacake/ilyasbat-lang/blob/main/LICENSE)
