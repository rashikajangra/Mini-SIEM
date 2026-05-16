#Simulates email alerts (no real email sent)
def alert_email(receiver_email, alerts):
#Builds a simulated email preview
    body = f"TO: {receiver_email}\n"
    body += f"FROM: minisiem.alerts@system.com\n"
    body += f"SUBJECT: Mini SIEM Alert — {len(alerts)} Threat(s) Detected\n"
    body += "=" * 40 + "\n\n"
    body += "Mini SIEM has detected the following threats:\n\n"

    for i, alert in enumerate(alerts, 1):
        body += f"Alert #{i}\n"
        body += f"  Type     : {alert.get('alert_type', 'N/A')}\n"
        body += f"  IP       : {alert.get('ip', 'N/A')}\n"
        body += f"  Severity : {alert.get('severity', 'N/A')}\n"
        body += f"  Country  : {alert.get('country', 'N/A')}\n"
        body += f"  City     : {alert.get('city', 'N/A')}\n"
        body += "-" * 30 + "\n"

    body += "\nThis is a simulated alert from Mini SIEM Dashboard."
    return body
