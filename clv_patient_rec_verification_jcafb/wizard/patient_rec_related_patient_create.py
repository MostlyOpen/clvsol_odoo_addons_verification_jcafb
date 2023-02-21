# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientRecRelatePatientCreate(models.TransientModel):
    _description = 'Patient (Rec) Related Patient Create'
    _name = 'clv.patient_rec.related_patient_create'

    def _default_patient_rec_ids(self):
        return self._context.get('active_ids')
    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_related_patient_create_rel',
        string='Patients (Rec)',
        default=_default_patient_rec_ids
    )

    patient_rec_set_code = fields.Boolean(
        string='Patient (Rec) Set Code',
        default=True
    )

    related_patient_verification_exec = fields.Boolean(
        string='Related Patient Verification Execute',
        default=True,
    )

    patient_rec_verification_exec = fields.Boolean(
        string='Patient (Rec) Verification Execute',
        default=True,
    )

    def do_patient_rec_related_patient_create(self):
        self.ensure_one()

        Patient = self.env['clv.patient']

        for patient_rec in self.patient_rec_ids:

            _logger.info(u'%s %s', '>>>>>', patient_rec.name)

            if not patient_rec.related_patient_is_unavailable:

                if patient_rec.related_patient_id.id is False:

                    if self.patient_rec_set_code:
                        if patient_rec.code is False:
                            patient_rec._patient_rec_set_code()

                    patient = Patient.search([
                        ('name', '=', patient_rec.name),
                    ])

                    if patient.id is False:

                        vals = {}

                        if (patient_rec.code is not False):

                            vals['code'] = patient_rec.code

                        if (patient_rec.phase_id.id is not False):

                            vals['phase_id'] = patient_rec.phase_id.id

                        if (patient_rec.state is not False):

                            vals['state'] = patient_rec.state

                        if (patient_rec.name is not False):

                            vals['name'] = patient_rec.name

                        if (patient_rec.is_absent is not False):

                            vals['is_absent'] = patient_rec.is_absent

                        if (patient_rec.gender is not False):

                            vals['gender'] = patient_rec.gender

                        if (patient_rec.estimated_age is not False):

                            vals['estimated_age'] = patient_rec.estimated_age

                        if (patient_rec.birthday is not False):

                            vals['birthday'] = patient_rec.birthday

                        if (patient_rec.date_death is not False):

                            vals['date_death'] = patient_rec.date_death

                        if (patient_rec.force_is_deceased is not False):

                            vals['force_is_deceased'] = patient_rec.force_is_deceased

                        if (patient_rec.zip is not False):

                            vals['zip'] = patient_rec.zip

                        if (patient_rec.street_name is not False):

                            vals['street_name'] = patient_rec.street_name

                        if (patient_rec.street_number is not False):

                            vals['street_number'] = patient_rec.street_number

                        if (patient_rec.street_number2 is not False):

                            vals['street_number2'] = patient_rec.street_number2

                        if (patient_rec.street2 is not False):

                            vals['street2'] = patient_rec.street2

                        if (patient_rec.country_id.id is not False):

                            vals['country_id'] = patient_rec.country_id.id

                        if (patient_rec.state_id.id is not False):

                            vals['state_id'] = patient_rec.state_id.id

                        if (patient_rec.city_id.id is not False):

                            vals['city_id'] = patient_rec.city_id.id

                        if (patient_rec.phone is not False):

                            vals['phone'] = patient_rec.phone

                        if (patient_rec.mobile is not False):

                            vals['mobile'] = patient_rec.mobile

                        if (patient_rec.global_tag_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_rec.global_tag_ids:
                                m2m_list.append((4, global_tag_id.id))
                                count += 1

                            if count > 0:
                                vals['global_tag_ids'] = m2m_list

                        if (patient_rec.category_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_rec.category_ids:
                                m2m_list.append((4, global_tag_id.id))
                                count += 1

                            if count > 0:
                                vals['category_ids'] = m2m_list

                        if (patient_rec.marker_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_rec.marker_ids:
                                m2m_list.append((4, global_tag_id.id))
                                count += 1

                            if count > 0:
                                vals['marker_ids'] = m2m_list

                        if vals != {}:

                            vals['reg_state'] = 'revised'

                            _logger.info(u'%s %s %s', '>>>>>>>>>>', 'vals:', vals)
                            new_related_patient = Patient.create(vals)

                            values = {}
                            values['related_patient_id'] = new_related_patient.id
                            patient_rec.write(values)

                    else:

                        values = {}
                        values['related_patient_id'] = patient.id
                        patient_rec.write(values)

            if self.related_patient_verification_exec:
                if patient_rec.related_patient_id.id is not False:
                    patient_rec.related_patient_id._patient_verification_exec()

            if self.patient_rec_verification_exec:
                patient_rec._patient_rec_verification_exec()

        return True
