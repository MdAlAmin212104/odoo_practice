from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EmployeeLeaveRequest(models.Model):
    _name = "employee.leave.request"
    _description = "Leave Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_date desc, id desc"

    name = fields.Char(string="Request Number", required=True, copy=False, readonly=True, default="/")
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        tracking=True,
        ondelete="restrict",
    )
    user_id = fields.Many2one(
        "res.users",
        string="User",
        related="employee_id.user_id",
        readonly=True,
        store=True,
    )
    department_id = fields.Many2one(
        "hr.department",
        string="Department",
        related="employee_id.department_id",
        readonly=True,
        store=True,
        tracking=True,
    )
    manager_id = fields.Many2one(
        "hr.employee",
        string="Manager",
        related="employee_id.manager_id",
        readonly=True,
        store=True,
        tracking=True,
    )
    leave_type_id = fields.Many2one(
        "employee.leave.type",
        string="Leave Type",
        required=True,
        tracking=True,
        ondelete="restrict",
    )
    start_date = fields.Date(string="Start Date", required=True, tracking=True)
    end_date = fields.Date(string="End Date", required=True, tracking=True)
    number_of_days = fields.Float(
        string="Number of Days",
        compute="_compute_number_of_days",
        store=True,
        tracking=True,
    )
    reason = fields.Text(string="Reason")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("manager_approved", "Manager Approved"),
            ("hr_approved", "HR Approved"),
            ("rejected", "Rejected"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )
    manager_comment = fields.Text(string="Manager Comment")
    hr_comment = fields.Text(string="HR Comment")
    create_date = fields.Datetime(string="Created Date", readonly=True)
    approved_date = fields.Datetime(string="Approved Date", readonly=True)
    rejected_date = fields.Datetime(string="Rejected Date", readonly=True)
    remaining_leave_balance = fields.Float(
        string="Remaining Leave Balance",
        compute="_compute_remaining_leave_balance",
        store=False,
    )
    employee_active = fields.Boolean(
        related="employee_id.active",
        string="Employee Active",
        readonly=True,
        store=False,
    )

    @api.depends("start_date", "end_date")
    def _compute_number_of_days(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    record.number_of_days = 0.0
                    continue
                delta = record.end_date - record.start_date
                record.number_of_days = delta.days + 1
            else:
                record.number_of_days = 0.0

    @api.depends("employee_id", "leave_type_id")
    def _compute_remaining_leave_balance(self):
        for record in self:
            if not record.employee_id or not record.leave_type_id:
                record.remaining_leave_balance = 0.0
                continue
            balance = self.env["employee.leave.balance"].search([
                ("employee_id", "=", record.employee_id.id),
                ("leave_type_id", "=", record.leave_type_id.id),
                ("year", "=", fields.Date.today().year),
            ], limit=1)
            record.remaining_leave_balance = balance.remaining_days if balance else 0.0

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id
            self.manager_id = self.employee_id.manager_id

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if not record.start_date:
                raise ValidationError("Start date is required.")
            if record.end_date < record.start_date:
                raise ValidationError("End date cannot be before the start date.")

    @api.constrains("employee_id")
    def _check_employee_active(self):
        for record in self:
            if record.employee_id and not record.employee_id.active:
                raise ValidationError("Employee must be active to request leave.")

    @api.constrains("employee_id", "leave_type_id", "start_date", "end_date")
    def _check_leave_balance(self):
        for record in self:
            if not record.employee_id or not record.leave_type_id:
                continue
            if record.state in ["draft", "cancelled"]:
                continue
            balance = self.env["employee.leave.balance"].search([
                ("employee_id", "=", record.employee_id.id),
                ("leave_type_id", "=", record.leave_type_id.id),
                ("year", "=", fields.Date.today().year),
            ], limit=1)
            if not balance:
                raise ValidationError("No leave balance found for this employee and leave type.")
            if record.number_of_days > balance.remaining_days:
                raise ValidationError("Leave days cannot exceed the available leave balance.")

    @api.constrains("employee_id", "start_date", "end_date")
    def _check_overlapping_leave(self):
        for record in self:
            if not record.employee_id or not record.start_date or not record.end_date:
                continue
            overlapping = self.search([
                ("id", "!=", record.id),
                ("employee_id", "=", record.employee_id.id),
                ("state", "in", ["submitted", "manager_approved", "hr_approved"]),
                ("start_date", "<=", record.end_date),
                ("end_date", ">=", record.start_date),
            ])
            if overlapping:
                raise ValidationError("The employee already has an overlapping approved or submitted leave request.")

    @api.model
    def create(self, vals):
        if vals.get("name", "/") == "/":
            vals["name"] = self.env["ir.sequence"].next_by_code("employee.leave.request") or "/"
        return super().create(vals)

    def action_submit(self):
        for record in self:
            record.state = "submitted"
            if record.employee_id.work_email:
                record._send_email_template("leave_submission_email_template")

    def action_manager_approve(self):
        for record in self:
            record.state = "manager_approved"
            record.approved_date = fields.Datetime.now()
            if record.employee_id.work_email:
                record._send_email_template("leave_manager_approved_email_template")

    def action_hr_approve(self):
        for record in self:
            record.state = "hr_approved"
            record.approved_date = fields.Datetime.now()
            if record.employee_id.work_email:
                record._send_email_template("leave_hr_approved_email_template")
            self._update_leave_balance(record)

    def action_reject(self, rejection_reason=False):
        for record in self:
            record.state = "rejected"
            record.rejected_date = fields.Datetime.now()
            if rejection_reason:
                record.manager_comment = rejection_reason
            if record.employee_id.work_email:
                record._send_email_template("leave_rejected_email_template")

    def action_cancel(self):
        for record in self:
            record.state = "cancelled"

    def action_reset_to_draft(self):
        for record in self:
            record.state = "draft"

    def _update_leave_balance(self, leave_request):
        balance = self.env["employee.leave.balance"].search([
            ("employee_id", "=", leave_request.employee_id.id),
            ("leave_type_id", "=", leave_request.leave_type_id.id),
            ("year", "=", fields.Date.today().year),
        ], limit=1)
        if not balance:
            balance = self.env["employee.leave.balance"].create({
                "employee_id": leave_request.employee_id.id,
                "leave_type_id": leave_request.leave_type_id.id,
                "year": fields.Date.today().year,
                "total_days": 20,
                "used_days": 0,
            })
        balance.used_days += leave_request.number_of_days

    def _send_email_template(self, template_xml_id):
        template = self.env.ref(template_xml_id, raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

    def _cron_close_expired_requests(self):
        domain = [
            ("state", "in", ["submitted", "manager_approved"]),
            ("end_date", "<", fields.Date.today()),
        ]
        for record in self.search(domain):
            record.state = "hr_approved" if record.leave_type_id.requires_hr_approval else "manager_approved"

    def unlink(self):
        for record in self:
            if record.state not in ("draft", "cancelled"):
                raise ValidationError("Only draft or cancelled requests can be deleted.")
        return super().unlink()
