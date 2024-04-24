from odoo import models , fields ,api
from odoo.exceptions import ValidationError


class HMSCustomerTemplate(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(required=True ,readonly=False)
    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    
    
    
    @api.constrains('related_patient_id')
    def _check_patient_email_exist(self):
        for customer in self:
            if customer.related_patient_id and customer.related_patient_id.email:
                linked_patients = self.search(
                    [('related_patient_id.email', '=', customer.related_patient_id.email), ('id', '!=', customer.id)])
                if linked_patients:
                    raise ValidationError("This email is already linked to another customer.")

    @api.constrains('related_patient_id')
    def _check_patient_count(self):
        for customer in self:
            if customer.related_patient_id:
                existing_linked_customers = self.search_count([('related_patient_id', '=', customer.related_patient_id.id)])
                if existing_linked_customers > 1:
                    raise ValidationError("A customer can only be related to one patient.")

    @api.ondelete(at_uninstall=True)
    def _prevent_delete_customer_linked_to_patient(self):
        for partner in self:
            if partner.related_patient_id:
                raise ValidationError("You can't delete this customer.")

