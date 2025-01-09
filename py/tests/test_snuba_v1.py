from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from sentry_protos.snuba.v1.endpoint_time_series_pb2 import (
    DataPoint,
    TimeSeries,
    TimeSeriesRequest,
    TimeSeriesResponse,
)
from sentry_protos.snuba.v1.endpoint_trace_item_attributes_pb2 import (
    TraceItemAttributeNamesRequest,
    TraceItemAttributeNamesResponse,
    TraceItemAttributeValuesRequest,
    TraceItemAttributeValuesResponse,
)
from sentry_protos.snuba.v1.endpoint_trace_item_table_pb2 import (
    AggregationComparisonFilter,
    AggregationFilter,
    Column,
    TraceItemColumnValues,
    TraceItemTableRequest,
    TraceItemTableResponse,
)
from sentry_protos.snuba.v1.endpoint_find_traces_pb2 import (
    FindTracesRequest,
    FindTracesResponse,
    TraceResponse,
    TraceOrderBy,
)
from sentry_protos.snuba.v1.endpoint_create_subscription_pb2 import (
    CreateSubscriptionRequest,
    CreateSubscriptionResponse,
)
from sentry_protos.snuba.v1.endpoint_trace_item_table_subscription_pb2 import (
    CreateTraceItemTableSubscriptionRequest,
    CreateTraceItemTableSubscriptionResponse,
)
from sentry_protos.snuba.v1.request_common_pb2 import (
    RequestMeta,
    PageToken,
    TraceItemName,
)
from sentry_protos.snuba.v1.endpoint_find_traces_pb2 import (
    TraceFilter,
    EventFilter,
    AndTraceFilter,
    OrTraceFilter,
)

from sentry_protos.snuba.v1.trace_item_filter_pb2 import (
    TraceItemFilter,
    ComparisonFilter,
    ExistsFilter,
    AndFilter,
    OrFilter,
)
from sentry_protos.snuba.v1.trace_item_attribute_pb2 import (
    AttributeAggregation,
    AttributeKey,
    AttributeValue,
    ExtrapolationMode,
    Function,
)


COMMON_META = RequestMeta(
    project_ids=[1, 2, 3],
    organization_id=1,
    cogs_category="something",
    referrer="something",
    start_timestamp=Timestamp(seconds=int(datetime(2024, 4, 20, 16, 20).timestamp())),
    end_timestamp=Timestamp(seconds=int(datetime(2024, 4, 20, 17, 20).timestamp())),
    trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_SPANS,
)


def test_example_time_series():
    TimeSeriesRequest(
        meta=COMMON_META,
        aggregations=[
            AttributeAggregation(
                aggregate=Function.FUNCTION_AVG,
                key=AttributeKey(type=AttributeKey.TYPE_FLOAT, name="sentry.duration"),
                label="p50",
            ),
            AttributeAggregation(
                aggregate=Function.FUNCTION_P95,
                key=AttributeKey(type=AttributeKey.TYPE_FLOAT, name="sentry.duration"),
                label="p90",
            ),
        ],
        granularity_secs=60,
        group_by=[
            AttributeKey(type=AttributeKey.TYPE_STRING, name="endpoint_name"),
            AttributeKey(type=AttributeKey.TYPE_STRING, name="consumer_group"),
        ],
    )

    TimeSeriesResponse(
        result_timeseries=[
            TimeSeries(
                label="p50",
                group_by_attributes={
                    "endpoint_name": "/v1/rpc",
                    "consumer_group": "snuba_outcomes_consumer",
                },
                buckets=[COMMON_META.start_timestamp for _ in range(60)],
                data_points=[DataPoint(data=42) for _ in range(60)],
                num_events=1337,
                avg_sampling_rate=0.1,
            ),
            TimeSeries(
                label="p50",
                group_by_attributes={
                    "endpoint_name": "/v2/rpc",
                    "consumer_group": "snuba_outcomes_consumer",
                },
                buckets=[COMMON_META.start_timestamp for _ in range(60)],
                data_points=[DataPoint(data=42) for _ in range(60)],
                num_events=1337,
                avg_sampling_rate=0.1,
            ),
            TimeSeries(
                label="p90",
                group_by_attributes={
                    "endpoint_name": "/v1/rpc",
                    "consumer_group": "snuba_outcomes_consumer",
                },
                buckets=[COMMON_META.start_timestamp for _ in range(60)],
                data_points=[DataPoint(data=42) for _ in range(60)],
                num_events=1337,
                avg_sampling_rate=0.1,
            ),
            TimeSeries(
                label="p90",
                group_by_attributes={
                    "endpoint_name": "/v2/rpc",
                    "consumer_group": "snuba_outcomes_consumer",
                },
                buckets=[COMMON_META.start_timestamp for _ in range(60)],
                data_points=[DataPoint(data=42) for _ in range(60)],
                num_events=1337,
                avg_sampling_rate=0.1,
            ),
        ]
    )


