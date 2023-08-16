import socket
import sys
import traceback
import os
import subprocess
import re
import time
import datetime
from inspect import getfullargspec
from tkinter import messagebox
import admin_test
import db_handler
import pwd,grp
import lsb_release
import platform
import configparser

#check
# Scoring Report creation
def draw_head():
    file = open(scoreIndex, 'w+')
    file.write('<!doctype html><html><head><title>CSEW Score Report</title><meta http-equiv="refresh" content="60"></head><body style="background-color:powderblue;">''\n')
    file.write('<table align="center" cellpadding="10"><tr><td><img src="C:/CyberPatriot/CCC_logo.png"></td><td><div align="center"><H2>Cyberpatriot Scoring Engine:Windows v1.1</H2></div></td><td><img src="C:/CyberPatriot/SoCalCCCC.png"></td></tr></table>If you see this wait a few seconds then refresh<br><H2>Your Score: #TotalScore#/' + str(menuSettings["Tally Points"]) + '</H2><H2>Vulnerabilities: #TotalVuln#/' + str(menuSettings["Tally Vulnerabilities"]) + '</H2><hr>')
    file.close()


def record_hit(name, points):
    global total_points, total_vulnerabilities
    write_to_html(('<p style="color:green">' + name + ' (' + str(points) + ' points)</p>'))
    total_points += int(points)
    total_vulnerabilities += 1


def record_miss(name):
    if not menuSettings['Silent Mode']:
        write_to_html(('<p style="color:red">MISS ' + name + ' Issue</p>'))


def record_penalty(name, points):
    global total_points
    write_to_html(('<p style="color:red">' + name + ' (' + str(points) + ' points)</p>'))
    total_points -= int(points)


def draw_tail():
    write_to_html('<hr><div align="center"><b>Coastline College</b>')
    #write_to_html('<hr><div align="center"><b>Coastline College</b><br>Created by Shaun Martin, Anthony Nguyen, and Minh-Khoi Do</br><br>Feedback welcome: <a href="mailto:smartin94@student.cccd.edu?Subject=CSEW Scoring Engine" target="_top">smartin94@student.cccd.edu</a></div>')
    #print(str(total_points) + ' / ' + str(menuSettings["Tally Points"]) + '\n' + str(total_vulnerabilities) + ' / ' + str(menuSettings["Tally Vulnerabilities"]))
    replace_section(scoreIndex, '#TotalScore#', str(total_points))
    replace_section(scoreIndex, '#TotalVuln#', str(total_vulnerabilities))
    replace_section(scoreIndex, 'If you see this wait a few seconds then refresh', '')

    #check
    path = os.path.join(Desktop, 'ScoreReport.lnk')
    target = scoreIndex
    icon = os.path.join(index, 'scoring_engine_logo_windows_icon_5TN_icon.ico')
    #fix
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    #check
    shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()


# Extra Functions
def check_runas():
    if not admin_test.isUserAdmin():
        messagebox.showerror('Administrator Access Needed', 'Please make sure the scoring engine is running as admin.')
        exit(admin_test.runAsAdmin())


def check_score():
    global total_points, total_vulnerabilities
    try:

        menuSettings["Current Vulnerabilities"] = total_vulnerabilities
        if total_points > menuSettings["Current Points"]:
            menuSettings["Current Points"] = total_points
            Settings.update_score(menuSettings)
            w.ShowWindow('Score Update', 'You gained points!!')
        elif total_points < menuSettings["Current Points"]:
            menuSettings["Current Points"] = total_points
            Settings.update_score(menuSettings)
            w.ShowWindow('Score Update', 'You lost points!!')
        if total_points == menuSettings["Tally Points"] and total_vulnerabilities == menuSettings["Tally Vulnerabilities"]:
            w.ShowWindow('Image Completed', 'Congratulations you finished the image.')
    except:
        #check
        f = open('scoring_engine.log', 'w')
        e = traceback.format_exc()
        #if "KeyboardInterrupt" in e:
        #sys.exit()
        f.write(str(e))
        f.close()
        messagebox.showerror('Crash Report','The scoring engine has stopped working, a log has been saved to ' + os.path.abspath('scoring_engine.log'))
        # sys.exit()


