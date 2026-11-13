#!/usr/bin/env python3
"""
Generator script to build a 215+ scenario library for shell-drill.
Categorized into:
1. Service Management (systemctl & journalctl)
2. Firewall & Network (firewall-cmd, nmcli, ip, ss, ping, curl)
3. Grep & Regex Mastery
4. Sed Stream Editing Recipes
5. Awk Processing & Reports
6. Find & Permissions
7. Pipes, Redirections & Process Flow
8. Security & SELinux Administration
"""

import json
import os
import re

scenarios = []

def add_scenario(id, cat, title, diff, desc, obj, hints, sol, regexes, setup_files=None, setup_perms=None, verify_cmd=None):
    scenarios.append({
        "id": id,
        "category": cat,
        "title": title,
        "difficulty": diff,
        "description": desc,
        "objective": obj,
        "hints": hints,
        "solution": sol,
        "accepted_regex": regexes,
        "setup_files": setup_files or {},
        "setup_perms": setup_perms or {},
        "verify_cmd": verify_cmd or ""
    })

# =========================================================================
# 1. SERVICE MANAGEMENT (systemctl & journalctl) - 40 Scenarios
# =========================================================================

add_scenario("sys-01", "Service Management", "Enable and Start Service Immediately", "Easy",
    "On RHEL 9/10, configure 'sshd' to start at boot and immediately start it now in one command.",
    "systemctl enable --now sshd",
    ["Use systemctl enable with --now", "Command: systemctl enable --now sshd"],
    "systemctl enable --now sshd",
    [r"systemctl\s+enable\s+--now\s+sshd(\.service)?", r"systemctl\s+--now\s+enable\s+sshd(\.service)?"],
    verify_cmd="systemctl is-enabled sshd 2>/dev/null || systemctl is-active sshd")

add_scenario("sys-02", "Service Management", "Reload systemd Daemon After Unit Edits", "Easy",
    "Notify systemd to scan the disk for new or changed unit files without rebooting.",
    "systemctl daemon-reload",
    ["Use systemctl daemon-reload", "Command: systemctl daemon-reload"],
    "systemctl daemon-reload",
    [r"systemctl\s+daemon-reload"])

add_scenario("sys-03", "Service Management", "Query Journald for Priority Errors in Past Hour", "Intermediate",
    "Query systemd-journald for 'sshd' logs filtering for priority 'err' from the last 1 hour.",
    "journalctl -u sshd -p err --since \"1 hour ago\"",
    ["Flags: -u sshd, -p err, --since '1 hour ago'", "Command: journalctl -u sshd -p err --since \"1 hour ago\""],
    'journalctl -u sshd -p err --since "1 hour ago"',
    [r'journalctl\s+.*-u\s+sshd.*-p\s+err.*--since\s+["\']?(-1h|1\s+hour\s+ago)["\']?'])

add_scenario("sys-04", "Service Management", "Mask Service to Prevent Accidental Activation", "Intermediate",
    "Completely prevent the 'cups' service from being started manually or as a dependency.",
    "systemctl mask cups",
    ["Use systemctl mask", "Command: systemctl mask cups"],
    "systemctl mask cups",
    [r"systemctl\s+mask\s+cups(\.service)?"])

add_scenario("sys-05", "Service Management", "List All Failed System Units", "Easy",
    "List all systemd units currently in a failed or degraded state.",
    "systemctl --failed",
    ["Command: systemctl --failed"],
    "systemctl --failed",
    [r"systemctl\s+--failed", r"systemctl\s+list-units\s+--state=failed"])

add_scenario("sys-06", "Service Management", "Check If Service Is Actively Running", "Easy",
    "Check whether 'sshd' is currently running without verbose output.",
    "systemctl is-active sshd",
    ["Use is-active verb", "Command: systemctl is-active sshd"],
    "systemctl is-active sshd",
    [r"systemctl\s+is-active\s+sshd(\.service)?"])

add_scenario("sys-07", "Service Management", "View Kernel Ring Buffer Logs via Journalctl", "Intermediate",
    "View only kernel messages from the current boot using journalctl.",
    "journalctl -k",
    ["Use -k or --dmesg", "Command: journalctl -k"],
    "journalctl -k",
    [r"journalctl\s+(-k|--dmesg)"])

add_scenario("sys-08", "Service Management", "Tail Live Service Logs in Follow Mode", "Intermediate",
    "Stream live logs for 'sshd', showing last 20 lines and following new output.",
    "journalctl -u sshd -f -n 20",
    ["Flags: -u sshd, -f, -n 20", "Command: journalctl -u sshd -f -n 20"],
    "journalctl -u sshd -f -n 20",
    [r"journalctl\s+.*-u\s+sshd.*(-f\s+-n\s+20|-n\s+20\s+-f|-fn\s*20)"])

add_scenario("sys-09", "Service Management", "Set Default Boot Target to Multi-User", "Intermediate",
    "Configure default system boot target to multi-user (console mode).",
    "systemctl set-default multi-user.target",
    ["Command: systemctl set-default multi-user.target"],
    "systemctl set-default multi-user.target",
    [r"systemctl\s+set-default\s+multi-user\.target"])

add_scenario("sys-10", "Service Management", "List Active Systemd Timers", "Easy",
    "List all systemd timer units on the machine.",
    "systemctl list-timers",
    ["Command: systemctl list-timers"],
    "systemctl list-timers",
    [r"systemctl\s+list-timers(\s+--all)?"])

add_scenario("sys-11", "Service Management", "Inspect Unit Configuration with systemctl cat", "Easy",
    "Display configuration file contents and drop-ins for 'sshd.service'.",
    "systemctl cat sshd",
    ["Command: systemctl cat sshd"],
    "systemctl cat sshd",
    [r"systemctl\s+cat\s+sshd(\.service)?"])

add_scenario("sys-12", "Service Management", "Vacuum Journal Logs to Free Disk Space", "Intermediate",
    "Clean up systemd journal logs to retain at most 100 Megabytes.",
    "journalctl --vacuum-size=100M",
    ["Command: journalctl --vacuum-size=100M"],
    "journalctl --vacuum-size=100M",
    [r"journalctl\s+--vacuum-size=100M"])

add_scenario("sys-13", "Service Management", "Reset Failed State on Cleaned Service", "Intermediate",
    "Clear the failed status memory for unit 'httpd'.",
    "systemctl reset-failed httpd",
    ["Command: systemctl reset-failed httpd"],
    "systemctl reset-failed httpd",
    [r"systemctl\s+reset-failed\s+httpd(\.service)?"])

add_scenario("sys-14", "Service Management", "Query Service SubState Property with systemctl show", "Intermediate",
    "Query the 'SubState' property value for unit 'sshd'.",
    "systemctl show -p SubState sshd",
    ["Command: systemctl show -p SubState sshd"],
    "systemctl show -p SubState sshd",
    [r"systemctl\s+show\s+(-p\s+SubState|--property=SubState)\s+sshd"])

add_scenario("sys-15", "Service Management", "Reload or Restart Service Conditionally", "Easy",
    "Reload configuration if supported; otherwise restart 'sshd'.",
    "systemctl reload-or-restart sshd",
    ["Command: systemctl reload-or-restart sshd"],
    "systemctl reload-or-restart sshd",
    [r"systemctl\s+reload-or-restart\s+sshd"])

add_scenario("sys-16", "Service Management", "List Unit Dependency Tree", "Easy",
    "Display the visual dependency tree for unit 'sshd.service'.",
    "systemctl list-dependencies sshd",
    ["Command: systemctl list-dependencies sshd"],
    "systemctl list-dependencies sshd",
    [r"systemctl\s+list-dependencies\s+sshd"])

add_scenario("sys-17", "Service Management", "Filter Journal Logs by Root User UID", "Intermediate",
    "Query journald for messages initiated by root (UID 0), showing last 25 lines.",
    "journalctl _UID=0 -n 25",
    ["Command: journalctl _UID=0 -n 25"],
    "journalctl _UID=0 -n 25",
    [r"journalctl\s+.*_UID=0.*-n\s+25", r"journalctl\s+.*-n\s+25.*_UID=0"])

add_scenario("sys-18", "Service Management", "View Logs from Previous System Boot", "Intermediate",
    "Query journalctl for logs from the prior boot session (offset -1).",
    "journalctl -b -1",
    ["Command: journalctl -b -1"],
    "journalctl -b -1",
    [r"journalctl\s+(-b\s+-1|--boot=-1)"])

add_scenario("sys-19", "Service Management", "Check If Service Is Enabled for Boot", "Easy",
    "Check if 'crond' is set to enable at system boot.",
    "systemctl is-enabled crond",
    ["Command: systemctl is-enabled crond"],
    "systemctl is-enabled crond",
    [r"systemctl\s+is-enabled\s+crond(\.service)?"])

add_scenario("sys-20", "Service Management", "Unmask a Masked Service", "Intermediate",
    "Restore the 'cups' service from masked state so it can be used again.",
    "systemctl unmask cups",
    ["Command: systemctl unmask cups"],
    "systemctl unmask cups",
    [r"systemctl\s+unmask\s+cups(\.service)?"])

add_scenario("sys-21", "Service Management", "Disable Service and Stop It Immediately", "Easy",
    "Disable 'postfix' from starting at boot and stop it right now in one command.",
    "systemctl disable --now postfix",
    ["Command: systemctl disable --now postfix"],
    "systemctl disable --now postfix",
    [r"systemctl\s+(disable\s+--now|--now\s+disable)\s+postfix(\.service)?"])

add_scenario("sys-22", "Service Management", "Isolate Graphical Target On Demand", "Intermediate",
    "Switch active operating state to graphical.target immediately.",
    "systemctl isolate graphical.target",
    ["Command: systemctl isolate graphical.target"],
    "systemctl isolate graphical.target",
    [r"systemctl\s+isolate\s+graphical\.target"])

add_scenario("sys-23", "Service Management", "List All Installed Service Unit Files", "Easy",
    "Display state of all unit files (enabled, disabled, static, masked).",
    "systemctl list-unit-files --type=service",
    ["Command: systemctl list-unit-files --type=service"],
    "systemctl list-unit-files --type=service",
    [r"systemctl\s+list-unit-files\s+--type=service"])

add_scenario("sys-24", "Service Management", "Vacuum Journal Logs by Retention Time", "Intermediate",
    "Purge journal archives older than 2 days.",
    "journalctl --vacuum-time=2d",
    ["Command: journalctl --vacuum-time=2d"],
    "journalctl --vacuum-time=2d",
    [r"journalctl\s+--vacuum-time=2d"])

add_scenario("sys-25", "Service Management", "Display Current Disk Usage of Journal Logs", "Easy",
    "Check how much storage space is currently consumed by systemd-journald.",
    "journalctl --disk-usage",
    ["Command: journalctl --disk-usage"],
    "journalctl --disk-usage",
    [r"journalctl\s+--disk-usage"])

add_scenario("sys-26", "Service Management", "Filter Journal by Specific Process ID", "Intermediate",
    "Query logs generated specifically by PID 1234.",
    "journalctl _PID=1234",
    ["Command: journalctl _PID=1234"],
    "journalctl _PID=1234",
    [r"journalctl\s+_PID=1234"])

add_scenario("sys-27", "Service Management", "Output Journal Entries in Pretty JSON", "Intermediate",
    "Query last 5 logs for 'sshd' formatted in structured json-pretty.",
    "journalctl -u sshd -n 5 -o json-pretty",
    ["Command: journalctl -u sshd -n 5 -o json-pretty"],
    "journalctl -u sshd -n 5 -o json-pretty",
    [r"journalctl\s+.*-u\s+sshd.*(-o\s+json-pretty|--output=json-pretty)"])

add_scenario("sys-28", "Service Management", "Check Current Default Boot Target", "Easy",
    "Print the currently configured default target without modifying it.",
    "systemctl get-default",
    ["Command: systemctl get-default"],
    "systemctl get-default",
    [r"systemctl\s+get-default"])

add_scenario("sys-29", "Service Management", "Kill Specific Service with SIGTERM", "Intermediate",
    "Send SIGTERM kill signal to all processes under unit 'httpd'.",
    "systemctl kill httpd",
    ["Command: systemctl kill httpd"],
    "systemctl kill httpd",
    [r"systemctl\s+kill\s+httpd(\.service)?"])

add_scenario("sys-30", "Service Management", "List All Active Socket Units", "Easy",
    "List all systemd socket units and their listening endpoints.",
    "systemctl list-sockets",
    ["Command: systemctl list-sockets"],
    "systemctl list-sockets",
    [r"systemctl\s+list-sockets"])

add_scenario("sys-31", "Service Management", "Query Journal Logs for System Boot Events", "Easy",
    "Show all log events recorded during the current boot from start to finish.",
    "journalctl -b",
    ["Command: journalctl -b"],
    "journalctl -b",
    [r"journalctl\s+(-b|--boot)(\s+0)?$"])

add_scenario("sys-32", "Service Management", "Show Only Service Description and Path", "Intermediate",
    "Display the Description and FragmentPath properties of unit 'sshd'.",
    "systemctl show -p Description,FragmentPath sshd",
    ["Command: systemctl show -p Description,FragmentPath sshd"],
    "systemctl show -p Description,FragmentPath sshd",
    [r"systemctl\s+show\s+(-p|--property=).*sshd"])

add_scenario("sys-33", "Service Management", "Restart Failed NetworkManager Service", "Easy",
    "Restart the NetworkManager service daemon.",
    "systemctl restart NetworkManager",
    ["Command: systemctl restart NetworkManager"],
    "systemctl restart NetworkManager",
    [r"systemctl\s+restart\s+NetworkManager(\.service)?"])

add_scenario("sys-34", "Service Management", "Inspect Journal Logs Between Exact Time Window", "Intermediate",
    "Query logs recorded between '2026-10-01 00:00:00' and '2026-10-01 12:00:00'.",
    'journalctl --since "2026-10-01 00:00:00" --until "2026-10-01 12:00:00"',
    ["Command: journalctl --since \"2026-10-01 00:00:00\" --until \"2026-10-01 12:00:00\""],
    'journalctl --since "2026-10-01 00:00:00" --until "2026-10-01 12:00:00"',
    [r'journalctl\s+.*--since\s+["\']2026-10-01.*--until\s+["\']2026-10-01'])

add_scenario("sys-35", "Service Management", "Audit Failed Status of Specific Service", "Easy",
    "Test if 'mariadb' is in a failed state using is-failed.",
    "systemctl is-failed mariadb",
    ["Command: systemctl is-failed mariadb"],
    "systemctl is-failed mariadb",
    [r"systemctl\s+is-failed\s+mariadb(\.service)?"])

add_scenario("sys-36", "Service Management", "View Explanation Help with journalctl -xe", "Intermediate",
    "View recent errors with catalog explanations jump to end.",
    "journalctl -xe",
    ["Command: journalctl -xe"],
    "journalctl -xe",
    [r"journalctl\s+(-xe|-ex)"])

add_scenario("sys-37", "Service Management", "Show Inactive Services on Host", "Intermediate",
    "List service units that are currently in inactive state.",
    "systemctl list-units --type=service --state=inactive",
    ["Command: systemctl list-units --type=service --state=inactive"],
    "systemctl list-units --type=service --state=inactive",
    [r"systemctl\s+list-units\s+--type=service\s+--state=inactive"])

