from flask import Flask, jsonify
from worker import execute_script_task
import os
import json
import time

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    # Record the request timestamp
    start_time = time.time()

    # Capture the pod ID where the task is received
    received_by = os.getenv('HOSTNAME', 'unknown_pod')
    
    # Queue the task using Celery
    task = execute_script_task.delay(start_time, received_by)
    
    return jsonify({"task_id": task.id, "received_by": received_by}), 202


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    result_file = os.path.join('/app/celery-results', f'celery-task-meta-{task_id}')
    
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            return json.load(f)
    else:
        return jsonify({"task_id": task_id, "task_status": "PENDING"}), 202

@app.route('/all-celery-results', methods=['GET'])
def all_celery_results():
    all_results = []
    
    for result_file in os.listdir('/app/celery-results'):
        result_path = os.path.join('/app/celery-results', result_file)
        if os.path.isfile(result_path):
            with open(result_path, 'r') as f:
                result_data = json.load(f)
                all_results.append(result_data)
    
    if not all_results:
        return jsonify({"message": "No tasks have been executed yet."}), 404
    
    return jsonify({"results": all_results}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
