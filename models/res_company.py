# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_date_synchro_vcard = fields.Datetime("Date de dernière synchronisation VCARD")

