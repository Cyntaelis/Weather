import requests
import datetime

def coords_to_zone(coords):
    url = f"https://api.weather.gov/points/{coords[0]},{coords[1]}"
    r = requests.get(url)
    try:
        zone = r.json()["properties"]["forecastZone"].split("/")[-1]
    except:
        print(coords,r.json().keys())
        z=1/0
    return zone

def weather(zone):
    
    post = ""
    name = ""
    try:
        header = {"accept" : "application/geo+json"}
        url = f"https://api.weather.gov/zones/public/{zone}/forecast"
        r = requests.get(url,headers=header)
        post += "\n\nDate: "
        post += r.json()["properties"]["updated"].replace("T","\n Time: ")[:-6]+"\n TZ: "+r.json()["properties"]["updated"][-6:]
        post += "\n\n"
    except Exception as e:
        post += str(e)
        
    
    counter=0
    for x in r.json()["properties"]["periods"]:
        counter+=1
        if counter==4:
            break
        try:
            post += "["+x["name"]+"]"
            post += "\n* "
            post += x["detailedForecast"].replace(".",".\n* ")
            post = post[:-2]
            post += "\n"
            #post += "\n"
        except Exception as e:
            return(post,"\n",e)
        
    try:
        url2 = f"https://api.weather.gov/zones/forecast/{zone}"
        r2 = requests.get(url2)
        name = " "+r2.json()["properties"]["name"]
    except:
        name = ""

    post += "=== END ==="        

    post = f"=== WEATHER {zone}{name.upper()} ===" + post #TODO add zone name

    return post
