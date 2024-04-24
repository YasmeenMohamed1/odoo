from odoo import models , fields


class HMSCustomerTemplate(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(required=True ,readonly=False)
    # mobile = fields.Char(required=True)

    related_patient_id = fields.Many2one('hms_patient', string='Related Patient')
