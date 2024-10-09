from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time

def run_test(test_id):
    print(test_id)
    # Create Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run headless if needed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the remote driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Test {test_id} failed to connect to Selenium Grid: {e}")
        return
    try:
        driver.get("https://the-internet.herokuapp.com/large")
        print(f"Test {test_id}: Title of the page is:", driver.title)
        time.sleep(3)
        rows = driver.find_elements(By.CSS_SELECTOR, "table[id='large-table'] tr")
        for r in rows:
            print(r.text)
    except Exception as e:
        print(f"Test {test_id} encountered an error: {e}")
    finally:
        driver.quit()

# Run tests in parallel
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(run_test, range(1, 3))  # Run two tests in parallel
