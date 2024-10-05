from celery import Celery
import subprocess
import os

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
    broker_connection_retry_on_startup=True
)

@app.task
def execute_script_task(script_name):
    script_path = os.path.join('/app/scripts', script_name)

    print(f"Executing: {script_path}")  # Debug print

    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        print(f"Script Output: {result.stdout}")  # Debug print
        return result.stdout
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print for errors
        return f"Error occurred: {str(e)}"

    