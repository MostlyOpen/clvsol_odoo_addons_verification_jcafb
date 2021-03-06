# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Family Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Family Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_family_jcafb',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/family_verification.xml',
        'data/default_value.xml',
        'views/verification_outcome_view.xml',
        'wizard/family_mass_edit_view.xml',
        'wizard/family_verification_exec_view.xml',
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
