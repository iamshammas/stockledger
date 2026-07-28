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
    def record_payment(*, sale, amount, payment_date, notes="", recorded_by):
        """
        Record a payment against an existing Sale.

        Validates the amount, creates a Payment record, and
        updates the Sale's financial fields + payment status.

        If the payment exceeds the remaining amount due, only the
        due portion is applied to the Sale and the excess is stored
        as a RetailerCredit (reason=OVERPAYMENT).
        """

        # --- 1. Validate payment amount ------------------------------
        if amount <= Decimal("0.00"):
            raise ValidationError("Payment amount must be greater than zero.")

        # --- 2. Calculate remaining due & split ----------------------
        remaining_due = sale.amount_due
        applied_amount = min(amount, remaining_due)
        excess = amount - applied_amount

        # --- 3. Create Payment record (always stores full amount) ----
        payment = Payment.objects.create(
            tenant=sale.tenant,
            sale=sale,
            amount=amount,
            payment_date=payment_date,
            note=notes,
            recorded_by=recorded_by,
        )

        # --- 4. Create RetailerCredit for overpayment ----------------
        if excess > Decimal("0.00"):
            RetailerCredit.objects.create(
                tenant=sale.tenant,
                retailer=sale.retailer,
                payment=payment,
                sale=sale,
                amount=excess,
                reason=RetailerCredit.Reason.OVERPAYMENT,
                note=f"Overpayment on invoice {sale.invoice_number}",
                created_by=recorded_by,
            )
            sale.retailer.credit_balance += excess
            sale.retailer.save(update_fields=["credit_balance"])

        # --- 5. Update Sale financial fields -------------------------
        sale.amount_paid += applied_amount
        sale.amount_due = sale.total_amount - sale.amount_paid

        # --- 6. Derive payment status --------------------------------
        if sale.amount_paid >= sale.total_amount:
            sale.status = Sale.Status.PAID
        elif sale.amount_paid > Decimal("0.00"):
            sale.status = Sale.Status.PARTIAL
        else:
            sale.status = Sale.Status.UNPAID

        sale.save(update_fields=["amount_paid", "amount_due", "status"])

        return payment
