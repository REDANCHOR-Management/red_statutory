"""
Wage Register Query
"""

import frappe
from collections import defaultdict


def get_data(filters):
    from_date = filters["from_date"]
    to_date = filters["to_date"]
    icc = filters["internal_client_code"]

    slips = frappe.get_all(
        "Salary Slip",
        filters={
            "docstatus": 1,
            "posting_date": ["between", [from_date, to_date]],
            "custom_internal_client_code": icc,
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "designation",
            "gross_pay",
            "total_deduction",
            "rounded_total",
            "total_working_days",
            "payment_days",
            "leave_without_pay",
            "custom_internal_client_code",
            "custom_uan as uan",
            "custom_statutory_esic_number as esic_number"
        ],
        order_by="posting_date asc, employee_name asc"
    )

    names = [d.name for d in slips]
    if not names:
        return {"register": {}, "rows": []}

    details = frappe.get_all(
        "Salary Detail",
        filters={"parent": ["in", names]},
        fields=[
            "parent",
            "parentfield",
            "abbr",
            "default_amount",
            "amount"
        ]
    )

    earnings = defaultdict(list)
    deductions = defaultdict(list)

    for d in details:
        if d.parentfield == "earnings":
            earnings[d.parent].append(d)
        else:
            deductions[d.parent].append(d)

    customer = frappe.db.get_value(
        "Customer",
        {"custom_documented_client_code": icc},
        ["name", "customer_name"],
        as_dict=True
    )

    address = ""
    if customer:
        address = frappe.db.sql("""
            SELECT CONCAT_WS(
                '\n',
                NULLIF(a.address_line1,''),
                NULLIF(a.address_line2,''),
                CONCAT_WS(', ',NULLIF(a.city,''),NULLIF(a.state,'')),
                NULLIF(a.pincode,'')
            )
            FROM `tabAddress` a
            JOIN `tabDynamic Link` dl
                ON dl.parent=a.name
            WHERE dl.link_doctype='Customer'
              AND dl.link_name=%s
            LIMIT 1
        """, customer.name)
        address = address[0][0] if address else ""

    rows = []

    for s in slips:

        e = {i.abbr: i for i in earnings[s.name]}
        d = {i.abbr: i for i in deductions[s.name]}

        other_ded = sum(
            x.amount for x in deductions[s.name]
            if x.abbr in ("MAND","UNIDED","TRNDED","ACCODED","DARR")
        )

        rows.append({
            "employee": s.employee,
            "employee_name": s.employee_name,
            "designation": s.designation,
            "uan": s.uan,
            "esic_number": s.esic_number,
            "working_days": s.total_working_days,
            "payment_days": s.payment_days,
            "leave_without_pay": s.leave_without_pay,
            "rate_basic": e.get("BASIC",{}).default_amount if e.get("BASIC") else 0,
            "rate_hra": e.get("HRA",{}).default_amount if e.get("HRA") else 0,
            "rate_other": e.get("OTH",{}).default_amount if e.get("OTH") else 0,
            "rate_conveyance": e.get("CONV",{}).default_amount if e.get("CONV") else 0,
            "rate_special": e.get("SPL",{}).default_amount if e.get("SPL") else 0,
            "basic": e.get("BASIC",{}).amount if e.get("BASIC") else 0,
            "hra": e.get("HRA",{}).amount if e.get("HRA") else 0,
            "other": e.get("OTH",{}).amount if e.get("OTH") else 0,
            "conveyance": e.get("CONV",{}).amount if e.get("CONV") else 0,
            "bonus": e.get("BONUS",{}).amount if e.get("BONUS") else 0,
            "leave": e.get("LEAVE",{}).amount if e.get("LEAVE") else 0,
            "gross_salary": s.gross_pay,
            "pf": d.get("PFEE",{}).amount if d.get("PFEE") else 0,
            "esi": d.get("ESICEE",{}).amount if d.get("ESICEE") else 0,
            "pt": d.get("PT",{}).amount if d.get("PT") else 0,
            "advance": d.get("ADV",{}).amount if d.get("ADV") else 0,
            "loan": d.get("LOAN",{}).amount if d.get("LOAN") else 0,
            "food": d.get("FOODED",{}).amount if d.get("FOODED") else 0,
            "penalty": d.get("PENALTY",{}).amount if d.get("PENALTY") else 0,
            "insurance": d.get("INSDED",{}).amount if d.get("INSDED") else 0,
            "other_deduction": other_ded,
            "gross_deduction": s.total_deduction,
            "net_payable": s.rounded_total,
        })

    return {
        "register": {
            "contractor_name": "SUPERMADE VENTURES PRIVATE LIMITED",
            "contractor_address": "",
            "principal_employer_name": customer.customer_name if customer else "",
            "principal_employer_address": address,
            "from_date": from_date,
            "to_date": to_date,
            "internal_client_code": icc,
        },
        "rows": rows,
    }
