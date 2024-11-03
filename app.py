from flask import Flask, request, jsonify
from worker import execute_script_task
import os
import json
import time

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    script_name = request.json.get('script_name')

    # Record the request timestamp
    start_time = time.time()
    
    # Queue the task using Celery
    task = execute_script_task.delay(script_name, start_time)
    
    return jsonify({"task_id": task.id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    result_file = os.path.join('/app/celery-results', f'celery-task-meta-{task_id}')
    
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            result_data = json.load(f)
            task_status = result_data['status']
            task_result = result_data.get('result', 'No result available')
            execution_time = result_data.get('execution_time', 'N/A')

        return jsonify({
            "task_id": task_id,
            "task_status": task_status,
            "task_result": task_result,
            "execution_time": execution_time
        })
    else:
        return jsonify({"task_id": task_id, "task_status": "PENDING"}), 202


@app.route('/average-time', methods=['GET'])
def average_time():
    total_time = 0
    task_count = 0
    
    # Iterate over the results and calculate the average
    for result_file in os.listdir('/app/celery-results'):
        with open(os.path.join('/app/celery-results', result_file), 'r') as f:
            result_data = json.load(f)
            execution_time = result_data.get('execution_time')
            if execution_time:
                total_time += execution_time
                task_count += 1
    
    if task_count == 0:
        return jsonify({"average_time": "No tasks have been executed yet."})
    
    average_time = total_time / task_count
    return jsonify({"average_time": average_time})

@app.route('/longest-time', methods=['GET'])
def longest_time():
    longest_time = 0
    
    # Iterate over the results and calculate the longest time
    for result_file in os.listdir('/app/celery-results'):
        with open(os.path.join('/app/celery-results', result_file), 'r') as f:
            result_data = json.load(f)
            execution_time = result_data.get('execution_time')
            if execution_time and execution_time > longest_time:
                longest_time = execution_time
    
    if longest_time == 0:
        return jsonify({"longest_time": "No tasks have been executed yet."})
    
    return jsonify({"longest_time": longest_time})

@app.route('/all-execution-times', methods=['GET'])
def all_execution_times():
    execution_times = []
    
    # Gather all execution times from result files
    for result_file in os.listdir('/app/celery-results'):
        with open(os.path.join('/app/celery-results', result_file), 'r') as f:
            result_data = json.load(f)
            execution_time = result_data.get('execution_time')
            if execution_time is not None:
                execution_times.append(execution_time)
    
    if not execution_times:
        return jsonify({"execution_times": "No tasks have been executed yet."})
    
    return jsonify({"execution_times": execution_times})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
