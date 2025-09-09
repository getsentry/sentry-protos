from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.struct_pb2 import Struct
from sentry_protos.conduit.v1alpha.publish_pb2 import (
    PublishRequest,
    Phase,
)

now = datetime.now()
payload = Struct()
payload.update({"value": "test"})

def test_publish_request():
    PublishRequest(
        channel_id="abc123",
        message_id="def456",
        client_timestamp=Timestamp().FromDatetime(now),
        phase=Phase.PHASE_DELTA,
        sequence=0,
        payload=payload,
    )
