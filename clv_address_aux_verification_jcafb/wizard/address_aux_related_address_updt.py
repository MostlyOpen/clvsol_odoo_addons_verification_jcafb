# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressAuxRelateAddressUpdt(models.TransientModel):
    _description = 'Address (Aux) Related Address Update'
    _name = 'clv.address_aux.related_address_updt'

    def _default_address_aux_ids(self):
        return self._context.get('active_ids')
    address_aux_ids = fields.Many2many(
        comodel_name='clv.address_aux',
        relation='clv_address_aux_related_address_updt_rel',
        string='Addresses (Aux)',
        default=_default_address_aux_ids
    )

    related_address_verification_exec = fields.Boolean(
        string='Related Address Verification Execute',
        default=True,
    )

    address_aux_verification_exec = fields.Boolean(
        string='Address (Aux) Verification Execute',
        default=True,
    )

    def do_address_aux_related_address_updt(self):
        self.ensure_one()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            if not address_aux.related_address_is_unavailable:

                related_address = address_aux.related_address_id
                vals = {}

                if (address_aux.phase_id != related_address.phase_id):

                    vals['phase_id'] = address_aux.phase_id.id

                if (address_aux.state != related_address.state):

                    vals['state'] = address_aux.state

                if (address_aux.zip != related_address.zip):

                    vals['zip'] = address_aux.zip

                if (address_aux.street_name != related_address.street_name):

                    vals['street_name'] = address_aux.street_name

                if (address_aux.street_number != related_address.street_number):

                    vals['street_number'] = address_aux.street_number

                if (address_aux.street_number2 != related_address.street_number2):

                    vals['street_number2'] = address_aux.street_number2

                if (address_aux.street2 != related_address.street2):

                    vals['street2'] = address_aux.street2

                if (address_aux.country_id != related_address.country_id):

                    vals['country_id'] = address_aux.country_id.id

                if (address_aux.state_id != related_address.state_id):

                    vals['state_id'] = address_aux.state_id.id

                if (address_aux.city_id != related_address.city_id):

                    vals['city_id'] = address_aux.city_id.id

                if (address_aux.phone is not False) and (address_aux.phone != related_address.phone):

                    vals['phone'] = address_aux.phone

                if (address_aux.mobile is not False) and (address_aux.mobile != related_address.mobile):

                    vals['mobile'] = address_aux.mobile

                if (address_aux.global_tag_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in address_aux.global_tag_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['global_tag_ids'] = m2m_list

                if (address_aux.category_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in address_aux.category_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['category_ids'] = m2m_list

                if (address_aux.marker_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for global_tag_id in address_aux.marker_ids:
                        m2m_list.append((4, global_tag_id.id))
                        count += 1

                    if count > 0:
                        vals['marker_ids'] = m2m_list

                if (address_aux.code != related_address.code):

                    vals['code'] = address_aux.code

                if vals != {}:

                    vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                related_address.write(vals)

            if self.related_address_verification_exec:
                if address_aux.related_address_id.id is not False:
                    address_aux.related_address_id._address_verification_exec()

            if self.address_aux_verification_exec:
                address_aux._address_aux_verification_exec()

        return True
