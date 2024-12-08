import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

download_dir = "./download"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Chrome options configuration
def get_chrome_options(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options

links = os.getenv("LINKS", "").splitlines()

def download_file(url, download_dir):
    driver = None
    try:
        # Initialize ChromeDriver
        chrome_options = get_chrome_options(download_dir)
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        time.sleep(4)
        
        download_button = driver.find_element(By.XPATH, "//a[contains(@class, 'link-button') and contains(text(), 'Download')]")
        
        actions = ActionChains(driver)
        for _ in range(1):
            actions.double_click(download_button).perform()
            time.sleep(1)
        
    except Exception as e:
        print(f"Error while processing {url}: {e}")
    finally:
        # Ensure the driver quits after use
        if driver:
            driver.quit()

def remove_downloads(directory):
    try:
        for file in os.listdir(directory):
            if file.endswith(".crdownload"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)
    except Exception as e:
        print(f"Error while canceling downloads: {e}")

# Process each link
for link in links:
    if link.strip().startswith("#"):
        continue
    download_file(link, download_dir)

# Clean up temporary downloads
time.sleep(3)
remove_downloads(download_dir)
