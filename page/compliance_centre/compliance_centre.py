import frappe


@frappe.whitelist()
def generate(register, filters=None):
    """
    Compliance Centre launcher.

    Receives:
        register
        filters

    Calls the selected register generator.

    Returns:
        PDF
    """

    if register == "Wage Register":
        from red_statutory.registers.wage_register.pdf import generate
        return generate(filters)

    frappe.throw("Unsupported Register")