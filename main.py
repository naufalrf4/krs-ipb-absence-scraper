import time
import os
import openpyxl
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from dotenv import load_dotenv
from colorama import init, Fore, Style
import shutil
import logging

# Load environment variables
load_dotenv()

krs_username = os.getenv('KRS_USERNAME')
krs_password = os.getenv('KRS_PASSWORD')
chrome_driver_path = os.getenv('CHROMEDRIVER_PATH')

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "krsipb.log")

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True)

# Welcome screen
def print_welcome():
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear console
    terminal_width = shutil.get_terminal_size().columns
    welcome_message = """
======================================== 
{blue}KRS IPB ABSENCE SCRAPER {reset}
by: NaufalRF
========================================
{yellow}notes: read readme.md first{reset}
========================================
""".format(blue=Fore.BLUE + Style.BRIGHT, yellow=Fore.YELLOW, reset=Style.RESET_ALL)
    centered_message = '\n'.join(line.center(terminal_width) for line in welcome_message.split('\n'))
    print(centered_message)

print_welcome()

# Setting up Selenium
service = ChromeService(chrome_driver_path)
options = webdriver.ChromeOptions()

# Enable headless mode
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")

# Disable images and CSS to speed up page loading
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2
}
options.add_experimental_option("prefs", prefs)

options.page_load_strategy = 'eager'

# Disable unnecessary extensions
options.add_argument("--disable-extensions")

try:
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("ChromeDriver berhasil dimulai.")
except WebDriverException as e:
    logging.error(f"Kesalahan saat memulai ChromeDriver: {e}")
    raise

def login_to_krs():
    try:
        driver.get("https://krs.ipb.ac.id/login")
        print("Berhasil menuju halaman login KRS IPB.")
        logging.info("Berhasil menuju halaman login KRS IPB.")

        username = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "input-username"))
        )
        password = driver.find_element(By.ID, "input-password")

        username.send_keys(krs_username)
        password.send_keys(krs_password)

        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )

        login_button.click()
        print("Login berhasil.")
        logging.info("Login berhasil.")
        time.sleep(2)  # Reduced sleep time

    except NoSuchElementException as e:
        print(f"Kesalahan saat login: {e}")
        logging.error(f"Kesalahan saat login: {e}")
        driver.quit()
        raise
    except Exception as e:
        print(f"Kesalahan tidak terduga saat login: {e}")
        logging.error(f"Kesalahan tidak terduga saat login: {e}")
        driver.quit()
        raise

def scrape_classes(course_code):
    try:
        course_url = f"https://krs.ipb.ac.id/mk/{course_code}"
        driver.get(course_url)
        print(f"Berhasil menuju halaman mata kuliah: {course_url}")
        logging.info(f"Berhasil menuju halaman mata kuliah: {course_url}")
        time.sleep(3)  # Reduced sleep time

        classes = driver.find_elements(By.XPATH, "//tbody/tr")
        if not classes:
            print("Tidak ada kelas yang ditemukan.")
            logging.info("Tidak ada kelas yang ditemukan.")
            return

        class_details = []
        for idx, class_row in enumerate(classes, start=1):
            cells = class_row.find_elements(By.TAG_NAME, "td")
            badge = cells[0].text.strip()
            group = cells[1].text.strip()
            schedule = cells[2].text.strip()
            class_details.append((idx, badge, group, schedule))

        print("Kelas yang tersedia:")
        for detail in class_details:
            print(f"{detail[0]}. {detail[1]} {detail[2]} - {detail[3]}")

        selected_class_index = int(input("Pilih nomor kelas yang diinginkan: ")) - 1
        if selected_class_index < 0 or selected_class_index >= len(class_details):
            print("Pilihan tidak valid.")
            logging.error("Pilihan kelas tidak valid.")
            return

        selected_class_row = classes[selected_class_index]
        detail_button = selected_class_row.find_element(By.XPATH, ".//button[contains(@class, 'btn-primary')]")
        detail_button.click()
        print("Tombol detail diklik.")
        logging.info("Tombol detail diklik.")
        time.sleep(3)  # Reduced sleep time

        # Clear previous student data
        student_data = []

        students = driver.find_elements(By.XPATH, "//div[@class='card']//tbody/tr")
        for student in students:
            cells = student.find_elements(By.TAG_NAME, "td")
            no = cells[0].text.strip()
            nim = cells[1].text.strip()
            name = cells[2].text.strip()
            status = cells[3].text.strip()
            student_data.append((no, nim, name, status))
            print(f"Berhasil ambil data {name} dengan NIM {nim}")

        wb = Workbook()
        ws = wb.active
        ws.append(["No", "NIM", "Nama", "Status"])
        for data in student_data:
            ws.append(data)
        
        output_file = f"{course_code}_attendance.xlsx"
        wb.save(output_file)
        print(f"Data berhasil disimpan ke {output_file}")
        logging.info(f"Data berhasil disimpan ke {output_file}")

    except NoSuchElementException as e:
        print(f"Kesalahan saat scraping: {e}")
        logging.error(f"Kesalahan saat scraping: {e}")
    except Exception as e:
        print(f"Kesalahan tidak terduga saat scraping: {e}")
        logging.error(f"Kesalahan tidak terduga saat scraping: {e}")
    finally:
        driver.quit()
        print("Driver ditutup.")
        logging.info("Driver ditutup.")

def main():
    try:
        login_to_krs()
        course_code = input("Masukkan kode mata kuliah: ")
        scrape_classes(course_code)
    except Exception as e:
        print(f"Terjadi kesalahan selama proses: {e}")
        logging.error(f"Terjadi kesalahan selama proses: {e}")

if __name__ == "__main__":
    main()
