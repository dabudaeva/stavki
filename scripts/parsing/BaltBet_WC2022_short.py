# Импорт опций Chrome
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from fake_useragent import UserAgent

# import split_div_BaltBet
# import save_to_csv
from parsing.save_to_csv import save_to_file
from parsing.split_div_BaltBet import split_list

"""
alternative calling driver for Chrome:
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#configure webdriver manager
driver = webdriver.Chrome(ChromeDriverManager().install())
# wait until page will downloaded in browser
time.sleep(5)
"""

"""
import os
path_to_driver = '/scripts/parsing/chromedriver'
path = os.getcwd() + path_to_driver
# print(path)
"""

def baltbet():
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
    driver.get("https://baltbet.ru/prematch")

    # wait until page will downloaded in browser
    time.sleep(20)

    try:    
        # page_source = driver.page_source
        # print(f'page_source: {page_source}')

        # save screenshot of the page
        driver.save_screenshot('./data/BaltBet_world_cup_2022.png')

        # xp_block = '//*[@id="bet-place"]/div/div[2]/div[147]/div/div'
        xp_block = '//*[@id="bet-place"]/div[3]/div[2]/div[224]/div/div'
        block_name = driver.find_elements(By.XPATH, xp_block)    
        block_name_list = [value.text for value in block_name]
        # print(f'\nblock_name_list: {block_name_list}\n')

        # splitted_list = split_div_BaltBet.split_list(block_name_list) # split List
        splitted_list = split_list(block_name_list) # split List
        save_to_file(splitted_list) # splitted List saving to csv-file
        
    except:
        print("some error happen with parsing in BaltBet!!")

