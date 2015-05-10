#!/usr/bin/env python3
# coding: utf-8
"""
task processor
"""
import redis
import time
import json
from service.main import process, classify

r = redis.StrictRedis(db = 1)

QUEUE_NAME = "jobq:task"

while True:
    task = r.rpop(QUEUE_NAME)
    if task is None:
        time.sleep(1)
        continue
    
    print(task)
    task_info = r.hgetall(task)
    # task_info = { 'id': task_info[b'id'], 'title': task_info[b'title'], 'attachments': [ { 'url': task_info[b'path'] } ] }
    print(task_info)
    r.hset(task, "status", "processing")
    r.publish("c:task", task)
    result = []
    for url, slit in process(task_info[b'id'], task_info[b'title'], [ task_info[b'path'].decode('utf-8') ]):
        info = classify(slit)
        info['url'] = url
        result += [ info ]
    r.hset(task, "result", json.dumps(result))
    r.hset(task, "status", "done")
    r.publish("c:task", task)
