# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientAuxReload(models.TransientModel):
    _description = 'Patient (Aux) Reload'
    _name = 'clv.patient_aux.reload'

    def _default_patient_aux_ids(self):
        return self._context.get('active_ids')
    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_reload_rel',
        string='Patients (Aux)',
        default=_default_patient_aux_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    patient_aux_verification_exec = fields.Boolean(
        string='Patient (Aux) Verification Execute',
        default=True,
    )

    def do_patient_aux_reload(self):
        self.ensure_one()

        for patient_aux in self.patient_aux_ids:

            _logger.info(u'%s %s', '>>>>>', patient_aux.name)

            if not patient_aux.related_patient_is_unavailable:

                related_patient = patient_aux.related_patient_id
                vals = {}

                if (patient_aux.phase_id.id != related_patient.phase_id.id):

                    vals['phase_id'] = related_patient.phase_id.id

                if (patient_aux.state != related_patient.state):

                    vals['state'] = related_patient.state

                if (related_patient.category_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for category_id in related_patient.category_ids:
                        m2m_list.append((4, category_id.id))
                        count += 1

                    if count > 0:
                        vals['category_ids'] = m2m_list

                if (patient_aux.name != related_patient.name):

                    vals['name'] = related_patient.name

                if (patient_aux.code != related_patient.code):

                    vals['code'] = related_patient.code

                if (patient_aux.is_absent != related_patient.is_absent):

                    vals['is_absent'] = related_patient.is_absent

                if (patient_aux.gender != related_patient.gender):

                    vals['gender'] = related_patient.gender

                if (patient_aux.birthday != related_patient.birthday):

                    vals['birthday'] = related_patient.birthday

                if (patient_aux.estimated_age != related_patient.estimated_age):

                    vals['estimated_age'] = related_patient.estimated_age

                if (patient_aux.date_death != related_patient.date_death):

                    vals['date_death'] = related_patient.date_death

                if (patient_aux.force_is_deceased != related_patient.force_is_deceased):

                    vals['force_is_deceased'] = related_patient.force_is_deceased

                if self.update_contact_info_data:

                    if (patient_aux.contact_info_is_unavailable != related_patient.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = related_patient.contact_info_is_unavailable

                    if (patient_aux.validate_contact_information != related_patient.validate_contact_information):

                        vals['validate_contact_information'] = related_patient.validate_contact_information

                    if (patient_aux.zip != related_patient.zip):

                        vals['zip'] = related_patient.zip

                    if (patient_aux.street_name != related_patient.street_name):

                        vals['street_name'] = related_patient.street_name

                    if (patient_aux.street_number != related_patient.street_number):

                        vals['street_number'] = related_patient.street_number

                    if (patient_aux.street_number2 != related_patient.street_number2):

                        vals['street_number2'] = related_patient.street_number2

                    if (patient_aux.street2 != related_patient.street2):

                        vals['street2'] = related_patient.street2

                    if (patient_aux.country_id != related_patient.country_id):

                        vals['country_id'] = related_patient.country_id.id

                    if (patient_aux.state_id != related_patient.state_id):

                        vals['state_id'] = related_patient.state_id.id

                    if (patient_aux.city_id != related_patient.city_id):

                        vals['city_id'] = related_patient.city_id.id

                    if (related_patient.phone is not False) and (patient_aux.phone != related_patient.phone):

                        vals['phone'] = related_patient.phone

                    if (related_patient.mobile is not False) and (patient_aux.mobile != related_patient.mobile):

                        vals['mobile'] = related_patient.mobile

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                patient_aux.write(vals)

            if self.patient_aux_verification_exec:
                patient_aux._patient_aux_verification_exec()

        return True