def write_to_html(message):
    file = open(scoreIndex, 'a')
    file.write(message)
    file.close()


def replace_section(loc, search, replace):
    lines = []
    with open(loc) as file:
        for line in file:
            line = line.replace(search, replace)
            lines.append(line)
    with open(loc, 'w') as file:
        for line in lines:
            file.write(line)


# Option Check
def forensic_question(vulnerability):
    for idx, vuln in enumerate(vulnerability):
        if vuln != 1:
            file = open(vulnerability[vuln]["Location"], 'r')
            content = file.read().splitlines()
            for c in content:
                if 'ANSWER:' in c:
                    if vulnerability[vuln]["Answers"] in c:
                        record_hit('Forensic question number ' + str(idx) + ' has been answered.', vulnerability[vuln]['Points'])
                    else:
                        record_miss('Forensic Question')



#fixed
def critical_users(vulnerability):
    users = pwd.getpwall()
    user_list = []
    for user in users:
        user_list.append(user.Name)[0]
    for vuln in vulnerability:
        if vuln != 1:
            if vulnerability[1]['User Name'] not in user_list:
                record_penalty(vulnerability[vuln]['User Name'] + ' was removed.', vulnerability[vuln]['Points'])


#fix
def users_manipulation(vulnerability, name):
    users = pwd.getgrall()
    user_list = []
    for user in users:
        user_list.append(user)[0]
    if name == "Add User":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] in user_list:
                    record_hit(vulnerability[vuln]['User Name'] + ' has been added.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')
    if name == "Remove User":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] not in user_list:
                    record_hit(vulnerability[vuln]['User Name'] + ' has been removed.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')


