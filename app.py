from flask import Flask, request, jsonify
from worker import execute_script_task
import os
import json

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    script_name = request.json.get('script_name')
    
    # Queue the task using Celery
    task = execute_script_task.delay(script_name)
    
    return jsonify({"task_id": task.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    result_file = os.path.join('/app/celery-results', f'celery-task-meta-{task_id}')
    
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            result_data = json.load(f)
            task_status = result_data['status']
            task_result = result_data.get('result', 'No result available')

        return jsonify({
            "task_id": task_id,
            "task_status": task_status,
            "task_result": task_result
        })
    else:
        return jsonify({"error": "Task ID not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
