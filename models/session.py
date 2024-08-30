import time
from odoo import api, fields, models

STATES = [('draft','Draft'),('confirmed','Confirmed'),('done','Done')]

class Session(models.Model):
    _name = "academic.session"

    # def cari_tanggal(self):
    #     return time.strftime("%Y-%m-%D")

    name = fields.Char("Name", required=True, size=100, readonly=True, states={'draft' : [('readonly', False)]})
    course_id = fields.Many2one(comodel_name="academic.course", readonly=True, states={'draft' : [('readonly', False)]}, string="Course")
    instructor_id = fields.Many2one(comodel_name="res.partner", readonly=True, states={'draft' : [('readonly', False)]}, string="Instructor")
    start_date = fields.Date("Start Date", readonly=True, states={'draft' : [('readonly', False)]}, default=lambda self: time.strftime("%Y-%m-%d"))
    duration = fields.Integer("Duration", readonly=True, states={'draft' : [('readonly', False)]})
    seats = fields.Integer("Seats")
    active = fields.Boolean("Is Active", default=True)
    attendee_ids = fields.One2many(comodel_name="academic.attendee", string="Attendee", inverse_name="session_id", readonly=True, states={'draft' : [('readonly', False)]})

    taken_seats = fields.Float(string="Taken Seats", compute="_compute_taken_seats", readonly=True, states={'draft' : [('readonly', False)]})

    image_small = fields.Binary("Image", attachment=True, readonly=True, states={'draft' : [('readonly', False)]})

    state = fields.Selection(string="State", selection=STATES, readonly=True, required=True, default=STATES[0][0])

    def _compute_taken_seats(self):
        for x in self:
            if x.seats > 0:
                x.taken_seats = 100.0 * len(x.attendee_ids) / x.seats
            else:
                x.taken_seats = 0.0

    @api.onchange('seats')
    def onchange_seats(self):
        if self.seats > 0:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats
        else:
            self.taken_seats = 0.0

    # @api.multi
    def _cek_instruktur(self):
        for session in self:
            # session.instructor_id ada di dalam session.attendee_ids: partner_id
            # x = []

            # for attendee in session.attendee_ids:
            #     x.append(attendee.partner_id.id)

            x = [att.partner_id.id for att in session.attendee_ids]

            if session.instructor_id.id in x:
                return False

        return True

    _constraints = [(_cek_instruktur,'Instruktur tidak boleh merangkap jadi attendee',['instructor_id', 'attendee_ids'])]

    # @api.multi
    def copy(self, default=None):
        default = dict(default or {}, name=self.name + " (copy)")
        return super(Session, self).copy(default=default)

    # @api.multi
    def action_confirm(self):
        self.state = STATES[1][0]

    # @api.multi
    def action_done(self):
        self.state = STATES[2][0]

    # @api.multi
    def action_draft(self):
        self.state = STATES[0][0]