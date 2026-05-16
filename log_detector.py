#detect log type from content
def detect_log_type(file_content):
    sample = "\n".join(file_content.splitlines()[:20])
    if "Failed password" in sample or "Accepted password" in sample:
        return "ssh"
    elif "GET" in sample or "POST" in sample or "HTTP/1." in sample:
        return "apache"
    elif "EventID" in sample or "4625" in sample or "4624" in sample:
        return "windows"
    else:
        return "unknown"