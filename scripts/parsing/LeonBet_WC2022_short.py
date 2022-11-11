# Импорт опций Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from fake_useragent import UserAgent

# import split_div_LeonBet
# import save_to_csv
from parsing.split_div_LeonBet import split_list
from parsing.save_to_csv import save_to_file

def leonbet():
    user_agent = UserAgent(verify_ssl=False).chrome
    # print(f"\nuser_agent: {user_agent}\n")

    # driver = webdriver.Chrome('/home/petrucho/Downloads/chromedriver_linux64/chromedriver')
    driver = webdriver.Chrome('./scripts/parsing/chromedriver')

    # Инициализация опций Chrome
    chrome_options = Options()

    # Добавление желаемых возможностей
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=" + user_agent)

    # Неявное ожидание
    driver.implicitly_wait(10) # in seconds

    # ЧМ 2022
    driver.get("https://leon.ru/bets/soccer/world/1970324836989529-world-cup-2022")

    # wait until page will downloaded in browser
    time.sleep(15)

    try:    
        # page_source = driver.page_source
        # print(page_source)

        # save screenshot of the page
        driver.save_screenshot('./data/LeonBet_world_cup_2022.png')

        xp_block = '//*[@id="app"]/section/div/main/div/div/div[2]/div/div[3]/div[2]/div/div/div[2]'
        block_name = driver.find_elements(By.XPATH, xp_block)    
        block_name_list = [value.text for value in block_name]
        # print(f'\nblock_name_list: {block_name_list}\n')

        splitted_list = split_list(block_name_list) # split List
        save_to_file(splitted_list) # splitted List saving to csv-file
        
    except:
        print("some error happen !!")