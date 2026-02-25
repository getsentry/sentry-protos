from sentry_protos.billing.v1.contract_pb2 import (
    Address,
    BillingConfig,
    BillingChannel,
    BillingType,
    Contract,
    Credit,
    CreditType,
    Date,
    ExternalBillingProvider,
    OptionValue,
    PricingTier,
    SKU,
    SKUConfig,
    SharedSKUBudget,
    TieredPricingRate,
)


def test_contract_with_all_sub_messages():
    payg_rate = TieredPricingRate(
        tiers=[
            PricingTier(start=0, end=100_000, rate_per_unit_cpe=500),
            PricingTier(start=100_001, end=-1, rate_per_unit_cpe=300),
        ]
    )
    reserved_rate = TieredPricingRate(
        tiers=[
            PricingTier(start=0, end=-1, rate_per_unit_cpe=100),
        ]
    )

    errors_config = SKUConfig(
        sku=SKU.SKU_ERRORS,
        base_price_cents=2900,
        payg_budget_cents=10000,
        reserved_volume=50_000,
        payg_rate=payg_rate,
        reserved_rate=reserved_rate,
        credits=[Credit(type=CreditType.CREDIT_TYPE_UNITS, amount=1000)],
    )
    assert errors_config.HasField("payg_budget_cents")

    spans_config = SKUConfig(
        sku=SKU.SKU_SPANS,
        base_price_cents=0,
        reserved_volume=100_000,
        payg_rate=payg_rate,
        reserved_rate=reserved_rate,
    )
    assert not spans_config.HasField("payg_budget_cents")

    shared_budget = SharedSKUBudget(
        skus=[spans_config],
        reserved_budget_cents=50000,
        payg_budget_cents=25000,
        credits=[Credit(type=CreditType.CREDIT_TYPE_DOLLARS, amount=5000)],
    )

    contract = Contract(
        id=12345,
        organization_id=67890,
        ruleset_version="2024.1",
        package_metadata={"plan": "business", "tier": "enterprise"},
        contract_start_date=Date(year=2024, month=1, day=1),
        contract_end_date=Date(year=2025, month=1, day=1),
        billing_period_start_date=Date(year=2024, month=6, day=1),
        billing_period_end_date=Date(year=2024, month=7, day=1),
        features={"sso": True, "custom_dashboards": True},
        sku_configs=[errors_config],
        shared_sku_budgets=[shared_budget],
        max_spend_cents=100000,
        base_price_cents=8900,
        billing_config=BillingConfig(
            billing_type=BillingType.BILLING_TYPE_CREDIT_CARD,
            channel=BillingChannel.BILLING_CHANNEL_SELF_SERVE,
            external_billing_provider=ExternalBillingProvider.EXTERNAL_BILLING_PROVIDER_STRIPE,
            address=Address(
                city="San Francisco",
                region="CA",
                country_code="US",
                postal_code="94107",
                address_line_1="45 Fremont St",
            ),
        ),
        custom_options={
            "override_rate_limit": OptionValue(int_value=5000),
            "is_internal": OptionValue(bool_value=True),
            "note": OptionValue(string_value="beta"),
        },
        credits=[Credit(type=CreditType.CREDIT_TYPE_DOLLARS, amount=10000)],
    )

    assert contract.id == 12345
    assert contract.organization_id == 67890
    assert contract.contract_start_date.year == 2024
    assert len(contract.sku_configs) == 1
    assert contract.sku_configs[0].sku == SKU.SKU_ERRORS
    assert len(contract.shared_sku_budgets) == 1
    assert contract.billing_config.address.city == "San Francisco"
    assert contract.features["sso"] is True
    assert contract.custom_options["override_rate_limit"].int_value == 5000
    assert contract.custom_options["is_internal"].bool_value is True
    assert contract.custom_options["note"].string_value == "beta"
    assert len(contract.credits) == 1
