from flask import Flask


app = Flask(__name__)


from demo.routes import *
