# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FamilyMassEdit(models.TransientModel):
    _inherit = 'clv.family.mass_edit'

    ref_address_is_unavailable = fields.Boolean(
        string='Address is unavailable'
    )
    ref_address_is_unavailable_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Address is unavailable:', default=False, readonly=False, required=False
    )

    ref_address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address'
    )
    ref_address_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Address:', default=False, readonly=False, required=False
    )

    get_ref_address_data = fields.Boolean(
        string='Get Reference Address Data'
    )

    verification_marker_ids = fields.Many2many(
        comodel_name='clv.verification.marker',
        relation='clv_family_mass_edit_verification_marker_rel',
        column1='family_id',
        column2='verification_marker_id',
        string='Verification Markers'
    )
    verification_marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Verification Markers:', default=False, readonly=False, required=False
    )

    family_verification_exec = fields.Boolean(
        string='Family Verification Execute'
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        value = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_family_verification_exec'),
            ('enabled', '=', True),
        ]).value
        family_verification_exec = False
        if value == 'True':
            family_verification_exec = True

        defaults['family_verification_exec'] = family_verification_exec

        return defaults

    def do_family_mass_edit(self):
        self.ensure_one()

        super().do_family_mass_edit()

        for family in self.family_ids:

            _logger.info(u'%s %s', '>>>>>', family.name)

            if self.ref_address_is_unavailable_selection == 'set':
                family.ref_address_is_unavailable = self.ref_address_is_unavailable
            if self.ref_address_is_unavailable_selection == 'remove':
                family.ref_address_is_unavailable = False

            if self.ref_address_id_selection == 'set':
                family.ref_address_id = self.ref_address_id.id
            if self.ref_address_id_selection == 'remove':
                family.ref_address_id = False

            if self.get_ref_address_data:
                family.do_family_get_ref_address_data()

            if self.verification_marker_ids_selection == 'add':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'set':
                m2m_list = []
                for verification_marker_id in family.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.verification_marker_ids = m2m_list
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.verification_marker_ids = m2m_list

            if self.family_verification_exec:
                family._family_verification_exec()

        return True
