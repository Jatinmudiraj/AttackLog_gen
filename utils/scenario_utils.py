# utils/scenario_utils.py

"""
AttackLogGen canonical scenarios for visualization.

Each scenario:
  - id: short stable id
  - name: human-readable title
  - description: short story
  - nodes: list of hostnames involved
  - edges: list of directed edges {src, dst, label}
  - mitre: list of technique IDs involved
  - phases: list of high-level steps for text view
"""

SCENARIOS = [
    {
        "id": "SCENARIO_1",
        "name": "Web SQLi → Webshell → Lateral SSH → Mail Exfil",
        "description": (
            "Attacker exploits DVWA on WEB via SQL injection, "
            "drops webshell, pivots via SSH into internal Ubuntu hosts, "
            "and finally exfiltrates data via MAIL server."
        ),
        "nodes": ["KALI", "WEB", "UBT5", "UBT4", "MAIL"],
        "edges": [
            {"src": "KALI", "dst": "WEB", "label": "SQLi on DVWA (login.php)"},
            {"src": "WEB", "dst": "WEB", "label": "Webshell upload & execution"},
            {"src": "WEB", "dst": "UBT5", "label": "SSH pivot (stolen creds)"},
            {"src": "UBT5", "dst": "UBT4", "label": "Lateral SSH movement"},
            {"src": "UBT4", "dst": "MAIL", "label": "Data exfil via SMTP/IMAP"},
        ],
        "mitre": ["T1190", "T1059", "T1021", "T1078", "T1041"],
        "phases": [
            "Recon and SQL injection against WEB (DVWA)",
            "Webshell deployment on WEB",
            "SSH pivot to UBT5",
            "Lateral movement from UBT5 to UBT4",
            "Exfiltration through MAIL server",
        ],
    },
    {
        "id": "SCENARIO_2",
        "name": "SSH Brute Force → Pivot to Audit Host",
        "description": (
            "Attacker brute-forces SSH on UB2 from KALI, "
            "then pivots from UB2 to UB3 where auditd is enabled, "
            "and probes other internal nodes."
        ),
        "nodes": ["KALI", "UB2", "UB3", "UBT4", "UBT5"],
        "edges": [
            {"src": "KALI", "dst": "UB2", "label": "SSH brute force (password spray)"},
            {"src": "UB2", "dst": "UB3", "label": "SSH pivot to auditd host"},
            {"src": "UB3", "dst": "UBT5", "label": "Probing further internal hosts"},
            {"src": "UB3", "dst": "UBT4", "label": "SSH attempts & scans"},
        ],
        "mitre": ["T1110", "T1021", "T1078", "T1083"],
        "phases": [
            "SSH brute-force attempts from KALI to UB2",
            "Successful SSH login and pivot to UB3",
            "Auditd captures execve bursts on UB3",
            "Probing attempts from UB3 to UBT5 / UBT4",
        ],
    },
    {
        "id": "SCENARIO_3",
        "name": "Phishing → User Click → Web Reset → UB1 Access",
        "description": (
            "User on UBT4 receives phishing mail, clicks link, "
            "which triggers DVWA password reset / login burst on WEB, "
            "and eventually attacker gains access to UB1."
        ),
        "nodes": ["KALI", "MAIL", "UBT4", "WEB", "UB1"],
        "edges": [
            {"src": "KALI", "dst": "MAIL", "label": "Send phishing email"},
            {"src": "MAIL", "dst": "UBT4", "label": "User receives and clicks link"},
            {"src": "UBT4", "dst": "WEB", "label": "DVWA reset & login burst"},
            {"src": "WEB", "dst": "UB1", "label": "SSH or app-layer access to UB1"},
        ],
        "mitre": ["T1566", "T1204", "T1190", "T1078"],
        "phases": [
            "Phishing email delivery to UBT4",
            "User click and browser-based execution",
            "DVWA password reset and login storm",
            "Follow-up access from WEB to UB1",
        ],
    },
    {
        "id": "SCENARIO_4",
        "name": "Dev Supply-Chain → Rsync → Web Deploy",
        "description": (
            "Developer on UBT5 pulls code, rsyncs to UBT4, "
            "and then deploys to WEB, optionally with hidden "
            "malicious endpoints being introduced."
        ),
        "nodes": ["UBT5", "UBT4", "WEB"],
        "edges": [
            {"src": "UBT5", "dst": "UBT5", "label": "Fetch artifacts (git/wget/curl)"},
            {"src": "UBT5", "dst": "UBT4", "label": "Rsync project to staging"},
            {"src": "UBT4", "dst": "WEB", "label": "Deploy to production (WEB)"},
        ],
        "mitre": ["T1195", "T1036", "T1071"],
        "phases": [
            "Developer retrieves or updates code on UBT5",
            "Rsync or scp transfer from UBT5 to UBT4",
            "Deployment from UBT4 to WEB (DVWA/Apache)",
        ],
    },
    {
        "id": "SCENARIO_5",
        "name": "Rogue Toolkit on META: Scans + SSH Spray + Web Probes",
        "description": (
            "Rogue toolkit runs on META host, performing light network scans, "
            "multi-host SSH credential spraying, and automated WEB exploit probes."
        ),
        "nodes": ["META", "KALI", "WEB", "UB1", "UB2", "UB3"],
        "edges": [
            {"src": "META", "dst": "KALI", "label": "Light scan / beaconing"},
            {"src": "META", "dst": "UB1", "label": "SSH credential spray"},
            {"src": "META", "dst": "UB2", "label": "SSH credential spray"},
            {"src": "META", "dst": "UB3", "label": "SSH credential spray"},
            {"src": "META", "dst": "WEB", "label": "sqlmap-style exploit probes"},
        ],
        "mitre": ["T1046", "T1110", "T1190"],
        "phases": [
            "Network scanning from META",
            "SSH credential spraying to multiple Ubuntu hosts",
            "HTTP exploit attempts (sqlmap UA) against WEB",
        ],
    },
    {
        "id": "SCENARIO_6",
        "name": "UB3 Log Tampering + Crypto-like File Burst → MAIL Touch",
        "description": (
            "Attacker on UB3 attempts to tamper with logs, "
            "creates crypto-ransomware-like file bursts, "
            "and touches MAIL services as part of exfiltration or signaling."
        ),
        "nodes": ["UB3", "MAIL"],
        "edges": [
            {"src": "UB3", "dst": "UB3", "label": "Log tampering attempts (rm, sed, echo)"},
            {"src": "UB3", "dst": "UB3", "label": "Mass file operations (encrypt-like)"},
            {"src": "UB3", "dst": "MAIL", "label": "MAIL touch / exfil / notification"},
        ],
        "mitre": ["T1070", "T1486", "T1041"],
        "phases": [
            "Log file modification and cleaning on UB3",
            "High-volume file writes/renames (crypto-like)",
            "Interactions with MAIL (exfil or signaling)",
        ],
    },
]


def load_scenarios():
    """
    Return scenarios as a list of dicts.
    Used by /api/load_scenarios.
    """
    return SCENARIOS
