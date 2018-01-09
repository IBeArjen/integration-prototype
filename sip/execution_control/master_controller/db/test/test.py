# -*- coding: utf-8 -*-
"""."""
import redis
import time


db = redis.Redis(host='localhost', port=6379, db=0)

db.set('foo', 2)
print('foo =', db.get('foo'))

data = dict(a=2, b=3, c='foo')
db.hmset('my-dict', data)
print('my-dict =', db.hgetall('my-dict'))
print('my-dict =', db.hget('my-dict', 'a'))

pubsub = db.pubsub()
pubsub.subscribe(['test'])

db.publish('test', 'hello')
db.publish('test', 'there')

print(db.pubsub_channels())

fail_count = 0

start = time.time()
while fail_count < 20:
    message = pubsub.get_message(timeout=0.01)
    if message:
        print(message)
    fail_count += 1
print('0.2f', time.time() - start)
