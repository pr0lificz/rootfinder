import os
import sys
import pwd
import subprocess
import argparse
import platform

banner = '''
8"""8  eeeeee eeeeee ""8"" 8"""" 8  8"""8 8""""8 8"""" 8"""8  
8   8  8    8 8    8   8   8     8  8   8 8    8 8     8   8  
8eee8e 8    8 8    8   8e  8eeee 8e 8e  8 8e   8 8eeee 8eee8e 
88   8 8    8 8    8   88  88    88 88  8 88   8 88    88   8 
88   8 8    8 8    8   88  88    88 88  8 88   8 88    88   8 
88   8 8eeee8 8eeee8   88  88    88 88  8 88eee8 88eee 88   8 
                                                              
'''

print(banner)

def sys_info():
    print(f'uid: \033[32m{os.getuid()}\033[0m')
    print(f'gid: \033[32m{os.getgid()}\033[0m')

    try:
      username = os.getlogin()
    except OSError:
       username = os.getenv('USER') or os.getenv('LOGNAME')

    print(f'Username: \033[32m{username}\033[0m')
    print(f'\033[32m{os.getcwd()}\033[0m')

    print(os.uname())
    print(platform.uname())

    try:
        with open('/etc/os-release', 'r') as os_info:
            print(os_info.readlines())
    except (FileNotFoundError, PermissionError) as error:
       print(error)

