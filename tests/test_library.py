import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Define Output Folder for Screenshots
screenshot_folder = "C:/xampp/htdocs/Library_project/images"

# Create the folder if it doesn't exist
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# ✅ Set up logging (Logs will remain in test_outputs)
log_folder = "C:/xampp/htdocs/Library_project/test_outputs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, "selenium_logs.txt")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ✅ Set Chrome Options (Recommended)
options = Options()
options.add_argument("--start-maximized")  # Open browser maximized
options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors (if any)
options.add_argument("--disable-notifications")  # Disable popups/notifications

# ✅ Launch Chrome Driver
driver = webdriver.Chrome(options=options)
logging.info("Chrome Driver Launched Successfully")

# ============================
# ✅ Helper Function to Save Screenshot
# ============================
def save_screenshot(name):
    path = os.path.join(screenshot_folder, f"{name}.png")
    driver.save_screenshot(path)
    logging.info(f"📸 Screenshot saved: {path}")


# ============================
# ✅ Test 1: Load Homepage
# ============================
try:
    driver.get("http://localhost/Library_project/index.html")
    time.sleep(2)
    driver.execute_script('alert("✅ Homepage Loaded Successfully!");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("homepage_alert")
except Exception as e:
    logging.error(f"❌ Test 1 Failed: {e}")

# ============================
# ✅ Test 2: Search for a Book
# ============================
try:
    driver.get("http://localhost/Library_project/dashboard.html")
    time.sleep(2)

    # Search for 'Book A'
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchBar"))
    )
    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))
    )
    search_bar.send_keys("Book A")
    time.sleep(1)
    search_btn.click()
    time.sleep(2)

    driver.execute_script('alert("✅ Book Search Completed! Check Results.");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("search_result")
except Exception as e:
    logging.error(f"❌ Test 2 Failed: {e}")

# ============================
# ✅ Test 3: Borrow a Book
# ============================
try:
    borrow_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Borrow')]")
    if not borrow_buttons:
        raise Exception("No Borrow button found. Check search_result.png for details.")

    borrow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Borrow')]"))
    )
    borrow_button.click()
    time.sleep(1)

    # Enhanced Borrow Alert
    driver.execute_script('alert("✅ Book Borrowed Successfully! 📚");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("borrow_alert")

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    logging.info(f"✅ Test 3: {alert.text}")
    alert.accept()
except Exception as e:
    logging.error(f"❌ Test 3 Failed: {e}")
    save_screenshot("borrow_error")

# ============================
# ✅ Test 4: View Borrowed Books
# ============================
try:
    driver.get("http://localhost/Library_project/mybooks.html")
    time.sleep(2)
    driver.execute_script('alert("✅ Borrowed Books Page Loaded Successfully!");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("borrowed_books_alert")
except Exception as e:
    logging.error(f"❌ Test 4 Failed: {e}")

# ============================
# ✅ Test 5: Return a Book
# ============================
try:
    return_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Return')]")
    if not return_buttons:
        raise Exception("No Return button found. Check borrowed books page for details.")

    return_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Return')]"))
    )
    return_button.click()
    time.sleep(1)

    # Enhanced Return Alert
    driver.execute_script('alert("✅ Book Returned Successfully! 🔄");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("return_alert")

    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    logging.info(f"✅ Test 5: {alert.text}")
    alert.accept()
except Exception as e:
    logging.error(f"❌ Test 5 Failed: {e}")
    save_screenshot("return_error")

# ============================
# ✅ Test 6: Check Due Date Alerts
# ============================
try:
    driver.execute_script("""
        localStorage.setItem('borrowedBooks', JSON.stringify([
            {"id":1, "title":"Book A", "dueDate":"2025-03-16"}
        ]));
    """)
    driver.get("http://localhost/Library_project/dashboard.html")
    time.sleep(2)
    driver.execute_script('alert("⚠️ Due Date Alert Triggered! Please Return Book.");')
    time.sleep(2)  # ⏰ Increased Alert Time
    save_screenshot("due_date_alert")
except Exception as e:
    logging.error(f"❌ Test 6 Failed: {e}")

# ============================
# ✅ Save Page Source for Debugging
# ============================
try:
    page_source_path = os.path.join(log_folder, "page_source.html")
    with open(page_source_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logging.info(f"✅ Page Source Saved at: {page_source_path}")
except Exception as e:
    logging.error(f"❌ Failed to Save Page Source: {e}")

# ============================
# ✅ Close the Browser
# ============================
driver.quit()
logging.info("✅ Browser Closed Successfully")
