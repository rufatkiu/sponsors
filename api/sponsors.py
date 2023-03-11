from bs4 import BeautifulSoup
import requests as req
import json
from http.server import BaseHTTPRequestHandler

def getSponsorNames():
    totalUsers = []
    for i in range(1, 1000):
        # todo: add opencollective support
        url = f'https://github.com/sponsors/mue/sponsors_partial?page={i}' # todo: get username from env variable
        resp = req.get(url)
        usrCount = 0
        htmlGH = BeautifulSoup(resp.text, 'html.parser')
        count = htmlGH.select("div.mr-1 > a > img")

        for handle in count:
            usrCount += 1
            handle['alt'] = handle['alt'].replace('@', '')
            totalUsers.append({"handle": handle['alt'],"avatar": handle['src']})

        if usrCount == 0:
            break

    d = json.dumps(totalUsers)
    return  '{"sponsors": '+d+"}"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'max-age=0, s-maxage=86400')
        self.end_headers()
        message = getSponsorNames()
        self.wfile.write(str(message).encode())
        return
