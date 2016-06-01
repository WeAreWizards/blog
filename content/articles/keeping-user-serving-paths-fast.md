Title: Keeping the user serving path fast
Date: 2016-06-01
Short_summary: A brief discussion on how to keep user requests fast
Category: Dev
Authors: Tom

*Reading time: ~10 minutes.*

Serving web requests should be fast and error free. There's
[some evidence](http://googleresearch.blogspot.co.uk/2009/06/speed-matters.html)
that slower pages result in less browsing.

We'll discuss a few strategies to keep requests fast.

<!-- PELICAN_END_SUMMARY -->

## Main idea

The main idea behind fast requests is to remove all work that isn't
strictly necessary to send the response.

Here are a few things that can be done asynchronously:

* Sending emails
* Uploading images to S3
* Extracting unimportant reporting data
* Notifying slack

There's a seconday advantage to this: If any of your non-serving code
paths have bugs your user might see a 500 error page even though it was
perfectly possible to reply successfully.

In some circumstances it makes sense to communicate errors
synchronously of course, so use your judgement.


## In-process queue

The first example shows how to implement a simple in-process
queue. This is useful for data that's not super important, but that
can be slow to process or send.

E.g. imagine sending metrics over the network: If the DNS query for
the metrics server blocks then your users will see slow responses
which could have been avoided.

```python
import queue
import threading

# Limit queue size to avoid filling up memory
log_queue = queue.Queue(maxsize=100)
slow_process = print

def worker():
    while True:
        # Block indefinitely
        item = log_queue.get()
        slow_process(item)


def log(line):
    try:
        log_queue.put_nowait(line)
    except Exception as e:
        print(e)
        # Note that silent exception swallowing is generally terrible,
        # but the idea here is that log data is not as important as
        # serving an error free request.
        pass

# Start the worker in-process
threading.Thread(target=worker, daemon=True).start()

log("hi")


input("hit enter to finish")
```


## Follow the syslog

Systemd's journal is a convenient tool sending messages out of process
reliably. Unlike in the thread queue example from above messages leave
the serving process immediately so the window for data loss is very
small.

The cost of sending a message to journald is between nanoseconds and
microseconds, so generally acceptable when compared to web requests
that are in the low to high milliseconds.

To use process the data we have one or several daemons that follow the
journal and respond to certain signals.

The example below looks for messages beginning with "SLACK: " and
posts their content to our [proppy](https://proppy.io/) slack
channel. We get notified by this daemon every time a new user signs up
which is very motivating.


```
import subprocess
import flask
from slackclient import SlackClient
import json

PREFIX = 'SLACK: '

def _send_message(sc, message):
    try:
        sc.api_call(
            "chat.postMessage",
            channel="#proppy",
            text=message,
            username='proppybot',
            icon_emoji=':robot_face:'
        )
    except Exception as e:
        # swallow all exceptions because this is a for fun only
        print("slack sending error.")
        print(e)


def slacklog_run_forever():
    """
    Listens to the journal forever. If you print "SLACK: xxx" to the
    logs (usually via stdout in proppy backend) well just dump that in
    the proppy channel.
    """

    token =  flask.current_app.config["SLACK_AUTH_TOKEN"]
    sc = SlackClient(token)
    p = subprocess.Popen(['journalctl', '-n', '0', '-o', 'json', '-f'], stdout=subprocess.PIPE)
    while True:
        entry = json.loads(p.stdout.readline().decode('utf8'))
        message = entry.get('MESSAGE', '')
        if not isinstance(message, str):
            continue
        if message.startswith(PREFIX):
            _send_message(sc, message[len(PREFIX):])
```

## Summary

We're using several other tricks to keep requests fast and error free,
such as storing raw POST data and only examining the contents offline
later. By skipping parsing in the user request we avoid exposing
parser bugs to the user - and we certainly had a few!

Following this principle has served us well: Last month we had an
error rate of less than one in a million for user requests in proppy.
