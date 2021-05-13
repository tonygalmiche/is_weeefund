# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class MassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'


    @api.multi
    def _supprimer_contacts_ir_cron(self):


        #** Supprimer les contacts sans liste *********************************
        filtre = [('list_ids','=', False )]
        contacts = self.env['mail.mass_mailing.contact'].search(filtre)
        for contact in contacts:
            print(contact,contact.name,contact.list_ids)
            contact.unlink()

        #** Actualiser les contacts (suite anomalies à la création) ***********
        partners = self.env['res.partner'].search([])
        for partner in partners:
            if partner.email and partner.is_mailing_list_ids:
                email = partner.email
                vals={'email': email}
                partner._update_mass_mailing_contact(vals,email)
                print(partner,partner.email,partner.is_mailing_list_ids)