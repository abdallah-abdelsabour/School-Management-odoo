from odoo import models,fields

class Skills(models.Model):
    _name = 'iti.skill'
    # _table = '7amada'  # if change table name in database

    name = fields.Char()
    students_ids = fields.Many2many('iti.student')