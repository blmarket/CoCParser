#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import json
import requests
from io import BytesIO
import parse
from concurrent.futures import ProcessPoolExecutor as Executor

import service.main

executor = Executor()
api_key = None

with open("config.json") as conf:
    api_key = json.load(conf)['mailgun']

def download_from_mailgun(url):
    response = requests.get(url, auth=('api', api_key))
    return BytesIO(response.content)

def convert_urls(attachments):
    for it in attachments:
        yield download_from_mailgun(it['url'])

class MainHandler(tornado.web.RequestHandler):
    def handle_task(task):
        from write_src import write_src as write_db 
        title = task['title']
        for fp in convert_urls(task['attachments']):
            write_db(parse.check_and_parse(fp), title)

    def post(self):
        to = self.get_argument('To')
        sender = self.get_argument('sender')
        attachments = json.loads(self.get_argument('attachments'))
        title = self.get_argument('Subject')

        task = {'to': to, 'sender': sender, 'attachments': attachments, 'title': title }
        print("MainHandler", json.dumps(task))

        executor.submit(handle_task, task)
        self.write("OK")

class ServiceHandler(tornado.web.RequestHandler):
    def handle_task(task):
        for fp in convert_urls(task['attachments']):
            print(service.main.classify(fp))

    def post(self):
        to = self.get_argument('To')
        sender = self.get_argument('sender')
        attachments = json.loads(self.get_argument('attachments'))
        title = self.get_argument('Subject')

        task = {'to': to, 'sender': sender, 'attachments': attachments, 'title': title }
        print("ServiceHandler", json.dumps(task))

        executor.submit(handle_task, task)

        self.write("OK")

app = tornado.web.Application([
    (r"/post", MainHandler),
    (r"/v0/post", ServiceHandler),
])

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
