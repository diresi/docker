from flask import Flask, render_template, request, jsonify
import json
import tasks.tasks

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = json.loads(request.data.decode())
    try:
        node_id = int(data["node_id"])
    except:
        node_id = None
    task = tasks.tasks.list_children.delay(node_id)
    return task.task_id

@app.route("/results/<task_id>", methods=['GET'])
def get_results(task_id):
    task = tasks.tasks.list_children.AsyncResult(task_id)
    try:
        if task.ready():
            return jsonify(result=task.get())
        else:
            return "Nay!", 202
    except Exception as e:
        return repr(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
