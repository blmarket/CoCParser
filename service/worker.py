#!/usr/bin/env python3
# coding: utf-8
"""
task processor
"""
import redis
import time
import json
from service.main import process, classify

r = None
with open("config.json", "r") as fp:
    obj = json.load(fp)
    if "redis" in obj:
        print("using redis from config")
        r = redis.StrictRedis(unix_socket_path=obj["redis"], db=1)
    else:
        r = redis.StrictRedis(db=1)

QUEUE_NAME = "jobq:task"

while True:
    task = r.rpop(QUEUE_NAME)
    if task is None:
        time.sleep(1)
        continue
    
    task_info = r.hgetall(task)
    # task_info = { 'id': task_info[b'id'], 'title': task_info[b'title'], 'attachments': [ { 'url': task_info[b'path'] } ] }
    r.hset(task, "status", "processing")
    r.publish("c:task", task)
    result = []
    for url, slit in process(task.decode('utf-8'), task_info[b'path'].decode('utf-8')):
        info = classify(slit)
        result += [ { 'url': url, 'prediction': info } ]
    r.hset(task, "result", json.dumps(result))
    r.hset(task, "status", "done")
    r.publish("c:task", task)
