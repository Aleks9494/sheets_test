import os

import pygsheets
from app.models import MyModel
from pycbrf.toolbox import ExchangeRates
from datetime import datetime, date
from flask import jsonify
from app import app, db, bot


@app.route('/orders', methods=['GET'])
def show_orders():
    orders = MyModel.query.all()
    orders_json = list()
    for order in orders:
        order_json = order.as_dict()  # объект БД в словарь
        orders_json.append(order_json)
    return jsonify(orders_json)       # возврат JSON


# Получаем данные с гугл таблиц
def update_data():
    gc = pygsheets.authorize(service_file='app/client_secret.json')  # Авторизация по по ключу из файла
    file = gc.open('test_2')         # открываем файл
    page = file[0]                    # 1 лист
    data = page.get_all_records()   # сохраняем данные с гугл таблиц в переменную, список словарей
    course = ExchangeRates(date.today())['USD'].value
    # получеем актульное значение доллара модулем pycbrf.toolbox: ExchangeRates
    db.session.query(MyModel).delete()   # Очищаем данные в таблице
    db.session.commit()
    for row in data:                    # для каждого ряда из таблицы создаем запись в БД
        id = row.get("№")
        order_number = row.get("заказ №")
        cost_dollar = row.get("стоимость,$")
        order_date = row.get("срок поставки")
        cost_rubles = float(cost_dollar) * float(course)
        order = MyModel(id=id, order_number=order_number, cost_dollar=cost_dollar,
                        cost_rubles=round(cost_rubles, 2), order_date=order_date)
        db.session.add(order)
        db.session.commit()
        db.session.close()


def check_date():                                     # проверка даты заказа
    orders = MyModel.query.all()
    for order in orders:                              # для каждой записи из БД
        date = datetime.strptime(order.order_date, "%d.%m.%Y").date()   # переводим дату типа str в тип date
        if date <= date.today():                                        # если дата заказа меньше или равна сегодня
            text = 'Заказ '+f'{order.order_number}'+' просрочен'
            bot.send_message(os.environ.get('id'), text)                    # бот отправляет сообщение по id в мой бот в телеграм
    db.session.close()