add_scenario("sys-38", "Service Management", "Verify Journalctl Log Priority Warning and Above", "Intermediate",
    "Query logs with priority warning (level 4) or higher.",
    "journalctl -p warning",
    ["Command: journalctl -p warning"],
    "journalctl -p warning",
    [r"journalctl\s+.*-p\s+(warning|4)"])

add_scenario("sys-39", "Service Management", "Check systemd System State Overall", "Easy",
    "Check if overall system manager status is running, degraded, or maintenance.",
    "systemctl is-system-running",
    ["Command: systemctl is-system-running"],
    "systemctl is-system-running",
    [r"systemctl\s+is-system-running"])

add_scenario("sys-40", "Service Management", "Query Unit Journal Logs Without Pagination", "Easy",
    "Print logs for 'firewalld' to terminal without piping into less/pager.",
    "journalctl -u firewalld --no-pager",
    ["Command: journalctl -u firewalld --no-pager"],
    "journalctl -u firewalld --no-pager",
    [r"journalctl\s+.*-u\s+firewalld.*--no-pager", r"journalctl\s+.*--no-pager.*-u\s+firewalld"])

# =========================================================================
# 2. FIREWALL & SECURITY (firewall-cmd & SELinux) - 40 Scenarios
# =========================================================================

add_scenario("net-01", "Firewall & Network", "Permanently Allow HTTPS Service in Public Zone", "Easy",
    "Allow inbound HTTPS traffic in default public zone across reboots.",
    "firewall-cmd --permanent --zone=public --add-service=https",
    ["Command: firewall-cmd --permanent --zone=public --add-service=https"],
    "firewall-cmd --permanent --zone=public --add-service=https",
    [r"firewall-cmd\s+.*--permanent.*--zone=public.*--add-service=https", r"firewall-cmd\s+.*--add-service=https.*--permanent"])

add_scenario("net-02", "Firewall & Network", "Reload Firewalld Without Dropping Connections", "Easy",
    "Apply permanent firewall rules into live runtime without disconnects.",
    "firewall-cmd --reload",
    ["Command: firewall-cmd --reload"],
    "firewall-cmd --reload",
    [r"firewall-cmd\s+--reload"])

add_scenario("net-03", "Firewall & Network", "Audit Active Firewall Rules", "Easy",
    "Inspect active firewall state for public default zone.",
    "firewall-cmd --list-all",
    ["Command: firewall-cmd --list-all"],
    "firewall-cmd --list-all",
    [r"firewall-cmd\s+--list-all(\s+--zone=public)?"])

add_scenario("net-04", "Firewall & Network", "Open Custom TCP Port 8080 Permanently", "Intermediate",
    "Allow inbound traffic on custom port 8080/tcp permanently.",
    "firewall-cmd --permanent --add-port=8080/tcp",
    ["Command: firewall-cmd --permanent --add-port=8080/tcp"],
    "firewall-cmd --permanent --add-port=8080/tcp",
    [r"firewall-cmd\s+.*--permanent.*--add-port=8080\/tcp", r"firewall-cmd\s+.*--add-port=8080\/tcp.*--permanent"])

add_scenario("net-05", "Firewall & Network", "Remove Insecure Service Permanently from Firewall", "Intermediate",
    "Remove 'cockpit' service from permanent firewall configuration.",
    "firewall-cmd --permanent --zone=public --remove-service=cockpit",
    ["Command: firewall-cmd --permanent --zone=public --remove-service=cockpit"],
    "firewall-cmd --permanent --zone=public --remove-service=cockpit",
    [r"firewall-cmd\s+.*--permanent.*--remove-service=cockpit", r"firewall-cmd\s+.*--remove-service=cockpit.*--permanent"])

add_scenario("net-06", "Firewall & Network", "Enable IP Masquerading Permanently", "Intermediate",
    "Enable IP masquerading (NAT) permanently in public zone.",
    "firewall-cmd --permanent --zone=public --add-masquerade",
    ["Command: firewall-cmd --permanent --zone=public --add-masquerade"],
    "firewall-cmd --permanent --zone=public --add-masquerade",
    [r"firewall-cmd\s+.*--permanent.*--add-masquerade", r"firewall-cmd\s+.*--add-masquerade.*--permanent"])

add_scenario("net-07", "Firewall & Network", "Add Port Forwarding Rule in Firewalld", "Advanced",
    "Permanently forward incoming port 80 traffic to internal port 8080.",
    "firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080",
    ["Command: firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080"],
    "firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080",
    [r"firewall-cmd\s+.*--permanent.*--add-forward-port=port=80:proto=tcp:toport=8080"])

add_scenario("net-08", "Firewall & Network", "Check Running Status of Firewalld", "Easy",
    "Check whether firewalld is running using firewall-cmd --state.",
    "firewall-cmd --state",
    ["Command: firewall-cmd --state"],
    "firewall-cmd --state",
    [r"firewall-cmd\s+--state"])

add_scenario("net-09", "Firewall & Network", "Get Default Firewall Zone", "Easy",
    "Print the name of default firewalld zone.",
    "firewall-cmd --get-default-zone",
    ["Command: firewall-cmd --get-default-zone"],
    "firewall-cmd --get-default-zone",
    [r"firewall-cmd\s+--get-default-zone"])

add_scenario("net-10", "Firewall & Network", "Set Default Firewall Zone to Internal", "Intermediate",
    "Change the default zone to 'internal'.",
    "firewall-cmd --set-default-zone=internal",
    ["Command: firewall-cmd --set-default-zone=internal"],
    "firewall-cmd --set-default-zone=internal",
    [r"firewall-cmd\s+--set-default-zone=internal"])

add_scenario("net-11", "Firewall & Network", "List All Available Firewall Services", "Easy",
    "List all predefined services supported by firewalld.",
    "firewall-cmd --get-services",
    ["Command: firewall-cmd --get-services"],
    "firewall-cmd --get-services",
    [r"firewall-cmd\s+--get-services"])

add_scenario("net-12", "Firewall & Network", "Permanently Restrict SSH to Source Subnet", "Advanced",
    "Add permanent rich rule permitting SSH only from subnet 10.0.0.0/24.",
    'firewall-cmd --permanent --add-rich-rule=\'rule family="ipv4" source address="10.0.0.0/24" service name="ssh" accept\'',
    ["Command: firewall-cmd --permanent --add-rich-rule='rule family=\"ipv4\" source address=\"10.0.0.0/24\" service name=\"ssh\" accept'"],
    'firewall-cmd --permanent --add-rich-rule=\'rule family="ipv4" source address="10.0.0.0/24" service name="ssh" accept\'',
    [r'firewall-cmd\s+.*--permanent.*--add-rich-rule=.*10\.0\.0\.0\/24.*ssh.*accept'])

add_scenario("net-13", "Firewall & Network", "Remove Open Port from Permanent Firewall", "Intermediate",
    "Remove port 8080/tcp from permanent public configuration.",
    "firewall-cmd --permanent --remove-port=8080/tcp",
    ["Command: firewall-cmd --permanent --remove-port=8080/tcp"],
    "firewall-cmd --permanent --remove-port=8080/tcp",
    [r"firewall-cmd\s+.*--permanent.*--remove-port=8080\/tcp", r"firewall-cmd\s+.*--remove-port=8080\/tcp.*--permanent"])

add_scenario("net-14", "Firewall & Network", "Query If Service Is Permitted in Firewall", "Easy",
    "Check if 'http' service is currently enabled in public zone (returns 0 or 1).",
    "firewall-cmd --zone=public --query-service=http",
    ["Command: firewall-cmd --zone=public --query-service=http"],
    "firewall-cmd --zone=public --query-service=http",
    [r"firewall-cmd\s+.*--query-service=http"])

add_scenario("net-15", "Firewall & Network", "Bind Network Interface to Trusted Zone Permanently", "Intermediate",
    "Assign interface 'ens224' to 'trusted' zone permanently.",
    "firewall-cmd --permanent --zone=trusted --add-interface=ens224",
    ["Command: firewall-cmd --permanent --zone=trusted --add-interface=ens224"],
    "firewall-cmd --permanent --zone=trusted --add-interface=ens224",
    [r"firewall-cmd\s+.*--permanent.*--zone=trusted.*--add-interface=ens224", r"firewall-cmd\s+.*--zone=trusted.*--add-interface=ens224.*--permanent"])

add_scenario("net-16", "Firewall & Network", "List Active Firewall Zones and Interfaces", "Easy",
    "Print only active zones and their bound network interfaces.",
    "firewall-cmd --get-active-zones",
    ["Command: firewall-cmd --get-active-zones"],
    "firewall-cmd --get-active-zones",
    [r"firewall-cmd\s+--get-active-zones"])

add_scenario("net-17", "Firewall & Network", "Audit Rules Across All Zones", "Intermediate",
    "Display rules and configurations for all existing zones.",
    "firewall-cmd --list-all-zones",
    ["Command: firewall-cmd --list-all-zones"],
    "firewall-cmd --list-all-zones",
    [r"firewall-cmd\s+--list-all-zones"])

add_scenario("net-18", "Firewall & Network", "Temporarily Add Service to Running State", "Easy",
    "Add 'nfs' to public zone temporarily without --permanent flag.",
    "firewall-cmd --zone=public --add-service=nfs",
    ["Command: firewall-cmd --zone=public --add-service=nfs"],
    "firewall-cmd --zone=public --add-service=nfs",
    [r"firewall-cmd\s+(--zone=public\s+)?--add-service=nfs$"])

add_scenario("net-19", "Firewall & Network", "Query Current SELinux Enforcement Mode", "Easy",
    "Print current SELinux status using getenforce.",
    "getenforce",
    ["Command: getenforce"],
    "getenforce",
    [r"^getenforce$"])

add_scenario("net-20", "Firewall & Network", "Switch SELinux Temporarily to Permissive", "Easy",
    "Set SELinux runtime mode to Permissive (0) without rebooting.",
    "setenforce 0",
    ["Command: setenforce 0"],
    "setenforce 0",
    [r"^setenforce\s+(0|Permissive)$"])

add_scenario("net-21", "Firewall & Network", "Check Comprehensive SELinux Status", "Easy",
    "Display detailed SELinux operational status with sestatus.",
    "sestatus",
    ["Command: sestatus"],
    "sestatus",
    [r"^sestatus$"])

add_scenario("net-22", "Firewall & Network", "Restore Default SELinux File Context Recursively", "Intermediate",
    "Restore default SELinux context on /var/www/html recursively with verbose output.",
    "restorecon -Rv /var/www/html",
    ["Command: restorecon -Rv /var/www/html"],
    "restorecon -Rv /var/www/html",
    [r"restorecon\s+(-Rv|-vR|-R\s+-v|-v\s+-R)\s+\/var\/www\/html"])

add_scenario("net-23", "Firewall & Network", "Set Persistent SELinux Boolean Value", "Intermediate",
    "Enable boolean 'httpd_can_network_connect' persistently across reboots.",
    "setsebool -P httpd_can_network_connect on",
    ["Use setsebool -P with on or 1", "Command: setsebool -P httpd_can_network_connect on"],
    "setsebool -P httpd_can_network_connect on",
    [r"setsebool\s+-P\s+httpd_can_network_connect\s+(on|1)"])

add_scenario("net-24", "Firewall & Network", "Query State of Specific SELinux Boolean", "Easy",
    "Check current and pending state of boolean 'httpd_enable_homedirs'.",
    "getsebool httpd_enable_homedirs",
    ["Command: getsebool httpd_enable_homedirs"],
    "getsebool httpd_enable_homedirs",
    [r"getsebool\s+httpd_enable_homedirs"])

add_scenario("net-25", "Firewall & Network", "Display Listening TCP Sockets with ss", "Intermediate",
    "Display all listening (-l) TCP (-t) sockets with numeric ports (-n) and processes (-p).",
    "ss -tlpn",
    ["Command: ss -tlpn"],
    "ss -tlpn",
    [r"ss\s+-(tlpn|tulpn|tnlp|ltpn|lntp)"])

add_scenario("net-26", "Firewall & Network", "Bring Up NetworkManager Connection", "Easy",
    "Activate NetworkManager connection profile 'ens192'.",
    "nmcli con up ens192",
    ["Command: nmcli con up ens192"],
    "nmcli con up ens192",
    [r"nmcli\s+(con|connection)\s+up\s+([a-zA-Z0-9_-]+)"])

add_scenario("net-27", "Firewall & Network", "List Active NetworkManager Connections", "Easy",
    "Display only currently active NetworkManager connections.",
    "nmcli con show --active",
    ["Command: nmcli con show --active"],
    "nmcli con show --active",
    [r"nmcli\s+(con|connection)\s+show\s+--active"])

add_scenario("net-28", "Firewall & Network", "Display Network Device Status Overview", "Easy",
    "Display status of all network hardware devices with nmcli.",
    "nmcli dev status",
    ["Command: nmcli dev status"],
    "nmcli dev status",
    [r"nmcli\s+(device|dev)\s+status"])

add_scenario("net-29", "Firewall & Network", "Set Static DNS Servers on Connection", "Intermediate",
    "Configure connection 'ens192' with DNS servers 8.8.8.8 and 1.1.1.1.",
    'nmcli con mod ens192 ipv4.dns "8.8.8.8 1.1.1.1"',
    ["Command: nmcli con mod ens192 ipv4.dns \"8.8.8.8 1.1.1.1\""],
    'nmcli con mod ens192 ipv4.dns "8.8.8.8 1.1.1.1"',
    [r'nmcli\s+(con|connection)\s+mod(ify)?\s+ens192\s+ipv4\.dns\s+["\']?8\.8\.8\.8'])

add_scenario("net-30", "Firewall & Network", "Brief View of All Interface IP Addresses", "Easy",
    "Display concise one-line overview of all network interfaces and IPs.",
    "ip -br a",
    ["Command: ip -br a"],
    "ip -br a",
    [r"ip\s+(-br|-brief)\s+(a|addr|address)"])

add_scenario("net-31", "Firewall & Network", "Inspect Default Kernel Gateway Route", "Easy",
    "Display only the default route entry from routing table.",
    "ip route show default",
    ["Command: ip route show default"],
    "ip route show default",
    [r"ip\s+(route|r)\s+(show\s+)?default", r"ip\s+(route|r)\s*\|\s*grep\s+default"])

add_scenario("net-32", "Firewall & Network", "Display Kernel ARP Neighbor Table", "Easy",
    "Inspect Linux kernel neighbor/ARP table using iproute2.",
    "ip neigh show",
    ["Command: ip neigh show"],
    "ip neigh show",
    [r"ip\s+(neigh(bor)?\s+(show)?|n)"])

add_scenario("net-33", "Firewall & Network", "Display Socket Summary Statistics with ss", "Easy",
    "Print summary statistics for total, TCP, UDP sockets.",
    "ss -s",
    ["Command: ss -s"],
    "ss -s",
    [r"ss\s+(-s|--summary)"])

