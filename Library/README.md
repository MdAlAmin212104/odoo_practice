# Practice Library

Copy Library into server/addons. Restart Odoo, update the Apps List
in developer mode, then activate Practice Library.
Open Practice Library > Books > New to add a book.
Practice creating, reading, editing, and deleting a test book.

Files:
- models/library_book.py defines the fields.
- views/library_book_views.xml defines list/form views and menus.
- security/ir.model.access.csv grants internal users CRUD access.
- __manifest__.py lists dependencies and data files.
- __init__.py files import the models.

Exercises:
1. Change the Book Title label.
2. Add publisher = fields.Char() to the model and add it to the form.
3. Show date_added in the list view.

Restart Odoo after Python changes and upgrade the module after field/view changes.
Database table: practice_library_book.
