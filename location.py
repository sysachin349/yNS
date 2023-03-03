import requests
import geocoder
# class loc():
#     def geoLoc(ip):
#         g = geocoder.ip(ip)
#         return(g.latlng)

class loc():
    def geoLoc( ip,port ):
        proxy = str(ip).strip() + ":" + str(port).strip()
        proxies = {"https": "http://"+proxy.strip()}
        try:
            r = requests.get("https://ipinfo.io/json", proxies=proxies , timeout=5)
            if r.status_code == 200:
                return(r.json()["loc"])
        except Exception as e:
            print("[  Proxy Error  ] ", proxy)