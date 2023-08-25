##############################################################################
############################### Discovery Module #############################
##############################################################################
"""
Python Program grab the information of the PC. 
Created by Josh Trouille 10/01/2019

"""

################################### Imports ##################################
import os
import sys
import wmi # Needs to be installed. 
import math
import io
import psutil # Needs to be installed. 
import winreg
import subprocess


############################## Global Variables ##############################

## Heading used in each sections.
# Variables used in the heading function.
global center_heading
center_heading = 'Center Heading Placeholder'
dash = '-' * 70

# Heading fuction that is used to seperate and hightlight each section. 
def dash_heading():
    print('\n\n')
    print(dash)
    print('{:-^70}'.format(' ' + center_heading + ' '))
    print(dash)

# Gathers Computer Hardware related information.
for sys in wmi.WMI().Win32_ComputerSystem():
    sys_hostname = sys.Name
    sys_domain = sys.Domain
    sys_domainrole = sys.DomainRole
    sys_manufacturer = sys.Manufacturer
    sys_model = sys.Model
    sys_make_model = ("%s %s" % (sys_manufacturer, sys_model))
    sys_physical_memory = sys.TotalPhysicalMemory
    sys_username = sys.UserName

# Gathers Computer BIOS Information.
for bio in wmi.WMI().Win32_BIOS():
    bio_serial_number = bio.SerialNumber

## Detailed CPU Information Variables.
cpu_physical_cores = psutil.cpu_count(logical=False)
cpu_virtual_cores = psutil.cpu_count(logical=True)
cpu_freq = psutil.cpu_freq()
cpu_max_freq = cpu_freq.max
cpu_min_freq = cpu_freq.min
cpu_current_freq = cpu_freq.current
cpu_core_usage_set = []
cpu_core_usage_get = psutil.cpu_percent(interval=1, percpu=True)
for i in range(cpu_virtual_cores):
    core_number = i
    core_usage_per_core = cpu_core_usage_get[i]
    core_output = (f"Core{core_number}: {core_usage_per_core}").split()
    cpu_core_usage_set.append(core_output)
cpu_total_cpu_usage = (f"Total_Usage: {psutil.cpu_percent()}%").split()
cpu_core_usage_set.append(cpu_total_cpu_usage)

## Gathers Processor information.
for cpu in wmi.WMI().Win32_Processor():
    cpu_name = cpu.Name.strip()
    cpu_bandwidth = str(cpu.DataWidth)
    cpu_socket = cpu.SocketDesignation

## Gathers OS related information.
for os in wmi.WMI().Win32_OperatingSystem():
    os_name = os.Caption
    os_architecture = os.OSArchitecture
    os_full_name = ("%s (%s)" % (os_name, os_architecture))

# Gathers Physical Drive Information
p_hdd_dataset = []
for p_disk in wmi.WMI().Win32_DiskDrive():
    p_hdd_id = p_disk.DeviceID.replace('\\\\.\\PHYSICALDRIVE', '')
    p_hdd_model = p_disk.Model
    p_hdd_serial = p_disk.SerialNumber.strip()
    p_hdd_size = p_disk.Size
    p_hdd_smart = p_disk.Status
    p_hdd_output = [p_hdd_id, p_hdd_model, p_hdd_serial, p_hdd_size, p_hdd_smart]
    p_hdd_dataset.append(p_hdd_output)
    

# Detailed Memory Information Calls
mem_dataset = []
for ram in wmi.WMI().Win32_physicalmemory():
    mem_bank_lable = ram.BankLabel
    mem_capacity = ram.Capacity
    mem_speed = ram.Speed
    mem_device_locator = ram.DeviceLocator
    mem_manufacturer = ram.Manufacturer
    mem_partnumber = ram.PartNumber.strip()
    mem_serialnumber = ram.SerialNumber
    mem_output = [mem_bank_lable, mem_capacity, mem_speed, mem_device_locator, mem_manufacturer, mem_partnumber, mem_serialnumber]
    mem_dataset.append(mem_output)

################ Functions that are called by later functions ################

