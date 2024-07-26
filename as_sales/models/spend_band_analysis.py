from odoo import models, fields, api, tools


class SpendBandAnalysis(models.Model):
    _name = 'spend.band.analysis'
    _auto = False
    _description = 'Spend Band Analysis Report'

    product_id = fields.Many2one(comodel_name='as.product', string='Product Name')
    code = fields.Char(string='Product Code')
    order_date = fields.Date(string='Order Date')
    trx_text = fields.Char(string='Nilai TRX', default="Nilai TRX")
    spend_type = fields.Selection(string='Type Spend', selection=[('a', 'Rp 0 - RP 50.000'), ('b', 'Rp 50.001 - Rp 100.000'), ('c', 'Rp 100.001 - Rp 200.000'), ('d', 'Rp 200.001 - Rp 500.000'), ('e', '> Rp 500.000.')])

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "spend_band_analysis")
        query = """
        CREATE OR REPLACE VIEW %s AS (
            SELECT
                row_number() OVER () as id,
                line.product_id,
                line.code,
                line.order_date,
                line.trx_text,
                line.spend_type
                FROM (
                    SELECT asl.product_id as product_id,
                    product.code as code,
                    so.order_date::DATE as order_date,
                    asl.price_subtotal as total,
                    'Nilai TRX' as trx_text,
                    CASE WHEN asl.price_subtotal > 0 AND asl.price_subtotal <= 50000 THEN 'a'
                    WHEN asl.price_subtotal > 50000 AND asl.price_subtotal <= 100000 THEN 'b'
                    WHEN asl.price_subtotal > 100000 AND asl.price_subtotal <= 200000 THEN 'c'
                    WHEN asl.price_subtotal > 200000 AND asl.price_subtotal <= 500000 THEN 'd'
                    WHEN asl.price_subtotal > 500000 THEN 'e' END spend_type
                    FROM as_order_line AS asl
                    JOIN as_sale_order so ON so.id = asl.order_id
                    JOIN as_product product ON product.id = asl.product_id
                ) as line
        )
        """%(self._table)
        self.env.cr.execute(query)
