"""
Bot Apply JobStreet
By Duwiaaw
"""

import time
import sys
import argparse
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

YEARS_2_PREFERENCES = [
    "2 years",
    "2 year",
    "2 yrs",
    "2 tahun",
    "dua tahun",
]
SYSTEMS_ADMIN_KEYWORDS = [
    "systems administrator",
    "system administrator",
    "sysadmin",
]

# Performa
FAST_MODE = True
TURBO_MODE = True
SLEEP_FACTOR = 0.12 if TURBO_MODE else (0.20 if FAST_MODE else 1.0)
MIN_SLEEP = 0.01 if TURBO_MODE else 0.02
LAMARAN_TERKIRIM = []
STOP_DUE_TO_LIMIT = False


def _sleep(seconds):
    time.sleep(max(MIN_SLEEP, seconds * SLEEP_FACTOR))


def _print_hijau(msg):
    print(f"{GREEN}{msg}{RESET}")


def _print_kuning(msg):
    print(f"{YELLOW}{msg}{RESET}")


def _print_merah(msg):
    print(f"{RED}{msg}{RESET}")


def _find_clickable(driver, selectors, max_wait=1.6, interval=0.1):
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
        _sleep(interval)
    return last_el if last_el and last_el.is_displayed() and last_el.is_enabled() else None


def _ambil_job_ids_dari_halaman(driver):
    ids = []
    cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='job-card'][data-job-id]")
    for card in cards:
        try:
            job_id = card.get_attribute("data-job-id")
            if job_id and job_id not in ids:
                ids.append(job_id)
        except Exception:
            continue
    return ids


def _ambil_ringkasan_job_dari_halaman(driver):
    ringkasan = []
    cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='job-card'][data-job-id]")
    for card in cards:
        try:
            job_id = (card.get_attribute("data-job-id") or "").strip()
        except Exception:
            job_id = ""
        if not job_id:
            continue

        title = "-"
        company = "-"
        try:
            title_el = card.find_elements(By.CSS_SELECTOR, "a[data-testid='job-card-title']")
            if title_el:
                t = (title_el[0].text or "").strip()
                if t:
                    title = t
        except Exception:
            pass
        try:
            company_el = card.find_elements(By.CSS_SELECTOR, "a[data-automation='jobCompany']")
            if company_el:
                c = (company_el[0].text or "").strip()
                if c:
                    company = c
        except Exception:
            pass
        ringkasan.append({"job_id": job_id, "title": title, "company": company})
    return ringkasan


def _ambil_info_card(card):
    title = "-"
    href = "-"
    try:
        title_links = card.find_elements(By.CSS_SELECTOR, "a[data-testid='job-card-title'], a[data-automation='jobTitle']")
        for link in title_links:
            txt = (link.text or "").strip()
            if txt:
                title = txt
                break
    except Exception:
        pass
    try:
        link = card.find_elements(By.CSS_SELECTOR, "a[data-testid='job-list-item-link-overlay'], a[data-automation='job-list-item-link-overlay']")
        if link:
            val = (link[0].get_attribute("href") or "").strip()
            if val:
                href = val
    except Exception:
        pass
    return title, href


def _is_initial_view_terlihat(driver):
    try:
        initial = driver.find_elements(By.CSS_SELECTOR, "[data-automation='initialView']")
    except Exception:
        initial = []
    for el in initial:
        try:
            if el.is_displayed():
                return True
        except Exception:
            continue
    return False


def _panel_kanan_sudah_detail_job(driver, job_id):
    """
    True jika split view kanan sudah menampilkan detail job yang sesuai job_id
    (bukan state awal 'Pilih lowongan kerja').
    """
    if _is_initial_view_terlihat(driver):
        return False
    try:
        wrappers = driver.find_elements(By.CSS_SELECTOR, "[data-automation='splitViewJobDetailsWrapper']")
        if not wrappers:
            return False
    except Exception:
        return False

    # Verifikasi detail aktif sesuai job_id
    try:
        anchors = driver.find_elements(
            By.XPATH,
            f"//*[@data-automation='splitViewJobDetailsWrapper']//a[contains(@href,'/id/job/{job_id}') or contains(@href,'/job/{job_id}')]",
        )
        for a in anchors:
            try:
                if a.is_displayed():
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _wait_detail_panel(driver, job_id, max_wait=1.8, interval=0.1):
    end = time.monotonic() + max_wait
    while time.monotonic() < end:
        if _panel_kanan_sudah_detail_job(driver, job_id):
            return True
        _sleep(interval)
    return False


def _klik_job_card_presisi(driver, job_id, max_wait=4.0):
    """
    Klik presisi hanya pada card job yang sesuai job_id.
    Hindari salah klik ke komponen lain (summary/sort/filter).
    """
    end = time.monotonic() + max_wait
    card_css = f"article[data-testid='job-card'][data-job-id='{job_id}']"
    while time.monotonic() < end:
        wrapper = None
        try:
            wrappers = driver.find_elements(By.CSS_SELECTOR, f"div[data-search-sol-meta*='\\\"jobId\\\":\\\"{job_id}\\\"']")
            if wrappers:
                wrapper = wrappers[0]
        except Exception:
            wrapper = None

        cards = []
        if wrapper:
            try:
                cards = wrapper.find_elements(By.CSS_SELECTOR, card_css)
            except Exception:
                cards = []
        if not cards:
            try:
                cards = driver.find_elements(By.CSS_SELECTOR, card_css)
            except Exception:
                cards = []
        if not cards:
            _sleep(0.12)
            continue

        card = cards[0]
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
        except Exception:
            pass

        title, href = _ambil_info_card(card)

        # Prioritas klik overlay link di dalam card yang target self.
        clicked = False
        clicked_via = ""
        for sel in (
            "a[data-testid='job-list-item-link-overlay'][target='_self']",
            "a[data-automation='job-list-item-link-overlay'][target='_self']",
            "a[data-testid='job-list-item-link-overlay']",
            "a[data-automation='job-list-item-link-overlay']",
            "a[data-testid='job-card-title']",
            "a[data-automation='jobTitle']",
        ):
            try:
                links = card.find_elements(By.CSS_SELECTOR, sel)
            except Exception:
                links = []
            for link in links:
                try:
                    if not link.is_displayed() or not link.is_enabled():
                        continue
                    if not _click_el(driver, link):
                        continue
                    clicked = True
                    clicked_via = sel
                    break
                except Exception:
                    continue
            if clicked:
                break

        # Fallback tetap di komponen card/wrapper yang sesuai job_id.
        if not clicked:
            try:
                if _click_el(driver, card):
                    clicked = True
                    clicked_via = "article[data-testid='job-card']"
            except Exception:
                if wrapper:
                    try:
                        if _click_el(driver, wrapper):
                            clicked = True
                            clicked_via = "div[data-search-sol-meta]"
                    except Exception:
                        clicked = False

        if clicked:
            print(
                f"Job ID {job_id}: kartu loker diklik via {clicked_via} | "
                f"title='{title}' | href='{href}'"
            )
            if _wait_detail_panel(driver, job_id, max_wait=1.8, interval=0.1):
                _sleep(0.15)
                return True
            print(
                f"Job ID {job_id}: klik terdeteksi tapi panel kanan belum tampil detail job "
                "(masih initialView/salah fokus), retry..."
            )

        _sleep(0.12)
    return False


def _detail_job_sesuai_id(driver, job_id):
    try:
        anchors = driver.find_elements(By.XPATH, f"//a[contains(@href,'/job/{job_id}')]")
        for a in anchors:
            if a.is_displayed():
                return True
    except Exception:
        pass
    return False


def _switch_ke_tab_apply(driver, max_wait=12.0, interval=0.25):
    """Sukses jika ada tab aktif/baru dengan URL yang mengandung /apply."""
    end = time.monotonic() + max_wait
    while time.monotonic() < end:
        try:
            handles = list(driver.window_handles)
        except Exception:
            handles = []

        for handle in handles:
            try:
                driver.switch_to.window(handle)
                current = driver.current_url or ""
                if "/apply" in current:
                    return True
            except Exception:
                continue
        _sleep(interval)
    return False


