import numpy as np
from flask import Flask, render_template, abort, request
from flask.json import jsonify
from scripts.forks import bet
import pandas as pd

bk = pd.read_csv('data/bookmakers.csv')
bk['Bookmakers'] = bk['bookmaker']

app = Flask(__name__)

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description['message']})
    abort(400, {'message': 'custom error message to appear in body'})

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           name=bk.name,
                           link=bk.homepage,
                           description=bk.description,
                           image=bk.logo,
                           indexes=np.arange(bk.shape[0]))

df = pd.read_csv('data/data.csv', decimal=',')
df['Marginal_'] = round((1/df.W1+1/df.Draw+1/df.W2)*100-100, 2)


@app.route('/data', methods=['GET', 'POST'])
def data():
    countries1 = df.Team_1.unique().tolist()
    countries2 = df.Team_2.unique().tolist()
    select1, select2 = None, None
    df_select = pd.DataFrame(columns=list(set(df.columns.append(bk.columns))))
    indexes = None
    # sort = None
    if request.method == 'POST':
        select1 = request.form.get('select-1')
        countries2 = df.loc[df.Team_1 == select1, 'Team_2'].unique().tolist()
        if select1 != None:
            select2 = request.form.get('select-2')
            if select2 != None:
                try:
                    df_select = df.loc[(df['Team_1'] == select1) & (df['Team_2'] == select2)]
                    df_select = df_select.merge(bk, on='Bookmakers')
                    indexes = np.arange(len(df_select.Bookmakers))

                    # sort = request.form.get('sort-action')
                    # if sort != None:
                    #     if sort == 'БК': df_select = df_select.sort_values(by='Bookmakers')
                    #     elif sort == select1: df_select = df_select.sort_values(by='W1')
                    #     elif sort == 'Ничья': df_select = df_select.sort_values(by='Draw')
                    #     elif sort == select2: df_select = df_select.sort_values(by='W2')
                    #     elif sort == 'Маржа': df_select = df_select.sort_values(by='Marginal_')
                except:
                    print('такого матча нет')
    return render_template('data.html',
                           countries1=countries1,
                           countries2=countries2,
                           select1=select1,
                           select2=select2,
                           link=df_select.homepage,
                           logo=df_select.logo,
                           coef1=df_select.W1,
                           draw=df_select.Draw,
                           coef2=df_select.W2,
                           marga=df_select.Marginal_,
                           indexes=indexes,
                           # sort=sort
                           )

@app.route('/fork')
def fork():
    countries1 = df.Team_1.unique().tolist()
    countries2 = df.Team_2.unique().tolist()
    select1, select2 = None, None
    if request.method == 'POST':
        select1 = request.form.get('select-1')
        countries2 = df.loc[df.Team_1 == select1, 'Team_2'].unique().tolist()
        if select1 != None:
            select2 = request.form.get('select-2')
    return render_template('fork.html',
                           countries1=countries1,
                           countries2=countries2,
                           select1=select1,
                           select2=select2,
                           )

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)

# Чтобы запустить приложение нужно ввести в консоли export FLASK_APP=app.py
# Затем flask run


#

#df = pd.read_csv('data/qatar_ecuador.csv', decimal=',')
# max_coef = [df.W1.max(), df.Draw.max(), df.W2.max()]
# my_bet = bet(100000, max_coef)
# best = my_bet.best_combinations3()
