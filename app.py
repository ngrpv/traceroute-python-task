from flask import Flask, url_for, render_template, request
from markupsafe import escape
import socket
from trace import Tracer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/trace', methods=['GET'])
def search():
    args = request.args
    try:
        dest = socket.gethostbyname(args['domain'])
    except socket.error:
        return f"Can't resolve ip address for \"{args['domain']}\". Check internet connection"
    tracer = Tracer(int(args['max-ttl']), dest, 34434, int(args['timeout']))
    result = ''
    for i in tracer.start():
        result += f'<div>{i}</div>'
    return result
