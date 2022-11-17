# Импорт опций Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from fake_useragent import UserAgent

# import split_div_BetCity
# import save_to_csv

from scripts.parsing.split_div_BetCity import split_list
from scripts.parsing.save_to_csv import save_to_file
"""
from parsing.split_div_BetCity import split_list
from parsing.save_to_csv import save_to_file
"""

"""
import os
path = os.getcwd()
print(f'\npath: {path}\n')
"""

def betcity(parsing_date):
    user_agent = UserAgent(verify_ssl=False, use_cache_server=False, fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36').chrome
    # print(f"\nuser_agent: {user_agent}\n")

    # driver = webdriver.Chrome('/home/petrucho/Downloads/chromedriver_linux64/chromedriver')
    driver = webdriver.Chrome('./scripts/parsing/chromedriver')
    # driver = webdriver.Chrome()

    # Инициализация опций Chrome
    chrome_options = Options()

    # Добавление желаемых возможностей
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=" + user_agent)

    # Неявное ожидание
    driver.implicitly_wait(10) # in seconds

    # Setting the window size to 1200 * 800
    driver.set_window_size(1200, 800)
    
    # ЧМ 2022
    driver.get("https://betcity.ru/ru/line/bets?chmp%5B%5D=167030")

    # maximize again
    driver.fullscreen_window()

    # wait until page will downloaded in browser
    time.sleep(10)    

    try:    
        # page_source = driver.page_source
        # print(f'page_source: {page_source}')

        # save screenshot of the page
        driver.save_screenshot('./images/BetCity_world_cup_2022.png')

        xp_block = '//div[@class="line__champ"]'   
        block_name = driver.find_elements(By.XPATH, xp_block)    
        block_name_list = [value.text for value in block_name]
        # print(f'\nblock_name_list: {block_name_list}\n')

        # splitted_list = split_div_BetCity.split_list(block_name_list) # split List
        # save_to_csv.save_to_file(splitted_list) # splitted List saving to csv-file
        splitted_list = split_list(block_name_list, parsing_date) # split List
        save_to_file(splitted_list) # splitted List saving to csv-file
        
    except:
        print("some error happen with parsing in betCity_WC2022.py!!")