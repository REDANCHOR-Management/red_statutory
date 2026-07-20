from frappe.utils.pdf import get_pdf


def html_to_pdf(html):
    """
    Convert HTML to PDF.
    """

    options = {
        "page-size": "A4",
        "orientation": "Landscape",
        "margin-top": "8mm",
        "margin-bottom": "8mm",
        "margin-left": "8mm",
        "margin-right": "8mm",
        "encoding": "UTF-8",
        "print-media-type": "",
        "disable-smart-shrinking": ""
    }

    return get_pdf(html, options)