pub mod sentry {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.sentry.v1");
   }
}

pub mod relay {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.relay.v1");
   }
}

pub mod seer {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.seer.v1");
   }
}

pub mod options {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.options.v1");
   }
}

pub mod events {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.kafka.events.v1");
   }
}

pub mod snuba {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.snuba.v1");
   }
}

pub mod taskbroker {
    pub mod v1 {
       tonic::include_proto!("sentry_protos.taskbroker.v1");
   }
}