def test_example_table() -> None:
    TraceItemTableRequest(
        meta=COMMON_META,
        columns=[
            Column(
                key=AttributeKey(
                    type=AttributeKey.TYPE_STRING, name="sentry.span_name"
                ),
                label="span_name",
            ),
            Column(
                key=AttributeKey(type=AttributeKey.TYPE_FLOAT, name="sentry.duration"),
                label="duration",
            ),
        ],
        filter=TraceItemFilter(
            or_filter=OrFilter(
                filters=[
                    TraceItemFilter(
                        comparison_filter=ComparisonFilter(
                            key=AttributeKey(
                                type=AttributeKey.TYPE_STRING,
                                name="eap.measurement",
                            ),
                            op=ComparisonFilter.OP_LESS_THAN_OR_EQUALS,
                            value=AttributeValue(val_float=101),
                        ),
                    ),
                    TraceItemFilter(
                        comparison_filter=ComparisonFilter(
                            key=AttributeKey(
                                type=AttributeKey.TYPE_STRING,
                                name="eap.measurement",
                            ),
                            op=ComparisonFilter.OP_GREATER_THAN,
                            value=AttributeValue(val_float=999),
                        ),
                    ),
                ]
            )
        ),
        order_by=[
            TraceItemTableRequest.OrderBy(
                column=Column(
                    key=AttributeKey(
                        type=AttributeKey.TYPE_FLOAT, name="sentry.duration"
                    )
                )
            )
        ],
        limit=100,
    )

    TraceItemTableResponse(
        column_values=[
            TraceItemColumnValues(
                attribute_name="span_name",
                results=[AttributeValue(val_str="xyz"), AttributeValue(val_str="abc")],
            ),
            TraceItemColumnValues(
                attribute_name="duration",
                results=[AttributeValue(val_float=4.2), AttributeValue(val_float=6.9)],
            ),
        ],
        page_token=PageToken(
            filter_offset=TraceItemFilter(
                comparison_filter=ComparisonFilter(
                    key=AttributeKey(
                        type=AttributeKey.TYPE_FLOAT, name="sentry.duration"
                    ),
                    op=ComparisonFilter.OP_GREATER_THAN_OR_EQUALS,
                    value=AttributeValue(val_float=6.9),
                )
            )
        ),
    )


def test_example_table_with_aggregations() -> None:
    TraceItemTableRequest(
        meta=COMMON_META,
        columns=[
            Column(
                key=AttributeKey(
                    type=AttributeKey.TYPE_STRING, name="sentry.span_name"
                ),
                label="span_name",
            ),
            Column(
                aggregation=AttributeAggregation(
                    aggregate=Function.FUNCTION_P95,
                    key=AttributeKey(
                        type=AttributeKey.TYPE_FLOAT, name="sentry.duration"
                    ),
                ),
                label="duration_p95",
            ),
        ],
        filter=TraceItemFilter(
            or_filter=OrFilter(
                filters=[
                    TraceItemFilter(
                        comparison_filter=ComparisonFilter(
                            key=AttributeKey(
                                type=AttributeKey.TYPE_STRING,
                                name="eap.measurement",
                            ),
                            op=ComparisonFilter.OP_LESS_THAN_OR_EQUALS,
                            value=AttributeValue(val_float=101),
                        ),
                    ),
                    TraceItemFilter(
                        comparison_filter=ComparisonFilter(
                            key=AttributeKey(
                                type=AttributeKey.TYPE_STRING,
                                name="eap.measurement",
                            ),
                            op=ComparisonFilter.OP_GREATER_THAN,
                            value=AttributeValue(val_float=999),
                        ),
                    ),
                ]
            )
        ),
        order_by=[TraceItemTableRequest.OrderBy(column=Column(label="duration_p95"))],
        limit=2,
    )

    TraceItemTableResponse(
        column_values=[
            TraceItemColumnValues(
                attribute_name="span_name",
                results=[AttributeValue(val_str="xyz"), AttributeValue(val_str="abc")],
            ),
            TraceItemColumnValues(
                attribute_name="duration_p95",
                results=[AttributeValue(val_float=4.2), AttributeValue(val_float=6.9)],
            ),
        ],
        page_token=PageToken(
            offset=2
        ),  # if we're ordering by aggregate values, we can't paginate by anything except offset
    )

