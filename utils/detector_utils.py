def detect_mitre(lines, mitre_rules):
    output = []

    for idx, line in enumerate(lines, start=1):
        l = line.strip()
        if not l:
            continue

        for tech_id, entry in mitre_rules.items():
            keywords = entry.get("keywords", [])
            name = entry.get("name", "")
            desc = entry.get("description", "")

            if any(k.lower() in l.lower() for k in keywords):
                output.append({
                    "line": idx,
                    "log": l,
                    "tech_id": tech_id,
                    "name": name or "Technique",
                    "description": desc
                })

    return output
