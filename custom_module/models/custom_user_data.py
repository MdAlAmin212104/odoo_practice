from odoo import fields, models


class CustomUserData(models.Model):
    _name = "custom.user.data"
    _description = "Custom User Data"

    # name = fields.Char(string="Name", required=True)
    # email = fields.Char(string="Email")
    # age = fields.Char(string="Age")
    # gender = fields.Char(string="Gender")
    # address = fields.Char(string="Address")

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("recieved", "Offer Recieved"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    postcode = fields.Char(string="Postcode")

    def _default_date(self):
        return fields.Date.today()

    date_avilability = fields.Date(string="Available From", default=_default_date)
    expected_price = fields.Float(string="Expected Price")
    best_Offer = fields.Float(string="Best Offer")
    selling_price = fields.Float(string="Selling Price")
    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms")
    living_areas = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garden", default=False)
    garage_area = fields.Integer(string="Garage Area (sqm)")
    Total_area = fields.Integer(string="Total Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        required=True,
        default="north",
    )
    property_type = fields.Selection(
        [
            ("house", "House"),
            ("apartment", "Apartment"),
            ("villa", "Villa"),
            ("townhouse", "Townhouse"),
        ],
        required=True,
        default="house",
    )