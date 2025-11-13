# Querying EAP

This folder contains the interface definitions for querying of the events analytics platform.


# Terminology

**Trace -** A collection of events that are triggered by a customer operation. Examples: A web request, an event going through a pipeline or all of those things grouped together (e.g. a web request triggers asynchronous processes which are still tied to the trace)

**TraceItem -** A queryable structured attribute of a trace. Everything that is queryable through EAP is a **TraceItem or a trace.** TraceItems are related to each other via traces.
**TraceItemAttribute -** An attribute on a traceitem that can be selected, aggregated (if it is numeric) or used to filter

**Virtual Column -** Column that is not stored on the storage of the TraceItem but rather passed in at query time.

Example:

    `project_id` is stored with the trace_item
    `project_name` is not
    `project_id` to name mapping is passed with the query so that project_name can be a virtual column


# Is this Protobuf definition a re-implementation of [SnQL](https://getsentry.github.io/snuba/language/snql.html)?

No, EAP-RPC differs from SnQL in key ways:

1. EAP-RPC does not distinguish between data stored as a column or a tag, TraceItems have attributes and the interface to query them is all the same.
    1. Note: attributes sent by sentry are prefixed with `sentry.{attr_name}` to allow users to send custom tags with the same name.
2. EAP-RPC aims to support homogenously structured query requests and responses rather than pass through SQL from a caller/data blobs from ClickHouse. Currently supported request types:
-    1. A timeseries request (with a predefined list of possible aggregations)
-    2. A request for attribute values (e.g. populating a table view)
-    3. A request for the list of all searchable attributes (e.g. tag autocompletion)
-    4. A request for possible attribute values (e.g. tag value autocompletion)
-    5. A request to delete stored items by trace_id or attribute (for PII)

3. EAP-RPC queries can be serviced by datastores other than clickhouse as long as they conform to the interfaces outlined in this repo. At time of writing (11-13-2025) no other datastores are being used but this is designed to allow us to transition from traditional ClickHouse.



# Conventions

* All endpoint definitions are prefixed with `endpoint_`
* All request payload are suffixed with `Request`
* All response payloads are suffixed with `Response`
* All requests must take a `RequestMeta` object


