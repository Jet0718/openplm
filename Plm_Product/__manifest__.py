{
    'name': 'cn_plm_product',
    'description': 'plm_product',
    'author': 'ebert',
    'version': '1.0',
    'category': 'Uncategorized',
    'website': 'http://www.example.com',
    'depends': ['base','mrp'],
    'data': [
        'views/product_templates.xml',
        'views/mrp_bom_views.xml',
        'data/prodcut_sequence.xml',
        'data/prodbom_sequence.xml',        
        'security/ir.model.access.csv',       

    ],
    'application': True,
}