def _switch_ke_tab_baru_atau_apply(driver, before_handles, max_wait=10.0, interval=0.25):
    """
    Sukses jika:
    - muncul tab baru lalu URL tab tersebut mengandung /apply, atau
    - salah satu tab (fallback) mengandung /apply.
    """
    end = time.monotonic() + max_wait
    before = set(before_handles or [])
    while time.monotonic() < end:
        try:
            handles = list(driver.window_handles)
        except Exception:
            handles = []

        new_handles = [h for h in handles if h not in before]
        if new_handles:
            try:
                driver.switch_to.window(new_handles[-1])
                current = driver.current_url or ""
                if "/apply" in current:
                    return True
            except Exception:
                pass

        if _switch_ke_tab_apply(driver, max_wait=0.8, interval=0.2):
            return True
        _sleep(interval)
    return False


def _sudah_pernah_melamar(driver, max_wait=3.0, interval=0.25):
    end = time.monotonic() + max_wait
    while time.monotonic() < end:
        try:
            badges = driver.find_elements(
                By.XPATH,
                "//span[contains(normalize-space(.),'Kamu telah mengirimkan lamaran pada')"
                " or contains(normalize-space(.),'You have applied')]",
            )
            for b in badges:
                txt = (b.text or "").strip()
                if (
                    "Kamu telah mengirimkan lamaran pada" in txt
                    or "You have applied" in txt
                ):
                    return True, txt
        except Exception:
            pass
        _sleep(interval)
    return False, ""


def _log_detail_job_sebelum_lamar(driver, job_id):
    """Log detail job aktif sebelum klik tombol Lamaran Cepat."""
    try:
        title_el = _find_clickable(
            driver,
            [(By.CSS_SELECTOR, "h1[data-automation='job-detail-title']")],
            max_wait=8.0,
        )
        title = title_el.text.strip() if title_el else "-"
    except Exception:
        title = "-"

    try:
        company_el = _find_clickable(
            driver,
            [(By.CSS_SELECTOR, "[data-automation='advertiser-name']")],
            max_wait=3.0,
        )
        company = company_el.text.strip() if company_el else "-"
    except Exception:
        company = "-"

    try:
        location_el = _find_clickable(
            driver,
            [(By.CSS_SELECTOR, "[data-automation='job-detail-location']")],
            max_wait=3.0,
        )
        location = location_el.text.strip() if location_el else "-"
    except Exception:
        location = "-"

    apply_href = "-"
    has_apply_path = False
    try:
        apply_anchors = driver.find_elements(By.CSS_SELECTOR, "a[data-automation='job-detail-apply']")
        for a in apply_anchors:
            href = (a.get_attribute("href") or "").strip()
            if href:
                apply_href = href
                if "/apply" in href:
                    has_apply_path = True
                    break
    except Exception:
        pass

    print(f"Job ID {job_id}: detail sebelum klik Lamaran Cepat")
    print(f"  - Judul      : {title}")
    print(f"  - Perusahaan : {company}")
    print(f"  - Lokasi     : {location}")
    print(f"  - Apply URL  : {apply_href}")
    print(f"  - URL apply? : {'YA' if has_apply_path else 'TIDAK'}")


def _ambil_judul_job_detail(driver):
    try:
        title_el = _find_clickable(
            driver,
            [(By.CSS_SELECTOR, "h1[data-automation='job-detail-title']")],
            max_wait=4.0,
        )
        if title_el:
            txt = (title_el.text or "").strip()
            if txt:
                return txt
    except Exception:
        pass
    return "-"


def _ambil_company_job_detail(driver):
    try:
        company_el = _find_clickable(
            driver,
            [(By.CSS_SELECTOR, "[data-automation='advertiser-name']")],
            max_wait=3.0,
        )
        if company_el:
            txt = (company_el.text or "").strip()
            if txt:
                return txt
    except Exception:
        pass
    return "-"


def _buat_teks_surat_lamaran(job_title, company):
    posisi = (job_title or "this position").strip()
    perusahaan = (company or "your company").strip()
    return (
        f"Dear Recruitment Team at {perusahaan},\n\n"
        f"My name is Duwi Anjar Ari Wibowo, and I graduated in Informatics from Universitas Ahmad Dahlan "
        f"(GPA 3.72). I am applying for the {posisi} role. I have hands-on experience as a Full Stack "
        "Developer, focusing on web and mobile application development using Laravel, JavaScript, Flutter, "
        "MySQL, and PostgreSQL.\n\n"
        "In my most recent role at PT. Radiator Springs Indonesia, I built and maintained internal systems "
        "such as Web SSO, warranty systems, and backend-integrated mobile applications, including IoT (BLE) "
        "communication. I am used to requirement analysis, feature implementation, debugging, and team "
        "collaboration to ensure applications are stable, secure, and efficient.\n\n"
        "I also hold JAVA IT Development Full Stack and Junior Network Administrator certifications, which "
        "support both my software development and infrastructure capabilities.\n\n"
        "I would welcome the opportunity to contribute and grow with your team. Thank you for your time and "
        "consideration.\n\n"
        "Sincerely,\n"
        "Duwi Anjar Ari Wibowo\n"
        "duwianjarariwibowo@gmail.com | +6282220649676"
    )


def _set_cover_letter_text(driver, text_area, cover_text):
    try:
        driver.execute_script(
            "const el = arguments[0];"
            "const val = arguments[1];"
            "const setter = Object.getOwnPropertyDescriptor("
            "window.HTMLTextAreaElement.prototype, 'value').set;"
            "setter.call(el, val);"
            "el.dispatchEvent(new Event('input', {bubbles:true}));"
            "el.dispatchEvent(new Event('change', {bubbles:true}));",
            text_area,
            cover_text,
        )
        return True
    except Exception:
        try:
            text_area.clear()
        except Exception:
            pass
        try:
            text_area.send_keys(cover_text)
            return True
        except Exception:
            return False


def _get_textarea_value(driver, text_area):
    val = ""
    try:
        val = (text_area.get_attribute("value") or "").strip()
    except Exception:
        val = ""
    if val:
        return val
    try:
        val = (driver.execute_script("return (arguments[0].value || '').toString();", text_area) or "").strip()
    except Exception:
        val = ""
    return val


def _get_cover_letter_textarea(driver, max_wait=2.0, interval=0.1):
    selectors = [
        (By.CSS_SELECTOR, "textarea[data-testid='coverLetterTextInput']"),
        (By.XPATH, "//textarea[contains(@aria-label,'Tulis surat lamaran')]"),
    ]
    end = time.monotonic() + max_wait
    last = None
    while time.monotonic() < end:
        for by, sel in selectors:
            try:
                els = driver.find_elements(by, sel)
            except Exception:
                continue
            for el in els:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    continue
            if els:
                last = els[0]
        _sleep(interval)
    return last


def _isi_cover_letter_dan_verifikasi(driver, cover_text, min_len=80, max_attempts=3):
    last_val = ""
    for _ in range(max_attempts):
        text_area = _get_cover_letter_textarea(driver, max_wait=2.0)
        if not text_area:
            return False, ""
        if not _set_cover_letter_text(driver, text_area, cover_text):
            continue
        try:
            driver.execute_script(
                "const el = arguments[0];"
                "el.focus();"
                "el.dispatchEvent(new Event('input', {bubbles:true}));"
                "el.dispatchEvent(new Event('change', {bubbles:true}));"
                "el.blur();"
                "el.dispatchEvent(new Event('blur', {bubbles:true}));",
                text_area,
            )
        except Exception:
            pass
        # Trigger input keyboard agar field dianggap "tersentuh"/terisi oleh UI.
        try:
            text_area.click()
            text_area.send_keys(Keys.END, " ")
            text_area.send_keys(Keys.BACKSPACE)
            text_area.send_keys(Keys.ENTER)
        except Exception:
            pass
        _sleep(0.18)
        last_val = _get_textarea_value(driver, text_area)
        if len((last_val or "").strip()) >= min_len:
            return True, (last_val or "").strip()
    return False, (last_val or "").strip()


def _cover_letter_wajib_error(messages):
    msgs = [_norm_text(m) for m in (messages or []) if m]
    for m in msgs:
        if "surat lamaran" in m and ("wajib diisi" in m or "silakan buat seleksi" in m):
            return True
    return False


