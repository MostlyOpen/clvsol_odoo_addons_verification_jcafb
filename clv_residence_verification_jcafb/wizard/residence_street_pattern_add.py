# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ResidenceStreetPatternAdd(models.TransientModel):
    _description = 'Residence Street Pattern Add'
    _name = 'clv.residence.street_pattern_add'

    def _default_residence_ids(self):
        return self._context.get('active_ids')
    residence_ids = fields.Many2many(
        comodel_name='clv.residence',
        relation='clv_residence_street_pattern_add_rel',
        string='Residences',
        default=_default_residence_ids)
    count_residences = fields.Integer(
        string='Number of Residences',
        compute='_compute_count_residences',
        store=False
    )

    residence_verification_exec = fields.Boolean(
        string='Residence Verification Execute',
        default=True,
    )

    @api.depends('residence_ids')
    def _compute_count_residences(self):
        for r in self:
            r.count_residences = len(r.residence_ids)

    def do_residence_street_pattern_add(self):
        self.ensure_one()

        PartnerEntityStreetPattern = self.env['clv.partner_entity.street_pattern']

        for residence in self.residence_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (residence):', residence.name)

            street_patern = PartnerEntityStreetPattern.search([
                ('street', '=', residence.street_name),
                ('street2', '=', residence.street2),
            ])

            if street_patern.street is False:

                values = {}
                values['street'] = residence.street_name
                values['street2'] = residence.street2
                values['active'] = True
                PartnerEntityStreetPattern.create(values)

            if self.residence_verification_exec:
                residence._residence_verification_exec()

        return True