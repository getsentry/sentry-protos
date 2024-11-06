from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from sentry_protos.sentry.v1.taskworker_pb2 import (
    TaskActivation,
    RetryState
)

now = datetime.now()


def test_task_activation():
    TaskActivation(
        id="abc123",
        namespace="integrations",
        taskname="sentry.integrations.tasks.fetch_commits",
        parameters='{"args": [1]}',
        received_at=Timestamp(seconds=int(now.timestamp())),
        retry_state=RetryState(
            attempts=5,
            kind="sentry.taskworker.retry.Retry",
            discard_after_attempt=5,
            deadletter_after_attempt=9
        ),
        processing_deadline_duration=5,
        expires=500
    )

