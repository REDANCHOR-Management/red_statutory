"""Data provider for the fixed statutory Wage Register."""

from collections import defaultdict
from datetime import datetime

import frappe


CONTRACTOR_NAME = "SUPERMADE VENTURES PRIVATE LIMITED"
CONTRACTOR_ADDRESS = "D/619, Swati Clover, Shilaj Circle,\nThaltej, Ahmedabad, Gujarat - 380058"
OTHER_DEDUCTION_ABBRS = ("MAND", "UNIDED", "TRNDED", "ACCODED", "DARR")


def _amount(details, abbr, field):
    return sum(flt(detail.get(field)) for detail in details if detail.abbr == abbr)


def _format_money(value):
    value = flt(value)
    whole, decimal = f"{value:.2f}".split(".")
    sign = "-" if whole.startswith("-") else ""
    whole = whole.lstrip("-")
    if len(whole) > 3:
        tail = whole[-3:]
        head = whole[:-3]
        groups = []
        while head:
            groups.append(head[-2:])
            head = head[:-2]
        whole = ",".join(reversed(groups)) + "," + tail
    return f"{sign}{whole}.{decimal}"


def _format_date(value):
    return datetime.strptime(str(value), "%Y-%m-%d").strftime("%d/%m/%Y")


def _get_customer(icc):
    customer = frappe.db.get_value(
        "Customer", {"custom_documented_client_code": icc}, ["name", "customer_name"], as_dict=True
    )
    if not customer:
        return None, ""
    address = frappe.db.sql(
        """
        SELECT CONCAT_WS('\n', NULLIF(a.address_line1, ''), NULLIF(a.address_line2, ''),
            CONCAT_WS(', ', NULLIF(a.city, ''), NULLIF(a.state, '')), NULLIF(a.pincode, ''))
        FROM `tabAddress` a
        INNER JOIN `tabDynamic Link` dl ON dl.parent = a.name
        WHERE dl.link_doctype = 'Customer' AND dl.link_name = %s
        LIMIT 1
        """,
        customer.name,
        as_list=True,
    )
    return customer, address[0][0] if address else ""


def get_data(filters):
    """Return only the fixed fields printed by the Wage Register."""
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    icc = filters.get("internal_client_code")
    slip_filters = {
        "docstatus": ["in", (0, 1)],
        "posting_date": ["between", (from_date, to_date)],
    }
    if icc:
        slip_filters["custom_internal_client_code"] = icc
    slips = frappe.get_all(
        "Salary Slip",
        filters=slip_filters,
        fields=[
            "name", "employee", "employee_name", "gross_pay", "total_deduction", "rounded_total",
            "total_working_days", "payment_days", "leave_without_pay",
        ],
        order_by="posting_date asc, employee_name asc",
    )
    customer, address = _get_customer(icc)
    if not slips:
        return _context(from_date, to_date, icc, customer, address, [])

    employees = frappe.get_all(
        "Employee",
        filters={"name": ["in", [slip.employee for slip in slips]]},
        fields=["name", "designation", "custom_uan", "custom_statutory_esic_number"],
    )
    employee_by_name = {employee.name: employee for employee in employees}
    details_by_slip = defaultdict(lambda: {"earnings": [], "deductions": []})
    for detail in frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", [slip.name for slip in slips]]},
        fields=["parent", "parentfield", "abbr", "default_amount", "amount"],
    ):
        if detail.parentfield in details_by_slip[detail.parent]:
            details_by_slip[detail.parent][detail.parentfield].append(detail)

    rows = []
    for slip in slips:
        employee = employee_by_name.get(slip.employee, {})
        earnings = details_by_slip[slip.name]["earnings"]
        deductions = details_by_slip[slip.name]["deductions"]
        rows.append({
            "employee": slip.employee, "employee_name": slip.employee_name, "designation": employee.get("designation", ""),
            "uan": employee.get("custom_uan", ""), "esic_number": employee.get("custom_statutory_esic_number", ""),
            "working_days": slip.total_working_days, "payment_days": slip.payment_days, "leave_without_pay": slip.leave_without_pay,
            "rate_basic": _amount(earnings, "BASIC", "default_amount"), "rate_hra": _amount(earnings, "HRA", "default_amount"),
            "rate_other_allowance": _amount(earnings, "OTH", "default_amount"), "rate_conveyance": _amount(earnings, "CONV", "default_amount"), "rate_spl_allowance": _amount(earnings, "SPL", "default_amount"),
            "basic": _amount(earnings, "BASIC", "amount"), "hra": _amount(earnings, "HRA", "amount"),
            "other_allowance": _amount(earnings, "OTH", "amount"), "conveyance": _amount(earnings, "CONV", "amount"),
            "bonus": _amount(earnings, "BONUS", "amount"), "leaves": _amount(earnings, "LEAVE", "amount"),
            "gross_earnings": slip.gross_pay, "pf": _amount(deductions, "PFEE", "amount"), "esi": _amount(deductions, "ESICEE", "amount"),
            "professional_tax": _amount(deductions, "PT", "amount"), "advance_deduction": _amount(deductions, "ADV", "amount"),
            "loan_deduction": _amount(deductions, "LOAN", "amount"), "food_deduction": _amount(deductions, "FOODED", "amount"),
            "penalty": _amount(deductions, "PENALTY", "amount"), "insurance": _amount(deductions, "INSDED", "amount"),
            "other_deduction": sum(flt(detail.amount) for detail in deductions if detail.abbr in OTHER_DEDUCTION_ABBRS),
            "gross_deductions": slip.total_deduction, "net_payable": slip.rounded_total,
        })
    return _context(from_date, to_date, icc, customer, address, rows)


def _context(from_date, to_date, icc, customer, address, rows):
    return {
        "register": {"contractor_name": CONTRACTOR_NAME, "contractor_address": CONTRACTOR_ADDRESS,
                     "principal_employer_name": customer.customer_name if customer else "",
                     "principal_employer_address": address, "from_date": from_date, "to_date": to_date,
                     "internal_client_code": icc},
        "rows": rows, "money": _format_money, "display_date": _format_date,
    }


def flt(value):
    return frappe.utils.flt(value or 0)
