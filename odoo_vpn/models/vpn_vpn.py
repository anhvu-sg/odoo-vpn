
import base64
import requests
from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging

_logger = logging.getLogger(__name__)


class VpnVpn(models.Model):
    _name = 'vpn.vpn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('VPN')
    _order = 'create_date desc'

    name = fields.Char(required=True)

    def cron_vpn_collect_data(self):
        self.env['vpn.provider'].vpn_collect_data()
        return True