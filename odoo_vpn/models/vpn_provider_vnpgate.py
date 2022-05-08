
import base64
import requests
from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging

_logger = logging.getLogger(__name__)


class VpnProviderVpnGate(models.Model):
    _inherit = 'vpn.provider'

    def queue_vpn_collect_data_vpngate(self, record_id):
        print('->>> queue_vpn_collect_data_vpngate')
        return True