# Conversion for bytes using a 1000 base for HDD byte conversion.
def convert_bytes_1000(size_bytes): 
    if size_bytes == 0: 
        return "0B" 
    size_name = ('', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa', 'zetta', 'yotta') 
    i = int(math.floor(math.log(size_bytes, 1000)))
    power = math.pow(1000, i) 
    size = round(size_bytes / power, 2) 
    return "{} {}".format(math.ceil(size), size_name[i]+'byte')

# Conversion for bytes using a 1024 base for normal byte conversion.
def convert_bytes_1024(size_bytes): 
    if size_bytes == 0: 
        return "0B" 
    size_name = ('', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa', 'zetta', 'yotta') 
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i) 
    size = round(size_bytes / power, 2) 
    return "{} {}".format(math.ceil(size), size_name[i]+'byte')

# Takes Dataset and outputs the data in a left and right format.
def data_2_output():
    global data
    for i in range(len(data)):
        print('{:<25s}{:>45s}'.format(data[i][0],data[i][1]))
    print(dash)

def data_3_output():
    dash = '-' * 137
    global data
    for i in range(len(data)):
        print('{:<70s}|{:<20}|{:>45s}'.format(data[i][0],data[i][1],data[i][2]))
    print(dash)

# Changes the system role variable from an integer to the coresponding string.
def sys_role():
    global sys_domainrole
    if sys_domainrole == 0:
        sys_domainrole = 'Standalone Workstation'
    elif sys_domainrole == 1:
        sys_domainrole = 'Domain Member Workstation'
    elif sys_domainrole == 2:
        sys_domainrole = 'Standalone Server'
    elif sys_domainrole == 3:
        sys_domainrole = 'Domain Member Server'
    elif sys_domainrole == 4:
        sys_domainrole = 'Backup Domain Controller'
    elif sys_domainrole == 5:
        sys_domainrole = 'Primary Domain Controller'
    else:
        sys_domainrole = 'error'

# Decodes the Windows Key
def decode_windows_key(rpk):
    rpkOffset = 52
    i = 28
    possible_chars = "BCDFGHJKMPQRTVWXY2346789"
    product_key = ""

    while i >= 0:
        dwAccumulator = 0
        j = 14
        while j >= 0:
            dwAccumulator = dwAccumulator * 256
            d = rpk[j + rpkOffset]
            if isinstance(d, str):
                d = ord(d)
            dwAccumulator = d + dwAccumulator
            rpk[j + rpkOffset] = int(dwAccumulator / 24) if int(dwAccumulator / 24) <= 255 else 255
            dwAccumulator = dwAccumulator % 24
            j = j - 1
        i = i - 1
        product_key = possible_chars[dwAccumulator] + product_key

        if ((29 - i) % 6) == 0 and i != -1:
            i = i - 1
            product_key = "-" + product_key
    return product_key

# Finds the Registry Location of the Windows Key
def get_key_from_reg_location(key, value='DigitalProductID'):
    arch_keys = [0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]
    for arch in arch_keys:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ | arch)
            value, type = winreg.QueryValueEx(key, value)
            # Return the first match
            return decode_windows_key(list(value))
        except (FileNotFoundError, TypeError) as e:
            pass

# Grab Windows Key from Registry
def windows_product_key_reg():
    return get_key_from_reg_location('SOFTWARE\Microsoft\Windows NT\CurrentVersion')
    print('Key WMI: %s' % get_key_from_reg_location('SOFTWARE\Microsoft\Windows NT\CurrentVersion'))

# Grab Windows Key using WMI
def windows_product_key_wmi():
    product_key = wmi.WMI().softwarelicensingservice()[0].OA3xOriginalProductKey
    print('Key WMI: %s' % product_key)
    if product_key != '':
        return product_key
    else:
        return None

################ Functions that require functions above. ################

# Basic Computer informaiton, Hostname, Domain, User etc.
def basic_information():
    global sys_domainrole
    global center_heading
    global data
    
    # Genterates Heading for the sections
    center_heading = 'Basic Information'
    dash_heading()
    sys_role()
    wmi_key = str(windows_product_key_wmi())
    reg_key = str(windows_product_key_reg())
        
    # Creates Dataset for output.
    data = [
    ['Host Name:', sys_hostname],
    ['Domain:', sys_domain],
    ['System Type:', sys_domainrole],
    ['Operating System: ', os_full_name],
    ['Operating System Key: ', wmi_key],
    ['', reg_key],
    ['System Serial Number', bio_serial_number],
    ['Model:', sys_make_model],
    ['Processor:', cpu_name],
    ['Memory:', convert_bytes_1024(int(sys_physical_memory))],
    ['Logged in User:', sys_username],
    ]

    data_2_output() # Outputs the dataset just created.

# Finds the status of the firewall
def firewall_status():
    global data
    firewall_domain_status = str(subprocess.Popen('netsh advfirewall show domainprofile state', stdout=subprocess.PIPE).stdout.read())
    if "ON" in firewall_domain_status:
        firewall_domain_status = "On"
    elif "OFF" in firewall_domain_status:
        firewall_domain_status = "Off"
    else:
        firewall_domain_status = "Error"
    firewall_private_status = str(subprocess.Popen('netsh advfirewall show privateprofile state', stdout=subprocess.PIPE).stdout.read())
    if "ON" in firewall_private_status:
        firewall_private_status = "On"
    elif "OFF" in firewall_private_status:
        firewall_private_status = "Off"
    else:
        firewall_private_status = "Error"
    firewall_public_status = str(subprocess.Popen('netsh advfirewall show publicprofile state', stdout=subprocess.PIPE).stdout.read())
    if "ON" in firewall_public_status:
        firewall_public_status = "On"
    elif "OFF" in firewall_public_status:
        firewall_public_status = "Off"
    else:
        firewall_public_status = "Error"
    data = [
    ['Domain Profile', firewall_domain_status],
    ['Private Profile', firewall_private_status],
    ['Public Profile', firewall_public_status]
    ]

