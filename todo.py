from flask import Flask, jsonify, request
from pymongo import MongoClient
import csv

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
tasks = db.tasks


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    all_tasks = list(tasks.find({}))
    return jsonify(all_tasks)


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.find_one({'_id': task_id})
    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.get_json()
    tasks.insert_one(task)
    return "Task added successfully"


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = request.get_json()
    tasks.update_one({'_id': task_id}, {'$set': task})
    return "Task updated successfully"


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks.delete_one({'_id': task_id})
    return "Task deleted successfully"


@app.route("/tasks", methods=["GET"])
def get_tasks_with_pagination():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    tasks = list(db.tasks.find().skip((page - 1) * limit).limit(limit))
    return jsonify(tasks)


@app.route("/tasks/export", methods=["GET"])
def export_tasks_to_csv():
    task_list = list(tasks.find({}))
    csv_file = "tasks.csv"
    with open(csv_file, 'w') as file:
        writer = csv.DictWriter(
            file, fieldnames=["task", "is_completed", "end_date"])
        writer.writeheader()
        for task in task_list:
            writer.writerow(task)
    return "Tasks exported successfully to csv"


if __name__ == '__main__':
    app.run()
