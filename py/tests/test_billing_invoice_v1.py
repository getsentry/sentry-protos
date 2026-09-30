from sentry_protos.billing.v1.services.contract.v1.invoice_pb2 import Invoice


def test_invoice_external_invoice_id() -> None:
    invoice = Invoice(external_invoice_id="external-invoice-id")

    assert invoice.HasField("external_invoice_id")
    assert invoice.external_invoice_id == "external-invoice-id"
