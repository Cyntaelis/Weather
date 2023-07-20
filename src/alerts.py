import requests

def get_alerts(coords):
    header = {"accept" : "application/geo+json"}
    url = "https://api.weather.gov/alerts/active"
    params = {
        "point":f"{coords[0]},{coords[1]}"
    }
    r = requests.get(url,headers=header,params=params)
    counter = 0
    post = "=== ALERTS ===\n\n"
    for alert in r.json()["features"]:
        counter += 1
        post += f'=== ALERT {counter} : {alert["properties"]["severity"]} ==='
        post += "\n"
        post += alert["properties"]["headline"]
        post += "\n"
        post += alert["properties"]["description"]
        post += "\n"
        if alert["properties"]["instruction"] is not None:
            post += alert["properties"]["instruction"]
            post += "\n"
        post += f"=== END ALERT {counter} ===\n"
    post += "\n=== END ==="
    return post