def _submit_limit_error_messages(driver, max_wait=4.0, interval=0.2):
    """
    Cek error panel sesaat setelah klik submit.
    Jika muncul error umum server/limit, kembalikan messages.
    """
    end = time.monotonic() + max_wait
    while time.monotonic() < end:
        messages = _ambil_error_panel_messages(driver)
        if messages:
            joined = _norm_text(" | ".join(messages))
            if (
                "terjadi kesalahan" in joined
                or "silakan coba lagi" in joined
                or "hubungi layanan pelanggan" in joined
            ):
                return messages
        _sleep(interval)
    return []


def _simpan_lamaran_terkirim(job_id, job_title):
    title = (job_title or "-").strip() or "-"
    for item in LAMARAN_TERKIRIM:
        if item.get("job_id") == job_id:
            if title != "-" and item.get("job_title", "-") == "-":
                item["job_title"] = title
            return
    LAMARAN_TERKIRIM.append({"job_id": job_id, "job_title": title})


def _log_rekap_lamaran_terkirim_hijau():
    total = len(LAMARAN_TERKIRIM)
    _print_hijau("REKAP LAMARAN TERKIRIM:")
    for i, item in enumerate(LAMARAN_TERKIRIM, start=1):
        _print_hijau(
            f"  {i}. job-id={item['job_id']} | loker={item.get('job_title', '-')}"
        )
    _print_hijau(f"TOTAL LAMARAN TERKIRIM: {total}")


def _click_el(driver, el):
    try:
        driver.execute_script("arguments[0].click();", el)
        return True
    except Exception:
        try:
            el.click()
            return True
        except Exception:
            return False


def _norm_text(s):
    return " ".join((s or "").split()).strip().lower()


def _teks_terlihat_elemen(el):
    txt = ""
    try:
        txt = (el.text or "").strip()
    except Exception:
        txt = ""
    if txt:
        return txt
    # fallback kalau text ada di child span
    try:
        spans = el.find_elements(By.XPATH, ".//*[self::span or self::div]")
        for sp in spans:
            t = (sp.text or "").strip()
            if t:
                return t
    except Exception:
        pass
    return ""


def _log_target_lamaran_cepat(job_id, attempt, el):
    try:
        tag = el.tag_name
    except Exception:
        tag = "?"
    try:
        href = (el.get_attribute("href") or "").strip()
    except Exception:
        href = ""
    try:
        aria = (el.get_attribute("aria-label") or "").strip()
    except Exception:
        aria = ""
    text = _teks_terlihat_elemen(el)
    try:
        outer = (el.get_attribute("outerHTML") or "").strip().replace("\n", " ")
        outer = outer[:220] + ("..." if len(outer) > 220 else "")
    except Exception:
        outer = ""
    print(f"Job ID {job_id}: target klik Lamaran Cepat (attempt={attempt})")
    print(f"  - tag       : {tag}")
    print(f"  - text      : {text}")
    print(f"  - aria-label: {aria}")
    print(f"  - href      : {href}")
    if outer:
        print(f"  - outerHTML : {outer}")


def _find_lamaran_cepat_button(driver, max_wait=10.0):
    end = time.monotonic() + max_wait
    selectors = [
        (By.XPATH, "//a[@data-automation='job-detail-apply']"),
        (By.XPATH, "//a[contains(@data-automation,'apply')]"),
        (By.XPATH, "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lamaran cepat')]"),
        (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'lamaran cepat')]"),
    ]
    while time.monotonic() < end:
        candidates = []
        for by, sel in selectors:
            try:
                candidates.extend(driver.find_elements(by, sel))
            except Exception:
                continue

        seen = set()
        for el in candidates:
            try:
                if not el.is_displayed() or not el.is_enabled():
                    continue
            except Exception:
                continue
            try:
                eid = el.id
            except Exception:
                eid = None
            if eid and eid in seen:
                continue
            if eid:
                seen.add(eid)

            text = _norm_text(_teks_terlihat_elemen(el))
            if "lamaran cepat" in text:
                return el
        _sleep(0.2)
    return None


def _pilih_opsi_terlihat(driver, preferred_texts=None):
    preferred = [_norm_text(x) for x in (preferred_texts or []) if x]
    try:
        options = driver.find_elements(
            By.XPATH,
            "//*[@role='option' and not(@aria-disabled='true')]",
        )
    except Exception:
        return False, ""

    visible = []
    for op in options:
        try:
            if op.is_displayed() and op.is_enabled():
                visible.append(op)
        except Exception:
            continue

    if not visible:
        return False, ""

    for pref in preferred:
        for op in visible:
            text = _norm_text(_teks_terlihat_elemen(op))
            if pref and pref in text and _click_el(driver, op):
                return True, _teks_terlihat_elemen(op)

    for op in visible:
        if _click_el(driver, op):
            return True, _teks_terlihat_elemen(op)
    return False, ""


def _set_native_select_by_preferences(driver, select_el, preferred_texts):
    """
    Set native <select> value by preferred labels, then fire change/input events.
    """
    prefs = [_norm_text(x) for x in (preferred_texts or []) if x]
    try:
        sel = Select(select_el)
    except Exception:
        return False, ""

    options = sel.options or []
    chosen_text = ""

    # 1) exact/contains match against preferred labels
    for pref in prefs:
        for opt in options:
            txt = _norm_text(opt.text or "")
            val = (opt.get_attribute("value") or "").strip()
            if not txt or not val:
                continue
            if txt == pref or pref in txt:
                try:
                    sel.select_by_visible_text(opt.text)
                    chosen_text = (opt.text or "").strip()
                    driver.execute_script(
                        "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
                        "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                        select_el,
                    )
                    return True, chosen_text
                except Exception:
                    continue

    # 2) fallback first valid non-empty option
    for opt in options:
        txt = (opt.text or "").strip()
        val = (opt.get_attribute("value") or "").strip()
        if not txt or not val:
            continue
        try:
            sel.select_by_visible_text(opt.text)
            chosen_text = txt
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                select_el,
            )
            return True, chosen_text
        except Exception:
            continue
    return False, ""


def _infer_preferences_from_question(question_text):
    """
    Heuristik adaptif berdasarkan teks pertanyaan.
    Return dict berisi preferensi untuk radio/checkbox/dropdown.
    """
    q = _norm_text(question_text)
    prefs = {
        "radio": [],
        "checkbox": [],
        "dropdown": [],
    }

    # Experience-related
    if "how many years" in q or "berapa tahun" in q or "experience" in q or "pengalaman" in q:
        prefs["dropdown"] = YEARS_2_PREFERENCES.copy()

    # Qualification / education
    if "kualifikasi" in q or "qualification" in q or "degree" in q or "pendidikan" in q:
        prefs["dropdown"] = prefs["dropdown"] + ["sarjana (s1)", "bachelor degree (s1)", "s1"]

    # Certification level questions (contoh: Cisco collaboration certification)
    if "certification" in q or "sertifikasi" in q or "highest level" in q:
        prefs["dropdown"] = prefs["dropdown"] + [
            "none",
            "not certified",
            "belum memiliki",
            "tidak ada",
            "no certification",
            "associate",
            "entry",
        ]

    # Expected salary heuristik: pilih kisaran menengah aman.
    if "gaji bulanan" in q or "expected monthly basic salary" in q or "expected salary" in q:
        prefs["dropdown"] = prefs["dropdown"] + ["rp 5 jt", "rp 6 jt", "rp 7 jt"]

    # English proficiency (checkbox/radio style)
    if "bahasa inggris" in q or "english language skills" in q:
        prefs["checkbox"] = [
            "berbicara dengan mahir",
            "speaks proficiently",
            "menulis dengan mahir",
            "writes proficiently",
        ]
        prefs["radio"] = ["mahir", "proficient", "baik", "good"]

    # Willingness questions -> prefer Yes
    yes_keywords = [
        "bersedia",
        "willing",
        "outside your usual hours",
        "luar jam kerja",
        "bepergian",
        "travel",
        "background check",
        "latar belakang",
        "technical writing",
        "do you have experience in an administration role",
        "experience in an administration role",
        "pengalaman dalam peran administrasi",
        "pengalaman di posisi administrasi",
        "scrum agile team",
        "scrum agile",
        "berpengalaman bekerja dalam scrum agile team",
        "software development lifecycle",
        "siklus hidup pengembangan software",
        "memahami sdlc",
        "pemahaman mendalam mengenai siklus hidup pengembangan software",
        "pelayanan pelanggan",
        "customer service",
        "berpengalaman di bidang pelayanan pelanggan",
        "pengalaman di bidang pelayanan pelanggan",
        "driver's licence",
        "driver's license",
        "surat izin mengemudi",
        "sim a",
        "sim c",
        "weekends",
        "public holidays",
        "akhir pekan",
        "hari libur",
    ]
    if any(k in q for k in yes_keywords):
        prefs["radio"] = prefs["radio"] + ["ya", "yes"]

    # Fluent languages
    if "bahasa apa saja" in q and "fasih" in q or "languages are you fluent" in q:
        prefs["checkbox"] = prefs["checkbox"] + [
            "bahasa inggris",
            "english",
            "bahasa indonesia",
            "indonesian",
        ]

    # Programming languages
    if "bahasa pemrograman" in q or "programming language" in q:
        prefs["checkbox"] = prefs["checkbox"] + ["c", "c#", ".net", "java", "python", "javascript"]

    # de-dup preserving order
    for key in ("radio", "checkbox", "dropdown"):
        seen = set()
        out = []
        for v in prefs[key]:
            n = _norm_text(v)
            if n and n not in seen:
                out.append(v)
                seen.add(n)
        prefs[key] = out
    return prefs


