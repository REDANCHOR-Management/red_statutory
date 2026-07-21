import frappe
from frappe.utils.pdf import get_pdf

from red_statutory.red_statutory.reports.wage_register.query import (
    get_wage_register_context,
)
from red_statutory.red_statutory.utils.pdf import LANDSCAPE_A4_OPTIONS


@frappe.whitelist()
def download_wage_register(internal_client_code, month, year):
    context = get_wage_register_context(
        internal_client_code=internal_client_code,
        month=month,
        year=year,
    )

    html = frappe.render_template(
        "red_statutory/templates/registers/wage_register.html",
        context,
    )

    frappe.local.response.filename = (
        f"Wage Register - {context['month']} {context['year']}.pdf"
    )

    frappe.local.response.filecontent = get_pdf(
        html,
        options=LANDSCAPE_A4_OPTIONS,
    )

    frappe.local.response.type = "download"