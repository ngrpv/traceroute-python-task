import json
import random
import socket
import threading

from flask import Flask, render_template, request

from trace import Tracer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


is_finished = {}
trace_result = {}


def start_tracing(tracer: Tracer, id: int):
    trace_result[id] = []
    is_finished[id] = False
    for i in tracer.start():
        trace_result[id].append(i)
    is_finished[id] = True


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


class Result:
    def __init__(self, data, is_finished):
        self.data = data
        self.is_finished = is_finished


@app.route('/get-state/<int:id>')
def get_state(id: int):
    while id not in trace_result or len(trace_result[id]) == 0:
        pass
    result = Result(trace_result[id][:], is_finished[id])
    trace_result[id] = []
    return json.dumps(result, default=lambda x: x.__dict__)
