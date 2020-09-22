# -*- coding: utf-8 -*-
{
    'name'     : 'Module Odoo 11 pour Weeefund',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
Module Odoo 11 pour Weeefund
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'account_bank_statement_import',
        "mass_mailing",
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/view_account_bank_statement_import.xml',
        'views/mailing_contact_views.xml',
    ],
    'installable': True,
    'application': True,
}
