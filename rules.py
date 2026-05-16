#ALERT DETECTION RULES

#BRUTE FORCE
def detect_brute_force(parsed_logs, threshold = 3):
#failed logins are more than 3, return alerts
    alerts = []
#count failed attempts per IP
    failed_counts = {} #empty dic {ip:count}
    for log in parsed_logs:
        if log["status"] == "Failed":
            ip = log["ip"]
#new ip start 0, if seen add 1
            failed_counts[ip] = failed_counts.get(ip, 0) + 1
#ip threshold >3
    for ip, count in failed_counts.items():
        if count >= threshold:
            alerts.append({
                "alert_type": "Brute Force",
                "ip": ip,
                "failed_attempts": count,
                "severity" : "CRITICAL"
            })

    return alerts

#APACHE ALERTS
def detect_apache_alerts(parsed_logs, threshold = 3):
    alerts = []
    error_counts = {} #count 404 and 500 per IP

    for log in parsed_logs:
        if log["status"] in ["404", "500"]:
            ip = log["ip"]
            error_counts[ip] = error_counts.get(ip, 0) + 1

    for ip, count in error_counts.items():
        if count >= threshold:
           alerts.append({
               "alert_type": "Suspicious Requests",
               "ip": ip,
               "error_count": count,
               "severity": "WARNING"
           })

    return alerts

#WINDOWS ALERTS
def detect_windows_alerts(parsed_logs, threshold = 3):
    alerts = []
    failed_counts = {}

    for log in parsed_logs:
        if log["event_id"] == "4625": #failed login event
            ip = log["ip"]
            failed_counts[ip] = failed_counts.get(ip, 0) + 1

    for ip, count in failed_counts.items():
        if count >= threshold:
            alerts.append({
                "alert_type": "Brute Force (Windows)",
                "ip": ip,
                "failed_attempts": count,
                "severity": "CRITICAL"
            })

    return alerts
