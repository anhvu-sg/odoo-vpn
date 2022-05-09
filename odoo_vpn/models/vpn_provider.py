from urllib import request

import base64
import requests
from bs4 import BeautifulSoup

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging

_logger = logging.getLogger(__name__)

ERROR_MSG = "Method: {0} throw exception: {1} at: {2}"

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
                    # getattr(self, 'queue_vpn_collect_data_%s' % provider_code)(provider_rec.id)
        return True

    def _get_url(self, url):
        try:
            req = request.Request(url)
            with request.urlopen(req, timeout=8) as response:
                if response.headers.get_content_charset() == None:
                    encoding = 'utf-8'
                else:
                    encoding = response.headers.get_content_charset()
                html = response.read().decode(encoding)
            return html
        except Exception as ex:
            print(ERROR_MSG.format(
                "_get_url", ex, datetime.now()))
            return None
