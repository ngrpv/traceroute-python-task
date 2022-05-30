from flask import Flask, url_for, render_template, request
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/trace', methods=['GET'])
def search():
    args = request.args
    return str(args['domain'])
