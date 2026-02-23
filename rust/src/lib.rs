pub mod billing {
    pub mod v1 {
       include!("sentry_protos.billing.v1.rs");
   }
}

pub mod conduit {
    pub mod v1alpha {
       include!("sentry_protos.conduit.v1alpha.rs");
   }
}

pub mod seer {
    pub mod v1 {
       include!("sentry_protos.seer.v1.rs");
   }
}

pub mod sentry {
    pub mod v1 {
       include!("sentry_protos.sentry.v1.rs");
   }
}

pub mod snuba {
    pub mod v1 {
       include!("sentry_protos.snuba.v1.rs");
   }
}

pub mod taskbroker {
    pub mod v1 {
       include!("sentry_protos.taskbroker.v1.rs");
   }
}

