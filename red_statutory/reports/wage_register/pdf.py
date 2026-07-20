import frappe

from red_statutory.utils.pdf import html_to_pdf
from red_statutory.reports.wage_register.query import get_data


TEMPLATE = "red_statutory/templates/registers/wage_register.html"


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
    filename = "WageRegister_{}.pdf".format(filters["from_date"])
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "content": pdf,
        "is_private": 1,
    }).insert(ignore_permissions=True)
    return file_doc.file_url
