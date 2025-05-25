import time
import os
import uuid
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@shared_task
def send_whatsapp_message(phone_numbers, message, profile_path):
    print(f"[INFO] Using Chrome profile path: {profile_path}")
    try:
      
        options = webdriver.ChromeOptions( )
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        # options.binary_location = "/usr/bin/google-chrome"  # Optional
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'







        chrome_version = "135.0.7049.97"
        cache_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        driver_path = os.path.join(cache_path, chrome_version, "chromedriver")

        if not os.path.exists(driver_path):
            print("[INFO] ChromeDriver not found in cache. Downloading...")
            driver_path = ChromeDriverManager(driver_version=chrome_version).install()

          # driver_path = ChromeDriverManager(version=chrome_version).install()
        else:
            print("[INFO] ChromeDriver already installed. Reusing.")

        # Launch driver
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
        driver.get("https://web.whatsapp.com/")

        print("Waiting for WhatsApp Web to load...")
        time.sleep(10)

        for number in phone_numbers:
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            driver.get(url)
            print(f"Opening chat with {number}")
            time.sleep(30)  # Wait for chat to load

            try:
                send_button = driver.find_element(By.XPATH, "//span[@data-icon='send']")
                send_button.click()
                print(f"Message sent to {number}")
                time.sleep(30)  # Delay between messages
            except Exception as e:
                print(f"Failed to send message to {number}: {e}")


        driver.quit()
    except Exception as e:
        print(f"Error in WhatsApp automation: {e}")