'''
def turn_on_firewall(vulnerability, name):
    file = open('firewall_status.txt')
    content = file.read()
    file.close()
    if name == "Turn On Domain Firewall":
        firewall = re.search(r"Domain Profile Settings: \n-+\n\w+\s+\w+\n\n", content).group(0)
        if re.search("ON", firewall):
            record_hit('Firewall has been turned on.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Turn On Private Firewall":
        firewall = re.search(r"Private Profile Settings: \n-+\n\w+\s+\w+\n\n", content).group(0)
        if re.search("ON", firewall):
            record_hit('Firewall has been turned on.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Turn On Public Firewall":
        firewall = re.search(r"Public Profile Settings: \n-+\n\w+\s+\w+\n", content).group(0)
        if re.search("ON", firewall):
            record_hit('Firewall has been turned on.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
'''
#fix
def firewallVulns(vulnerability, name):
    try:
        # Run the ufw status command and capture the output
        completed_process = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True, check=True)
        if ' active' in completed_process.stdout.strip():
            record_hit('Domain Firewall has been turned on.', vulnerability[1]['Points'])
        else:
            record_miss('Firewall Management')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def check_tcp(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Set a timeout for the connection attempt
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def check_udp(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Set a timeout for the socket operations
    try:
        sock.sendto(b"", (host, port))
        data, addr = sock.recvfrom(1024)
        sock.close()
        return True
    except socket.timeout:
        sock.close()
        return False

def portVulns(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            if str.upper(vulnerability[vuln]['Protocol']) is 'TCP':
                if (check_tcp(vulnerability[vuln]['IP']), vulnerability[vuln]['Port']):
                    record_hit('Port ' + Vulnerabilities[vuln]['Port'] + ' is opened.', vulnerability[vuln]['Points'])
                else: 
                    record_miss('Firewall Management')
            else:
                if (check_udp(vulnerability[vuln]['IP']), vulnerability[vuln]['Port']):
                    record_hit('Port ' + Vulnerabilities[vuln]['Port'] + ' is opened.', vulnerability[vuln]['Points'])
                else: 
                    record_miss('Firewall Management')


def audit_check():
    try:
        cp = subprocess.run(['systemctl','is-active','auditd'],capture_output=True,text=True,check=True)
        captured = cp.stdout.strip()
        if 'inactive' in captured:
            return False
        else:
            return True
    except:
            return False


#fix
def local_group_policy(vulnerability, name):
    if name == "Minimum  Age":
        if 30 <= (int(re.search(r"(?<=PASS_MIN_DAYS = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=PASS_MIN_DAYS = )\d+", policy_settings_content) else 0) <= 60:
            record_hit('Minimum password age is set to 30-60.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Maximum Password Age":
        if 60 <= (int(re.search(r"(?<=PASS_MAX_DAYS = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=PASS_MAX_DAYS = )\d+", policy_settings_content) else 0) <= 90:
            record_hit('Maximum password age is set to 60-90.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Maximum Login Tries":
        if 5 <= (int(password_settings_content.get('retry')) if int(password_settings_content.get('retry')) else 0) <= 10:
            record_hit('Maximum login tries is set to 5-10.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management1')
    if name == "Lockout Duration":
        if 30 <= (int(re.search(r"(?<=LOGIN_TIMEOUT = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=LOGIN_TIMEOUT = )\d+", policy_settings_content) else 0):
            record_hit('Lockout duration set is set to 30.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management2')
            #get rid of the following
            #fix
    if name == "Lockout Reset Duration":
        if 30 <= (int(re.search(r"(?<=ResetLockoutCount = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=ResetLockoutCount = )\d+", policy_settings_content) else 0):
            record_hit('Lockout counter reset is set to 30.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Minimum Password Length":
        if 10 <= (int(password_settings_content.get('minlen')) if int(password_settings_content.get('minlen')) else 0):
            record_hit('Minimum password length is set to 10 or more.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Password History":
        if 5 <= int(password_settings_content.get('remember')) if int(password_settings_content.get('remember')) else 0:
            record_hit('Password history size is set to 5 or more.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
            #wip         
        '''
    if name == "Password Complexity":
        if (int(re.search(r"(?<=PasswordComplexity = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=PasswordComplexity = )\d+", policy_settings_content) else 0) == 1:
            record_hit('Password complexity has been enabled.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
            
    if name == "Reversible Password Encryption":
        if (int(re.search(r"(?<=ClearTextPassword = )\d+", policy_settings_content).group(0)) if re.search(r"(?<=ClearTextPassword = )\d+", policy_settings_content) else 1) == 0:
            record_hit('Reversible password encryption has been Disabled.', vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
            '''
    if name == "Audit":
        if audit_check:
            record_hit('Auditing is on.',  vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
#wip         
'''
    if name == "Do Not Require CTRL_ALT_DEL":
        if (int(re.search(r"(?<=MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\DisableCAD=\d,)\d+", policy_settings_content).group(0)) if re.search(r"(?<=MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\DisableCAD=\d,)\d+", policy_settings_content) else 1) == 0:
            record_hit('Do not require CTRL + ALT + DEL has been disabled.',  vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')
    if name == "Don't Display Last User":
        if (int(re.search(r"(?<=MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\DontDisplayLastUserName=\d,)\d+", policy_settings_content).group(0)) if re.search(r"(?<=MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\DontDisplayLastUserName=\d,)\d+", policy_settings_content) else 0) == 1:
            record_hit('Don\'t Display Last User Name has been enabled.',  vulnerability[1]['Points'])
        else:
            record_miss('Policy Management')'''


#test
def group_manipulation(vulnerability, name):
    groups = grp.getgrall()
    if name == "Add Admin":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] in grp.getgrnam('sudo')[3]:
                    record_hit(vulnerability[vuln]['User Name'] + ' has been promoted to administrator.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')
    if name == "Remove Admin":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] not in grp.getgrnam('sudo')[3]:
                    record_hit(vulnerability[vuln]['User Name'] + ' has been demoted to standard user.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')
    if name == "Add User to Group":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] in grp.getgrnam[vulnerability[vuln]['Group Name']][3]:
                    record_hit(vulnerability[vuln]['User Name'] + ' is in the ' + vulnerability[vuln]['Group Name'] + ' group.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')
    if name == "Remove User from Group":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]['User Name'] not in grp.getgrnam[vulnerability[vuln]['Group Name']][3]:
                    record_hit(vulnerability[vuln]['User Name'] + ' is no longer in the ' + vulnerability[vuln]['Group Name'] + ' group.', vulnerability[vuln]['Points'])
                else:
                    record_miss('User Management')


#check
def user_change_password(vulnerability):
    for vuln in vulnerability:
        file = open('user_' + vulnerability[vuln]['User Name'].lower() + '.txt')
        content = file.read()
        file.close()
        last_changed_list = re.search(r"(?<=Password last set\s{12})\S+", content).group(0).split('/')
        last_changed = ''
        for date in last_changed_list:
            if int(date) < 10:
                temp = '0' + date
            else:
                temp = date
            last_changed = last_changed + temp + '/'
        if datetime.datetime.now().strftime('%m/%d/%Y') == last_changed.rsplit('/', 1)[0]:
            record_hit(vulnerability[vuln]['User Name'] + '\'s password was changed.', vulnerability[vuln]['Points'])
        else:
            record_miss('Policy Management')


#check
def check_startup(vulnerability):
    file = open('startup.txt', 'r', encoding='utf-16-le')
    content = file.read().splitlines()
    file.close()
    for vuln in vulnerability:
        if vuln != 1:
            if vulnerability[vuln]['Program Name'] in content:
                record_hit('Program Removed from Startup', vulnerability[vuln]['Points'])
            else:
                record_miss('Program Management')


def update_check_period(vulnerability):
    
    for vuln in vulnerability:
        if vuln != 1:
            with open('/etc/apt/apt.conf.d/10periodic', 'r') as config_file:
                for line in config_file:
                    if line.strip().startswith(key):
                        _, value = line.strip().split(None, 1)
                        val =  value
            if val == '\"1\";':
                record_hit('Check Period is set to 1', vulnerability[vuln]['Points'])
            else:
                record_miss('Program Management')

#check
def add_text_to_file(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            file = open(vulnerability[vuln]["File Path"], 'r')
            content = file.read()
            file.close()
            if re.search(vulnerability[vuln]["Text to Add"], content):
                record_hit(vulnerability[vuln]["Text to Add"] + ' has been added to ' + vulnerability[vuln]["File Path"], vulnerability[vuln]["Points"])
            else:
                record_miss('File Management')

#check
def remove_text_from_file(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            file = open(vulnerability[vuln]["File Path"], 'r')
            content = file.read()
            file.close()
            if not re.search(vulnerability[vuln]["Text to Remove"], content):
                record_hit(vulnerability[vuln]["Text to Remove"] + ' has been removed from ' + vulnerability[vuln]["File Path"], vulnerability[vuln]["Points"])
            else:
                record_miss('File Management')



def start_up_apps(vulnerability):
    startup_apps = []
    # List all files in the specified directory
    file_list = os.listdir('/etc/xdg/autostart')

    for filename in file_list:
        if filename.endswith('.desktop'):
            file_path = os.path.join('/etc/xdg/autostart', filename)
            config = configparser.ConfigParser()
            config.read(file_path)

            # Read the application name and command
            app_exec = config.get('Desktop Entry', 'Exec')
            startup_apps.append({'command': app_exec})
    for vuln in vulnerability:
        if vuln != 1:
            if vulnerability[vuln] not in start_up_apps:
                record_hit(vulnerability[vuln]["Checks"] + ' has been removed from start up', vulnerability[vuln]["Points"])
            else:
                record_miss('File Management')
    

def check_hosts(vulnerability):
    hosts_file_path = '/etc/hosts'

    with open(hosts_file_path, 'r') as file:
        hosts_content = file.read().strip()

    if not hosts_content:
        record_hit()
    else:
        print("Hosts file is not empty.")



#fix
def critical_services(vulnerability):

    for vuln in vulnerability:
        if vuln != 1:
            name = vulnerability[vuln]['Service Name']
            if name in services_content["unit"] and vulnerability[vuln]['Service State'] == services_content["active"]:
                    record_penalty(name + ' was changed.', vulnerability[vuln]['Points'])


#fix

def manage_services(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            name = vulnerability[vuln]['Service Name']
            if name in services_content:
                if name in services_content["unit"] and vulnerability[vuln]['Service State'] == services_content["active"]:
                    record_hit(name + ' has been ' + vulnerability[vuln]['Service State'] + ' and set to ' + vulnerability[vuln]['Service Start Mode'], vulnerability[vuln]['Points'])
                else:
                    record_miss('Program Management')




def disable_SSH_Root_Login(vulnerability):
    try:
        with open('/etc/ssh/sshd_config', 'r') as ssh_config_file:
            for line in ssh_config_file:
                if line.strip().startswith('PermitRootLogin'):
                    value = line.strip().split()[1].lower()
                    if value in ('no', 'without-password'):
                        record_hit('SSH_Root_Login Disabled.',  vulnerability[1]['Points'])


    except FileNotFoundError:
        record_hit('SSH_Root_Login Disabled.',  vulnerability[1]['Points'])

    record_miss('Local Policy')


def check_kernel(Vulnerability):
    kernel_version = platform.uname().release
    print("Kernel Version:", kernel_version)
    if Vulnerability is kernel_version:
        record_hit('Kernel is current version', Vulnerability[1]['Points'])
    else: 
        record_miss('Local Policy')


def programs(vulnerability, name):

    if name == "Good Program":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]["Program Name"] in program_content:
                    record_hit(vulnerability[vuln]["Program Name"] + ' is installed', vulnerability[vuln]["Points"])
                else:
                    record_miss('Program Management')
    if name == "Bad Program":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]["Program Name"] not in program_content:
                    record_hit(vulnerability[vuln]["Program Name"] + ' is not installed', vulnerability[vuln]["Points"])
                else:
                    record_miss('Program Management')
    if name == "Update Program":
        for vuln in vulnerability:
            if vuln != 1:
                if vulnerability[vuln]["Version"] not in program_versions:
                    record_hit(vulnerability[vuln]["Version"] + ' version of ' + vulnerability[vuln]["Program Name"] , vulnerability[vuln]["Points"])
                else:
                    record_miss('Program Management')


#wip
def anti_virus(vulnerability):
    z = open('security.txt', 'r', encoding='utf-16-le')
    content = z.read()
    z.close()
    if 'Real-time Protection Status : Enabled' in content:
        record_hit('Virus & threat protection enabled.', vulnerability[1]['Points'])
    else:
        record_miss('Security')


#test
def bad_file(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            if not os.path.exists(vulnerability[vuln]["File Path"]):
                record_hit('The item ' + vulnerability[vuln]["File Path"] + ' has been removed.', vulnerability[vuln]["Points"])
            else:
                record_miss('File Management')


def permission_checks(vulnerability):
    for vuln in vulnerability:
        if vuln != 1:
            if oct(os.stat(vulnerability[vuln]["File Path"]).st_mode & 0o777) is vulnerability[vuln]["Permissions"]:
                record_hit('The item ' + vulnerability[vuln]["File Path"] + ' has been removed.', vulnerability[vuln]["Points"])
            else:
                record_miss('File Management')


def no_scoring_available(name):
    messagebox.showerror(("No scoring for:", name), ("There is no scoring definition for", name, ". Please remove this option if you are the image creator, if you are a competitor ignore this message."))


#fix
#test
def load_policy_settings():
    with open('/etc/login.defs', 'r') as file:
            lines = file.readlines()
    login_defs_list = []
    for line in lines:
        line = line.strip()
        if not line.startswith('#') and line:
            key, value = line.split()
            login_defs_list.append((key, value))
    
    with open('/etc/pam.d/common-password', 'r') as common_password_file:
            for line in common_password_file:
                line = line.strip()
                if line.startswith('password'):
                    login_defs_list.append(line)

    return login_defs_list


def get_file_names_in_directory(directory):
    file_names = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_names.append(filename)
    return file_names

def load_programs():
    usr_bin_file_names = get_file_names_in_directory('/usr/bin')
    snap_bin_file_names = get_file_names_in_directory('/snap/bin')

    all_file_names = usr_bin_file_names + snap_bin_file_names
    return set(all_file_names)


def load_versions():
    command = "dpkg -l"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        installed_packages =  result.stdout.splitlines()[5:]  # Skip the header lines
    else:
        installed_packages = []

    package_list = []
    for line in installed_packages:
        parts = line.split()
        package_name = parts[1]
        package_version = parts[2]
        package_list.append({"name": package_name, "version": package_version})
    return package_list


#fix
def load_password_settings():
    password_settings = {}
    with open('/etc/security/pwquality.conf', 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line and '=' in line:
            key, value = line.split('=')
            key = key.strip().lstrip('# ')  
            password_settings[key.strip()] = value.strip()
    return password_settings

def load_services():

    # Run the systemctl command to list all services
    command = ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--plain"]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        services_output = result.stdout
        
        # Split the output into lines
        services_lines = services_output.splitlines()
        
        # Process each line and create a dictionary
        for line in services_lines:
            words = line.split()
            
            # Define dictionary keys and extract values from words
            service_data = {
                "unit": words[0],
                "load": words[1],
                "active": words[2],
                "sub": words[3],
                "description": ' '.join(words[4:])
            }
            
        # Print the dictionary for the current line
        return(service_data)
    else:
        return(result.stderr)



#check
def ps_create():
    vuln_scripts = ["Good Program", "Bad Program", "Turn On Domain Firewall", "Turn On Private Firewall", "Turn On Public Firewall"]
    #vuln_scripts = ["Good Program", "Bad Program", "Anti-Virus", "User Change Password", "Turn On Domain Firewall", "Turn On Private Firewall", "Turn On Public Firewall"]
    vuln_obj = {}
    for vuln in vuln_scripts:
        vuln_obj.update({vuln: Vulnerabilities.get_option_table(vuln, False)})
    m = open('check.ps1', 'w+')

    if vuln_obj["Bad Program"][1]["Enabled"] or vuln_obj["Good Program"][1]["Enabled"]:
        m.write('Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize > programs.txt\n')
    #if vuln_obj["Anti-Virus"][1]["Enabled"]:
        #m.write('function Get-AntiVirusProduct {\n[CmdletBinding()]\nparam (\n[parameter(ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]\n[Alias(\'name\')]\n$computername=$env:computername\n\n)\n\n#$AntivirusProducts = Get-WmiObject -Namespace "root\\SecurityCenter2" -Query $wmiQuery  @psboundparameters # -ErrorVariable myError -ErrorAction \'SilentlyContinue\' # did not work\n$AntiVirusProducts = Get-WmiObject -Namespace "root\\SecurityCenter2" -Class AntiVirusProduct  -ComputerName $computername\n\n$ret = @()\nforeach($AntiVirusProduct in $AntiVirusProducts){\n#Switch to determine the status of antivirus definitions and real-time protection.\n#The values in this switch-statement are retrieved from the following website: http://community.kaseya.com/resources/m/knowexch/1020.aspx\nswitch ($AntiVirusProduct.productState) {\n"262144" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}\n"262160" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"266240" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}\n"266256" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\n"393216" {$defstatus = "Up to date" ;$rtstatus = "Disabled"}\n"393232" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"393488" {$defstatus = "Out of date" ;$rtstatus = "Disabled"}\n"397312" {$defstatus = "Up to date" ;$rtstatus = "Enabled"}\n"397328" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\n"397584" {$defstatus = "Out of date" ;$rtstatus = "Enabled"}\ndefault {$defstatus = "Unknown" ;$rtstatus = "Unknown"}\n}\n\n#Create hash-table for each computer\n$ht = @{}\n$ht.Computername = $computername\n$ht.Name = $AntiVirusProduct.displayName\n$ht.\'Product GUID\' = $AntiVirusProduct.instanceGuid\n$ht.\'Product Executable\' = $AntiVirusProduct.pathToSignedProductExe\n$ht.\'Reporting Exe\' = $AntiVirusProduct.pathToSignedReportingExe\n$ht.\'Definition Status\' = $defstatus\n$ht.\'Real-time Protection Status\' = $rtstatus\n\n#Create a new object for each computer\n$ret += New-Object -TypeName PSObject -Property $ht \n}\nReturn $ret\n} \nGet-AntiVirusProduct > security.txt\n')
    m.close()
    m = open('check.bat', 'w+')
    m.write('@echo off\n echo > trigger.cfg\n')
    #if vuln_obj["User Change Password"][1]["Enabled"]:
    #    for vuln in vuln_obj["User Change Password"]:
    #        if vuln != 1:
    #            m.write('net user ' + vuln_obj["User Change Password"][vuln]["User Name"].lower() + ' > user_' + vuln_obj["User Change Password"][vuln]["User Name"].lower() + '.txt\n')
    if vuln_obj["Turn On Domain Firewall"][1]["Enabled"] or vuln_obj["Turn On Private Firewall"][1]["Enabled"] or vuln_obj["Turn On Public Firewall"][1]["Enabled"]:
        m.write('netsh advfirewall show allprofiles state > firewall_status.txt\n')
    #if vuln_obj["Bad Program"][1]["Enabled"] or vuln_obj["Good Program"][1]["Enabled"] or vuln_obj["Anti-Virus"][1]["Enabled"]:
    if vuln_obj["Bad Program"][1]["Enabled"] or vuln_obj["Good Program"][1]["Enabled"]:
        m.write('Powershell.exe -Command "& {Start-Process Powershell.exe -ArgumentList \'-ExecutionPolicy Bypass -File "check.ps1"\' -Verb RunAs -Wait -WindowStyle Hidden}"\n')
    if vuln_obj["Check Port Open"][1]["Enabled"]:
        v = open('portVulns.vbs', 'w+')
    m.write('timeout 30')
    m.close()
    f = open('invisible.vbs', 'w+')
    f.write('CreateObject("Wscript.Shell").Run """" & WScript.Arguments(0) & """", 0, False')
    f.close()
    CREATE_NO_WINDOW = 0x08000000
    #os.system('wscript.exe "invisible.vbs" "check.bat" /quiet')
    subprocess.check_call('wscript.exe "invisible.vbs" "check.bat" "fRules.vbs" /quiet', creationflags=CREATE_NO_WINDOW)


#check1
def account_management(vulnerabilities):
    write_to_html('<H3>USER MANAGEMENT</H3>')
    vulnerability_def = {"Add Admin": group_manipulation, "Remove Admin": group_manipulation, "Add User to Group": group_manipulation, "Remove User from Group": group_manipulation, "Add User": users_manipulation, "Remove User": users_manipulation}
    #vulnerability_def = {"Disable Admin": disable_admin, "Disable Guest": disable_guest, "Add Admin": group_manipulation, "Remove Admin": group_manipulation, "Add User to Group": group_manipulation, "Remove User from Group": group_manipulation, "Add User": users_manipulation, "Remove User": users_manipulation, "User Change Password": user_change_password}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if "Critical" in vuln.name:
            critical_items.append(vuln)
        elif vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)


#check1
def local_policies(vulnerabilities):
    write_to_html('<H3>SECURITY POLICIES</H3>')
    vulnerability_def = {"Do Not Require CTRL_ALT_DEL": local_group_policy, "Don't Display Last User": local_group_policy, "Minimum Password Age": local_group_policy, "Maximum Password Age": local_group_policy, "Minimum Password Length": local_group_policy, "Maximum Login Tries": local_group_policy, "Lockout Duration": local_group_policy, "Lockout Reset Duration": local_group_policy, "Password History": local_group_policy, "Password Complexity": local_group_policy, "Reversible Password Encryption": local_group_policy, "Audit Account Login": auditing}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)


#check1
def program_management(vulnerabilities):
    write_to_html('<H3>PROGRAMS</H3>')
    vulnerability_def = {"Good Program": programs, "Bad Program": programs, "Update Program": programs, "Services": manage_services}
    #vulnerability_def = {"Good Program": programs, "Bad Program": programs, "Update Program": no_scoring_available, "Add Feature": no_scoring_available, "Remove Feature": no_scoring_available, "Services": manage_services}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if "Critical" in vuln.name:
            critical_items.append(vuln)
        elif vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)


#check1
def file_management(vulnerabilities):
    write_to_html('<H3>FILE MANAGEMENT</H3>')
    vulnerability_def = {"Forensic": forensic_question, "Bad File": bad_file, "Add Text to File": add_text_to_file, "Remove Text From File": remove_text_from_file}
    #vulnerability_def = {"Forensic": forensic_question, "Bad File": bad_file, "Check Hosts": no_scoring_available, "Add Text to File": add_text_to_file, "Remove Text From File": remove_text_from_file, "File Permissions": no_scoring_available}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)


#check1
def firewall_management(vulnerabilities):
    write_to_html('<H3>FIREWALL MANAGEMENT</H3>')
    vulnerabilities
    vulnerability_def = {"Turn On Domain Firewall": firewallVulns, "Turn On Private Firewall": firewallVulns, "Turn On Public Firewall": firewallVulns, "Check Port Open": portVulns, "Check Port Closed": portVulns}
    #vulnerability_def = {"Forensic": forensic_question, "Bad File": bad_file, "Check Hosts": no_scoring_available, "Add Text to File": add_text_to_file, "Remove Text From File": remove_text_from_file, "File Permissions": no_scoring_available}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)


"""
def miscellaneous(vulnerabilities):
    write_to_html('<H3>MISCELLANEOUS</H3>')
    vulnerability_def = {"Anti-Virus": anti_virus, "Update Check Period": no_scoring_available, "Update Auto Install": no_scoring_available, "Task Scheduler": no_scoring_available, "Check Startup": no_scoring_available}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if vulnerability[1]["Enabled"]:
            if len(getfullargspec(vulnerability_def[vuln.name]).args) == 1:
                vulnerability_def[vuln.name](vulnerability if "vulnerability" in getfullargspec(vulnerability_def[vuln.name]).args else vuln.name)
            else:
                vulnerability_def[vuln.name](vulnerability, vuln.name)
"""


#check1
def critical_functions(vulnerabilities):
    write_to_html('<H4>Critical Functions:</H4>')
    vulnerability_def = {"Critical Users": critical_users, "Critical Programs": critical_programs, "Critical Services": critical_services}
    for vuln in vulnerabilities:
        vulnerability = Vulnerabilities.get_option_table(vuln.name, False)
        if vulnerability[1]["Enabled"]:
            vulnerability_def[vuln.name](vulnerability)


def policyCreation():
      with open('/etc/login.defs', 'r') as source, open(destination_file, 'w') as destination:
        for line in source:
            if not line.strip().startswith("#"):
                destination.write(line)


try:
    Settings = db_handler.Settings()
    menuSettings = Settings.get_settings(False)
    Categories = db_handler.Categories()
    categories = Categories.get_categories()
    Vulnerabilities = db_handler.OptionTables()
    Vulnerabilities.initialize_option_table()
except:
    f = open('scoring_engine.log', 'w')
    e = traceback.format_exc()
    #if "KeyboardInterrupt" in e:
        #sys.exit()
    f.write(str(e))
    f.close()
    messagebox.showerror('Crash Report', 'The scoring engine has stopped working, a log has been saved to ' + os.path.abspath('scoring_engine.log'))
    sys.exit()

total_points = 0
total_vulnerabilities = 0
prePoints = 0
category_def = {"Account Management": account_management, "Local Policy": local_policies, "Program Management": program_management, "File Management": file_management, "Firewall Management": firewall_management}
Desktop = menuSettings["Desktop"]
#fix
index = 'C:/CyberPatriot/'
scoreIndex = index + 'ScoreReport.html'

# --------- Main Loop ---------#
check_runas()
while True:
    #print("Initializing Variables and Running Scrips(~20 seconds)")
    try:
        if not os.path.exists('trigger.cfg'):
            #print("Creating PS")
            ps_create()
        else:
            os.remove('trigger.cfg')
        total_points = 0
        total_vulnerabilities = 0
        critical_items = []
        policy_settings_content = load_policy_settings()
        password_settings_content = load_password_settings()
        services_content = load_services()
        program_content = load_programs()
        program_versions = load_versions()
        time.sleep(20)
        #print("Building Report Head")
        draw_head()
        for category in categories:
            #print("Checking", category.name, "Options")
            category_def[category.name](Vulnerabilities.get_option_template_by_category(category.id))
        critical_functions(critical_items)
        draw_tail()
        check_score()
        

        time.sleep(30)
    except:
        f = open('scoring_engine.log', 'w')
        e = traceback.format_exc()
        #if "KeyboardInterrupt" in e:
            #sys.exit()
        f.write(str(e))
        f.close()
        messagebox.showerror('Crash Report', 'The scoring engine has stopped working, a log has been saved to ' + os.path.abspath('scoring_engine.log'))
        #sys.exit()

#TODO add Functions:
#updatecheckperiod    ["Miscellaneous"]["Update Check Period"]
# updateautoinstall    ["Miscellaneous"]["Update Auto Install"]
# checkhosts           ["File Management"]["Check Hosts"]
# taskscheduler        ["Miscellaneous"]["Task Scheduler"]
# checkstartup         ["Miscellaneous"]["Check Startup"]
