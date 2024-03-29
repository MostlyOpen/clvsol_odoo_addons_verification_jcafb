# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Person (Aux) Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Person (Aux) Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.2',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_person_aux_jcafb',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/person_aux_verification.xml',
        'data/default_value.xml',
        'views/verification_outcome_view.xml',
        'wizard/person_aux_mass_edit_view.xml',
        'wizard/person_aux_verification_exec_view.xml',
        'wizard/person_aux_related_person_updt_view.xml',
        'wizard/person_aux_related_person_create_view.xml',
        'wizard/person_aux_family_updt_view.xml',
        'wizard/person_aux_reload_view.xml',
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
