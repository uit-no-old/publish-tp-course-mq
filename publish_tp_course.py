#!/usr/bin/env python

# Python script to publish changes in course timetable from TP to RabbitMQ
# Author: Øyvind Årnes

import pika
from datetime import datetime
from pathlib import Path
import requests
import json
import time
import sys
import logging
import os


logging.basicConfig(filename='publish_tp_course.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("pika").setLevel(logging.WARNING)

tp_rest_api_base_url = "https://tp.uio.no/uit/ws"

timestamp_file = Path("timestamp_pub")
if not timestamp_file.is_file():
    timestamp_file.write_text(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

credentials = pika.PlainCredentials(os.environ['MQ_USER'], os.environ['MQ_PASS'])
connection = pika.BlockingConnection(pika.ConnectionParameters('fulla.uit.no', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='tp-course-pub',
                         exchange_type='fanout',
                         durable=True)


timestamp = timestamp_file.read_text()
new_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
url = tp_rest_api_base_url + f"/1.4/lastchanged-list.php?type=course&timestamp={timestamp}"
r = requests.get(url)
changed_courses = r.json()

if changed_courses["elements"] is None:
    sys.exit()

for course in changed_courses["elements"]:
    print(course)
    channel.basic_publish(exchange='tp-course-pub',
                    routing_key='',
                    body=json.dumps(course),
                    properties=pika.BasicProperties(
                      delivery_mode = 2, # make message persistent
                   ))
    logging.info(f"[x] Sent: {course}")
timestamp_file.write_text(new_timestamp)
