#Mini SIEM — Log Analyzer Dashboard
A lightweight, open-source Security Information and Event Management (SIEM) tool built with Python and Streamlit. Designed as a free alternative to enterprise tools like Splunk and QRadar.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)


##Problem Statement
Enterprise SIEM tools like Splunk and IBM QRadar are expensive, complex, and require significant infrastructure — making them inaccessible for small organizations, students, and security beginners.
This project provides a free, lightweight alternative that:
- Requires only Python and Streamlit
- Auto-detects log formats without configuration
- Provides real-time threat detection out of the box
- Includes a training mode for SOC analyst learning


##Features
1. Auto Log Detection: Detects SSH, Apache, Windows logs automatically.
2. Threat Detection: Brute force, suspicious requests, anomaly rules.
3. IP Geolocation: Traces attack origin country and city.
4. Visual Analytics: Bar charts and status breakdown graphs.
5. Log Summary: Top IPs, usernames, attack statistics.
6. Alert Timestamps: Records exact time each threat was detected.
7. CSV Export: Download full alert report as CSV.
8. Email Simulation: Preview alert emails without sending.
9. Search & Filter: Filter logs by keyword or status.
10. Training Mode: Pre-loaded sample logs with explanations.


##Tech Stack
- *Python 3.12* — Core logic and parsing
- *Streamlit* — Web dashboard UI
- *Pandas* — Data manipulation and tables
- *Regex (re)* — Log pattern matching
- *ip-api.com* — Free IP geolocation API
- *smtplib* — Email simulation


##Project Structure
Mini-SIEM/
├── app.py                  ← Main Streamlit application
├── parser/
│   ├── ssh_parser.py       ← SSH auth log parser
│   ├── apache_parser.py    ← Apache access log parser
│   └── windows_parser.py   ← Windows event log parser
├── detector/
│   └── rules.py            ← Alert detection rules
├── utils/
│   ├── log_detector.py     ← Auto log format detection
│   ├── geoip.py            ← IP geolocation
│   ├── emailer.py          ← Email alert simulation
│   ├── sample_logs.py      ← Built-in sample logs
│   └── ai_explainer.py     ← AI log explanation
├── test_ssh.log            ← Sample SSH log for testing
├── test_apache.log         ← Sample Apache log for testing
└── test_windows.log        ← Sample Windows log for testing


##How to Run
1. Clone the repository
```bash
git clone https://github.com/rashikajangra/Mini-SIEM.git
cd Mini-SIEM
```
2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```
3. Install dependencies
```bash
pip install streamlit pandas google-generativeai
```
4. Run the app
```bash
streamlit run app.py
```
5. Open in browser
http://localhost:8501


##Supported Log Types
1. SSH Auth Logs
- Parses failed and successful login attempts
- Detects brute force attacks (3+ failed attempts from same IP)
- Extracts: timestamp, username, IP, status

2. Apache Access Logs
- Parses web server access logs
- Detects suspicious scanning (3+ 404/500 errors from same IP)
- Extracts: IP, timestamp, method, URL, status code

3. Windows Event Logs
- Parses exported Windows security events
- Detects brute force via EventID 4625
- Extracts: EventID, event name, timestamp, username, IP, status


##Detection Rules
|_Rule____________|_Log Type_|_Trigger________________________|_Severity_|
|-----------------|----------|--------------------------------|----------|
|_Brute Force_____|_SSH______|_3+ failed logins from same IP__|_Critical_|
|_Brute Force_____|_Window___|_3+ EventID 4625 from same IP___|_Critical_|
|_Suspicious Scan_|_Apache___|_3+ 404/500 errors from same IP_|_Warning__|


##Screenshots
-Dashboard with parsed SSH logs, brute force alert, and visual charts
<img width="1879" height="920" alt="image" src="https://github.com/user-attachments/assets/a3fd08f9-ec02-42c7-b10a-18f4a1d276ab" />
<img width="1881" height="911" alt="image" src="https://github.com/user-attachments/assets/05e55769-f16e-40a4-97ba-4312b2f421ab" />
<img width="1889" height="898" alt="image" src="https://github.com/user-attachments/assets/d4ea4a75-030f-416b-be3e-be6f919a061c" />


##Author
Rashika Jangra 
[GitHub](https://github.com/rashikajangra)


##License
This project is licensed under the MIT License — see the
[LICENSE](LICENSE) file for details.


##If this helped you, give it a star⭐!
