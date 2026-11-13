export interface CheatSheetItem {
  command: string;
  summary: string;
}

export const CATEGORY_LIST = [
  'Service Management',
  'Firewall & Network',
  'Grep & Regex',
  'Sed Stream Editing',
  'Awk Processing',
  'Find & Permissions',
  'Pipes & Redirections',
] as const;

export const CHEAT_SHEETS: Record<string, CheatSheetItem[]> = {
  'Service Management': [
    { command: 'systemctl enable --now <unit>', summary: 'Enable at boot and start immediately' },
    { command: 'systemctl disable --now <unit>', summary: 'Stop immediately and disable at boot' },
    { command: 'systemctl mask <unit>', summary: 'Link unit to /dev/null to prevent manual or dependency start' },
    { command: 'systemctl edit <unit>', summary: 'Create a drop-in override snippet under /etc/systemd/system/' },
    { command: 'systemctl list-dependencies <unit>', summary: 'Show unit dependency tree' },
    { command: 'journalctl -u <unit> --since "1 hour ago"', summary: 'Inspect unit logs within time window' },
    { command: 'systemd-analyze blame', summary: 'Rank units by boot initialization duration' },
    { command: 'systemctl set-default multi-user.target', summary: 'Switch default boot target to non-graphical' },
  ],
  'Firewall & Network': [
    { command: 'firewall-cmd --permanent --zone=public --add-service=https', summary: 'Persist service rule in public zone' },
    { command: 'firewall-cmd --permanent --add-port=8080/tcp', summary: 'Open TCP port 8080 permanently' },
    { command: 'firewall-cmd --reload', summary: 'Apply permanent rules to runtime configuration' },
    { command: 'firewall-cmd --permanent --add-rich-rule=\'...\'', summary: 'Add granular source/action rich rule' },
    { command: 'nmcli connection modify <con> ipv4.addresses 10.0.0.5/24', summary: 'Set static IPv4 CIDR on connection' },
    { command: 'nmcli connection up <con>', summary: 'Activate modified NetworkManager profile' },
    { command: 'ss -tlpn', summary: 'List listening TCP sockets with process PIDs' },
    { command: 'semanage port -a -t http_port_t -p tcp 8081', summary: 'Label custom port for SELinux httpd context' },
  ],
  'Grep & Regex': [
    { command: 'grep -n "pattern" file', summary: 'Print matching lines prefixed with line numbers' },
    { command: 'grep -E "err|warn" file', summary: 'Extended regex alternation without backslash escaping' },
    { command: 'grep -v "^#" file', summary: 'Invert match to exclude commented lines' },
    { command: 'grep -oE "[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+" file', summary: 'Print only matched substring tokens' },
    { command: 'grep -rn --exclude-dir=.git "TODO" .', summary: 'Recursive search skipping specified directory' },
    { command: 'grep -B 2 -A 3 "FATAL" app.log', summary: 'Include 2 lines before and 3 lines after match' },
    { command: 'grep -w "root" /etc/passwd', summary: 'Match whole words bounded by non-word chars' },
    { command: 'grep -c "ERROR" app.log', summary: 'Count total matching lines' },
  ],
  'Sed Stream Editing': [
    { command: "sed 's/old/new/g' file", summary: 'Substitute all occurrences per line' },
    { command: "sed -i.bak 's/old/new/g' file", summary: 'Edit file in place while preserving .bak backup' },
    { command: "sed -n '10,20p' file", summary: 'Suppress auto-print and print lines 10 through 20' },
    { command: "sed '/^#/d;/^$/d' file", summary: 'Delete comment and blank lines' },
    { command: "sed 's|/var/www|/srv/www|g' file", summary: 'Use alternate delimiter when paths contain slashes' },
    { command: "sed -E 's/([a-z]+)/\\U\\1/' file", summary: 'Extended capture group with uppercase transform' },
    { command: "sed '/pattern/a\\new_line' file", summary: 'Append a line immediately after matching pattern' },
    { command: "sed '1i\\# Header' file", summary: 'Insert text before line 1' },
  ],
  'Awk Processing': [
    { command: "awk -F':' '$7 == \"/bin/bash\" {print $1\":\"$3}' file", summary: 'Split fields by colon and filter on column 7' },
    { command: "awk '{sum += $3} END {print sum}' file", summary: 'Accumulate column values and print total in END' },
    { command: "awk '{counts[$1]++} END {for (k in counts) print k, counts[k]}' file", summary: 'Frequency count using associative array' },
    { command: "awk 'BEGIN {OFS=\",\"} {print $1, $2}' file", summary: 'Set output field separator to comma' },
    { command: "awk 'NR>=5 && NR<=10' file", summary: 'Filter records by line number range' },
    { command: "awk '{gsub(/foo/, \"bar\", $2); print}' file", summary: 'Global regex replacement inside column 2' },
    { command: "awk 'length($0) > 80' file", summary: 'Print lines exceeding 80 characters' },
    { command: "awk '!seen[$0]++' file", summary: 'Deduplicate lines while preserving first-seen order' },
  ],
  'Find & Permissions': [
    { command: 'find ./dir -type f -perm 0777', summary: 'Find files with exact 0777 permissions' },
    { command: 'find ./dir -type f -perm -4000', summary: 'Find files with at least SUID bit set' },
    { command: 'find ./dir -type f -size +10M', summary: 'Locate files strictly larger than 10 MiB' },
    { command: 'find ./dir -mtime -7 -name "*.log"', summary: 'Log files modified within the last 7 days' },
    { command: 'find ./dir -type f -exec chmod 0644 {} +', summary: 'Batch execute chmod across matched files' },
    { command: 'setfacl -m u:alice:rw file', summary: 'Grant POSIX ACL read/write access to user alice' },
    { command: 'getfacl file', summary: 'Display standard permissions and extended ACL entries' },
    { command: 'chmod u+s,g+s binary', summary: 'Set SUID and SGID bits symbolically' },
  ],
  'Pipes & Redirections': [
    { command: './script.sh > out.log 2>&1', summary: 'Redirect stdout to file, then route stderr to same descriptor' },
    { command: './script.sh &> out.log', summary: 'Bash shorthand capturing both stdout and stderr' },
    { command: 'cmd 2>/dev/null', summary: 'Discard standard error output' },
    { command: 'cmd | tee -a output.log', summary: 'Display stdout on screen and append to log file' },
    { command: 'diff <(sort a.txt) <(sort b.txt)', summary: 'Compare sorted outputs via process substitution' },
    { command: "find . -name '*.tmp' -print0 | xargs -0 rm -f", summary: 'Null-delimited safe handling of spaces in filenames' },
    { command: 'sort file | uniq -c | sort -rn', summary: 'Count unique lines sorted by descending frequency' },
    { command: 'cat urls.txt | xargs -n 1 -P 4 curl -sI', summary: 'Run up to 4 parallel workers via xargs -P' },
  ],
};
