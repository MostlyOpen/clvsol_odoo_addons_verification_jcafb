# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PatientAuxStreetPatternAdd(models.TransientModel):
    _description = 'Patient (Aux) Street Pattern Add'
    _name = 'clv.patient_aux.street_pattern_add'

    def _default_patient_aux_ids(self):
        return self._context.get('active_ids')
    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_street_pattern_add_rel',
        string='Patients (Aux)',
        default=_default_patient_aux_ids)
    count_patients_aux = fields.Integer(
        string='Number of Patients (Aux)',
        compute='_compute_count_patients_aux',
        store=False
    )

    patient_aux_verification_exec = fields.Boolean(
        string='Patient (Aux) Verification Execute',
        default=True,
    )

    @api.depends('patient_aux_ids')
    def _compute_count_patients_aux(self):
        for r in self:
            r.count_patients_aux = len(r.patient_aux_ids)

    def do_patient_aux_street_pattern_add(self):
        self.ensure_one()

        PartnerEntityStreetPattern = self.env['clv.partner_entity.street_pattern']

        for patient_aux in self.patient_aux_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (patient_aux):', patient_aux.name)

            street_patern = PartnerEntityStreetPattern.search([
                ('street', '=', patient_aux.street_name),
                ('street2', '=', patient_aux.street2),
            ])

            if street_patern.street is False:

                values = {}
                values['street'] = patient_aux.street_name
                values['street2'] = patient_aux.street2
                values['active'] = True
                PartnerEntityStreetPattern.create(values)

            if self.patient_aux_verification_exec:
                patient_aux._patient_aux_verification_exec()

        return True
