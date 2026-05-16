#APACHE PARSER
import re
def parse_apache_log(file_content):
    results = []

    pattern = re.compile(
        r'([\d.])' #ip add
        r'\s+-\s+-\s+' #skip dashes
        r'\[(.+?)\]' #timestamp
        r'\s+"(\w+)\s+(\S+)\s+HTTP/[\d.]+"' #method and url
        r'\s+(\d+)' #status code
        r'\s+(\d+)' #response size
    )

    for line in file_content.splitlines():
        match = pattern.search(line)
        if match:
            results.append({
                "ip" : match.group(1),
                "timestamp" : match.group(2),
                "method" : match.group(3),
                "url" : match.group(4),
                "status" : match.group(5),
                "size" : match.group(6)
            })

    return results
