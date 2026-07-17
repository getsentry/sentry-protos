//! Tests for generated proto bindings.
//!
//! These tests verify that:
//! - All expected modules are importable at the correct paths
//! - Cross-package type references resolve correctly (the exact bug
//!   that broke v0.8.3, where `super::` paths were invalid)
//! - Proto messages can be encoded and decoded via prost

use prost::Message;

// ── Module importability ────────────────────────────────────────────
// These `use` statements are compile-time tests. If a module path is
// wrong or a type doesn't exist, the test file won't compile.

use sentry_protos::billing::v1::common::v1::{DataCategoryRetention, RetentionSettings};
use sentry_protos::billing::v1::DataCategory;
use sentry_protos::billing::v1::Date;
use sentry_protos::billing::v1::SeatCategory;
use sentry_protos::billing::v1::UsageData;
use sentry_protos::billing::v1::services::contract::v1::{
    Contract, GetContractRequest, RetentionConfig, RetentionOverride,
};
use sentry_protos::billing::v1::services::package::v1::PackageConfig;
use sentry_protos::billing::v1::services::usage::v1::{
    CategorySeatUsage, CategoryUsage, DailySeatUsage, DailyUsage, GetUsageRequest,
    GetUsageResponse,
};
use sentry_protos::sentry::v1::RetryState;

fn assert_roundtrip<M: Message + Default + PartialEq + std::fmt::Debug>(msg: &M) {
    let bytes = msg.encode_to_vec();
    let decoded = M::decode(bytes.as_slice()).unwrap();
    assert_eq!(*msg, decoded);
}

// ── Protobuf encode/decode roundtrip ────────────────────────────────
// These tests also serve as cross-package regression coverage: types
// from nested packages (usage::v1, contract::v1) reference types from
// parent packages (billing::v1). If the module hierarchy is wrong,
// these won't compile.

#[test]
fn roundtrip_category_usage() {
    assert_roundtrip(&CategoryUsage {
        category: DataCategory::Transaction as i32,
        data: Some(UsageData {
            accepted: 1000,
            dropped: 50,
            ..Default::default()
        }),
    });
}

#[test]
fn roundtrip_get_usage_response() {
    assert_roundtrip(&GetUsageResponse {
        days: vec![DailyUsage {
            date: Some(Date {
                year: 2026,
                month: 1,
                day: 15,
            }),
            usage: vec![CategoryUsage {
                category: DataCategory::Error as i32,
                data: Some(UsageData {
                    accepted: 500,
                    dropped: 10,
                    ..Default::default()
                }),
            }],
        }],
        seat_days: vec![DailySeatUsage {
            date: Some(Date {
                year: 2026,
                month: 1,
                day: 15,
            }),
            seats: vec![CategorySeatUsage {
                category: SeatCategory::Monitor as i32,
                count: 5,
            }],
        }],
        ..Default::default()
    });
}

#[test]
fn roundtrip_get_contract_request() {
    assert_roundtrip(&GetContractRequest {
        organization_id: 42,
        date: None,
    });
}

#[test]
fn roundtrip_retry_state() {
    assert_roundtrip(&RetryState {
        attempts: 3,
        kind: "exponential".into(),
        discard_after_attempt: Some(10),
        deadletter_after_attempt: Some(5),
        at_most_once: Some(false),
    });
}

#[test]
fn default_messages_roundtrip() {
    assert_roundtrip(&CategoryUsage::default());
    assert_roundtrip(&GetUsageRequest::default());
    assert_roundtrip(&GetUsageResponse::default());
    assert_roundtrip(&Contract::default());
}

#[test]
fn roundtrip_retention_with_downsampled_days() {
    assert_roundtrip(&DataCategoryRetention {
        category: DataCategory::Span as i32,
        settings: Some(RetentionSettings {
            standard_days: 30,
            downsampled_days: Some(90),
        }),
    });
}

#[test]
fn roundtrip_retention_with_downsampled_compatibility_value() {
    assert_roundtrip(&DataCategoryRetention {
        category: DataCategory::Transaction as i32,
        settings: Some(RetentionSettings {
            standard_days: 30,
            downsampled_days: Some(0),
        }),
    });
}

#[test]
fn roundtrip_retention_without_downsampled_representation() {
    assert_roundtrip(&DataCategoryRetention {
        category: DataCategory::Error as i32,
        settings: Some(RetentionSettings {
            standard_days: 90,
            downsampled_days: None,
        }),
    });
}

#[test]
fn roundtrip_package_config_with_retention_defaults() {
    assert_roundtrip(&PackageConfig {
        uid: "business".into(),
        retention_defaults: vec![
            DataCategoryRetention {
                category: DataCategory::Span as i32,
                settings: Some(RetentionSettings {
                    standard_days: 30,
                    downsampled_days: Some(396),
                }),
            },
            DataCategoryRetention {
                category: DataCategory::Transaction as i32,
                settings: Some(RetentionSettings {
                    standard_days: 30,
                    downsampled_days: Some(0),
                }),
            },
            DataCategoryRetention {
                category: DataCategory::Error as i32,
                settings: Some(RetentionSettings {
                    standard_days: 90,
                    downsampled_days: None,
                }),
            },
        ],
        ..Default::default()
    });
}

#[test]
fn roundtrip_contract_retention_config() {
    assert_roundtrip(&Contract {
        retention_config: Some(RetentionConfig {
            revision: "rev_abc123".into(),
            organization_days: Some(180),
            overrides: vec![
                // Standard-only override: downsampled uses the package default.
                RetentionOverride {
                    category: DataCategory::Span as i32,
                    standard_days: Some(90),
                    downsampled_days: None,
                },
                // Downsampled-only override: standard uses the package default.
                RetentionOverride {
                    category: DataCategory::Transaction as i32,
                    standard_days: None,
                    downsampled_days: Some(396),
                },
            ],
        }),
        ..Default::default()
    });
}
