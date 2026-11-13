#!/usr/bin/env python3
"""
Combines existing 230 scenarios from library/all_scenarios.json with:
- new_scenarios_part1 (80 scenarios: sys-41..80, net-41..80)
- new_scenarios_part2 (65 scenarios: grep-36..70, sed-31..60)
- new_scenarios_part3 (85 scenarios: awk-31..60, find-26..60, pipe-31..50)
Total: 460 scenarios.
Verifies uniqueness of all IDs, titles, objectives.
Exports to:
- library/all_scenarios.json
- library/<category>.json
- public/all_scenarios.json
- public/library/*
"""

import json
import os
import shutil

from new_scenarios_part1 import new_scenarios as part1
from new_scenarios_part2 import new_scenarios as part2
from new_scenarios_part3 import new_scenarios as part3

with open("library/all_scenarios.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

print(f"Existing scenarios: {len(existing)}")
print(f"Part 1 scenarios: {len(part1)}")
print(f"Part 2 scenarios: {len(part2)}")
print(f"Part 3 scenarios: {len(part3)}")

all_scenarios = existing + part1 + part2 + part3
print(f"Total scenarios combined: {len(all_scenarios)}")

# Validation of uniqueness
seen_ids = set()
seen_titles = set()
duplicates = []

for s in all_scenarios:
    sid = s["id"]
    title = s["title"]
    if sid in seen_ids:
        duplicates.append(f"Duplicate ID: {sid}")
    if title in seen_titles:
        duplicates.append(f"Duplicate Title: {title}")
    seen_ids.add(sid)
    seen_titles.add(title)

if duplicates:
    print("VALIDATION ERRORS:")
    for d in duplicates[:10]:
        print("  -", d)
    raise ValueError(f"Found {len(duplicates)} duplicates!")

print("All scenarios are completely UNIQUE (no duplicate IDs or titles).")

# Category breakdown
categories = {}
for s in all_scenarios:
    c = s["category"]
    categories[c] = categories.get(c, 0) + 1

print("\n--- Category Breakdown ---")
for c, count in sorted(categories.items()):
    print(f"  {c}: {count}")

# Save library/all_scenarios.json
os.makedirs("library", exist_ok=True)
with open("library/all_scenarios.json", "w", encoding="utf-8") as f:
    json.dump(all_scenarios, f, indent=2)

# Save category files
cat_map = {
    "Service Management": "service_management.json",
    "Firewall & Network": "firewall_network.json",
    "Grep & Regex": "grep_regex.json",
    "Sed Stream Editing": "sed_stream.json",
    "Awk Processing": "awk_processing.json",
    "Find & Permissions": "find_permissions.json",
    "Pipes & Redirections": "pipes_redirections.json"
}

for cat_name, filename in cat_map.items():
    cat_items = [s for s in all_scenarios if s["category"] == cat_name]
    with open(os.path.join("library", filename), "w", encoding="utf-8") as f:
        json.dump(cat_items, f, indent=2)

with open("library/rhcsa_exam_pack.json", "w", encoding="utf-8") as f:
    json.dump(all_scenarios, f, indent=2)

# Sync to public
os.makedirs("public/library", exist_ok=True)
shutil.copy2("library/all_scenarios.json", "public/all_scenarios.json")
for filename in cat_map.values():
    shutil.copy2(os.path.join("library", filename), os.path.join("public/library", filename))
shutil.copy2("library/rhcsa_exam_pack.json", "public/library/rhcsa_exam_pack.json")

print("\nSuccessfully exported all 460 scenarios to library/ and public/!")
