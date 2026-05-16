#WINDOW LOG PARSER
import re
def parse_windows_log(file_content):
    results = []

    pattern = re.compile(
        r'EventID:\s*(\d+)' #event id
        r'.*?Time:\s*([\d\- :]+)' #timestamp
        r'.*?User:\s*(\w+)' #username
        r'.*?IP:\s*([\d.]+)' #ip
        r'.*?Status:\s*(\w+)' #status
    )

    for line in file_content.splitlines():
        match = pattern.search(line)
        if match:
            event_id = match.group(1)
#event id to human readable

            if event_id == "4625":
                event_name = "Failed Login"
            elif event_id == "4624":
                event_name = "Successful Login"
            elif event_id == "4634":
                event_name = "Logout"
            else:
                event_name = "Unkown Event"

            results.append({
                "event_id": event_id,
                "event_name": event_name,
                "timestamp": match.group(2).strip(),
                "username": match.group(3),
                "ip": match.group(4),
                "status": match.group(5)
            })
    return results