# Detailed Logical Hard Disk. Pulls information about Letter drives. 
def detailed_logical_disk():
    global center_heading
    center_heading = 'Detailed Logical HDD'
    dash_heading()
    for disk in wmi.WMI().Win32_LogicalDisk():
        l_hdd_name = disk.name
        l_hdd_description = disk.description
        l_hdd_filesys = disk.filesystem
        if l_hdd_description == "Local Fixed Disk":
            l_hdd_freespace = convert_bytes_1024(int(disk.freespace))
            l_hdd_size = convert_bytes_1024(int(disk.size))
            l_hdd_volumename = disk.volumename
            print(f'Drive: {l_hdd_name}')
            print(f'Name: {l_hdd_volumename}')
            print(f'Type: {l_hdd_description}')
            print(f'FileSystem: {l_hdd_filesys}')
            print(f'Freespace: {l_hdd_freespace}')
            print(f'Size: {l_hdd_size}')
        elif l_hdd_description == "CD-ROM Disc":
            print(f'Drive: {l_hdd_name}')
            print(f'Name: {l_hdd_volumename}')
            print(f'Type: {l_hdd_description}')
        else:
            print(dash)
            print("Drive type not in program")
        print(dash)

# Detailed Memory Information
# Converts Capacity into a more readable, then prints out all information. 
# Status and SKU commenented out due to not pulling information on my PC.
def detailed_memory():
    global center_heading
    center_heading = 'Detailed Memory'
    dash_heading()
    for i in mem_dataset:
        ram = i
        mem_bank_lable = ram[0]
        mem_capacity = convert_bytes_1024(int(ram[1]))
        mem_speed = str(ram[2])
        mem_device_locator = ram[3]
        mem_manufacturer = ram[4]
        mem_partnumber = ram[5]
        mem_serialnumber = ram[6]
        global data
        data = [
        ['Bank Label:', mem_bank_lable],
        ['Slot:', mem_device_locator],
        ['Manufacturer:', mem_manufacturer],
        ['Capacity:', mem_capacity],
        ['Speed:', mem_speed],
        ['Part Number:', mem_partnumber],
        ['Serial Number:', mem_serialnumber]
        ]
        data_2_output()

# Detailed CPU Fuction to convert the size data set and print out detailed report.
def detailed_physical_disk():
    global center_heading
    center_heading = 'Detailed Physical HDD'
    dash_heading()
    for i in p_hdd_dataset:
        disk = i
        p_disk_id = disk[0]
        p_disk_model = disk[1]
        p_disk_serial = disk[2]
        p_disk_size = convert_bytes_1024(int(disk[3]))
        p_disk_smart = disk[4]
        global data
        data = [
        ['Disk ID:', p_disk_id],
        ['Disk Model:', p_disk_model],
        ['Disk Serial Number:', p_disk_serial],
        ['Disk Size: ', p_disk_size],
        ['Smart Status:', p_disk_smart]
        ]
        data_2_output()

# Detailed Processor Information 
def detailed_processor():
    global center_heading
    center_heading = 'Detailed CPU Information'
    dash_heading()
    global data
    data = [
        ['CPU Name:', cpu_name],
        ['CPU Bandwidth:', cpu_bandwidth],
        ['CPU Socket:', cpu_socket]
        ]
    data_2_output()
    
    center_heading = 'CPU Core Usage'
    dash_heading()
    data = cpu_core_usage_set # Outputs the data for core usaged to a dataset for output.
    data_2_output()

# Builds list of all installed software.
def software_list_build(hive, flag):
    
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

# Takes the list build in def software_list_build() and splits each 
# data set into three columns and output the data in the terminal.
def software_list_information():
    software_list = software_list_build(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + software_list_build(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + software_list_build(winreg.HKEY_CURRENT_USER, 0)
    global center_heading
    center_heading = 'Installed Software'
    dash_heading()
    global data 
    data = [['Software Name', 'Version', 'Publisher']]
    data_3_output()
    for software in software_list:
        software_name =  software['name']
        software_version = software['version']
        software_publisher = software['publisher']
        data = [[software_name, software_version, software_publisher]]
        data_3_output()
    print('Number of installed apps: %s' % len(software_list))

################ Main Function that calls other functions and controlls output ################
def main():
    basic_information()
    detailed_logical_disk()
    detailed_physical_disk()
    detailed_processor()
    detailed_memory()
    software_list_information()
    firewall_status()
main()