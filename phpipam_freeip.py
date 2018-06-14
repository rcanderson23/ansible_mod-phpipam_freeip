#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: phpipam_freeip

short_description: Grabs a free ip address from a subnet using phpipam api.

version_added: "2.4"

description:
    - "Simple module that grabs a free ip address from a subnet"

options:
    subnet:
        description:
            - Subnet in phpipam that you need to obtain a free ip address from
        required: true
    url:
        description:
            - Address of phpipam server including api and app name
        required: true
    username:
        description:
            - Username for initial authentication to phpipam api
        required: true
    password:
        description:
            - Password for initial authentication to phpipam api

author:
    - Carson Anderson (@rcanderson23)
'''

EXAMPLES = '''
# Pass in a message
- name: obtain a free ip address from phpipam
  phpipam_getfree:
    subnet: '192.168.0.0/24'
    url: ipam.domain.tld/api/app_name/
    username: user
    password: password
  delegate_to: localhost
  register: ip_address
'''

RETURN = '''
changed:
    description: If module successfully obtained an ip
    returned: success
    type: bool
subnet_id:
    description: Subnet id of the ip address obtained
    returned: success
    type: str
    sample: '7'
ip:
    description: IP address obtained from PHPIPAM
    returned: success
    type: str
    sample: '192.168.0.7'
token:
    description: Authentication token used after initial user/pass authentication
    returned: success
    type: str



'''

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    module_args = dict(
        subnet=dict(type='str', required=True),
        url=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    
    s = requests.Session()
    
    token = get_token(module.params['url'], 
                      module.params['username'], module.params['password'])
    result['token'] = token
    s.headers.update({'token': '%s' % token})

    subnet_id = get_subnet_id(s, module.params['url'], module.params['subnet'])
    
    result['subnet_id'] = subnet_id

    ip = get_free_ip(s, module.params['url'], subnet_id)
    
    result['ip'] = ip
    result['changed'] = True
    
    module.exit_json(**result)
    
def get_token(url, username, password):
    url += 'user/'
    r = requests.post(url, auth=(username, password))
    return r.json().get('data').get('token')

def get_subnet_id(session, url, subnet):
    url += 'subnets/cidr/%s/' % subnet
    subnet_id = session.get(url)
    return subnet_id.json().get('data')[0].get('id')

def get_free_ip(session, url, subnet_id):
    payload = {'hostname': 'test-api', 'subnetId': '%s' % subnet_id}
    url += 'addresses/first_free/'
    free_ip = session.post(url, payload)
    return free_ip.json().get('data')

def main():
    run_module()

if __name__ == '__main__':
    main()
