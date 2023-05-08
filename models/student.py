from odoo import models , fields,api
import datetime
from odoo.exceptions import ValidationError
class StudentModel(models.Model):
    _name = 'iti.student'
    # _log_access = False

    name = fields.Char()
    email = fields.Char(required=True)
    age = fields.Integer()
    info = fields.Text()
    salary = fields.Float()
    birthdate = fields.Date()
    interview_time = fields.Datetime()
    description = fields.Html()
    is_accepted = fields.Boolean()
    gender = fields.Selection([
        ('male','Male'),
        ('female', 'Female'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('interviewing', 'Interviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ],default='new')
    avatar = fields.Image()
    track_id = fields.Many2one('iti.track')
    # branch_track = fields.Char(related='track_id.branch',store=False, readonly=False)
    branch_track = fields.Char(related='track_id.branch')
    skills_ids = fields.Many2many('iti.skill')
    # computed_age = fields.Integer(compute='compute_student_age',store=True)
    computed_age = fields.Integer(compute='compute_student_age')

    # _sql_constraints = [
    #     ('check_salary', 'CHECK(salary > 0)', 'Salary must be greater than 0'),
    #     ('unique_email', 'UNIQUE(email)', 'Email already Exists'),
    # ]

    _sql_constraints = [
        ('check_salary', 'CHECK(salary > 0)', 'Salary must be greater than 0'),
        ('unique_email', 'UNIQUE(email)', 'Email already exists'),
    ]

    @api.depends('birthdate')
    def compute_student_age(self):
        for record in self:
            if record.birthdate:
                record.computed_age = datetime.datetime.now().year - record.birthdate.year
            else:
                record.computed_age = 0

    @api.onchange('birthdate')
    def _onchange_birthdate(self):

        if self.birthdate:
            self.age = datetime.datetime.now().year - self.birthdate.year
            return {
                'warning':{
                    'title':'Age Change',
                    'message':'Age has been changed'
                }
            }

    def set_to_interview(self):
        self.state = 'interviewing'

    def set_to_accepted(self):
        self.state = 'accepted'

    def set_to_rejected(self):
        self.state = 'rejected'

    def set_to_new(self):
        self.state = 'new'


    @api.constrains('email')
    def validate_email(self):
        for record in self:
            if '@' not in record.email:
                raise ValidationError("Please insert valid email")


    # to ovvride create method which bilt it in odoo
    @api.model
    def create(self,vals):
        print(vals)
        if '@' not in vals['email']:
            vals['email'] += '@gmail.com'
        return super().create(vals)

    def write(self,vals):
        if vals.get('email') and '@' not in vals['email']:
            vals['email'] += '@gmail.com'
        return super().write(vals)
