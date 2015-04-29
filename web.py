#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import json
import requests
from io import BytesIO
from write_src import write_src as write_db 
import parse

api_key = None

with open("config.json") as conf:
    api_key = json.load(conf)['mailgun']

def write_src(title, url):
    response = requests.get(url, auth=('api', api_key))
    fp = BytesIO(response.content)
    write_db(parse.check_and_parse(fp), title)

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        to = self.get_argument('To')
        sender = self.get_argument('sender')
        attachments = json.loads(self.get_argument('attachments'))
        title = self.get_argument('Subject')

        print(json.dumps(attachments))
        for it in attachments:
            write_src(title, it['url'])

        self.write("OK")

app = tornado.web.Application([
    (r"/post", MainHandler),
])

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
