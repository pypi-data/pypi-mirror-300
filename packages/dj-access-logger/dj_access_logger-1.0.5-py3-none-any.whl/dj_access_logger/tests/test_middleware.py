# python
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.utils.timezone import now

from dj_access_logger.middleware import AccessLogMiddleware


class AccessLogMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AccessLogMiddleware(get_response=lambda r: HttpResponse("Test response"))
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', phone='1234567890', password='12345')

    def test_middleware_processes_request(self):
        request = self.factory.get('/test-url/')
        request.user = self.user

        self.middleware.process_request(request)
        self.assertIsNotNone(request.start_time)

    def test_middleware_processes_response(self):
        request = self.factory.get('/test-url/')
        request.user = self.user
        request.start_time = now()
        response = HttpResponse("Test response")

        with patch('dj_access_logger.repositories.repositories.LogData.log') as mock_log:
            processed_response = self.middleware.process_response(request, response)

            mock_log.assert_called_once()
            self.assertEqual(processed_response, response)

    def test_middleware_logs_post_request(self):
        post_data = {'key': 'value'}
        request = self.factory.post('/test-url/', data=post_data)
        request.user = self.user
        request.start_time = now()
        response = HttpResponse("Test response")

        with patch('dj_access_logger.repositories.repositories.LogData.log') as mock_log:
            self.middleware.process_response(request, response)

            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            self.assertEqual(call_args.request.method, 'POST')
            self.assertEqual(call_args.request.request_path, '/test-url/')
            self.assertIn('key=value', call_args.request.data)

    def test_middleware_logs_ip_address(self):
        request = self.factory.get('/test-url/')
        request.user = self.user
        request.start_time = now()
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        response = HttpResponse("Test response")

        with patch('dj_access_logger.repositories.repositories.LogData.log') as mock_log:
            self.middleware.process_response(request, response)

            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            self.assertEqual(call_args.request.ip_address, '127.0.0.1')
            self.assertEqual(call_args.request.ipv4_address, '127.0.0.1')

    def test_middleware_logs_response_data(self):
        request = self.factory.get('/test-url/')
        request.user = self.user
        request.start_time = now()
        response = HttpResponse("Test response", status=201)

        with patch('dj_access_logger.repositories.repositories.LogData.log') as mock_log:
            self.middleware.process_response(request, response)

            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            self.assertEqual(call_args.response.status_code, 201)
            self.assertEqual(call_args.response.data, "Test response")

    def test_get_client_ip(self):
        request = self.factory.get('/test-url/')
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'

        ip, ipv4, ipv6 = self.middleware.get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')
        self.assertEqual(ipv4, '192.168.1.1')
        self.assertIsNone(ipv6)

        request.META['HTTP_X_FORWARDED_FOR'] = '2001:db8::1'
        ip, ipv4, ipv6 = self.middleware.get_client_ip(request)
        self.assertEqual(ip, '2001:db8::1')
        self.assertIsNone(ipv4)
        self.assertEqual(ipv6, '2001:db8::1')
