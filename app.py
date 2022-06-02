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
call_arguments = {}


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
        dest = socket.gethostbyname(args['target'])
    except socket.error:
        return f"Can't resolve ip address for \"{args['target']}\". Check internet connection", 400
    id = random.randint(0, 1000000)
    call_arguments[id] = {"target": args['target'], "max_ttl": args['max_ttl'], "timeout": args['timeout']}
    tracer = Tracer(int(args['max_ttl']), dest, 34434, int(args['timeout']))
    threading.Thread(target=start_tracing, args=[tracer, id]).start()
    return str(id)


class JobDetails:
    def __init__(self, nodes, is_finished, call_arguments):
        self.nodes = nodes
        self.is_finished = is_finished
        self.call_arguments = call_arguments


@app.route('/get-state/<int:id>')
def get_state(id: int):
    if id not in trace_result:
        return "Not found", 404
    result = JobDetails(trace_result[id], is_finished[id], call_arguments[id])
    return json.dumps(result, default=lambda x: x.__dict__)
