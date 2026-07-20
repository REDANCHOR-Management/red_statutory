import frappe

from red_statutory.utils.pdf import html_to_pdf
from red_statutory.registers.wage_register.query import get_data


TEMPLATE = "red_statutory/registers/wage_register/template.html"


@frappe.whitelist()
def generate(filters):

    if isinstance(filters, str):
        filters = frappe.parse_json(filters)

    context = get_data(filters)

    html = frappe.render_template(
        TEMPLATE,
        context
    )

    pdf = html_to_pdf(html)

    frappe.local.response.filename = (
        f"{filters['internal_client_code']}"
        f"_WageRegister_"
        f"{filters['from_date']}"
        ".pdf"
    )

    frappe.local.response.filecontent = pdf
    frappe.local.response.type = "download"

    return