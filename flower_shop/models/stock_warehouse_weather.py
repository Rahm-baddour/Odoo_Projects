from odoo import models, fields


class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Stock Warehouse Weather'

    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")
    temperature = fields.Float(string="Temperature")
    pressure = fields.Float(string="Pressure")
    humidity = fields.Float(string="Humidity")
    wind_speed= fields.Float(string="Wind Speed")
    rain_volume= fields.Float(string="Rain Volume")
    description= fields.Char(string="Description")
    capture_time= fields.Date(string="Capture Time", default=fields.datetime.now())
