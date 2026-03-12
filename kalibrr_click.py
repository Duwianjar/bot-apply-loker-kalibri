"""
Bot Apply Loker Kalibri
By Duwiaaw
Contact: 085157993801
Email: duwianjarariwibowo@gmail.com
Website: daaw.online
GitHub: github.com/Duwianjar
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time  
import webbrowser

SIGNATURE_BLOCK = '''"""
Bot Apply Loker Kalibri
By Duwiaaw
Contact: 085157993801
Email: duwianjarariwibowo@gmail.com
Website: daaw.online
GitHub: github.com/Duwianjar
"""'''


def _ensure_signature_block_present():
    with open(__file__, "r", encoding="utf-8") as f:
        content = f.read()
    if SIGNATURE_BLOCK not in content:
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(f"{SIGNATURE_BLOCK}\n\n{content.lstrip()}")
        print("Signature block tidak ditemukan. Signature otomatis ditambahkan di atas file.")
  

def _find_clickable(driver, selectors, max_wait=2.0, interval=0.2):
    end = time.monotonic() + max_wait
    last_el = None
    while time.monotonic() < end:
        for by, sel in selectors:
            try:
                els = driver.find_elements(by, sel)
                for el in els:
                    if el.is_displayed() and el.is_enabled():
                        return el
                if els:
                    last_el = els[0]
            except Exception:
                continue
        time.sleep(interval)
    return last_el if last_el and last_el.is_displayed() and last_el.is_enabled() else None


def _trim_tabs(driver, keep_last=5):
    try:
        handles = driver.window_handles
    except Exception:
        return
    if len(handles) <= keep_last:
        return

    current = driver.current_window_handle
    to_close = handles[:-keep_last]
    for h in to_close:
        if h != current:
            try:
                driver.switch_to.window(h)
                driver.close()
            except Exception:
                continue

    try:
        driver.switch_to.window(current)
    except Exception:
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception:
            pass


def _job_title_selectors_for_retry():
    return [
        (By.XPATH, "//div[contains(@class,'k-flex-1')]//a[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(ancestor::button) and not(ancestor::kb-location-filter) and not(contains(@class,'k-text-caption')) and not(ancestor::*[contains(@class,'k-text-caption')]) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))]"),
        (By.XPATH, "//div[contains(@class,'k-flex-1')]//div[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))] and not(ancestor::button) and not(ancestor::kb-location-filter) and not(ancestor::*[contains(@class,'k-text-caption')])]"),
        (By.XPATH, "//div[contains(@class,'k-font-bold') and contains(@class,'k-text-black') and contains(@class,'lg:k-flex') and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))]]"),
    ]


def _retry_click_job_title_until_lamar(driver, lamar_selectors, max_seconds=50):
    print("Sebelum buka tab baru, coba klik job title dulu sampai 50 detik...")
    retry_until = time.monotonic() + max_seconds
    job_selectors = _job_title_selectors_for_retry()
    lanjutkan_selectors = [
        (By.XPATH, "//a[normalize-space()='Terus lanjutkan']"),
        (By.XPATH, "//a[contains(@class,'k-btn-primary') and normalize-space()='Terus lanjutkan']"),
    ]
    while time.monotonic() < retry_until:
        lanjutkan_btn = _find_clickable(driver, lanjutkan_selectors, max_wait=0.8)
        if lanjutkan_btn:
            print("Terdeteksi tombol 'Terus lanjutkan', langsung buka tab baru.")
            return None, True

        lamar_btn = _find_clickable(driver, lamar_selectors, max_wait=1.0)
        if lamar_btn:
            print("Tombol 'Lamar Sekarang' ditemukan sebelum buka tab baru.")
            return lamar_btn, False

        job_title = _find_clickable(driver, job_selectors, max_wait=1.5)
        if job_title:
            try:
                child = job_title.find_elements(By.XPATH, ".//div")[0]
                driver.execute_script("arguments[0].click();", child)
            except Exception:
                driver.execute_script("arguments[0].click();", job_title)
            print("Klik job title (Odoo terdeteksi), lanjut klik Lamar1.")
        time.sleep(0.3)

    print("Sudah 50 detik klik job title terus, tetap tidak menemukan 'Lamar Sekarang'.")
    return None, False


def _open_job_board_new_tab(driver, lamar_selectors):
    retry_lamar_btn, force_open_now = _retry_click_job_title_until_lamar(
        driver, lamar_selectors, max_seconds=50
    )
    if retry_lamar_btn:
        return retry_lamar_btn, False

    if force_open_now:
        print("Bypass tunggu 50 detik karena tombol 'Terus lanjutkan' terdeteksi.")
    print("Tetap tidak menemukan 'Lamar Sekarang', buka tab baru...")
    try:
        driver.switch_to.new_window("tab")
        driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/te/full%20stack%20developer/1")
    except Exception:
        driver.execute_script("window.open('https://jobseeker.kalibrr.com/job-board/co/Indonesia/te/full%20stack%20developer/1', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
    time.sleep(0.2)
    _trim_tabs(driver, keep_last=5)
    return None, True


def buka_kalibrr_dan_klik_lamar(jumlah=100, max_run_seconds=300):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 10)
    print("Membuka halaman Kalibrr...")
    driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/te/full%20stack%20developer/1")

    stop_urls = [
        "https://jobseeker.kalibrr.com/c/astro-technologies-indonesia/jobs/263679/senior-data-engineer",
        "https://jobseeker.kalibrr.com/c/pt-bumi-amartha-teknologi-mandiri/jobs/263716/it-business-analyst-16",
    ]

    lamar_selectors = [
        (By.XPATH, "//button[normalize-space()='Lamar Sekarang']"),
        (By.XPATH, "//button[contains(@class,'k-btn-primary') and contains(normalize-space(.),'Lamar Sekarang')]"),
        (By.XPATH, "//a[normalize-space()='Lamar Sekarang']"),
    ] 

    submit_selectors = [
        (By.XPATH, "//button[.//span[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'kirimkan profil')]]"),
        (By.XPATH, "//button[.//span[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'kirimkan')]]"),
        (By.XPATH, "//*[self::button or self::a][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'kirimkan profil')]"),
        (By.XPATH, "//*[self::button or self::a][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit profile')]"),
    ]

    run_start = time.monotonic()
    for i in range(1, jumlah + 1):
        _trim_tabs(driver, keep_last=5)
        if time.monotonic() - run_start > max_run_seconds:
            print("Batas waktu run tercapai, restart dari awal...")
            return False
        try:
            print(f"Status: loop={i}, url={driver.current_url}, tabs={len(driver.window_handles)}")
        except Exception:
            print(f"Status: loop={i}, url=<unknown>, tabs=<unknown>")
        # Jika muncul dialog meninggalkan Kalibrr, klik "Batal" lebih awal
        try:
            leave_dialog = driver.find_elements(
                By.XPATH,
                "//h1[contains(normalize-space(.),'Anda akan meninggalkan Kalibrr.com.')]",
            )
            if leave_dialog:
                cancel_btn = _find_clickable(
                    driver,
                    [(By.XPATH, "//button[normalize-space()='Batal']")],
                    max_wait=3.0,
                )
                if cancel_btn:
                    driver.execute_script("arguments[0].click();", cancel_btn)
        except Exception:
            pass
        # Jika terhenti di halaman job detail tertentu, kembali ke job board
        cur = driver.current_url.split("?")[0]
        if cur in stop_urls:
            print("Terdeteksi halaman job detail, kembali ke job board...")
            driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/te/full%20stack%20developer/1")

        print(f"Proses ke-{i} dari {jumlah}")
        # Jika halaman mengandung kata "Odoo", klik job title tertentu
        try:
            page_has_odoo = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'odoo')]",
            )
            if page_has_odoo:
                print("Terdeteksi kata 'Odoo', klik job title terkait...")
                # Jika muncul dialog meninggalkan Kalibrr, klik "Batal" dulu
                try:
                    leave_dialog = driver.find_elements(
                        By.XPATH,
                        "//h1[contains(normalize-space(.),'Anda akan meninggalkan Kalibrr.com.')]",
                    )
                    if leave_dialog:
                        cancel_btn = _find_clickable(
                            driver,
                            [(By.XPATH, "//button[normalize-space()='Batal']")],
                            max_wait=2.0,
                        )
                        if cancel_btn:
                            driver.execute_script("arguments[0].click();", cancel_btn)
                except Exception:
                    pass

                # Jika ada Odoo, klik job title dulu baru lanjut klik "Lamar Sekarang"
                job_selectors = [
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//a[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(ancestor::button) and not(ancestor::kb-location-filter) and not(contains(@class,'k-text-caption')) and not(ancestor::*[contains(@class,'k-text-caption')]) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))]"),
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//div[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))] and not(ancestor::button) and not(ancestor::kb-location-filter) and not(ancestor::*[contains(@class,'k-text-caption')])]"),
                ]
                job_title = _find_clickable(driver, job_selectors, max_wait=10.0)
                if job_title:
                    try:
                        child = job_title.find_elements(By.XPATH, ".//div")[0]
                        driver.execute_script("arguments[0].click();", child)
                    except Exception:
                        driver.execute_script("arguments[0].click();", job_title)
                    print("Klik job title (Odoo terdeteksi), lanjut klik Lamar2.")
        except Exception:
            pass
        step_start = time.monotonic()
        step_limit = 20  # detik

        # Jika halaman berisi Odoo, klik job title dulu baru lanjut ke Lamar Sekarang
        odoo_clicked = False
        try:
            has_odoo = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'odoo')]",
            )
            if has_odoo:
                job_selectors = [
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//a[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(ancestor::button) and not(ancestor::kb-location-filter) and not(contains(@class,'k-text-caption')) and not(ancestor::*[contains(@class,'k-text-caption')]) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))]"),
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//div[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))] and not(ancestor::button) and not(ancestor::kb-location-filter) and not(ancestor::*[contains(@class,'k-text-caption')])]"),
                ]
                job_title = _find_clickable(driver, job_selectors, max_wait=10.0)
                if job_title:
                    try:
                        child = job_title.find_elements(By.XPATH, ".//div")[0]
                        driver.execute_script("arguments[0].click();", child)
                    except Exception:
                        driver.execute_script("arguments[0].click();", job_title)
                    print("Klik job title (Odoo terdeteksi), lanjut klik Lamar3.")
                    odoo_clicked = True
        except Exception:
            pass

        lamar_btn = _find_clickable(driver, lamar_selectors, max_wait=1.0)

        if not lamar_btn:
            # Jika ada banner "Lamaran terkirim", klik job title dulu lalu coba Lamar lagi
            try:
                sent_banner = driver.find_elements(
                    By.XPATH,
                    "//div[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lamaran terkirim')]",
                )
                if sent_banner:
                    print("Banner 'Lamaran terkirim' terdeteksi, klik job title lalu coba Lamar lagi...")
                    print("Menambahkan pengecualian judul job (banner 'Lamaran terkirim')...")
                    job_selectors = [
                        (By.XPATH, "//div[contains(@class,'k-flex-1')]//a[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(ancestor::button) and not(ancestor::kb-location-filter) and not(contains(@class,'k-text-caption')) and not(ancestor::*[contains(@class,'k-text-caption')]) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))]"),
                        (By.XPATH, "//div[contains(@class,'k-flex-1')]//div[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))] and not(ancestor::button) and not(ancestor::kb-location-filter) and not(ancestor::*[contains(@class,'k-text-caption')])]"),
                        # Fallback untuk judul job di luar k-flex-1
                        (By.XPATH, "//div[contains(@class,'k-font-bold') and contains(@class,'k-text-black') and contains(@class,'lg:k-flex') and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'cedar park')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'healthcare virtual assistant hva')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'digital marketere, ecommerce, multimedia editing')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'navigate_before')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'first_page'))]]"),
                    ]
                    retry_until = time.monotonic() + 50
                    while time.monotonic() < retry_until:
                        job_title = _find_clickable(driver, job_selectors, max_wait=2.0)
                        if job_title:
                            try:
                                child = job_title.find_elements(By.XPATH, ".//div")[0]
                                driver.execute_script("arguments[0].click();", child)
                            except Exception:
                                driver.execute_script("arguments[0].click();", job_title)
                            print("Klik job title setelah banner 'Lamaran terkirim'.")
                            time.sleep(0.3)
                            lamar_btn = _find_clickable(driver, lamar_selectors, max_wait=1.0)
                            if lamar_btn:
                                print("Tombol 'Lamar Sekarang' ditemukan setelah klik job title.")
                                break
                        time.sleep(0.3)

                    if not lamar_btn:
                        print("Sudah 50 detik klik job title, tetap tidak menemukan tombol 'Lamar Sekarang'.")
            except Exception:
                pass

            if not lamar_btn:
                lamar_btn, opened_new_tab = _open_job_board_new_tab(driver, lamar_selectors)
                if not lamar_btn and not opened_new_tab:
                    print("Tidak menemukan 'Lamar Sekarang' meski retry, lanjut loop berikutnya.")
                    continue
                if opened_new_tab:
                    # lanjut ke iterasi berikutnya (ulang dari tab baru)
                    continue
                # lanjut ke iterasi berikutnya (ulang dari tab baru)

        print("Klik tombol 'Lamar Sekarang'...")
        driver.execute_script("arguments[0].click();", lamar_btn)

        print("Menunggu tombol 'Kirimkan Profil' muncul...")
        submit_btn = _find_clickable(driver, submit_selectors, max_wait=2.0)

        if not submit_btn:
            print("Tombol 'Kirimkan Profil' tidak ditemukan, cek dialog 'Batal' dan job title...")
            # Klik job title jika ada, lalu coba cari "Kirimkan Profil" lagi
            try:
                # Coba klik elemen job title berdasarkan class
                job_selectors = [
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//a[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(ancestor::button) and not(ancestor::kb-location-filter) and not(contains(@class,'k-text-caption')) and not(ancestor::*[contains(@class,'k-text-caption')]) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))]"),
                    (By.XPATH, "//div[contains(@class,'k-flex-1')]//div[(contains(@class,'k-font-bold') or contains(@class,'k-text-black')) and .//div[normalize-space()!='Partner Growth & Enablement Executive' and normalize-space()!='Business Analyst' and normalize-space()!='Terapkan Filter' and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tangerang')) and not(contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'penuh waktu'))] and not(ancestor::button) and not(ancestor::kb-location-filter) and not(ancestor::*[contains(@class,'k-text-caption')])]"),
                ]
                job_title = _find_clickable(driver, job_selectors, max_wait=10.0)
                if job_title:
                    # Klik child div agar lebih tepat ke judulnya
                    try:
                        child = job_title.find_elements(By.XPATH, ".//div")[0]
                        driver.execute_script("arguments[0].click();", child)
                    except Exception:
                        driver.execute_script("arguments[0].click();", job_title)
                    print("Berhasil klik job title setelah 'Batal'.")
                    # Setelah klik job title, klik "Lamar Sekarang" lalu "Kirimkan Profil"
                    time.sleep(0.5)
                    lamar_after = _find_clickable(driver, lamar_selectors, max_wait=3.0)
                    if lamar_after:
                        driver.execute_script("arguments[0].click();", lamar_after)
                        time.sleep(0.5)
                        submit_after = _find_clickable(driver, submit_selectors, max_wait=3.0)
                        if submit_after:
                            driver.execute_script("arguments[0].click();", submit_after)
                        else:
                            print("Setelah klik job title, tombol 'Kirimkan Profil' tidak ditemukan.")
                    else:
                        print("Setelah klik job title, tombol 'Lamar Sekarang' tidak ditemukan.")
                else:
                    print("Gagal menemukan job title setelah 'Batal'.")
            except Exception:
                print("Gagal klik job title setelah 'Batal'.")

            submit_btn = _find_clickable(driver, submit_selectors, max_wait=2.0)
            if not submit_btn:
                print("Masih tidak menemukan 'Kirimkan Profil', buka tab baru dan ulangi...")
                _, opened_new_tab = _open_job_board_new_tab(driver, lamar_selectors)
                if opened_new_tab:
                    continue
                submit_btn = _find_clickable(driver, submit_selectors, max_wait=1.0)
                if not submit_btn:
                    continue

        driver.execute_script("arguments[0].click();", submit_btn)
        # Beri jeda singkat agar klik ter-register sebelum membuka tab baru
        time.sleep(0.5)

        # Jika langkah ini terlalu lama, buka tab baru dan ulangi proses
        if time.monotonic() - step_start > step_limit:
            print("Langkah terlalu lama, buka tab baru dan ulangi...")
            _, opened_new_tab = _open_job_board_new_tab(driver, lamar_selectors)
            if opened_new_tab:
                continue

        # Jika muncul banner "Lamaran terkirim", kembali ke job board
        try:
            banner = driver.find_elements(
                By.XPATH,
                "//div[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lamaran terkirim')]",
            )
            if banner:
                print("Banner 'Lamaran terkirim' terdeteksi, kembali ke job board...")
                driver.get("https://jobseeker.kalibrr.com/job-board/co/Indonesia/te/full%20stack%20developer/1")
        except Exception:
            pass

        if i < jumlah:
            print("Buka tab baru ke job board untuk proses berikutnya...")
            _open_job_board_new_tab(driver, lamar_selectors)

    print("Selesai.")
    return True

if __name__ == "__main__":
    _ensure_signature_block_present()
    total_seconds = 3000  # 50 menit
    start = time.monotonic()
    while time.monotonic() - start < total_seconds:
        try:
            # Jika proses terasa hang, akan restart lewat max_run_seconds
            selesai = buka_kalibrr_dan_klik_lamar(100, max_run_seconds=60)
            if selesai:
                # lanjut sampai 50 menit habis
                continue
        except Exception as e:
            print(f"Error: {e}. Restart dari awal...")
            continue
    print("Waktu proses habis, membuka https://daaw.online ...")
    webbrowser.open("https://daaw.online")
    print("Selesai 50 menit.")