def test_example_table_with_aggregation_filter() -> None:
    TraceItemTableRequest(
        meta=COMMON_META,
        columns=[
            Column(
                key=AttributeKey(
                    type=AttributeKey.TYPE_STRING, name="sentry.browser.name"
                ),
                label="browser_name",
            ),
            Column(
                aggregation=AttributeAggregation(
                    aggregate=Function.FUNCTION_AVG,
                    key=AttributeKey(
                        type=AttributeKey.TYPE_FLOAT, name="sentry.duration"
                    ),
                    extrapolation_mode=ExtrapolationMode.EXTRAPOLATION_MODE_NONE,
                ),
                label="duration_avg",
            ),
        ],
        order_by=[TraceItemTableRequest.OrderBy(column=Column(label="duration_avg"))],
        aggregation_filter=AggregationFilter(
            comparison_filter=AggregationComparisonFilter(
                column=Column(
                    aggregation=AttributeAggregation(
                        aggregate=Function.FUNCTION_COUNT,
                        key=AttributeKey(
                            type=AttributeKey.TYPE_FLOAT, name="sentry.duration"
                        ),
                        extrapolation_mode=ExtrapolationMode.EXTRAPOLATION_MODE_SAMPLE_WEIGHTED,
                    ),
                ),
                op=AggregationComparisonFilter.OP_GREATER_THAN,
                value=AttributeValue(val_float=100),
            ),
        ),
        limit=2,
    )

    TraceItemTableResponse(
        column_values=[
            TraceItemColumnValues(
                attribute_name="browser_name",
                results=[AttributeValue(val_str="xyz"), AttributeValue(val_str="abc")],
            ),
            TraceItemColumnValues(
                attribute_name="duration_avg",
                results=[AttributeValue(val_float=4.2), AttributeValue(val_float=6.9)],
            ),
        ],
        page_token=PageToken(
            offset=2
        ), 
    )

