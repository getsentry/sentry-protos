from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from sentry_protos.billing.v1.contract_pb2 import (
    BillingChannel,
    BillingConfig,
    BillingInterval,
    BillingType,
    CategoryConfig,
    Contract,
    Credit,
    CreditKind,
    Date,
    ExternalBillingProvider,
    PricingTier,
    SKUConfig,
    StockKeepingUnit,
    SubscriptionOptionValue,
    TieredPricingRate,
)

now = datetime.now()


def test_contract():
    Contract(
        id=1,
        organization_id=42,
        version="2025-01-01_business_abc123",
        created_at=Timestamp(seconds=int(now.timestamp())),
        billing_interval=BillingInterval.BILLING_INTERVAL_ANNUAL,
        contract_period_start=Date(year=2025, month=1, day=1),
        contract_period_end=Date(year=2026, month=1, day=1),
        billing_config=BillingConfig(
            billing_type=BillingType.BILLING_TYPE_CREDIT_CARD,
            channel=BillingChannel.BILLING_CHANNEL_SELF_SERVE,
            external_billing_provider=(
                ExternalBillingProvider.EXTERNAL_BILLING_PROVIDER_STRIPE
            ),
        ),
        base_price_cents=8900,
        max_spend_cents=50000,
        category_configs={
            1: CategoryConfig(
                unit_multiplier=1,
                reserved_rate=TieredPricingRate(
                    tiers=[
                        PricingTier(start=0, end=100000, rate_per_unit_cpe=10),
                        PricingTier(start=100000, end=-1, rate_per_unit_cpe=5),
                    ]
                ),
                reserved_volume=100000,
                free_units=10000,
            ),
        },
        sku_configs=[
            SKUConfig(
                sku=StockKeepingUnit.STOCK_KEEPING_UNIT_ERRORS,
                categories={
                    1: CategoryConfig(
                        unit_multiplier=1,
                        reserved_volume=50000,
                    ),
                },
                base_price_cents=2900,
                payg_budget_cents=10000,
                credits=[
                    Credit(
                        kind=CreditKind.CREDIT_KIND_UNITS,
                        amount=5000,
                        sku=StockKeepingUnit.STOCK_KEEPING_UNIT_ERRORS,
                    ),
                ],
            ),
        ],
        credits=[
            Credit(
                kind=CreditKind.CREDIT_KIND_DOLLARS,
                amount=10000,
            ),
        ],
        features=["sso-basic", "custom-inbound-filters", "data-forwarding"],
        package_metadata={"plan_id": "business", "tier": "business", "name": "Business"},
        subscription_options={
            "max_members": SubscriptionOptionValue(int_value=50),
            "custom_retention": SubscriptionOptionValue(int_value=90),
            "org_name": SubscriptionOptionValue(string_value="Acme Corp"),
        },
    )
