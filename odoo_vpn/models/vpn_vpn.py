import base64

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.modules.module import get_module_path

from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF


import logging

_logger = logging.getLogger(__name__)


class VpnVpn(models.Model):
    _name = 'vpn.vpn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('VPN')
    _order = 'create_date desc'

    provider_id = fields.Many2one('vpn.provider', required=True)
    name = fields.Char(required=True)
    ip = fields.Char()
    score = fields.Char()
    ping = fields.Char()
    speed = fields.Float()
    country_long = fields.Char()
    country_short = fields.Char()
    num_vpn_sessions = fields.Char()
    uptime = fields.Char()
    total_user = fields.Char()
    total_traffic = fields.Float()
    log_type = fields.Char()
    operator = fields.Char()
    message = fields.Char()
    openvpn_config_base64 = fields.Char()
    active = fields.Boolean(default=True)

    def btn_download(self):
        self.ensure_one()
        module_path = get_module_path('odoo_vpn')
        file_name = '%s.ovpn' % (self.name)
        file_path = '%s/static/src/download/%s' % (module_path, file_name)
        f = open(file_path, 'w')
        f.write(base64.b64decode(self.openvpn_config_base64).decode('utf-8'))
        f.close()
        return {
            'type': 'ir.actions.act_url',
            'url': str('odoo_vpn/static/src/download/%s' % (file_name)),
            'target': 'new',
        }

    def cron_vpn_collect_data(self):
        self.env['vpn.provider'].vpn_collect_data()
        return True

    def _api_get_free_vpn(self, kw):
        res = {
            'message': _('Success'),
            'code': 200,
            'data': []
        }
        param_env = self.env['ir.config_parameter'].sudo()
        number_of_record = param_env.get_param('number_of_record', 10)
        number_of_record = int(number_of_record)
        if not kw:
            sql = '''
                SELECT *
                FROM vpn_vpn
                WHERE
                    id in (
                        SELECT id
                        FROM vpn_vpn
                        WHERE active = 't'
                        ORDER BY RANDOM()
                        LIMIT {limit}
                    )
                ORDER BY speed DESC, create_date DESC
            '''.format(limit=number_of_record)
            self.env.cr.execute(sql)
            data = self.env.cr.dictfetchall()
            res['data'] = data
        return res