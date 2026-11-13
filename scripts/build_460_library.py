#!/usr/bin/env python3
"""
Generator script to double the question bank to 460 unique, non-identical scenarios.
Covers real-world RHEL 9/10 administration:
- Service Management & systemd (80 scenarios)
- Firewall, Networking & SELinux (80 scenarios)
- Grep & Regular Expressions (70 scenarios)
- Sed Stream Editing (60 scenarios)
- Awk Text Processing & Reporting (60 scenarios)
- Find, Permissions, ACLs & Attributes (60 scenarios)
- Pipes, Redirection & Process Substitution (50 scenarios)
Total: 460 scenarios
"""

import json
import os
import re

scenarios = []
seen_titles = set()
seen_ids = set()

def add_scenario(id, cat, title, diff, desc, obj, hints, sol, regexes, setup_files=None, setup_perms=None, verify_cmd=None):
    if id in seen_ids:
        raise ValueError(f"Duplicate id: {id}")
    if title in seen_titles:
        raise ValueError(f"Duplicate title: {title}")
    seen_ids.add(id)
    seen_titles.add(title)
    
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

# Load the initial 230 scenarios from library/all_scenarios.json
with open("library/all_scenarios.json", "r", encoding="utf-8") as f:
    existing_scenarios = json.load(f)

for s in existing_scenarios:
    add_scenario(
        s["id"], s["category"], s["title"], s["difficulty"],
        s["description"], s["objective"], s["hints"], s["solution"],
        s["accepted_regex"], s.get("setup_files", {}), s.get("setup_perms", {}),
        s.get("verify_cmd", "")
    )

print(f"Loaded existing {len(scenarios)} scenarios.")
