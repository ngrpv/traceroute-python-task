import json
import random
import socket
import threading
from trace import Tracer

from flask import Flask, Response, render_template, request, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


trace_result = {}


def start_tracing(tracer: Tracer, id: int):
    trace_result[id] = []
    for i in tracer.start():
        trace_result[id].append(i)
        print(len(trace_result[id]))


@app.route('/trace', methods=['GET'])
def search():
    args = request.args
    try:
        dest = socket.gethostbyname(args['domain'])
    except socket.error:
        return f"Can't resolve ip address for \"{args['domain']}\". Check internet connection"
    id = random.randint(0, 1000000)
    tracer = Tracer(int(args['max-ttl']), dest, 34434, int(args['timeout']))
    threading.Thread(target=start_tracing, args=[tracer, id]).start()
    return str(id)


@app.route('/get-state/<int:id>')
def get_state(id: int):
    while id not in trace_result or len(trace_result[id]) == 0:
        pass
    return json.dumps(trace_result[id].pop(0), default=lambda x: x.__dict__)
