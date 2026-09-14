from odoo import fields, models


class CustomUserData(models.Model):
    _name = "custom.user.data"
    _description = "Custom User Data"

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    age = fields.Char(string="Age")
    gender = fields.Char(string="Gender")
    address = fields.Char(string="Address")