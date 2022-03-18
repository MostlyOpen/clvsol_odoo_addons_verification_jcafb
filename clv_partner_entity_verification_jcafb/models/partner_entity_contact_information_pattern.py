# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerEntityStreetPattern(models.Model):
    _description = 'Partner Entity Contact_Information Pattern'
    _name = "clv.partner_entity.contact_information_pattern"
    _order = "name"

    name = fields.Char(string='Address Name', required=False, help="Address Name")

    street = fields.Char(string='Street')

    street_number = fields.Char(string='Street Number')

    street_number2 = fields.Char(string='Street Number 2')

    street2 = fields.Char(string='Street 2')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('pattern_uniq',
         'UNIQUE(street, street_number, street_number2, street2)',
         u'Error! The Pattern must be unique!'
         ),
    ]

    suggested_name = fields.Char(
        string="Suggested Name", required=False, store=True,
        compute="_get_suggested_name",
        help='Suggested Name for the Address.'
    )

    @api.depends('street', 'street_number', 'street_number2', 'street2')
    def _get_suggested_name(self):
        for record in self:
            if record.street:
                record.suggested_name = record.street
                if record.street_number:
                    record.suggested_name = record.suggested_name + ', ' + record.street_number
                    if record.street_number2:
                        record.suggested_name = record.suggested_name + '/' + record.street_number2
                else:
                    if record.street_number2:
                        record.suggested_name = record.suggested_name + ', ' + record.street_number2
                if record.street2:
                    record.suggested_name = record.suggested_name + ' (' + record.street2 + ')'
            else:
                record.suggested_name = 'Address Name...'

    @api.model
    def create(self, values):
        record = super().create(values)

        if record.name != record.suggested_name:
            record['name'] = record.suggested_name

        return record

    def write(self, values):
        ret = super().write(values)
        for record in self:
            if record.suggested_name is not False:
                if record.name != record.suggested_name:
                    values['name'] = record.suggested_name
                    super().write(values)
                else:
                    if ('name' in values and values['name'] == '/') or \
                       (record.name == '/'):
                        values['name'] = record.suggested_name
                        super().write(values)
        return ret
