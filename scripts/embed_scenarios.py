#!/usr/bin/env python3
import json
import os
import shutil

with open("library/all_scenarios.json", "r", encoding="utf-8") as f:
    scenarios = json.load(f)

print(f"Loaded {len(scenarios)} scenarios from library/all_scenarios.json")

with open("shell_drill.py", "r", encoding="utf-8") as f:
    content = f.read()

# Locate BUILTIN_SCENARIOS = json.loads(r'''[ or BUILTIN_SCENARIOS = [
start_idx = content.find("BUILTIN_SCENARIOS =")
if start_idx == -1:
    raise ValueError("BUILTIN_SCENARIOS not found")

end_marker = "SCENARIOS = list(BUILTIN_SCENARIOS)"
end_idx = content.find(end_marker)
if end_idx == -1:
    raise ValueError("SCENARIOS = list(BUILTIN_SCENARIOS) marker not found")

# Replace BUILTIN_SCENARIOS with json.loads of the full dataset
scenarios_json_repr = json.dumps(scenarios, indent=2)

new_builtin_block = f"""# Embedded comprehensive scenario bank ({len(scenarios)} drills)
BUILTIN_SCENARIOS = json.loads(r'''{scenarios_json_repr}''')

"""

new_content = content[:start_idx] + new_builtin_block + content[end_idx:]

with open("shell_drill.py", "w", encoding="utf-8") as f:
    f.write(new_content)

with open("shell-drill", "w", encoding="utf-8") as f:
    f.write(new_content)

os.makedirs("public", exist_ok=True)
shutil.copy2("shell_drill.py", "public/shell_drill.py")
shutil.copy2("shell-drill", "public/shell-drill")

print(f"Successfully updated shell_drill.py and shell-drill with {len(scenarios)} embedded scenarios!")
