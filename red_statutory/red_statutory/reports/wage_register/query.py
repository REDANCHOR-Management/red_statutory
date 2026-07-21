import calendar
from datetime import date

import frappe
from frappe import _
from frappe.utils import flt


WAGE_REGISTER_QUERY = """
SELECT
	ss.name AS salary_slip_id,
	ss.employee AS employee_id,
	ss.employee_name,
	ss.gross_pay AS gross_earnings,
	ss.total_deduction AS gross_deductions,
	ss.rounded_total AS net_payable,
	emp.designation,
	emp.custom_uan AS uan,
	emp.custom_statutory_esic_number AS esic_number,
	ss.total_working_days AS working_days,
	ss.payment_days,
	ss.leave_without_pay,
	cust.customer_name AS principal_employer_name,
	CONCAT_WS('\\n', NULLIF(addr.address_line1, ''), NULLIF(addr.address_line2, ''),
		CONCAT_WS(', ', NULLIF(addr.city, ''), NULLIF(addr.state, '')), NULLIF(addr.pincode, ''))
		AS principal_employer_address,
	earning.rate_basic, earning.rate_hra, earning.rate_other_allowance, earning.rate_conveyance,
	earning.rate_spl_allowance, earning.basic, earning.hra, earning.other_allowance,
	earning.conveyance, earning.bonus, earning.leaves, deduction.pf, deduction.esi,
	deduction.professional_tax, deduction.advance_deduction, deduction.loan_deduction,
	deduction.food_deduction, deduction.penalty, deduction.insurance, deduction.other_deduction
FROM `tabSalary Slip` ss
LEFT JOIN `tabEmployee` emp ON emp.name = ss.employee
LEFT JOIN `tabCustomer` cust ON cust.custom_documented_client_code = ss.custom_internal_client_code
LEFT JOIN `tabAddress` addr ON addr.name = (
	SELECT dl.parent FROM `tabDynamic Link` dl
	WHERE dl.link_doctype = 'Customer' AND dl.link_name = cust.name LIMIT 1
)
LEFT JOIN (
	SELECT parent,
		SUM(CASE WHEN abbr = 'BASIC' THEN default_amount ELSE 0 END) AS rate_basic,
		SUM(CASE WHEN abbr = 'HRA' THEN default_amount ELSE 0 END) AS rate_hra,
		SUM(CASE WHEN abbr = 'OTH' THEN default_amount ELSE 0 END) AS rate_other_allowance,
		SUM(CASE WHEN abbr = 'CONV' THEN default_amount ELSE 0 END) AS rate_conveyance,
		SUM(CASE WHEN abbr = 'SPL' THEN default_amount ELSE 0 END) AS rate_spl_allowance,
		SUM(CASE WHEN abbr = 'BASIC' THEN amount ELSE 0 END) AS basic,
		SUM(CASE WHEN abbr = 'HRA' THEN amount ELSE 0 END) AS hra,
		SUM(CASE WHEN abbr = 'OTH' THEN amount ELSE 0 END) AS other_allowance,
		SUM(CASE WHEN abbr = 'CONV' THEN amount ELSE 0 END) AS conveyance,
		SUM(CASE WHEN abbr = 'BONUS' THEN amount ELSE 0 END) AS bonus,
		SUM(CASE WHEN abbr = 'LEAVE' THEN amount ELSE 0 END) AS leaves
	FROM `tabSalary Detail` WHERE parentfield = 'earnings' GROUP BY parent
) earning ON earning.parent = ss.name
LEFT JOIN (
	SELECT parent,
		SUM(CASE WHEN abbr = 'PFEE' THEN amount ELSE 0 END) AS pf,
		SUM(CASE WHEN abbr = 'ESICEE' THEN amount ELSE 0 END) AS esi,
		SUM(CASE WHEN abbr = 'PT' THEN amount ELSE 0 END) AS professional_tax,
		SUM(CASE WHEN abbr = 'ADV' THEN amount ELSE 0 END) AS advance_deduction,
		SUM(CASE WHEN abbr = 'LOAN' THEN amount ELSE 0 END) AS loan_deduction,
		SUM(CASE WHEN abbr = 'FOODED' THEN amount ELSE 0 END) AS food_deduction,
		SUM(CASE WHEN abbr = 'PENALTY' THEN amount ELSE 0 END) AS penalty,
		SUM(CASE WHEN abbr = 'INSDED' THEN amount ELSE 0 END) AS insurance,
		SUM(CASE WHEN abbr IN ('MAND', 'UNIDED', 'TRNDED', 'ACCODED', 'DARR') THEN amount ELSE 0 END) AS other_deduction
	FROM `tabSalary Detail` WHERE parentfield = 'deductions' GROUP BY parent
) deduction ON deduction.parent = ss.name
WHERE ss.posting_date BETWEEN %(from_date)s AND %(to_date)s
	AND ss.custom_internal_client_code = %(internal_client_code)s
	AND ss.docstatus IN (0, 1)
ORDER BY ss.posting_date ASC, ss.employee_name ASC
"""

AMOUNT_FIELDS = (
	"gross_earnings", "gross_deductions", "net_payable", "rate_basic", "rate_hra",
	"rate_other_allowance", "rate_conveyance", "rate_spl_allowance", "basic", "hra",
	"other_allowance", "conveyance", "bonus", "leaves", "pf", "esi",
	"professional_tax", "advance_deduction", "loan_deduction", "food_deduction",
	"penalty", "insurance", "other_deduction",
)


def get_wage_register_context(internal_client_code, month, year):
	internal_client_code = (internal_client_code or "").strip()
	if not internal_client_code:
		frappe.throw(_("Internal Client Code is required."))
	from_date, to_date = get_wage_period(month, year)
	rows = frappe.db.sql(
		WAGE_REGISTER_QUERY,
		{"internal_client_code": internal_client_code, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)
	if not rows:
		frappe.throw(_("No Salary Slips found for the selected period and Internal Client Code."))
	for row in rows:
		for fieldname in AMOUNT_FIELDS:
			row[fieldname] = flt(row.get(fieldname))
		for fieldname in ("working_days", "payment_days", "leave_without_pay"):
			row[fieldname] = flt(row.get(fieldname))
	return {
		"rows": rows,
		"from_date": from_date.strftime("%d/%m/%Y"),
		"to_date": to_date.strftime("%d/%m/%Y"),
		"month": month,
		"year": year,
		"principal_employer_name": rows[0].principal_employer_name or "",
		"principal_employer_address_lines": (rows[0].principal_employer_address or "").splitlines(),
		"total_gross_earnings": sum(row.gross_earnings for row in rows),
		"total_gross_deductions": sum(row.gross_deductions for row in rows),
		"total_net_payable": sum(row.net_payable for row in rows),
	}


def get_wage_period(month, year):
	month_numbers = {name: number for number, name in enumerate(calendar.month_name) if name}
	if month not in month_numbers:
		frappe.throw(_("Select a valid month."))
	try:
		year_number = int(year)
	except (TypeError, ValueError):
		frappe.throw(_("Select a valid year."))
	if not 2000 <= year_number <= 2100:
		frappe.throw(_("Select a valid year."))
	month_number = month_numbers[month]
	return date(year_number, month_number, 1), date(
		year_number, month_number, calendar.monthrange(year_number, month_number)[1]
	)
