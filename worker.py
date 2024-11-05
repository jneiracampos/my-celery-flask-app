from celery import Celery
import subprocess
import os
import time
import json

app = Celery('worker', broker='sqs://', backend='file:///app/celery-results')

app.conf.update(
    broker_transport_options={
        'region': 'us-east-2',
        'predefined_queues': {
            'MyQueue': {
                'url': 'https://sqs.us-east-2.amazonaws.com/203918887857/MyQueue'
            }
        }
    },
    task_default_queue='MyQueue',
    broker_connection_retry_on_startup=True,
    task_acks_late=True,  # Ensure the task is acknowledged only after successful completion
    worker_prefetch_multiplier=1,  # Fetch one task at a time
)


@app.task
def execute_script_task(script_name, start_time):
    script_path = os.path.join('/app/scripts', script_name)

    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time

        # Save the result and execution time to a file in the shared directory
        result_file = os.path.join('/app/celery-results', f'celery-task-meta-{execute_script_task.request.id}')
        with open(result_file, 'w') as f:
            json.dump({
                'status': 'SUCCESS',
                'result': result.stdout,
                'execution_time': execution_time
            }, f)
        
        return result.stdout

    except Exception as e:
        return f"Error occurred: {str(e)}"
