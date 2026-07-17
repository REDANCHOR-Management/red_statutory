import frappe
from frappe.utils.pdf import get_pdf


class PDFGenerator:
    """
    RED Statutory
    PDF Generator

    Responsibilities
    ----------------
    • Convert HTML to PDF
    • Return PDF bytes

    No ERP queries.
    No business logic.
    """

    @staticmethod
    def generate_pdf(html):
        """
        Convert HTML into PDF.
        """
        return get_pdf(html)

    @staticmethod
    def download_pdf(html, filename):
        """
        Return PDF as downloadable response.
        """
        pdf = get_pdf(html)

        frappe.local.response.filename = filename
        frappe.local.response.filecontent = pdf
        frappe.local.response.type = "pdf"

        return pdf
