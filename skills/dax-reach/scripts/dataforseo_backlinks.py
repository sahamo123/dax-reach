#!/usr/bin/env python3
"""Optional DataForSEO backlink adapter. Dry-run unless --execute-paid is explicit."""
import argparse
import base64
from datetime import datetime, timezone
import http.client
import json
import os
import re
import sys

HOST = 'api.dataforseo.com'
ENDPOINTS = {'summary': '/v3/backlinks/summary/live', 'links': '/v3/backlinks/backlinks/live'}
MAX_RESPONSE = 5_000_000


def prepare(target, mode='summary', limit=20):
    # A domain-only adapter deliberately avoids arbitrary URLs, paths, and credentials.
    target = target.strip().lower().rstrip('.').encode('idna').decode('ascii')
    if len(target) > 253 or not re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,62}', target):
        raise ValueError('Use a bare public domain, such as example.com')
    if mode not in ENDPOINTS or not 1 <= limit <= 100:
        raise ValueError('Choose summary or links with a limit from 1 to 100')
    task = {'target': target}
    if mode == 'links':
        task.update({'mode': 'as_is', 'limit': limit})
    return {'status': 'dry-run', 'endpoint': 'https://' + HOST + ENDPOINTS[mode],
            'payload': [task], 'requests': 1, 'automatic_retries': 0,
            'cost': 'Paid API; exact charge is not estimated here. Check current account pricing before execution.'}


def redact(value, secrets):
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, '[REDACTED]')
        return value
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, dict):
        return {redact(str(key), secrets): redact(item, secrets) for key, item in value.items()
                if str(key).lower() not in ('authorization', 'password', 'login', 'api_key', 'token')}
    return value


def run(target, mode='summary', limit=20, execute_paid=False, environ=None, connection_factory=None):
    plan = prepare(target, mode, limit)
    if not execute_paid:
        return plan
    environ = os.environ if environ is None else environ
    login, password = environ.get('DATAFORSEO_LOGIN', ''), environ.get('DATAFORSEO_PASSWORD', '')
    if not login or not password or ':' in login or any(c in login + password for c in '\r\n'):
        raise ValueError('Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD locally using the API Access credentials')
    token = base64.b64encode((login + ':' + password).encode()).decode('ascii')
    factory = connection_factory or http.client.HTTPSConnection
    connection = factory(HOST, timeout=30)
    try:
        connection.request('POST', ENDPOINTS[mode], body=json.dumps(plan['payload']).encode(),
                           headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + token})
        response = connection.getresponse()
        # Never follow redirects or forward Authorization to another origin.
        if response.status != 200:
            raise ValueError('DataForSEO HTTP request failed; no retry performed')
        raw = response.read(MAX_RESPONSE + 1)
        if len(raw) > MAX_RESPONSE:
            raise ValueError('Response exceeds size limit; no retry performed')
        payload = json.loads(raw)
        tasks = payload.get('tasks') if isinstance(payload, dict) else None
        if payload.get('status_code') != 20000 or not isinstance(tasks, list) or len(tasks) != 1:
            raise ValueError('DataForSEO API did not return one successful task; check account/API access')
        task = tasks[0]
        if not isinstance(task, dict) or task.get('status_code') != 20000 or not isinstance(task.get('result'), list):
            raise ValueError('DataForSEO task failed; check account access, balance, and request support')
        result = {'provider': 'DataForSEO', 'target': plan['payload'][0]['target'], 'mode': mode,
                  'retrieved_at': datetime.now(timezone.utc).isoformat(), 'requests': 1,
                  'reported_cost': payload.get('cost'), 'result': task['result'],
                  'scope': 'Provider-index observation; not a complete web index or proof of current link presence.'}
        return redact(result, [login, password, token])
    except (OSError, http.client.HTTPException, UnicodeError, json.JSONDecodeError, AttributeError) as error:
        raise ValueError('DataForSEO request or response failed; no automatic retry. Inspect account usage before retrying.') from None
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    parser.add_argument('--mode', choices=ENDPOINTS, default='summary')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--execute-paid', action='store_true', help='Authorize one billable API request using local credentials')
    args = parser.parse_args()
    try:
        result = run(args.target, args.mode, args.limit, args.execute_paid)
    except (ValueError, UnicodeError):
        parser.exit(1, 'Request not completed. Check domain, limit, API credentials, account access/balance, and network. No automatic retry; credentials and raw errors are suppressed.\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
