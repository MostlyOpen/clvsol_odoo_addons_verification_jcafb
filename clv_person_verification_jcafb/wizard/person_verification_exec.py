# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PersonVerificationExecute(models.TransientModel):
    _description = 'Person Verification Execute'
    _name = 'clv.person.verification_exec'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_verification_outcome_refresh_rel',
        string='Persons',
        default=_default_person_ids)
    count_persons_aux = fields.Integer(
        string='Number of Persons',
        compute='_compute_count_persons_aux',
        store=False
    )

    @api.depends('person_ids')
    def _compute_count_persons_aux(self):
        for r in self:
            r.count_persons_aux = len(r.person_ids)

    def do_person_verification_exec(self):
        self.ensure_one()

        for person in self.person_ids:

            person._person_verification_exec()

        return True
