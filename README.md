# Bot Apply Loker Kalibri

Script Python berbasis Selenium untuk membantu proses klik tombol **"Lamar Sekarang"** dan **"Kirimkan Profil"** di Kalibrr.

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
- Membuka halaman job board Kalibrr.
- Mencari tombol `Lamar Sekarang` secara otomatis.
- Klik `Kirimkan Profil` jika tersedia.
- Fallback buka tab baru saat elemen tidak ditemukan.
- Loop otomatis sampai durasi selesai.

## Struktur Repo
- `kalibrr_click.py`: script utama.
- `requirements.txt`: daftar dependency Python.

## Prasyarat
- Google Chrome terpasang.
- Python 3.10+ (disarankan Python 3.11 atau lebih baru).
- Koneksi internet aktif.

## Quick Checklist Sebelum Run
- `git --version` berhasil.
- `python --version` (Windows) atau `python3 --version` (macOS/Linux) berhasil.
- Chrome sudah dijalankan dengan mode remote debugging di port `9222`.
- Sudah login akun Kalibrr di Chrome debug.
- CV/profil Kalibrr sudah terisi lengkap.

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
- Jangan pakai `cd : bot-apply-loker-kalibri` karena akan error.
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
Script ini butuh Chrome berjalan di port `9222`.

### macOS
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-kalibrr
```

### Windows
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-kalibrr"
```

Jika Chrome ada di `Program Files (x86)`, gunakan:

```powershell
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-kalibrr"
```

### Linux
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-kalibrr
```

Jika command `google-chrome` tidak ada, coba:

```bash
chromium-browser --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-kalibrr
```

## 7. Jalankan Script
Sebelum menjalankan script, pastikan akun Kalibrr sudah login di Chrome yang dibuka dengan mode debug, dan data CV/profil sudah terisi lengkap.

Buka terminal baru (biarkan Chrome debug tetap hidup), lalu:

### macOS
```bash
python3 kalibrr_click.py
```

### Windows (PowerShell)
```powershell
python kalibrr_click.py
```

### Linux
```bash
python3 kalibrr_click.py
```

## Contoh Output Saat Bot Jalan
Contoh output normal di terminal (kurang lebih):

```text
[INFO] Connected to Chrome on 127.0.0.1:9222
[INFO] Membuka halaman job board Kalibrr...
[INFO] Menemukan tombol "Lamar Sekarang"
[INFO] Klik "Kirimkan Profil" berhasil
[INFO] Loop berikutnya...
```

Jika muncul log berulang dan tidak ada error fatal, artinya bot sedang berjalan.

## Cara Stop Bot dan Keluar
- Stop bot: tekan `Ctrl+C` di terminal tempat script berjalan.
- Keluar virtual environment:
  - macOS/Linux: `deactivate`
  - Windows (PowerShell): `deactivate`

## Cara Kerja Singkat
- Script akan mencoba run berulang selama ~50 menit (`total_seconds = 3000`).
- Tiap batch mencoba hingga 100 proses klik lamaran.
- Jika flow macet, script akan retry dengan tab baru.

## Konfigurasi Cepat
Edit parameter di bagian bawah `kalibrr_click.py`:
- `total_seconds = 3000` -> total waktu script berjalan.
- `buka_kalibrr_dan_klik_lamar(100, max_run_seconds=60)`:
  - `100` = jumlah loop per batch.
  - `60` = batas detik per batch sebelum restart.
- Link job board default:
  - `https://jobseeker.kalibrr.com/job-board/co/Indonesia/1`

### Ganti Link Sesuai Filter (Remote/Daerah/Job Tertentu)
1. Buka Kalibrr job board di browser.
2. Pilih filter yang kamu inginkan:
   - remote atau on-site
   - kota/daerah tertentu
   - posisi/job title tertentu
3. Setelah filter terpasang, copy URL dari address bar browser.
4. Buka `kalibrr_click.py`, lalu ganti link ini:
   - `driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/1")`
5. Simpan file, lalu jalankan ulang script.

Contoh:
```python
driver.get("PASTE_LINK_HASIL_FILTER_DI_SINI")
```

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
