from odoo import fields, models


class LibraryBook(models.Model):
    _name = "practice.library.book"
    _description = "Library Book"
    _order = "id desc"

    name = fields.Char(string="Book Title", required=True)
    author = fields.Char(required=True)
    price = fields.Float()
    pages = fields.Integer()
    date_added = fields.Date(default=fields.Date.context_today)
    is_read = fields.Boolean(string="Finished Reading")
    notes = fields.Text()
