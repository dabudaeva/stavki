from scripts.parsing.baltBet_WC2022 import baltbet
from scripts.parsing.betCity_WC2022 import betcity
from scripts.parsing.fonBet_WC2022 import fonbet
from scripts.parsing.leonBet_WC2022 import leonbet
from scripts.parsing.olimpBet_WC2022 import olimpbet
from scripts.parsing.pari_WC2022 import pari
from scripts.parsing.sportBet_WC2022 import sportbet
from scripts.parsing.zenitBet_WC2022 import zenitbet

import pandas as pd
import os

import time

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple) # looks like 28/12/2022, 09:47:41
# print(f'time_string: {time_string}')
def update_data():
    """
    try:
        os.remove('./data/data.csv')
    except: pass
    """
    
    """
    baltbet(time_string) # need to find on page
    print('baltbet - done')
    """
        
    betcity(time_string)
    print('betcity - done')

    fonbet(time_string)
    print('fonbet - done')

    leonbet(time_string)
    print('leonbet - done')
    
    #olimpbet(time_string)
    #print('olimpbet - done')
    
    pari(time_string)
    print('pari - done')

    sportbet(time_string)
    print('sportbet - done')

    zenitbet(time_string)
    print('zenitbet - done')

    
    df = pd.read_csv('./data/data.csv', on_bad_lines='skip')
    df[['W1', 'Draw', 'W2']] = df[['W1', 'Draw', 'W2']].apply(lambda x: x.astype(str).str.replace(',', '.'))
    df = df.astype({'W1': 'float64', 'Draw': 'float64', 'W2': 'float64'})
    df['Marginal'] = round((1 / df.W1 + 1 / df.Draw + 1 / df.W2) * 100 - 100, 2)
    df.loc[df['Team_1'].str.contains('Корея'), 'Team_1'] = 'Южная Корея'
    df.loc[df['Team_2'].str.contains('Корея'), 'Team_2'] = 'Южная Корея'
    df.Team_1 = df.Team_1.replace(r'\s+', ' ', regex=True).str.strip()
    df.Team_2 = df.Team_2.replace(r'\s+', ' ', regex=True).str.strip()
    df.to_csv('./data/data.csv', index=False)
    
    return 'Done!'

# update_data()