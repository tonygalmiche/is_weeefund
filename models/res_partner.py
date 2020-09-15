# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vcard_uid = fields.Char("UID pour synchronisation VCARD",copy=False)
    is_vcard     = fields.Text("vcard Nextcloud",copy=False)
