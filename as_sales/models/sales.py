from odoo import models, fields, api


class Sales(models.Model):
    _name = 'as.sale.order'
    _description = 'Sales'

    name = fields.Char(string='Order Number', default="New", tracking=1)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now(), tracking=1)
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Customer')
    line_ids = fields.One2many(comodel_name='as.order.line', inverse_name='order_id', string='Order Lines')
    amount_total = fields.Float(string='Amount Total', compute="_compute_price")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('line_ids.price_subtotal')
    def _compute_price(self):
        for rec in self:
            total = 0
            for line in rec.line_ids:
                total += line.price_subtotal
            rec.amount_total = total
    
    @api.model
    def create(self, values):
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('as.sale.order')
        res = super(Sales, self).create(values)
        return res


class orderLines(models.Model):
    _name = 'as.order.line'
    _description = 'Order Lines'

    order_id = fields.Many2one(comodel_name='as.sale.order', string='Order Number')
    product_id = fields.Many2one(comodel_name='as.product', string='Product')
    code = fields.Char(string='Product Code', related="product_id.code")
    uom_id = fields.Many2one(comodel_name='as.product.uom', string='Unit of Measure', related="product_id.uom_id")
    barcode = fields.Char(string='Barcodes', related="product_id.barcode")
    categ_id = fields.Many2one(comodel_name='as.product.category', string='Category', related="product_id.categ_id")
    brand_id = fields.Many2one(comodel_name='as.product.brand', string='Brand', related="product_id.brand_id")
    price_unit = fields.Float(string='Price Unit', related="product_id.price_unit")
    quantity = fields.Integer(string='Quantity')
    price_subtotal = fields.Float(string='Total', compute="_compute_price", store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related="order_id.currency_id")

    @api.depends('product_id','quantity')
    def _compute_price(self):
        for rec in self:
            total = 0
            if rec.product_id and rec.quantity:
                total = rec.product_id.price_unit * rec.quantity
            rec.price_subtotal = total
    
