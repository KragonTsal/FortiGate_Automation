#! Fortigate Automation

#from cmath import log
#from stat import filemode
from netmiko import Netmiko
from time import strftime
import csv
import logging
import os
import sys

# Absolute Variables
program_folder = os.getcwd()

# Setups for base configuration
fortigate_config = {
    'device_type': 'fortinet',
    'host': '192.168.1.99',
    'username': 'admin',
    'password': 'N0passwd.'
}

# Import Base Config Information
with open('import.csv', mode='r') as inp:
    reader = csv.reader(inp)
    dict_import = {rows[0]:rows[1] for rows in reader}

string_hostname = dict_import.get('Enter the Hostname')
string_public_ip = dict_import.get('Enter the Usable Public IP Address')
string_public_gateway_ip = dict_import.get('Enter the Public Gateway IP Address')
string_public_subnet = dict_import.get('Enter the Public Subnet (IE 255.255.255.252)')
string_lan_fortigate_ip = dict_import.get('Enter the LAN IP Address for the Fortigate')
string_lan_fortigate_subnet = str(dict_import.get('Enter the LAN IP Subnet Mask'))
string_dhcp_first_ip = dict_import.get('Enter the first Address in the DHCP Scope')
string_dhcp_last_ip = dict_import.get('Enter the last Address in the DHCP Scope')
string_dns_1_ip = dict_import.get('Enter the Primary DNS Server IP Address')
string_dns_2_ip = dict_import.get('Enter the Second DNS Server IP Address')
string_dns_3_ip = dict_import.get('Enter the Third DNS Server IP Address')
string_domain_name = dict_import.get('Enter the local domain (ie Entre.local)')

# Setup Log File
date_time = strftime("%Y%m%d-%H%M%S")
log_file_name = f'{string_hostname}-{date_time}.log'
log_file_path = os.path.join(program_folder, 'Logs',log_file_name)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(message)s')

logging.info(f"{'#'*20} Connecting to the device {'#'*20}")
net_connect = Netmiko(**fortigate_config)
logging.info(f"{'#'*20} Connected {'#'*20}")

# Identify Multiple WAN interfaces
output = net_connect.send_command("show system interface")

if 'wan1' in output:
    logging.info("Multiple WAN Ports Detected")
    string_wan_interface = 'wan1'
else:
    logging.info("Single WAN interface Detected.")
    string_wan_interface = 'wan'

# Identify LAN/Internal interfaces name.
output = net_connect.send_command("show system interface")

if 'internal' in output:
    logging.info("Internal Interface Identefied")
    string_lan_interface = 'internal'
else:
    logging.info("LAN Interface Identified.")
    string_lan_interface = 'lan'

# Initial config that changes the hostname, timezone and security ports.
config_initial =[
    'config system global',
	'set timezone 08',
	'set admin-port 8080',
	'set admin-sport 4443',
    'end'
]

config_hostname_line = 'set hostname ' + string_hostname

config_initial.insert(1, config_hostname_line)

send_config = net_connect.send_config_set(config_initial)

logging.info(send_config)

# SIP ALG Disable
config_sip_alg_disable_1 =[
    'config system settings',
	'set sip-expectation disable',
	'set sip-nat-trace disable',
	'set default-voip-alg-mode kernel-helper-based',
    'end'
]

send_config = net_connect.send_config_set(config_sip_alg_disable_1)

logging.info(send_config)

config_sip_alg_disable_2 =[
    'config system session-helper',
	'delete 13',
    'end'
]

send_config = net_connect.send_config_set(config_sip_alg_disable_2)

logging.info(send_config)

config_sip_alg_disable_3 =[
    'config voip profile',
	'edit default',
	'config sip',
	'set rtp disable',
	'end',
    'end'
]

send_config = net_connect.send_config_set(config_sip_alg_disable_3)

logging.info(send_config)

# WAN Static IP.
config_wan_ip =[
    'config system interface',
    'set mode static',
    'unset allowaccess',
    'end'
]

config_wan_ip_line_2 = 'edit ' + string_wan_interface
config_wan_ip_line_3 = 'set ip ' + string_public_ip + ' ' + string_public_subnet

config_wan_ip.insert(1, config_wan_ip_line_2)
config_wan_ip.insert(3, config_wan_ip_line_3)

send_config = net_connect.send_config_set(config_wan_ip)

logging.info(send_config)

# Static Route for WAN
config_static_route =[
    'config router static',
    'edit 1',
    'set status enable',
    'next',
    'end'
]

