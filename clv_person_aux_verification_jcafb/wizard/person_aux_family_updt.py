# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonAuxFamilyUpdt(models.TransientModel):
    _description = 'Person (Aux) Family Update'
    _name = 'clv.person_aux.family_updt'

    def _default_person_aux_ids(self):
        return self._context.get('active_ids')
    person_aux_ids = fields.Many2many(
        comodel_name='clv.person_aux',
        relation='clv_person_aux_family_updt_rel',
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
        default=False,
        readonly=False
    )

    family_verification_exec = fields.Boolean(
        string='Family Verification Execute',
        default=True,
    )

    person_aux_verification_exec = fields.Boolean(
        string='Person (Aux) Verification Execute',
        default=True,
    )

    def do_person_aux_family_updt(self):
        self.ensure_one()

        for person_aux in self.person_aux_ids:

            _logger.info(u'%s %s', '>>>>>', person_aux.name)

            if not person_aux.family_is_unavailable:

                if person_aux.family_id.id is not False:

                    family = person_aux.family_id
                    vals = {}

                    if (person_aux.phase_id != family.phase_id):

                        vals['phase_id'] = person_aux.phase_id.id

                    if person_aux.ref_address_id.id is not False:
                        if (person_aux.ref_address_id.state != family.state):
                            vals['state'] = person_aux.ref_address_id.state
                    else:
                        if (person_aux.state != family.state):
                            vals['state'] = person_aux.state

                    if self.update_contact_info_data:

                        if (person_aux.contact_info_is_unavailable != family.contact_info_is_unavailable):

                            vals['contact_info_is_unavailable'] = person_aux.contact_info_is_unavailable

                        if (person_aux.zip != family.zip):

                            vals['zip'] = person_aux.zip

                        if (person_aux.street_name != family.street_name):

                            vals['street_name'] = person_aux.street_name

                        if (person_aux.street_number != family.street_number):

                            vals['street_number'] = person_aux.street_number

                        if (person_aux.street_number2 != family.street_number2):

                            vals['street_number2'] = person_aux.street_number2

                        if (person_aux.street2 != family.street2):

                            vals['street2'] = person_aux.street2

                        if (person_aux.country_id != family.country_id):

                            vals['country_id'] = person_aux.country_id.id

                        if (person_aux.state_id != family.state_id):

                            vals['state_id'] = person_aux.state_id.id

                        if (person_aux.city_id != family.city_id):

                            vals['city_id'] = person_aux.city_id.id

                        # if (person_aux.phone is not False) and (person_aux.phone != family.phone):

                        #     vals['phone'] = person_aux.phone

                        # if (person_aux.mobile is not False) and (person_aux.mobile != family.mobile):

                        #     vals['mobile'] = person_aux.mobile

                    if self.update_ref_address_data:

                        if (person_aux.ref_address_is_unavailable != family.ref_address_is_unavailable):

                            vals['ref_address_is_unavailable'] = person_aux.ref_address_is_unavailable

                        if (person_aux.ref_address_id != family.ref_address_id):

                            vals['ref_address_id'] = person_aux.ref_address_id.id

                    if vals != {}:

                        vals['reg_state'] = 'revised'

                    _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                    family.write(vals)

            if self.family_verification_exec:
                if person_aux.family_id.ref_address_id.id is not False:
                    person_aux.family_id.ref_address_id._address_verification_exec()
                if person_aux.family_id.id is not False:
                    person_aux.family_id._family_verification_exec()
                if person_aux.related_person_id.id is not False:
                    person_aux.related_person_id._person_verification_exec()

            if self.person_aux_verification_exec:
                if person_aux.ref_address_aux_id.id is not False:
                    person_aux.ref_address_aux_id._address_aux_verification_exec()
                person_aux._person_aux_verification_exec()

        return True
