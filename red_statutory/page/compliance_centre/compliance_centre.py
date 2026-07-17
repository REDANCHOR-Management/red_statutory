import frappe

from red_statutory.utils.document_engine import DocumentEngine


@frappe.whitelist()
def get_salary_slips(internal_client_code, month, year):

    return DocumentEngine.build_wage_register(
        internal_client_code=internal_client_code,
        month=int(month),
        year=int(year),
    )
