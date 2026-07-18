from collections import OrderedDict


def build_wage_register(salary_slips):
    """
    Converts Salary Slip Reader output into a generic
    Wage Register structure.

    Input:
        List returned by salary_slip_reader.get_salary_slips()

    Output:
        {
            headers,
            earning_components,
            deduction_components,
            rows,
            totals
        }
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

    earning_components = list(earning_components.keys())
    deduction_components = list(deduction_components.keys())

    rows = []

    totals = {
        "earnings": {c: 0 for c in earning_components},
        "deductions": {c: 0 for c in deduction_components},
        "gross_pay": 0,
        "total_deduction": 0,
        "net_pay": 0,
    }

    # -------------------------------------------------------
    # Build Employee Rows
    # -------------------------------------------------------

    for sr, slip in enumerate(salary_slips, start=1):

        row = {
            "sr_no": sr,
            "employee": slip["employee"],
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
            "gross_pay": slip["gross_pay"],
            "total_deduction": slip["total_deduction"],
            "net_pay": slip["net_pay"],
        }

        # Earnings

        for component in earning_components:

            amount = slip["earnings"].get(component, 0)

            row["earnings"][component] = amount

            totals["earnings"][component] += amount

        # Deductions

        for component in deduction_components:

            amount = slip["deductions"].get(component, 0)

            row["deductions"][component] = amount

            totals["deductions"][component] += amount

        totals["gross_pay"] += slip["gross_pay"]
        totals["total_deduction"] += slip["total_deduction"]
        totals["net_pay"] += slip["net_pay"]

        rows.append(row)

    return {
        "earning_components": earning_components,
        "deduction_components": deduction_components,
        "rows": rows,
        "totals": totals,
    }