"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



import FlaskWebProject1.views
