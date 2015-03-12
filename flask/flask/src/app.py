from flask import Flask, render_template, request, jsonify
import json
import tasks.tasks

app = Flask(__name__)

def node_info_task(id):
    return tasks.tasks.node_info.delay(id)

@app.route('/api/node/<int:id>')
def api_node(id):
    data = node_info_task(id).wait()
    return jsonify(data)

@app.route('/app/node/<int:id>')
def app_node(id):
    task = node_info_task(id)
    return render_template('index.html', task_id=task.task_id)

@app.route('/')
@app.route('/app/')
@app.route('/app/view/')
@app.route('/app/view/node/')
@app.route('/app/view/node/<int:id>')
def index(id=None):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
