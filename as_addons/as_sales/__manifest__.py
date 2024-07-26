# -*- coding: utf-8 -*-

{
    "name": "Sales by Alvins",
    "author": "Alvin Risman",
    'version': '14.0.1',
    'summary': """""",
    'description': """Sales Modules""",
    'category': '',
    'depends': [
    ],
    'data': [
        "security/sales_security.xml",
        "security/ir.model.access.csv",
        "data/sale_order_sequence.xml",
        "views/product_views.xml",
        "views/sale_views.xml",
        "views/spend_band_analysis.xml",
        "views/sales_menu_views.xml",
    ],
    "qweb": [
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
