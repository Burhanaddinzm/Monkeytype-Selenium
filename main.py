from selenium import webdriver 
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC  
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains 
import time

driver = webdriver.Chrome()

try:
    driver.get("https://monkeytype.com")

    try:
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.active.acceptAll"))
        )
        accept_all_button.click()
        print("Clicked 'accept all' button")
    except TimeoutException:
        print("Timed out waiting for 'accept all' button")

    try:
        timeconfig_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[timeconfig='60']"))
        )
        timeconfig_button.click()
        print("Clicked 'timeconfig=60' button")
        time.sleep(1)
    except TimeoutException:
        print("Timed out waiting for 'timeconfig=60' button")

    words_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "words"))
    )
    words_div.click()
    print("Clicked on 'words' div to focus")

    actions = ActionChains(driver)

    def get_current_active_word():
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.word.active"))
            )
            return "".join([letter.text for letter in element.find_elements(By.TAG_NAME, "letter")])
        except TimeoutException:
            return None

    while True:
        current_word = get_current_active_word()

        if current_word is None or current_word == "":
            print("No active word found or the typing test ended.")
            break

        print(f"Current active word: '{current_word}'")

        actions.send_keys(current_word).perform()
        actions.send_keys(Keys.SPACE).perform()

finally:
    time.sleep(10)
    driver.quit()
