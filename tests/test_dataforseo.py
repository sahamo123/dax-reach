import json
import unittest
from unittest.mock import Mock
from test_tools import load

adapter = load('dataforseo', 'skills/dax-reach/scripts/dataforseo_backlinks.py')


class DataForSEOTests(unittest.TestCase):
    def response(self, payload, status=200):
        connection = Mock()
        response = connection.getresponse.return_value
        response.status = status
        response.read.return_value = json.dumps(payload).encode()
        return connection, Mock(return_value=connection)

    def credentials(self):
        return {'DATAFORSEO_LOGIN': 'fictional@example.com', 'DATAFORSEO_PASSWORD': 'fictional-credential'}

    def test_dry_run_never_reads_credentials_or_calls_network(self):
        factory = Mock(side_effect=AssertionError('No network allowed'))
        result = adapter.run('example.com', connection_factory=factory)
        self.assertEqual(result['status'], 'dry-run')
        factory.assert_not_called()

    def test_exactly_one_bounded_request_and_success(self):
        connection, factory = self.response({'status_code': 20000, 'cost': 0.01, 'tasks': [{'status_code': 20000, 'result': [{'backlinks': 12}]}]})
        result = adapter.run('Example.com', 'links', 25, True, self.credentials(), factory)
        factory.assert_called_once_with('api.dataforseo.com', timeout=30)
        connection.request.assert_called_once()
        args, kwargs = connection.request.call_args
        self.assertEqual(args, ('POST', '/v3/backlinks/backlinks/live'))
        self.assertEqual(json.loads(kwargs['body']), [{'target': 'example.com', 'mode': 'as_is', 'limit': 25}])
        self.assertTrue(kwargs['headers']['Authorization'].startswith('Basic '))
        self.assertEqual(result['result'][0]['backlinks'], 12)
        self.assertNotIn('fictional-credential', json.dumps(result))
        connection.close.assert_called_once()

    def test_missing_credentials_do_not_contact_provider(self):
        factory = Mock()
        with self.assertRaises(ValueError):
            adapter.run('example.com', execute_paid=True, environ={}, connection_factory=factory)
        factory.assert_not_called()

    def test_redirect_and_http_failure_are_not_retried(self):
        for status in (301, 302, 307, 401, 429, 500):
            with self.subTest(status=status):
                connection, factory = self.response({}, status)
                with self.assertRaises(ValueError):
                    adapter.run('example.com', execute_paid=True, environ=self.credentials(), connection_factory=factory)
                connection.request.assert_called_once()
                connection.close.assert_called_once()

    def test_api_failure_and_malformed_response_fail_without_raw_echo(self):
        for payload in ({'status_code': 40100}, {'status_code': 20000, 'tasks': [{'status_code': 40000}]}, [], {'status_code': 20000, 'tasks': []}):
            with self.subTest(payload=payload):
                _, factory = self.response(payload)
                with self.assertRaises(ValueError):
                    adapter.run('example.com', execute_paid=True, environ=self.credentials(), connection_factory=factory)

    def test_echoed_credentials_are_redacted(self):
        payload = {'status_code': 20000, 'tasks': [{'status_code': 20000, 'result': [{'note': 'fictional-credential', 'password': 'do not expose'}]}]}
        _, factory = self.response(payload)
        result = adapter.run('example.com', execute_paid=True, environ=self.credentials(), connection_factory=factory)
        self.assertEqual(result['result'], [{'note': '[REDACTED]'}])

    def test_invalid_target_or_limit_rejected(self):
        for target, limit in [('https://example.com', 20), ('example.com/path', 20), ('x@example.com', 20), ('example.com', 101), ('example.com', 0)]:
            with self.subTest(target=target, limit=limit), self.assertRaises(ValueError):
                adapter.prepare(target, limit=limit)

    def test_transport_error_is_redacted_and_not_retried(self):
        connection, factory = self.response({})
        connection.request.side_effect = OSError('fictional-credential')
        with self.assertRaises(ValueError) as raised:
            adapter.run('example.com', execute_paid=True, environ=self.credentials(), connection_factory=factory)
        self.assertNotIn('fictional-credential', str(raised.exception))
        connection.request.assert_called_once()
        connection.close.assert_called_once()

    def test_oversized_and_invalid_json_responses_fail(self):
        for body in (b'x' * (adapter.MAX_RESPONSE + 1), b'not JSON'):
            connection, factory = self.response({})
            connection.getresponse.return_value.read.return_value = body
            with self.assertRaises(ValueError):
                adapter.run('example.com', execute_paid=True, environ=self.credentials(), connection_factory=factory)
            connection.close.assert_called_once()
