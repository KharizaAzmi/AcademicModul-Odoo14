import string
from odoo import api, fields, models

class Attendee(models.Model):
    _name = "academic.attendee"
    name = fields.Char("Reg Number", required=True)
    session_id = fields.Many2one(comodel_name="academic.session", string="Session")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    course_id = fields.Many2one(comodel_name="academic.course", string="Course", related="session_id.course_id", store=True)

    _sql_constraints = [
        ('sql_cek_attendee', 'UNIQUE(session_id, partner_id)', 'Attendee tidak boleh dobel dalam satu session')    
    ]