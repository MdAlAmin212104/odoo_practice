from odoo import api, fields, models


class EmployeeLeaveBalance(models.Model):
    _name = "employee.leave.balance"
    _description = "Leave Balance"
    _order = "employee_id, leave_type_id"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        ondelete="cascade",
    )
    leave_type_id = fields.Many2one(
        "employee.leave.type",
        string="Leave Type",
        required=True,
        ondelete="restrict",
    )
    total_days = fields.Float(string="Total Days", default=0.0)
    used_days = fields.Float(string="Used Days", default=0.0)
    remaining_days = fields.Float(
        string="Remaining Days",
        compute="_compute_remaining_days",
        store=True,
    )
    year = fields.Integer(string="Year", required=True, default=fields.Date.today().year)

    _sql_constraints = [
        (
            "leave_balance_unique",
            "unique(employee_id, leave_type_id, year)",
            "Each employee can have only one leave balance per leave type and year.",
        )
    ]

    @api.depends("total_days", "used_days")
    def _compute_remaining_days(self):
        for record in self:
            record.remaining_days = record.total_days - record.used_days
