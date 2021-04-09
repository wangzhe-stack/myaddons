# -*- coding: utf-8 -*-
{
    'name': "geo",

    'summary': """
        陕西省地勘基金项目管理信息系统
    """,

    'description': """
        陕西省地勘基金项目管理信息系统
    """,

    'author': "fanglei",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_views.xml',
        'views/regulations_views.xml',
        'views/system_manage_views.xml',
        'views/system_setting_views.xml',
        'views/project_views.xml',
        'views/project_manage_views.xml',
        'views/project_change_views.xml',
        'views/attachment_manage_views.xml',
        'views/monthly_report_views.xml',
        'views/monthly_synthesize_fill.xml',
        'views/monthly_prospecting_fill.xml',
        'views/actions.xml',
        'views/menus.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/data.xml',
    ],
    'qweb': [
            "static/src/xml/*.xml",
    ],
}