add_scenario("net-34", "Firewall & Network", "Ping Remote Host with 3 Count and 2s Timeout", "Easy",
    "Send exactly 3 ICMP echo requests with 2-second timeout to 192.168.1.1.",
    "ping -c 3 -W 2 192.168.1.1",
    ["Command: ping -c 3 -W 2 192.168.1.1"],
    "ping -c 3 -W 2 192.168.1.1",
    [r"ping\s+.*-c\s+3.*(-W\s+2)?.*192\.168\.1\.1"])

add_scenario("net-35", "Firewall & Network", "Check HTTP Response Headers with Curl", "Easy",
    "Fetch only HTTP headers (HEAD request) from http://localhost.",
    "curl -I http://localhost",
    ["Command: curl -I http://localhost"],
    "curl -I http://localhost",
    [r"curl\s+(-I|--head)\s+http:\/\/localhost"])

add_scenario("net-36", "Firewall & Network", "Configure Static IPv4 Address on Connection", "Intermediate",
    "Set static IP 192.168.1.50/24 with manual method on 'ens192'.",
    "nmcli con mod ens192 ipv4.addresses 192.168.1.50/24 ipv4.method manual",
    ["Command: nmcli con mod ens192 ipv4.addresses 192.168.1.50/24 ipv4.method manual"],
    "nmcli con mod ens192 ipv4.addresses 192.168.1.50/24 ipv4.method manual",
    [r"nmcli\s+.*con\s+mod.*ens192.*ipv4\.addresses\s+192\.168\.1\.50\/24.*ipv4\.method\s+manual"])

add_scenario("net-37", "Firewall & Network", "Add New Ethernet Connection Profile", "Intermediate",
    "Create a new ethernet connection profile named 'con-ens224' for device ens224.",
    "nmcli con add type ethernet con-name con-ens224 ifname ens224",
    ["Command: nmcli con add type ethernet con-name con-ens224 ifname ens224"],
    "nmcli con add type ethernet con-name con-ens224 ifname ens224",
    [r"nmcli\s+con\s+add\s+type\s+ethernet\s+con-name\s+con-ens224\s+ifname\s+ens224"])

add_scenario("net-38", "Firewall & Network", "Reload NetworkManager Connection Files from Disk", "Easy",
    "Instruct NetworkManager to reload connection keyfiles from /etc/NetworkManager/system-connections/.",
    "nmcli con reload",
    ["Command: nmcli con reload"],
    "nmcli con reload",
    [r"nmcli\s+con\s+reload"])

add_scenario("net-39", "Firewall & Network", "Check Socket Listening on Specific Port 3306", "Intermediate",
    "Filter ss output to check if port 3306 is listening.",
    "ss -tlpn sport = :3306",
    ["Command: ss -tlpn sport = :3306 or ss -tlpn | grep 3306"],
    "ss -tlpn sport = :3306",
    [r"ss\s+.*3306", r"ss\s+-tlpn\s*\|\s*grep\s+3306"])

add_scenario("net-40", "Firewall & Network", "Display Detailed Link Statistics with ip -s", "Easy",
    "Display packet transfer and error statistics for interface ens192.",
    "ip -s link show ens192",
    ["Command: ip -s link show ens192"],
    "ip -s link show ens192",
    [r"ip\s+-s\s+link\s+show\s+ens192"])

# =========================================================================
# 3. GREP & REGEX MASTERY - 30 Scenarios
# =========================================================================

add_scenario("grep-01", "Grep & Regex", "Filter HTTP 500 Server Errors with Line Numbers", "Easy",
    "Extract lines containing status code 500 with line numbers from httpd_access.log.",
    'grep -n " 500 " httpd_access.log',
    ["Command: grep -n \" 500 \" httpd_access.log"],
    'grep -n " 500 " httpd_access.log',
    [r'grep\s+(-n\s+["\']?\s*500\s*["\']?|["\']?\s*500\s*["\']?\s+-n)\s+httpd_access\.log'],
    setup_files={"httpd_access.log": '10.0.0.1 - [date] "GET / HTTP/1.1" 200 120\n10.0.0.2 - [date] "POST /api HTTP/1.1" 500 512\n'})

add_scenario("grep-02", "Grep & Regex", "Invert Match Comment & Empty Lines", "Intermediate",
    "Filter out lines starting with '#' and empty lines from sshd_config.test.",
    "grep -v -E '^(#|$)' sshd_config.test",
    ["Command: grep -v -E '^(#|$)' sshd_config.test"],
    "grep -v -E '^(#|$)' sshd_config.test",
    [r"grep\s+(-vE|-Ev|-E\s+-v|-v\s+-E)\s+['\"]?\^(\#|\$)[|](\#|\$)['\"]?\s+sshd_config\.test"],
    setup_files={"sshd_config.test": "# comment\nPort 22\n\nPermitRootLogin no\n"})

add_scenario("grep-03", "Grep & Regex", "Count Failed SSH Password Log Occurrences", "Easy",
    "Count matching lines recording 'Failed password' in auth.log.",
    'grep -c "Failed password" auth.log',
    ["Command: grep -c \"Failed password\" auth.log"],
    'grep -c "Failed password" auth.log',
    [r'grep\s+-c\s+["\']Failed password["\']\s+auth\.log'],
    setup_files={"auth.log": "Failed password for root\nAccepted publickey\nFailed password for admin\n"})

add_scenario("grep-04", "Grep & Regex", "Match Exact Whole Word Using Boundary", "Intermediate",
    "Search services.txt for exact word 'root' (not chroot or rootfs).",
    "grep -w 'root' services.txt",
    ["Command: grep -w 'root' services.txt"],
    "grep -w 'root' services.txt",
    [r"grep\s+-w\s+['\"]?root['\"]?\s+services\.txt"],
    setup_files={"services.txt": "user root\nuser chroot\nuser rootfs\n"})

add_scenario("grep-05", "Grep & Regex", "Display Lines with Context Surrounding Match", "Intermediate",
    "Search app.log for 'FATAL' showing 2 lines before and after.",
    "grep -C 2 'FATAL' app.log",
    ["Command: grep -C 2 'FATAL' app.log"],
    "grep -C 2 'FATAL' app.log",
    [r"grep\s+(-C\s*2|-B\s*2\s+-A\s*2)\s+['\"]?FATAL['\"]?\s+app\.log"],
    setup_files={"app.log": "line1\nline2\nFATAL: crash\nline4\nline5\n"})

add_scenario("grep-06", "Grep & Regex", "List Only Filenames Containing Match", "Easy",
    "Search *.conf for 'AllowOverride' printing only matching filenames.",
    "grep -l 'AllowOverride' *.conf",
    ["Command: grep -l 'AllowOverride' *.conf"],
    "grep -l 'AllowOverride' *.conf",
    [r"grep\s+-l\s+['\"]?AllowOverride['\"]?\s+\*\.conf"],
    setup_files={"a.conf": "AllowOverride All\n", "b.conf": "None\n"})

add_scenario("grep-07", "Grep & Regex", "Match Valid IPv4 Address Lines with ERE", "Advanced",
    "Search nodes.txt for lines starting with an IPv4 address.",
    "grep -E '^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' nodes.txt",
    ["Command: grep -E '^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' nodes.txt"],
    "grep -E '^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' nodes.txt",
    [r"grep\s+-E\s+['\"]\^\[0-9\]\{1,3\}"],
    setup_files={"nodes.txt": "192.168.1.1 server\nhostname-only\n"})

add_scenario("grep-08", "Grep & Regex", "Case-Insensitive Recursive Search Ignoring Binaries", "Intermediate",
    "Search directory configs recursively (-r), ignoring binaries (-I), ignoring case (-i) for 'API_KEY'.",
    "grep -rIi 'API_KEY' configs",
    ["Command: grep -rIi 'API_KEY' configs"],
    "grep -rIi 'API_KEY' configs",
    [r"grep\s+(-rIi|-riI|-Iri|-Iir)\s+['\"]?API_KEY['\"]?\s+configs"],
    setup_files={"configs/settings.json": '{"api_key": "123"}\n'})

add_scenario("grep-09", "Grep & Regex", "List Files NOT Matching Pattern with grep -L", "Intermediate",
    "Print filenames of *.conf that do NOT contain 'PermitRootLogin'.",
    "grep -L 'PermitRootLogin' *.conf",
    ["Command: grep -L 'PermitRootLogin' *.conf"],
    "grep -L 'PermitRootLogin' *.conf",
    [r"grep\s+-L\s+['\"]?PermitRootLogin['\"]?\s+\*\.conf"],
    setup_files={"sec.conf": "PermitRootLogin no\n", "insec.conf": "Port 22\n"})

add_scenario("grep-10", "Grep & Regex", "Extract Only the Matching String with grep -o", "Intermediate",
    "Extract only the IP address part from connection.log using grep -o.",
    "grep -o -E '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' connection.log",
    ["Command: grep -o -E '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' connection.log"],
    "grep -o -E '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' connection.log",
    [r"grep\s+(-oE|-Eo|-o\s+-E|-E\s+-o)\s+['\"][0-9]"],
    setup_files={"connection.log": "Connected from 10.0.0.5 port 22\n"})

add_scenario("grep-11", "Grep & Regex", "Quiet Match for Script Exit Code Check", "Easy",
    "Check if 'ansible' exists in /etc/passwd quietly without outputting text.",
    "grep -q 'ansible' /etc/passwd",
    ["Command: grep -q 'ansible' /etc/passwd"],
    "grep -q 'ansible' /etc/passwd",
    [r"grep\s+-q\s+['\"]?ansible['\"]?\s+\/etc\/passwd"])

add_scenario("grep-12", "Grep & Regex", "Match Lines Ending with Semicolon", "Easy",
    "Search code.c for lines ending with a semicolon (;).",
    "grep ';$' code.c",
    ["Command: grep ';$' code.c"],
    "grep ';$' code.c",
    [r"grep\s+['\"]?;\$['\"]?\s+code\.c"],
    setup_files={"code.c": "int x = 10;\nif (x) {\n    return 0;\n}\n"})

add_scenario("grep-13", "Grep & Regex", "Match Lines with Alternative Patterns using -e", "Intermediate",
    "Search syslog for either 'WARNING' or 'CRITICAL' using multiple -e flags.",
    "grep -e 'WARNING' -e 'CRITICAL' syslog",
    ["Command: grep -e 'WARNING' -e 'CRITICAL' syslog"],
    "grep -e 'WARNING' -e 'CRITICAL' syslog",
    [r"grep\s+-e\s+['\"]?WARNING['\"]?\s+-e\s+['\"]?CRITICAL['\"]?\s+syslog", r"grep\s+-E\s+['\"](WARNING|CRITICAL)"],
    setup_files={"syslog": "INFO: ok\nWARNING: disk\nCRITICAL: cpu\n"})

add_scenario("grep-14", "Grep & Regex", "Match Exact Entire Line with grep -x", "Intermediate",
    "Find lines in state.txt that match exactly 'ENABLED' with nothing else on the line.",
    "grep -x 'ENABLED' state.txt",
    ["Command: grep -x 'ENABLED' state.txt"],
    "grep -x 'ENABLED' state.txt",
    [r"grep\s+-x\s+['\"]?ENABLED['\"]?\s+state\.txt"],
    setup_files={"state.txt": "ENABLED\nENABLED_SOON\nPRE_ENABLED\n"})

add_scenario("grep-15", "Grep & Regex", "Match Hexadecimal MAC Addresses", "Advanced",
    "Search ens192.nmconnection for standard MAC addresses matching format XX:XX:XX:XX:XX:XX.",
    "grep -E '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' ens192.nmconnection",
    ["Command: grep -E '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' ens192.nmconnection"],
    "grep -E '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' ens192.nmconnection",
    [r"grep\s+-E\s+.*\[0-9A-Fa-f\]\{2\}:"],
    setup_files={"ens192.nmconnection": "HWADDR=52:54:00:12:34:56\nNAME=eth0\n"})

add_scenario("grep-16", "Grep & Regex", "Invert Match Excluding Multiple Status Codes", "Intermediate",
    "Read web.log. Exclude all lines containing status code 200 or 304.",
    "grep -v -E ' (200|304) ' web.log",
    ["Command: grep -v -E ' (200|304) ' web.log"],
    "grep -v -E ' (200|304) ' web.log",
    [r"grep\s+(-vE|-Ev|-E\s+-v|-v\s+-E)\s+.*(200\|304)"],
    setup_files={"web.log": 'GET / 200 120\nGET /img 304 0\nPOST /err 500 40\n'})

add_scenario("grep-17", "Grep & Regex", "Count Blank Lines in Script", "Easy",
    "Count how many completely empty lines exist in script.sh.",
    "grep -c '^$' script.sh",
    ["Command: grep -c '^$' script.sh"],
    "grep -c '^$' script.sh",
    [r"grep\s+-c\s+['\"]?\^\$['\"]?\s+script\.sh"],
    setup_files={"script.sh": "#!/bin/bash\n\necho 1\n\necho 2\n"})

add_scenario("grep-18", "Grep & Regex", "Match Standard UUID Format Lines", "Advanced",
    "Find lines containing a standard 36-character UUID with 8-4-4-4-12 hex format.",
    "grep -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' fstab.test",
    ["Command: grep -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' fstab.test"],
    "grep -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' fstab.test",
    [r"grep\s+-E\s+.*\[0-9a-f\]\{8\}-"],
    setup_files={"fstab.test": "UUID=c1b9d5a3-0000-4b21-8899-abcdef123456 / xfs defaults 0 0\n/dev/sda1 /boot ext4 defaults 0 0\n"})

add_scenario("grep-19", "Grep & Regex", "Print 3 Lines After Each Matching Error", "Easy",
    "Search trace.log for 'Exception' printing 3 lines after each match (-A 3).",
    "grep -A 3 'Exception' trace.log",
    ["Command: grep -A 3 'Exception' trace.log"],
    "grep -A 3 'Exception' trace.log",
    [r"grep\s+-A\s*3\s+['\"]?Exception['\"]?\s+trace\.log"],
    setup_files={"trace.log": "Exception in thread main\nat class.method\nat class.caller\nat main\ninfo\n"})

add_scenario("grep-20", "Grep & Regex", "Print 4 Lines Before Each Matching Error", "Easy",
    "Search trace.log for 'CRASH' printing 4 lines before each match (-B 4).",
    "grep -B 4 'CRASH' trace.log",
    ["Command: grep -B 4 'CRASH' trace.log"],
    "grep -B 4 'CRASH' trace.log",
    [r"grep\s+-B\s*4\s+['\"]?CRASH['\"]?\s+trace\.log"],
    setup_files={"trace.log": "step1\nstep2\nstep3\nstep4\nCRASH\n"})

add_scenario("grep-21", "Grep & Regex", "Filter Directives in /etc/fstab Starting with UUID", "Easy",
    "Search fstab for active lines beginning with 'UUID='.",
    "grep '^UUID=' /etc/fstab",
    ["Command: grep '^UUID=' /etc/fstab"],
    "grep '^UUID=' /etc/fstab",
    [r"grep\s+['\"]?\^UUID=['\"]?\s+\/etc\/fstab"])

add_scenario("grep-22", "Grep & Regex", "Match ISO-8601 Date Timestamps", "Intermediate",
    "Search events.log for lines starting with dates formatted as YYYY-MM-DD.",
    "grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' events.log",
    ["Command: grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' events.log"],
    "grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' events.log",
    [r"grep\s+-E\s+['\"]\^\[0-9\]\{4\}-\[0-9\]\{2\}-\[0-9\]\{2\}['\"]"],
    setup_files={"events.log": "2026-10-09 12:00:00 Started\ninvalid timestamp\n"})