config_static_route_line_4 = 'set gateway ' + string_public_gateway_ip
config_static_route_line_5 = 'set device ' + string_wan_interface

config_static_route.insert(3,config_static_route_line_4)
config_static_route.insert(4,config_static_route_line_5)

send_config = net_connect.send_config_set(config_static_route)

# DHCP Settings
config_dhcp =[
    'config system dhcp server',
	'edit 1',
    'set lease-time 14400',
    'set dns-service specify',
	'config ip-range',
	'edit 1',
	'end',
    'end'
]

config_dhcp_line_4 = 'set default-gateway ' + string_lan_fortigate_ip
config_dhcp_line_8 = 'set start-ip ' + string_dhcp_first_ip
config_dhcp_line_9 = 'set end-ip ' + string_dhcp_last_ip
config_dhcp_line_11 = 'set dns-server1 ' + string_dns_1_ip
config_dhcp_line_12 = 'set dns-server2 ' + string_dns_2_ip
config_dhcp_line_13 = 'set dns-server3 ' + string_dns_3_ip

config_dhcp.insert(3, config_dhcp_line_4)
config_dhcp.insert(7, config_dhcp_line_8)
config_dhcp.insert(8, config_dhcp_line_9)
config_dhcp.insert(10, config_dhcp_line_11)
config_dhcp.insert(11, config_dhcp_line_12)
config_dhcp.insert(12, config_dhcp_line_13)

send_config = net_connect.send_config_set(config_dhcp)

logging.info(send_config)

# DNS Domain
config_dns =[
    'config system dns',
    'end'
]

config_dns_line_2 = 'set domain ' + string_domain_name

config_dns.insert(1, config_dns_line_2)

send_config = net_connect.send_config_set(config_dns)

logging.info(send_config)

# VIP Rules
vips_folder_path = os.path.join(program_folder, 'VIPs')

