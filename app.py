import os

import numpy as np
import pandas as pd
from itertools import product

from flask import Flask, render_template, abort, request
from flask.json import jsonify
from scripts.forks import compute_bet

from scripts.parser import update_data

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


@app.route('/json')
def json():
    return render_template('json.html')


@app.route('/background_process_test')
def background_process_test():
    update_data()
    return ("nothing")


@app.route('/bet', methods=['GET', 'POST'])
def bet():
    df = pd.read_csv('data/data.csv')
    df = df.groupby(['BookMakers', 'Team_1', 'Team_2']).agg(['last']).reset_index()
    df['Marginal'] = round((1 / df.W1 + 1 / df.Draw + 1 / df.W2) * 100 - 100, 2)
    df.columns = df.columns.droplevel(1)
    bk = pd.read_csv('data/bookmakers_all.csv')
    countries1 = df.Team_1.sort_values(ascending=True).unique().tolist()
    countries2 = None
    select1, select2 = None, None
    indexes, indexes2 = None, None
    df_select = pd.DataFrame(columns=list(set(df.columns.append(bk.columns))))
    best_coef, link, logo = None, None, None

    preds = pd.read_csv('data/ratings/predicted2.csv', index_col=[0])
    coefs = 1/preds.iloc[:, 2:]

    coefs[['home_team', 'away_team']] = preds[['home_team', 'away_team']]
    teams = {'Qatar':'Катар', 'Ecuador':'Эквадор', 'Senegal':'Сенегал', 'Netherlands':'Нидерланды',
             'England':'Англия', 'Iran':'Иран', 'USA':'США', 'Wales':'Уэльс', 'Argentina':'Аргентина',
             'Saudi Arabia':'Саудовская Аравия', 'Mexico':'Мексика', 'Poland':'Польша',
             'France':'Франция', 'Australia':'Австралия', 'Denmark':'Дания', 'Tunisia':'Тунис',
             'Spain':'Испания', 'Costa Rica':'Коста-Рика', 'Germany':'Германия', 'Japan':'Япония',
             'Belgium':'Бельгия', 'Canada':'Канада', 'Morocco':'Марокко', 'Croatia':'Хорватия',
             'Brazil':'Бразилия', 'Serbia':'Сербия', 'Switzerland':'Швейцария',
             'Cameroon':'Камерун', 'Portugal':'Португалия', 'Ghana':'Гана', 'Uruguay':'Уругвай',
             'South Korea':'Южная Корея'}
    coefs.home_team = coefs.home_team.map(teams)
    coefs.away_team = coefs.away_team.map(teams)

    df_select_coef=pd.DataFrame(columns=['Команда 1', 'Команда 2'])

    if request.method == 'POST':
        if request.form.get('update_data') == 'Update!':
            update_data()

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

        try:
            df_select_coef = coefs.loc[(coefs.home_team == select1) & (coefs.away_team == select2)]
            if df_select_coef.empty:
                df_select_coef = pd.DataFrame(columns=['Команда 1', 'Команда 2'])
            df_select_coef = pd.DataFrame([df_select_coef[['mean_home', 'mean_away']].to_numpy()[0],
                                           df_select_coef[['lm_home', 'lm_away']].to_numpy()[0],
                                           df_select_coef[['knn_home', 'knn_away']].to_numpy()[0],
                                           df_select_coef[['rf_home', 'rf_away']].to_numpy()[0],
                                           df_select_coef[['gb_home', 'gb_away']].to_numpy()[0],
                                           df_select_coef[['lgbm_home', 'lgbm_away']].to_numpy()[0],
                                           df_select_coef[['xgb_home', 'xgb_away']].to_numpy()[0],
                                           df_select_coef[['cb_home', 'cb_away']].to_numpy()[0],
                                           df_select_coef[['sc_home', 'sc_away']].to_numpy()[0],
                                           df_select_coef[['nn_home', 'nn_away']].to_numpy()[0]],
                                         index=['Mean', 'LogisticRegression', 'KNeighborsClassifier',
                                                'RandomForestClassifier', 'GradientBoostingClassifier',
                                                'LGBMClassifier', 'XGBClassifier',
                                                'CatBoostClassifier', 'StackingClassifier',
                                                'Simple NN'], columns=[select1, select2])
            df_select_coef = df_select_coef.round(2)
            df_select_coef = df_select_coef.apply(lambda x: x.astype('object'))
        except:
            try:
                df_select_coef = coefs.loc[(coefs.home_team == select2) & (coefs.away_team == select1)]
                if df_select_coef.empty:
                    df_select_coef = pd.DataFrame(columns=['Команда 1', 'Команда 2'])
                df_select_coef = pd.DataFrame([df_select_coef[['mean_away', 'mean_home']].to_numpy()[0],
                                               df_select_coef[['lm_away', 'lm_home']].to_numpy()[0],
                                               df_select_coef[['knn_away', 'knn_home']].to_numpy()[0],
                                               df_select_coef[['rf_away', 'rf_home']].to_numpy()[0],
                                               df_select_coef[['gb_away', 'gb_home']].to_numpy()[0],
                                               df_select_coef[['lgbm_away', 'lgbm_home']].to_numpy()[0],
                                               df_select_coef[['xgb_away', 'xgb_home']].to_numpy()[0],
                                               df_select_coef[['cb_away', 'cb_home']].to_numpy()[0],
                                               df_select_coef[['sc_away', 'sc_home']].to_numpy()[0],
                                               df_select_coef[['nn_away', 'nn_home']].to_numpy()[0]],
                                              index=['Mean', 'LogisticRegression', 'KNeighborsClassifier',
                                                     'RandomForestClassifier', 'GradientBoostingClassifier',
                                                     'LGBMClassifier', 'XGBClassifier',
                                                     'CatBoostClassifier', 'StackingClassifier',
                                                     'Simple NN'], columns=[select1, select2])
                df_select_coef = df_select_coef.round(2)
                df_select_coef = df_select_coef.apply(lambda x: x.astype('object'))
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
                           tables=[df_select_coef.to_html(classes='table')],
                           )

@app.route('/fork', methods=['GET', 'POST'])
def fork():
    df = pd.read_csv('data/data.csv')
    bk = pd.read_csv('data/bookmakers_all.csv')
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
                           tables=[data_coef.to_html(classes='table')],
                           titles=data_coef.columns.values,
                           deposit=deposit, coef1=coef1, draw=draw, coef2=coef2,
                           best_bet=best_bet, profit=profit, coefs=coefs,
                           )


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)