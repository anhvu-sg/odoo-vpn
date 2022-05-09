import base64
import requests

from datetime import date, datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DF,\
    DEFAULT_SERVER_DATETIME_FORMAT as DTF

import logging

_logger = logging.getLogger(__name__)


class VpnProviderVpnGate1(models.Model):
    _inherit = 'queue.job'

    def write(self,vals):
        print('ooo')
        return super(VpnProviderVpnGate1, self).write(vals)
class VpnProviderVpnGate(models.Model):
    _inherit = 'vpn.provider'

    @api.model
    def queue_vpn_collect_data_vpngate(self, record_id):
        record = self.search([
            ('id', '=', record_id),
            ('code', '=', 'vpngate'),
        ])
        vpn_env = self.env['vpn.vpn']
        if record:
            try:
                vpn_data = requests.get(record.base_url).text.replace('\r','')
                servers = [line.split(',') for line in vpn_data.split('\n')]
                servers = [s for s in servers[2:] if len(s) > 1]
                for server in servers:
                    host_name = server[0]
                    ip = server[1]
                    score = server[2]
                    ping = server[3]
                    speed = server[4]
                    country_long = server[5]
                    country_short = server[6]
                    num_vpn_sessions = server[7]
                    uptime = server[8]
                    total_user = server[9]
                    total_traffic = server[10]
                    log_type = server[11]
                    operator = server[12]
                    message = server[13]
                    openvpn_config_base64 = server[14]
                    # tcp_port = server[15]
                    # udp_port = server[16]
                    # l2tp = server[17]
                    #HostName,IP,Score,Ping,Speed,CountryLong,CountryShort,NumVpnSessions,Uptime,TotalUsers,TotalTraffic,LogType,Operator,Message,OpenVPN_ConfigData_Base64
                    vpn_recs = vpn_env.search([('name', '=', host_name)])
                    if not vpn_recs:
                        vpn_env.create({
                            'name': host_name,
                            'ip': ip,
                            'score': score,
                            'ping': ping,
                            'speed': float(speed)/1000000, #Mbps
                            'country_long': country_long,
                            'country_short': country_short,
                            'num_vpn_sessions': num_vpn_sessions,
                            'uptime': uptime,
                            'total_user': total_user,
                            'total_traffic': float(total_traffic)/1000000000, #GB,
                            'log_type': log_type,
                            'operator': operator,
                            'message': message,
                            'openvpn_config_base64': openvpn_config_base64,
                            'provider_id': record_id,
                        })
            except Exception as e:
                return e
        return True

