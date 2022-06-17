from app import main, scheduler, app


if __name__ == '__main__':
    # установка планировщика apscheduler обновлять каждык 60 сек бд с таблицей,
    # каждый вечер в 20.00 отправлять сообщение просроченных заказах
    # и его запуск
    scheduler.add_job(id='update_data', func=main.update_data, trigger="interval", seconds=60)
    scheduler.add_job(id='check_date', func=main.check_date, trigger="cron", hour=17, minute=00)
    scheduler.start()

    app.run(host="0.0.0.0")