def _is_systems_admin_experience_question(question_text):
    q = _norm_text(question_text)
    if not q:
        return False
    is_experience = (
        "how many years" in q
        or "berapa tahun" in q
        or "experience" in q
        or "pengalaman" in q
    )
    if not is_experience:
        return False
    return any(k in q for k in SYSTEMS_ADMIN_KEYWORDS)


def _pilih_2_years_native_select(driver, select_el):
    return _set_native_select_by_preferences(driver, select_el, YEARS_2_PREFERENCES)


def _get_container_question_text(container):
    try:
        return _teks_terlihat_elemen(container)
    except Exception:
        return ""


def _ambil_href_lamaran_cepat(driver, max_wait=10.0):
    end = time.monotonic() + max_wait
    while time.monotonic() < end:
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[data-automation='job-detail-apply']")
        for a in anchors:
            try:
                if not a.is_displayed() or not a.is_enabled():
                    continue
                text = _norm_text(_teks_terlihat_elemen(a))
                href = (a.get_attribute("href") or "").strip()
                if "lamaran cepat" in text and href and "/apply" in href:
                    return a, href
            except Exception:
                continue
        _sleep(0.2)
    return None, ""


def _isi_radio_wajib_yang_kosong(driver):
    changed = 0
    groups = {}
    radios = driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name]")
    for radio in radios:
        try:
            if not radio.is_displayed() or not radio.is_enabled():
                continue
            nm = (radio.get_attribute("name") or "").strip()
            if not nm:
                continue
            groups.setdefault(nm, []).append(radio)
        except Exception:
            continue

    for _, group in groups.items():
        any_checked = False
        for r in group:
            try:
                if r.is_selected() or (r.get_attribute("aria-checked") == "true"):
                    any_checked = True
                    break
            except Exception:
                continue
        if any_checked:
            continue

        for candidate in group:
            if _click_el(driver, candidate):
                changed += 1
                break
    return changed


def _isi_dropdown_kosong(driver):
    changed = 0
    # Native <select>
    selects = driver.find_elements(By.CSS_SELECTOR, "select")
    for sel in selects:
        try:
            if not sel.is_displayed() or not sel.is_enabled():
                continue
            val = (sel.get_attribute("value") or "").strip()
            if val:
                continue
            q_text = ""
            try:
                sid = (sel.get_attribute("id") or "").strip()
                if sid:
                    labels = driver.find_elements(By.XPATH, f"//label[@for='{sid}']")
                    if labels:
                        q_text = _teks_terlihat_elemen(labels[0])
                if not q_text:
                    q_text = _teks_terlihat_elemen(
                        sel.find_element(By.XPATH, "./ancestor::div[.//label or .//strong][1]")
                    )
            except Exception:
                pass
            inferred = _infer_preferences_from_question(q_text)
            is_sysadmin_q = _is_systems_admin_experience_question(q_text)
            if is_sysadmin_q:
                ok, chosen = _pilih_2_years_native_select(driver, sel)
                if ok:
                    print("Native select khusus: Systems Administrator -> pilih 2 years.")
                    changed += 1
                    continue
            ok, chosen = _set_native_select_by_preferences(
                driver,
                sel,
                inferred["dropdown"] or YEARS_2_PREFERENCES,
            )
            if ok:
                if any(_norm_text(p) in _norm_text(chosen) for p in YEARS_2_PREFERENCES):
                    print("Native select: pilih opsi preferensi 2 years/2 tahun.")
                changed += 1
        except Exception:
            continue

    # Combobox custom; ambil yang invalid dulu
    combos = driver.find_elements(By.XPATH, "//*[@role='combobox' and (@aria-invalid='true' or @aria-required='true')]")
    for cb in combos:
        try:
            if not cb.is_displayed() or not cb.is_enabled():
                continue
            if not _click_el(driver, cb):
                continue
            _sleep(0.2)
            q_text = ""
            try:
                q_text = _get_container_question_text(
                    cb.find_element(By.XPATH, "./ancestor::div[.//*[@role='combobox'] or .//select][1]")
                )
            except Exception:
                pass
            inferred = _infer_preferences_from_question(q_text)
            is_sysadmin_q = _is_systems_admin_experience_question(q_text)
            prefs = YEARS_2_PREFERENCES if is_sysadmin_q else (inferred["dropdown"] or YEARS_2_PREFERENCES)
            ok, chosen = _pilih_opsi_terlihat(
                driver,
                preferred_texts=prefs,
            )
            if ok:
                chosen_norm = _norm_text(chosen)
                if any(_norm_text(p) in chosen_norm for p in YEARS_2_PREFERENCES):
                    if is_sysadmin_q:
                        print("Dropdown khusus: Systems Administrator -> pilih 2 years.")
                    else:
                        print("Dropdown: pilih opsi preferensi 2 years/2 tahun.")
                changed += 1
        except Exception:
            continue
    return changed


def _pilih_radio_dengan_label(driver, container, preferred_labels):
    prefs = [_norm_text(x) for x in (preferred_labels or []) if x]
    radios = container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
    if not radios:
        return False

    # skip jika sudah ada yang selected
    for r in radios:
        try:
            if r.is_selected() or (r.get_attribute("aria-checked") == "true"):
                return False
        except Exception:
            continue

    for r in radios:
        try:
            rid = (r.get_attribute("id") or "").strip()
        except Exception:
            rid = ""

        label_text = ""
        label_el = None
        if rid:
            try:
                labels = container.find_elements(By.XPATH, f".//label[@for='{rid}']")
                if labels:
                    label_el = labels[0]
                    label_text = _norm_text(_teks_terlihat_elemen(label_el))
            except Exception:
                pass

        # fallback: ambil teks sibling terdekat
        if not label_text:
            try:
                parent_txt = _norm_text(_teks_terlihat_elemen(r.find_element(By.XPATH, "./ancestor::*[self::div or self::label][1]")))
                label_text = parent_txt
            except Exception:
                label_text = ""

        if not any(p in label_text for p in prefs):
            continue

        # Prioritaskan klik label/wrapper untuk UI custom radio.
        if label_el is not None and _click_el(driver, label_el):
            return True
        try:
            wrapper = r.find_element(
                By.XPATH,
                "./following-sibling::*[contains(@class,'_1fk61uehx') or self::div][1]",
            )
            if _click_el(driver, wrapper):
                return True
        except Exception:
            pass
        if _click_el(driver, r):
            return True
    return False


def _ambil_teks_opsi_radio(container):
    texts = []
    radios = container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
    for r in radios:
        txt = ""
        rid = ""
        try:
            rid = (r.get_attribute("id") or "").strip()
        except Exception:
            rid = ""
        if rid:
            try:
                labels = container.find_elements(By.XPATH, f".//label[@for='{rid}']")
                for lb in labels:
                    t = _norm_text(_teks_terlihat_elemen(lb))
                    if t:
                        txt = t
                        break
            except Exception:
                pass
        if not txt:
            try:
                txt = _norm_text(
                    _teks_terlihat_elemen(
                        r.find_element(By.XPATH, "./ancestor::*[self::div or self::label][1]")
                    )
                )
            except Exception:
                txt = ""
        if txt and txt not in texts:
            texts.append(txt)
    return texts


