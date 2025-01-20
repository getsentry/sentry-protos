from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from sentry_protos.sentry.v2.taskbroker_pb2 import (
    OnAttemptsExceeded,
    TaskActivation,
    RetryState,
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
            attempts_remaining=5,
            on_attempts_exceeded=(
                OnAttemptsExceeded.ON_ATTEMPTS_EXCEEDED_DISCARD
            )
        ),
        processing_deadline_duration=5,
        expires=500
    )
