from odoo import api, fields, models

class Course(models.Model):
    _name = "academic.course"
    _description = "Course"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    responsible_id = fields.Many2one(comodel_name="res.users", string="Responsible", required=True)

    session_ids = fields.One2many(comodel_name="academic.session", inverse_name="course_id", string="Sessions")

    _sql_constraints = [
        ('sql_check_name_unique', 'UNIQUE(name)', 'The course name must be unique!'),
        ('sql_check_name_description_diff', 'CHECK(name <> description)', 'The course name and description cannot be the same!'),
    ]
