from odoo import models, fields ,api,tools
from odoo import exceptions
from odoo.exceptions import ValidationError
import re
from datetime import date
from dateutil.relativedelta import relativedelta 

class HMSStateLogs(models.Model):
    _name = 'hms_state_logs'
    
    description = fields.Text(string='Description')
    patient_id = fields.Many2one('hms.patient')


class HMSPaitents(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char(string='First Name', required = True)
    last_name = fields.Char(string='Last Name', required = True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    # age = fields.Integer(string='Age')
    age = fields.Integer(compute='_compute_age', store=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    email = fields.Char(string="Email", store=True ,unique=True)

    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related = 'department_id.capacity')

    doctor_ids = fields.Many2many('hms.doctor')

    state_logs = fields.One2many('hms_state_logs', 'patient_id')

    def change_state(self):
        for patient in self:
            if patient.states == 'Undetermined':
                patient.states = 'Good'
            elif patient.states == 'Good':
                patient.states = 'Fair'
            elif patient.states == 'Fair':
                patient.states = 'Serious'
            msg = {
                'description': f'State changed to {patient.states}',
                'patient_id': patient.id,
            }
            self.env['hms_state_logs'].create(msg)


    @api.onchange('age')
    def onchange_age(self):
        if self.age:
            if self.age < 30:
                self.pcr = True
                return {
                    'warning':{'title': 'Warning PCR Checked',
                    'message': 'PCR has been automatically checked for patients under 30 years old.'
                               }
                }

    @api.onchange('state')
    def create_state_log(self):
        if self.state:
            vals = {
                'description': 'State changed to %s' % (self.state),
                'patient_id': self.id
            }
            self.env['hms_state_logs'].create(vals)

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))

            else:
                rec.age = 5
                
                
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'The email address must be unique.')            
    ]
    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not tools.email_split(record.email):
                raise exceptions.ValidationError("Invalid email.")