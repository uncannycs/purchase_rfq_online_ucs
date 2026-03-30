from odoo import http, fields
from odoo.http import request
import base64,json
from odoo.tools import float_round
from psutil import process_iter
import datetime


class PurchasePortal(http.Controller):

    @http.route(['/purchase/rfq/<int:order_id>'], type='http', auth="public", website=True)
    def portal_rfq_page(self, order_id, **kw):
        order = request.env['purchase.order'].sudo().browse(order_id)
        if not order or order.vendor_response_state != 'draft':
            return request.redirect('/my/purchase')
        values = {
            'order': order,
            'object': order,
            'user_name': request.env.user.name or 'Vendor',
        }
        return request.render('purchase_rfq_online_ucs.portal_rfq_template', values)


    # for signing and send button
    @http.route('/purchase/rfq/sign', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def sign_rfq(self):
        try:
            raw_data = request.httprequest.data.decode('utf-8')
            post = json.loads(raw_data) if raw_data else {}
        except json.JSONDecodeError:
            return request.make_json_response({'success': False, 'error': 'Invalid JSON data'}, status=400)

        order_id = post.get('order_id')
        updated_prices = post.get('updated_prices', {})
        vendor_signed_by = post.get('vendor_signed_by')
        vendor_signature = post.get('vendor_signature')
        vendor_signed_on = post.get('vendor_signed_on')

        if not all([order_id, vendor_signed_by, vendor_signature, vendor_signed_on]):
            return {'success': False, 'error': 'Missing required fields'}

        try:
            order = request.env['purchase.order'].sudo().browse(int(order_id))
            if not order:
                return {'success': False, 'error': 'Order not found'}


            for line_id, price in updated_prices.items():
                line = order.order_line.filtered(lambda l: l.id == int(line_id))

                if line:
                    line.sudo().write({'price_unit': float(price)})

            vendor_signed_on_dt = datetime.datetime.fromisoformat(vendor_signed_on.replace('Z', '+00:00'))

            signature_data = vendor_signature.split(',')[1] if ',' in vendor_signature else vendor_signature

            order.sudo().write({
                'vendor_signed_by': vendor_signed_by,
                'vendor_signed_on': vendor_signed_on_dt.date(),
                'vendor_signature': signature_data,
                'vendor_response_state': 'sent',
            })

            report_action = request.env.ref('purchase.report_purchase_quotation')

            pdf_content, content_type = request.env['ir.actions.report']._render_qweb_pdf(
                'purchase.report_purchase_quotation', [order.id]
            )

            pdf_base64 = base64.b64encode(pdf_content)

            attachment = request.env['ir.attachment'].sudo().create({
                'name': f'Signed Quotation - {order.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'purchase.order',
                'res_id': order.id,
                'mimetype': 'application/pdf'
            })

            attachment = request.env['ir.attachment'].sudo().browse(attachment.id)

            order.sudo().message_post(
                body=f"Quotation signed by {order.vendor_signed_by}",
                attachment_ids=[attachment.id],
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )

            return request.make_json_response({'success': True})

        except Exception as e:
            return {'success': False, 'error': str(e)}