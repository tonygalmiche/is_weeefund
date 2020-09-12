import logging
import io

from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.addons.base_iban.models.res_partner_bank import _map_iban_template
from odoo.addons.base_iban.models.res_partner_bank import validate_iban
import datetime

_logger = logging.getLogger(__name__)

try:
    from ofxparse import OfxParser
except ImportError:
    _logger.debug("ofxparse not found.")
    OfxParser = None


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _check_journal_bank_account(self, journal, account_number):
        res = super(
            AccountBankStatementImport, self
        )._check_journal_bank_account(journal, account_number)
        if not res:
            e_acc_num = journal.bank_account_id.sanitized_acc_number
            e_acc_num = e_acc_num.replace(" ", "")
            validate_iban(e_acc_num)
            country_code = e_acc_num[:2].lower()
            iban_template = _map_iban_template[country_code].replace(
                " ", "")
            e_acc_num = "".join(
                [c for c, t in zip(e_acc_num, iban_template) if t == "C"])
            res = (e_acc_num == account_number)
        return res

    @api.model
    def _check_weeefund(self, data_file):
        weeefund = False
        code_banque = False
        try:
            data = data_file.decode('ISO-8859-1')
            lines = data.split('\n')
            if len(lines)>0:
                vals = lines[0].split(';')
                if len(vals)==5:
                    code_banque=vals[0].split(' : ')[1]
        except Exception as e:
            _logger.debug(e)
            return False
        if code_banque:
            weeefund=True
        return weeefund


    def _str2float(self,val):
        try:
            x = val.replace(',','.').replace('+','').strip()
            x = float(x)
        except ValueError:
            x = 0
        return x


    def _parse_file(self, data_file):
        weeefund = self._check_weeefund(data_file)
        if not weeefund:
            return super(AccountBankStatementImport, self)._parse_file(data_file)
        data = data_file.decode('ISO-8859-1')
        lines = data.split('\n')
        lig=0
        code_banque=number=debut=fin='?'
        transactions = []
        for line in lines:
            lig+=1
            vals = line.split(';')
            print(lig,len(vals),vals)
            if lig==1 and len(vals)==5:
                code_banque=vals[0].split(' : ')[1]
                debut = vals[2].split(' : ')[1]
                fin   = vals[3].split(' : ')[1]
            if lig==2 and len(vals)==4:
                number=vals[0].split(' : ')[1]

            if lig>=6:
                if len(vals)==7:
                    date = datetime.datetime.strptime(vals[0], '%d/%m/%y')
                    unique = vals[1]
                    name   = vals[2]
                    ref    = vals[5]
                    debit  = self._str2float(vals[3])
                    credit = self._str2float(vals[4])
                    amount = credit + debit
                    vals = {'date': date, 'name': name, 'ref': ref, 'amount': amount, 'unique_import_id': unique}
                    transactions.append(vals)
        total_amt = 0.00
        print('number =',number)
        #number = code_banque
        balance = 0
        vals_bank_statement = {
            'name': u'du '+debut+u' au '+fin,
            'transactions': transactions,
            'balance_start': balance - total_amt,
            'balance_end_real': balance,
        }
        return 'eur', number, [vals_bank_statement]