another_vip = True
while another_vip == True:
    user_response_another_vip = input("Do you want to add another VIP? (yes/no/): ")
    if user_response_another_vip.lower() in ["yes", "y"]:
        file_list = os.listdir(vips_folder_path)
        selected_file = None
        while not selected_file:
            for i, file in enumerate(file_list):
                print(f'{i+1}. {file}')
            user_input = input("Please select a file by typing the number: ")
            try:
                selected_file = file_list[int(user_input)-1]
                selected_file_path = os.path.join(vips_folder_path, selected_file)
                # read csv file as a list of lists
                with open(selected_file_path, 'r') as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader = csv.reader(read_obj)
                    # Pass reader object to list() to get a list of lists
                    list_of_rows = list(csv_reader)
                    
                    x = 0

                    #int_loop_max = len(list_of_rows) - 1

                for x in range(len(list_of_rows)):
                    if x == 0:
                        continue

                    #if x == int_loop_max:
                    # send_config = net_connect.send_config_set("end")

                    # logging.info(send_config)
                    #   continue

                    config_vip =[
                        'config firewall vip',
                        'set portforward enable',
                        'next'
                    ]
                    
                    string_config_vip_line_2 = 'edit "' + list_of_rows[x][0] + '"'
                    string_config_vip_line_4 = 'set mappedip ' + list_of_rows[x][2]
                    string_config_vip_line_5 = 'set extintf ' + string_wan_interface
                    string_config_vip_line_7 = 'set protocol ' + list_of_rows[x][4]
                    if "icmp" not in list_of_rows[x][4]:
                        string_config_vip_line_8 = 'set extport ' + list_of_rows[x][5]
                        string_config_vip_line_9 = 'set mappedport ' + list_of_rows[x][6]

                    config_vip.insert(1, string_config_vip_line_2)
                    config_vip.insert(3, string_config_vip_line_4)
                    config_vip.insert(4, string_config_vip_line_5)
                    config_vip.insert(5, string_config_vip_line_7)
                    if "icmp" not in list_of_rows[x][4]:
                        config_vip.insert(6, string_config_vip_line_8)
                        config_vip.insert(7, string_config_vip_line_9)

                    #print(config_vip)
                    if x != 1:
                        config_vip.remove('config firewall vip')

                    send_config = net_connect.send_config_set(config_vip)

                    logging.info(send_config)

                send_config = net_connect.send_config_set("end")

                logging.info(send_config)

                # VIP Group
                # read csv file as a list of lists
                with open(selected_file_path, 'r') as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader = csv.reader(read_obj)
                    # Pass reader object to list() to get a list of lists
                    list_of_rows = list(csv_reader)
                    
                    x = 0

                    int_loop_max = len(list_of_rows) - 1

                    list_vip_group = []

                for x in range(len(list_of_rows)):
                    if x == 0:
                        list_vip_group.append(list_of_rows[0][8])

                    if x == int_loop_max:
                        continue

                    x += 1
                    
                    list_vip_group.append(list_of_rows[x][0])

                string_vip_group=''

                for word in list_vip_group:
                    string_vip_group += ' "' + str(word) + '"'

                string_vip_group_name_remove = ' "' + list_of_rows[0][8] + '" '
                string_vip_group_2 = string_vip_group.replace(string_vip_group_name_remove, "")

                config_vip_grp =[
                        'config firewall vipgrp',
                        'next',
                        'end'
                        ]

                string_vip_grp_name = list_of_rows[0][8]
                string_config_vip_grp_line_2 = 'edit "' + string_vip_grp_name + '"'
                string_config_vip_grp_line_3 = 'set interface ' + string_wan_interface
                string_config_vip_grp_line_4 = 'set member ' + string_vip_group_2

                config_vip_grp.insert(1, string_config_vip_grp_line_2)
                config_vip_grp.insert(2, string_config_vip_grp_line_3)
                config_vip_grp.insert(3, string_config_vip_grp_line_4)

                send_config = net_connect.send_config_set(config_vip_grp)

                logging.info(send_config)

                # Address Objects
                # read csv file as a list of lists
                with open('addresses.csv', 'r') as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader = csv.reader(read_obj)
                    # Pass reader object to list() to get a list of lists
                    list_of_rows = list(csv_reader)
                    
                    x = 0

                    #int_loop_max = len(list_of_rows) - 1

                for x in range(len(list_of_rows)):
                    if x == 0:
                        continue

                    #if x == int_loop_max:
                    # send_config = net_connect.send_config_set("end")

                    # logging.info(send_config)
                    #   continue

                    config_addr =[
                        'config firewall address',
                        'next'
                    ]
                    
                    type_compare = str(list_of_rows[x][1])

                    string_config_addr_line_2 = 'edit "' + list_of_rows[x][0] + '"'
                    string_config_addr_line_3 = 'set type ' + list_of_rows[x][1]
                    if type_compare == 'fqdn':
                        logging.info("Set FQDN")
                        string_config_addr_line_4 = 'set fqdn ' + list_of_rows[x][2]
                    else:
                        string_config_addr_line_4 = 'set subnet ' + list_of_rows[x][2]


                    config_addr.insert(1, string_config_addr_line_2)
                    config_addr.insert(2, string_config_addr_line_3)
                    config_addr.insert(3, string_config_addr_line_4)

                    if x != 1:
                        config_addr.remove('config firewall address')

                    send_config = net_connect.send_config_set(config_addr)

                    logging.info(send_config)

                send_config = net_connect.send_config_set("end")

                logging.info(send_config)

                # Address Object Group
                # read csv file as a list of lists
                with open('addresses.csv', 'r') as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader = csv.reader(read_obj)
                    # Pass reader object to list() to get a list of lists
                    list_of_rows = list(csv_reader)
                    
                    x = 0

                    int_loop_max = len(list_of_rows) - 1

                    list_addr_grp = []

                for x in range(len(list_of_rows)):
                    if x == 0:
                        list_addr_grp.append(list_of_rows[0][3])

                    if x == int_loop_max:
                        continue

                    x += 1
                    
                    list_addr_grp.append(list_of_rows[x][0])

                string_addr_grp=''

                for word in list_addr_grp:
                    string_addr_grp += ' ' + str(word)

                
                #print(string_addr_grp)
                string_addr_grp_name_remove = ' ' + list_of_rows[0][3] + ' '
                #print(string_addr_grp_name_remove)
                string_addr_grp_2 = string_addr_grp.replace(string_addr_grp_name_remove, "")
                #print(string_addr_grp_2)
                config_addr_grp =[
                        'config firewall addrgrp',
                        'next',
                        'end'
                        ]

                string_addr_grp_name = list_of_rows[0][3]
                string_config_vip_grp_line_2 = 'edit "' + string_addr_grp_name + '"'
                string_config_vip_grp_line_3 = 'set member ' + string_addr_grp_2

                config_addr_grp.insert(1, string_config_vip_grp_line_2)
                config_addr_grp.insert(2, string_config_vip_grp_line_3)

                send_config = net_connect.send_config_set(config_addr_grp)

                logging.info(send_config)

                # Firewall Policies
                config_fw_pol =[
                    'config firewall policy',
                    'edit 2',
                    'set action accept',
                    'set status enable',
                    'set schedule "always"',
                    'set service ALL',
                    'next',
                    'end'
                ]

                string_config_fw_pol_line_3 = 'set srcintf ' + string_wan_interface
                string_config_fw_pol_line_4 = 'set dstintf ' + string_lan_interface
                string_config_fw_pol_line_5 = 'set srcaddr "' + string_addr_grp_name + '"'
                string_config_fw_pol_line_6 = 'set dstaddr "' + string_vip_grp_name + '"'

                config_fw_pol.insert(2, string_config_fw_pol_line_3)
                config_fw_pol.insert(3, string_config_fw_pol_line_4)
                config_fw_pol.insert(4, string_config_fw_pol_line_5)
                config_fw_pol.insert(5, string_config_fw_pol_line_6)

                send_config = net_connect.send_config_set(config_fw_pol)

                logging.info(send_config)


            except (IndexError, ValueError):
                print("Invalid input, please try again.")
        print(f"You have selected: {selected_file}")
    elif user_response_another_vip.lower() in ["no", "n"]:
        logging.info("Leaving VIP Loop")
        break
    else:
        print("Do you want to add another VIP? (yes/no/): ")

