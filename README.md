# shell-drill: RHEL 9/10 Terminal Muscle-Memory Trainer

An interactive RHEL 9 & 10 terminal muscle-memory trainer available as both a sandboxed web workbench and a zero-dependency Python curses CLI executable.
Master sysadmin tools (`systemctl`, `journalctl`, `firewall-cmd`, `nmcli`, `semanage`, `grep`, `sed`, `awk`, `find`, `setfacl`, pipes, process substitution) across 460 hands-on drills.

---

## Web Workbench

Run the full-stack web trainer (`server.ts` + React frontend):

```bash
npm install
npm run dev
```

Or build and run in production:

```bash
npm run build
npm start
```

---

## Standalone RHEL 9/10 CLI Usage

`shell-drill` requires only **Python 3.6+** and the native `curses` library included with default RHEL 9/10 installations.

```bash
# Run directly:
./shell-drill

# Or as a python script:
python3 shell_drill.py
```

### CLI Session Options

```bash
# Start standard interactive trainer:
./shell-drill

# Set exact number of questions for this session:
./shell-drill --count 10
./shell-drill -n 25

# Filter by category:
./shell-drill --category "Firewall & Network"
./shell-drill --category "Service Management"
./shell-drill -n 15 --category "Awk Processing"

# List all 460 scenarios:
./shell-drill --list

# Export or load scenario libraries:
./shell-drill --export-library scenarios.json
./shell-drill --library scenarios.json
```

---

## Curriculum (460 Scenarios)

- **Service Management (80)**: `enable --now`, `systemd-analyze`, drop-ins, unit masking, cgroups, timer units.
- **Firewall & Network (80)**: `firewall-cmd --permanent`, rich rules, zone dispatch, `ss -tlpn`, `nmcli` bonding/profiles, `semanage`.
- **Grep & Regex (70)**: `-E`, `-v`, word boundaries `\< \>`, regex extraction `-o`, context flags `-B/-A/-C`.
- **Sed Stream Editing (60)**: In-place edits `-i`, substitution delimiters, line ranges, branch deletion, append/insert.
- **Awk Processing (60)**: Custom `-F`, associative frequency arrays, column arithmetic, `OFS`, `gsub`, multi-file summaries.
- **Find & Permissions (60)**: `-size`, `-perm`, POSIX ACLs (`getfacl`/`setfacl`), immutable attributes (`chattr +i`), `-exec +`.
- **Pipes & Redirections (50)**: `2>&1`, `&>`, process substitution `<()`, `tee -a`, `xargs -0`, `paste`, `comm`.
