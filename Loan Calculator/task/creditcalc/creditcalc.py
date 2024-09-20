"""Loan calculator"""

import argparse
import math
import sys

ERROR_MSG = "Incorrect parameters."

parser = argparse.ArgumentParser(description="Calculates loan parameters.")

parser.add_argument("--type", type=str, help="indicates the type of payment")
parser.add_argument(
    "--payment", type=int, help="The monthly payment amount(annuity payment)"
)
parser.add_argument(
    "--principal", type=int, help="The amount of money borrowed in a loan"
)
parser.add_argument("--periods", type=int, help="")
parser.add_argument("--interest", type=float, help="It must always be provided!")

# Parse the command-line arguments
args = parser.parse_args()
arg_dict = vars(args)
# print(arg_dict)

# Access the arguments
payments_type = args.type  # indicates the type of payment
payment_value = args.payment  # The monthly payment amount(annuity payment)
principal_value = args.principal  # The amount of money borrowed in a loan
periods_value = args.periods  # The number of months needed to repay the loan
interest_value = args.interest  # It must always be provided!


def calculate_periods(payment_val, principal_val, interest_val):
    """Calculates periods of years and months to repay the loan"""
    nominal_interest_rate = interest_val / (12 * 100)
    denominator = payment_val - nominal_interest_rate * principal_val
    if denominator <= 0:
        print(
            "The payment is too low to cover the interest. Please increase your payment."
        )
        sys.exit()
    number_months = math.log(payment_val / denominator) / math.log(
        1 + nominal_interest_rate
    )
    years, months_left = divmod(math.ceil(number_months), 12)
    s = "s" if years > 1 else ""
    years_count = f"{years} year{s}" if years else ""
    m = f"and {months_left} months " if months_left > 0 else ""
    overpayment = round(payment_val * math.ceil(number_months) - principal_val)
    return print(
        f"It will take {years_count}{m} to repay this loan!\nOverpayment = {overpayment}"
    )


def calculate_monthly_payment(principal_val, periods_val, interest_val):
    """Calculates the monthly payment to repay the loan"""
    interest = (interest_val / 100) / 12
    numerator = interest * (1 + interest) ** periods_val
    denominator = (1 + interest) ** periods_val - 1
    monthly_payment = principal_val * (numerator / denominator)
    annuity_payment = math.ceil(monthly_payment)
    overpayment = annuity_payment * periods_val - principal_val
    return print(
        f"Your annuity payment = {annuity_payment}!\nOverpayment = {overpayment}"
    )


def calculate_principal(payment_val, periods_val, interest_val):
    """Calculates the loan principal"""
    interest = (interest_val / 100) / 12
    numerator = interest * (1 + interest) ** periods_val
    denominator = (1 + interest) ** periods_val - 1
    loan_principal = math.floor(payment_val / (numerator / denominator))
    overpayment = round(payment_val * periods_val - loan_principal)
    return print(
        f"Your loan principal = {loan_principal}!\nOverpayment = {overpayment}"
    )


def calculate_differentiated_payment(principal_val, num_payments, interest_val):
    """Calculate differentiated payment of the loan"""
    interest_val /= 12 * 100
    payments = []
    for m in range(1, num_payments + 1):
        base_payment = principal_val / num_payments
        interest_portion = interest_val * (
            principal_val - (principal_val * (m - 1)) / num_payments
        )
        payment = base_payment + interest_portion
        payments.append(math.ceil(payment))
    overpayment = sum(payments) - principal_val
    month = 0
    for month, payment in enumerate(payments, 1):
        print(f"Month {month}: payment is {payment}")
        month += 1
    print(f"\nOverpayment = {overpayment}")


def main():
    """Main function that orchestrates the flow of the script"""

    # python creditcalc.py --type=diff --principal=-1000000 --periods=10 --interest=10
    # python creditcalc.py --type=diff --principal=1000000 --periods=-10 --interest=10
    for value in arg_dict.values():
        if value is not None and not isinstance(value, str) and int(value) < 1:
            print(ERROR_MSG)
            sys.exit()

    # python creditcalc.py --type=diff --principal=1000000 --payment=104000
    if sum(1 for value in arg_dict.values() if value) < 4:
        print(ERROR_MSG)

    # python creditcalc.py --type=diff --principal=1000000 --periods=10 --interest=10
    elif payments_type == "diff" and payment_value is None:
        calculate_differentiated_payment(principal_value, periods_value, interest_value)

    # python creditcalc.py --type=annuity --principal=1000000 --periods=60 --interest=10
    elif payments_type == "annuity" and payment_value is None:
        calculate_monthly_payment(principal_value, periods_value, interest_value)

    # python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6
    # python creditcalc.py --type=annuity --payment=6898 --periods=240 --interest=3.4
    elif payments_type == "annuity" and principal_value is None:
        calculate_principal(payment_value, periods_value, interest_value)

    # python creditcalc.py --type=annuity --principal=500000 --payment=23000 --interest=7.8
    elif payments_type == "annuity" and periods_value is None:
        calculate_periods(payment_value, principal_value, interest_value)
    else:
        print(ERROR_MSG)


# Entry point to run the script
if __name__ == "__main__":
    main()
