# JobSeek Bot Automation

Script Python berbasis Selenium untuk membantu proses automasi lamaran kerja di platform **JobStreet** dan **Kalibrr**.

<div align="center" style="border:1px solid #e5e7eb; border-radius:12px; padding:16px; margin:12px 0;">
  <h2>Duwiaaw | Bot Automation Services</h2>
  <p><strong>Layanan pembuatan bot, web app, aplikasi custom, automasi workflow, scraper, serta layanan IT lainnya.</strong></p>
  <p>
    <a href="https://wa.me/6285157993801"><img alt="WhatsApp" src="https://img.shields.io/badge/WhatsApp-085157993801-22c55e?style=for-the-badge"></a>
    <a href="mailto:duwianjarariwibowo@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-duwianjarariwibowo%40gmail.com-f97316?style=for-the-badge"></a>
    <a href="https://daaw.online"><img alt="Website" src="https://img.shields.io/badge/Website-daaw.online-2563eb?style=for-the-badge"></a>
  </p>
  <p><em>Kontak cepat: <a href="https://wa.me/6285157993801">WhatsApp</a> | <a href="mailto:duwianjarariwibowo@gmail.com">Email</a> | <a href="https://daaw.online">Website</a></em></p>
</div>

> [!WARNING]
> Gunakan bot secara bijak dan pastikan sesuai Terms of Service platform terkait.

## Disclaimer
Gunakan script ini dengan tanggung jawab sendiri.
Pastikan penggunaan tidak melanggar Terms of Service platform yang dipakai.

## Fitur
### JobStreet
- Membuka halaman job board JobStreet.
- Klik "Lamaran Cepat" pada setiap loker yang ditemukan.
- Mengisi otomatis **surat lamaran (cover letter)** dengan template.
- Mengisi otomatis pertanyaan-pertanyaan umum dari rekruter.
- Menyimpan riwayat lamaran yang berhasil terkirim.

### Kalibrr
- Membuka halaman job board Kalibrr.
- Mencari tombol `Lamar Sekarang` secara otomatis.
- Klik `Kirimkan Profil` jika tersedia.
- Fallback buka tab baru saat elemen tidak ditemukan.
- Loop otomatis sampai durasi selesai.

## Struktur Repo
- `jobstreet_click.py`: script automasi untuk JobStreet.
- `kalibrr_click.py`: script automasi untuk Kalibrr.
- `requirements.txt`: daftar dependency Python.

## Prasyarat
- Google Chrome terpasang.
- Python 3.10+ (disarankan Python 3.11 atau lebih baru).
- Koneksi internet aktif.

## Quick Checklist Sebelum Run
- `git --version` berhasil.
- `python --version` (Windows) atau `python3 --version` (macOS/Linux) berhasil.
- Chrome sudah dijalankan dengan mode remote debugging di port `9222`.
- Sudah **login akun JobStreet/Kalibrr** di Chrome debug.
- CV/profil di platform terkait sudah terisi lengkap.

## 1. Install Python
Pilih sesuai device/OS.

### macOS
1. Download Python dari: https://www.python.org/downloads/
2. Install, lalu cek:

```bash
python3 --version
```

### Windows
1. Download Python dari: https://www.python.org/downloads/windows/
2. Saat install, centang **Add Python to PATH**.
3. Cek:

```powershell
python --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
```

## 2. Install Git
Cek dulu apakah Git sudah ada:

```bash
git --version
```

Jika belum ada, install sesuai OS:

### macOS
```bash
xcode-select --install
```

### Windows
- Download dan install Git dari: https://git-scm.com/download/win
- Setelah install, buka terminal baru lalu cek lagi `git --version`.

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y git
git --version
```

## 3. Clone Repo
### macOS
```bash
git clone https://github.com/Duwianjar/bot-apply-loker-kalibri.git
cd bot-apply-loker-kalibri
```

### Windows (PowerShell)
```powershell
git clone https://github.com/Duwianjar/bot-apply-loker-kalibri.git
cd bot-apply-loker-kalibri
```

### Linux
```bash
git clone https://github.com/Duwianjar/bot-apply-loker-kalibri.git
cd bot-apply-loker-kalibri
```

Catatan:
- Jangan pakai `cd : jobseek-bot` karena akan error.
- Jika muncul `warning: You appear to have cloned an empty repository.`, berarti repo GitHub belum ada isi/commit. Pastikan kamu clone repo yang benar dan branch default sudah berisi file project.

## 4. Buat Virtual Environment
### macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Jika muncul error execution policy saat aktivasi:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 5. Install Dependency (Selenium)
### macOS
```bash
python3 -m pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
python -m pip install -r requirements.txt
```

### Linux
```bash
python3 -m pip install -r requirements.txt
```

## 6. Buka Chrome Dengan Remote Debugging
Script ini butuh Chrome berjalan di port `9222` agar bisa terhubung ke sesi browser yang sudah login.

### macOS
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-jobseek
```

