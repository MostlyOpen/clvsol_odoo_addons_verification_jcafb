# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientAuxRelatePatientCreate(models.TransientModel):
    _description = 'Patient (Aux) Related Patient Create'
    _name = 'clv.patient_aux.related_patient_create'

    def _default_patient_aux_ids(self):
        return self._context.get('active_ids')
    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_related_patient_create_rel',
        string='Patients (Aux)',
        default=_default_patient_aux_ids
    )

    patient_aux_set_code = fields.Boolean(
        string='Patient (Aux) Set Code',
        default=True
    )

    related_patient_verification_exec = fields.Boolean(
        string='Related Patient Verification Execute',
        default=True,
    )

    patient_aux_verification_exec = fields.Boolean(
        string='Patient (Aux) Verification Execute',
        default=True,
    )

    def do_patient_aux_related_patient_create(self):
        self.ensure_one()

        Patient = self.env['clv.patient']

        for patient_aux in self.patient_aux_ids:

            _logger.info(u'%s %s', '>>>>>', patient_aux.name)

            if not patient_aux.related_patient_is_unavailable:

                if patient_aux.related_patient_id.id is False:

                    if self.patient_aux_set_code:
                        if patient_aux.code is False:
                            patient_aux._patient_aux_set_code()

                    patient = Patient.search([
                        ('name', '=', patient_aux.name),
                    ])

                    if patient.id is False:

                        vals = {}

                        if (patient_aux.code is not False):

                            vals['code'] = patient_aux.code

                        if (patient_aux.phase_id.id is not False):

                            vals['phase_id'] = patient_aux.phase_id.id

                        if (patient_aux.state is not False):

                            vals['state'] = patient_aux.state

                        if (patient_aux.name is not False):

                            vals['name'] = patient_aux.name

                        if (patient_aux.is_absent is not False):

                            vals['is_absent'] = patient_aux.is_absent

                        if (patient_aux.gender is not False):

                            vals['gender'] = patient_aux.gender

                        if (patient_aux.estimated_age is not False):

                            vals['estimated_age'] = patient_aux.estimated_age

                        if (patient_aux.birthday is not False):

                            vals['birthday'] = patient_aux.birthday

                        if (patient_aux.date_death is not False):

                            vals['date_death'] = patient_aux.date_death

                        if (patient_aux.force_is_deceased is not False):

                            vals['force_is_deceased'] = patient_aux.force_is_deceased

                        if (patient_aux.zip is not False):

                            vals['zip'] = patient_aux.zip

                        if (patient_aux.street_name is not False):

                            vals['street_name'] = patient_aux.street_name

                        if (patient_aux.street_number is not False):

                            vals['street_number'] = patient_aux.street_number

                        if (patient_aux.street_number2 is not False):

                            vals['street_number2'] = patient_aux.street_number2

                        if (patient_aux.street2 is not False):

                            vals['street2'] = patient_aux.street2

                        if (patient_aux.country_id.id is not False):

                            vals['country_id'] = patient_aux.country_id.id

                        if (patient_aux.state_id.id is not False):

                            vals['state_id'] = patient_aux.state_id.id

                        if (patient_aux.city_id.id is not False):

                            vals['city_id'] = patient_aux.city_id.id

                        if (patient_aux.phone is not False):

                            vals['phone'] = patient_aux.phone

                        if (patient_aux.mobile is not False):

                            vals['mobile'] = patient_aux.mobile

                        if (patient_aux.global_tag_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_aux.global_tag_ids:
                                m2m_list.append((4, global_tag_id.id))
                                count += 1

                            if count > 0:
                                vals['global_tag_ids'] = m2m_list

                        if (patient_aux.category_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_aux.category_ids:
                                m2m_list.append((4, global_tag_id.id))
                                count += 1

                            if count > 0:
                                vals['category_ids'] = m2m_list

                        if (patient_aux.marker_ids.id is not False):

                            m2m_list = []
                            count = 0
                            for global_tag_id in patient_aux.marker_ids:
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
                            patient_aux.write(values)

                    else:

                        values = {}
                        values['related_patient_id'] = patient.id
                        patient_aux.write(values)

            if self.related_patient_verification_exec:
                if patient_aux.related_patient_id.id is not False:
                    patient_aux.related_patient_id._patient_verification_exec()

            if self.patient_aux_verification_exec:
                patient_aux._patient_aux_verification_exec()

        return True
