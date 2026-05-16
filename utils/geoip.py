#Get location info for an IP add
import urllib.request
import json

#return info of an ip
def get_ip(ip):
    try:
        if ip.startswith('192.168') or ip.startswith("10.") or ip.startswith("127."):
            return {
                "ip": ip,
                "country": "Private Network",
                "region" : "N/A",
                "city": "N/A"}

        url = f"http://ip-api.com/json/{ip}"
        with urllib.request.urlopen(url, timeout = 5) as response:
            data = json.loads(response.read().decode())

        if data["status"] == "success":
            return{
                "ip": ip,
                "country": data.get("country", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown") }
        else:
            return{"ip": ip,
                "country": "Unknown",
                "region": "Unknown",
                "city": "Unknown" }

    except Exception:
        return{"ip": ip,
                "country": "ERROR",
                "region": "ERROR",
                "city": "ERROR" }

#return list of alerts with loc info
def geolocate_alerts(alerts):
    results = []
    for alerts in alerts:
        location = get_ip(alerts["ip"])
        alerts["country"] = location["country"]
        alerts["city"] = location["city"]
        results.append(alerts)

    return results