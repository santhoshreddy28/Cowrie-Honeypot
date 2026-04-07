# scripts/analyze_logs.py

import json
import os
from collections import Counter
from datetime import datetime

LOG_PATH = "../logs/raw/"
REPORT_PATH = "../reports/"


def load_logs(log_dir):
    events = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".json"):
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    try:
                        events.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
    return events


def analyze(events):
    ips = Counter()
    commands = Counter()
    usernames = Counter()
    passwords = Counter()
    sessions = set()

    for e in events:
        etype = e.get("eventid", "")
        src_ip = e.get("src_ip", "unknown")

        # 🔐 Count login attempts
        if "login" in etype:
            ips[src_ip] += 1
            usernames[e.get("username", "")] += 1

            pwd = e.get("password", "")
            if pwd and "fishy" not in pwd.lower():  # filter sensitive password
                passwords[pwd] += 1

        # 💻 Count executed commands (cleaned)
        if "command" in etype:
            cmd = e.get("input", "").strip()

            if (
                cmd
                and not cmd.startswith("#")          # ignore comments
                and "cowrie" not in cmd              # ignore your setup cmds
                and "activate" not in cmd
            ):
                commands[cmd] += 1

        # 📌 Track sessions
        sessions.add(e.get("session", ""))

    return {
        "total_events": len(events),
        "unique_sessions": len(sessions),
        "top_attacker_ips": ips.most_common(10),
        "top_usernames": usernames.most_common(10),
        "top_passwords": passwords.most_common(10),
        "top_commands": commands.most_common(10),
    }


def save_report(report):
    os.makedirs(REPORT_PATH, exist_ok=True)
    filename = REPORT_PATH + f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Report saved to {filename}")
    return filename


def print_report(report):
    print("\n===== COWRIE HONEYPOT ANALYSIS REPORT =====")
    print(f"Total Events     : {report['total_events']}")
    print(f"Unique Sessions  : {report['unique_sessions']}")

    print("\n[+] Top Attacker IPs:")
    for ip, count in report["top_attacker_ips"]:
        print(f"    {ip:<20} {count} attempts")

    print("\n[+] Top Usernames Tried:")
    for u, c in report["top_usernames"]:
        print(f"    {u:<20} {c}")

    print("\n[+] Top Passwords Tried:")
    for p, c in report["top_passwords"]:
        print(f"    {p:<20} {c}")

    print("\n[+] Top Commands Executed:")
    for cmd, c in report["top_commands"]:
        print(f"    {str(cmd)[:50]:<52} {c}")


if __name__ == "__main__":
    print("[*] Loading Cowrie JSON logs...")
    events = load_logs(LOG_PATH)

    print(f"[*] Loaded {len(events)} events.")

    if len(events) == 0:
        print("[!] No logs found. Generate traffic first!")
        exit()

    report = analyze(events)

    print_report(report)
    save_report(report)
