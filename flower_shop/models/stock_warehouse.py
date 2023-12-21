from odoo import models, fields
from odoo.exceptions import ValidationError
import requests


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    partner_id = fields.Many2one("res.partner", string="Partner")

    # getting api_key, Warehouse Location(latitude, longitude)
    def _get_api_key_and_location(self, show_error):
        print('_get_api_key_and_location')
        api_key = self.env["ir.config_parameter"].sudo().get_param("flower_shop.weather_api_key")
        if api_key == "unset" or not api_key:
            raise ValidationError("Please Make sure you set a working API key!")
        if not self.partner_id or not self.partner_id.partner_latitude or not self.partner_id.partner_longitude:
            raise ValidationError("Unable to retrieve warehouse location, could be because the warehouse doesn't exist")
        return api_key, self.partner_id.partner_latitude, self.partner_id.partner_longitude

    def get_weather(self, show_error=True):
        print('get_weather')
        self.ensure_one()
        api_key, lat, lon = self._get_api_key_and_location(show_error)
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            entries = response.json()
            self.env["stock.warehouse.weather"].create({
                "warehouse_id": self.id,
                "description": entries["weather"][0]["description"],
                "pressure": entries["main"]["pressure"],
                "temperature": entries["main"]["temp"],
                "humidity": entries["main"]["humidity"] / 100,
                "wind_speed": entries["wind"]["speed"],
                "rain_volume": entries["rain"]["1h"] if "rain" in entries else 0,
                "capture_time": fields.Datetime.now(),
            })
        except Exception as e:
            raise ValidationError(str(e))

    def get_weather_all_warehouses(self):
        print('get_weather_all_warehouses')
        for warehouse in self.search([]):
            warehouse.get_weather(show_error=False)

    def get_forecast_all_warehouses(self, show_error=True):
        print('get_forecast_all_warehouses')
        flower_serials_to_water = self.env["stock.lot"]
        for warehouse in self:
            api_key, lat, lng = warehouse._get_api_key_and_location(show_error)
            url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lng, api_key)
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                entries = response.json()
                is_rainy_today = False
                for i in range(0, 4):
                    if "rain" in entries["list"][i]:
                        rain = entries["list"][i]["rain"]["3h"]
                        if rain > 0.2:
                            is_rainy_today = True
                            break
                if is_rainy_today:
                    flower_products = self.env["product.product"].search([("is_flower", "=", True)])
                    quants = self.env["stock.quant"].search([
                        ("product_id", "in", flower_products.ids),
                        ("location_id", "=", warehouse.lot_stock_id.id)
                    ])
                    flower_serials_to_water |= quants.lot_id
            except Exception as e:
                raise ValidationError(str(e))
        for flower_serial in flower_serials_to_water:
            self.env["flower.water"].create({
                "serial_id": flower_serial.id,
            })
