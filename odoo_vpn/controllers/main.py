# -*- coding: utf-8 -*-
import json
import werkzeug
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug import wrappers
from odoo.exceptions import AccessDenied, UserError
from odoo.http import Controller, Response, request, route
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import http
from odoo import _
import odoo.tools as tools

import logging
_logger = logging.getLogger(__name__)


class VpnController(Controller):

    @route('/api/v1/get_free_vpn',
        type='json', auth='api_key', methods=['POST', 'OPTIONS'])
    def api_get_free_vpn(self, **kw):
        _logger.info('Start api_get_free_vpn >>>\n%s' % kw)
        response = {}
        try:
            data = request.env['vpn.vpn'].sudo()._api_get_free_vpn(kw)
            response = data
        except Exception as err:
            response = {
                'message': '%s' % err,
                'code': 400,
            }
        # _logger.info('END api_get_free_vpn <<<\n%s' % response)
        _logger.info('END api_get_free_vpn <<<')
        return response
