from odoo import fields, models


class EmployeeLeaveType(models.Model):
    _name = "employee.leave.type"
    _description = "Leave Type"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    max_days = fields.Float(string="Maximum Days", default=0.0)
    requires_manager_approval = fields.Boolean(string="Requires Manager Approval", default=True)
    requires_hr_approval = fields.Boolean(string="Requires HR Approval", default=True)
    paid = fields.Boolean(string="Paid", default=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    leave_request_ids = fields.One2many(
        "employee.leave.request",
        "leave_type_id",
        string="Leave Requests",
    )

    _sql_constraints = [
        (
            "leave_type_code_unique",
            "unique(code)",
            "Leave type code must be unique.",
        )
    ]
