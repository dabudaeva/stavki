import os

import numpy as np
import pandas as pd
from itertools import product

from flask import Flask, render_template, abort, request
from flask.json import jsonify
from scripts.forks import compute_bet

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


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
    bk = pd.read_csv('data/bookmakers.csv')
    return render_template('info.html',
                           name=bk.name,
                           link=bk.homepage,
                           description=bk.description,
                           image=bk.logo,
                           indexes=np.arange(bk.shape[0]))

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    df = pd.read_csv('data/data.csv')
    bk = pd.read_csv('data/bookmakers.csv')
    countries1 = df.Team_1.sort_values(ascending=True).unique().tolist()
    countries2 = None
    select1, select2 = None, None
    indexes, indexes2 = None, None
    df_select = pd.DataFrame(columns=list(set(df.columns.append(bk.columns))))
    best_coef, link, logo = None, None, None

    if request.method == 'POST':
        select1 = request.form.get('select-1')
        select1 = None if select1 == 'None' else select1
        countries2 = df.loc[df.Team_1 == select1, 'Team_2'].sort_values(ascending=True).unique().tolist()
        select2 = request.form.get('select-2')
        select2 = None if select2 == 'None' else select2

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


    return render_template('bet.html',
                           countries1=countries1, countries2=countries2,
                           select1=select1, select2=select2,
                           indexes=indexes,
                           indexes2=indexes2,
                           link=df_select.homepage, logo=df_select.logo,
                           tcoef1=df_select.W1, tdraw=df_select.Draw, tcoef2=df_select.W2,
                           marga=df_select.Marginal,
                           best_coef=best_coef,
                           best_link=link, best_logo=logo,
                           )

@app.route('/fork', methods=['GET', 'POST'])
def fork():
    df = pd.read_csv('data/data.csv')
    bk = pd.read_csv('data/bookmakers.csv')
    deposit, coef1, draw, coef2 = None, None, None, None
    coefs, best_bet, profit = [None, None, None], [None, None, None], [None, None, None]
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
    data_coef = data_coef.drop_duplicates()
    data_coef = pd.merge(data_coef, df[['BookMakers', 'Team_1', 'Team_2', 'W1']], how='left', on=['W1', 'Team_1', 'Team_2'])
    data_coef = pd.merge(data_coef, df[['BookMakers', 'Team_1', 'Team_2', 'Draw']], how='left', on=['Draw', 'Team_1', 'Team_2'])
    data_coef = pd.merge(data_coef, df[['BookMakers', 'Team_1', 'Team_2', 'W2']], how='left', on=['W2', 'Team_1', 'Team_2'])

    data_coef = data_coef[data_coef.Fork < 1]
    data_coef = pd.DataFrame([
        data_coef.Team_1,
        data_coef.Team_2,
        data_coef[['W1', 'BookMakers_x']].apply(lambda x: ' '.join(map(str, x)), axis=1),
        data_coef[['Draw', 'BookMakers_y']].apply(lambda x: ' '.join(map(str, x)), axis=1),
        data_coef[['W2', 'BookMakers']].apply(lambda x: ' '.join(map(str, x)), axis=1)
    ], index=['Команда 1', 'Команда 2', 'Победа 1', 'Ничья', 'Победа 2']).transpose()

    if request.method == 'POST':
        deposit = request.form.get('deposit')
        coef1 = request.form.get('coef-1')
        coef2 = request.form.get('coef-2')
        draw = request.form.get('draw')

        try:
            coefs = [float(coef1), float(draw), float(coef2)]
            best_bet = compute_bet(int(deposit), coefs).best_combinations3()
            profit = [round(coefs[0] * best_bet[0] - int(deposit), 2),
                      round(coefs[1] * best_bet[1] - int(deposit), 2),
                      round(coefs[2] * best_bet[2] - int(deposit), 2)]
        except: pass

    return render_template('fork.html',
                           tables=[data_coef.to_html(classes='data')],
                           titles=data_coef.columns.values,
                           deposit=deposit, coef1=coef1, draw=draw, coef2=coef2,
                           best_bet=best_bet, profit=profit, coefs=coefs,
    )


@app.route("/datapage", methods=['GET', 'POST'])
def data_page():
    if request.method == 'POST':
        filesDict = request.files.to_dict()
        uploadData = request.files['media']
        data_file_name = uploadData.filename
        uploadData.save(os.path.join(app.root_path, 'uploads\\' + data_file_name))

    return render_template("upload.html")




if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)