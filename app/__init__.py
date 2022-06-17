from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import warnings
from telebot import TeleBot
from apscheduler.schedulers.background import BackgroundScheduler
import os


app = Flask(__name__)
app.config.from_object(Config)
scheduler = BackgroundScheduler()  # создание планировщика
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
bot = TeleBot(os.environ.get('token'))   # создание бота


warnings.filterwarnings(
 "ignore", message="The normalize method is no longer necessary, as this time zone supports the fold attribute")
warnings.filterwarnings(
 "ignore", message="The zone attribute is specific to pytz's interface")
warnings.filterwarnings(
 "ignore", message="The localize method is no longer necessary, as this time zone supports the fold attribute")


from app import main, models
