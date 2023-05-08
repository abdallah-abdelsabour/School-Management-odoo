from odoo import models,fields

class WizardTrack(models.TransientModel):
    _name = 'iti.track.wizard'

    name = fields.Char()
    description = fields.Text()

    def save_track_values(self):
        # self.env['iti.track'].create({
        #     'name':self.name,
        #     'description':self.description
        # })

        students = self.env['iti.student'].search([('state','=','accepted')])
        # students.write({
        #     'state':'interviewing'
        # })
        students.unlink()
        # print(students)