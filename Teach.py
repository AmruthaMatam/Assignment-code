from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

number = "0000020232"
otp = "120992"

default_options = [
    "--disable-extensions",
    "--disable-user-media-security=true",
    "--allow-file-access-from-files",
    "--use-fake-device-for-media-stream",
    "--use-fake-ui-for-media-stream",
    "--disable-popup-blocking",
    "--disable-infobars",
    "--enable-usermedia-screen-capturing",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--auto-select-desktop-capture-source=Screen 1",
    "--disable-blink-features=AutomationControlled",
    "--disable-more"
]

headless_options = ["--headless", "--use-system-clipboard", "--window-size=1920x1080"]


def browser_options(type_of_chrome):
    webdriver_options = webdriver.ChromeOptions()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)

    if type_of_chrome == "headless":
        var = default_options + headless_options
    else:
        var = default_options

    for d_o in var:
        webdriver_options.add_argument(d_o)

    return webdriver_options


# opening the chrome and launching the website
chrome_type = "default"
options = browser_options(chrome_type)
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)
driver.set_window_position(0, 0)
driver.implicitly_wait(10)
driver.maximize_window()
download_dir = "C:/path/to/download/directory"

driver.get("https://accounts.teachmint.com/")
driver.implicitly_wait(25)

# input phone No
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'user-input'))).click()
loginBox = driver.find_element(By.XPATH, "//input[@type='text']")
loginBox.send_keys(number)
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="send-otp-btn-id"]').click()
time.sleep(3)

# input otp & login
_input_otp_field = "//input[@data-group-idx='{}']"
for i, otp_digit in enumerate(otp):
    otp_field_xpath = _input_otp_field.format(i)
    otp_field = driver.find_element(By.XPATH, otp_field_xpath)
    time.sleep(1)
    otp_field.send_keys(otp_digit)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit-otp-btn-id"]'))).click()
time.sleep(5)

# Open the profile
automate2_profile = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[4]/div[2]/div/div[1]/div[3]'))
)
automate2_profile.click()
time.sleep(10)
# Go to the dashboard
element = driver.find_element(By.CSS_SELECTOR, 'span[data-qa="icon-dashboard1"]')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
time.sleep(5)

# Select Administrator
driver.find_element(By.CSS_SELECTOR, 'span[data-qa="icon-administrator"]').click()
time.sleep(5)
driver.find_element(By.LINK_TEXT, 'Certificates').click()  # click on certificates
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//h6[@data-qa='heading' and contains(text(), 'School leaving "
                                          "certificate')]"))).click()
time.sleep(5)

# Click to generate and download certificate.
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="button,disabled-false"][body="Generate"]'))).click()
time.sleep(5)
button = driver.find_element(By.XPATH, "//td[@class='krayon__TableVirtualized-module__KaQPS "
                                       "krayon__TableVirtualized-module__1bLc2']//button[@data-qa='button,"
                                       "disabled-false']//div[text()='Generate']")
button.click()
time.sleep(5)
driver.execute_script("window.scrollTo(0,200);")
remarks_input = driver.find_element(By.XPATH, "//input[@class='krayon__TextInput-module__3VrcP' and "
                                              "@placeholder='Remarks']")
remarks_input.send_keys("Sam is a very good student")
time.sleep(5)
generate_button = driver.find_element(By.XPATH, "//div[@class='krayon__Button-module__UJ3Zt "
                                                "krayon__Button-module__GCm3-' and text()='Generate']")
generate_button.click()
time.sleep(5)
download_button = driver.find_element(By.XPATH, '//*[@id="download"]')
download_button.click()
time.sleep(6)
# Go back to certificates page
driver.back()
time.sleep(2)
driver.back()
time.sleep(3)
# validate history of certificates
view_all_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'TemplatesOverview_documentHeader__pWOoK')]/span[text()='View All']"))
)
view_all_button.click()
time.sleep(3)

driver.quit()
