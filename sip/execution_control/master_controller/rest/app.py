# -*- coding: utf-8 -*-
"""SDP Element Master (REST flavour).

Run with (from the rest directory):
    gunicorn -b 0.0.0.0:5555 --reload app:APP

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import random
import socket
from time import time

import redis
from flask import Flask, jsonify, request


APP = Flask('MasterController')
MC_STATES = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
             'UNKNOWN']
START_TIME = time()


@APP.errorhandler(404)
def not_found(error=None):
    """Handler for URL not found error."""
    message = {
        'status': 404,
        'message': 'Route not Found: ' + request.path
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@APP.errorhandler(405)
def not_allowed(error=None):
    """Handler for URL method not allowed."""
    message = {
        'status': 405,
        'message': 'Method not allowed.'
    }
    if error:
        message['error'] = error
    response = jsonify(message)
    response.status_code = 405
    return response


@APP.route('/')
@APP.route('/state')
def get_state():
    """Get the SDP state."""
    message = {
        'module': 'Master Controller',
        'state': random.choice(MC_STATES)
    }
    # Add the query count to the message (if possible)
    try:
        data = redis.Redis(host='master_db')
        counter = data.incr('counter')
        message['counter'] = counter
    except redis.exceptions.ConnectionError:
        pass
    return jsonify(message)


@APP.route('/health')
@APP.route('/healthcheck')
def health_check():
    """Health check endpoint."""
    return jsonify(module='Master Controller',
                   hostname=socket.gethostname(), uptime=time() - START_TIME)


@APP.route('/init')
def init():
    """Triggers transition to INIT state."""
    try:
        data = redis.Redis(host='master_db')
        data.delete('counter')
    except redis.exceptions.ConnectionError:
        pass
    return jsonify(module='Master Controller',
                   message='Setting state to INIT.')


@APP.route('/standby')
def standby():
    """Triggers transition to STANDBY state."""
    return jsonify(module='Master Controller',
                   message='Setting state to STANDBY.')


@APP.route('/disable')
def disable():
    """Triggers transition to DISABLE state."""
    return jsonify(module='Master Controller',
                   message='Setting state to DISABLE.')


@APP.route('/on')
@APP.route('/online')
def on():
    """Triggers transition to ON state."""
    return jsonify(module='Master Controller',
                   message='Setting state to ON.')


@APP.route('/processing_blocks')
def processing_blocks():
    """Returns a list of processing blocks."""
    block_ids = [random.randrange(0, 100)
                 for _ in range(random.randint(0, 10))]
    return jsonify(count=len(block_ids), block_ids=sorted(block_ids))


@APP.route('/new_processing_block', methods=['POST', 'GET'])
def new_processing_block():
    """Creates a new processing block."""
    if request.method == 'GET':
        return not_allowed(error='GET method not availble for this route.')
    elif request.method == 'POST':
        request_data = request.get_json(silent=False)
        return jsonify(block_id=random.randint(0, 1000), request=request_data)


@APP.route('/processing_block/<block_id>')
def get_processing_block(block_id):
    """Returns information on a processing block."""
    if random.choice([True, False]):
        response = jsonify(message="Unknown processing block.")
        response.status_code = 404
        return response
    states = ['INIT', 'RUNNING', 'FINISHED']
    return jsonify(block_id=block_id, state=random.choice(states))


@APP.route('/delete_processing_block/<block_id>')
def delete_processing_block(block_id):
    """Removes a processing block."""
    if random.choice([True, False]):
        response = jsonify(message="Unknown processing block.")
        response.status_code = 404
        return response
    return jsonify(message='Removed processing block', block_id=block_id)


@APP.route('/capacity', methods=['POST'])
def capacity():
    """Returns current capacity to engage resources in processing.

    Takes JSON input with fields:

    - type (str): The processing type
    - baselines (int): Number of baselines / beams
    - frequencies (int): Frequency band extent

    Returns a JSON string with:

    - ingest buffer availability for the processing specified as available
      ingest time in seconds.

    Test with:
        curl -H "Content-Type: application/json" -X POST \
            -d '{"type":"ical", "baselines":20}' \
            http://localhost:5555/capacity
    """
    request_data = request.get_json(silent=False)
    if 'type' not in request_data:
        response = jsonify(message="Invalid or missing type.")
        response.status_code = 404
        return response
    return jsonify(request=request_data,
                   ingest_time=random.randint(0, 3600 * 20))


if __name__ == "__main__":
    APP.run(debug=True)
