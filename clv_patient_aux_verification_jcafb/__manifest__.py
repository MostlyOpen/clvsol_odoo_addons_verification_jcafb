# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient (Aux) Verification (for CLVhealth-JCAFB Solution)',
    'summary': 'Patient (Aux) Verification Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.1',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient_aux',
        'clv_verification',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_aux_verification.xml',
        'data/default_value.xml',
        'data/street_pattern_match.xml',
        'views/verification_outcome_view.xml',
        'wizard/patient_aux_mass_edit_view.xml',
        'wizard/patient_aux_verification_exec_view.xml',
        'wizard/patient_aux_related_patient_updt_view.xml',
        'wizard/patient_aux_related_patient_create_view.xml',
        'wizard/patient_aux_reload_view.xml',
        'wizard/patient_aux_street_pattern_add_view.xml',
        'wizard/patient_aux_contact_information_pattern_add_view.xml',
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