add_scenario("grep-23", "Grep & Regex", "Match Port Digits in Config Lines", "Intermediate",
    "Search ports.conf for lines containing 'Port' followed by 2 to 5 digits.",
    "grep -E 'Port [0-9]{2,5}' ports.conf",
    ["Command: grep -E 'Port [0-9]{2,5}' ports.conf"],
    "grep -E 'Port [0-9]{2,5}' ports.conf",
    [r"grep\s+-E\s+['\"]Port\s+\[0-9\]\{2,5\}['\"]"],
    setup_files={"ports.conf": "Port 22\nPort 8080\nPort abc\n"})

add_scenario("grep-24", "Grep & Regex", "Extract Email Addresses Using Regex", "Advanced",
    "Extract valid email addresses from contacts.txt using grep -o -E.",
    "grep -o -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}' contacts.txt",
    ["Command: grep -o -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}' contacts.txt"],
    "grep -o -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}' contacts.txt",
    [r"grep\s+(-oE|-Eo|-o\s+-E|-E\s+-o)\s+.*@.*contacts\.txt"],
    setup_files={"contacts.txt": "Contact admin@example.com or support@redhat.com\n"})

add_scenario("grep-25", "Grep & Regex", "Invert Matching Specific User Logins", "Easy",
    "Filter out lines from users.log containing 'admin' or 'root'.",
    "grep -v -E '(admin|root)' users.log",
    ["Command: grep -v -E '(admin|root)' users.log"],
    "grep -v -E '(admin|root)' users.log",
    [r"grep\s+(-vE|-Ev|-E\s+-v|-v\s+-E)\s+.*(admin\|root)"],
    setup_files={"users.log": "user: admin\nuser: alice\nuser: root\nuser: bob\n"})

add_scenario("grep-26", "Grep & Regex", "Display Matching Line Numbers for TODO Items", "Easy",
    "Search code.py for 'TODO' displaying each match with its line number.",
    "grep -n 'TODO' code.py",
    ["Command: grep -n 'TODO' code.py"],
    "grep -n 'TODO' code.py",
    [r"grep\s+-n\s+['\"]?TODO['\"]?\s+code\.py"],
    setup_files={"code.py": "# TODO: fix bug\ndef run():\n    pass\n# TODO: test\n"})

add_scenario("grep-27", "Grep & Regex", "Search Only Compressed Gz Logs with zgrep", "Intermediate",
    "Search compressed file access.log.gz directly for '404' using zgrep.",
    "zgrep '404' access.log.gz",
    ["Command: zgrep '404' access.log.gz"],
    "zgrep '404' access.log.gz",
    [r"zgrep\s+['\"]?404['\"]?\s+access\.log\.gz"])

add_scenario("grep-28", "Grep & Regex", "Match Digits Only Lines", "Easy",
    "Search numbers.txt for lines composed exclusively of numeric digits.",
    "grep -E '^[0-9]+$' numbers.txt",
    ["Command: grep -E '^[0-9]+$' numbers.txt"],
    "grep -E '^[0-9]+$' numbers.txt",
    [r"grep\s+(-E\s+)?['\"]\^\[0-9\]\+\$['\"]\s+numbers\.txt"],
    setup_files={"numbers.txt": "12345\n12a34\n999\n"})

add_scenario("grep-29", "Grep & Regex", "Search Case-Insensitively for Warning or Error", "Easy",
    "Search app.log case-insensitively for 'error'.",
    "grep -i 'error' app.log",
    ["Command: grep -i 'error' app.log"],
    "grep -i 'error' app.log",
    [r"grep\s+-i\s+['\"]?error['\"]?\s+app\.log"],
    setup_files={"app.log": "ERROR: fatal\nInfo: ok\nError: minor\n"})

add_scenario("grep-30", "Grep & Regex", "Match Beginning and End of Word for Sysctl", "Intermediate",
    "Search sysctl.conf for directives starting with 'net.ipv4.ip_forward'.",
    "grep '^net\\.ipv4\\.ip_forward' sysctl.conf",
    ["Command: grep '^net\\.ipv4\\.ip_forward' sysctl.conf"],
    "grep '^net\\.ipv4\\.ip_forward' sysctl.conf",
    [r"grep\s+['\"]\^net\\\.ipv4\\\.ip_forward['\"]\s+sysctl\.conf"],
    setup_files={"sysctl.conf": "net.ipv4.ip_forward = 1\nnet.ipv6.conf.all.disable_ipv6 = 1\n"})

# =========================================================================
# 4. SED STREAM EDITING RECIPES - 25 Scenarios
# =========================================================================

add_scenario("sed-01", "Sed Stream Editing", "SELinux Enforce Substitution", "Easy",
    "Substitute 'SELINUX=enforcing' with 'SELINUX=permissive' in selinux.conf.",
    "sed 's/enforcing/permissive/' selinux.conf",
    ["Command: sed 's/enforcing/permissive/' selinux.conf"],
    "sed 's/enforcing/permissive/' selinux.conf",
    [r"sed\s+['\"]s\/enforcing\/permissive\/['\"]\s+selinux\.conf"],
    setup_files={"selinux.conf": "SELINUX=enforcing\nSELINUXTYPE=targeted\n"})

add_scenario("sed-02", "Sed Stream Editing", "Delete Comment Lines Using Pattern Addressing", "Intermediate",
    "Delete all lines beginning with '#' from crontab.test.",
    "sed '/^#/d' crontab.test",
    ["Command: sed '/^#/d' crontab.test"],
    "sed '/^#/d' crontab.test",
    [r"sed\s+['\"]\/\^\#\/d['\"]\s+crontab\.test"],
    setup_files={"crontab.test": "# backup\n0 2 * * * root /bin/backup\n# audit\n"})

add_scenario("sed-03", "Sed Stream Editing", "Replace Directory Path with Custom Delimiter", "Intermediate",
    "Replace '/var/www/html' with '/data/www/html' in vhost.conf using '#' delimiter.",
    "sed 's#/var/www/html#/data/www/html#g' vhost.conf",
    ["Command: sed 's#/var/www/html#/data/www/html#g' vhost.conf"],
    "sed 's#/var/www/html#/data/www/html#g' vhost.conf",
    [r"sed\s+['\"]s[#|@]\/var\/www\/html[#|@]\/data\/www\/html[#|@](g)?['\"]\s+vhost\.conf"],
    setup_files={"vhost.conf": 'DocumentRoot "/var/www/html"\n'})

add_scenario("sed-04", "Sed Stream Editing", "Print Specific Line Range with sed -n", "Intermediate",
    "Print lines 3 through 5 (inclusive) from audit.log.",
    "sed -n '3,5p' audit.log",
    ["Command: sed -n '3,5p' audit.log"],
    "sed -n '3,5p' audit.log",
    [r"sed\s+-n\s+['\"]3,5p['\"]\s+audit\.log"],
    setup_files={"audit.log": "1\n2\n3\n4\n5\n6\n7\n"})

add_scenario("sed-05", "Sed Stream Editing", "Strip Leading Whitespace Indentation", "Intermediate",
    "Remove leading spaces and tabs from code.txt.",
    "sed 's/^[ \t]*//' code.txt",
    ["Command: sed 's/^[ \t]*//' code.txt"],
    "sed 's/^[ \t]*//' code.txt",
    [r"sed\s+['\"]s\/\^\[\s*\\t\]\*\/.*['\"]\s+code\.txt"],
    setup_files={"code.txt": "    hello\n        world\n"})

add_scenario("sed-06", "Sed Stream Editing", "Delete All Empty Blank Lines with sed", "Easy",
    "Delete all empty lines (zero characters) from notes.txt.",
    "sed '/^$/d' notes.txt",
    ["Command: sed '/^$/d' notes.txt"],
    "sed '/^$/d' notes.txt",
    [r"sed\s+['\"]\/\^\$\/d['\"]\s+notes\.txt"],
    setup_files={"notes.txt": "a\n\nb\n\nc\n"})

add_scenario("sed-07", "Sed Stream Editing", "Strip Windows Carriage Returns", "Intermediate",
    "Remove trailing DOS/Windows \\r carriage returns from windows.txt.",
    "sed 's/\\r$//' windows.txt",
    ["Command: sed 's/\\r$//' windows.txt"],
    "sed 's/\\r$//' windows.txt",
    [r"sed\s+['\"]s\/\\r\$\/\/['\"]\s+windows\.txt"],
    setup_files={"windows.txt": "line1\r\nline2\r\n"})

add_scenario("sed-08", "Sed Stream Editing", "Global Replace All Occurrences on Lines", "Easy",
    "Replace every occurrence of 'foo' with 'bar' globally across words.txt.",
    "sed 's/foo/bar/g' words.txt",
    ["Command: sed 's/foo/bar/g' words.txt"],
    "sed 's/foo/bar/g' words.txt",
    [r"sed\s+['\"]s\/foo\/bar\/g['\"]\s+words\.txt"],
    setup_files={"words.txt": "foo and foo are foos\n"})

add_scenario("sed-09", "Sed Stream Editing", "Delete Specific First Line of File", "Easy",
    "Delete the first header line (line 1) from data.csv.",
    "sed '1d' data.csv",
    ["Command: sed '1d' data.csv"],
    "sed '1d' data.csv",
    [r"sed\s+['\"]1d['\"]\s+data\.csv"],
    setup_files={"data.csv": "id,name\n1,alice\n2,bob\n"})

add_scenario("sed-10", "Sed Stream Editing", "Delete the Last Line of File", "Easy",
    "Delete the final line ($d) from records.txt.",
    "sed '$d' records.txt",
    ["Command: sed '$d' records.txt"],
    "sed '$d' records.txt",
    [r"sed\s+['\"]\$d['\"]\s+records\.txt"],
    setup_files={"records.txt": "first\nsecond\ntrailer\n"})

add_scenario("sed-11", "Sed Stream Editing", "Replace Second Occurrence on Each Line", "Intermediate",
    "Replace only the 2nd occurrence of 'test' on each line with 'pass'.",
    "sed 's/test/pass/2' items.txt",
    ["Command: sed 's/test/pass/2' items.txt"],
    "sed 's/test/pass/2' items.txt",
    [r"sed\s+['\"]s\/test\/pass\/2['\"]\s+items\.txt"],
    setup_files={"items.txt": "test one test two test three\n"})

add_scenario("sed-12", "Sed Stream Editing", "Comment Out Matching Configuration Directives", "Intermediate",
    "Prepend '#' to lines starting with 'Listen 80' in httpd.conf.",
    "sed 's/^Listen 80/#Listen 80/' httpd.conf",
    ["Command: sed 's/^Listen 80/#Listen 80/' httpd.conf"],
    "sed 's/^Listen 80/#Listen 80/' httpd.conf",
    [r"sed\s+['\"]s\/\^Listen\s+80\/#Listen\s+80\/['\"]\s+httpd\.conf"],
    setup_files={"httpd.conf": "Listen 80\nServerName test\n"})

add_scenario("sed-13", "Sed Stream Editing", "Extract Block Between Two Delimiter Tags", "Advanced",
    "Print content exclusively between lines matching 'START' and 'END'.",
    "sed -n '/START/,/END/p' block.txt",
    ["Command: sed -n '/START/,/END/p' block.txt"],
    "sed -n '/START/,/END/p' block.txt",
    [r"sed\s+-n\s+['\"]\/START\/,\/END\/p['\"]\s+block\.txt"],
    setup_files={"block.txt": "preface\nSTART\ninside1\ninside2\nEND\npost\n"})

add_scenario("sed-14", "Sed Stream Editing", "Strip Trailing Whitespace at End of Lines", "Intermediate",
    "Remove all spaces and tabs at line ends from code.py.",
    "sed 's/[ \t]*$//' code.py",
    ["Command: sed 's/[ \t]*$//' code.py"],
    "sed 's/[ \t]*$//' code.py",
    [r"sed\s+['\"]s\/\[\s*\\t\]\*\$\/\/['\"]\s+code\.py"],
    setup_files={"code.py": "def test():   \n    return 1 \n"})

add_scenario("sed-15", "Sed Stream Editing", "Replace Only on Lines Matching Condition", "Intermediate",
    "On lines containing 'port', substitute '80' with '8080'.",
    "sed '/port/s/80/8080/' app.conf",
    ["Command: sed '/port/s/80/8080/' app.conf"],
    "sed '/port/s/80/8080/' app.conf",
    [r"sed\s+['\"]\/port\/s\/80\/8080\/['\"]\s+app\.conf"],
    setup_files={"app.conf": "port = 80\nmax_clients = 80\n"})

add_scenario("sed-16", "Sed Stream Editing", "In-Place File Edit with Backup Creation", "Intermediate",
    "Edit config.env in-place creating config.env.bak, replacing 'DEV' with 'PROD'.",
    "sed -i.bak 's/DEV/PROD/' config.env",
    ["Command: sed -i.bak 's/DEV/PROD/' config.env"],
    "sed -i.bak 's/DEV/PROD/' config.env",
    [r"sed\s+-i\.bak\s+['\"]s\/DEV\/PROD\/['\"]\s+config\.env"],
    setup_files={"config.env": "ENV=DEV\n"})

add_scenario("sed-17", "Sed Stream Editing", "Delete Lines 2 Through 4", "Easy",
    "Delete lines 2 through 4 from numbers.txt.",
    "sed '2,4d' numbers.txt",
    ["Command: sed '2,4d' numbers.txt"],
    "sed '2,4d' numbers.txt",
    [r"sed\s+['\"]2,4d['\"]\s+numbers\.txt"],
    setup_files={"numbers.txt": "1\n2\n3\n4\n5\n"})

add_scenario("sed-18", "Sed Stream Editing", "Transliterate Lowercase Vowels to Uppercase", "Intermediate",
    "Translate characters 'aeiou' to 'AEIOU' in vowels.txt using sed y command.",
    "sed 'y/aeiou/AEIOU/' vowels.txt",
    ["Command: sed 'y/aeiou/AEIOU/' vowels.txt"],
    "sed 'y/aeiou/AEIOU/' vowels.txt",
    [r"sed\s+['\"]y\/aeiou\/AEIOU\/['\"]\s+vowels\.txt"],
    setup_files={"vowels.txt": "quick brown fox\n"})

add_scenario("sed-19", "Sed Stream Editing", "Append Line After Match with 'a' Command", "Intermediate",
    "Append a new line 'Include conf.d/*.conf' after line matching 'ServerRoot' in httpd.conf.",
    "sed '/ServerRoot/a Include conf.d/*.conf' httpd.conf",
    ["Command: sed '/ServerRoot/a Include conf.d/*.conf' httpd.conf"],
    "sed '/ServerRoot/a Include conf.d/*.conf' httpd.conf",
    [r"sed\s+['\"]\/ServerRoot\/a\s+Include\s+conf\.d\/\*\.conf['\"]\s+httpd\.conf"],
    setup_files={"httpd.conf": "ServerRoot /etc/httpd\nListen 80\n"})