def test_example_find_traces() -> None:
    # Find traces that contain a span event with a `span_name` of "database_query"
    FindTracesRequest(
        meta=COMMON_META,
        filter=TraceFilter(
            event_filter=EventFilter(
                trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_SPANS,
                filter=TraceItemFilter(
                    comparison_filter=ComparisonFilter(
                        key=AttributeKey(
                            type=AttributeKey.TYPE_STRING,
                            name="sentry.span_name",
                        ),
                        op=ComparisonFilter.OP_EQUALS,
                        value=AttributeValue(val_str="database_query"),
                    ),
                ),
            ),
        ),
        order_by=TraceOrderBy.TRACE_ORDER_BY_END_TIME,
    )

    # Find traces with a single span event with a `span_name` of "database_query"
    # and a `transaction_name` of "GET /v1/rpc"
    FindTracesRequest(
        meta=COMMON_META,
        filter=TraceFilter(
            event_filter=EventFilter(
                trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_SPANS,
                filter=TraceItemFilter(
                    and_filter=AndFilter(
                        filters=[
                            TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="sentry.span_name",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="database_query"),
                                ),
                            ),
                            TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="sentry.transaction_name",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="GET /v1/rpc"),
                                ),
                            )
                        ]
                    ),
                ),
            ),
        ),
        order_by=TraceOrderBy.TRACE_ORDER_BY_TRACE_DURATION,
    )

    # Find traces that contain two events: a span with a `span_name` of
    # "database_query" and an error with a `group_id` of "1123"
    FindTracesRequest(
        meta=COMMON_META,
        filter=TraceFilter(
            and_filter=AndTraceFilter(
                filters=[
                    TraceFilter(
                        event_filter=EventFilter(
                            trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_SPANS,
                            filter=TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="sentry.span_name",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="database_query"),
                                ),
                            ),
                        ),
                    ),
                    TraceFilter(
                        event_filter=EventFilter(
                            trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_ERRORS,
                            filter=TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="group_id",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="1123"),
                                ),
                            ),
                        ),
                    ),
                ],
            ),
        ),
    )

    # Find traces that contain at least one of: a span with a `span_name` of
    # "database_query" and an error with a `group_id` of "1123"
    FindTracesRequest(
        meta=COMMON_META,
        filter=TraceFilter(
            or_filter=OrTraceFilter(
                filters=[
                    TraceFilter(
                        event_filter=EventFilter(
                            trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_SPANS,
                            filter=TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="sentry.span_name",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="database_query"),
                                ),
                            ),
                        ),
                    ),
                    TraceFilter(
                        event_filter=EventFilter(
                            trace_item_name=TraceItemName.TRACE_ITEM_NAME_EAP_ERRORS,
                            filter=TraceItemFilter(
                                comparison_filter=ComparisonFilter(
                                    key=AttributeKey(
                                        type=AttributeKey.TYPE_STRING,
                                        name="group_id",
                                    ),
                                    op=ComparisonFilter.OP_EQUALS,
                                    value=AttributeValue(val_str="1123"),
                                ),
                            ),
                        ),
                    ),
                ],
            ),
        ),
    )

    FindTracesResponse(
        traces=[
            TraceResponse(
                trace_id="1234567890abcdef",
                start_timestamp=Timestamp(
                    seconds=int(datetime(2024, 4, 20, 16, 20).timestamp())
                ),
                end_timestamp=Timestamp(
                    seconds=int(datetime(2024, 4, 20, 17, 20).timestamp())
                ),
            ),
            TraceResponse(
                trace_id="fedcba0987654321",
                start_timestamp=Timestamp(
                    seconds=int(datetime(2024, 4, 20, 16, 20).timestamp())
                ),
                end_timestamp=Timestamp(
                    seconds=int(datetime(2024, 4, 20, 17, 20).timestamp())
                ),
            ),
        ],
    )

def test_example_create_trace_item_table_subscription() -> None:
    CreateTraceItemTableSubscriptionRequest(
        table_request=TraceItemTableRequest(
            meta=COMMON_META,
            columns=[
                Column(
                    aggregation=AttributeAggregation(
                        aggregate=Function.FUNCTION_COUNT,
                        key=AttributeKey(
                            type=AttributeKey.TYPE_INT, name="span.duration"
                        ),
                    ),
                ),
            ],
            filter=TraceItemFilter(
                comparison_filter=ComparisonFilter(
                    key=AttributeKey(
                        type=AttributeKey.TYPE_STRING,
                        name="span.op",
                    ),
                    op=ComparisonFilter.OP_EQUALS,
                    value=AttributeValue(val_str="http.client"),
                ),
            ),
        ),
        project_id=1,
        time_window=3600,
        resolution=180,
    )

    CreateTraceItemTableSubscriptionResponse(
        subscription_id="123",
    )

def test_example_create_subscription() -> None:
    CreateSubscriptionRequest(
        time_series_request=TimeSeriesRequest(
            meta=COMMON_META,
            aggregations=[
                AttributeAggregation(
                    aggregate=Function.FUNCTION_COUNT,
                    key=AttributeKey(type=AttributeKey.TYPE_INT, name="span.duration"),
                ),
            ],
            filter=TraceItemFilter(
                comparison_filter=ComparisonFilter(
                    key=AttributeKey(
                        type=AttributeKey.TYPE_STRING,
                        name="span.op",
                    ),
                    op=ComparisonFilter.OP_EQUALS,
                    value=AttributeValue(val_str="http.client"),
                ),
            ),
            granularity_secs=3600,
        ),
        time_window_secs=3600,
        resolution_secs=180,
    )

    CreateSubscriptionResponse(
        subscription_id="123",
    )
