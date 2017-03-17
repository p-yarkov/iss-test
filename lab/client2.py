#!/usr/bin/env python

import asyncio
import websocket
import _thread
import json
import time

REQS = [ # нумерация с 0
    {
		'type': 'subscribe',
		'id': 1,
		'data': {
			'clear' : False,
			'add_rules': [
					{
						'type': 'CAM',
						'action': 'STATE_CHANGED'
					}
				]
		}
	},
        {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'add_rules': [
                {
                    'type': 'CAM',
                    'action': 'STATE_CHANGED'
                },
                {
                    'type': 'SLAVE',
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    },
    {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'add_rules': [
                {
                    'type': 'CAM',
                    'id': '1',
                    'action': 'STATE_CHANGED'
                },
                {
                    'type': 'SLAVE',
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    },
    {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'delete_rules': [
                {
                    'type': 'CAM',
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    },
    {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'delete_rules': [
                {
                    'type': 'CAM',
                    'id': '1',
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    },
    {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'add_rules': [
                {
                    'type': 'CAM',
                    'states': ['attached'],
                    'action': 'STATE_CHANGED'
                },
                {
                    'type': 'SLAVE',
                    'states': ['attached'],
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    },
    {
        'type': 'subscribe',
        'id': 12345,
        'data': {
            'clear': False,
            'add_rules': [
                {
                    'type': 'CAM',
                    'states': ['attached'],
                    'action': 'STATE_CHANGED'
                },
                {
                    'type': 'SLAVE',
                    'id': 'FAKE',
                    'states': ['attached'],
                    'action': 'STATE_CHANGED'
                }
            ]
        }
    }
]

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def single(n):
    req = REQS[n]
    print("REQUEST SEND: " + json.dumps(req))
    while True:
        ws.send(json.dumps(req))
        time.sleep(1)

def all():

    for req in REQS:
        print("REQUEST SEND: " + json.dumps(req))
        ws.send(json.dumps(req))
        time.sleep(1)

def on_open(ws):
    def run(*args):

        single(0)
        #all()
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/echo",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
