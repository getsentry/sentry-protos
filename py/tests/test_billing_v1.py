from sentry_protos.billing.v1.services.contract.v1.billing_config_pb2 import (
    Address,
    BillingChannel,
    BillingConfig,
    BillingType,
    Date,
    ExternalBillingProvider,
)
from sentry_protos.billing.v1.services.contract.v1.contract_metadata_pb2 import (
    ContractMetadata,
    FeatureOption,
    FeatureOptions,
    MetadataOption,
    MetadataOptions,
    OptionValue,
)
from sentry_protos.billing.v1.services.contract.v1.contract_pb2 import (
    Contract,
    GetContractRequest,
    GetContractResponse,
)
from sentry_protos.billing.v1.services.contract.v1.pricing_config_pb2 import (
    PricingConfig,
    PricingTier,
    SharedSKUBudget,
    SKUConfig,
    TieredPricingRate,
)
from sentry_protos.billing.v1.services.contract.v1.sku_pb2 import SKU


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
        skus=[SKU.SKU_SPANS],
        reserved_budget_cents=50000,
        payg_budget_cents=25000,
    )

    contract = Contract(
        metadata=ContractMetadata(
            id=12345,
            organization_id=67890,
            ruleset_version="2024.1",
            package_metadata=MetadataOptions(
                options=[
                    MetadataOption(key="plan", value=OptionValue(string_value="business")),
                    MetadataOption(
                        key="tier", value=OptionValue(string_value="enterprise")
                    ),
                ],
            ),
            features=FeatureOptions(
                options=[
                    FeatureOption(key="sso", enabled=True),
                    FeatureOption(key="custom_dashboards", enabled=True),
                ],
            ),
            custom_options=MetadataOptions(
                options=[
                    MetadataOption(
                        key="override_rate_limit", value=OptionValue(int_value=5000)
                    ),
                    MetadataOption(key="is_internal", value=OptionValue(bool_value=True)),
                    MetadataOption(key="note", value=OptionValue(string_value="beta")),
                ],
            ),
        ),
        billing_config=BillingConfig(
            billing_type=BillingType.BILLING_TYPE_CREDIT_CARD,
            channel=BillingChannel.BILLING_CHANNEL_SELF_SERVE,
            external_billing_provider=ExternalBillingProvider.EXTERNAL_BILLING_PROVIDER_STRIPE,
            contract_start_date=Date(year=2024, month=1, day=1),
            contract_end_date=Date(year=2025, month=1, day=1),
            address=Address(
                city="San Francisco",
                region="CA",
                country_code="US",
                postal_code="94107",
                address_line_1="45 Fremont St",
            ),
        ),
        pricing_config=PricingConfig(
            sku_configs=[errors_config],
            shared_sku_budgets=[shared_budget],
            billing_period_start_date=Date(year=2024, month=6, day=1),
            billing_period_end_date=Date(year=2024, month=7, day=1),
            max_spend_cents=100000,
            base_price_cents=8900,
        ),
    )

    assert contract.metadata.id == 12345
    assert contract.metadata.organization_id == 67890
    assert contract.billing_config.contract_start_date.year == 2024
    assert len(contract.pricing_config.sku_configs) == 1
    assert contract.pricing_config.sku_configs[0].sku == SKU.SKU_ERRORS
    assert len(contract.pricing_config.shared_sku_budgets) == 1
    assert contract.billing_config.address.city == "San Francisco"

    package_metadata = {
        option.key: option.value.string_value
        for option in contract.metadata.package_metadata.options
    }
    assert package_metadata["plan"] == "business"
    assert package_metadata["tier"] == "enterprise"

    features = {option.key: option.enabled for option in contract.metadata.features.options}
    assert features["sso"] is True

    custom_options = {
        option.key: option.value for option in contract.metadata.custom_options.options
    }
    assert custom_options["override_rate_limit"].int_value == 5000
    assert custom_options["is_internal"].bool_value is True
    assert custom_options["note"].string_value == "beta"


def test_get_contract_request():
    request = GetContractRequest(organization_id=67890)
    assert request.organization_id == 67890


def test_get_contract_response():
    contract = Contract(
        metadata=ContractMetadata(
            id=12345,
            organization_id=67890,
        ),
        billing_config=BillingConfig(
            billing_type=BillingType.BILLING_TYPE_CREDIT_CARD,
        ),
        pricing_config=PricingConfig(
            base_price_cents=8900,
        ),
    )
    response = GetContractResponse(contract=contract)
    assert response.contract.metadata.id == 12345
    assert response.contract.metadata.organization_id == 67890
    assert response.contract.billing_config.billing_type == BillingType.BILLING_TYPE_CREDIT_CARD
    assert response.contract.pricing_config.base_price_cents == 8900
