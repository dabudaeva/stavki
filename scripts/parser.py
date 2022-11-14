# from parsing.BaltBet_WC2022_short import baltbet
from scripts.parsing.BetCity_WC2022_short import betcity
from scripts.parsing.FonBet_WC2022_short import fonbet
from scripts.parsing.LeonBet_WC2022_short import leonbet
from scripts.parsing.OlimpBet_WC2022_short import olimpbet
from scripts.parsing.Pari_WC2022_short import pari
from scripts.parsing.SportBet_WC2022_short import sportbet
from scripts.parsing.ZenitBet_WC2022_short import zenitbet
import pandas as pd
import os

def update_data():
    try:
        os.remove('./data/data.csv')
    except: pass

    # baltbet() # need to find on page
    # print('baltbet - done')

    betcity()
    print('betcity - done')

    fonbet()
    print('fonbet - done')

    leonbet()
    print('leonbet - done')

    olimpbet()
    print('olimpbet - done')

    pari()
    print('pari - done')

    sportbet()
    print('sportbet - done')

    zenitbet()
    print('zenitbet - done')

    df = pd.read_csv('./data/data.csv')
    df[['W1', 'Draw', 'W2']] = df[['W1', 'Draw', 'W2']].apply(lambda x: x.astype(str).str.replace(',', '.'))
    df = df.astype({'W1': 'float64', 'Draw': 'float64', 'W2': 'float64'})
    df['Marginal'] = round((1 / df.W1 + 1 / df.Draw + 1 / df.W2) * 100 - 100, 2)

    df.loc[df['Team_1'].str.contains('Корея'), 'Team_1'] = 'Южная Корея'
    df.loc[df['Team_2'].str.contains('Корея'), 'Team_2'] = 'Южная Корея'
    df.Team_1 = df.Team_1.replace(r'\s+', ' ', regex=True).str.strip()
    df.Team_2 = df.Team_2.replace(r'\s+', ' ', regex=True).str.strip()

    df.to_csv('./data/data.csv', index=False)
    return 'Done!'
