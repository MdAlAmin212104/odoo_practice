{
    'name': 'Practice Library', 
    'summary': 'Simple book collection for Odoo practice', 'version': '19.0.1.0.0', 
    'author': 'Learning Project', 
    'license': 'LGPL-3', 
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv', 
        'views/library_book_views.xml'
    ], 
    'application': True, 
    'installable': True
    
}