add_scenario("sed-20", "Sed Stream Editing", "Insert Line Before Match with 'i' Command", "Intermediate",
    "Insert '# Managed by Ansible' before line 1 in hosts.txt.",
    "sed '1i # Managed by Ansible' hosts.txt",
    ["Command: sed '1i # Managed by Ansible' hosts.txt"],
    "sed '1i # Managed by Ansible' hosts.txt",
    [r"sed\s+['\"]1i\s+# Managed by Ansible['\"]\s+hosts\.txt"],
    setup_files={"hosts.txt": "127.0.0.1 localhost\n"})

add_scenario("sed-21", "Sed Stream Editing", "Double Space Text by Appending Newlines", "Intermediate",
    "Insert an empty line after every line using sed G command.",
    "sed 'G' file.txt",
    ["Command: sed 'G' file.txt"],
    "sed 'G' file.txt",
    [r"sed\s+['\"]G['\"]\s+file\.txt"],
    setup_files={"file.txt": "line1\nline2\n"})

add_scenario("sed-22", "Sed Stream Editing", "Delete Lines NOT Matching Pattern", "Intermediate",
    "Delete all lines except those matching 'KEEP' in keep.txt.",
    "sed '/KEEP/!d' keep.txt",
    ["Command: sed '/KEEP/!d' keep.txt"],
    "sed '/KEEP/!d' keep.txt",
    [r"sed\s+['\"]\/KEEP\/!d['\"]\s+keep\.txt"],
    setup_files={"keep.txt": "drop1\nKEEP this\ndrop2\n"})

add_scenario("sed-23", "Sed Stream Editing", "Replace HTML Tags with Nothing", "Advanced",
    "Strip all basic HTML tags (<...>) from page.html.",
    "sed 's/<[^>]*>//g' page.html",
    ["Command: sed 's/<[^>]*>//g' page.html"],
    "sed 's/<[^>]*>//g' page.html",
    [r"sed\s+['\"]s\/<\[\^>\]\*>\/\/g['\"]\s+page\.html"],
    setup_files={"page.html": "<h1>Title</h1><p>Text</p>\n"})

add_scenario("sed-24", "Sed Stream Editing", "Print Only the First Line and Quit", "Easy",
    "Print line 1 and immediately quit using sed '1q'.",
    "sed '1q' big.log",
    ["Command: sed '1q' big.log"],
    "sed '1q' big.log",
    [r"sed\s+['\"]1q['\"]\s+big\.log"],
    setup_files={"big.log": "first\nsecond\nthird\n"})

add_scenario("sed-25", "Sed Stream Editing", "Substitute Port at the End of Line", "Easy",
    "Change ':80' to ':443' at the end of the line in endpoint.txt.",
    "sed 's/:80$/:443/' endpoint.txt",
    ["Command: sed 's/:80$/:443/' endpoint.txt"],
    "sed 's/:80$/:443/' endpoint.txt",
    [r"sed\s+['\"]s\/:80\$\/:443\/['\"]\s+endpoint\.txt"],
    setup_files={"endpoint.txt": "http://example.com:80\n"})

# =========================================================================
# 5. AWK PROCESSING & DATA TRANSFORMATION - 25 Scenarios
# =========================================================================

add_scenario("awk-01", "Awk Processing", "Extract System Users with Bash Shell", "Intermediate",
    "Using delimiter ':', print $1 and $3 as 'user:UID' for accounts with shell '/bin/bash'.",
    'awk -F\':\' \'$7 == "/bin/bash" {print $1":"$3}\' passwd.sample',
    ["Command: awk -F\':\' \'$7 == \"/bin/bash\" {print $1\":\"$3}\' passwd.sample"],
    'awk -F\':\' \'$7 == "/bin/bash" {print $1":"$3}\' passwd.sample',
    [r"awk\s+-F['\"]?:['\"]?\s+['\"]\s*\$7\s*==\s*[\"']/bin/bash[\"'].*passwd\.sample"],
    setup_files={"passwd.sample": "root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\nansible:x:1001:1001::/home/ansible:/bin/bash\n"})

add_scenario("awk-02", "Awk Processing", "Sum Column Values of Log Transfer Bytes", "Intermediate",
    "Calculate and print total sum of transferred byte sizes in column 2 of transfers.tsv.",
    "awk '{sum += $2} END {print sum}' transfers.tsv",
    ["Command: awk '{sum += $2} END {print sum}' transfers.tsv"],
    "awk '{sum += $2} END {print sum}' transfers.tsv",
    [r"awk\s+['\"]\{sum\s*\+=\s*\$2\}\s*END\s*\{\s*print\s+sum\s*\}['\"]\s+transfers\.tsv"],
    setup_files={"transfers.tsv": "fileA 100\nfileB 250\nfileC 50\n"})

add_scenario("awk-03", "Awk Processing", "Print Last Field of Variable Length Log Lines", "Intermediate",
    "Print only the final field ($NF) of each line in commands.log.",
    "awk '{print $NF}' commands.log",
    ["Command: awk '{print $NF}' commands.log"],
    "awk '{print $NF}' commands.log",
    [r"awk\s+['\"]\{print\s+\$NF\}['\"]\s+commands\.log"],
    setup_files={"commands.log": "cmd1 arg1\ncmd2 arg1 arg2 end\ncmd3 done\n"})

add_scenario("awk-04", "Awk Processing", "Filter Human Interactive Users with UID >= 1000", "Intermediate",
    "Print username from passwd.sample for users with UID >= 1000 and < 65534.",
    "awk -F':' '$3 >= 1000 && $3 < 65534 {print $1}' passwd.sample",
    ["Command: awk -F':' '$3 >= 1000 && $3 < 65534 {print $1}' passwd.sample"],
    "awk -F':' '$3 >= 1000 && $3 < 65534 {print $1}' passwd.sample",
    [r"awk\s+-F['\"]?:['\"]?\s+['\"]\s*\$3\s*>=\s*1000"],
    setup_files={"passwd.sample": "root:x:0:0:::/bin/bash\nuser1:x:1001:1001:::/bin/bash\nnobody:x:65534:65534:::/sbin/nologin\n"})

add_scenario("awk-05", "Awk Processing", "Custom Output Field Separator with OFS", "Intermediate",
    "Print col 1 and 2 separated by ' -> ' from tab-delimited users.tsv.",
    'awk -F\'\\t\' \'BEGIN {OFS=" -> "} {print $1, $2}\' users.tsv',
    ["Command: awk -F'\\t' 'BEGIN {OFS=\" -> \"} {print $1, $2}' users.tsv"],
    'awk -F\'\\t\' \'BEGIN {OFS=" -> "} {print $1, $2}\' users.tsv',
    [r'awk\s+.*BEGIN\s*\{\s*OFS\s*=\s*["\']\s*->\s*["\']\s*\}.*users\.tsv'],
    setup_files={"users.tsv": "alice\tadmin\nbob\tuser\n"})

add_scenario("awk-06", "Awk Processing", "Print Total Number of Records in File", "Easy",
    "Use awk's built-in NR variable in END block to print total record count of items.txt.",
    "awk 'END {print NR}' items.txt",
    ["Command: awk 'END {print NR}' items.txt"],
    "awk 'END {print NR}' items.txt",
    [r"awk\s+['\"]END\s*\{\s*print\s+NR\s*\}['\"]\s+items\.txt"],
    setup_files={"items.txt": "a\nb\nc\nd\ne\n"})

add_scenario("awk-07", "Awk Processing", "Compute Average Value of Column 2", "Intermediate",
    "Calculate and print average of values in column 2 of scores.txt.",
    "awk '{sum += $2} END {print sum/NR}' scores.txt",
    ["Command: awk '{sum += $2} END {print sum/NR}' scores.txt"],
    "awk '{sum += $2} END {print sum/NR}' scores.txt",
    [r"awk\s+['\"].*sum\s*\+=\s*\$2.*print\s+sum\/NR.*scores\.txt"],
    setup_files={"scores.txt": "test1 80\ntest2 100\ntest3 90\n"})

add_scenario("awk-08", "Awk Processing", "Filter Lines Having More Than 4 Fields", "Easy",
    "Print lines from table.txt where Number of Fields (NF) is greater than 4.",
    "awk 'NF > 4' table.txt",
    ["Command: awk 'NF > 4' table.txt"],
    "awk 'NF > 4' table.txt",
    [r"awk\s+['\"]NF\s*>\s*4['\"]\s+table\.txt"],
    setup_files={"table.txt": "a b c\na b c d e\na b\n"})

add_scenario("awk-09", "Awk Processing", "Count Frequency of IP Addresses with Array", "Advanced",
    "Count and print frequency of IPs in column 1 of access.log using associative arrays.",
    "awk '{ips[$1]++} END {for (ip in ips) print ips[ip], ip}' access.log",
    ["Command: awk '{ips[$1]++} END {for (ip in ips) print ips[ip], ip}' access.log"],
    "awk '{ips[$1]++} END {for (ip in ips) print ips[ip], ip}' access.log",
    [r"awk\s+['\"].*ips\[\$1\]\+\+.*for\s*\(.*access\.log"],
    setup_files={"access.log": "10.0.0.1 - /index\n10.0.0.2 - /login\n10.0.0.1 - /img\n"})

add_scenario("awk-10", "Awk Processing", "Filter Rows Where Column 3 Matches Regex", "Intermediate",
    "Print rows in services.txt where column 3 starts with 'HTTP'.",
    "awk '$3 ~ /^HTTP/' services.txt",
    ["Command: awk '$3 ~ /^HTTP/' services.txt"],
    "awk '$3 ~ /^HTTP/' services.txt",
    [r"awk\s+['\"]\s*\$3\s*~\s*\/(\^)?HTTP\/['\"]\s+services\.txt"],
    setup_files={"services.txt": "1 web HTTPS\n2 mail SMTP\n3 web HTTP/1.1\n"})

add_scenario("awk-11", "Awk Processing", "Format Output with printf Columns", "Intermediate",
    "Print formatted columns '%-10s %5d\\n' for $1 and $2 from inventory.txt.",
    "awk '{printf \"%-10s %5d\\n\", $1, $2}' inventory.txt",
    ["Command: awk '{printf \"%-10s %5d\\n\", $1, $2}' inventory.txt"],
    "awk '{printf \"%-10s %5d\\n\", $1, $2}' inventory.txt",
    [r"awk\s+['\"].*printf.*%-10s.*inventory\.txt"],
    setup_files={"inventory.txt": "apples 50\noranges 120\n"})

add_scenario("awk-12", "Awk Processing", "Print Line Number Alongside Each Record", "Easy",
    "Print record number NR followed by the full line $0 from sample.txt.",
    "awk '{print NR, $0}' sample.txt",
    ["Command: awk '{print NR, $0}' sample.txt"],
    "awk '{print NR, $0}' sample.txt",
    [r"awk\s+['\"]\{print\s+NR,\s*\$0\}['\"]\s+sample\.txt"],
    setup_files={"sample.txt": "first\nsecond\nthird\n"})

add_scenario("awk-13", "Awk Processing", "Print Lines Exceeding 80 Characters in Length", "Intermediate",
    "Find and print lines in code.py whose length exceeds 80 characters.",
    "awk 'length($0) > 80' code.py",
    ["Command: awk 'length($0) > 80' code.py"],
    "awk 'length($0) > 80' code.py",
    [r"awk\s+['\"]length\((\$0)?\)\s*>\s*80['\"]\s+code\.py"],
    setup_files={"code.py": "short line\n" + "x" * 85 + "\n"})

add_scenario("awk-14", "Awk Processing", "Preserve Header Line While Filtering Rows", "Intermediate",
    "In metrics.csv (comma delimited), print line 1 (header), and for subsequent lines print only where $2 > 50.",
    "awk -F',' 'NR==1 || $2 > 50' metrics.csv",
    ["Command: awk -F',' 'NR==1 || $2 > 50' metrics.csv"],
    "awk -F',' 'NR==1 || $2 > 50' metrics.csv",
    [r"awk\s+-F['\"]?,['\"]?\s+['\"]NR\s*==\s*1\s*\|\|\s*\$2\s*>\s*50['\"]\s+metrics\.csv"],
    setup_files={"metrics.csv": "server,load\nsrv1,20\nsrv2,85\nsrv3,90\n"})

add_scenario("awk-15", "Awk Processing", "Calculate Column Value Differences", "Intermediate",
    "Print $1 and the difference ($3 - $2) from numbers.tsv.",
    "awk '{print $1, $3 - $2}' numbers.tsv",
    ["Command: awk '{print $1, $3 - $2}' numbers.tsv"],
    "awk '{print $1, $3 - $2}' numbers.tsv",
    [r"awk\s+['\"]\{print\s+\$1,\s*\$3\s*-\s*\$2\}['\"]\s+numbers\.tsv"],
    setup_files={"numbers.tsv": "row1 10 30\nrow2 20 50\n"})

add_scenario("awk-16", "Awk Processing", "Find Maximum Value in Column 2", "Intermediate",
    "Find and print the highest number in column 2 of stats.txt.",
    "awk '$2 > max {max = $2} END {print max}' stats.txt",
    ["Command: awk '$2 > max {max = $2} END {print max}' stats.txt"],
    "awk '$2 > max {max = $2} END {print max}' stats.txt",
    [r"awk\s+['\"].*\$2\s*>\s*max.*print\s+max.*stats\.txt"],
    setup_files={"stats.txt": "a 15\nb 95\nc 40\n"})

add_scenario("awk-17", "Awk Processing", "Substr Function to Extract Date Substring", "Advanced",
    "Extract first 10 characters (YYYY-MM-DD) from timestamp column 1 using substr($1, 1, 10).",
    "awk '{print substr($1, 1, 10)}' logs.txt",
    ["Command: awk '{print substr($1, 1, 10)}' logs.txt"],
    "awk '{print substr($1, 1, 10)}' logs.txt",
    [r"awk\s+['\"]\{print\s+substr\(\$1,\s*1,\s*10\)\}['\"]\s+logs\.txt"],
    setup_files={"logs.txt": "2026-10-09T12:34:56Z event1\n2026-10-09T13:00:00Z event2\n"})

add_scenario("awk-18", "Awk Processing", "Count Occurrences Where Field Equals Target", "Easy",
    "Count how many rows have column 2 equal to 'SUCCESS' in status.txt.",
    "awk '$2 == \"SUCCESS\" {count++} END {print count}' status.txt",
    ["Command: awk '$2 == \"SUCCESS\" {count++} END {print count}' status.txt"],
    "awk '$2 == \"SUCCESS\" {count++} END {print count}' status.txt",
    [r"awk\s+['\"].*\$2\s*==\s*[\"']SUCCESS[\"'].*count.*status\.txt"],
    setup_files={"status.txt": "job1 SUCCESS\njob2 FAILED\njob3 SUCCESS\n"})

add_scenario("awk-19", "Awk Processing", "Print Range of Records from NR 5 to 8", "Easy",
    "Print records where NR is between 5 and 8 (inclusive).",
    "awk 'NR >= 5 && NR <= 8' records.txt",
    ["Command: awk 'NR >= 5 && NR <= 8' records.txt"],
    "awk 'NR >= 5 && NR <= 8' records.txt",
    [r"awk\s+['\"]NR\s*>=\s*5\s*&&\s*NR\s*<=\s*8['\"]\s+records\.txt"],
    setup_files={"records.txt": "\n".join([f"line {i}" for i in range(1, 11)]) + "\n"})

