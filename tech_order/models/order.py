from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class Order(models.Model):
    _name = "order.order"
    _description = "Orders"
    _order = 'name'

    def customer_domain(self):
        is_company = self.env.context.get('is_company')
        customers = self.env['res.partner'].search([])
        if is_company:
            customers = self.env['res.partner'].search([('is_company', '=', True)])
        # return type always list of tuples
        return [('id', 'in', customers.ids)]

    name = fields.Char("Name", required=True, copy=False, default='Order')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('in_process', 'In Process'),
                              ('delivered', 'Delivered'),
                              ('cancelled', 'Cancelled'),
                              ],
                              string='State', default='draft')
    total_price = fields.Float("Total Price", store=True, compute='_compute_total_price')
                               # ,groups="tech_order.tech_order_mgr")
    order_type = fields.Selection([('internal', 'Internal'), ('external', 'External')],
                                  string="Order Type", required=False, default='internal',
                                  readonly=True, states={'draft': [('readonly', False),('required', True)]})
    note = fields.Text("Note")
    order_date = fields.Date('Order Date', default=fields.datetime.now().date(), readonly=True)
    expected_date = fields.Datetime('Expected Date', readonly=False, compute="_compute_expected_date",
                                     inverse="inverse_expected_date")
    expected_duration_in_days = fields.Float(string="Expected duration in days")
                                                                    # domain method should be defined before
    customer_id = fields.Many2one("res.partner", "Customer", ondelete='restrict', domain=customer_domain)
    table_number = fields.Integer("Table Number")
    is_urgent = fields.Boolean("Is Urgent")
    items = fields.One2many('order.item', 'order_id', string="Items")
    external_items = fields.Many2many('external.item', string="External Items", readonly=True,
                                      states={'draft': [('readonly', False)]})
    # in many2many relation we give the model it connects to and an attribute consisting of
    # the name of the table which 1stId + 2ndId, and then the id columns of both tables
    # ,although I can emit the 2nd 3rd 4th attribute and let odoo handle it
    # but to avoid same naming I put it
    tags = fields.Many2many('order.tag', string="Tags") # 'relation_order_tag_ids', 'order_id', 'tag_id'
    # constraint directly on postgres
    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Order Name already exists!')
    ]

    def _check_date_existance_and_if_in_future(self, order):
        if order.order_date and order.order_date > datetime.now().date():
            return True
        return False

    @api.constrains('order_date')
    def check_order_date(self):
        for order in self:
            if self._check_date_existance_and_if_in_future(order):
                raise ValidationError(_("Order date must be in present or past!"))

    # @api.constrains('table_number')
    # def check_table_number(self):
    #     max_table_number = self.env['ir.config_parameter'].sudo().get_param('tech_order.max_table_number')
    #     # max_table_number = self.env['res.config.settings'].get_values().get('max_table_number')
    #     if self.table_number > max_table_number:
    #         raise ValidationError("Max Table Number is " + str(max_table_number))

    # items.total_price
    @api.depends('items','items.price', 'items.quantity')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(order.items.mapped('total_price'))

    @api.depends('order_date', 'expected_duration_in_days')
    def _compute_expected_date(self):
        for order in self:
            order.expected_date = order.order_date + timedelta(
                days=order.expected_duration_in_days
            )

    # @api.depends('expected_date') deos NOT update without manually saving
    # use @api.onchange('expected_date') instead if instant update is needed
    def inverse_expected_date(self):
        for order in self:
            order.expected_duration_in_days = (order.expected_date.date() - order.order_date).days

    def action_confirm(self):
        self.state = 'confirmed'
        self.order_date = datetime.now().date()

    def action_in_process(self):
        self.state = 'in_process'

    def action_delivered(self):
        self.state = 'delivered'

    def action_cancelled(self):
        self.state = 'cancelled'

    def check_urgent(self):
        for order in self:
            expected_date = order.expected_date.date() - timedelta(days=1)
            if expected_date == datetime.now().date():
                order.is_urgent= True

    def env_method(self):
        model = self.env.ref('tech_order.model_order_order')
        user = self.env.user
        user_time_zone = user.tz
        raise ValidationError(str(user) + ", " + str(user_time_zone))
        # raise ValidationError(str(model))
        # self.with_context({"is_urgent": True}) if I want to split a method into 2 paths

    # def create(self,vals):
    # have to named vals ^ to be considered as an extension to the create method in the super class
    @api.model
    def create(self, vals):
        # if vals.get('name', 'Order') == 'Order':
        if vals.get('name') == 'Order':
            vals['name'] = self.env['ir.sequence'].next_by_code('order_order_name_seq')
        if vals.get('customer_id'):
            customer_id = self.env['res.partner'].browse(vals.get('customer_id'))
            customer_id.update({'customer_rank': customer_id.customer_rank + 1})
        return super(Order, self).create(vals)

    def write(self, vals):
        old_customer_id = False
        old_customer_id = self.customer_id
        result = super(Order, self).write(vals)
        if vals.get('customer_id'):
            new_customer = self.customer_id
            new_customer.update({'customer_rank': new_customer.customer_rank + 1})
            old_customer_id.update({'customer_rank': old_customer_id.customer_rank - 1})
        return result

    def unlink(self):
        if self.customer_id:
            self.customer_id.update({'customer_rank': self.customer_id.customer_rank - 1})
        result = super(Order, self).unlink()
        return result
