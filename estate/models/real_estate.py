from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text()
    address = fields.Char()
    expected_price = fields.Float(string="Expected Price", required=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    garden = fields.Boolean()
    date_available = fields.Date(default=fields.Date.context_today)
    state = fields.Selection(
        [
            ("new", "New"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )
