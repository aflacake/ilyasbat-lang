# IlyasBat – Bahasa Prosedural Mini

> Beberapa pengerjaan proyek ini dibantu oleh generative AI.

Sudah menjadi bahasa pemrograman prosedural sederhana, ide karya turanan dari Earl. Memanfaatkan perintah-perintah mirip dengan bahasa pemrograman modern.

Kemampuan sederhananya dengan mengimpor modul, mengambil _input_, melakukan perhitungan, menangani percabangan dasar, dan mengakhiri program.

# Instalasi
## Diperlukan
- **Python versi terbaru**. Karena menggunakan teknologi ini. Jika belum terinstal, unduh Python [disini](https://www.python.org/downloads/).

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

# Lisensi
[Apache-2.0 license](https://github.com/aflacake/ilyasbat-lang/blob/main/LICENSE)
