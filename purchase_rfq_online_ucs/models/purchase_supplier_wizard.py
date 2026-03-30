import base64
from odoo import api, fields, models, _

class PurchaseOrderSignWizard(models.TransientModel):
    _name = 'purchase.order.sign.wizard'
    _description = 'Purchase Order Sign Wizard'

    order_id = fields.Many2one('purchase.order', string="Order", required=True, readonly=True)
    vendor_signed_by = fields.Char("Full Name", required=True, readonly=True, default=lambda self: self.env.user.name)
    signature_method = fields.Selection([
        ('draw', 'Draw'),
        ('auto', 'Auto'),
        ('load', 'Upload')
    ], string="Signature Method", default='draw', required=True)
    vendor_signed_on = fields.Datetime(string='Sign Date', default=fields.Datetime.now)
    vendor_signature = fields.Binary("Signature")

    def action_accept_send(self):
        self.ensure_one()
        order = self.order_id
        order.write({
            'vendor_signature': self.vendor_signature,
            'vendor_signed_by': self.vendor_signed_by,
            'vendor_signed_on': fields.Datetime.now(),
            'vendor_response_state': 'signed'
        })
        return {'type': 'ir.actions.act_window_close'}