def sudo_priv_check():
   check = subprocess.run(['sudo', '-n', '-l'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True)

   if check.returncode == 0:
      print(f'\033[32m[+] SUDO PERMS FOUND [+]\033[0m')
      for i in check.stdout.strip().splitlines():
         print(f' {i}')
   else:
      print(f'\033[31m[X] SUDO PERMS NOT FOUND [X]\nNo sudo passwordless action available\033[0m')

def get_SUID():
    check = subprocess.run(['find', '/', '-perm', '-4000'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True)
   
    if check.stdout.strip(): 
        for i in check.stdout.strip().splitlines():
            print(f' {i}')

    else: 
        print('\033[31m[X] No SUID Binaries Locatable...[X]\033[0m')

def get_SGID():
    check = subprocess.run(['find', '/', '-perm', '-2000'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True)

    if check.stdout.strip(): 
            for i in check.stdout.strip().splitlines():
                print(f' {i}')
    
    else: 
        print('\033[31m[X] No SGID Binaries Locatable...[X]\033[0m')

def get_capabilities():
    try:
        check = subprocess.run(['getcap', '-r', '/'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
       
        if check.stdout.strip(): 
            for i in check.stdout.strip().splitlines():
                print(f' {i}')
        else: 
            print('\033[31m[X] No Capabilities Locatable...[X]\033[0m')
    except FileNotFoundError:
        print('\033[31m[X] getcap utility not found on system...[X]\033[0m')
    

def check_cron():
    crond_check = False
    crontab_check = False

    if os.path.exists('/etc/crontab'):
        try:
            with open('/etc/crontab', 'r') as crontab:
                print(crontab.readlines())

            crontab_check = True
        except (FileNotFoundError, PermissionError) as error:
            print(error)
            crontab_check = False

    if os.path.exists('/etc/cron.d'):
        try:
            print(os.listdir('/etc/cron.d'))
            crond_check = True
        except (FileNotFoundError, PermissionError) as error:
            print(error)
            crond_check = False

    if crontab_check == True and crond_check == True:
        print('\n\033[32m[+]crontabs and cron.d found and readable[+]\033[0m')
    elif crontab_check == True and crond_check == False:
        print('\n\033[93m[-]crontabs found and readable but no cron.d\033[0m')
    elif crontab_check == False and crond_check == True:
        print('\n\033[93m[-]cron.d found and readable but no crontabs\033[0m')
    else:
        print('\n\033[31m[X]Neither crontabs or cron.d found or readable[X]\033[0m')
 
def sensitive_dirs():
    path = os.environ.get('PATH').split(':')

    for p in path:
        try:
            stats = os.stat(p)

            if (stats.st_mode & 0o002) != 0:
                print(f'\033[32m[+] Writable Dir Found! [+]\033[0m')
        except (FileNotFoundError, PermissionError) as error:
            print(error) 

    files_to_check = ['/etc/passwd', '/etc/shadow', '/etc/group', '/etc/sudoers']
    
    for filepath in files_to_check:
        if os.path.exists(filepath):
            try:
                stats = os.stat(filepath)
                is_writable = (stats.st_mode & 0o002) != 0
                is_readable = os.access(filepath, os.R_OK)
                
                status_parts = []
                if is_writable:
                    status_parts.append("\033[31m[!] WORLD-WRITABLE [!]\033[0m")
                
                if is_readable:
                    status_parts.append("\033[32m[Readable]\033[0m")
                else:
                    status_parts.append("\033[93m[Restricted]\033[0m")
                    
                print(f" {filepath}: {' '.join(status_parts)}")
            except (FileNotFoundError, PermissionError) as error:
                print(f" [X] Error checking {filepath}: {error} [X]")
        else:
            print(f" [X] {filepath} not found [X]")

def run_all():
    print(f'\033[94m[*]Retrieving System Info...[*]\033[0m')
    sys_info()
    print('')
    
    print(f'\033[94m[*]Checking for SUDO Permissions...[*]\033[0m')
    sudo_priv_check()
    print('')

    print(f'\033[94m[*]Retrieving SUID Binaries...[*]\033[0m')
    get_SUID()
    print('')

    print(f'\033[94m[*]Retrieving SGID Binaries...[*]\033[0m')
    get_SGID()
    print('')

    print(f'\033[94m[*]Checking Linux Capabilities...[*]\033[0m')
    get_capabilities()
    print('')

    print(f'\033[94m[*]Checking cron for possible PrivEsc paths...[*]\033[0m')
    check_cron()
    print('')

    print(f'\033[94m[*]Checking for Other Sensitive Directories...[*]\033[0m')
    sensitive_dirs()
    print('')

def credits():
    print('''\033[31m
             %%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@
             %%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
             %%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
             %%%%%%%%%%%#*,,(////((%%%%#/((((#(*((/((((###%%%%%&%%%%&%%%%%%&&&&&&&&&&&&&&&&&&
             ##((((#(((((((((/******///((((/(((((/(///(/(/(/(#%%%%%#%#%%%%%%%%%%%%%&&&&&&&&&&
             ((,,,****,*,**,***,,,,,*/**////(((//////////(((//*//****///,(#%%%%%%%%%%%%%%&&&&
             #((((#####(///***,,,,,,...,,.*//.,******/////,,,***,**,..,,.//((#####%%%%%%%%%%%
             ####(((###(((***,**,,,******,,....,.,,.,/(##%%%%%&&&%%%%%%##(/*,..,,,*/**/**/%%%
             ##########((/*//((///((/*,,,.,*,...,(%%%%%%%%%%%%%%%%%&&&&%%%%%%%#(*,**,,,,,,(##
             ((//((####(//(////////(((/////*,*#%%%%%%%&&&&%%%#%##%%&&&&&&%%%%%%%%(*,..,.,/((/
             ((#(((/(#(///**//**//**//*(((//#%%%%%%%&&&&&&&&&@&&&&&&&&&&&&&%%%%%%%%#*,,,,*//,
             (##(#((####(((///(((((/(((((((#%%%%&&&&&&&&&&@@@@@@@@@@@@@&&&&&&&%%%%%%#/*///**,
             %%%%%#%%%#%#####%%####((#((((#%%&&&&&&&&&@@@@@@@@@@@@@@@@@@@&&&&&&&&%%%%(****/((
             %%%###(**#%%%%%%%%%%%%%%%%%%##%&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&&&%%#(##(#/*
             #%%%#%#(#%%%%#%%%%%%&%%%%%%%##%&&&&@@@@&&&&%&&&&&&&&&&&@@@@@@@@@&&&&&&&%##%##%#(
             #############(###############&&@@@@&&%%%%%%%%%#%%%&&&%%%%&&&&@@@&&&&&&&%#%%%%%%#
             ##############(((((((((((#%&@@@@@&%%%%&&@@@&%#%%%%%%%%%%%%%%%%&&&&&&&&&%#%%%%%%%
             #########((((((((((((((%&@@@@@@@%%##%&@&&@@&&###%%%%%%#%&@@@@&%%&&@@@&&%########
             #######((((((((((((((#&&@@@@@@@&%%%%%%%&&&&%%%###%%#%%%&@@@@@&%%%&&&@@@&%#(#####
             ##########(((##(((##%&@@@@@@@@&&%%%%%%%%%#%%%##%%%%%%%%&&&@@@&%%%%&&@@@&&%######
             ################(#&&@@@@@@@@@&&&&%%%##########%%%%%#%%%%%%%%%%%%%%&&@@@@@&%#####
             ################&&@@@@@@@@@@@&&&%%%%%#(###%#%%%%%&%%%%%%%%%%%%%%%&&@@@@@@&&%####
             ##############%&@@@@@@@@@@@@&%%%%%%%######%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@&&%###
             #############%&@@@@@@@@@@@@@@&&%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%&&&&@@@@@@@@@&%%##
             #############&&@@@@@@@@@@@@@&&%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&@@@@@@@@@&&%#
             %%%%%%%%%##%&&&@@@@@@@@@@&&&%%&%&&&&&&&&%%%%%%##%%%%%%%%%&&&&&&&&&@@@@@@@@@@@&%%
             %%%%%%%%%%%%%%&&@@@@@@@&&%%%%%%&%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@&&\nDev: pr0lificz\033[0m''')

def help():
    print('rootfinder is a Linux Privilege Escalation Recon Tool\nUsage:\nsys-info: get system information like id, username, working directory, OS Info, etc.\ncron: Enumerate possible privesc paths via cron\nsensitive: Search for Other Sensitive files and directories\nrun-full: Run a full PrivEsc vector scan\npython3 rootfinder.py <flag>\nexample: python3 rootfinder.py run-full' ) 
   
parser = argparse.ArgumentParser(
    prog='rootfinder',
    description='A linux privesc tool made in python'
)

subparsers = parser.add_subparsers(dest='action', required=True)

sys_parser = subparsers.add_parser('sys-info', help='Get Linux system info')

sudo_parser = subparsers.add_parser('sudopriv', help='Check for sudo permissions')

suid_parser = subparsers.add_parser('suid', help='Check for SUID binaries')

sgid_parser = subparsers.add_parser('sgid', help='Check for SGID binaries')

cap_parser = subparsers.add_parser('caps', help='Check for Linux capabilities')

cron_parser = subparsers.add_parser('cron', help='Check for readable/writable cron files')

sens_parser = subparsers.add_parser('sensitive', help='Check for other sensitive files or directories')

all_parser = subparsers.add_parser('run-full', help='Run a full PrivEsc path check')

credits_parser = subparsers.add_parser('credits', help='Display Dev Credits')

help_parser = subparsers.add_parser('help', help='Tool Help/Usage')

args = parser.parse_args()

if args.action == 'sys-info':
    sys_info()
elif args.action == 'sudopriv':
    sudo_priv_check()
elif args.action == 'suid':
    get_SUID()
elif args.action == 'sgid':
    get_SGID()
elif args.action == 'caps':
    get_capabilities()
elif args.action == 'cron':
    check_cron()
elif args.action == 'sensitive':
    sensitive_dirs()
elif args.action == 'run-full':
    run_all()
elif args.action == 'credits':
    credits()
elif args.action == 'help':
    help()