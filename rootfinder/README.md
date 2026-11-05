```text
8"""8  eeeeee eeeeee ""8"" 8"""" 8  8"""8 8""""8 8"""" 8"""8  
8   8  8    8 8    8   8   8     8  8   8 8    8 8     8   8  
8eee8e 8    8 8    8   8e  8eeee 8e 8e  8 8e   8 8eeee 8eee8e 
88   8 8    8 8    8   88  88    88 88  8 88   8 88    88   8 
88   8 8    8 8    8   88  88    88 88  8 88   8 88    88   8 
88   8 8eeee8 8eeee8   88  88    88 88  8 88eee8 88eee 88   8 

*rootfinder*
Made by *pr0lificz*

rootfinder is a modular, lightweight Linux system information and privesc enumerator.

## Features

* **System Information (`sys-info`)**: Gathers current UID, GID, username, working directory, kernel details, and OS release information.
* **SUDO Privilege Check (`sudopriv`)**: Checks for passwordless sudo execution permissions available to the current user.
* **SUID Binary Audit (`suid`)**: Audits the filesystem for SUID binaries (`perm -4000`).
* **SGID Binary Audit (`sgid`)**: Audits the filesystem for SGID binaries (`perm -2000`).
* **Linux Capabilities Check (`caps`)**: Scans the filesystem for binaries with elevated capabilities via `getcap`.
* **Cron Job Inspection (`cron`)**: Checks access and contents of system-wide crontab and `/etc/cron.d/` jobs.
* **Sensitive Files & Path Audit (`sensitive`)**: Scans `$PATH` directories for world-writable permissions and audits security permissions on critical system files (`/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/sudoers`).

# Requirements

Python 3.6+

No external dependencies (uses standard library modules: os, sys, pwd, subprocess, argparse, platform).

Installation & Setup
git clone https://github.com/pr0lificz/rootfinder/

Ensure Python 3 is installed.

python3 rootfinder.py help

Usage

# Run system information audit
python3 rootfinder.py sys-info

# Check sudo permissions
python3 rootfinder.py sudopriv

# Search for SUID binaries
python3 rootfinder.py suid

# Search for SGID binaries
python3 rootfinder.py sgid

# Check Linux capabilities
python3 rootfinder.py caps

# Run cron audit
python3 rootfinder.py cron

# Check $PATH and sensitive file permissions
python3 rootfinder.py sensitive

# Execute all modules in sequence
python3 rootfinder.py run-full

# Display general help
python3 rootfinder.py help

# View author credits
python3 rootfinder.py credits

