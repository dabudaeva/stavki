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
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html',
                           name=bk.name,
                           link=bk.homepage,
                           description=bk.description,
                           image=bk.logo,
                           indexes=np.arange(bk.shape[0]))

df = pd.read_csv('data/data.csv', decimal=',')
df['Marginal_'] = round((1/df.W1+1/df.Draw+1/df.W2)*100-100, 2)


@app.route('/bet', methods=['GET', 'POST'])
def fork():
    countries1 = df.Team_1.unique().tolist()
    countries2 = df.Team_2.unique().tolist()
    select1, select2 = None, None
    coef1, draw, coef2 = None, None, None
    deposit, best = None, None
    indexes = None
    df_select = pd.DataFrame(columns=list(set(df.columns.append(bk.columns))))
    if request.method == 'POST':
        select1 = request.form.get('select-1')
        select1 = None if select1 == 'None' else select1
        countries2 = df.loc[df.Team_1 == select1, 'Team_2'].unique().tolist()
        select2 = request.form.get('select-2')
        select2 = None if select2 == 'None' else select2
        try:
            df_select = df.loc[(df['Team_1'] == select1) & (df['Team_2'] == select2)]
            df_select = df_select.merge(bk, on='Bookmakers')
            indexes = np.arange(len(df_select.Bookmakers))
        except: pass
        coef1 = request.form.get('coef-1')
        coef1 = None if coef1 == 'None' else coef1
        coef2 = request.form.get('coef-2')
        coef2 = None if coef2 == 'None' else coef2
        draw = request.form.get('draw')
        draw = None if draw == 'None' else draw
        deposit = request.form.get('deposit')
        deposit = None if deposit == 'None' else deposit
    if all([deposit, coef1, coef2, draw]):
        try:
            my_bet = bet(int(deposit), [float(coef1), float(draw), float(coef2)])
            best = my_bet.best_combinations3()
        except:
            print("Не получилось рассчитать вилку")
    return render_template('bet.html',
                           countries1=countries1,
                           countries2=countries2,
                           select1=select1,
                           select2=select2,
                           indexes=indexes,
                           link=df_select.homepage,
                           logo=df_select.logo,
                           tcoef1=df_select.W1,
                           tdraw=df_select.Draw,
                           tcoef2=df_select.W2,
                           marga=df_select.Marginal_,
                           coefs1=df_select.W1.sort_values(ascending=False),
                           draws=df_select.Draw.sort_values(ascending=False),
                           coefs2=df_select.W2.sort_values(ascending=False),
                           coef1=coef1,
                           draw=draw,
                           coef2=coef2,
                           deposit=deposit,
                           bet=best
                           )

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)

