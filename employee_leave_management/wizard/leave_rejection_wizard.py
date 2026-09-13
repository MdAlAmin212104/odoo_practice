from odoo import fields, models


class EmployeeLeaveRejectionWizard(models.TransientModel):
    _name = "employee.leave.rejection.wizard"
    _description = "Leave Rejection Wizard"

    rejection_reason = fields.Text(string="Rejection Reason", required=True)

    def action_confirm_rejection(self):
        active_id = self.env.context.get("active_id")
        leave_request = self.env["employee.leave.request"].browse(active_id)
        if leave_request:
            leave_request.action_reject(self.rejection_reason)
        return {"type": "ir.actions.act_window_close"}
