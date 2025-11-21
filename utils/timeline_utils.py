def compute_timeline(lines):
    events = []
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        events.append({"id": i, "text": line.strip()})
    return events
