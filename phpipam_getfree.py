#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: phpipam_getfree

short_description: Grabs a free ip address from a subnet using phpipam API.

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

author:
    - Carson Anderson (@rcanderson23)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        subnet=dict(type='str', required=True),
        url=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False),
        set_alive=dict(type='bool', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    
    s = requests.Session()
    
    token = get_token(module.params['url'], module.params['username'], module.params['password'])
    s.headers.update({'token': '%s' % token})

    subnet_id = get_subnet_id(s, module.params['url'], module.params['subnet'])
    print subnet_id
    #result['message'] += token    

    #get_subnet_id(module.params['url'], request, module.params['subnet']) 

    module.exit_json(**result)
    
def get_token(url, username, password):
    url += 'user/'
    r = requests.post(url, auth=(username, password))
    return r.json().get('data').get('token')

def get_subnet_id(session, url, subnet):
    url += 'subnets/cidr/%s/' % subnet
    subnet_id = session.get(url)
    return subnet_id.json().get('data')[0].get('id')

#def get_free_ip(url, request, subnet_id):
    #placeholder

def main():
    run_module()

if __name__ == '__main__':
    main()
