# red_statutory/utils/salary_slip_reader.py

import frappe
from frappe import _


class SalarySlipReader:
    """
    RED Statutory

    Salary Slip Reader

    Responsibilities
    ----------------
    • Read submitted Salary Slips.
    • Read Employee metadata.
    • Read Customer metadata.
    • Read dynamic Earnings.
    • Read dynamic Deductions.

    This module MUST NOT:

    - Generate HTML
    - Generate PDF
    - Perform payroll calculations
    - Hardcode salary components
    """

    COMPANY_PF_CODE = "GJAHD2437699000"
    COMPANY_ESIC_CODE = "37001255260000999"

    @staticmethod
    def get_salary_slips(internal_client_code, month, year):
        """
        Returns all submitted salary slips
        for the selected Internal Client Code,
        Posting Month and Posting Year.
        """

        salary_slips = frappe.get_all(
            "Salary Slip",
            filters={
                "docstatus": 1,
                "custom_internal_client_code": internal_client_code,
                "month": month,
                "year": year,
            },
            fields=["name"],
            order_by="employee asc",
        )

        return [
            SalarySlipReader.get_salary_slip(slip.name)
            for slip in salary_slips
        ]

    @staticmethod
    def get_salary_slip(salary_slip_name):
        """
        Returns one complete Salary Slip object.
        """

        ss = frappe.get_doc("Salary Slip", salary_slip_name)

        employee = frappe.get_doc("Employee", ss.employee)

        customer = frappe.db.get_value(
            "Customer",
            {
                "custom_internal_client_code": ss.custom_internal_client_code
            },
            ["name", "primary_address"],
            as_dict=True,
        )

        return {

            # ----------------------------------------------------
            # Salary Slip
            # ----------------------------------------------------

            "salary_slip": {

                "name": ss.name,
                "employee": ss.employee,
                "employee_name": ss.employee_name,
                "designation": ss.designation,

                "company": ss.company,

                "internal_client_code": ss.custom_internal_client_code,

                "posting_date": ss.posting_date,
                "start_date": ss.start_date,
                "end_date": ss.end_date,

                "working_days": ss.total_working_days,
                "payment_days": ss.payment_days,
                "leave_without_pay": ss.leave_without_pay,

                "gross_pay": ss.gross_pay,
                "total_deduction": ss.total_deduction,
                "net_pay": ss.net_pay,
            },

            # ----------------------------------------------------
            # Employee
            # ----------------------------------------------------

            "employee": {

                "employee": employee.name,

                "employee_name": employee.employee_name,

                "uan": employee.custom_uan,

                "esic_number": employee.custom_statutory_esic_number,

                "pf_number": employee.provident_fund_account,

                "aadhaar": employee.custom_aadhar_number,

                "pan": employee.pan_number,

                "bank_account": employee.bank_ac_no,

                "ifsc": employee.ifsc_code,
            },

            # ----------------------------------------------------
            # Customer
            # ----------------------------------------------------

            "customer": {

                "name": customer.name if customer else None,

                "principal_employer_address":
                    customer.primary_address if customer else None,
            },

            # ----------------------------------------------------
            # Company
            # ----------------------------------------------------

            "company": {

                "name": ss.company,

                "pf_code": SalarySlipReader.COMPANY_PF_CODE,

                "esic_code": SalarySlipReader.COMPANY_ESIC_CODE,
            },

            # ----------------------------------------------------
            # Earnings (Dynamic)
            # ----------------------------------------------------

            "earnings": [

                {
                    "salary_component": row.salary_component,
                    "amount": row.amount,
                    "default_amount": row.default_amount,
                }

                for row in ss.earnings

            ],

            # ----------------------------------------------------
            # Deductions (Dynamic)
            # ----------------------------------------------------

            "deductions": [

                {
                    "salary_component": row.salary_component,
                    "amount": row.amount,
                    "default_amount": row.default_amount,
                }

                for row in ss.deductions

            ],
        }
