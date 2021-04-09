# -*- coding: utf-8 -*-
{
    'name': "inventory_apply",

    'summary': """
        物品申领""",

    'description': """
        物品申领
    """,

    'author': "My Company",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'demo/demo.xml',
        'data/sequence_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/inventory_views.xml',
        'views/base_data_tree_and_search.xml',
        'views/inventory_apply_views.xml',
        'views/actions.xml',
        'views/menus.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'post_init_hook': 'post_init_hook',
}