def _infer_radio_preference_dari_opsi(question_text, option_texts):
    q = _norm_text(question_text)
    options = [_norm_text(x) for x in (option_texts or []) if x]
    if not options:
        return []

    has_yes = any((" ya" in f" {o}" or "yes" in o or "iya" in o) for o in options)
    has_no = any((" tidak" in f" {o}" or "no" == o or " no " in f" {o} ") for o in options)

    prefs = []
    # Pertanyaan umum ketersediaan/pengalaman/kemauan: prefer Yes.
    if has_yes and has_no and any(
        k in q
        for k in [
            "apakah",
            "do you",
            "are you",
            "bersedia",
            "willing",
            "experience",
            "pengalaman",
            "available",
            "background check",
            "driver",
            "licence",
            "license",
        ]
    ):
        prefs += ["ya", "yes", "iya"]

    # Pertanyaan notice period: prefer tercepat.
    if "notice" in q or "memberi tahu perusahaanmu" in q or "waktu yang kamu butuhkan" in q:
        prefs += [
            "tidak ada",
            "siap bekerja segera",
            "kurang dari 1 bulan",
            "less than 1 month",
            "immediately",
        ]

    # de-dup
    seen = set()
    out = []
    for p in prefs:
        n = _norm_text(p)
        if n and n not in seen:
            out.append(p)
            seen.add(n)
    return out


def _is_pertanyaan_outside_hours(container):
    try:
        txt = _norm_text(_teks_terlihat_elemen(container))
    except Exception:
        txt = ""
    keywords = [
        "bekerja di luar jam kerja",
        "luar jam kerja biasa",
        "work outside your usual hours",
        "weekends",
        "public holidays",
    ]
    return any(k in txt for k in keywords)


def _is_pertanyaan_bahasa_fasih(container):
    try:
        txt = _norm_text(_teks_terlihat_elemen(container))
    except Exception:
        txt = ""
    keywords = [
        "bahasa apa saja di bawah ini yang fasih kamu gunakan",
        "which of the following languages are you fluent in",
    ]
    return any(k in txt for k in keywords)


def _ambil_error_panel_messages(driver):
    try:
        panel = driver.find_element(By.ID, "errorPanel")
    except Exception:
        return []

    try:
        if not panel.is_displayed():
            return []
    except Exception:
        return []

    msgs = []
    try:
        items = panel.find_elements(By.XPATH, ".//li//span")
        for it in items:
            t = (it.text or "").strip()
            if t and t not in msgs:
                msgs.append(t)
    except Exception:
        pass

    if not msgs:
        try:
            t = (panel.text or "").strip()
            if t:
                msgs.append(t)
        except Exception:
            pass
    return msgs


def _log_status_error_panel(driver):
    msgs = _ambil_error_panel_messages(driver)
    if msgs:
        print("Error panel terdeteksi setelah klik 'Lanjut':")
        for m in msgs:
            print(f"  - {m}")
        return False

    print("\033[92mSemua pertanyaan terisi, tidak ada error panel.\033[0m")
    return True


def _check_checkbox_labels(driver, container, target_labels):
    targets = [_norm_text(x) for x in (target_labels or []) if x]
    if not targets:
        return 0

    changed = 0
    checks = container.find_elements(By.CSS_SELECTOR, "input[type='checkbox'][id]")

    def _is_checked(inp):
        try:
            if inp.is_selected():
                return True
        except Exception:
            pass
        try:
            return (inp.get_attribute("aria-checked") or "").strip().lower() == "true"
        except Exception:
            return False

    for c in checks:
        try:
            cid = (c.get_attribute("id") or "").strip()
            if not cid:
                continue
            labels = container.find_elements(By.XPATH, f".//label[@for='{cid}']")
            if not labels:
                continue
            label = labels[0]
            ltxt = _norm_text(_teks_terlihat_elemen(label))
            if not any(t in ltxt for t in targets):
                continue
            if _is_checked(c):
                continue
            if _click_el(driver, label) or _click_el(driver, c):
                _sleep(0.1)
                if _is_checked(c):
                    changed += 1
        except Exception:
            continue
    return changed


