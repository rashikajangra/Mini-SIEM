#SSH PARSER
import re
def parse_ssh_log(file_content):
#raw logs into dic, each line = one dic
    results = []

    pattern = re.compile(
        r'(\w+\s+\d+\s+\d+:\d+:\d+)' #date and time
        r'.*?(Failed|Accepted)' #status
        r'\s+password\s+for\s+(\w+)' #username
        r'\s+from\s+([\d.]+)' #IP add
    )
#split file into individual lines
    for line in file_content.splitlines():
        match = pattern.search(line) #try to match pattern
        if match:
            results.append({
                "timestamp": match.group(1),
                "status": match.group(2),
                "username": match.group(3),
                "ip": match.group(4)
            })

    return results #list of all parsed lines
