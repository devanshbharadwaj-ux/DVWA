#!/usr/bin/env python3
import json
import sys
import os

f = sys.argv[1]
out = os.path.join("results", "converted_" + os.path.basename(f).replace(".sarif", ".json"))

with open(f) as sarif_file:
    sarif = json.load(sarif_file)

eslint_results = []
for run in sarif.get("runs", []):
    for result in run.get("results", []):
        rule_id = result.get("ruleId", "UNKNOWN")
        message = result.get("message", {}).get("text", "")
        locations = result.get("locations", [])
        file_path = locations[0]["physicalLocation"]["artifactLocation"]["uri"] if locations else "unknown"
        start_line = locations[0]["physicalLocation"]["region"].get("startLine", 1) if locations else 1
        eslint_results.append({
            "ruleId": rule_id,
            "severity": "error",
            "message": message,
            "filePath": file_path,
            "line": start_line
        })

with open(out, "w") as out_file:
    json.dump(eslint_results, out_file, indent=2)

print(f"Converted {f} -> {out}")