def _isi_field_dari_error_sections(driver):
    """
    Isi field berdasarkan section yang memunculkan error 'Silakan buat seleksi'.
    Ini menangani radio/checkbox/combobox per-pertanyaan.
    """
    changed = 0
    processed = set()

    errors = driver.find_elements(By.XPATH, "//*[contains(normalize-space(.),'Silakan buat seleksi')]")
    for err in errors:
        try:
            if not err.is_displayed():
                continue
        except Exception:
            continue

        # Abaikan item ringkasan di error panel; yang dibutuhkan adalah field inline di pertanyaan.
        try:
            in_error_panel = err.find_elements(By.XPATH, "./ancestor::*[@id='errorPanel']")
            if in_error_panel:
                continue
        except Exception:
            pass

        try:
            container = err.find_element(
                By.XPATH,
                "./ancestor::*[(self::fieldset or self::div) and (.//input[@type='radio' or @type='checkbox'] or .//*[@role='combobox'] or .//select)][1]",
            )
        except Exception:
            continue

        try:
            key = container.id
        except Exception:
            key = None
        if key and key in processed:
            continue
        if key:
            processed.add(key)

        # 1) Radio: pilih opsi pertama yang belum terpilih
        radios = container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        picked = False
        question_text = _get_container_question_text(container)
        inferred = _infer_preferences_from_question(question_text)
        opsi_radio = _ambil_teks_opsi_radio(container)
        is_sysadmin_q = _is_systems_admin_experience_question(question_text)
        for r in radios:
            try:
                if not r.is_displayed() or not r.is_enabled():
                    continue
                if r.is_selected() or (r.get_attribute("aria-checked") == "true"):
                    picked = True
                    break
            except Exception:
                continue

        # Rule khusus: pertanyaan outside-hours => pilih Ya/Yes.
        if not picked and radios and _is_pertanyaan_outside_hours(container):
            if _pilih_radio_dengan_label(driver, container, ["ya", "yes"]):
                changed += 1
                picked = True
                print("Radio khusus: pertanyaan outside-hours dipilih 'Ya/Yes'.")

        # Heuristik umum radio berdasarkan teks pertanyaan
        if not picked and radios and inferred["radio"]:
            if _pilih_radio_dengan_label(driver, container, inferred["radio"]):
                changed += 1
                picked = True
                print(f"Radio heuristik: pertanyaan '{_norm_text(question_text)[:80]}' -> {inferred['radio'][0]}")

        # Heuristik adaptif dari opsi yang tersedia (untuk pertanyaan baru).
        if not picked and radios:
            adaptive_radio = _infer_radio_preference_dari_opsi(question_text, opsi_radio)
            if adaptive_radio and _pilih_radio_dengan_label(driver, container, adaptive_radio):
                changed += 1
                picked = True
                print(
                    f"Radio adaptif: pertanyaan '{_norm_text(question_text)[:80]}' -> {adaptive_radio[0]}"
                )

        if not picked:
            for r in radios:
                try:
                    if r.is_displayed() and r.is_enabled() and _click_el(driver, r):
                        changed += 1
                        picked = True
                        break
                except Exception:
                    continue
        if picked:
            continue

        # 2) Checkbox: centang opsi pertama
        checks = container.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        def _is_checked_input(inp):
            try:
                if inp.is_selected():
                    return True
            except Exception:
                pass
            try:
                aria = (inp.get_attribute("aria-checked") or "").strip().lower()
                if aria == "true":
                    return True
            except Exception:
                pass
            return False

        for c in checks:
            try:
                if _is_checked_input(c):
                    picked = True
                    break
            except Exception:
                continue
        if not picked:
            for c in checks:
                try:
                    if _is_checked_input(c):
                        picked = True
                        break

                    # 1) Coba klik input langsung jika memungkinkan
                    if c.is_displayed() and c.is_enabled() and _click_el(driver, c):
                        if _is_checked_input(c):
                            changed += 1
                            picked = True
                            break

                    # 2) Coba klik label yang terhubung: <label for="...">
                    input_id = (c.get_attribute("id") or "").strip()
                    if input_id:
                        labels = container.find_elements(By.XPATH, f".//label[@for='{input_id}']")
                        for lb in labels:
                            if lb.is_displayed() and _click_el(driver, lb):
                                _sleep(0.1)
                                if _is_checked_input(c):
                                    changed += 1
                                    picked = True
                                    break
                        if picked:
                            break

                    # 3) Fallback klik wrapper custom checkbox
                    wrappers = container.find_elements(
                        By.XPATH,
                        ".//div[contains(@class,'_1fk61uehx') and contains(@class,'_1fk61ue5d')]",
                    )
                    for w in wrappers:
                        if w.is_displayed() and _click_el(driver, w):
                            _sleep(0.1)
                            if _is_checked_input(c):
                                changed += 1
                                picked = True
                                break
                    if picked:
                        break
                except Exception:
                    continue
        if picked:
            continue

        # Rule khusus: pertanyaan bahasa fasih => centang Inggris + Indonesia.
        if checks and _is_pertanyaan_bahasa_fasih(container):
            lang_changed = _check_checkbox_labels(
                driver,
                container,
                target_labels=[
                    "bahasa inggris",
                    "english",
                    "bahasa indonesia",
                    "indonesian",
                ],
            )
            if lang_changed > 0:
                changed += lang_changed
                picked = True
                print("Checkbox khusus: pilih Bahasa Inggris + Bahasa Indonesia.")
                continue

        # Heuristik umum checkbox berdasarkan teks pertanyaan
        if checks and inferred["checkbox"]:
            check_changed = _check_checkbox_labels(driver, container, inferred["checkbox"])
            if check_changed > 0:
                changed += check_changed
                picked = True
                print(
                    f"Checkbox heuristik: pertanyaan '{_norm_text(question_text)[:80]}' -> "
                    f"{', '.join(inferred['checkbox'][:2])}"
                )
                continue

        # 2b) Checkbox custom (tanpa input checkbox yang mudah diakses),
        # contoh class: "_1fk61uehx _1fk61ue5d ..."
        custom_checks = []
        custom_selectors = [
            ".//*[@role='checkbox']",
            ".//div[contains(@class,'_1fk61uehx') and contains(@class,'_1fk61ue5d')]",
            ".//div[contains(@class,'_1fk61uehx') and contains(@class,'_1fk61ue65')]",
            ".//span[contains(@class,'_1fk61ue65')]/ancestor::div[contains(@class,'_1fk61uehx')][1]",
        ]
        for sel in custom_selectors:
            try:
                custom_checks.extend(container.find_elements(By.XPATH, sel))
            except Exception:
                continue

        seen_custom = set()
        for cc in custom_checks:
            try:
                cid = cc.id
            except Exception:
                cid = None
            if cid and cid in seen_custom:
                continue
            if cid:
                seen_custom.add(cid)

            try:
                if not cc.is_displayed() or not cc.is_enabled():
                    continue
                # Skip jika sudah checked
                aria_checked = (cc.get_attribute("aria-checked") or "").strip().lower()
                if aria_checked == "true":
                    picked = True
                    break
                classes = (cc.get_attribute("class") or "").strip().lower()
                if "checked" in classes:
                    picked = True
                    break
                if _click_el(driver, cc):
                    changed += 1
                    picked = True
                    break
            except Exception:
                continue
        if picked:
            continue

        # 3) Combobox custom: pilih opsi pertama dari list
        combos = container.find_elements(By.XPATH, ".//*[@role='combobox']")
        combo_done = False
        for cb in combos:
            try:
                if not cb.is_displayed() or not cb.is_enabled():
                    continue
                if not _click_el(driver, cb):
                    continue
                _sleep(0.2)
                ok, chosen = _pilih_opsi_terlihat(
                    driver,
                    preferred_texts=YEARS_2_PREFERENCES if is_sysadmin_q else (inferred["dropdown"] or YEARS_2_PREFERENCES),
                )
                if ok:
                    chosen_norm = _norm_text(chosen)
                    if any(_norm_text(p) in chosen_norm for p in YEARS_2_PREFERENCES):
                        if is_sysadmin_q:
                            print("Error-section dropdown khusus: Systems Administrator -> pilih 2 years.")
                        else:
                            print("Error-section dropdown: pilih opsi preferensi 2 years/2 tahun.")
                    changed += 1
                    combo_done = True
                    break
            except Exception:
                continue
        if combo_done:
            continue

        # 4) Native select
        selects = container.find_elements(By.CSS_SELECTOR, "select")
        for sel in selects:
            try:
                if not sel.is_displayed() or not sel.is_enabled():
                    continue
                val = (sel.get_attribute("value") or "").strip()
                if val:
                    continue
                if is_sysadmin_q:
                    ok, chosen = _pilih_2_years_native_select(driver, sel)
                    if ok:
                        changed += 1
                        combo_done = True
                        print("Native select khusus: Systems Administrator -> pilih 2 years.")
                        break
                ok, chosen = _set_native_select_by_preferences(
                    driver,
                    sel,
                    inferred["dropdown"] or YEARS_2_PREFERENCES,
                )
                if ok:
                    changed += 1
                    combo_done = True
                    chosen_norm = _norm_text(chosen)
                    if any(_norm_text(p) in chosen_norm for p in YEARS_2_PREFERENCES):
                        print("Native select: pilih opsi preferensi 2 years/2 tahun.")
                    else:
                        print(f"Native select heuristik: pilih '{chosen}'.")
                if combo_done:
                    break
            except Exception:
                continue
    return changed


def _isi_field_dari_error_panel_messages(driver):
    """
    Fallback: gunakan teks pertanyaan dari error panel untuk menemukan field
    pertanyaan yang sesuai, lalu isi radio/select di container tersebut.
    """
    changed = 0
    messages = _ambil_error_panel_messages(driver)
    if not messages:
        return 0

    for msg in messages:
        q = (msg or "").split(" - ")[0].strip()
        if not q:
            continue
        q_norm = _norm_text(q)
        if not q_norm:
            continue

        try:
            candidates = driver.find_elements(
                By.XPATH,
                "//*[self::fieldset or self::div][.//strong or .//label]",
            )
        except Exception:
            candidates = []

        containers = []
        for c in candidates:
            try:
                txt = _norm_text(_teks_terlihat_elemen(c))
            except Exception:
                txt = ""
            if txt and q_norm in txt:
                containers.append(c)

        for container in containers:
            try:
                if not container.is_displayed():
                    continue
            except Exception:
                continue

            question_text = _get_container_question_text(container)
            inferred = _infer_preferences_from_question(question_text)

            # Radio
            radios = []
            try:
                radios = container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            except Exception:
                radios = []
            if radios:
                adaptive = _infer_radio_preference_dari_opsi(
                    question_text,
                    _ambil_teks_opsi_radio(container),
                )
                prefs = inferred["radio"] or adaptive or ["ya", "yes"]
                if _pilih_radio_dengan_label(driver, container, prefs):
                    changed += 1
                    break

            # Native select
            try:
                selects = container.find_elements(By.CSS_SELECTOR, "select")
            except Exception:
                selects = []
            for sel in selects:
                try:
                    if not sel.is_displayed() or not sel.is_enabled():
                        continue
                    val = (sel.get_attribute("value") or "").strip()
                    if val:
                        continue
                    ok, _ = _set_native_select_by_preferences(
                        driver,
                        sel,
                        inferred["dropdown"] or YEARS_2_PREFERENCES,
                    )
                    if ok:
                        changed += 1
                        break
                except Exception:
                    continue

    return changed


def _selesaikan_form_role_requirements(driver, max_rounds=4):
    for ronde in range(1, max_rounds + 1):
        if "/apply/role-requirements" not in (driver.current_url or ""):
            return True

        radio_changes = _isi_radio_wajib_yang_kosong(driver)
        dropdown_changes = _isi_dropdown_kosong(driver)
        error_section_changes = _isi_field_dari_error_sections(driver)
        error_panel_changes = _isi_field_dari_error_panel_messages(driver)
        total_changes = radio_changes + dropdown_changes + error_section_changes + error_panel_changes
        print(
            "Role requirements ronde-"
            f"{ronde}: isi radio={radio_changes}, dropdown={dropdown_changes}, "
            f"error-section={error_section_changes}, error-panel-fallback={error_panel_changes}"
        )

        lanjut = _find_clickable(
            driver,
            [
                (By.CSS_SELECTOR, "button[data-testid='continue-button']"),
                (By.XPATH, "//button[contains(normalize-space(.),'Lanjut')]"),
            ],
            max_wait=6.0,
        )
        if not lanjut:
            print("Role requirements: tombol 'Lanjut' tidak ditemukan.")
            return False

        _click_el(driver, lanjut)
        _sleep(0.8)
        _log_status_error_panel(driver)

        if "/apply/role-requirements" not in (driver.current_url or ""):
            print(f"Role requirements selesai, pindah ke URL: {driver.current_url}")
            return True

        errors = driver.find_elements(By.XPATH, "//*[contains(normalize-space(.),'Silakan buat seleksi')]")
        if not errors and total_changes == 0:
            # Tidak ada error terlihat tapi masih di halaman sama; coba lanjutkan ronde berikutnya
            continue
    return "/apply/role-requirements" not in (driver.current_url or "")


