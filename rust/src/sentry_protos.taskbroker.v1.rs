// This file is @generated by prost-build.
#[derive(Clone, Copy, PartialEq, ::prost::Message)]
pub struct RetryState {
    /// Current attempt number
    #[prost(uint32, tag = "1")]
    pub attempts: u32,
    /// After this number of attempts, the task is either discarded or deadlettered.
    #[prost(uint32, tag = "2")]
    pub max_attempts: u32,
    /// The action to take after the max_attempts is exceeded.
    #[prost(enumeration = "OnAttemptsExceeded", tag = "3")]
    pub on_attempts_exceeded: i32,
    /// Whether a task should be executed at most once.
    #[prost(bool, optional, tag = "4")]
    pub at_most_once: ::core::option::Option<bool>,
    /// Duration in seconds that a task must wait to begin execution after it is retried.
    #[prost(uint64, optional, tag = "5")]
    pub delay_on_retry: ::core::option::Option<u64>,
}
/// Task message that is stored in Kafka and shared over RPC.
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TaskActivation {
    /// A GUID for the task. Used to update tasks
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    /// The task namespace
    #[prost(string, tag = "2")]
    pub namespace: ::prost::alloc::string::String,
    /// The name of the task. This name is resolved within the worker
    #[prost(string, tag = "3")]
    pub taskname: ::prost::alloc::string::String,
    /// An opaque parameter collection. Could be JSON or protobuf encoded
    #[prost(string, tag = "4")]
    pub parameters: ::prost::alloc::string::String,
    /// A map of headers for the task.
    #[prost(map = "string, string", tag = "5")]
    pub headers: ::std::collections::HashMap<
        ::prost::alloc::string::String,
        ::prost::alloc::string::String,
    >,
    /// The timestamp a task was stored in Kafka
    #[prost(message, optional, tag = "6")]
    pub received_at: ::core::option::Option<::prost_types::Timestamp>,
    /// Retry state
    #[prost(message, optional, tag = "7")]
    pub retry_state: ::core::option::Option<RetryState>,
    /// The duration in seconds that a worker has to complete task execution.
    /// When an activation is moved from pending -> processing a result is expected
    /// in this many seconds.
    #[prost(uint64, tag = "8")]
    pub processing_deadline_duration: u64,
    /// The duration in seconds that a task has to start execution.
    /// After received_at + expires has passed an activation is expired and will not be executed.
    #[prost(uint64, optional, tag = "9")]
    pub expires: ::core::option::Option<u64>,
    /// The duration in seconds that a task must wait to begin execution after it is emitted.
    /// After received_at + delay has passed, the activation will become pending.
    #[prost(uint64, optional, tag = "11")]
    pub delay: ::core::option::Option<u64>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetTaskRequest {
    #[prost(string, optional, tag = "1")]
    pub namespace: ::core::option::Option<::prost::alloc::string::String>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct GetTaskResponse {
    /// If there are no tasks available, this will be empty
    #[prost(message, optional, tag = "1")]
    pub task: ::core::option::Option<TaskActivation>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FetchNextTask {
    #[prost(string, optional, tag = "1")]
    pub namespace: ::core::option::Option<::prost::alloc::string::String>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SetTaskStatusRequest {
    #[prost(string, tag = "1")]
    pub id: ::prost::alloc::string::String,
    #[prost(enumeration = "TaskActivationStatus", tag = "2")]
    pub status: i32,
    /// If fetch_next is provided, receive a new task in the response
    #[prost(message, optional, tag = "3")]
    pub fetch_next_task: ::core::option::Option<FetchNextTask>,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct SetTaskStatusResponse {
    /// The next task the worker should execute. Requires fetch_next to be set on the request.
    #[prost(message, optional, tag = "1")]
    pub task: ::core::option::Option<TaskActivation>,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum OnAttemptsExceeded {
    Unspecified = 0,
    Discard = 1,
    Deadletter = 2,
}
impl OnAttemptsExceeded {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            OnAttemptsExceeded::Unspecified => "ON_ATTEMPTS_EXCEEDED_UNSPECIFIED",
            OnAttemptsExceeded::Discard => "ON_ATTEMPTS_EXCEEDED_DISCARD",
            OnAttemptsExceeded::Deadletter => "ON_ATTEMPTS_EXCEEDED_DEADLETTER",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "ON_ATTEMPTS_EXCEEDED_UNSPECIFIED" => Some(Self::Unspecified),
            "ON_ATTEMPTS_EXCEEDED_DISCARD" => Some(Self::Discard),
            "ON_ATTEMPTS_EXCEEDED_DEADLETTER" => Some(Self::Deadletter),
            _ => None,
        }
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord, ::prost::Enumeration)]
#[repr(i32)]
pub enum TaskActivationStatus {
    Unspecified = 0,
    Pending = 1,
    Processing = 2,
    Failure = 3,
    Retry = 4,
    Complete = 5,
}
impl TaskActivationStatus {
    /// String value of the enum field names used in the ProtoBuf definition.
    ///
    /// The values are not transformed in any way and thus are considered stable
    /// (if the ProtoBuf definition does not change) and safe for programmatic use.
    pub fn as_str_name(&self) -> &'static str {
        match self {
            TaskActivationStatus::Unspecified => "TASK_ACTIVATION_STATUS_UNSPECIFIED",
            TaskActivationStatus::Pending => "TASK_ACTIVATION_STATUS_PENDING",
            TaskActivationStatus::Processing => "TASK_ACTIVATION_STATUS_PROCESSING",
            TaskActivationStatus::Failure => "TASK_ACTIVATION_STATUS_FAILURE",
            TaskActivationStatus::Retry => "TASK_ACTIVATION_STATUS_RETRY",
            TaskActivationStatus::Complete => "TASK_ACTIVATION_STATUS_COMPLETE",
        }
    }
    /// Creates an enum from field names used in the ProtoBuf definition.
    pub fn from_str_name(value: &str) -> ::core::option::Option<Self> {
        match value {
            "TASK_ACTIVATION_STATUS_UNSPECIFIED" => Some(Self::Unspecified),
            "TASK_ACTIVATION_STATUS_PENDING" => Some(Self::Pending),
            "TASK_ACTIVATION_STATUS_PROCESSING" => Some(Self::Processing),
            "TASK_ACTIVATION_STATUS_FAILURE" => Some(Self::Failure),
            "TASK_ACTIVATION_STATUS_RETRY" => Some(Self::Retry),
            "TASK_ACTIVATION_STATUS_COMPLETE" => Some(Self::Complete),
            _ => None,
        }
    }
}
/// Generated client implementations.
pub mod consumer_service_client {
    #![allow(
        unused_variables,
        dead_code,
        missing_docs,
        clippy::wildcard_imports,
        clippy::let_unit_value,
    )]
    use tonic::codegen::*;
    use tonic::codegen::http::Uri;
    /// //////////////////////////
    /// RPC messages and services
    /// //////////////////////////
    #[derive(Debug, Clone)]
    pub struct ConsumerServiceClient<T> {
        inner: tonic::client::Grpc<T>,
    }
    impl ConsumerServiceClient<tonic::transport::Channel> {
        /// Attempt to create a new client by connecting to a given endpoint.
        pub async fn connect<D>(dst: D) -> Result<Self, tonic::transport::Error>
        where
            D: TryInto<tonic::transport::Endpoint>,
            D::Error: Into<StdError>,
        {
            let conn = tonic::transport::Endpoint::new(dst)?.connect().await?;
            Ok(Self::new(conn))
        }
    }
    impl<T> ConsumerServiceClient<T>
    where
        T: tonic::client::GrpcService<tonic::body::Body>,
        T::Error: Into<StdError>,
        T::ResponseBody: Body<Data = Bytes> + std::marker::Send + 'static,
        <T::ResponseBody as Body>::Error: Into<StdError> + std::marker::Send,
    {
        pub fn new(inner: T) -> Self {
            let inner = tonic::client::Grpc::new(inner);
            Self { inner }
        }
        pub fn with_origin(inner: T, origin: Uri) -> Self {
            let inner = tonic::client::Grpc::with_origin(inner, origin);
            Self { inner }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> ConsumerServiceClient<InterceptedService<T, F>>
        where
            F: tonic::service::Interceptor,
            T::ResponseBody: Default,
            T: tonic::codegen::Service<
                http::Request<tonic::body::Body>,
                Response = http::Response<
                    <T as tonic::client::GrpcService<tonic::body::Body>>::ResponseBody,
                >,
            >,
            <T as tonic::codegen::Service<
                http::Request<tonic::body::Body>,
            >>::Error: Into<StdError> + std::marker::Send + std::marker::Sync,
        {
            ConsumerServiceClient::new(InterceptedService::new(inner, interceptor))
        }
        /// Compress requests with the given encoding.
        ///
        /// This requires the server to support it otherwise it might respond with an
        /// error.
        #[must_use]
        pub fn send_compressed(mut self, encoding: CompressionEncoding) -> Self {
            self.inner = self.inner.send_compressed(encoding);
            self
        }
        /// Enable decompressing responses.
        #[must_use]
        pub fn accept_compressed(mut self, encoding: CompressionEncoding) -> Self {
            self.inner = self.inner.accept_compressed(encoding);
            self
        }
        /// Limits the maximum size of a decoded message.
        ///
        /// Default: `4MB`
        #[must_use]
        pub fn max_decoding_message_size(mut self, limit: usize) -> Self {
            self.inner = self.inner.max_decoding_message_size(limit);
            self
        }
        /// Limits the maximum size of an encoded message.
        ///
        /// Default: `usize::MAX`
        #[must_use]
        pub fn max_encoding_message_size(mut self, limit: usize) -> Self {
            self.inner = self.inner.max_encoding_message_size(limit);
            self
        }
        /// Fetch a new task activation to process.
        pub async fn get_task(
            &mut self,
            request: impl tonic::IntoRequest<super::GetTaskRequest>,
        ) -> std::result::Result<
            tonic::Response<super::GetTaskResponse>,
            tonic::Status,
        > {
            self.inner
                .ready()
                .await
                .map_err(|e| {
                    tonic::Status::unknown(
                        format!("Service was not ready: {}", e.into()),
                    )
                })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static(
                "/sentry_protos.taskbroker.v1.ConsumerService/GetTask",
            );
            let mut req = request.into_request();
            req.extensions_mut()
                .insert(
                    GrpcMethod::new(
                        "sentry_protos.taskbroker.v1.ConsumerService",
                        "GetTask",
                    ),
                );
            self.inner.unary(req, path, codec).await
        }
        /// Update the state of a task with execution results.
        pub async fn set_task_status(
            &mut self,
            request: impl tonic::IntoRequest<super::SetTaskStatusRequest>,
        ) -> std::result::Result<
            tonic::Response<super::SetTaskStatusResponse>,
            tonic::Status,
        > {
            self.inner
                .ready()
                .await
                .map_err(|e| {
                    tonic::Status::unknown(
                        format!("Service was not ready: {}", e.into()),
                    )
                })?;
            let codec = tonic::codec::ProstCodec::default();
            let path = http::uri::PathAndQuery::from_static(
                "/sentry_protos.taskbroker.v1.ConsumerService/SetTaskStatus",
            );
            let mut req = request.into_request();
            req.extensions_mut()
                .insert(
                    GrpcMethod::new(
                        "sentry_protos.taskbroker.v1.ConsumerService",
                        "SetTaskStatus",
                    ),
                );
            self.inner.unary(req, path, codec).await
        }
    }
}
/// Generated server implementations.
pub mod consumer_service_server {
    #![allow(
        unused_variables,
        dead_code,
        missing_docs,
        clippy::wildcard_imports,
        clippy::let_unit_value,
    )]
    use tonic::codegen::*;
    /// Generated trait containing gRPC methods that should be implemented for use with ConsumerServiceServer.
    #[async_trait]
    pub trait ConsumerService: std::marker::Send + std::marker::Sync + 'static {
        /// Fetch a new task activation to process.
        async fn get_task(
            &self,
            request: tonic::Request<super::GetTaskRequest>,
        ) -> std::result::Result<tonic::Response<super::GetTaskResponse>, tonic::Status>;
        /// Update the state of a task with execution results.
        async fn set_task_status(
            &self,
            request: tonic::Request<super::SetTaskStatusRequest>,
        ) -> std::result::Result<
            tonic::Response<super::SetTaskStatusResponse>,
            tonic::Status,
        >;
    }
    /// //////////////////////////
    /// RPC messages and services
    /// //////////////////////////
    #[derive(Debug)]
    pub struct ConsumerServiceServer<T> {
        inner: Arc<T>,
        accept_compression_encodings: EnabledCompressionEncodings,
        send_compression_encodings: EnabledCompressionEncodings,
        max_decoding_message_size: Option<usize>,
        max_encoding_message_size: Option<usize>,
    }
    impl<T> ConsumerServiceServer<T> {
        pub fn new(inner: T) -> Self {
            Self::from_arc(Arc::new(inner))
        }
        pub fn from_arc(inner: Arc<T>) -> Self {
            Self {
                inner,
                accept_compression_encodings: Default::default(),
                send_compression_encodings: Default::default(),
                max_decoding_message_size: None,
                max_encoding_message_size: None,
            }
        }
        pub fn with_interceptor<F>(
            inner: T,
            interceptor: F,
        ) -> InterceptedService<Self, F>
        where
            F: tonic::service::Interceptor,
        {
            InterceptedService::new(Self::new(inner), interceptor)
        }
        /// Enable decompressing requests with the given encoding.
        #[must_use]
        pub fn accept_compressed(mut self, encoding: CompressionEncoding) -> Self {
            self.accept_compression_encodings.enable(encoding);
            self
        }
        /// Compress responses with the given encoding, if the client supports it.
        #[must_use]
        pub fn send_compressed(mut self, encoding: CompressionEncoding) -> Self {
            self.send_compression_encodings.enable(encoding);
            self
        }
        /// Limits the maximum size of a decoded message.
        ///
        /// Default: `4MB`
        #[must_use]
        pub fn max_decoding_message_size(mut self, limit: usize) -> Self {
            self.max_decoding_message_size = Some(limit);
            self
        }
        /// Limits the maximum size of an encoded message.
        ///
        /// Default: `usize::MAX`
        #[must_use]
        pub fn max_encoding_message_size(mut self, limit: usize) -> Self {
            self.max_encoding_message_size = Some(limit);
            self
        }
    }
    impl<T, B> tonic::codegen::Service<http::Request<B>> for ConsumerServiceServer<T>
    where
        T: ConsumerService,
        B: Body + std::marker::Send + 'static,
        B::Error: Into<StdError> + std::marker::Send + 'static,
    {
        type Response = http::Response<tonic::body::Body>;
        type Error = std::convert::Infallible;
        type Future = BoxFuture<Self::Response, Self::Error>;
        fn poll_ready(
            &mut self,
            _cx: &mut Context<'_>,
        ) -> Poll<std::result::Result<(), Self::Error>> {
            Poll::Ready(Ok(()))
        }
        fn call(&mut self, req: http::Request<B>) -> Self::Future {
            match req.uri().path() {
                "/sentry_protos.taskbroker.v1.ConsumerService/GetTask" => {
                    #[allow(non_camel_case_types)]
                    struct GetTaskSvc<T: ConsumerService>(pub Arc<T>);
                    impl<
                        T: ConsumerService,
                    > tonic::server::UnaryService<super::GetTaskRequest>
                    for GetTaskSvc<T> {
                        type Response = super::GetTaskResponse;
                        type Future = BoxFuture<
                            tonic::Response<Self::Response>,
                            tonic::Status,
                        >;
                        fn call(
                            &mut self,
                            request: tonic::Request<super::GetTaskRequest>,
                        ) -> Self::Future {
                            let inner = Arc::clone(&self.0);
                            let fut = async move {
                                <T as ConsumerService>::get_task(&inner, request).await
                            };
                            Box::pin(fut)
                        }
                    }
                    let accept_compression_encodings = self.accept_compression_encodings;
                    let send_compression_encodings = self.send_compression_encodings;
                    let max_decoding_message_size = self.max_decoding_message_size;
                    let max_encoding_message_size = self.max_encoding_message_size;
                    let inner = self.inner.clone();
                    let fut = async move {
                        let method = GetTaskSvc(inner);
                        let codec = tonic::codec::ProstCodec::default();
                        let mut grpc = tonic::server::Grpc::new(codec)
                            .apply_compression_config(
                                accept_compression_encodings,
                                send_compression_encodings,
                            )
                            .apply_max_message_size_config(
                                max_decoding_message_size,
                                max_encoding_message_size,
                            );
                        let res = grpc.unary(method, req).await;
                        Ok(res)
                    };
                    Box::pin(fut)
                }
                "/sentry_protos.taskbroker.v1.ConsumerService/SetTaskStatus" => {
                    #[allow(non_camel_case_types)]
                    struct SetTaskStatusSvc<T: ConsumerService>(pub Arc<T>);
                    impl<
                        T: ConsumerService,
                    > tonic::server::UnaryService<super::SetTaskStatusRequest>
                    for SetTaskStatusSvc<T> {
                        type Response = super::SetTaskStatusResponse;
                        type Future = BoxFuture<
                            tonic::Response<Self::Response>,
                            tonic::Status,
                        >;
                        fn call(
                            &mut self,
                            request: tonic::Request<super::SetTaskStatusRequest>,
                        ) -> Self::Future {
                            let inner = Arc::clone(&self.0);
                            let fut = async move {
                                <T as ConsumerService>::set_task_status(&inner, request)
                                    .await
                            };
                            Box::pin(fut)
                        }
                    }
                    let accept_compression_encodings = self.accept_compression_encodings;
                    let send_compression_encodings = self.send_compression_encodings;
                    let max_decoding_message_size = self.max_decoding_message_size;
                    let max_encoding_message_size = self.max_encoding_message_size;
                    let inner = self.inner.clone();
                    let fut = async move {
                        let method = SetTaskStatusSvc(inner);
                        let codec = tonic::codec::ProstCodec::default();
                        let mut grpc = tonic::server::Grpc::new(codec)
                            .apply_compression_config(
                                accept_compression_encodings,
                                send_compression_encodings,
                            )
                            .apply_max_message_size_config(
                                max_decoding_message_size,
                                max_encoding_message_size,
                            );
                        let res = grpc.unary(method, req).await;
                        Ok(res)
                    };
                    Box::pin(fut)
                }
                _ => {
                    Box::pin(async move {
                        let mut response = http::Response::new(
                            tonic::body::Body::default(),
                        );
                        let headers = response.headers_mut();
                        headers
                            .insert(
                                tonic::Status::GRPC_STATUS,
                                (tonic::Code::Unimplemented as i32).into(),
                            );
                        headers
                            .insert(
                                http::header::CONTENT_TYPE,
                                tonic::metadata::GRPC_CONTENT_TYPE,
                            );
                        Ok(response)
                    })
                }
            }
        }
    }
    impl<T> Clone for ConsumerServiceServer<T> {
        fn clone(&self) -> Self {
            let inner = self.inner.clone();
            Self {
                inner,
                accept_compression_encodings: self.accept_compression_encodings,
                send_compression_encodings: self.send_compression_encodings,
                max_decoding_message_size: self.max_decoding_message_size,
                max_encoding_message_size: self.max_encoding_message_size,
            }
        }
    }
    /// Generated gRPC service name
    pub const SERVICE_NAME: &str = "sentry_protos.taskbroker.v1.ConsumerService";
    impl<T> tonic::server::NamedService for ConsumerServiceServer<T> {
        const NAME: &'static str = SERVICE_NAME;
    }
}