add_scenario("awk-20", "Awk Processing", "Replace Field 2 Value Before Printing", "Intermediate",
    "In data.txt, change $2 to 'REDACTED' and print the modified full line.",
    "awk '{$2 = \"REDACTED\"; print}' data.txt",
    ["Command: awk '{$2 = \"REDACTED\"; print}' data.txt"],
    "awk '{$2 = \"REDACTED\"; print}' data.txt",
    [r"awk\s+['\"]\{\s*\$2\s*=\s*[\"']REDACTED[\"'];?\s*print\}['\"]\s+data\.txt"],
    setup_files={"data.txt": "user secret pass\nadmin secret pass\n"})

add_scenario("awk-21", "Awk Processing", "Print Second to Last Field $(NF-1)", "Intermediate",
    "Extract the second-to-last field $(NF-1) from variable length rows in items.txt.",
    "awk '{print $(NF-1)}' items.txt",
    ["Command: awk '{print $(NF-1)}' items.txt"],
    "awk '{print $(NF-1)}' items.txt",
    [r"awk\s+['\"]\{print\s+\$\(NF-1\)\}['\"]\s+items\.txt"],
    setup_files={"items.txt": "a b c d\nx y z\n"})

add_scenario("awk-22", "Awk Processing", "Case-Insensitive Match in Awk using tolower", "Intermediate",
    "Print rows in auth.log where tolower($0) matches 'error'.",
    "awk 'tolower($0) ~ /error/' auth.log",
    ["Command: awk 'tolower($0) ~ /error/' auth.log"],
    "awk 'tolower($0) ~ /error/' auth.log",
    [r"awk\s+['\"]tolower\(\$0\)\s*~\s*\/error\/['\"]\s+auth\.log"],
    setup_files={"auth.log": "ERROR: fail\nInfo: ok\nError: minor\n"})

add_scenario("awk-23", "Awk Processing", "Multiply Two Columns and Sum Total", "Intermediate",
    "Calculate total revenue by summing ($2 * $3) (quantity * price) in orders.tsv.",
    "awk '{total += $2 * $3} END {print total}' orders.tsv",
    ["Command: awk '{total += $2 * $3} END {print total}' orders.tsv"],
    "awk '{total += $2 * $3} END {print total}' orders.tsv",
    [r"awk\s+['\"].*total\s*\+=\s*\$2\s*\*\s*\$3.*print\s+total.*orders\.tsv"],
    setup_files={"orders.tsv": "item1 2 10\nitem2 5 20\n"})

add_scenario("awk-24", "Awk Processing", "Print Unique Entries in Column 1 Without External Sort", "Advanced",
    "Print unique entries from column 1 of dups.txt preserving first appearance.",
    "awk '!seen[$1]++' dups.txt",
    ["Command: awk '!seen[$1]++' dups.txt"],
    "awk '!seen[$1]++' dups.txt",
    [r"awk\s+['\"]!seen\[\$1\]\+\+['\"]\s+dups\.txt"],
    setup_files={"dups.txt": "a 1\nb 2\na 3\nc 4\nb 5\n"})

add_scenario("awk-25", "Awk Processing", "Sum Columns from df -h Output in Megabytes", "Intermediate",
    "Sum column 4 (available blocks) in df.txt skipping the first header line.",
    "awk 'NR > 1 {sum += $4} END {print sum}' df.txt",
    ["Command: awk 'NR > 1 {sum += $4} END {print sum}' df.txt"],
    "awk 'NR > 1 {sum += $4} END {print sum}' df.txt",
    [r"awk\s+['\"]NR\s*>\s*1\s*\{\s*sum\s*\+=\s*\$4.*print\s+sum.*df\.txt"],
    setup_files={"df.txt": "Filesystem 1K-blocks Used Available Use% Mounted\n/dev/sda1 1000 200 800 20% /\n/dev/sda2 2000 500 1500 25% /home\n"})

# =========================================================================
# 6. FIND & PERMISSIONS - 20 Scenarios
# =========================================================================

add_scenario("find-01", "Find & Permissions", "Locate Insecure World-Writable Files", "Intermediate",
    "Search './target_dir' for regular files with permissions 0777 (world-writable).",
    "find ./target_dir -type f -perm 0777",
    ["Command: find ./target_dir -type f -perm 0777"],
    "find ./target_dir -type f -perm 0777",
    [r"find\s+(\.\/)?target_dir\s+(-type\s+f\s+-perm\s+(0?777)|-perm\s+(0?777)\s+-type\s+f)"],
    setup_files={"target_dir/safe.sh": "ok", "target_dir/insecure.tmp": "bad"},
    setup_perms={"target_dir/safe.sh": 0o755, "target_dir/insecure.tmp": 0o777})

add_scenario("find-02", "Find & Permissions", "Find Log Files Modified Within Last 24 Hours", "Intermediate",
    "Search './var_logs' for files ending in '.log' modified within the last 1 day.",
    "find ./var_logs -name '*.log' -mtime -1",
    ["Command: find ./var_logs -name '*.log' -mtime -1"],
    "find ./var_logs -name '*.log' -mtime -1",
    [r"find\s+(\.\/)?var_logs\s+.*-name\s+['\"]?\*\.log['\"]?.*-mtime\s+-1"],
    setup_files={"var_logs/app.log": "today", "var_logs/old.txt": "text"})

add_scenario("find-03", "Find & Permissions", "Find SUID Binaries on System", "Advanced",
    "Search './bin_dir' for regular files that have SUID (octal 4000) permission bit set.",
    "find ./bin_dir -type f -perm -4000",
    ["Command: find ./bin_dir -type f -perm -4000"],
    "find ./bin_dir -type f -perm -4000",
    [r"find\s+(\.\/)?bin_dir\s+(-type\s+f\s+-perm\s+[-/]4000|-perm\s+[-/]4000\s+-type\s+f)"],
    setup_files={"bin_dir/suid_prog": "bin", "bin_dir/norm_prog": "bin"},
    setup_perms={"bin_dir/suid_prog": 0o4755, "bin_dir/norm_prog": 0o755})

add_scenario("find-04", "Find & Permissions", "Find Files Larger Than 10 Megabytes", "Intermediate",
    "Search './data_store' for regular files strictly larger than 10 Megabytes (+10M).",
    "find ./data_store -type f -size +10M",
    ["Command: find ./data_store -type f -size +10M"],
    "find ./data_store -type f -size +10M",
    [r"find\s+(\.\/)?data_store\s+(-type\s+f\s+-size\s+\+10M|-size\s+\+10M\s+-type\s+f)"],
    setup_files={"data_store/s.txt": "small", "data_store/b.img": "__SPARSE_BYTES:12582912"})

add_scenario("find-05", "Find & Permissions", "Find All Empty Directories", "Easy",
    "Search './tree' for directories that contain no files or subdirectories.",
    "find ./tree -type d -empty",
    ["Command: find ./tree -type d -empty"],
    "find ./tree -type d -empty",
    [r"find\s+(\.\/)?tree\s+(-type\s+d\s+-empty|-empty\s+-type\s+d)"],
    setup_files={"tree/not_empty/a": "1", "tree/empty_dir/.keep": ""})

add_scenario("find-06", "Find & Permissions", "Find and Execute Chmod in Batches", "Intermediate",
    "Find all *.sh files under './scripts' and chmod them to 755 using -exec ... {} +.",
    "find ./scripts -type f -name '*.sh' -exec chmod 755 {} +",
    ["Command: find ./scripts -type f -name '*.sh' -exec chmod 755 {} +"],
    "find ./scripts -type f -name '*.sh' -exec chmod 755 {} +",
    [r"find\s+(\.\/)?scripts\s+.*-name\s+['\"]?\*\.sh['\"]?\s+-exec\s+chmod\s+755\s+\{\}\s+\+"],
    setup_files={"scripts/run.sh": "echo 1\n", "scripts/test.sh": "echo 2\n"})

add_scenario("find-07", "Find & Permissions", "Find Files Owned by Specific User", "Easy",
    "Search directory './home' for files owned by user 'nobody'.",
    "find ./home -user nobody",
    ["Command: find ./home -user nobody"],
    "find ./home -user nobody",
    [r"find\s+(\.\/)?home\s+.*-user\s+nobody"],
    setup_files={"home/user_file": "data"})

add_scenario("find-08", "Find & Permissions", "Find SGID Binaries on Directory", "Advanced",
    "Search './bin_dir' for files with SGID bit set (octal 2000).",
    "find ./bin_dir -type f -perm -2000",
    ["Command: find ./bin_dir -type f -perm -2000"],
    "find ./bin_dir -type f -perm -2000",
    [r"find\s+(\.\/)?bin_dir\s+.*-perm\s+[-/]2000"],
    setup_files={"bin_dir/sgid_bin": "b"},
    setup_perms={"bin_dir/sgid_bin": 0o2755})

add_scenario("find-09", "Find & Permissions", "Find Files Modified in Last 30 Minutes", "Intermediate",
    "Locate regular files in /tmp modified less than 30 minutes ago (-mmin -30).",
    "find /tmp -type f -mmin -30",
    ["Command: find /tmp -type f -mmin -30"],
    "find /tmp -type f -mmin -30",
    [r"find\s+\/tmp\s+(-type\s+f\s+-mmin\s+-30|-mmin\s+-30\s+-type\s+f)"])

add_scenario("find-10", "Find & Permissions", "Limit Search Depth to Maximum 2 Directories", "Easy",
    "Find all .conf files under './etc' without descending more than 2 levels deep.",
    "find ./etc -maxdepth 2 -name '*.conf'",
    ["Command: find ./etc -maxdepth 2 -name '*.conf'"],
    "find ./etc -maxdepth 2 -name '*.conf'",
    [r"find\s+(\.\/)?etc\s+.*-maxdepth\s+2.*-name\s+['\"]?\*\.conf['\"]?"],
    setup_files={"etc/app.conf": "1", "etc/sub/deep.conf": "2"})

add_scenario("find-11", "Find & Permissions", "Find Broken Symbolic Links", "Advanced",
    "Find broken/dangling symbolic links in directory './links'.",
    "find ./links -xtype l",
    ["Command: find ./links -xtype l"],
    "find ./links -xtype l",
    [r"find\s+(\.\/)?links\s+.*-xtype\s+l"])

add_scenario("find-12", "Find & Permissions", "Case-Insensitive Filename Search", "Easy",
    "Search directory './docs' for files matching 'readme.txt' case-insensitively.",
    "find ./docs -iname 'readme.txt'",
    ["Command: find ./docs -iname 'readme.txt'"],
    "find ./docs -iname 'readme.txt'",
    [r"find\s+(\.\/)?docs\s+.*-iname\s+['\"]?readme\.txt['\"]?"],
    setup_files={"docs/README.TXT": "docs"})

add_scenario("find-13", "Find & Permissions", "Find Files with Read-Only Permissions 0444", "Intermediate",
    "Search './archive' for files with exact permissions 0444 (read-only for all).",
    "find ./archive -type f -perm 0444",
    ["Command: find ./archive -type f -perm 0444"],
    "find ./archive -type f -perm 0444",
    [r"find\s+(\.\/)?archive\s+.*-perm\s+(0?444)"],
    setup_files={"archive/locked.txt": "1"},
    setup_perms={"archive/locked.txt": 0o444})

add_scenario("find-14", "Find & Permissions", "Find and Delete Files Matching Pattern Directly", "Intermediate",
    "Find all *.tmp files in './scratch' and delete them using find's -delete action.",
    "find ./scratch -type f -name '*.tmp' -delete",
    ["Command: find ./scratch -type f -name '*.tmp' -delete"],
    "find ./scratch -type f -name '*.tmp' -delete",
    [r"find\s+(\.\/)?scratch\s+.*-name\s+['\"]?\*\.tmp['\"]?\s+-delete"],
    setup_files={"scratch/temp1.tmp": "1"})

add_scenario("find-15", "Find & Permissions", "Find Files Accessed More Than 30 Days Ago", "Intermediate",
    "Locate files in './cache' that have not been accessed in over 30 days (-atime +30).",
    "find ./cache -type f -atime +30",
    ["Command: find ./cache -type f -atime +30"],
    "find ./cache -type f -atime +30",
    [r"find\s+(\.\/)?cache\s+.*-atime\s+\+30"],
    setup_files={"cache/old.bin": "bin"})

add_scenario("find-16", "Find & Permissions", "Find Directories with Sticky Bit Set", "Advanced",
    "Search /tmp for directories having the sticky bit set (octal 1000).",
    "find /tmp -type d -perm -1000",
    ["Command: find /tmp -type d -perm -1000"],
    "find /tmp -type d -perm -1000",
    [r"find\s+\/tmp\s+(-type\s+d\s+-perm\s+[-/]1000|-perm\s+[-/]1000\s+-type\s+d)"])

add_scenario("find-17", "Find & Permissions", "Find Regular Files Between 1M and 5M in Size", "Intermediate",
    "Locate files under './media' whose size is between 1 Megabyte and 5 Megabytes.",
    "find ./media -type f -size +1M -size -5M",
    ["Command: find ./media -type f -size +1M -size -5M"],
    "find ./media -type f -size +1M -size -5M",
    [r"find\s+(\.\/)?media\s+.*-size\s+\+1M\s+-size\s+-5M"],
    setup_files={"media/song.mp3": "__SPARSE_BYTES:2621440"})

add_scenario("find-18", "Find & Permissions", "Find Files Not Owned by Current User", "Intermediate",
    "Search './shared' for files not owned by root (! -user root).",
    "find ./shared ! -user root",
    ["Command: find ./shared ! -user root"],
    "find ./shared ! -user root",
    [r"find\s+(\.\/)?shared\s+(!\s+-user\s+root|-not\s+-user\s+root)"],
    setup_files={"shared/data": "content"})

add_scenario("find-19", "Find & Permissions", "Find and Print Formatted Output with -printf", "Advanced",
    "Find regular files in './logs' and print '%p: %s bytes\\n'.",
    'find ./logs -type f -printf "%p: %s bytes\\n"',
    ["Command: find ./logs -type f -printf \"%p: %s bytes\\n\""],
    'find ./logs -type f -printf "%p: %s bytes\\n"',
    [r'find\s+(\.\/)?logs\s+.*-printf\s+["\'].*%p.*%s'],
    setup_files={"logs/sys.log": "data"})

add_scenario("find-20", "Find & Permissions", "Find Files Matching Either of Two Names", "Intermediate",
    "Search './project' for files named either '*.c' or '*.h' using -o (OR).",
    "find ./project -name '*.c' -o -name '*.h'",
    ["Command: find ./project -name '*.c' -o -name '*.h'"],
    "find ./project -name '*.c' -o -name '*.h'",
    [r"find\s+(\.\/)?project\s+.*-name\s+['\"]?\*\.c['\"]\s+-o\s+-name\s+['\"]?\*\.h['\"]"],
    setup_files={"project/main.c": "1", "project/main.h": "2"})

# =========================================================================
# 7. PIPES, REDIRECTIONS & PROCESS FLOW - 25 Scenarios
# =========================================================================

