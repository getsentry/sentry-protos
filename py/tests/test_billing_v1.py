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
    MetadataOption,
    MetadataOptions,
    OptionValue,
)
from sentry_protos.billing.v1.feature_pb2 import FeatureOption, FeatureOptions
from sentry_protos.billing.v1.services.contract.v1.contract_pb2 import Contract
from sentry_protos.billing.v1.services.contract.v1.endpoint_get_contract_pb2 import (
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
from sentry_protos.billing.v1.sku_pb2 import SKU
from sentry_protos.billing.v1.credit_pb2 import (
    Credit,
    CreditStatus,
    CreditType,
)
from sentry_protos.billing.v1.date_pb2 import Date as BillingDate
from sentry_protos.billing.v1.services.trial.v1.endpoint_get_trials_pb2 import (
    GetTrialsRequest,
    GetTrialsResponse,
)
from sentry_protos.billing.v1.common.v1.billable_metric_pb2 import (
    BillableMetric,
    BinaryOperation,
    CategoryReference,
    Expression,
    Operator,
)
from sentry_protos.billing.v1.common.v1.billing_interval_pb2 import BillingInterval
from sentry_protos.billing.v1.services.package.v1.package_pb2 import PackageConfig
from sentry_protos.billing.v1.services.package.v1.endpoint_get_package_pb2 import (
    GetPackageRequest,
    GetPackageResponse,
)
from sentry_protos.billing.v1.data_category_pb2 import DataCategory


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
        billing_sku=SKU.SKU_ERRORS,
        base_price_cents=2900,
        payg_budget_cents=10000,
        payg_rate=payg_rate,
        reserved_rate=reserved_rate,
    )
    assert errors_config.HasField("payg_budget_cents")
    assert errors_config.billing_sku == SKU.SKU_ERRORS

    spans_config = SKUConfig(
        billing_sku=SKU.SKU_SPANS,
        base_price_cents=0,
        payg_rate=payg_rate,
        reserved_rate=reserved_rate,
    )
    assert not spans_config.HasField("payg_budget_cents")

    shared_budget = SharedSKUBudget(
        billing_skus=[SKU.SKU_SPANS],
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
            billing_features=FeatureOptions(
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
    assert contract.pricing_config.sku_configs[0].billing_sku == SKU.SKU_ERRORS
    assert len(contract.pricing_config.shared_sku_budgets) == 1
    assert list(contract.pricing_config.shared_sku_budgets[0].billing_skus) == [SKU.SKU_SPANS]
    assert contract.billing_config.address.city == "San Francisco"

    package_metadata = {
        option.key: option.value.string_value
        for option in contract.metadata.package_metadata.options
    }
    assert package_metadata["plan"] == "business"
    assert package_metadata["tier"] == "enterprise"

    billing_features = {
        option.key: option.enabled for option in contract.metadata.billing_features.options
    }
    assert billing_features["sso"] is True
    assert billing_features["custom_dashboards"] is True

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


def test_get_trials_request():
    request = GetTrialsRequest(
        organization_id=12345,
        start_date=BillingDate(year=2026, month=3, day=1),
        end_date=BillingDate(year=2026, month=6, day=1),
    )
    assert request.organization_id == 12345
    assert request.start_date.year == 2026
    assert request.start_date.month == 3
    assert request.end_date.month == 6


def test_get_trials_response():
    credits = [
        Credit(
            type=CreditType.CREDIT_TYPE_CENTS,
            sku=SKU.SKU_ERRORS,
            amount=500000,
            start_date=BillingDate(year=2026, month=3, day=1),
            end_date=BillingDate(year=2026, month=6, day=1),
            status=CreditStatus.CREDIT_STATUS_ACTIVE,
        ),
        Credit(
            type=CreditType.CREDIT_TYPE_UNITS,
            sku=SKU.SKU_REPLAYS,
            amount=10000,
            start_date=BillingDate(year=2026, month=3, day=1),
            end_date=BillingDate(year=2026, month=6, day=1),
            status=CreditStatus.CREDIT_STATUS_ACTIVE,
        ),
    ]
    features = [
        FeatureOptions(
            options=[
                FeatureOption(key="sso", enabled=True),
                FeatureOption(key="custom_dashboards", enabled=True),
            ],
            start_date=BillingDate(year=2026, month=3, day=1),
            end_date=BillingDate(year=2026, month=6, day=1),
        ),
        FeatureOptions(
            options=[
                FeatureOption(key="advanced_analytics", enabled=False),
            ],
            start_date=BillingDate(year=2026, month=4, day=1),
            end_date=BillingDate(year=2026, month=5, day=1),
        ),
    ]
    response = GetTrialsResponse(credits=credits, features=features)
    assert len(response.credits) == 2
    assert response.credits[0].type == CreditType.CREDIT_TYPE_CENTS
    assert response.credits[0].sku == SKU.SKU_ERRORS
    assert response.credits[0].amount == 500000
    assert response.credits[1].type == CreditType.CREDIT_TYPE_UNITS
    assert response.credits[1].sku == SKU.SKU_REPLAYS
    assert len(response.features) == 2
    assert len(response.features[0].options) == 2
    assert response.features[0].start_date.month == 3
    assert response.features[0].end_date.month == 6
    feature_map = {f.key: f.enabled for f in response.features[0].options}
    assert feature_map["sso"] is True
    assert feature_map["custom_dashboards"] is True


def test_get_trials_response_empty():
    response = GetTrialsResponse()
    assert len(response.credits) == 0
    assert len(response.features) == 0


def test_feature_options_with_dates():
    features = FeatureOptions(
        options=[
            FeatureOption(key="sso", enabled=True),
            FeatureOption(key="custom_dashboards", enabled=True),
            FeatureOption(key="advanced_analytics", enabled=False),
        ],
        start_date=BillingDate(year=2026, month=3, day=1),
        end_date=BillingDate(year=2026, month=6, day=1),
    )
    assert len(features.options) == 3
    assert features.start_date.year == 2026
    assert features.start_date.month == 3
    assert features.end_date.month == 6
    feature_map = {f.key: f.enabled for f in features.options}
    assert feature_map["sso"] is True
    assert feature_map["advanced_analytics"] is False


def test_cents_credit():
    credit = Credit(
        type=CreditType.CREDIT_TYPE_CENTS,
        sku=SKU.SKU_ERRORS,
        amount=500000,
        start_date=BillingDate(year=2026, month=3, day=1),
        end_date=BillingDate(year=2026, month=6, day=1),
        status=CreditStatus.CREDIT_STATUS_ACTIVE,
    )
    assert credit.type == CreditType.CREDIT_TYPE_CENTS
    assert credit.sku == SKU.SKU_ERRORS
    assert credit.amount == 500000
    assert credit.start_date.year == 2026
    assert credit.end_date.month == 6
    assert credit.status == CreditStatus.CREDIT_STATUS_ACTIVE


def test_units_credit():
    credit = Credit(
        type=CreditType.CREDIT_TYPE_UNITS,
        sku=SKU.SKU_REPLAYS,
        amount=50000,
        start_date=BillingDate(year=2026, month=3, day=10),
        end_date=BillingDate(year=2026, month=4, day=10),
        status=CreditStatus.CREDIT_STATUS_ACTIVE,
    )
    assert credit.type == CreditType.CREDIT_TYPE_UNITS
    assert credit.sku == SKU.SKU_REPLAYS
    assert credit.amount == 50000


def test_inactive_credit():
    credit = Credit(
        type=CreditType.CREDIT_TYPE_CENTS,
        sku=SKU.SKU_ERRORS,
        amount=100000,
        start_date=BillingDate(year=2026, month=2, day=1),
        end_date=BillingDate(year=2026, month=5, day=1),
        status=CreditStatus.CREDIT_STATUS_INACTIVE,
    )
    assert credit.status == CreditStatus.CREDIT_STATUS_INACTIVE
    assert credit.amount == 100000


def test_billable_metric_with_combined_expression():
    """Illustrates creating a billable metric that combines two data categories.

    This demonstrates the expression:
    performance_unit = DATA_CATEGORY_PROFILE_INDEXED * 0.3 + DATA_CATEGORY_TRANSACTION_INDEXED
    """
    BillableMetric(
        id="perf_unit_1",
        name="performance_units",
        expression=Expression(
            binary_op=BinaryOperation(
                operator=Operator.OPERATOR_ADD,
                left=Expression(
                    binary_op=BinaryOperation(
                        operator=Operator.OPERATOR_MULTIPLY,
                        left=Expression(
                            category_ref=CategoryReference(
                                data_category=DataCategory.DATA_CATEGORY_PROFILE_INDEXED
                            )
                        ),
                        right=Expression(constant=0.3),
                    )
                ),
                right=Expression(
                    category_ref=CategoryReference(
                        data_category=DataCategory.DATA_CATEGORY_TRANSACTION_INDEXED
                    )
                ),
            )
        ),
    )


def test_package_config_with_billing_interval():
    """Test that PackageConfig can be created with a billing interval."""
    # Test monthly billing
    monthly_package = PackageConfig(
        uid="pkg_monthly_123",
        base_price_cents=10000,
        billing_interval=BillingInterval.BILLING_INTERVAL_MONTHLY,
    )
    assert monthly_package.uid == "pkg_monthly_123"
    assert monthly_package.base_price_cents == 10000
    assert monthly_package.billing_interval == BillingInterval.BILLING_INTERVAL_MONTHLY

    # Test annual base with monthly PAYG
    annual_package = PackageConfig(
        uid="pkg_annual_456",
        base_price_cents=100000,
        billing_interval=BillingInterval.BILLING_INTERVAL_ANNUAL_BASE_MONTHLY_PAYG,
    )
    assert annual_package.billing_interval == BillingInterval.BILLING_INTERVAL_ANNUAL_BASE_MONTHLY_PAYG


def test_get_package_request():
    request = GetPackageRequest(package_uid="pkg_monthly_123")
    assert request.package_uid == "pkg_monthly_123"


def test_get_package_response():
    package = PackageConfig(
        uid="pkg_monthly_123",
        base_price_cents=10000,
        billing_interval=BillingInterval.BILLING_INTERVAL_MONTHLY,
    )
    response = GetPackageResponse(package_config=package)
    assert response.package_config.uid == "pkg_monthly_123"
    assert response.package_config.base_price_cents == 10000
    assert response.package_config.billing_interval == BillingInterval.BILLING_INTERVAL_MONTHLY
