# -*- coding: utf-8 -*-
{
    'name': "Food Orders",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': "Food company that accepts indoor and delivery orders",

    'author': "Tasty Company",
    'website': "https://www.tastycompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Order',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale'],

    # always loaded
    # take care of the order of the files!!, u can't call a wizard if it is included after its caller
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'wizard/add_external.xml',
        'wizard/add_feedback_rejection_reason.xml',
        'views/order_meal.xml',
        'views/meal_category.xml',
        'views/meal_ingredient.xml',
        'views/order.xml',
        'views/order_item.xml',
        'views/order_tag.xml',
        'views/customer_feedback.xml',
        'views/external_item.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml',
        'report/order_report.xml',
        'data/server_action.xml',
        'data/scheduled_action.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
