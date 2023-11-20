from sanic import Sanic

from src.core import init_app

app = Sanic(__name__)
init_app(app)
