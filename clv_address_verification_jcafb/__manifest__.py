# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Address Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Address Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_address',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/address_verification.xml',
        'views/verification_outcome_view.xml',
        'wizard/address_mass_edit_view.xml',
        'wizard/address_verification_exec_view.xml',
        'wizard/address_street_pattern_add_view.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
