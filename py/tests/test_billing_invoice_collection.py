from google.protobuf.timestamp_pb2 import Timestamp

from sentry_protos.billing.v1.common.v1.external_billing_provider_pb2 import (
    EXTERNAL_BILLING_PROVIDER_VERCEL,
)
from sentry_protos.billing.v1.services.charge.v1.endpoint_capture_charge_pb2 import (
    CHARGE_METHOD_VERCEL,
    CaptureChargeRequest,
    CaptureChargeResponse,
    VercelInvoiceData,
    VercelInvoiceLineItem,
)
from sentry_protos.billing.v1.services.contract.v1.invoice_pb2 import Invoice


def test_invoice_external_billing_provider() -> None:
    period_start = Timestamp(seconds=1_700_000_000)
    period_end = Timestamp(seconds=1_702_592_000)
    invoice = Invoice(
        external_billing_provider=EXTERNAL_BILLING_PROVIDER_VERCEL,
        period_start=period_start,
        period_end=period_end,
        package_uid="0e9df1c7-05dd-4584-9f45-4dad1dc4778f",
    )

    assert invoice.HasField("external_billing_provider")
    assert invoice.external_billing_provider == EXTERNAL_BILLING_PROVIDER_VERCEL
    assert invoice.period_start == period_start
    assert invoice.period_end == period_end
    assert invoice.package_uid == "0e9df1c7-05dd-4584-9f45-4dad1dc4778f"


def test_vercel_charge_can_await_asynchronous_payment() -> None:
    request = CaptureChargeRequest(
        charge_method=CHARGE_METHOD_VERCEL,
        vercel_invoice=VercelInvoiceData(
            billing_plan_id="pro",
            line_items=[
                VercelInvoiceLineItem(
                    amount_cents=1_000,
                    description="Subscription",
                    type="subscription",
                )
            ],
        ),
    )
    response = CaptureChargeResponse(paid=False, awaiting_payment=True)

    assert request.charge_method == CHARGE_METHOD_VERCEL
    assert request.vercel_invoice.billing_plan_id == "pro"
    assert request.vercel_invoice.line_items[0].amount_cents == 1_000
    assert response.paid is False
    assert response.awaiting_payment is True
