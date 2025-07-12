# 🥗 Sistem Pre-Order (PO) Makanan Kantin Sekolah

Sistem ini dirancang untuk memudahkan proses pemesanan makanan dan minuman di kantin sekolah melalui metode *pre-order*. Siswa dapat memesan makanan H-1 sebelum dikonsumsi. Sistem ini bertujuan mengurangi antrean dan meningkatkan efisiensi layanan kantin.

---

## 🛠️ Teknologi yang Digunakan

- **Frontend**: Vue.js  
- **Backend**: Flask (Python)  
- **Database**: MySQL  
- **Session Management**: Redis (sesi login disimpan 1 hari penuh)  
- **Rate Limiting**: Flask-Limiter (maksimal 5 login per menit per IP)  
- **Scheduler**: APScheduler (untuk reset stok otomatis harian)

---

## 🔄 Alur Sistem PO Makanan Kantin

### 1. 🧑‍💻 Register dan Login
- Pengguna mendaftar dengan data pribadi.
- Login dibatasi maksimal 5x per menit per IP oleh Flask-Limiter.
- Sesi pengguna disimpan di Redis selama 1 hari.

### 2. 🍽️ Lihat Menu
- Siswa melihat daftar makanan yang tersedia (stok > 0).
- Gambar makanan diambil dari folder `uploads/menu`.

### 3. 🛒 Tambah ke Keranjang
- Siswa memilih makanan, menentukan jumlah, lalu menambahkan ke keranjang.

### 4. 📋 Lihat Keranjang dan Total
- Pengguna melihat isi keranjang dan total harga.
- Sistem otomatis memeriksa stok agar tidak melebihi kapasitas.

### 5. ✅ Lakukan Pemesanan (PO)
- PO hanya dapat dilakukan antara pukul **08:00 pagi - 07:59 esok harinya**.
- Pengguna mengunggah **bukti pembayaran**.
- Sistem:
  - Mengecek ulang stok
  - Menghitung total biaya
  - Mengubah status keranjang menjadi `ordered`
  - Mengurangi stok makanan
  - Menyimpan data pesanan

### 6. 📦 Lihat Status Pesanan
- Pengguna dapat melihat riwayat dan status pesanan mereka.

### 7. 🛠️ Admin Panel
- Melihat semua pesanan dari seluruh pengguna.
- Menambah, mengedit, atau mengarsipkan menu makanan.
- Stok makanan otomatis di-*reset* setiap hari pukul **08:00 pagi** via APScheduler.

---

## 🚀 Cara Menjalankan Proyek (Local)

### Backend (Flask):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate (Windows)
pip install -r requirements.txt
python app.py

### Frontend (Vue.js):
```bash
cd frontend
npm install
npm run serve
