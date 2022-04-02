# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vcard_uid        = fields.Char("UID pour synchronisation VCARD",copy=False)
    is_vcard            = fields.Text("vcard Nextcloud",copy=False)
    is_mailing_list_ids = fields.Many2many('mail.mass_mailing.list', column1='mailing_list_id', column2='partner_id', string='Listes de diffusion')


    @api.multi
    def _update_mass_mailing_contact(self,vals,new_mail):
        if 'is_mailing_list_ids' in vals or 'email' in vals:
            if 'is_mailing_list_ids' in vals:
                ids = vals['is_mailing_list_ids'][0][2]
            else:
                ids=[]
                for mailing_list in self.is_mailing_list_ids:
                    ids.append(mailing_list.id)
            contacts = self.env['mail.mass_mailing.contact'].sudo().search([('email', '=', new_mail)])
            contact = False
            if contacts:
                contact = contacts[0]
            else:
                contact=self.env['mail.mass_mailing.contact'].sudo().create({'name':new_mail,'email':new_mail})
            if contact:
                vals2={
                    'list_ids': [[6, False, ids]],
                    'opt_out' : False,
                }
                contact.sudo().write(vals2)


    @api.model
    def create(self, vals):
        new_mail = vals.get('email') or False
        if new_mail:
            self._update_mass_mailing_contact(vals,new_mail)
        res = super(ResPartner, self).create(vals)
        return res


    @api.multi
    def write(self, vals):
        for obj in self:
            old_mail = obj.email
            new_mail = vals.get('email') or obj.email
            if old_mail!=new_mail and old_mail!='':
                contacts = obj.env['mail.mass_mailing.contact'].sudo().search([('email', '=', old_mail)])
                for contact in contacts:
                    contact.opt_out = True
            if 'active' in vals:
                email = obj.email or False
                if email:
                    contacts = obj.env['mail.mass_mailing.contact'].sudo().search([('email', '=', email)])
                    for contact in contacts:
                        contact.opt_out = not vals['active']
            self._update_mass_mailing_contact(vals,new_mail)
        res = super(ResPartner, self).write(vals)
        return res


    @api.multi
    def unlink(self):
        email = self.email or False
        if email:
            contacts = self.env['mail.mass_mailing.contact'].sudo().search([('email', '=', email)])
            for contact in contacts:
                contact.opt_out = True
        return super(ResPartner, self).unlink()
