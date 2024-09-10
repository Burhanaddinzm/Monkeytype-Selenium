from selenium import webdriver # type: ignore 
from selenium.webdriver.common.by import By # type: ignore 
from selenium.webdriver.support.ui import WebDriverWait # type: ignore 
from selenium.webdriver.support import expected_conditions as EC # type: ignore 
from selenium.common.exceptions import TimeoutException# type: ignore 
from selenium.webdriver.chrome.options import Options # type: ignore 
from selenium.webdriver.common.keys import Keys # type: ignore 
from selenium.webdriver.common.action_chains import ActionChains # type: ignore 
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
    def get_words_list():
        words_list_elements = driver.find_elements(By.CSS_SELECTOR, "div.word:not(.typed)")
        return [element.text.strip() for element in words_list_elements if element.text.strip()]

    def get_current_active_word():
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.word.active"))
        )
        return "".join([letter.text for letter in element.find_elements(By.TAG_NAME, "letter")])

    words_list = get_words_list()
    word_index = 0

    while True:
        try:
            current_word = get_current_active_word()
            if current_word == "":  
                break
            print(f"Current active word: '{current_word}'")

            if word_index >= len(words_list):
                words_list = get_words_list()
                word_index = 0
                print("Word list updated with new words.")

            if current_word == words_list[word_index]:
                print(f"Completing word '{current_word}'")

                actions.send_keys(current_word).perform()
                actions.send_keys(Keys.SPACE).perform()
                
                word_index += 1
            else:
                print(f"Current word '{current_word}' not in the expected list at index {word_index}.")

        except TimeoutException:
            print("Timed out waiting for active word element or processing word")
            break

finally:
    time.sleep(10)
    driver.quit()