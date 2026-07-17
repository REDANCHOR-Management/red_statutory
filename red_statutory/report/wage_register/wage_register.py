import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}

	document = get_document(filters)
	columns = get_columns(document)
	data = get_data(document)

	return columns, data


def get_document(filters):
	internal_client_code = filters.get("internal_client_code")
	month = filters.get("month")
	year = filters.get("year")

	if not internal_client_code or not month or not year:
		return {
			"header": {},
			"earning_columns": [],
			"deduction_columns": [],
			"employees": [],
			"employee_count": 0,
		}

	from red_statutory.utils.document_engine import DocumentEngine

	return DocumentEngine.build_wage_register(
		internal_client_code=internal_client_code,
		month=int(month),
		year=int(year),
	)


def get_columns(document):
	columns = [
		{"label": _("Sr"), "fieldname": "sr", "fieldtype": "Int", "width": 40},
		{"label": _("Employee Details"), "fieldname": "employee_details", "fieldtype": "Data", "width": 220},
		{"label": _("Attendance"), "fieldname": "attendance", "fieldtype": "Data", "width": 110},
	]

	for col in document.get("earning_columns", []):
		columns.append({
			"label": col,
			"fieldname": frappe.scrub(col),
			"fieldtype": "Currency",
			"width": 110,
		})

	columns.extend([
		{"label": _("Gross Salary"), "fieldname": "gross_salary", "fieldtype": "Currency", "width": 110},
	])

	for col in document.get("deduction_columns", []):
		columns.append({
			"label": col,
			"fieldname": f"ded_{frappe.scrub(col)}",
			"fieldtype": "Currency",
			"width": 110,
		})

	columns.extend([
		{"label": _("Gross Deductions"), "fieldname": "gross_deductions", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Payable"), "fieldname": "net_payable", "fieldtype": "Currency", "width": 110},
		{"label": _("Signature"), "fieldname": "signature", "fieldtype": "Data", "width": 90},
	])

	return columns


def get_data(document):
	rows = []

	for idx, emp in enumerate(document.get("employees", []), start=1):
		salary_slip = emp.get("salary_slip", {})
		employee = emp.get("employee", {})
		customer = emp.get("customer", {})
		earnings = emp.get("earnings", {})
		deductions = emp.get("deductions", {})

		row = {
			"sr": idx,
			"employee_details": "\n".join([
				employee.get("employee_name") or salary_slip.get("employee_name") or "",
				salary_slip.get("employee") or employee.get("employee") or "",
				salary_slip.get("designation") or "",
				f"UAN : {employee.get('uan') or '-'}",
				f"ESIC : {employee.get('esic_number') or '-'}",
			]).strip(),
			"attendance": "\n".join([
				f"WD : {salary_slip.get('working_days') or 0}",
				f"PD : {salary_slip.get('payment_days') or 0}",
				f"LWP : {salary_slip.get('leave_without_pay') or 0}",
			]),
			"gross_salary": salary_slip.get("gross_pay") or 0,
			"gross_deductions": salary_slip.get("total_deduction") or 0,
			"net_payable": salary_slip.get("net_pay") or 0,
			"signature": "",
		}

		for col in document.get("earning_columns", []):
			row[frappe.scrub(col)] = earnings.get(col, 0) or 0

		for col in document.get("deduction_columns", []):
			row[f"ded_{frappe.scrub(col)}"] = deductions.get(col, 0) or 0

		rows.append(row)

	return rows
