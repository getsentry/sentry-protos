import pytest

from sentry_protos.billing.v1.services.seer_feature_billing.v1.endpoint_check_seer_credits_pb2 import (
    CheckSeerCreditsRequest,
)
from sentry_protos.billing.v1.services.seer_feature_billing.v1.endpoint_get_seer_usage_pb2 import (
    GetSeerUsageRequest,
)


@pytest.mark.parametrize("attribution_id", [None, 0, -(1 << 40)])
def test_check_seer_credits_attribution_roundtrip(attribution_id):
    request = CheckSeerCreditsRequest(
        organization_id=7,
        feature_id="automations",
        predicted_credit_usage=100,
        take_lease=True,
    )
    if attribution_id is not None:
        request.attribution_id = attribution_id

    decoded = CheckSeerCreditsRequest.FromString(request.SerializeToString())

    assert decoded == request
    assert decoded.HasField("attribution_id") == (attribution_id is not None)


@pytest.mark.parametrize("attribution_id", [None, 0, -(1 << 40)])
def test_get_seer_usage_attribution_roundtrip(attribution_id):
    request = GetSeerUsageRequest(organization_id=7, feature_id="automations")
    if attribution_id is not None:
        request.attribution_id = attribution_id

    decoded = GetSeerUsageRequest.FromString(request.SerializeToString())

    assert decoded == request
    assert decoded.HasField("attribution_id") == (attribution_id is not None)
