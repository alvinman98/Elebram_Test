import base64
from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from odoo.tools import image_process


class uomCategory(models.Model):
    _name = 'as.uom.category'
    _description = 'Unit of Measure'

    name = fields.Char(string='Unit of Measure category')


class productCategory(models.Model):
    _name = 'as.product.category'
    _description = 'Product Categories'

    name = fields.Char(string='Product Category')


class productBrand(models.Model):
    _name = 'as.product.brand'
    _description = 'Product Brands'

    name = fields.Char(string='Product Brand')


class ProductUom(models.Model):
    _name = 'as.product.uom'
    _description = 'Unit of Measure'

    name = fields.Char(string='Unit of Measure')
    categ_id = fields.Many2one(comodel_name='as.uom.category', string='Category')


class productCatalogs(models.Model):
    _name = 'as.product'
    _description = 'Product Catalogs'
    
    @api.model
    def _get_default_image(self):
        image_path = get_module_resource('as_sales', 'static/img', 'avatar.png')
        image = base64.b64encode(open(image_path, 'rb').read())
        return image_process(image, colorize=True)

    active = fields.Boolean(default=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    name = fields.Char(string='Product Name')
    code = fields.Char(string='Product Code')
    uom_id = fields.Many2one(comodel_name='as.product.uom', string='Unit of Measure')
    barcode = fields.Char(string='Barcodes')
    categ_id = fields.Many2one(comodel_name='as.product.category', string='Category')
    brand_id = fields.Many2one(comodel_name='as.product.brand', string='Brand')
    price_unit = fields.Float(string='Price Unit')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_get_default_image)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