# Check if DMZ interface Exists
output = net_connect.send_command("show syste interface")

# If DMZ interface exists Change the IP of the Interface. If not Logs there is not interface.
if 'dmz' in output:
    logging.info("DMZ Interface Found Modifying IP Address")
    config_DMZ_update =[
        'config system interface',
        'edit dmz',
        'set ip 10.10.1.254 255.255.255.0',
        'next',
        'end'
    ]

    send_config = net_connect.send_config_set(config_DMZ_update)

    logging.info(send_config)
else:
    logging.info("There is no DMZ.")

# LAN IP
config_lan_ip =[
    'config system interface',
    'set allowaccess http https ping ssh',
    'set vdom root',
    'set secondary-IP enable',
    'config secondaryip',
    'edit 1',
    'set ip 10.10.10.254 255.255.255.0',
    'set allowaccess ping https ssh snmp',
    'next',
    'end',
    'end'
]

string_conf_lan_ip_line_2 = 'edit ' + string_lan_interface
string_conf_lan_ip_line_3 = 'set ip ' + string_lan_fortigate_ip + ' ' + string_lan_fortigate_subnet

config_lan_ip.insert(1, string_conf_lan_ip_line_2)
config_lan_ip.insert(2, string_conf_lan_ip_line_3)

send_config = net_connect.send_config_set(config_lan_ip)

logging.info(send_config)

#Add Widget to default Dashboard for Bandwidth Monitor for LAN Interface
# config_gui_widget =[
#     'config system admin',
#     'edit admin',
#     'config gui-dashboard',
#     'edit 1',
#     'set name "Main"',
#     'config widget',
#     'edit 1',
#     'set type fortiview',
#     'set width 2',
#     'set height 1',
#     'set fortiview-type "destination"',
#     'set fortiview-sort-by "bandwidth"',
#     'set fortiview-timeframe "realtime"',
#     'set fortiview-visualization "table"',
#     'next',
#     'edit 2',
#     'set type fortiview',
#     'set x-pos 1',
#     'set width 2',
#     'set height 1',
#     'set fortiview-type "source"',
#     'set fortiview-sort-by "bandwidth"',
#     'set fortiview-timeframe "realtime"',
#     'set fortiview-visualization "table"',
#     'next',
#     'edit 3',
#     'set type fortiview',
#     'set x-pos 2',
#     'set width 2',
#     'set height 1',
#     'set fortiview-type "website"',
#     'set fortiview-sort-by "bandwidth"',
#     'set fortiview-timeframe "realtime"',
#     'set fortiview-visualization "table"',
#     'next',
#     'edit 4',
#     'set type tr-history',
#     'set x-pos 3',
#     'set width 2',
#     'set height 1',
#     'set interface "lan"',
#     'next',
#     'edit 5',
#     'set type tr-history',
#     'set x-pos 4',
#     'set width 2',
#     'set height 1',
#     'set interface "wan"',
#     'next',
#     'edit 6',
#     'set type ipsec-vpn',
#     'set x-pos 5',
#     'set width 2',
#     'set height 1',
#     'next',
#     'edit 7',
#     'set type ssl-vpn',
#     'set x-pos 6',
#     'set width 2',
#     'set height 1',
#     'next',
#     'next',
#     'end',
#     'end',
#     'end'
# ]

# send_config = net_connect.send_config_set(config_gui_widget)

# logging.info(send_config)



# Backup Config
