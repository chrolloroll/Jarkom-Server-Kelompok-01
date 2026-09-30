# TCP Text & Matrix Service Server
### Kelompok 1


Proyek ini merupakan server TCP multi-client yang menyediakan 5 layanan ke client yang
terhubung: pengolahan teks (hitung jumlah karakter, hitung jumlah kata,
membalik string, menghapus huruf vokal) dan operasi matriks (determinan &
invers matriks 3x3). Server secara acak mengirim jawaban yang sengaja
dibuat salah untuk menguji logika verifikasi di sisi client — jika client
melaporkan suatu jawaban salah, layanan terkait langsung dinonaktifkan
untuk semua client, dan begitu seluruh layanan sudah nonaktif, server akan
berhenti dengan sendirinya.

Program ini dikembangkan sepenuhnya menggunakan Python 
dengan memanfaatkan standard library tanpa dependency eksternal. 
Komunikasi dilakukan melalui TCP socket dengan protokol khusus berbasis line-delimited JSON. 
Spesifikasi lengkap protokol (jenis pesan, sintaksis, semantik, dan aturan) didokumentasikan di
[`docs/PROTOCOL.md`](docs/PROTOCOL.md).

Program ini merupakan tugas kelompok untuk mata kuliah Jaringan Komputer.

### Requirements:
- Python 3.8 ke atas

### Cara menjalankan:
1. Install Python 3.8+ **jika belum ada** (https://www.python.org/downloads/).
2. Clone branch main dari repository berikut:
```
git clone https://github.com/chrolloroll/Jarkom-Server-Kelompok-01.git --branch=main
```
3. Masuk ke folder hasil clone.
4. Jalankan server dari root folder repository:
```
python3 src/server.py
```
   > Bagi pengguna Windows: gunakan `python` jika `python3` tidak dikenali.

5. (Opsional) Sesuaikan host, port, dan peluang jawaban salah:
```
python3 src/server.py --host 127.0.0.1 --port 8080 --corrupt-prob 0.5
```

| Argumen | Default | Keterangan |
|---|---|---|
| `--host` | `0.0.0.0` | Alamat IP tempat server mendengarkan koneksi |
| `--port` | `5000` | Port TCP yang digunakan |
| `--corrupt-prob` | `0.3` | Peluang (0.0–1.0) server sengaja mengirim jawaban salah |

6. Hentikan server dengan `Ctrl+C`, atau biarkan berhenti otomatis setelah
   kelima layanan sudah dinonaktifkan lewat feedback client.

### Contributors:
- [Aisyah Yasmina Huwaida (Inti server & integrasi)](https://github.com/chrolloroll)
- [Naufal Dzakiryah (Penanganan koneksi)](https://github.com/Hexagontal)
- [Naila Syakira (Layanan teks)](https://github.com/fishpenyet)
- [Andika Wahyu Dwi Saputra (Layanan matriks & penanganan ACK)](https://github.com/andumpss)