add_scenario("pipe-01", "Pipes & Redirections", "Redirect stdout and stderr into audit.log", "Intermediate",
    "Execute './deploy_check.sh' redirecting BOTH stdout (fd 1) and stderr (fd 2) into audit.log.",
    "./deploy_check.sh > audit.log 2>&1",
    ["Command: ./deploy_check.sh > audit.log 2>&1"],
    "./deploy_check.sh > audit.log 2>&1",
    [r"\.\/deploy_check\.sh\s+>\s*audit\.log\s+2>&1", r"\.\/deploy_check\.sh\s+&>\s*audit\.log"],
    setup_files={"deploy_check.sh": "#!/bin/bash\necho out\necho err >&2\n"},
    setup_perms={"deploy_check.sh": 0o755})

add_scenario("pipe-02", "Pipes & Redirections", "Count Frequency and Sort Top 3", "Intermediate",
    "Extract column 1 (IP) from connections.log, count unique IPs, and sort top 3 descending.",
    "awk '{print $1}' connections.log | sort | uniq -c | sort -nr | head -n 3",
    ["Command: awk '{print $1}' connections.log | sort | uniq -c | sort -nr | head -n 3"],
    "awk '{print $1}' connections.log | sort | uniq -c | sort -nr | head -n 3",
    [r"(awk\s+['\"]\{print\s+\$1\}['\"]|cut\s+-d['\"]\s*['\"]\s+-f1)\s+connections\.log\s*\|\s*sort\s*\|\s*uniq\s+-c\s*\|\s*sort\s+(-nr|-rn|-n\s+-r|-r\s+-n)\s*\|\s*head\s+(-n\s*3|-3)"],
    setup_files={"connections.log": "10.0.0.1 a\n10.0.0.2 b\n10.0.0.1 c\n10.0.0.1 d\n10.0.0.2 e\n10.0.0.3 f\n"})

add_scenario("pipe-03", "Pipes & Redirections", "Tee Output to File While Filtering in Pipeline", "Intermediate",
    "Cat events.log, tee unfiltered output to backup_events.log, and filter stream with grep ERROR.",
    "cat events.log | tee backup_events.log | grep ERROR",
    ["Command: cat events.log | tee backup_events.log | grep ERROR"],
    "cat events.log | tee backup_events.log | grep ERROR",
    [r"cat\s+events\.log\s*\|\s*tee\s+backup_events\.log\s*\|\s*grep\s+ERROR"],
    setup_files={"events.log": "INFO 1\nERROR 2\nINFO 3\n"})

add_scenario("pipe-04", "Pipes & Redirections", "Sort Numerical Column in Reverse with Delimiter", "Intermediate",
    "Read disk_usage.txt. Sort by column 2 numerically in reverse order (-k2 -nr).",
    "sort -k2 -nr disk_usage.txt",
    ["Command: sort -k2 -nr disk_usage.txt"],
    "sort -k2 -nr disk_usage.txt",
    [r"sort\s+.*-k\s*2.*-nr\s+disk_usage\.txt", r"sort\s+.*-k\s*2\s+-n\s+-r\s+disk_usage\.txt"],
    setup_files={"disk_usage.txt": "/var 500\n/home 1000\n/tmp 100\n"})

add_scenario("pipe-05", "Pipes & Redirections", "Skip First Header Line Before Sorting", "Intermediate",
    "Read metrics.csv. Skip header with 'tail -n +2' and sort remaining by column 2 numerically.",
    "tail -n +2 metrics.csv | sort -t',' -k2 -n",
    ["Command: tail -n +2 metrics.csv | sort -t',' -k2 -n"],
    "tail -n +2 metrics.csv | sort -t',' -k2 -n",
    [r"tail\s+-n\s+\+2\s+metrics\.csv\s*\|\s*sort\s+.*-k\s*2"],
    setup_files={"metrics.csv": "server,load\nsrv1,90\nsrv2,20\nsrv3,50\n"})

add_scenario("pipe-06", "Pipes & Redirections", "Discard Error Output to /dev/null", "Easy",
    "Run 'find / -name secret.txt', redirecting all standard error to /dev/null.",
    "find / -name secret.txt 2>/dev/null",
    ["Command: find / -name secret.txt 2>/dev/null"],
    "find / -name secret.txt 2>/dev/null",
    [r"find\s+\/\s+-name\s+secret\.txt\s+2>\/dev\/null"])

add_scenario("pipe-07", "Pipes & Redirections", "Append Standard Output Without Overwriting", "Easy",
    "Append date timestamp to deploy.log without truncating existing content.",
    "date >> deploy.log",
    ["Use >> to append", "Command: date >> deploy.log"],
    "date >> deploy.log",
    [r"date\s+>>\s*deploy\.log"])

add_scenario("pipe-08", "Pipes & Redirections", "Pass Word List to Xargs Command", "Intermediate",
    "Cat packages.txt and pass package names to 'rpm -q' using xargs.",
    "cat packages.txt | xargs rpm -q",
    ["Command: cat packages.txt | xargs rpm -q"],
    "cat packages.txt | xargs rpm -q",
    [r"cat\s+packages\.txt\s*\|\s*xargs\s+rpm\s+-q"],
    setup_files={"packages.txt": "bash\ncoreutils\n"})

add_scenario("pipe-09", "Pipes & Redirections", "Cut Specific Delimited Fields", "Easy",
    "Extract columns 1 and 3 from comma-delimited users.csv using cut.",
    "cut -d',' -f1,3 users.csv",
    ["Command: cut -d',' -f1,3 users.csv"],
    "cut -d',' -f1,3 users.csv",
    [r"cut\s+-d['\"]?,['\"]?\s+-f1,3\s+users\.csv"],
    setup_files={"users.csv": "alice,pass1,admin\nbob,pass2,user\n"})

add_scenario("pipe-10", "Pipes & Redirections", "Translate Characters to Uppercase with tr", "Easy",
    "Cat input.txt and convert all lowercase letters to uppercase using tr '[:lower:]' '[:upper:]'.",
    "cat input.txt | tr '[:lower:]' '[:upper:]'",
    ["Command: cat input.txt | tr '[:lower:]' '[:upper:]'"],
    "cat input.txt | tr '[:lower:]' '[:upper:]'",
    [r"cat\s+input\.txt\s*\|\s*tr\s+.*'\[:lower:\]'.*'\[:upper:\]'"],
    setup_files={"input.txt": "hello world\n"})

add_scenario("pipe-11", "Pipes & Redirections", "Count Total Lines in Pipeline with wc -l", "Easy",
    "Count how many processes are listed by 'ps -ef' (piped into wc -l).",
    "ps -ef | wc -l",
    ["Command: ps -ef | wc -l"],
    "ps -ef | wc -l",
    [r"ps\s+(-ef|-aux|aux)\s*\|\s*wc\s+-l"])

add_scenario("pipe-12", "Pipes & Redirections", "Display Only Duplicate Lines with uniq -d", "Intermediate",
    "Read sorted list items.txt and output only the lines that appear more than once (uniq -d).",
    "uniq -d items.txt",
    ["Command: uniq -d items.txt"],
    "uniq -d items.txt",
    [r"uniq\s+-d\s+items\.txt"],
    setup_files={"items.txt": "a\nb\nb\nc\nd\nd\n"})

add_scenario("pipe-13", "Pipes & Redirections", "Display Only Unique Non-Repeated Lines with uniq -u", "Intermediate",
    "Read sorted list items.txt and output only lines that appear exactly once (uniq -u).",
    "uniq -u items.txt",
    ["Command: uniq -u items.txt"],
    "uniq -u items.txt",
    [r"uniq\s+-u\s+items\.txt"],
    setup_files={"items.txt": "a\nb\nb\nc\nd\nd\n"})

add_scenario("pipe-14", "Pipes & Redirections", "Combine stdout of Command into Variable with Command Substitution", "Easy",
    "Assign the current date string into variable CURRENT_DATE.",
    "CURRENT_DATE=$(date)",
    ["Command: CURRENT_DATE=$(date)"],
    "CURRENT_DATE=$(date)",
    [r"CURRENT_DATE=\$\(date\)"])

add_scenario("pipe-15", "Pipes & Redirections", "Append Output with Tee -a", "Intermediate",
    "Echo 'NEW_ENTRY' and append it to status.log while viewing it in console with tee -a.",
    "echo 'NEW_ENTRY' | tee -a status.log",
    ["Command: echo 'NEW_ENTRY' | tee -a status.log"],
    "echo 'NEW_ENTRY' | tee -a status.log",
    [r"echo\s+['\"]?NEW_ENTRY['\"]?\s*\|\s*tee\s+-a\s+status\.log"])

add_scenario("pipe-16", "Pipes & Redirections", "Paste Two Files Side by Side with Tab Separator", "Easy",
    "Merge lines of col1.txt and col2.txt side-by-side using paste.",
    "paste col1.txt col2.txt",
    ["Command: paste col1.txt col2.txt"],
    "paste col1.txt col2.txt",
    [r"paste\s+col1\.txt\s+col2\.txt"],
    setup_files={"col1.txt": "a\nb\n", "col2.txt": "1\n2\n"})

add_scenario("pipe-17", "Pipes & Redirections", "Filter Unique Lines Ignoring Case with uniq -i", "Intermediate",
    "Filter adjacent duplicate lines from case_items.txt ignoring case differences.",
    "uniq -i case_items.txt",
    ["Command: uniq -i case_items.txt"],
    "uniq -i case_items.txt",
    [r"uniq\s+-i\s+case_items\.txt"],
    setup_files={"case_items.txt": "apple\nApple\nbanana\n"})

add_scenario("pipe-18", "Pipes & Redirections", "Sort by IP Address Numerically with sort -V or sort -n", "Intermediate",
    "Sort ip_list.txt by natural version/numeric order.",
    "sort -V ip_list.txt",
    ["Command: sort -V ip_list.txt"],
    "sort -V ip_list.txt",
    [r"sort\s+-V\s+ip_list\.txt"],
    setup_files={"ip_list.txt": "10.0.0.10\n10.0.0.2\n10.0.0.1\n"})

add_scenario("pipe-19", "Pipes & Redirections", "Delete Specific Characters with tr -d", "Easy",
    "Strip all comma (,) characters from text.txt using tr -d.",
    "cat text.txt | tr -d ','",
    ["Command: cat text.txt | tr -d ','"],
    "cat text.txt | tr -d ','",
    [r"cat\s+text\.txt\s*\|\s*tr\s+-d\s+['\"],['\"]"],
    setup_files={"text.txt": "1,000,000\n"})

add_scenario("pipe-20", "Pipes & Redirections", "Execute Parallel Tasks with xargs -P", "Advanced",
    "Cat urls.txt and fetch headers in parallel using 4 workers with xargs -n 1 -P 4.",
    "cat urls.txt | xargs -n 1 -P 4 curl -sI",
    ["Command: cat urls.txt | xargs -n 1 -P 4 curl -sI"],
    "cat urls.txt | xargs -n 1 -P 4 curl -sI",
    [r"cat\s+urls\.txt\s*\|\s*xargs\s+.*-P\s*4\s+curl"],
    setup_files={"urls.txt": "http://localhost\nhttp://127.0.0.1\n"})

add_scenario("pipe-21", "Pipes & Redirections", "Sort Colon-Delimited File by Numeric Column 3", "Intermediate",
    "Sort /etc/passwd by UID (column 3) in numeric ascending order.",
    "sort -t':' -k3 -n /etc/passwd",
    ["Command: sort -t':' -k3 -n /etc/passwd"],
    "sort -t':' -k3 -n /etc/passwd",
    [r"sort\s+-t['\"]?:['\"]?\s+-k3\s+-n\s+\/etc\/passwd"])

add_scenario("pipe-22", "Pipes & Redirections", "Find Common Lines Between Two Sorted Files with comm", "Intermediate",
    "Compare sorted fileA.txt and fileB.txt and output only the lines common to both (comm -12).",
    "comm -12 fileA.txt fileB.txt",
    ["Command: comm -12 fileA.txt fileB.txt"],
    "comm -12 fileA.txt fileB.txt",
    [r"comm\s+-12\s+fileA\.txt\s+fileB\.txt"],
    setup_files={"fileA.txt": "a\nb\nc\n", "fileB.txt": "b\nc\nd\n"})

add_scenario("pipe-23", "Pipes & Redirections", "View Last 15 Lines of File with tail -n 15", "Easy",
    "Display the last 15 lines of /var/log/messages.",
    "tail -n 15 /var/log/messages",
    ["Command: tail -n 15 /var/log/messages"],
    "tail -n 15 /var/log/messages",
    [r"tail\s+(-n\s*15|-15)\s+\/var\/log\/messages"])

add_scenario("pipe-24", "Pipes & Redirections", "View First 8 Lines of File with head -n 8", "Easy",
    "Display the first 8 lines of /etc/hosts.",
    "head -n 8 /etc/hosts",
    ["Command: head -n 8 /etc/hosts"],
    "head -n 8 /etc/hosts",
    [r"head\s+(-n\s*8|-8)\s+\/etc\/hosts"])

add_scenario("pipe-25", "Pipes & Redirections", "Redirect Standard Input with Here-Doc", "Intermediate",
    "Use a bash here-doc (<<EOF) to pass multiple lines into cat and save to doc.txt.",
    "cat << 'EOF' > doc.txt\nline1\nline2\nEOF",
    ["Use cat << 'EOF' > doc.txt"],
    "cat << 'EOF' > doc.txt\nline1\nline2\nEOF",
    [r"cat\s+<<.*doc\.txt"])

# =========================================================================
# ADDITIONAL SCENARIOS TO REACH 230+ DRILLS (TRIPLING ORIGINAL QUESTION BANK)
# =========================================================================

# --- Find & Permissions (find-21 to find-25) ---
add_scenario("find-21", "Find & Permissions", "Find Large Files Over 100MB", "Intermediate",
    "Find all regular files in /var/log exceeding 100 Megabytes in size.",
    "find /var/log -type f -size +100M",
    ["Use -size +100M and -type f", "Command: find /var/log -type f -size +100M"],
    "find /var/log -type f -size +100M",
    [r"find\s+\/var\/log\s+.*-type\s+f.*-size\s+\+100M", r"find\s+\/var\/log\s+.*-size\s+\+100M.*-type\s+f"])

add_scenario("find-22", "Find & Permissions", "Set Sticky Bit on Shared Temporary Directory", "Intermediate",
    "Set the sticky bit on directory /shared/tmp (chmod +t or chmod 1777) so only file owners can delete their files.",
    "chmod +t /shared/tmp",
    ["Use chmod +t or chmod 1777", "Command: chmod +t /shared/tmp"],
    "chmod +t /shared/tmp",
    [r"chmod\s+(\+t|1[0-7]{3})\s+\/shared\/tmp"])

add_scenario("find-23", "Find & Permissions", "Set SGID on Directory for Group Collaboration", "Intermediate",
    "Set the SetGID (SGID) bit on /opt/project so all newly created files inherit the directory's owning group.",
    "chmod g+s /opt/project",
    ["Use chmod g+s or chmod 2775", "Command: chmod g+s /opt/project"],
    "chmod g+s /opt/project",
    [r"chmod\s+(g\+s|2[0-7]{3})\s+\/opt\/project"])

