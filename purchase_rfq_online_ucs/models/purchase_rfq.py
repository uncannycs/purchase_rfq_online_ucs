from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    vendor_comment = fields.Text("Vendor Comment")
    vendor_signature = fields.Binary("Vendor Signature")
    vendor_signed_by = fields.Char("Signed By", readonly=True)
    vendor_signed_on = fields.Datetime("Signed On", readonly=True)
    vendor_response_state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('signed', 'Signed'),
    ], string="Vendor Response", default="draft")

    sign_ids = fields.One2many('purchase.order.sign.wizard', 'order_id', string='Quotation Signs')

    def supply_preview(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/purchase/rfq/{self.id}',
            'target': 'new',
        }

    def action_resend_rfq(self):
        self.ensure_one()
        self.write({'vendor_response_state': 'sent'})
        body = f"RFQ has been resent by vendor with updated pricing on {fields.Datetime.now()}"
        self.message_post(body=body, message_type='notification', subtype_xmlid='mail.mt_note')
        return True


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    is_editable = fields.Boolean("Is Editable", compute="_compute_is_editable")

    @api.depends('order_id.vendor_response_state')
    def _compute_is_editable(self):
        for line in self:
            line.is_editable = line.order_id.vendor_response_state == 'draft'