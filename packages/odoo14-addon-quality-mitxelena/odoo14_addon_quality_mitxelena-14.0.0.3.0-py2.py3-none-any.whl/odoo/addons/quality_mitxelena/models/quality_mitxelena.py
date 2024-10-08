from odoo import api, fields, models, _ # type: ignore
from logging import getLogger
import requests
import logging
import base64
_logger = getLogger(__name__)
class Product(models.Model):
    _inherit = ["product.template"]
    product_test = fields.Many2one(comodel_name='qc.test', string='Test', tracking=True)
    test_question = fields.One2many(related='product_test.test_lines')

    
class Question(models.Model):
    _inherit = ["qc.test.question"]
    valor_nominal = fields.Float(string='Valor Nominal', tracking=True)
    cota_min = fields.Float(string='Cota Mínima', tracking=True)
    cota_max = fields.Float(string='Cota Máxima', tracking=True)
    min_value = fields.Float(string="Min", digits="Quality Control", compute="_compute_test", store=True)    
    max_value = fields.Float(string="Max", digits="Quality Control", compute="_compute_test", store=True)
    short_notes = fields.Text(string='Notes', store=True, compute='_compute_short_notes')
    icon_select= fields.Selection(selection=[('paralelismo.png', 'Paralelismo'),
                                            ('simetria.png', 'Simetria'),
                                            ('inclinacion.png', 'Inclinacion'),
                                            ('redondez.png', 'Redondez'),
                                            ('planicidad.png', 'Planicidad'),
                                            ('posicion.png', 'Posicion'),
                                            ('perpendicularidad.png', 'Perpendicularidad'),
                                            ('formasuperficie.png', 'Forma Superficie'),
                                            ('circular.png', 'Circular'),
                                            ('total.png', 'Total'),
                                            ('cilindricidad.png', 'Cilindricidad'),
                                            ('formalinea.png', 'Forma Linea'),
                                            ('concentricidad.png', 'Concentricidad'),
                                            ('rectitud.png', 'Rectitud')
                                            ], string='Icon Select', tracking=True)
    icon = fields.Binary(string='Icon', store=True, compute='_compute_icon', attachment=False)
    
    @api.depends("icon_select")
    def _compute_icon(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            if record.icon_select:
                url = base_url + '/quality_mitxelena/static/src/img/' + record.icon_select
                icon = ""
                try:    
                    icon = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
                except Exception as e:
                    _logger.warning("Can't load the image from URL %s" % url)
                    logging.exception(e)                
            record.update({"icon": icon, })
    
    @api.depends('notes', 'short_notes')
    def _compute_short_notes(self):
        for record in self:
            if record.notes:
                record.short_notes = record.notes[:30] + '...' if len(record.notes) > 30 else record.notes


    @api.depends('valor_nominal', 'cota_min', 'cota_max')
    def _compute_test(self):        
        for record in self:
            record.min_value = record.valor_nominal - record.cota_min
            record.max_value = record.valor_nominal + record.cota_max
            
