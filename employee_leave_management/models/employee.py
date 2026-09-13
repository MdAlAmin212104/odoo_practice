from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_code = fields.Char(
        string="Employee ID",
        required=False,
        copy=False,
        index=True,
        tracking=True,
    )
    job_position = fields.Char(string="Job Position")
    joining_date = fields.Date(string="Joining Date")
    manager_id = fields.Many2one(
        "hr.employee",
        string="Manager",
        tracking=True,
    )
    leave_request_ids = fields.One2many(
        "employee.leave.request",
        "employee_id",
        string="Leave Requests",
    )
    leave_balance_ids = fields.One2many(
        "employee.leave.balance",
        "employee_id",
        string="Leave Balances",
    )
    department_name = fields.Char(
        related="department_id.name",
        string="Department Name",
        readonly=True,
        store=False,
    )
    manager_name = fields.Char(
        related="manager_id.name",
        string="Manager Name",
        readonly=True,
        store=False,
    )

    _sql_constraints = [
        (
            "employee_code_uniq",
            "unique(employee_code)",
            "Employee ID must be unique.",
        )
    ]
