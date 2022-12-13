# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FormioComponentServerApi(models.Model):
    _name = 'formio.component.server.api'
    _description = 'Forms Component Server API'

    DEFAULT_PYTHON_CODE = """# Available variables:
# Return, only one of:
#  if API type is "values"
#  - values: Dictionary, read by the Forms Data API to set Components (key) value
#  elif API type is "convert":
#  - convert: A value in component's supported type, read by the Forms Data API to convert and return a value
# Others:
#  - env: Odoo Environment on which the action is triggered
#  - component: Form component (formiodata.Component) object
#  - builder: formio.builder object (record) on which the action is triggered
#  - form: formio.form object (record) on which the action is triggered; maybe None (not present)
#  - params: Dictionary with optional params provided eg. URL query params
#  - time, datetime, dateutil, timezone: useful Python libraries
# Assign to values (dict), eg values['foo'] = 'bar', values.update({some_dict})"""

    formio_builder_id = fields.Many2one(
        'formio.builder', string='Form Builder',
        required=True, readonly=True, ondelete='cascade')
    name = fields.Char(string='API Name', required=True)
    type = fields.Selection(
        string='Type',
        selection=[('values', 'values'), ('convert', 'convert')],
        default='values',
        ondelete='set null',
    )
    # Python code
    code = fields.Text(
        string='Python Code',
        default=DEFAULT_PYTHON_CODE,
        groups='base.group_system',
        help="Write Python code that the Component Value will get set. Some variables are "
        "available for use; help about python expression is given in the help tab.")
    active = fields.Boolean(string='Active', default=True)

    @api.constrains('name', 'type')
    def _constraint_unique(self):
        domain = [('name', '=', self.name), ('type', '=', self.type)]
        if self.search(domain):
            msg = _('Components API Name and Type should be unique.\nOnly 1 Component API with name "%s" and type "%s" is allowed.') % (self.name, self.type)
            raise ValidationError(msg)
