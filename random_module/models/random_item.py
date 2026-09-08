from odoo import fields, models


class RandomItem(models.Model):
    _name = "random.item"
    _description = "Random Item"
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    quantity = fields.Integer(string="Quantity", default=1)
    price = fields.Float(string="Price", default=0.0)
    is_active = fields.Boolean(string="Active", default=True)
    created_on = fields.Date(string="Created On", default=fields.Date.context_today)
