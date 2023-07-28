# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.addons.payment_authorize.models.authorize_request import AuthorizeAPI
from odoo.addons.payment.models.payment_acquirer import _partner_split_name
import logging
_logger = logging.getLogger(__name__)

class PaymentAcquirerAuthorize(models.Model):
    _inherit = 'payment.acquirer'
        
    def debit_bank_account(self, partner, amount, order_line, amount_tax):
        values = {
                "createTransactionRequest": {
                    "merchantAuthentication": {
                        "name": self.authorize_login,
                        "transactionKey": self.authorize_transaction_key
                    },
                    # "refId": "123456",
                    "transactionRequest": {
                        "transactionType": "authCaptureTransaction",
                        "amount": amount,
                        "payment": {
                            "bankAccount": {
                                "accountType": "checking",
                                "routingNumber": partner.bank_ids[-1].aba_routing,
                                "accountNumber": partner.bank_ids[-1].acc_number,
                                "nameOnAccount": partner.bank_ids[-1].acc_holder_name
                            }
                        },
                        "lineItems": {
                            "lineItem": {
                                "itemId": order_line.id,
                                "name": order_line.product_id.name,
                                "description": order_line.name,
                                "quantity": order_line.product_uom_qty,
                                "unitPrice": order_line.price_unit
                            }
                        },
                        "tax": {
                            "amount": amount_tax,
                            "name": order_line.tax_id.name,
                            "description": order_line.tax_id.description
                        },
                        # "duty": {
                        #     "amount": "8.55",
                        #     "name": "duty name",
                        #     "description": "duty description"
                        # },
                        # "shipping": {
                        #     "amount": "4.26",
                        #     "name": "level2 tax name",
                        #     "description": "level2 tax"
                        # },
                        # "poNumber": "456654",
                        "billTo": {
                           'firstName': '' if partner.is_company else _partner_split_name(partner.name)[0],
                            'lastName': _partner_split_name(partner.name)[1],
                            'address': (partner.street or '' + (partner.street2 if partner.street2 else '')) or None,
                            'city': partner.city,
                            'state': partner.state_id.name or None,
                            'zip': partner.zip or '',
                            'country': partner.country_id.name or None
                        },
                        "shipTo": {
                            'firstName': '' if partner.is_company else _partner_split_name(partner.name)[0],
                            'lastName': _partner_split_name(partner.name)[1],
                            'address': (partner.street or '' + (partner.street2 if partner.street2 else '')) or None,
                            'city': partner.city,
                            'state': partner.state_id.name or None,
                            'zip': partner.zip or '',
                            'country': partner.country_id.name or None
                        },
                        # "customerIP": "192.168.1.1"
                    }
                }
            }
        API = AuthorizeAPI(self)
        response = API._authorize_request(values)
        _logger.info(response)
        return response

# class AuthorizeAPI():

#     def __init__(self, acquirer):
#         """Initiate the environment with the acquirer data.

#         :param record acquirer: payment.acquirer account that will be contacted
#         """
#         print ("\n\n >>>>>>>>. here it is ???????")
#         1/0
#         super().__init__(acquirer)

#     def debit_bank_account(self, partner, amount, token):
#         """
#             Debit a bank account
#             """

#         # Create a merchantAuthenticationType object with authentication details
#         # retrieved from the constants file
#         values = {
#             "createTransactionRequest": {
#                 "merchantAuthentication": {
#                     "name": self.name,
#                     "transactionKey": self.transaction_key
#                 },
#                 "refId": token.acquirer_ref,
#                 "transactionRequest": {
#                     "transactionType": "authCaptureTransaction",
#                     "amount": amount,
#                     "payment": {
#                         "bankAccount": {
#                             "accountType": "checking",
#                             "routingNumber": partner.bank_ids[0].aba_routing,
#                             "accountNumber": partner.bank_ids[0].acc_number,
#                             "nameOnAccount": partner.bank_ids[0].acc_holder_name
#                         }
#                     },
#                     "lineItems": {
#                         "lineItem": {
#                             "itemId": "1",
#                             "name": "vase",
#                             "description": "Cannes logo",
#                             "quantity": "18",
#                             "unitPrice": "45.00"
#                         }
#                     },
#                     "tax": {
#                         "amount": "4.26",
#                         "name": "level2 tax name",
#                         "description": "level2 tax"
#                     },
#                     "duty": {
#                     },
#                     "shipping": {
#                     },
#                     "poNumber": "456654",
#                     "billTo": {
#                         'firstName': '' if partner.is_company else _partner_split_name(partner.name)[0],
#                         'lastName': _partner_split_name(partner.name)[1],
#                         'address': (partner.street or '' + (partner.street2 if partner.street2 else '')) or None,
#                         'city': partner.city,
#                         'state': partner.state_id.name or None,
#                         'zip': partner.zip or '',
#                         'country': partner.country_id.name or None
#                     },
#                     "shipTo": {
#                         'firstName': '' if partner.is_company else _partner_split_name(partner.name)[0],
#                         'lastName': _partner_split_name(partner.name)[1],
#                         'address': (partner.street or '' + (partner.street2 if partner.street2 else '')) or None,
#                         'city': partner.city,
#                         'state': partner.state_id.name or None,
#                         'zip': partner.zip or '',
#                         'country': partner.country_id.name or None
#                     },
#                     "customerIP": "192.168.1.1"
#                 }
#             }
#         }
#         response = self._authorize_request(values)

class TxAuthorize(models.Model):
    _inherit = 'payment.transaction'
    
    def get_transaction_details(self):
        allowed_states = ('draft', 'pending','authorized')
        transactions = self.search([('state','in',allowed_states),('acquirer_id.display_as','=','ACH')])
        for tranaction in transactions:
            if tranaction.acquirer_reference:
                data = {
                    "getTransactionDetailsRequest": {
                        "merchantAuthentication": {
                            "name": tranaction.acquirer_id.authorize_login,
                            "transactionKey": tranaction.acquirer_id.authorize_transaction_key
                        },
                        "transId": tranaction.acquirer_reference
                    }
                }
                API = AuthorizeAPI(tranaction.acquirer_id)
                response = API._authorize_request(data)
                _logger.info(response)
                if response['transaction']['transactionStatus'] == 'settledSuccessfully' and \
                    response['transaction']['responseCode'] == 1:
                    tranaction.write({
                        'state': 'done',
                        'date': fields.Datetime.now(),
                        'state_message': '',
                    })
#                     tranaction._log_payment_transaction_received()
                elif response['transaction']['responseCode'] == 4:
                    tranaction.write({
                        'state': 'pending',
                        'date': fields.Datetime.now(),
                        'state_message': '',
                    })
#                     tranaction._log_payment_transaction_received()
                elif response['transaction']['responseCode'] == 3:
                    tranaction.write({
                        'state': 'error',
                        'date': fields.Datetime.now(),
                        'state_message': '',
                    })
#                     tranaction._log_payment_transaction_received()
                elif response['transaction']['responseCode'] == 2:
                    tranaction.write({
                        'state': 'cancel',
                        'date': fields.Datetime.now(),
                        'state_message': '',
                    })
#                     tranaction._log_payment_transaction_received()
        return True
