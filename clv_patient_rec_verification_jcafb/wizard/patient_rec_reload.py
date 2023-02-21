# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientRecReload(models.TransientModel):
    _description = 'Patient (Rec) Reload'
    _name = 'clv.patient_rec.reload'

    def _default_patient_rec_ids(self):
        return self._context.get('active_ids')
    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_reload_rel',
        string='Patients (Rec)',
        default=_default_patient_rec_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    patient_rec_verification_exec = fields.Boolean(
        string='Patient (Rec) Verification Execute',
        default=True,
    )

    def do_patient_rec_reload(self):
        self.ensure_one()

        for patient_rec in self.patient_rec_ids:

            _logger.info(u'%s %s', '>>>>>', patient_rec.name)

            if not patient_rec.related_patient_is_unavailable:

                related_patient = patient_rec.related_patient_id
                vals = {}

                if (patient_rec.phase_id != related_patient.phase_id):

                    vals['phase_id'] = related_patient.phase_id.id

                if (patient_rec.state != related_patient.state):

                    vals['state'] = related_patient.state

                if (related_patient.category_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for category_id in related_patient.category_ids:
                        m2m_list.append((4, category_id.id))
                        count += 1

                    if count > 0:
                        vals['category_ids'] = m2m_list

                if (patient_rec.name != related_patient.name):

                    vals['name'] = related_patient.name

                if (patient_rec.code != related_patient.code):

                    vals['code'] = related_patient.code

                if (patient_rec.is_absent != related_patient.is_absent):

                    vals['is_absent'] = related_patient.is_absent

                if (patient_rec.gender != related_patient.gender):

                    vals['gender'] = related_patient.gender

                if (patient_rec.birthday != related_patient.birthday):

                    vals['birthday'] = related_patient.birthday

                if (patient_rec.date_death != related_patient.date_death):

                    vals['date_death'] = related_patient.date_death

                if (patient_rec.force_is_deceased != related_patient.force_is_deceased):

                    vals['force_is_deceased'] = related_patient.force_is_deceased

                if self.update_contact_info_data:

                    if (patient_rec.contact_info_is_unavailable != related_patient.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = related_patient.contact_info_is_unavailable

                    if (patient_rec.validate_contact_information != related_patient.validate_contact_information):

                        vals['validate_contact_information'] = related_patient.validate_contact_information

                    if (patient_rec.zip != related_patient.zip):

                        vals['zip'] = related_patient.zip

                    if (patient_rec.street_name != related_patient.street_name):

                        vals['street_name'] = related_patient.street_name

                    if (patient_rec.street_number != related_patient.street_number):

                        vals['street_number'] = related_patient.street_number

                    if (patient_rec.street_number2 != related_patient.street_number2):

                        vals['street_number2'] = related_patient.street_number2

                    if (patient_rec.street2 != related_patient.street2):

                        vals['street2'] = related_patient.street2

                    if (patient_rec.country_id != related_patient.country_id):

                        vals['country_id'] = related_patient.country_id.id

                    if (patient_rec.state_id != related_patient.state_id):

                        vals['state_id'] = related_patient.state_id.id

                    if (patient_rec.city_id != related_patient.city_id):

                        vals['city_id'] = related_patient.city_id.id

                    if (related_patient.phone is not False) and (patient_rec.phone != related_patient.phone):

                        vals['phone'] = related_patient.phone

                    if (related_patient.mobile is not False) and (patient_rec.mobile != related_patient.mobile):

                        vals['mobile'] = related_patient.mobile

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                patient_rec.write(vals)

            if self.patient_rec_verification_exec:
                patient_rec._patient_rec_verification_exec()

        return True
