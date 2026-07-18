import frappe

from red_statutory.utils.salary_slip_reader import get_salary_slips
from red_statutory.utils.document_engine import build_wage_register


@frappe.whitelist()
def generate_wage_register(internal_client_code, month, year):
    """
    Compliance Centre API

    Input:
        internal_client_code
        month
        year

    Output:
        Generic Wage Register JSON
    """

    if not internal_client_code:
        frappe.throw("Internal Client Code is required.")

    if not month:
        frappe.throw("Month is required.")

    if not year:
        frappe.throw("Year is required.")

    salary_slips = get_salary_slips(
        internal_client_code=internal_client_code,
        month=month,
        year=year,
    )

    register = build_wage_register(salary_slips)

    return register