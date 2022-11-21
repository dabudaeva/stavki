# DataBet

DataBet - это агрегатор-приложение для сбора и анализа букмекерских коэффициентов на предстоящий ЧМ 2022 по футболу.
Приложение реализовано с помощью:

- Selenium (для парсинга коэффициентов)
- Numpy, pandas (для работы с данными)
- scikit-learn, lightgbm, XGBoost, catboost, pytorch (для предсказания собственных коэффициентов)
- flask, html&css (для разработки сайта)


Чтобы запустить приложение, нужно скачать репозиторию, ввестив терминале:

- $ pip install -r requirements.txt
- $ export FLASK_APP=app.py
- $ flask run
