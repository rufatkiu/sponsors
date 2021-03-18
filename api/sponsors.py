from bs4 import BeautifulSoup
import requests as req
import re
import json
from http.server import BaseHTTPRequestHandler

from os import environ, getenv

def getUsrDetails(u):
    reqs = req.get("https://api.github.com/users/"+u).text
    return json.loads(reqs)

def getSponsorNames():
    totalUsers = []
    for i in range(1, 1000):
        url = f'https://github.com/sponsors/davidjcralph/sponsors_partial?page={i}' # todo: get username from env variable
        resp = req.get(url)
        usrCount = 0
        sponsors = 0
        if resp.history:
            sponsors = None
        else:
            htmlGH = BeautifulSoup(resp.text, 'html.parser')
            count = htmlGH.select("div.mr-1 > a > img")

            for handle in count:
                usrCount += 1
                handle['alt'] = handle['alt'].replace('@', '')
                if len(count) > 10:
                    totalUsers.append({"handle": handle['alt'],"avatar": handle['src'], "profile": "https://github.com/"+handle['alt']})
                else:
                    totalUsers.append({"handle": handle['alt'],"avatar": handle['src'], "profile": "https://github.com/"+handle['alt'], "details": getUsrDetails(handle['alt'])})

            if usrCount == 0:
                break

    d = json.dumps(totalUsers)
    return  '{"sponsors": '+d+"}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        message = getSponsorNames()
        self.wfile.write(str(message).encode())
        return