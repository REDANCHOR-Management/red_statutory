import calendar
from datetime import date

import frappe


def get_salary_slips(internal_client_code, month, year):
    """
    Reads all submitted Salary Slips for a client/month and
    returns normalized data for Document Engine.

    Returns:
        [
            {
                employee,
                employee_name,
                company,
                department,
                designation,
                branch,
                posting_date,
                salary_slip,
                payment_days,
                working_days,
                earnings: {},
                deductions: {},
                gross_pay,
                total_deduction,
                net_pay
            }
        ]
    """

    month = int(month)
    year = int(year)

    from_date = date(year, month, 1)
    to_date = date(year, month, calendar.monthrange(year, month)[1])

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "docstatus": 1,
            "posting_date": ["between", [from_date, to_date]],
            "custom_internal_client_code": internal_client_code,
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "company",
            "department",
            "designation",
            "branch",
            "posting_date",
            "payment_days",
            "total_working_days",
            "gross_pay",
            "total_deduction",
            "net_pay",
        ],
        order_by="employee_name asc",
    )

    result = []

    for row in salary_slips:

        slip = frappe.get_doc("Salary Slip", row.name)

        earnings = {}

        for item in slip.earnings:
            earnings[item.salary_component] = float(item.amount or 0)

        deductions = {}

        for item in slip.deductions:
            deductions[item.salary_component] = float(item.amount or 0)

        result.append(
            {
                "salary_slip": row.name,
                "employee": row.employee,
                "employee_name": row.employee_name,
                "company": row.company,
                "department": row.department,
                "designation": row.designation,
                "branch": row.branch,
                "posting_date": row.posting_date,
                "payment_days": row.payment_days,
                "working_days": row.total_working_days,
                "gross_pay": float(row.gross_pay or 0),
                "total_deduction": float(row.total_deduction or 0),
                "net_pay": float(row.net_pay or 0),
                "earnings": earnings,
                "deductions": deductions,
            }
        )

    return result