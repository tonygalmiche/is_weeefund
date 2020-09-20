# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vcard_uid        = fields.Char("UID pour synchronisation VCARD",copy=False)
    is_vcard            = fields.Text("vcard Nextcloud",copy=False)
    is_mailing_list_ids = fields.Many2many('mail.mass_mailing.list', column1='mailing_list_id', column2='partner_id', string='Listes de diffusion')


    @api.multi
    def write(self, vals):
        old_mail = self.email
        new_mail = vals.get('email') or self.email
        if old_mail!=new_mail and old_mail!='':
            contacts = self.env['mail.mass_mailing.contact'].search([('email', '=', old_mail)])
            for contact in contacts:
                contact.opt_out = True
        if 'is_mailing_list_ids' in vals or 'email' in vals:
            if 'is_mailing_list_ids' in vals:
                ids = vals['is_mailing_list_ids'][0][2]
            else:
                ids=[]
                for mailing_list in self.is_mailing_list_ids:
                    ids.append(mailing_list.id)
            contacts = self.env['mail.mass_mailing.contact'].search([('email', '=', new_mail)])
            contact = False
            if contacts:
                contact = contacts[0]
            else:
                contact=self.env['mail.mass_mailing.contact'].create({'name':new_mail,'email':new_mail})
            if contact:
                contact.list_ids=[[6, False, ids]]
                contact.opt_out = False
        res = super(ResPartner, self).write(vals)
        return res