def _lanjut_hingga_submit_review(driver, job_id, job_title="-"):
    """
    Setelah role requirements lolos:
    - jika halaman skill terdeteksi (add-skills), klik lanjut,
    - lalu cari tombol kirim lamaran (review-submit-application) dan klik.
    """
    _sleep(0.35)

    add_skills = _find_clickable(
        driver,
        [
            (By.CSS_SELECTOR, "button[data-testid='add-skills']"),
            (By.XPATH, "//button[@data-testid='add-skills' or contains(normalize-space(.),'Tambah keahlian')]"),
        ],
        max_wait=3.0,
    )
    if add_skills:
        print(f"Job ID {job_id}: halaman 'Tambah keahlian' terdeteksi.")
        lanjut_btn = _find_clickable(
            driver,
            [
                (By.CSS_SELECTOR, "button[data-testid='continue-button']"),
                (By.XPATH, "//button[contains(normalize-space(.),'Lanjut')]"),
            ],
            max_wait=4.0,
        )
        if lanjut_btn:
            print(f"Job ID {job_id}: klik 'Lanjut' di halaman skill.")
            _click_el(driver, lanjut_btn)
            _sleep(0.35)
        else:
            print(f"Job ID {job_id}: tombol 'Lanjut' di halaman skill tidak ditemukan.")

    submit_btn = _find_clickable(
        driver,
        [
            (By.CSS_SELECTOR, "button[data-testid='review-submit-application']"),
            (By.XPATH, "//button[@type='submit' and @data-testid='review-submit-application']"),
            (By.XPATH, "//button[contains(normalize-space(.),'Kirim lamaran')]"),
        ],
        max_wait=5.0,
    )
    if submit_btn:
        print(f"Job ID {job_id}: tombol 'Kirim lamaran' ditemukan, klik submit.")
        _click_el(driver, submit_btn)
        _sleep(0.35)
        print(f"Job ID {job_id}: submit 'Kirim lamaran' sudah diklik.")

        limit_msgs = _submit_limit_error_messages(driver, max_wait=4.5, interval=0.2)
        if limit_msgs:
            _print_merah(
                f"Job ID {job_id}: terdeteksi error submit/limit. Proses dihentikan."
            )
            for m in limit_msgs:
                _print_merah(f"  - {m}")
            return "halt_limit"

        _simpan_lamaran_terkirim(job_id, job_title)
        _print_hijau(
            f"Lamaran tersimpan: job-id={job_id} | loker={job_title or '-'}"
        )
        _log_rekap_lamaran_terkirim_hijau()
        return True

    print(f"Job ID {job_id}: tombol 'Kirim lamaran' belum ditemukan, stop sementara di tahap ini.")
    return True


def _lamar_job_berdasarkan_id(driver, job_id):
    if not _klik_job_card_presisi(driver, job_id, max_wait=3.2):
        print(f"Job ID {job_id}: kartu loker tidak ditemukan / gagal diklik presisi.")
        print(f"Job ID {job_id}: lewati job ini, lanjut ke kartu berikutnya.")
        return "skip_click_fail"

    print(f"Job ID {job_id}: klik kartu loker (presisi) berhasil.")
    _sleep(0.35)
    if not _detail_job_sesuai_id(driver, job_id):
        print(f"Job ID {job_id}: detail aktif tidak cocok, coba klik ulang kartu.")
        if not _klik_job_card_presisi(driver, job_id, max_wait=2.2):
            print(f"Job ID {job_id}: klik ulang gagal.")
            print(f"Job ID {job_id}: lewati job ini, lanjut ke kartu berikutnya.")
            return "skip_click_fail"
        _sleep(0.25)
    already_applied, badge_text = _sudah_pernah_melamar(driver, max_wait=0.7)
    if already_applied:
        print(f"Job ID {job_id}: skip, sudah pernah melamar -> {badge_text}")
        return None

    detail_job_title = _ambil_judul_job_detail(driver)
    detail_job_company = _ambil_company_job_detail(driver)
    apply_btn, apply_href = _ambil_href_lamaran_cepat(driver, max_wait=3.2)
    if not apply_btn or not apply_href:
        print(
            f"Job ID {job_id}: elemen 'Lamaran Cepat' tidak ditemukan "
            "(a[data-automation='job-detail-apply'] + teks 'Lamaran Cepat')."
        )
        print(f"Job ID {job_id}: lewati job ini, lanjut ke kartu berikutnya.")
        return "skip_no_lamaran_cepat"

    _log_detail_job_sebelum_lamar(driver, job_id)
    _log_target_lamaran_cepat(job_id, 1, apply_btn)
    full_apply_url = urljoin("https://id.jobstreet.com", apply_href)
    print(f"Job ID {job_id}: href Lamaran Cepat -> {full_apply_url}")
    print(f"Job ID {job_id}: buka link apply dari href...")
    try:
        driver.get(full_apply_url)
    except Exception as e:
        print(f"Job ID {job_id}: gagal membuka URL apply -> {e}")
        return False
    _sleep(0.35)

    if "/apply" not in (driver.current_url or ""):
        print(f"Job ID {job_id}: setelah buka href, belum masuk /apply. URL={driver.current_url}")
        return False

    print(f"Job ID {job_id}: pindah ke halaman apply -> {driver.current_url}")

    cover_letter_selectors = [
        (By.XPATH, "//label[contains(normalize-space(.),'Tulis surat lamaran')]"),
        (By.CSS_SELECTOR, "input[data-testid='coverLetter-method-change']"),
    ]
    cover_change = _find_clickable(driver, cover_letter_selectors, max_wait=3.0)
    if not cover_change:
        print(f"Job ID {job_id}: opsi 'Tulis surat lamaran' tidak ditemukan.")
        return False

    _print_kuning(f"Job ID {job_id}: pilih 'Tulis surat lamaran'...")
    driver.execute_script("arguments[0].click();", cover_change)
    _sleep(0.12)

    cover_text = _buat_teks_surat_lamaran(detail_job_title, detail_job_company)
    text_area = _get_cover_letter_textarea(driver, max_wait=3.0)
    if not text_area:
        print(f"Job ID {job_id}: textarea surat lamaran tidak ditemukan.")
        return False

    ok_cover, current_cover = _isi_cover_letter_dan_verifikasi(driver, cover_text, min_len=80, max_attempts=4)
    if not ok_cover:
        print(f"Job ID {job_id}: gagal mengisi textarea surat lamaran dengan benar.")
        return False

    _print_hijau(f"Job ID {job_id}: mengisi surat lamaran dengan teks:\n{cover_text}")
    _print_kuning(f"Job ID {job_id}: trigger keyboard SPACE/ENTER pada surat lamaran sebelum lanjut.")
    _print_hijau(
        f"Job ID {job_id}: verifikasi panjang isi surat lamaran = {len(current_cover)} karakter."
    )

    continue_selectors = [
        (By.CSS_SELECTOR, "button[data-testid='continue-button']"),
        (By.XPATH, "//button[@data-testid='continue-button' and .//*[contains(normalize-space(.),'Lanjut')]]"),
    ]
    continue_btn = _find_clickable(driver, continue_selectors, max_wait=3.0)
    if not continue_btn:
        print(f"Job ID {job_id}: tombol 'Lanjut' tidak ditemukan.")
        return False

    print(f"Job ID {job_id}: klik 'Lanjut'...")
    _click_el(driver, continue_btn)
    _sleep(0.25)

    # Jika server masih menganggap surat lamaran kosong, isi ulang lalu lanjut lagi.
    for retry in range(1, 4):
        messages = _ambil_error_panel_messages(driver)
        if not _cover_letter_wajib_error(messages):
            break
        _print_kuning(
            f"Job ID {job_id}: terdeteksi 'Surat lamaran - Wajib diisi' (retry={retry}), validasi ulang..."
        )
        # Re-select mode "Tulis surat lamaran" untuk memastikan field aktif.
        cover_change_retry = _find_clickable(driver, cover_letter_selectors, max_wait=2.0)
        if cover_change_retry:
            try:
                driver.execute_script("arguments[0].click();", cover_change_retry)
            except Exception:
                _click_el(driver, cover_change_retry)
            _sleep(0.12)

        text_area_retry = _get_cover_letter_textarea(driver, max_wait=2.0)
        if not text_area_retry:
            print(f"Job ID {job_id}: textarea surat lamaran tidak ditemukan saat retry.")
            break
        current_retry = _get_textarea_value(driver, text_area_retry).strip()
        if not current_retry or len(current_retry) < 80:
            _print_kuning(
                f"Job ID {job_id}: isi surat lamaran kosong/terlalu pendek ({len(current_retry)}), isi ulang..."
            )
            ok_retry, current_retry = _isi_cover_letter_dan_verifikasi(
                driver, cover_text, min_len=80, max_attempts=3
            )
            if not ok_retry:
                print(f"Job ID {job_id}: isi ulang surat lamaran saat retry gagal.")
                break
        _print_hijau(
            f"Job ID {job_id}: retry verifikasi panjang isi surat lamaran = {len(current_retry)} karakter."
        )
        continue_btn_retry = _find_clickable(driver, continue_selectors, max_wait=2.0)
        if not continue_btn_retry:
            print(f"Job ID {job_id}: tombol 'Lanjut' tidak ditemukan saat retry surat lamaran.")
            break
        print(f"Job ID {job_id}: klik 'Lanjut' ulang setelah validasi surat lamaran...")
        _click_el(driver, continue_btn_retry)
        _sleep(0.25)

    messages_after_retry = _ambil_error_panel_messages(driver)
    if _cover_letter_wajib_error(messages_after_retry):
        print(f"Job ID {job_id}: surat lamaran masih dianggap kosong setelah retry, lewati job ini.")
        return False

    if "/apply/role-requirements" in (driver.current_url or ""):
        print(f"Job ID {job_id}: masuk halaman role requirements, mulai isi form...")
        done = _selesaikan_form_role_requirements(driver, max_rounds=5)
        if not done:
            print(f"Job ID {job_id}: form role requirements belum selesai terisi.")
            return False

    submit_state = _lanjut_hingga_submit_review(driver, job_id, detail_job_title)
    if submit_state == "halt_limit":
        return "halt_limit"
    return True


