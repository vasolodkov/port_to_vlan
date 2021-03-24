#!/usr/bin/env python3

#
# create config.yaml with similar parameters
# 'ssh_user': 'user'
# 'ssh_pass'" 'pass'
# 'cores':
#   - '10.10.10.1'
#   - '10.10.10.2'
# 'access':
#   - '10.10.20.1'
#   - '10.10.20.2'
#

import sys
from netmiko import ConnectHandler
import ruamel.yaml as yaml


def generate_devices(device_ips, device_type):
    devices = [{'device_type': device_type,
                'ip': device,
                'username': ssh_user,
                'password': ssh_pass) for device in device_ips]
    return devices


with open('config.yaml') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

try:
    mac = sys.argv[1]
    access_vlan = sys.argv[2]
except IndexError as err:
    print('need more arguments: mac and vlan')
    mac = input('type mac: ')
    access_vlan = input('type new vlan: ')
    pass


while not access_vlan.isdigit():
    print('not digits in vlan')
    access_vlan = input('type new vlan: ')

ssh_user = config['sh_user']
ssh_pass = config['ssh_pass']
access = config['access']

sw_port_template = ['int sw_port',
                    'switchport access vlan access_vlan',
                    'end', 'wr']

access switches = generate_devices(access, 'cisco_ios')

for switch in access_switches:
    try:
        net_connect = ConnectHandler(**switch)
        port = net_connect.send_command(f'show mac ad | i {mac}')
        if 'STATIC' in port:
            sw_port = port.split()[-1]
            current_vlan = port.split()[0]
            print(f'switch {switch["ip"]}', f'port {sw_port}',
                  f'current vlan {current_vlan}', sep=' ')
            sw_port_template[0] = f'int {sw_port}'
            sw_port_template[1] = f'switchport access vlan {access_vlan}'
            result = net_connect.send_config_set(sw_port_template)
            print(result)
            net_connect.disconnect()
            break
        else:
            net_connect.disconnect()
    except:
        print(f'{mac} not on {switch["ip"]}')
