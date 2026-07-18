import frappe
from red_statutory.utils.document_engine import generate_wage_register


@frappe.whitelist()
def generate_wage_register_api(internal_client_code, month, year):
    return generate_wage_register(
        internal_client_code,
        month,
        year
    )