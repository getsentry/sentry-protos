from google.protobuf.timestamp_pb2 import Timestamp

from sentry_protos.billing.v1.data_category_pb2 import DataCategory
from sentry_protos.billing.v1.endpoint_usage_pb2 import (
    CategoryUsage,
    DailyUsage,
    GetUsageRequest,
    GetUsageResponse,
    UsageData,
)


def test_usage_data():
    data = UsageData(
        total=1000,
        accepted=800,
        dropped=100,
        filtered=50,
        over_quota=30,
        smart_limit=10,
        dynamic_sampling=10,
    )
    assert data.total == 1000
    assert data.accepted == 800
    assert data.dropped == 100
    assert data.filtered == 50
    assert data.over_quota == 30
    assert data.smart_limit == 10
    assert data.dynamic_sampling == 10


def test_usage_data_defaults():
    data = UsageData()
    assert data.total == 0
    assert data.accepted == 0
    assert data.dropped == 0
    assert data.filtered == 0
    assert data.over_quota == 0
    assert data.smart_limit == 0
    assert data.dynamic_sampling == 0


def test_category_usage():
    data = UsageData(total=500, accepted=400, dropped=100)
    category_usage = CategoryUsage(
        category=DataCategory.DATA_CATEGORY_ERROR,
        data=data,
    )
    assert category_usage.category == DataCategory.DATA_CATEGORY_ERROR
    assert category_usage.data.total == 500
    assert category_usage.data.accepted == 400
    assert category_usage.data.dropped == 100


def test_daily_usage():
    day = Timestamp(seconds=1704067200)  # 2024-01-01T00:00:00Z
    error_usage = CategoryUsage(
        category=DataCategory.DATA_CATEGORY_ERROR,
        data=UsageData(total=1000, accepted=900, dropped=100),
    )
    span_usage = CategoryUsage(
        category=DataCategory.DATA_CATEGORY_SPAN,
        data=UsageData(total=5000, accepted=4500, filtered=500),
    )
    daily = DailyUsage(date=day, usage=[error_usage, span_usage])

    assert daily.date.seconds == 1704067200
    assert len(daily.usage) == 2
    assert daily.usage[0].category == DataCategory.DATA_CATEGORY_ERROR
    assert daily.usage[0].data.total == 1000
    assert daily.usage[1].category == DataCategory.DATA_CATEGORY_SPAN
    assert daily.usage[1].data.accepted == 4500


def test_get_usage_request():
    start = Timestamp(seconds=1704067200)
    end = Timestamp(seconds=1706745600)
    request = GetUsageRequest(
        organization_id=67890,
        start=start,
        end=end,
    )
    assert request.organization_id == 67890
    assert request.start.seconds == 1704067200
    assert request.end.seconds == 1706745600


def test_get_usage_request_has_field():
    request = GetUsageRequest(organization_id=1)
    assert not request.HasField("start")
    assert not request.HasField("end")

    request_with_times = GetUsageRequest(
        organization_id=1,
        start=Timestamp(seconds=100),
        end=Timestamp(seconds=200),
    )
    assert request_with_times.HasField("start")
    assert request_with_times.HasField("end")


def test_get_usage_response():
    day1 = DailyUsage(
        date=Timestamp(seconds=1704067200),
        usage=[
            CategoryUsage(
                category=DataCategory.DATA_CATEGORY_ERROR,
                data=UsageData(total=1000, accepted=900, dropped=50, filtered=50),
            ),
        ],
    )
    day2 = DailyUsage(
        date=Timestamp(seconds=1704153600),
        usage=[
            CategoryUsage(
                category=DataCategory.DATA_CATEGORY_ERROR,
                data=UsageData(total=1200, accepted=1100, dropped=100),
            ),
            CategoryUsage(
                category=DataCategory.DATA_CATEGORY_TRANSACTION,
                data=UsageData(total=3000, accepted=2800, over_quota=200),
            ),
        ],
    )
    response = GetUsageResponse(days=[day1, day2])

    assert len(response.days) == 2
    assert len(response.days[0].usage) == 1
    assert len(response.days[1].usage) == 2
    assert response.days[0].usage[0].data.total == 1000
    assert response.days[1].usage[1].category == DataCategory.DATA_CATEGORY_TRANSACTION
    assert response.days[1].usage[1].data.over_quota == 200


def test_get_usage_response_empty():
    response = GetUsageResponse()
    assert len(response.days) == 0


def test_get_usage_response_serialization_roundtrip():
    response = GetUsageResponse(
        days=[
            DailyUsage(
                date=Timestamp(seconds=1704067200),
                usage=[
                    CategoryUsage(
                        category=DataCategory.DATA_CATEGORY_SPAN,
                        data=UsageData(total=10000, accepted=9500, dynamic_sampling=500),
                    ),
                ],
            ),
        ],
    )
    serialized = response.SerializeToString()
    deserialized = GetUsageResponse()
    deserialized.ParseFromString(serialized)

    assert len(deserialized.days) == 1
    assert deserialized.days[0].date.seconds == 1704067200
    assert deserialized.days[0].usage[0].category == DataCategory.DATA_CATEGORY_SPAN
    assert deserialized.days[0].usage[0].data.total == 10000
    assert deserialized.days[0].usage[0].data.dynamic_sampling == 500
