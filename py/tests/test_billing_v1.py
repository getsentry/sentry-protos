from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from sentry_protos.billing.v1.data_category_pb2 import DataCategory
from sentry_protos.billing.v1.endpoint_usage_pb2 import (
    CategoryUsage,
    DailyUsage,
    GetUsageRequest,
    GetUsageResponse,
    UsageData,
)


now = datetime.now()


def test_usage_data():
    UsageData(
        total=1000,
        accepted=800,
        dropped=100,
        filtered=50,
        over_quota=30,
        smart_limit=10,
        dynamic_sampling=10,
    )


def test_get_usage_request():
    start = Timestamp(seconds=int(now.timestamp()))
    end = Timestamp(seconds=int(now.timestamp()) + 86400)
    GetUsageRequest(
        organization_id=1,
        start=start,
        end=end,
    )


def test_category_usage():
    CategoryUsage(
        category=DataCategory.DATA_CATEGORY_ERROR,
        data=UsageData(
            total=500,
            accepted=400,
            dropped=50,
            filtered=30,
            over_quota=10,
            smart_limit=5,
            dynamic_sampling=5,
        ),
    )


def test_get_usage_response():
    day = Timestamp(seconds=int(now.timestamp()))
    GetUsageResponse(
        days=[
            DailyUsage(
                date=day,
                usage=[
                    CategoryUsage(
                        category=DataCategory.DATA_CATEGORY_ERROR,
                        data=UsageData(
                            total=500,
                            accepted=400,
                            dropped=50,
                            filtered=30,
                            over_quota=10,
                            smart_limit=5,
                            dynamic_sampling=5,
                        ),
                    ),
                    CategoryUsage(
                        category=DataCategory.DATA_CATEGORY_TRANSACTION,
                        data=UsageData(
                            total=2000,
                            accepted=1800,
                            dropped=100,
                            filtered=50,
                            over_quota=30,
                            smart_limit=10,
                            dynamic_sampling=10,
                        ),
                    ),
                ],
            ),
        ],
    )
