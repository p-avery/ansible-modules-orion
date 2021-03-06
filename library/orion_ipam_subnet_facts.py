#!/usr/bin/env python

import requests
from orionsdk import SwisClient
from ansible.module_utils.basic import *
from ansible.module_utils.pycompat24 import get_exception
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def main():
    module = AnsibleModule(
        argument_spec = dict(
            api_url = dict(required=True, default=None),
            username = dict(required=True, default=None),
            password = dict(required=True, default=None, no_log=True),
            subnet = dict(required=True),
            validate_certs = dict(required=False, default=True)
        ),
        required_together = [['username', 'password']],
        supports_check_mode = False
    )

    api_url = module.params['api_url']
    username = module.params['username']
    password = module.params['password']
    subnet = module.params['subnet']
    validate_certs = module.params['validate_certs']

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    client = SwisClient(api_url, username, password, verify=validate_certs)
    query = "SELECT TOP 255 I.DisplayName FROM IPAM.IPNode I WHERE Status=2 AND I.Subnet.DisplayName Like '{}%'".format(subnet)
    response = client.query(query)
    available_ip_addresses = [ ip_node['DisplayName'] for ip_node in response['result'] ]

    module.exit_json(changed=True, available_ip_addresses=available_ip_addresses)


if __name__ == '__main__':
    main()
