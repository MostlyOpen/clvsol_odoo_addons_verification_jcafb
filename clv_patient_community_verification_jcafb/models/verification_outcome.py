# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import models, _

_logger = logging.getLogger(__name__)


class VerificationOutcome(models.Model):
    _inherit = 'clv.verification.outcome'

    def _person_verification_patient(self, verification_outcome, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_verification = datetime.now()

        state = 'Ok'
        outcome_info = ''

        patient_ids = model_object.patient_ids

        if model_object.is_patient:

            if len(patient_ids) == 0:
                outcome_info = _('Missing related "Patient" register.')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

            if len(patient_ids) > 1:
                outcome_info = _('There are more than one related "Patient" register.')
                state = self._get_verification_outcome_state(state, 'Error (L0)')

        else:

            if len(patient_ids) != 0:

                outcome_info = _('"Related Patient" should not be set.\n')
                state = self._get_verification_outcome_state(state, 'Error (L1)')

        if outcome_info == '':
            outcome_info = False

        self._object_verification_outcome_updt(
            verification_outcome, state, outcome_info, date_verification, model_object
        )

        verification_values = {}
        verification_values['date_verification'] = date_verification
        verification_values['outcome_info'] = outcome_info
        verification_values['state'] = state
        verification_outcome.write(verification_values)


class VerificationOutcome_2(models.Model):
    _inherit = 'clv.verification.outcome'

    def _patient_verification_related_person(self, verification_outcome, model_object):

        _logger.warning(u'%s %s',
                        '>>>>>>>>>>>>>>> "_patient_verification_related_person" was not processed for', model_object.name)

        date_verification = datetime.now()

        state = 'Ok'
        outcome_info = ''

        if outcome_info == '':
            outcome_info = False

        self._object_verification_outcome_updt(
            verification_outcome, state, outcome_info, date_verification, model_object
        )
