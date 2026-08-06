from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from sales.models import Sale

from .models import Payment, RetailerCredit


class PaymentService:

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def record_payment(*, sale, amount, payment_date, payment_method="", notes="", recorded_by):
        """
        Record a payment against an existing Sale.

        Validates the amount, creates a Payment record, and
        updates the Sale's financial fields + payment status.

        If the payment exceeds the remaining amount due, only the
        due portion is applied to the Sale and the excess is stored
        as a RetailerCredit (reason=OVERPAYMENT).
        """

        # --- 1. Validate -------------------------------------------
        PaymentService._validate_amount(amount)

        # --- 2. Split into applied vs. excess ----------------------
        applied_amount = min(amount, sale.amount_due)
        excess = amount - applied_amount

        # --- 3. Create Payment record (always stores full amount) --
        payment = PaymentService._create_payment(
            sale=sale,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            notes=notes,
            recorded_by=recorded_by,
        )

        # --- 4. Handle overpayment → retailer credit ---------------
        if excess > Decimal("0.00"):
            PaymentService._handle_overpayment(
                sale=sale,
                payment=payment,
                excess=excess,
                recorded_by=recorded_by,
            )

        # --- 5. Update Sale financials + payment status ------------
        PaymentService._update_sale_financials(sale, applied_amount)

        return payment

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_amount(amount):
        """Raise if the payment amount is not positive."""
        if amount <= Decimal("0.00"):
            raise ValidationError("Payment amount must be greater than zero.")

    @staticmethod
    def _create_payment(*, sale, amount, payment_date, payment_method, notes, recorded_by):
        """Persist a Payment record for the full amount received."""
        return Payment.objects.create(
            sale=sale,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            note=notes,
            recorded_by=recorded_by,
            tenant=recorded_by.tenant,
        )

    @staticmethod
    def _handle_overpayment(*, sale, payment, excess, recorded_by):
        """
        Create a RetailerCredit for the overpaid portion and
        increase the retailer's credit balance.
        """
        RetailerCredit.objects.create(
            retailer=sale.retailer,
            payment=payment,
            sale=sale,
            amount=excess,
            reason=RetailerCredit.Reason.OVERPAYMENT,
            note=f"Overpayment on invoice {sale.invoice_number}",
            created_by=recorded_by,
            tenant=recorded_by.tenant,
        )
        sale.retailer.credit_balance += excess
        sale.retailer.save(update_fields=["credit_balance"])

    @staticmethod
    def _update_sale_financials(sale, applied_amount):
        """
        Add the applied portion to amount_paid, recalculate
        amount_due, and derive the payment status.

        Must be called inside an existing @transaction.atomic block.
        """
        sale.amount_paid += applied_amount
        sale.amount_due = sale.total_amount - sale.amount_paid

        # Derive payment status
        if sale.amount_paid >= sale.total_amount:
            sale.status = Sale.Status.PAID
        elif sale.amount_paid > Decimal("0.00"):
            sale.status = Sale.Status.PARTIAL
        else:
            sale.status = Sale.Status.UNPAID

        sale.save(update_fields=["amount_paid", "amount_due", "status"])
