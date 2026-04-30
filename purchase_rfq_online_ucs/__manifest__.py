# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Uncanny Consulting Services LLP
#    Copyright (C) 2023 Uncanny Consulting Services LLP (<https://uncannycs.com>).
#
##############################################################################
{
    'name': 'Odoo Vendor Portal: Sign Purchase RFQ Online UCS',
    'version': '18.0.0.0.1',
    'category': 'Tools',
    "price": 70,
    "currency": "USD",
    'summary': 'You send your RFQ to your vendor. They preview it, they input the prices and sign online!',
    "author": "Uncanny Consulting Services LLP",
    "maintainers": "Uncanny Consulting Services LLP",
    "website": "https://uncannycs.com",
    'description': """It is used to manage company service 
    """,
    'depends':['base','purchase','portal','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_rfq_views.xml',
        'views/portal_rfq_template.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
            'https://fonts.googleapis.com/css?family=Cedarville+Cursive',
            'https://cdn.jsdelivr.net/npm/signature_pad@4.0.0/dist/signature_pad.umd.min.js',
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
        ],
    },
    'installable': True,
    'application':False,
    'license': 'LGPL-3',
}
