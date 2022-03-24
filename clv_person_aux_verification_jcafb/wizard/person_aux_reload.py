# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAuxReload(models.TransientModel):
    _description = 'Person (Aux) Reload'
    _name = 'clv.person_aux.reload'

    def _default_person_aux_ids(self):
        return self._context.get('active_ids')
    person_aux_ids = fields.Many2many(
        comodel_name='clv.person_aux',
        relation='clv_person_aux_reload_rel',
        string='Persons (Aux)',
        default=_default_person_aux_ids
    )

    update_contact_info_data = fields.Boolean(
        string='Update Contact Information Data',
        default=True,
        readonly=False
    )

    update_ref_address_data = fields.Boolean(
        string='Update Address Data',
        default=True,
        readonly=False
    )

    update_family_data = fields.Boolean(
        string='Update Family Data',
        default=True,
        readonly=False
    )

    # related_person_verification_exec = fields.Boolean(
    #     string='Related Person Verification Execute',
    #     default=True,
    # )

    person_aux_verification_exec = fields.Boolean(
        string='Person (Aux) Verification Execute',
        default=True,
    )

    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def do_person_aux_reload(self):
        self.ensure_one()

        for person_aux in self.person_aux_ids:

            _logger.info(u'%s %s', '>>>>>', person_aux.name)

            if not person_aux.related_person_is_unavailable:

                related_person = person_aux.related_person_id
                vals = {}

                if (person_aux.phase_id != related_person.phase_id):

                    vals['phase_id'] = related_person.phase_id.id

                if (person_aux.state != related_person.state):

                    vals['state'] = related_person.state

                # if (related_person.global_tag_ids.id is not False):

                #     m2m_list = []
                #     count = 0
                #     for global_tag_id in related_person.global_tag_ids:
                #         m2m_list.append((4, global_tag_id.id))
                #         count += 1

                #     if count > 0:
                #         vals['global_tag_ids'] = m2m_list

                if (related_person.category_ids.id is not False):

                    m2m_list = []
                    count = 0
                    for category_id in related_person.category_ids:
                        m2m_list.append((4, category_id.id))
                        count += 1

                    if count > 0:
                        vals['category_ids'] = m2m_list

                # if (related_person.marker_ids is not False):

                #     m2m_list = []
                #     count = 0
                #     for marker_id in related_person.marker_ids:
                #         m2m_list.append((4, marker_id.id))
                #         count += 1

                #     if count > 0:
                #         vals['marker_ids'] = m2m_list

                if (person_aux.name != related_person.name):

                    vals['name'] = related_person.name

                if (person_aux.code != related_person.code):

                    vals['code'] = related_person.code

                if (person_aux.is_absent != related_person.is_absent):

                    vals['is_absent'] = related_person.is_absent

                if (person_aux.gender != related_person.gender):

                    vals['gender'] = related_person.gender

                if (person_aux.birthday != related_person.birthday):

                    vals['birthday'] = related_person.birthday

                if (person_aux.date_death != related_person.date_death):

                    vals['date_death'] = related_person.date_death

                if (person_aux.force_is_deceased != related_person.force_is_deceased):

                    vals['force_is_deceased'] = related_person.force_is_deceased

                if self.update_contact_info_data:

                    if (person_aux.contact_info_is_unavailable != related_person.contact_info_is_unavailable):

                        vals['contact_info_is_unavailable'] = person_aux.contact_info_is_unavailable

                    if (person_aux.zip != related_person.zip):

                        vals['zip'] = person_aux.zip

                    if (person_aux.street_name != related_person.street_name):

                        vals['street_name'] = related_person.street_name

                    if (person_aux.street_number != related_person.street_number):

                        vals['street_number'] = related_person.street_number

                    if (person_aux.street_number2 != related_person.street_number2):

                        vals['street_number2'] = related_person.street_number2

                    if (person_aux.street2 != related_person.street2):

                        vals['street2'] = related_person.street2

                    if (person_aux.country_id != related_person.country_id):

                        vals['country_id'] = related_person.country_id.id

                    if (person_aux.state_id != related_person.state_id):

                        vals['state_id'] = related_person.state_id.id

                    if (person_aux.city_id != related_person.city_id):

                        vals['city_id'] = related_person.city_id.id

                    if (related_person.phone is not False) and (person_aux.phone != related_person.phone):

                        vals['phone'] = related_person.phone

                    if (related_person.mobile is not False) and (person_aux.mobile != related_person.mobile):

                        vals['mobile'] = related_person.mobile

                if self.update_ref_address_data:

                    if (person_aux.ref_address_is_unavailable != related_person.ref_address_is_unavailable):

                        vals['ref_address_is_unavailable'] = related_person.ref_address_is_unavailable

                    if (person_aux.ref_address_id != related_person.ref_address_id):

                        vals['ref_address_id'] = related_person.ref_address_id.id

                if self.update_family_data:

                    if (person_aux.family_is_unavailable != related_person.family_is_unavailable):

                        vals['family_is_unavailable'] = related_person.family_is_unavailable

                    if (person_aux.family_id != related_person.family_id):

                        vals['family_id'] = related_person.family_id.id

                # if vals != {}:

                #     vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                person_aux.write(vals)

            # if self.related_person_verification_exec:
            #     if person_aux.related_person_id.ref_address_id.id is not False:
            #         person_aux.related_person_id.ref_address_id._address_verification_exec()
            #     if person_aux.related_person_id.id is not False:
            #         person_aux.related_person_id._person_verification_exec()

            if self.person_aux_verification_exec:
                # if person_aux.ref_address_aux_id.id is not False:
                #     person_aux.ref_address_aux_id._address_aux_verification_exec()
                person_aux._person_aux_verification_exec()

        return True
