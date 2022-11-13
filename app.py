import os

import numpy as np
import pandas as pd
from itertools import product

from flask import Flask, render_template, abort, request
from flask.json import jsonify
from scripts.forks import bet

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

bk = pd.read_csv('data/bookmakers.csv')

app = Flask(__name__)

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description['message']})
    abort(400, {'message': 'custom error message to appear in body'})

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html',
                           name=bk.name,
                           link=bk.homepage,
                           description=bk.description,
                           image=bk.logo,
                           indexes=np.arange(bk.shape[0]))

# os.system('scripts/parser.py')

df = pd.read_csv('data/data.csv')
data_coef = []
for i, row in df[['Team_1', 'Team_2']].drop_duplicates().iterrows():
    df_select = df.loc[(df['Team_1'] == row.Team_1) & (df['Team_2'] == row.Team_2)]
    data = pd.DataFrame(list(product(*df_select[['W1', 'Draw', 'W2']].values.T)), columns=['W1', 'Draw', 'W2'])
    data['Fork'] = 1 / data.W1 + 1 / data.W2 + 1 / data.Draw
    data['Team_1'] = row.Team_1
    data['Team_2'] = row.Team_2
    data_coef.append(data)

data_coef = pd.concat(data_coef)
data_coef = data_coef.sort_values(by='Fork')
data_coef = data_coef[data_coef.Fork < 1]


@app.route('/bet', methods=['GET', 'POST'])
def fork():
    countries1 = df.Team_1.sort_values(ascending=False).unique().tolist()
    countries2 = None
    select1, select2 = None, None
    coef1, draw, coef2 = None, None, None
    deposit, best_coef, best_bet = None, None, None
    indexes, indexes2 = None, None
    df_select = pd.DataFrame(columns=list(set(df.columns.append(bk.columns))))
    coefs, profit = None, None
    link, logo = None, None

    if request.method == 'POST':
        select1 = request.form.get('select-1')
        select1 = None if select1 == 'None' else select1
        countries2 = df.loc[df.Team_1 == select1, 'Team_2'].sort_values(ascending=False).unique().tolist()
        select2 = request.form.get('select-2')
        select2 = None if select2 == 'None' else select2

        deposit = request.form.get('deposit')
        deposit = None if deposit == 'None' else deposit

        coef1 = request.form.get('coef-1')
        coef1 = None if coef1 == 'None' else coef1
        coef2 = request.form.get('coef-2')
        coef2 = None if coef2 == 'None' else coef2
        draw = request.form.get('draw')
        draw = None if draw == 'None' else draw

        try:
            df_select = df.loc[(df['Team_1'] == select1) & (df['Team_2'] == select2)]
            df_select = df_select.merge(bk, on='BookMakers')
            indexes = np.arange(df_select.shape[0])

            data = pd.DataFrame(list(product(*df_select[['W1', 'Draw', 'W2']].values.T)), columns=['W1', 'Draw', 'W2'])
            data['Fork'] = 1 / data.W1 + 1 / data.W2 + 1 / data.Draw
            data = data[data.Fork < 1]
            data = data.reset_index(drop=True)
            if not data.empty:
                indexes2 = np.arange(data.shape[0])
                best_coef = data.loc[data.Fork == data.Fork.min()]
                best_coef = [best_coef.W1.item(), best_coef.Draw.item(), best_coef.W2.item()]
                logo = [df_select.loc[df_select.W1==best_coef[0], 'logo'].item(),
                        df_select.loc[df_select.Draw==best_coef[1], 'logo'].item(),
                        df_select.loc[df_select.W2==best_coef[2], 'logo'].item()]
                link = [df_select.loc[df_select.W1==best_coef[0], 'homepage'].item(),
                        df_select.loc[df_select.Draw==best_coef[1], 'homepage'].item(),
                        df_select.loc[df_select.W2==best_coef[2], 'homepage'].item()]

        except: pass

        try:
            coefs = [float(coef1), float(draw), float(coef2)]
            my_bet = bet(int(deposit), coefs)
            best_bet = my_bet.best_combinations3()
            profit = [round(coefs[0]*best_bet[0]-int(deposit), 2),
                      round(coefs[1]*best_bet[1]-int(deposit), 2),
                      round(coefs[2]*best_bet[2]-int(deposit), 2)]

        except: pass

    return render_template('bet.html',
                           countries1=countries1, countries2=countries2,
                           select1=select1, select2=select2,
                           indexes=indexes,
                           link=df_select.homepage, logo=df_select.logo,
                           tcoef1=df_select.W1, tdraw=df_select.Draw, tcoef2=df_select.W2,
                           marga=df_select.Marginal,
                           coefs1=df_select.W1.sort_values(ascending=False),
                           draws=df_select.Draw.sort_values(ascending=False),
                           coefs2=df_select.W2.sort_values(ascending=False),
                           coef1=coef1, draw=draw, coef2=coef2,
                           deposit=deposit,
                           best_coef=best_coef,
                           best_link=link, best_logo=logo,
                           best_bet=best_bet,
                           indexes2=indexes2,
                           coefs=coefs,
                           profit=profit)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)