add_scenario("find-24", "Find & Permissions", "Locate Broken or Dead Symlinks", "Intermediate",
    "Find all broken symbolic links in /etc using find -xtype l.",
    "find /etc -xtype l",
    ["Use -xtype l to test target existence", "Command: find /etc -xtype l"],
    "find /etc -xtype l",
    [r"find\s+\/etc\s+-xtype\s+l"])

add_scenario("find-25", "Find & Permissions", "Find Files Modified in the Last 24 Hours", "Easy",
    "Find all files in /etc modified within the last 24 hours (-mtime -1).",
    "find /etc -mtime -1",
    ["Use -mtime -1", "Command: find /etc -mtime -1"],
    "find /etc -mtime -1",
    [r"find\s+\/etc\s+.*-mtime\s+-1"])

# --- Grep & Regex (grep-31 to grep-35) ---
add_scenario("grep-31", "Grep & Regex", "Match Lines Beginning with One or More Digits", "Easy",
    "Search 'data.txt' for all lines starting with one or more numerical digits.",
    "grep -E '^[0-9]+' data.txt",
    ["Use anchor ^ and [0-9]+ with -E", "Command: grep -E '^[0-9]+' data.txt"],
    "grep -E '^[0-9]+' data.txt",
    [r"grep\s+(-E|--extended-regexp)\s+['\"]?\^[0-9]\+['\"]?\s+data\.txt"],
    setup_files={"data.txt": "100 apples\nbanana\n200 oranges\n"})

add_scenario("grep-32", "Grep & Regex", "Recursive Grep Ignoring Binary Files", "Intermediate",
    "Recursively search /etc for 'DB_PASSWORD' while ignoring binary files using -r -I.",
    "grep -rI 'DB_PASSWORD' /etc",
    ["Use -r (recursive) and -I (ignore binaries)", "Command: grep -rI 'DB_PASSWORD' /etc"],
    "grep -rI 'DB_PASSWORD' /etc",
    [r"grep\s+(-rI|-Ir|-r\s+-I|-I\s+-r)\s+['\"]?DB_PASSWORD['\"]?\s+\/etc"])

add_scenario("grep-33", "Grep & Regex", "Extract All IPv4 Addresses from Log", "Intermediate",
    "Extract only valid IPv4 address strings from network.log using grep -oE.",
    "grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' network.log",
    ["Use -o for only-matching and -E for regex", "Command: grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' network.log"],
    "grep -oE '([0-9]{1,3}\\.){3}[0-9]{1,3}' network.log",
    [r"grep\s+(-oE|-Eo)\s+['\"].*([0-9].*){3}.*['\"]\s+network\.log"],
    setup_files={"network.log": "Connection from 192.168.1.50 port 22\nRefused 10.0.0.1 port 80\n"})

add_scenario("grep-34", "Grep & Regex", "Count Exact Number of Matches Across Log", "Easy",
    "Count the total number of lines in error.log containing 'FAIL' using grep -c.",
    "grep -c 'FAIL' error.log",
    ["Use grep -c 'FAIL' error.log", "Command: grep -c 'FAIL' error.log"],
    "grep -c 'FAIL' error.log",
    [r"grep\s+-c\s+['\"]?FAIL['\"]?\s+error\.log"],
    setup_files={"error.log": "FAIL: disk\nOK\nFAIL: memory\n"})

add_scenario("grep-35", "Grep & Regex", "Invert Search to Strip Comments and Blank Lines", "Intermediate",
    "Display /etc/chrony.conf excluding all comments (starting with #) and empty lines.",
    "grep -vE '^#|^$' /etc/chrony.conf",
    ["Use -vE with pattern '^#|^$'", "Command: grep -vE '^#|^$' /etc/chrony.conf"],
    "grep -vE '^#|^$' /etc/chrony.conf",
    [r"grep\s+(-vE|-Ev)\s+['\"]?\^#\|\^\$['\"]?\s+\/etc\/chrony\.conf"])

# --- Sed Stream Editing (sed-26 to sed-30) ---
add_scenario("sed-26", "Sed Stream Editing", "Replace Entire Line Matching Pattern with 'c\\'", "Intermediate",
    "In /etc/selinux/config, replace the entire line containing 'SELINUX=' with 'SELINUX=enforcing' using sed change command.",
    "sed -i '/^SELINUX=/c\\SELINUX=enforcing' /etc/selinux/config",
    ["Use /pattern/c\\replacement", "Command: sed -i '/^SELINUX=/c\\SELINUX=enforcing' /etc/selinux/config"],
    "sed -i '/^SELINUX=/c\\SELINUX=enforcing' /etc/selinux/config",
    [r"sed\s+.*-i.*\/(\^)?SELINUX=\/c.*SELINUX=enforcing.*\/etc\/selinux\/config"])

add_scenario("sed-27", "Sed Stream Editing", "Print Content Between START and END Markers", "Intermediate",
    "Print only the lines between /START/ and /END/ inclusive from build.log using sed -n.",
    "sed -n '/START/,/END/p' build.log",
    ["Use range /START/,/END/p with -n", "Command: sed -n '/START/,/END/p' build.log"],
    "sed -n '/START/,/END/p' build.log",
    [r"sed\s+-n\s+['\"]\/START\/,\/END\/p['\"]\s+build\.log"],
    setup_files={"build.log": "header\nSTART\nstep1\nstep2\nEND\nfooter\n"})

add_scenario("sed-28", "Sed Stream Editing", "Delete Blank and Whitespace-Only Lines", "Easy",
    "Remove all blank lines and lines containing only spaces or tabs from config.txt.",
    "sed '/^[[:space:]]*$/d' config.txt",
    ["Use pattern /^[[:space:]]*$/d", "Command: sed '/^[[:space:]]*$/d' config.txt"],
    "sed '/^[[:space:]]*$/d' config.txt",
    [r"sed\s+['\"]\/(\^\[\[:space:\]\]\*\$|\^\s\*\$)\/d['\"]\s+config\.txt"],
    setup_files={"config.txt": "item1\n   \nitem2\n\nitem3\n"})

add_scenario("sed-29", "Sed Stream Editing", "Case-Insensitive Global Substitution", "Easy",
    "Replace all occurrences of 'localhost' (any case: Localhost, LOCALHOST) with '127.0.0.1' using sed flag 'I'.",
    "sed 's/localhost/127.0.0.1/gI' hosts.txt",
    ["Use s/localhost/127.0.0.1/gI", "Command: sed 's/localhost/127.0.0.1/gI' hosts.txt"],
    "sed 's/localhost/127.0.0.1/gI' hosts.txt",
    [r"sed\s+['\"]s\/localhost\/127\.0\.0\.1\/(gI|Ig)['\"]\s+hosts\.txt"],
    setup_files={"hosts.txt": "LocalHost\nlocalhost\nLOCALHOST\n"})

add_scenario("sed-30", "Sed Stream Editing", "Append Line After Pattern Match with 'a\\'", "Intermediate",
    "Append a new line 'Include conf.modules.d/*.conf' after the line matching '# Load modules' in httpd.conf.",
    "sed '/# Load modules/a\\Include conf.modules.d/*.conf' httpd.conf",
    ["Use /pattern/a\\text", "Command: sed '/# Load modules/a\\Include conf.modules.d/*.conf' httpd.conf"],
    "sed '/# Load modules/a\\Include conf.modules.d/*.conf' httpd.conf",
    [r"sed\s+['\"]\/#\s*Load modules\/a.*Include.*conf['\"]\s+httpd\.conf"],
    setup_files={"httpd.conf": "# Load modules\nServerRoot /etc/httpd\n"})

# --- Awk Processing (awk-26 to awk-30) ---
add_scenario("awk-26", "Awk Processing", "Print Lines Where Field Count NF Greater Than 3", "Easy",
    "Print only lines from inventory.txt that have more than 3 whitespace-separated columns.",
    "awk 'NF > 3' inventory.txt",
    ["Condition: NF > 3", "Command: awk 'NF > 3' inventory.txt"],
    "awk 'NF > 3' inventory.txt",
    [r"awk\s+['\"]NF\s*>\s*3['\"]\s+inventory\.txt"],
    setup_files={"inventory.txt": "a b c\na b c d\na b\na b c d e\n"})

add_scenario("awk-27", "Awk Processing", "Prefix Every Line with Line Number (NR)", "Easy",
    "Print line numbers alongside each line from data.txt using awk '{print NR, $0}'.",
    "awk '{print NR, $0}' data.txt",
    ["Use NR and $0", "Command: awk '{print NR, $0}' data.txt"],
    "awk '{print NR, $0}' data.txt",
    [r"awk\s+['\"]\{\s*print\s+NR\s*,\s*\$0\s*\}['\"]\s+data\.txt"],
    setup_files={"data.txt": "first\nsecond\nthird\n"})

add_scenario("awk-28", "Awk Processing", "Calculate Column Average in END Block", "Intermediate",
    "Calculate the arithmetic average of numeric column 2 in scores.txt and print the result.",
    "awk '{sum += $2} END {print sum/NR}' scores.txt",
    ["Accumulate sum += $2 and in END print sum/NR", "Command: awk '{sum += $2} END {print sum/NR}' scores.txt"],
    "awk '{sum += $2} END {print sum/NR}' scores.txt",
    [r"awk\s+['\"]\{\s*sum\s*\+=\s*\$2\s*\}\s*END\s*\{\s*print\s+sum\s*\/\s*NR\s*\}['\"]\s+scores\.txt"],
    setup_files={"scores.txt": "Alice 90\nBob 80\nCharlie 100\n"})

add_scenario("awk-29", "Awk Processing", "Filter Lines Exceeding 80 Characters", "Easy",
    "Find and display all lines in source.c longer than 80 characters using awk 'length($0) > 80'.",
    "awk 'length($0) > 80' source.c",
    ["Use length($0) > 80", "Command: awk 'length($0) > 80' source.c"],
    "awk 'length($0) > 80' source.c",
    [r"awk\s+['\"]length(\(\$0\))?\s*>\s*80['\"]\s+source\.c"],
    setup_files={"source.c": "int main() { return 0; }\n/* " + ("a" * 85) + " */\n"})

add_scenario("awk-30", "Awk Processing", "Extract the Last Column Dynamically with $NF", "Easy",
    "Extract and print the final column of each line in logs.txt regardless of how many columns exist.",
    "awk '{print $NF}' logs.txt",
    ["Use $NF for the last column", "Command: awk '{print $NF}' logs.txt"],
    "awk '{print $NF}' logs.txt",
    [r"awk\s+['\"]\{\s*print\s+\$NF\s*\}['\"]\s+logs\.txt"],
    setup_files={"logs.txt": "2026-10-09 GET 200 /index.html\n2026-10-09 POST /login\n"})

# --- Pipes & Redirections (pipe-26 to pipe-30) ---
add_scenario("pipe-26", "Pipes & Redirections", "Merge Two Files Horizontally with paste -d", "Easy",
    "Combine names.txt and ages.txt side by side, delimited by a comma (paste -d',').",
    "paste -d',' names.txt ages.txt",
    ["Use paste -d',' names.txt ages.txt", "Command: paste -d',' names.txt ages.txt"],
    "paste -d',' names.txt ages.txt",
    [r"paste\s+-d['\"]?,['\"]?\s+names\.txt\s+ages\.txt"],
    setup_files={"names.txt": "Alice\nBob\n", "ages.txt": "30\n25\n"})

add_scenario("pipe-27", "Pipes & Redirections", "Join Files by Common Leading Field with join", "Intermediate",
    "Join sorted files id_names.txt and id_dept.txt on their shared first field (ID).",
    "join id_names.txt id_dept.txt",
    ["Use join id_names.txt id_dept.txt", "Command: join id_names.txt id_dept.txt"],
    "join id_names.txt id_dept.txt",
    [r"join\s+id_names\.txt\s+id_dept\.txt"],
    setup_files={"id_names.txt": "101 Alice\n102 Bob\n", "id_dept.txt": "101 Engineering\n102 Finance\n"})

add_scenario("pipe-28", "Pipes & Redirections", "Silence Both Output and Errors with &> /dev/null", "Easy",
    "Execute ping -c 1 8.8.8.8 and discard both standard output and standard error completely.",
    "ping -c 1 8.8.8.8 &> /dev/null",
    ["Redirect with &> /dev/null or > /dev/null 2>&1", "Command: ping -c 1 8.8.8.8 &> /dev/null"],
    "ping -c 1 8.8.8.8 &> /dev/null",
    [r"ping\s+-c\s*1\s+8\.8\.8\.8\s+(&>\s*\/dev\/null|>\s*\/dev\/null\s+2>&1)"])

add_scenario("pipe-29", "Pipes & Redirections", "Append String to File as Superuser with tee -a", "Intermediate",
    "Echo 'nameserver 1.1.1.1' and append it to /etc/resolv.conf using sudo tee -a.",
    "echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf",
    ["Pipe echo to tee -a /etc/resolv.conf", "Command: echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf"],
    "echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf",
    [r"echo\s+['\"]nameserver 1\.1\.1\.1['\"]\s*\|\s*(sudo\s+)?tee\s+-a\s+\/etc\/resolv\.conf"])

add_scenario("pipe-30", "Pipes & Redirections", "Safe Whitespace Pipe with find -print0 | xargs -0", "Advanced",
    "Safely delete all .tmp files in /var/tmp even if names contain spaces or newlines using find -print0 and xargs -0 rm -f.",
    "find /var/tmp -type f -name '*.tmp' -print0 | xargs -0 rm -f",
    ["Use find -print0 | xargs -0 rm -f", "Command: find /var/tmp -type f -name '*.tmp' -print0 | xargs -0 rm -f"],
    "find /var/tmp -type f -name '*.tmp' -print0 | xargs -0 rm -f",
    [r"find\s+\/var\/tmp\s+.*-print0\s*\|\s*xargs\s+-0\s+rm\s+-f"])

print(f"Total Scenarios Generated: {len(scenarios)}")

# Write to library files
os.makedirs("./library", exist_ok=True)
os.makedirs("./public/library", exist_ok=True)

with open("./library/all_scenarios.json", "w", encoding="utf-8") as f:
    json.dump(scenarios, f, indent=2)

with open("./public/all_scenarios.json", "w", encoding="utf-8") as f:
    json.dump(scenarios, f, indent=2)

# Generate category packs
cats = {
    "service_management.json": [s for s in scenarios if s['category'] == 'Service Management'],
    "firewall_network.json": [s for s in scenarios if s['category'] == 'Firewall & Network'],
    "grep_regex.json": [s for s in scenarios if s['category'] == 'Grep & Regex'],
    "sed_stream.json": [s for s in scenarios if s['category'] == 'Sed Stream Editing'],
    "awk_processing.json": [s for s in scenarios if s['category'] == 'Awk Processing'],
    "find_permissions.json": [s for s in scenarios if s['category'] == 'Find & Permissions'],
    "pipes_redirections.json": [s for s in scenarios if s['category'] == 'Pipes & Redirections'],
    "rhcsa_exam_pack.json": scenarios
}

for name, dat in cats.items():
    with open(f"./library/{name}", "w", encoding="utf-8") as f:
        json.dump(dat, f, indent=2)
    with open(f"./public/library/{name}", "w", encoding="utf-8") as f:
        json.dump(dat, f, indent=2)

print("All JSON libraries written successfully.")
