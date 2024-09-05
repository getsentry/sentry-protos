// This file is @generated by prost-build.
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct RequestMeta {
    #[prost(uint64, tag = "1")]
    pub organization_id: u64,
    #[prost(string, tag = "2")]
    pub cogs_category: ::prost::alloc::string::String,
    #[prost(string, tag = "3")]
    pub referrer: ::prost::alloc::string::String,
    /// can be empty
    #[prost(uint64, repeated, tag = "4")]
    pub project_ids: ::prost::alloc::vec::Vec<u64>,
    #[prost(message, optional, tag = "5")]
    pub start_timestamp: ::core::option::Option<::prost_types::Timestamp>,
    #[prost(message, optional, tag = "6")]
    pub end_timestamp: ::core::option::Option<::prost_types::Timestamp>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttributeKey {
    #[prost(enumeration = "attribute_key::Type", tag = "1")]
    pub r#type: i32,
    /// if you use span_id this will route to span.span_id,
    /// if you use derp this will route to attr_{str,num}_{n}\['derp'\]
    #[prost(string, tag = "2")]
    pub name: ::prost::alloc::string::String,
}
/// Nested message and enum types in `AttributeKey`.
pub mod attribute_key {
    /// this mostly reflects what types are able to be ingested, see eap_spans consumer for ingest details
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum Type {
        /// called "none" sometimes
        Unspecified = 0,
        Boolean = 1,
        String = 2,
        Float = 3,
        /// note: all numbers are stored as float64, so massive integers can be rounded. USE STRING FOR IDS.
        Int = 4,
    }
    impl Type {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                Type::Unspecified => "TYPE_UNSPECIFIED",
                Type::Boolean => "TYPE_BOOLEAN",
                Type::String => "TYPE_STRING",
                Type::Float => "TYPE_FLOAT",
                Type::Int => "TYPE_INT",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "TYPE_UNSPECIFIED" => Some(Self::Unspecified),
                "TYPE_BOOLEAN" => Some(Self::Boolean),
                "TYPE_STRING" => Some(Self::String),
                "TYPE_FLOAT" => Some(Self::Float),
                "TYPE_INT" => Some(Self::Int),
                _ => None,
            }
        }
    }
}
/// Special cases for attributes, in particular things like project name
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttributeKeyTransformContext {
    #[prost(map = "uint64, string", tag = "1")]
    pub project_ids_to_names: ::std::collections::HashMap<
        u64,
        ::prost::alloc::string::String,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AttributeValue {
    #[prost(oneof = "attribute_value::Value", tags = "1, 2, 3, 4")]
    pub value: ::core::option::Option<attribute_value::Value>,
}
/// Nested message and enum types in `AttributeValue`.
pub mod attribute_value {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Value {
        #[prost(bool, tag = "1")]
        ValBool(bool),
        #[prost(string, tag = "2")]
        ValStr(::prost::alloc::string::String),
        #[prost(float, tag = "3")]
        ValFloat(f32),
        #[prost(int64, tag = "4")]
        ValInt(i64),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AndFilter {
    #[prost(message, repeated, tag = "1")]
    pub filters: ::prost::alloc::vec::Vec<TraceItemFilter>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct OrFilter {
    #[prost(message, repeated, tag = "1")]
    pub filters: ::prost::alloc::vec::Vec<TraceItemFilter>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ComparisonFilter {
    #[prost(message, optional, tag = "1")]
    pub key: ::core::option::Option<AttributeKey>,
    #[prost(enumeration = "comparison_filter::Op", tag = "2")]
    pub op: i32,
    #[prost(message, optional, tag = "3")]
    pub value: ::core::option::Option<AttributeValue>,
}
/// Nested message and enum types in `ComparisonFilter`.
pub mod comparison_filter {
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum Op {
        Unspecified = 0,
        LessThan = 1,
        GreaterThan = 2,
        LessThanOrEquals = 3,
        GreaterThanOrEquals = 4,
        Equals = 5,
        NotEquals = 6,
        /// string only
        Like = 7,
        /// string only
        NotLike = 8,
    }
    impl Op {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                Op::Unspecified => "OP_UNSPECIFIED",
                Op::LessThan => "OP_LESS_THAN",
                Op::GreaterThan => "OP_GREATER_THAN",
                Op::LessThanOrEquals => "OP_LESS_THAN_OR_EQUALS",
                Op::GreaterThanOrEquals => "OP_GREATER_THAN_OR_EQUALS",
                Op::Equals => "OP_EQUALS",
                Op::NotEquals => "OP_NOT_EQUALS",
                Op::Like => "OP_LIKE",
                Op::NotLike => "OP_NOT_LIKE",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "OP_UNSPECIFIED" => Some(Self::Unspecified),
                "OP_LESS_THAN" => Some(Self::LessThan),
                "OP_GREATER_THAN" => Some(Self::GreaterThan),
                "OP_LESS_THAN_OR_EQUALS" => Some(Self::LessThanOrEquals),
                "OP_GREATER_THAN_OR_EQUALS" => Some(Self::GreaterThanOrEquals),
                "OP_EQUALS" => Some(Self::Equals),
                "OP_NOT_EQUALS" => Some(Self::NotEquals),
                "OP_LIKE" => Some(Self::Like),
                "OP_NOT_LIKE" => Some(Self::NotLike),
                _ => None,
            }
        }
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct ExistsFilter {
    #[prost(message, optional, tag = "1")]
    pub key: ::core::option::Option<AttributeKey>,
}
/// Represents a condition on searching for a particular "trace item"
/// (e.g., spans, replays, errors)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TraceItemFilter {
    #[prost(oneof = "trace_item_filter::Value", tags = "1, 2, 3, 4")]
    pub value: ::core::option::Option<trace_item_filter::Value>,
}
/// Nested message and enum types in `TraceItemFilter`.
pub mod trace_item_filter {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Value {
        #[prost(message, tag = "1")]
        AndFilter(super::AndFilter),
        #[prost(message, tag = "2")]
        OrFilter(super::OrFilter),
        #[prost(message, tag = "3")]
        ComparisonFilter(super::ComparisonFilter),
        #[prost(message, tag = "4")]
        ExistsFilter(super::ExistsFilter),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AggregateBucketRequest {
    #[prost(message, optional, tag = "1")]
    pub meta: ::core::option::Option<RequestMeta>,
    #[prost(enumeration = "aggregate_bucket_request::Function", tag = "4")]
    pub aggregate: i32,
    #[prost(message, optional, tag = "5")]
    pub filter: ::core::option::Option<TraceItemFilter>,
    #[prost(uint64, tag = "6")]
    pub granularity_secs: u64,
    #[prost(message, optional, tag = "7")]
    pub key: ::core::option::Option<AttributeKey>,
    #[prost(message, optional, tag = "8")]
    pub attribute_key_transform_context: ::core::option::Option<
        AttributeKeyTransformContext,
    >,
}
/// Nested message and enum types in `AggregateBucketRequest`.
pub mod aggregate_bucket_request {
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum Function {
        Unspecified = 0,
        Sum = 1,
        Average = 2,
        Count = 3,
        P50 = 4,
        P95 = 5,
        P99 = 6,
        Avg = 7,
    }
    impl Function {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                Function::Unspecified => "FUNCTION_UNSPECIFIED",
                Function::Sum => "FUNCTION_SUM",
                Function::Average => "FUNCTION_AVERAGE",
                Function::Count => "FUNCTION_COUNT",
                Function::P50 => "FUNCTION_P50",
                Function::P95 => "FUNCTION_P95",
                Function::P99 => "FUNCTION_P99",
                Function::Avg => "FUNCTION_AVG",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "FUNCTION_UNSPECIFIED" => Some(Self::Unspecified),
                "FUNCTION_SUM" => Some(Self::Sum),
                "FUNCTION_AVERAGE" => Some(Self::Average),
                "FUNCTION_COUNT" => Some(Self::Count),
                "FUNCTION_P50" => Some(Self::P50),
                "FUNCTION_P95" => Some(Self::P95),
                "FUNCTION_P99" => Some(Self::P99),
                "FUNCTION_AVG" => Some(Self::Avg),
                _ => None,
            }
        }
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct AggregateBucketResponse {
    #[prost(float, repeated, tag = "1")]
    pub result: ::prost::alloc::vec::Vec<f32>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SpanSamplesRequest {
    #[prost(message, optional, tag = "1")]
    pub meta: ::core::option::Option<RequestMeta>,
    #[prost(message, optional, tag = "2")]
    pub filter: ::core::option::Option<TraceItemFilter>,
    #[prost(message, repeated, tag = "3")]
    pub order_by: ::prost::alloc::vec::Vec<span_samples_request::OrderBy>,
    #[prost(message, repeated, tag = "4")]
    pub keys: ::prost::alloc::vec::Vec<AttributeKey>,
    #[prost(uint32, tag = "5")]
    pub limit: u32,
    /// contains context for special columns like project_name, only needs to be included if you are requesting one of those
    #[prost(message, optional, tag = "6")]
    pub attribute_key_transform_context: ::core::option::Option<
        AttributeKeyTransformContext,
    >,
}
/// Nested message and enum types in `SpanSamplesRequest`.
pub mod span_samples_request {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Message)]
    pub struct OrderBy {
        #[prost(message, optional, tag = "1")]
        pub key: ::core::option::Option<super::AttributeKey>,
        #[prost(bool, tag = "2")]
        pub descending: bool,
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SpanSample {
    #[prost(map = "string, message", tag = "1")]
    pub results: ::std::collections::HashMap<
        ::prost::alloc::string::String,
        AttributeValue,
    >,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SpanSamplesResponse {
    #[prost(message, repeated, tag = "1")]
    pub span_samples: ::prost::alloc::vec::Vec<SpanSample>,
}
/// A request for "which tags are available for these projects between these dates" - used for things like autocompletion
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TagsListRequest {
    #[prost(message, optional, tag = "1")]
    pub meta: ::core::option::Option<RequestMeta>,
    #[prost(uint32, tag = "2")]
    pub limit: u32,
    #[prost(uint32, tag = "3")]
    pub offset: u32,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TagsListResponse {
    #[prost(message, repeated, tag = "1")]
    pub tags: ::prost::alloc::vec::Vec<tags_list_response::Tag>,
}
/// Nested message and enum types in `TagsListResponse`.
pub mod tags_list_response {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Message)]
    pub struct Tag {
        #[prost(string, tag = "1")]
        pub name: ::prost::alloc::string::String,
        #[prost(enumeration = "Type", tag = "2")]
        pub r#type: i32,
    }
    #[derive(
        Clone,
        Copy,
        Debug,
        PartialEq,
        Eq,
        Hash,
        PartialOrd,
        Ord,
        ::prost::Enumeration
    )]
    #[repr(i32)]
    pub enum Type {
        Unspecified = 0,
        String = 1,
        Number = 2,
    }
    impl Type {
        /// String value of the enum field names used in the ProtoBuf definition.
        ///
        /// The values are not transformed in any way and thus are considered stable
        /// (if the ProtoBuf definition does not change) and safe for programmatic use.
        pub fn as_str_name(&self) -> &'static str {
            match self {
                Type::Unspecified => "TYPE_UNSPECIFIED",
                Type::String => "TYPE_STRING",
                Type::Number => "TYPE_NUMBER",
            }
        }
        /// Creates an enum from field names used in the ProtoBuf definition.
        pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
            match value {
                "TYPE_UNSPECIFIED" => Some(Self::Unspecified),
                "TYPE_STRING" => Some(Self::String),
                "TYPE_NUMBER" => Some(Self::Number),
                _ => None,
            }
        }
    }
}
