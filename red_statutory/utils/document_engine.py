# red_statutory/utils/document_engine.py

from calendar import monthrange
from datetime import date

from .salary_slip_reader import SalarySlipReader


class DocumentEngine:
    """
    RED Statutory

    Document Engine

    Responsibilities
    ----------------
    • Read data from SalarySlipReader
    • Build document model
    • Discover dynamic earning columns
    • Discover dynamic deduction columns

    This module MUST NOT

    • Query ERP directly
    • Generate HTML
    • Generate PDF
    • Perform payroll calculations
    """

    @staticmethod
    def build_wage_register(internal_client_code, month, year):

        salary_slips = SalarySlipReader.get_salary_slips(
            internal_client_code=internal_client_code,
            month=month,
            year=year,
        )

        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])

        earning_columns = set()
        deduction_columns = set()

        employees = []

        for slip in salary_slips:

            earning_map = {}
            deduction_map = {}

            for earning in slip["earnings"]:
                component = earning["salary_component"]
                earning_columns.add(component)
                earning_map[component] = earning["amount"]

            for deduction in slip["deductions"]:
                component = deduction["salary_component"]
                deduction_columns.add(component)
                deduction_map[component] = deduction["amount"]

            employees.append({

                "salary_slip": slip["salary_slip"],

                "employee": slip["employee"],

                "customer": slip["customer"],

                "company": slip["company"],

                "earnings": earning_map,

                "deductions": deduction_map,

            })

        earning_columns = sorted(list(earning_columns))
        deduction_columns = sorted(list(deduction_columns))

        header = {}

        if salary_slips:

            first = salary_slips[0]

            header = {

                "company": first["company"]["name"],

                "pf_code": first["company"]["pf_code"],

                "esic_code": first["company"]["esic_code"],

                "principal_employer": first["customer"]["name"],

                "principal_employer_address":
                    first["customer"]["principal_employer_address"],

                "internal_client_code":
                    first["salary_slip"]["internal_client_code"],

                "period_from": first_day,

                "period_to": last_day,

            }

        return {

            "header": header,

            "earning_columns": earning_columns,

            "deduction_columns": deduction_columns,

            "employees": employees,

            "employee_count": len(employees),

        }
