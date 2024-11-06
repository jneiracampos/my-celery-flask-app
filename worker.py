from celery import Celery
from scripts.memory_cpu_intensive import memory_cpu_intensive
import os
import time
import json
import logging

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

# Logger
logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=10)
def execute_script_task(self, start_time, received_by):
    executed_by = os.getenv('HOSTNAME', 'unknown_pod')
    retry_count = self.request.retries
    task_id = self.request.id

    try:
        result = memory_cpu_intensive()

        end_time = time.time()
        execution_time = end_time - start_time

        # Log success
        result_file = os.path.join('/app/celery-results', f'celery-task-meta-{self.request.id}')
        with open(result_file, 'w') as f:
            json.dump({
                'task_id': task_id,
                'status': 'SUCCESS',
                'result': result,
                'execution_time': execution_time,
                'received_by': received_by,
                'executed_by': executed_by,
                'retry_count': retry_count
            }, f)
        
        return result

    except Exception as e:
        logger.exception(f"Error executing task {task_id} - Retry count: {retry_count}")

        # Retry the task if it's a recoverable error
        raise self.retry(exc=e)
    
