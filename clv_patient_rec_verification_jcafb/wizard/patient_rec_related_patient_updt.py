# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientRecRelatePatientUpdt(models.TransientModel):
    _description = 'Patient (Rec) Related Patient Update'
    _name = 'clv.patient_rec.related_patient_updt'

    def _default_patient_rec_ids(self):
        return self._context.get('active_ids')
    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_related_patient_updt_rel',
        string='Patients (Rec)',
        default=_default_patient_rec_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    related_patient_verification_exec = fields.Boolean(
        string='Related Patient Verification Execute',
        default=True,
    )

    patient_rec_verification_exec = fields.Boolean(
        string='Patient (Rec) Verification Execute',
        default=True,
    )

    def do_patient_rec_related_patient_updt(self):
        self.ensure_one()

        for patient_rec in self.patient_rec_ids:

            _logger.info(u'%s %s', '>>>>>', patient_rec.name)

            if not patient_rec.related_patient_is_unavailable:

                related_patient = patient_rec.related_patient_id
                vals = {}

                if (patient_rec.phase_id != related_patient.phase_id):

                    vals['phase_id'] = patient_rec.phase_id.id

                if (patient_rec.state != related_patient.state):

                    vals['state'] = patient_rec.state

                if (patient_rec.global_tag_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in patient_rec.global_tag_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['global_tag_ids'] = m2m_list

                if (patient_rec.category_ids != related_patient.category_ids):

                    m2m_list = []
                    for category_id in related_patient.category_ids:
                        m2m_list.append((3, category_id.id))
                    for category_id in patient_rec.category_ids:
                        m2m_list.append((4, category_id.id))
                    if m2m_list != []:
                        vals['category_ids'] = m2m_list

                if (patient_rec.marker_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in patient_rec.marker_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['marker_ids'] = m2m_list

                if (patient_rec.name != related_patient.name):

                    vals['name'] = patient_rec.name

                if (patient_rec.code != related_patient.code):

                    vals['code'] = patient_rec.code

                if (patient_rec.is_absent != related_patient.is_absent):

                    vals['is_absent'] = patient_rec.is_absent

                if (patient_rec.gender != related_patient.gender):

                    vals['gender'] = patient_rec.gender

                if (patient_rec.estimated_age != related_patient.estimated_age):

                    vals['estimated_age'] = patient_rec.estimated_age

                if (patient_rec.birthday != related_patient.birthday):

                    vals['birthday'] = patient_rec.birthday

                if (patient_rec.date_death != related_patient.date_death):

                    vals['date_death'] = patient_rec.date_death

                if (patient_rec.force_is_deceased != related_patient.force_is_deceased):

                    vals['force_is_deceased'] = patient_rec.force_is_deceased

                if self.update_contact_info_data:

                    if (patient_rec.contact_info_is_unavailable != related_patient.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = patient_rec.contact_info_is_unavailable

                    if (patient_rec.validate_contact_information != related_patient.validate_contact_information):

                        vals['validate_contact_information'] = patient_rec.validate_contact_information

                    if (patient_rec.zip != related_patient.zip):

                        vals['zip'] = patient_rec.zip

                    if (patient_rec.street_name != related_patient.street_name):

                        vals['street_name'] = patient_rec.street_name

                    if (patient_rec.street_number != related_patient.street_number):

                        vals['street_number'] = patient_rec.street_number

                    if (patient_rec.street_number2 != related_patient.street_number2):

                        vals['street_number2'] = patient_rec.street_number2

                    if (patient_rec.street2 != related_patient.street2):

                        vals['street2'] = patient_rec.street2

                    if (patient_rec.country_id != related_patient.country_id):

                        vals['country_id'] = patient_rec.country_id.id

                    if (patient_rec.state_id != related_patient.state_id):

                        vals['state_id'] = patient_rec.state_id.id

                    if (patient_rec.city_id != related_patient.city_id):

                        vals['city_id'] = patient_rec.city_id.id

                    if (patient_rec.phone is not False) and (patient_rec.phone != related_patient.phone):

                        vals['phone'] = patient_rec.phone

                    if (patient_rec.mobile is not False) and (patient_rec.mobile != related_patient.mobile):

                        vals['mobile'] = patient_rec.mobile

                if vals != {}:

                    vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                related_patient.write(vals)

            if self.related_patient_verification_exec:
                if patient_rec.related_patient_id.id is not False:
                    patient_rec.related_patient_id._patient_verification_exec()

            if self.patient_rec_verification_exec:
                patient_rec._patient_rec_verification_exec()

        return True
