from collections import OrderedDict


def build_wage_register(salary_slips):
    """
    Converts Salary Slip Reader output into a generic
    Wage Register structure.
    """

    earning_components = OrderedDict()
    deduction_components = OrderedDict()

    # -------------------------------------------------------
    # Discover every earning & deduction component dynamically
    # -------------------------------------------------------

    for slip in salary_slips:

        for component in slip["earnings"]:
            earning_components[component] = True

        for component in slip["deductions"]:
            deduction_components[component] = True

    earning_component_names = list(earning_components.keys())
    deduction_component_names = list(deduction_components.keys())

    # Build component objects for HTML

    earning_components = [
        {
            "key": component,
            "label": component
        }
        for component in earning_component_names
    ]

    deduction_components = [
        {
            "key": component,
            "label": component
        }
        for component in deduction_component_names
    ]

    rows = []

    totals = {
        "earnings": {c: 0 for c in earning_component_names},
        "deductions": {c: 0 for c in deduction_component_names},
        "gross_earnings": 0,
        "gross_deductions": 0,
        "net_payable": 0,
    }

    # -------------------------------------------------------
    # Build Employee Rows
    # -------------------------------------------------------

    for sr, slip in enumerate(salary_slips, start=1):

        row = {
            "sr_no": sr,
            "employee_id": slip["employee"],
            "employee_name": slip["employee_name"],
            "designation": slip["designation"],
            "company": slip["company"],
            "department": slip["department"],
            "branch": slip["branch"],
            "posting_date": slip["posting_date"],
            "working_days": slip["working_days"],
            "payment_days": slip["payment_days"],
            "earnings": {},
            "deductions": {},
            "gross_earnings": slip["gross_pay"],
            "gross_deductions": slip["total_deduction"],
            "net_payable": slip["net_pay"],
        }

        # Earnings

        for component in earning_component_names:

            amount = slip["earnings"].get(component, 0)

            row["earnings"][component] = amount

            totals["earnings"][component] += amount

        # Deductions

        for component in deduction_component_names:

            amount = slip["deductions"].get(component, 0)

            row["deductions"][component] = amount

            totals["deductions"][component] += amount

        totals["gross_earnings"] += slip["gross_pay"]
        totals["gross_deductions"] += slip["total_deduction"]
        totals["net_payable"] += slip["net_pay"]

        rows.append(row)

    return {
        "earning_components": earning_components,
        "deduction_components": deduction_components,
        "rows": rows,
        "totals": totals,
    }