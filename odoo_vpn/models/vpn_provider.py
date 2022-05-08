
import base64
import requests
from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging

_logger = logging.getLogger(__name__)


class VpnProvider(models.Model):
    _name = 'vpn.provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = _('VPN Provider')
    _order = 'create_date desc'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    base_url = fields.Char(required=True)

    def vpn_collect_data(self):
        provider_recs = self.search([])
        for provider_rec in provider_recs:
            provider_code = provider_rec.code
            if provider_code:
                if hasattr(self, 'queue_vpn_collect_data_%s' % provider_code):
                    getattr(self.with_delay(), 'queue_vpn_collect_data_%s' % provider_code)(provider_rec.id)
        return True