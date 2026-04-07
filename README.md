# 🍯 Cowrie SSH Honeypot Deployment & Analysis

## 📌 Overview

This project demonstrates the deployment of a **Cowrie SSH honeypot** on Kali Linux to capture and analyze real-world attack attempts.
It includes a **Python-based log analysis system** to extract attacker behavior such as IP addresses, login attempts, and executed commands.

---

## 🎯 Objectives

* Deploy a functional SSH honeypot
* Capture attacker login attempts and commands
* Analyze logs to identify attack patterns
* Generate structured reports from raw data

---

## ⚙️ Features

* 🛡️ SSH Honeypot running on port **2222**
* 📊 JSON-based logging of attacker activity
* 🧠 Python script for log analysis
* 📈 Reports showing:

  * Top attacker IPs
  * Most attempted usernames & passwords
  * Commands executed by attackers
* 🔐 Sensitive logs excluded using `.gitignore`

---

## 🛠️ Tech Stack

* **Operating System:** Kali Linux
* **Honeypot:** Cowrie
* **Language:** Python
* **Data Format:** JSON
* **Tools:** Git, GitHub

---

## 📁 Project Structure

cowrie-honeypot-project/
├── cowrie/                 # Cowrie honeypot source
├── scripts/
│   └── analyze_logs.py     # Log analysis script
├── logs/
│   ├── raw/                # Raw logs (excluded from GitHub)
│   └── parsed/             # Processed logs
├── reports/                # Generated analysis reports
├── docs/                   # Notes and documentation
├── .gitignore              # Ignore sensitive files
├── README.md               # Project documentation
└── requirements.txt        # Dependencies

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/santhoshreddy28/Cowrie-Honeypot.git
cd Cowrie-Honeypot
```

### 2️⃣ Install Dependencies

```bash
sudo apt update
sudo apt install -y git python3-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind
```

### 3️⃣ Setup Cowrie

```bash
cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt
cp etc/cowrie.cfg.dist etc/cowrie.cfg
```

### 4️⃣ Configure SSH Port

Edit:

```bash
nano etc/cowrie.cfg
```

Set:

```ini
[ssh]
listen_port = 2222
```

### 5️⃣ Start Honeypot

```bash
cowrie start
cowrie status
```

---

## 🧪 Testing the Honeypot

Simulate attack attempts:

```bash
ssh root@localhost -p 2222
ssh admin@localhost -p 2222
```

Use sample passwords:

```
123456
password
admin
toor
```

---

## 📊 Log Analysis

### Copy Logs

```bash
cp cowrie/var/log/cowrie/cowrie.json* logs/raw/
```

### Run Analyzer

```bash
cd scripts
python3 analyze_logs.py
```

---

## 📄 Sample Output

```
===== COWRIE HONEYPOT ANALYSIS REPORT =====
Total Events     : 50
Unique Sessions  : 10

Top Attacker IPs:
127.0.0.1        12 attempts

Top Usernames:
root             15
admin            10

Top Passwords:
123456           20

Top Commands:
wget http://malicious.com
```

---

## 🔍 Key Findings

* Observed brute-force login attempts
* Common credentials:

  * `root / 123456`
  * `admin / admin`
* Frequently executed commands:

  * `uname -a`
  * `cat /etc/passwd`
  * `wget`, `curl`

---

## 🔐 Security Considerations

* Raw logs are **excluded from GitHub** to prevent exposure of sensitive data
* Honeypot should be deployed in a **controlled or isolated environment**
* Avoid exposing real SSH port (22) directly

---

## 💡 Skills Demonstrated

* Honeypot deployment & configuration
* Log analysis and threat detection
* Python scripting for cybersecurity
* Understanding attacker behavior patterns

---

## 🚀 Future Improvements

* 🌍 GeoIP tracking (attacker location)
* 📊 Dashboard visualization (Streamlit)
* 📈 Graph-based analytics
* ☁️ Cloud deployment (AWS)

---

## 👨‍💻 Author

**Santhosh Reddy**
GitHub: https://github.com/santhoshreddy28

---

## ⭐ Acknowledgment

* Cowrie Honeypot Project
* Open-source cybersecurity community
