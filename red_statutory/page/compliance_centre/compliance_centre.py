import calendar
from datetime import date

import frappe


MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


@frappe.whitelist()
def generate(register, month, year, internal_client_code):

    year = int(year)
    month_no = MONTHS.get(month)

    if not month_no:
        frappe.throw("Invalid Month")

    from_date = date(year, month_no, 1)

    to_date = date(
        year,
        month_no,
        calendar.monthrange(year, month_no)[1]
    )

    filters = {
        "month": month,
        "year": year,
        "from_date": from_date.strftime("%Y-%m-%d"),
        "to_date": to_date.strftime("%Y-%m-%d"),
        "internal_client_code": internal_client_code
    }

    if register == "Wage Register":
        from red_statutory.registers.wage_register.pdf import generate
        return generate(filters)

    frappe.throw(f"Unsupported Register : {register}")