# Odoo Practice

Two simple Odoo 19 addons for learning models, views, menus, and access rights.

- **estate**: manage properties, prices, bedrooms, and sale status.
- **Library** (Practice Library): manage books, authors, prices, and reading status.

## Install

1. Copy `estate` and `Library` into your Odoo custom addons directory, or add
   this repository directory to `addons_path` in your local Odoo configuration.
2. Restart Odoo.
3. Enable developer mode and open Apps > Update Apps List.
4. Find Real Estate and Practice Library, then activate them.
5. Open Real Estate > Properties or Practice Library > Books from the app menu.

## Practice

Create a record, open it, edit it, save it, refresh, then delete your test record.
Add a field in the Python model and display it in the XML form.
Restart Odoo after Python changes and upgrade the relevant module after
changing fields or views.

Database tables: `estate_property` and `practice_library_book`.
Keep database passwords and your local `odoo.conf` out of Git.