def buka_jobstreet_dan_lamar_cepat(max_jobs=10, debugger_address="127.0.0.1:9222", page=1):
    global STOP_DUE_TO_LIMIT
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(12)

    page_url = f"https://id.jobstreet.com/id/full-stack-jobs?page={page}"
    print(f"Membuka halaman JobStreet IT page {page}...")
    driver.get(page_url)
    _sleep(0.35)

    ringkasan_jobs = _ambil_ringkasan_job_dari_halaman(driver)
    job_ids = [x["job_id"] for x in ringkasan_jobs]
    if not job_ids:
        print("Tidak ada job card ditemukan di halaman.")
        return False

    print(f"Total job terdeteksi: {len(job_ids)}. Target proses: semua job di page {page}.")
    if max_jobs != len(job_ids):
        print(
            f"Info: --max-jobs={max_jobs} diabaikan untuk mode ini. "
            "Bot akan cek Lamaran Cepat untuk setiap job."
        )
    print(f"Daftar loker terdeteksi di page {page}:")
    for i, item in enumerate(ringkasan_jobs, start=1):
        print(f"  {i}. job-id={item['job_id']} | title={item['title']} | company={item['company']}")
    sukses = 0
    skip = 0
    skip_no_lamaran_cepat = 0
    skip_click_fail = 0
    gagal = 0
    kartu_diklik = 0

    processed_count = 0
    for idx, job_id in enumerate(job_ids, start=1):
        if STOP_DUE_TO_LIMIT:
            break
        print(f"Proses job {idx}/{len(job_ids)} (job-id={job_id})")
        halt_now = False

        try:
            result = _lamar_job_berdasarkan_id(driver, job_id)
            if result is True:
                kartu_diklik += 1
                sukses += 1
            elif result is None:
                kartu_diklik += 1
                skip += 1
                # skip karena sudah melamar -> lanjut ke kartu berikutnya
                continue
            elif result == "skip_no_lamaran_cepat":
                kartu_diklik += 1
                skip_no_lamaran_cepat += 1
                # skip karena tidak ada Lamaran Cepat -> lanjut ke kartu berikutnya
                continue
            elif result == "skip_click_fail":
                skip_click_fail += 1
                # skip karena gagal klik card presisi -> lanjut ke kartu berikutnya
                continue
            elif result == "halt_limit":
                kartu_diklik += 1
                halt_now = True
                STOP_DUE_TO_LIMIT = True
                _print_merah("Terdeteksi limit/error submit. Hentikan proses JobStreet.")
                break
            else:
                gagal += 1
        except Exception as e:
            print(f"Job ID {job_id}: gagal, {e}")
            gagal += 1
        finally:
            processed_count += 1
            if not (halt_now or STOP_DUE_TO_LIMIT):
                try:
                    driver.get(page_url)
                    _sleep(0.6)
                except Exception:
                    pass

    if processed_count == len(job_ids) and not STOP_DUE_TO_LIMIT:
        _print_hijau(
            f"Sudah cek semua job di page {page} ({processed_count}/{len(job_ids)}). Lanjut ke page berikutnya."
        )
        _log_rekap_lamaran_terkirim_hijau()

    print(
        f"Flow JobStreet selesai. Berhasil: {sukses}, gagal: {gagal}, "
        f"skip-sudah-melamar: {skip}, skip-tidak-ada-lamaran-cepat: {skip_no_lamaran_cepat}, "
        f"skip-gagal-klik-card: {skip_click_fail}, "
        f"kartu-terklik: {kartu_diklik}/{len(job_ids)}, total-job-page{page}: {len(job_ids)}"
    )
    if STOP_DUE_TO_LIMIT:
        _print_merah("Flow dihentikan karena terdeteksi limit/error submit dari JobStreet.")
    return sukses > 0


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Bot apply JobStreet")
        parser.add_argument("max_jobs_pos", nargs="?", type=int, help="Positional lama: max_jobs")
        parser.add_argument("total_seconds_pos", nargs="?", type=int, help="Positional lama: total_seconds")
        parser.add_argument("--max-jobs", type=int, default=None, help="Target job non-skip per siklus")
        parser.add_argument("--total-seconds", type=int, default=None, help="Durasi total loop (detik)")
        parser.add_argument("--debugger-address", default="127.0.0.1:9222", help="Contoh: 127.0.0.1:9222")
        args = parser.parse_args()

        max_jobs = (
            args.max_jobs
            if args.max_jobs is not None
            else (args.max_jobs_pos if args.max_jobs_pos is not None else 1)
        )
        total_seconds = (
            args.total_seconds
            if args.total_seconds is not None
            else (args.total_seconds_pos if args.total_seconds_pos is not None else 10800)
        )
        start = time.monotonic()
        cycle = 0
        current_page = 1

        print(
            f"Mode loop aktif: target {max_jobs} job non-skip per siklus, "
            f"durasi total {total_seconds} detik. Auto paging mulai dari page {current_page}."
        )
        while time.monotonic() - start < total_seconds:
            cycle += 1
            elapsed = int(time.monotonic() - start)
            print(f"\n=== Siklus {cycle} | Page {current_page} (elapsed {elapsed}s) ===")
            try:
                buka_jobstreet_dan_lamar_cepat(
                    max_jobs=max_jobs,
                    debugger_address=args.debugger_address,
                    page=current_page,
                )
            except Exception as e:
                print(f"Siklus {cycle} error: {e}")
            if STOP_DUE_TO_LIMIT:
                _print_merah("Loop dihentikan: terdeteksi limit/error submit dari JobStreet.")
                break
            current_page += 1
            _sleep(0.4)

        print("Loop 3 jam selesai.")
    except Exception as e:
        print(f"Error JobStreet: {e}")
