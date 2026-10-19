# GuruCerdas AI

**Open source, gratis, dan tanpa login.** Tidak ada akun pengguna, paywall, atau fitur berbayar. Aplikasi dapat berjalan tanpa API key dalam mode template. Integrasi AI eksternal bersifat opsional dan hanya digunakan jika pengelola sendiri mengonfigurasi API key; layanan AI pihak ketiga mungkin mengenakan biaya.

GuruCerdas AI adalah MVP web app berbahasa Indonesia untuk membantu guru menyiapkan draf:
- Paket soal
- Kisi-kisi penilaian
- Lembar Kerja Peserta Didik (LKPD)
- Rubrik penilaian
- Bahan ajar

Guru memilih jenjang, mata pelajaran, topik, tujuan pembelajaran, dan opsi lainnya. Hasil dapat diedit di browser dan diunduh sebagai dokumen Word.

> **Penting:** keluaran aplikasi adalah draf. Guru wajib memeriksa akurasi, kesesuaian usia, tujuan pembelajaran, serta acuan kurikulum sebelum digunakan. Mode template tidak menghasilkan soal faktual lengkap secara otomatis.

## Prinsip proyek

- Gratis digunakan dan dikembangkan.
- Open source dengan lisensi MIT (lihat `LICENSE`).
- Tidak memerlukan login atau registrasi.
- Tidak menyimpan riwayat dokumen ke database; dokumen diproses saat sesi permintaan dan dapat diunduh pengguna.
- Mode template berjalan tanpa API key atau biaya layanan AI.
- Integrasi API AI opsional bukan layanan gratis yang dijamin; pemilik deployment bertanggung jawab atas biaya dan privasi API.

## Fitur MVP

- UI responsif untuk desktop dan ponsel
- Lima jenis dokumen pembelajaran
- Mode template tanpa API eksternal
- Mode generasi AI opsional melalui OpenAI API
- Edit hasil sebelum ekspor
- Unduh `.docx`
- Endpoint pemeriksaan kesehatan `/health`
- Docker dan Gunicorn untuk deployment

## Teknologi

- Python 3.12+
- Flask
- Jinja2 + CSS
- python-docx
- OpenAI Python SDK (opsional)

## Menjalankan secara lokal

### 1. Siapkan Python dan virtual environment

```bash
python -m venv .venv
```

Aktifkan environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### 2. Instal dependensi

```bash
pip install -r requirements.txt
```

### 3. Siapkan konfigurasi

Salin `.env.example` menjadi `.env`, lalu ubah `FLASK_SECRET_KEY` menjadi nilai acak yang panjang.

Aplikasi berjalan tanpa API key dalam mode template. Untuk mengaktifkan generasi AI eksternal, pengelola dapat mengisi `OPENAI_API_KEY`; ini opsional dan dapat menimbulkan biaya sesuai penyedia. Jangan pernah mengunggah file `.env` atau API key ke GitHub.

### 4. Jalankan

```bash
python app.py
```

Buka `http://127.0.0.1:5000`.

## Menjalankan dengan Docker

```bash
docker build -t gurucerdas-ai .
docker run --rm -p 5000:5000 --env-file .env gurucerdas-ai
```

Buka `http://127.0.0.1:5000`.

## Upload ke GitHub

Buat repository baru di GitHub, misalnya `gurucerdas-ai`. Dari folder proyek:

```bash
git init
git add .
git commit -m "Initial GuruCerdas AI MVP"
git branch -M main
git remote add origin https://github.com/USERNAME/gurucerdas-ai.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub Anda. Jangan tambahkan `.env` ke repository.

## Deployment

Aplikasi dapat dijalankan pada layanan hosting yang mendukung Python/Gunicorn atau Docker. Atur environment variables pada dashboard hosting:
- `FLASK_SECRET_KEY`
- `OPENAI_API_KEY` (opsional)
- `OPENAI_MODEL` (opsional)

Jangan menyimpan API key di source code. Pastikan penggunaan model AI sesuai anggaran dan kebijakan privasi.

## Struktur proyek

```text
gurucerdas-ai/
├── app.py
├── generator.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## Lisensi dan kontribusi

Proyek ini dirilis di bawah lisensi MIT. Pengguna bebas menggunakan, memodifikasi, dan mendistribusikan kode sesuai ketentuan lisensi. Kontribusi perbaikan dan template pembelajaran dipersilakan melalui pull request.

## Roadmap yang disarankan

1. Validasi dengan 5–10 guru.
2. Tambahkan template soal yang benar-benar spesifik per kelas dan mata pelajaran.
3. Tambahkan penyimpanan dokumen dan autentikasi.
4. Tambahkan bank soal dan ekspor PDF.
5. Tambahkan pengelolaan kelas, akun sekolah, dan pembatasan kuota.
6. Buat pembayaran setelah kebutuhan dan retensi tervalidasi.

## Batasan MVP

- Belum memiliki login dan penyimpanan dokumen permanen.
- Belum memiliki paket berbayar atau panel administrasi sekolah.
- Mode template menyediakan kerangka yang perlu dilengkapi, bukan konten tervalidasi.
- Mode AI memerlukan API key dan menimbulkan biaya penggunaan.
- Tidak menjamin kepatuhan penuh terhadap kurikulum atau dokumen resmi.
