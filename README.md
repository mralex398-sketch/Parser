# LogAnalyzer - Cyber Threat Intelligence & Log Analytics Tool

LogAnalyzer is a Python-based security auditing tool designed to parse server log files (such as Nginx, Apache, or SSH logs), extract IPv4 addresses, and enrich them with real-time geographical data. The tool generates a clean command-line summary of the most active IP addresses and exports a styled HTML threat intelligence report.

---

## ✨ Features

- **🎯 Automated IP Extraction**: Utilizes a robust Regular Expression (RegEx) pattern to accurately parse and compile all IPv4 addresses from unformatted raw text/log files.
- **🌐 Real-Time Geo-IP Enrichment**: Automatically filters out internal network ranges (`127.0.0.0/8`, `192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`) and queries the secure HTTPS endpoint of the `ipinfo.io` API to detect the country of origin for external IPs.
- **📊 Statistical Analysis**: Uses the `collections.Counter` engine to instantly calculate global hits, unique visitors, and isolate the TOP-N most aggressive IP addresses hitting your server.
- **📄 Interactive HTML Reporting**: Automatically exports analysis metrics into a clean, modern HTML table (`cyber_report.html`) complete with status badges and dynamic UI hovering for security analysts.

---

## 📋 Requirements & Installation

This project requires **Python 3.x** and the `requests` library for communicating with the Geo-IP API.

1. Clone or download this repository into your dedicated project folder:
```bash
git clone https://github.com/mralex398-sketch/
cd LogAnalyzer
```

2. Install the necessary Python packages:
```bash
pip install requests urllib3
```

---

## 🚀 Setup & Usage

To successfully run the analyzer, you need to provide a sample log file named `log.txt` in the same directory as the script.

1. Place your target server log file inside the script folder and name it:
```text
log.txt
```

2. Execute the python script:
```bash
python LogAnalyzer.py
```

### Expected Output:
- **Console**: Displays total parsed IPs, unique count, and a beautifully formatted console matrix showing the TOP 5 active IPs along with their request counts and originating countries.
- **File System**: Automatically generates a file named `cyber_report.html` containing the TOP 10 active threats.

---

## ⚖️ Disclaimer
This tool is created for administrative server maintenance, log monitoring, and legitimate cybersecurity threat analysis. Always ensure you have the proper authorization before collecting or analyzing infrastructure telemetry data.
