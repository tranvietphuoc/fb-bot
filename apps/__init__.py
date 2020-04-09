from dotenv import load_dotenv
import os
from flask import Flask
from apps.config import Config


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
# print(dotenv_path)
load_dotenv(dotenv_path=dotenv_path, override=True)


PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PORT = os.getenv('PORT')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from apps.webhooks.routes import webhooks
    app.register_blueprint(webhooks)

    return app
