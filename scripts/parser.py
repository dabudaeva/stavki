import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
time.sleep(5)

driver.get("https://1xstavka.ru/line/football/1938952-fifa-world-cup-2022")
time.sleep(5)

# textarea = driver.find_element(By.CSS_SELECTOR, ".textarea") # поиск текстового поля
# textarea.send_keys("get()") # заполнить текстовое поле
# time.sleep(5)

# submit_button = driver.find_element(By.CSS_SELECTOR, ".submit-submission") # поиск кнопки
# submit_button.click() # нажать на кнопку
# time.sleep(5)

driver.quit()