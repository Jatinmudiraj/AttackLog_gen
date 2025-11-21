import re
import os


# ------------------------------
# TIMESTAMP PATTERNS
# ------------------------------

SYSLOG_REGEX = re.compile(
    r"^[A-Z][a-z]{2}\s+\d{1,2}\s+\d\d:\d\d:\d\d\s+[\w\-\_\.]+"
)

APACHE_REGEX = re.compile(
    r'^\d+\.\d+\.\d+\.\d+\s+-\s+-\s+\[\d{2}/[A-Za-z]{3}/\d{4}'
)


# ------------------------------
# GENERIC CLEANING HELPERS
# ------------------------------

def remove_ansi(text: str) -> str:
    """Remove terminal color escapes."""
    return re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", text)


def strip_explanations(line: str) -> str:
    """Remove model-generated English explanations."""
    bad = [
        "note:", "explanation:", "example:", 
        "as requested", "these are logs", "generated",
        "here is", "this means", "clarification", 
        "summary:", "output:", "line-by-line"
    ]
    lower = line.lower()
    return "" if any(b in lower for b in bad) else line


def normalize_spaces(line: str) -> str:
    """Remove duplicate spaces."""
    return re.sub(r"\s+", " ", line).strip()


def is_valid_syslog(line: str) -> bool:
    return bool(SYSLOG_REGEX.match(line))


def is_valid_apache(line: str) -> bool:
    return bool(APACHE_REGEX.match(line))


# ------------------------------
# CLEANER MODES
# ------------------------------

def clean_sshd_line(line: str) -> str:
    """Keep only valid SSH/syslog events."""

    if not is_valid_syslog(line):
        return ""

    allowed = [
        "sshd", "sudo", "CRON", "session", "Failed password",
        "Invalid user", "Accepted password", "pam_unix",
        "systemd", "login"
    ]

    if any(k in line for k in allowed):
        return line

    return ""


def clean_apache_line(line: str) -> str:
    """Keep only valid Apache logs."""
    if is_valid_apache(line):
        return line
    return ""


def clean_generic_line(line: str) -> str:
    """Generic cleaner: keep valid syslog or apache."""
    if is_valid_syslog(line) or is_valid_apache(line):
        return line
    return ""


# ------------------------------
# MAIN CLEANING FUNCTION
# ------------------------------

def clean_log_file(input_path: str, output_path: str, mode: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input not found: {input_path}")

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    cleaned = []

    for line in lines:
        if not line.strip():
            continue

        # Strip junk
        line = remove_ansi(line)
        line = strip_explanations(line)
        line = normalize_spaces(line)

        if not line:
            continue

        # Mode-specific cleaning
        if mode == "sshd":
            line = clean_sshd_line(line)
        elif mode == "apache":
            line = clean_apache_line(line)
        else:  # generic
            line = clean_generic_line(line)

        if line:
            cleaned.append(line)

    # Remove duplicates
    cleaned = list(dict.fromkeys(cleaned))

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

    # Return preview
    return cleaned[:500]
