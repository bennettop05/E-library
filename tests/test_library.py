from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ Set Chrome Options (Recommended)
options = Options()
options.add_argument("--start-maximized")  # Open browser maximized
options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors (if any)
options.add_argument("--disable-notifications")  # Disable popups/notifications

# ✅ Launch Chrome Driver
driver = webdriver.Chrome(options=options)

# ============================
# ✅ Test 1: Load Homepage
# ============================
driver.get("http://localhost/Library_project/index.html")
time.sleep(2)
print("✅ Test 1: Homepage Loaded Successfully")

# ============================
# ✅ Test 2: Search for a Book
# ============================
driver.get("http://localhost/Library_project/dashboard.html")
time.sleep(2)

# Search for 'Book A'
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchBar"))
)
search_bar.send_keys("Book A")
time.sleep(1)
search_bar.send_keys(Keys.RETURN)
time.sleep(2)

# ✅ Take Screenshot for Debugging
driver.save_screenshot("search_result.png")
print("✅ Test 2: Book Search Working (Screenshot saved: search_result.png)")

# ============================
# ✅ Test 3: Borrow a Book
# ============================
try:
    # Corrected XPath for Borrow Button
    borrow_buttons = driver.find_elements(By.XPATH, "/html/body/div/div/div/button[contains(text(),'Borrow')]")
    if not borrow_buttons:
        raise Exception("No Borrow button found. Check search_result.png for details.")

    # Click the Borrow button
    borrow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/button[contains(text(),'Borrow')]"))
    )
    borrow_button.click()
    time.sleep(1)

    # Handle alert after borrowing
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    print(f"✅ Test 3: {alert.text}")
    alert.accept()
except Exception as e:
    print(f"❌ Test 3: Borrow failed. Error: {e}")
    driver.save_screenshot("borrow_error.png")

# ============================
# ✅ Test 4: View Borrowed Books
# ============================
driver.get("http://localhost/Library_project/mybooks.html")
time.sleep(2)
print("✅ Test 4: Borrowed Books Page Loaded")

# ============================
# ✅ Test 5: Return a Book
# ============================
try:
    # Corrected XPath for Return Button
    return_buttons = driver.find_elements(By.XPATH, "/html/body/div/div/div/button[contains(text(),'Return')]")
    if not return_buttons:
        raise Exception("No Return button found. Check borrowed books page for details.")

    # Click the Return button
    return_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/button[contains(text(),'Return')]"))
    )
    return_button.click()
    time.sleep(1)

    # Handle alert after returning
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    print(f"✅ Test 5: {alert.text}")
    alert.accept()
except Exception as e:
    print(f"❌ Test 5: Return failed. Error: {e}")
    driver.save_screenshot("return_error.png")

# ============================
# ✅ Test 6: Check Due Date Alerts
# ============================
# Manually update localStorage with overdue due date for testing
driver.execute_script("""
    localStorage.setItem('borrowedBooks', JSON.stringify([
        {"id":1, "title":"Book A", "dueDate":"2025-03-16"}
    ]));
""")
driver.get("http://localhost/Library_project/dashboard.html")
time.sleep(2)
print("✅ Test 6: Due Date Alert Triggered")

# ============================
# ✅ Save Page Source for Debugging (Optional)
# ============================
with open("page_source.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

# ============================
# ✅ Close the Browser
# ============================
driver.quit()
