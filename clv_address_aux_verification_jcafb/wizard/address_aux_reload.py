# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressAuxReload(models.TransientModel):
    _description = 'Address (Aux) Reload'
    _name = 'clv.address_aux.reload'

    def _default_address_aux_ids(self):
        return self._context.get('active_ids')
    address_aux_ids = fields.Many2many(
        comodel_name='clv.address_aux',
        relation='clv_address_aux_reload_rel',
        string='Addresses (Aux)',
        default=_default_address_aux_ids
    )

    address_aux_verification_exec = fields.Boolean(
        string='Address (Aux) Verification Execute',
        default=True,
    )

    def do_address_aux_reload(self):
        self.ensure_one()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            if not address_aux.related_address_is_unavailable:

                related_address = address_aux.related_address_id
                vals = {}

                if (address_aux.phase_id != related_address.phase_id):

                    vals['phase_id'] = related_address.phase_id.id

                if (address_aux.state != related_address.state):

                    vals['state'] = related_address.state

                if (address_aux.zip != related_address.zip):

                    vals['zip'] = related_address.zip

                if (address_aux.street_name != related_address.street_name):

                    vals['street_name'] = related_address.street_name

                if (address_aux.street_number != related_address.street_number):

                    vals['street_number'] = related_address.street_number

                if (address_aux.street_number2 != related_address.street_number2):

                    vals['street_number2'] = related_address.street_number2

                if (address_aux.street2 != related_address.street2):

                    vals['street2'] = related_address.street2

                if (address_aux.country_id != related_address.country_id):

                    vals['country_id'] = related_address.country_id.id

                if (address_aux.state_id != related_address.state_id):

                    vals['state_id'] = related_address.state_id.id

                if (address_aux.city_id != related_address.city_id):

                    vals['city_id'] = related_address.city_id.id

                if (related_address.phone is not False) and (address_aux.phone != related_address.phone):

                    vals['phone'] = related_address.phone

                if (related_address.mobile is not False) and (address_aux.mobile != related_address.mobile):

                    vals['mobile'] = related_address.mobile

                # if (related_address.global_tag_ids.id is not False):

                #     m2m_list = []
                #     count = 0
                #     for global_tag_id in related_address.global_tag_ids:
                #         m2m_list.append((4, global_tag_id.id))
                #         count += 1

                #     if count > 0:
                #         vals['global_tag_ids'] = m2m_list

                if (related_address.category_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for category_id in related_address.category_ids:
                        m2m_list.append((4, category_id.id))
                        count += 1

                    if count > 0:
                        vals['category_ids'] = m2m_list

                # if (related_address.marker_ids.id is not False):

                #     m2m_list = []
                #     count = 0
                #     for marker_id in related_address.marker_ids:
                #         m2m_list.append((4, marker_id.id))
                #         count += 1

                #     if count > 0:
                #         vals['marker_ids'] = m2m_list

                if (address_aux.code != related_address.code):

                    vals['code'] = related_address.code

                # if vals != {}:

                    vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                address_aux.write(vals)

            # if self.related_address_verification_exec:
            #     if address_aux.related_address_id.id is not False:
            #         address_aux.related_address_id._address_verification_exec()

            if self.address_aux_verification_exec:
                address_aux._address_aux_verification_exec()

        return True