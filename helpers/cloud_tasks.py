import datetime
import json
import logging
import os

import google.cloud.tasks_v2
from google.cloud.tasks_v2 import CloudTasksClient
from google.cloud import tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2

TASK_PROJECT_ID = os.getenv('PROJECT_ID', 'blossom-419321')
TASK_LOCATION = os.getenv('TASK_LOCATION', 'us-central1')
TASK_QUEUE = os.getenv('TASK_QUEUE', 'automations-queue')
SERVICE_URL = os.getenv('SERVICE_URL', 'https://4d25-200-162-235-42.ngrok-free.app')


client = CloudTasksClient()
parent = client.queue_path(TASK_PROJECT_ID, TASK_LOCATION, TASK_QUEUE)

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

def add_task(
    task: google.cloud.tasks_v2.types.Task,
    seconds_from_now: int | None = None,
    deadline_in_seconds: int | None = None
):
    if seconds_from_now is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(
            datetime.datetime.utcnow()
            + datetime.timedelta(seconds=seconds_from_now)
        )
        task.schedule_time = timestamp

        # Convert "deadline in seconds" to a Protobuf Duration
    if deadline_in_seconds is not None:
        duration = duration_pb2.Duration()
        duration.FromSeconds(deadline_in_seconds)
        task.dispatch_deadline = duration

    response = client.create_task(parent=parent, task=task)
    eta = response.schedule_time.strftime("%m/%d/%Y, %H:%M:%S")

    logger.info(f"[CLOUD TASKS][ADD TASK][TASK {response.name}] Task enqueued, ETA {eta}.")


def bot_start_processing_run(thread_id: str, run_id: str):
    task = tasks_v2.Task({
        "http_request": {
            "url": f"{SERVICE_URL}/background",
            "http_method": tasks_v2.HttpMethod.POST,
            "headers": {"Content-type": "application/json"},
            "body": json.dumps({"thread_id": thread_id, "run_id": run_id}).encode()
        }
    })

    add_task(task)