Catatan (macOS) jika ingin pakai **profile Chrome yang sudah login**:
- Chrome menolak `--remote-debugging-port` jika `--user-data-dir` menunjuk ke data default.
- Solusinya: copy data Chrome ke folder baru, lalu jalankan dengan `--profile-directory="Profile 2"`.

```bash
# 1) Copy data Chrome ke folder non-default
rsync -a "$HOME/Library/Application Support/Google/Chrome/" /tmp/chrome-jobseek/

# 2) Jalankan Chrome debug dengan profile yang diinginkan
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-jobseek \
  --profile-directory="Profile 2"

# 3) Cek port (harus keluar JSON)
curl http://127.0.0.1:9222/json/version
```

### Windows
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-jobseek"
```

Jika Chrome ada di `Program Files (x86)`, gunakan:

```powershell
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-jobseek"
```

### Linux
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-jobseek
```

Jika command `google-chrome` tidak ada, coba:

```bash
chromium-browser --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-jobseek
```

## 7. Jalankan Script
Sebelum menjalankan, pastikan **akun JobStreet atau Kalibrr sudah login** di Chrome yang dibuka dengan mode debug, dan data CV/profil sudah terisi lengkap.

Buka terminal baru (biarkan Chrome debug tetap hidup), lalu pilih script yang ingin dijalankan.

---

### A. Menjalankan Bot JobStreet
Script ini akan membuka URL JobStreet, mencari loker, dan mencoba melamar dengan "Lamaran Cepat".

#### macOS
```bash
.venv/bin/python jobstreet_click.py
```

#### Windows (PowerShell)
```powershell
python jobstreet_click.py
```

#### Linux
```bash
.venv/bin/python jobstreet_click.py
```

---

### B. Menjalankan Bot Kalibrr
Script ini akan membuka URL Kalibrr dan mengklik "Lamar Sekarang".

#### macOS
```bash
.venv/bin/python kalibrr_click.py
```

#### Windows (PowerShell)
```powershell
python kalibrr_click.py
```

#### Linux
```bash
.venv/bin/python kalibrr_click.py
```

---

### Kenapa tidak pakai `python3 nama_script.py`?
Di project ini, dependency dipasang di virtual environment `.venv`.
Command `python3` sering mengarah ke Python global/system, jadi package dari `.venv` tidak terbaca dan script bisa gagal (mis. `ModuleNotFoundError`).

Kalau tetap ingin menjalankan dengan `python3`, aktifkan dulu virtual environment:

```bash
# macOS/Linux
source .venv/bin/activate
python3 jobstreet_click.py

# Windows
.venv\Scripts\Activate.ps1
python jobstreet_click.py
```

## Contoh Output Saat Bot Jalan
Output di terminal akan bervariasi tergantung platform, namun contohnya seperti ini:

```text
# Contoh JobStreet
[INFO] Terhubung ke Chrome di port 9222
[INFO] Membuka halaman JobStreet...
[INFO] Job ID 12345: kartu loker diklik
[INFO] Job ID 12345: mengisi surat lamaran...
[INFO] Lamaran tersimpan: job-id=12345

# Contoh Kalibrr
[INFO] Connected to Chrome on 127.0.0.1:9222
[INFO] Membuka halaman job board Kalibrr...
[INFO] Menemukan tombol "Lamar Sekarang"
[INFO] Klik "Kirimkan Profil" berhasil
```

Jika muncul log berulang dan tidak ada error fatal, artinya bot sedang berjalan.

## Cara Stop Bot dan Keluar
- Stop bot: tekan `Ctrl+C` di terminal tempat script berjalan.
- Keluar virtual environment:
  - macOS/Linux: `deactivate`
  - Windows (PowerShell): `deactivate`

## Konfigurasi Cepat
### JobStreet
Untuk mengubah link pencarian kerja (misalnya berdasarkan filter tertentu):

1. Buka `jobstreet_click.py`.
2. Cari dan ganti URL di dalam fungsi `main`:
   ```python
   parser.add_argument(
       "--url",
       default="https://www.jobstreet.co.id/id/id/jobs",  # <-- GANTI URL DI SINI
       help="URL job board JobStreet yang akan dibuka.",
   )
   ```
3. Simpan file, lalu jalankan ulang script.

Template surat lamaran juga bisa diubah di dalam fungsi `_buat_teks_surat_lamaran`.

### Kalibrr
Untuk mengubah link pencarian kerja:

1. Buka `kalibrr_click.py`.
2. Ganti link di dalam `try...finally` block:
   ```python
   driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/1") # <-- GANTI URL DI SINI
   ```
3. Simpan file, lalu jalankan ulang script.

## Troubleshooting
- Error koneksi ke Chrome (`127.0.0.1:9222`):
  - Pastikan Chrome dijalankan dengan `--remote-debugging-port=9222`.
- `ModuleNotFoundError: selenium`:
  - Jalankan lagi `pip install -r requirements.txt` di virtual env aktif.
- ChromeDriver mismatch:
  - Update Chrome ke versi terbaru.
  - Update Selenium: `pip install -U selenium`.

## Catatan Device
- Script ini untuk desktop/laptop (Windows, macOS, Linux).
- Tidak didesain untuk Android/iOS native environment.
