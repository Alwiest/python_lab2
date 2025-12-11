import io
import json
import unittest
from unittest.mock import Mock, patch

import requests

from main import logger, get_currencies


class TestGetCurrenciesFunction(unittest.TestCase):
    def test_correct_currency_return(self):
        with patch('main.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "Valute": {
                    "USD": {"Value": 93.25},
                    "EUR": {"Value": 101.7}
                }
            }
            mock_get.return_value = mock_resp

            result = get_currencies(['USD', 'EUR'])
            self.assertIsInstance(result, dict)
            self.assertEqual(result['USD'], 93.25)
            self.assertEqual(result['EUR'], 101.7)

    def test_non_exist_currency(self):
        with patch('main.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "Valute": {
                    "USD": {"Value": 93.25}
                }
            }
            mock_get.return_value = mock_resp

            with self.assertRaises(KeyError) as ctx:
                get_currencies(['XYZ'])

            self.assertIn("XYZ", str(ctx.exception))
            self.assertIn("отсутствует", str(ctx.exception))

    def test_connection_error(self):
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            with self.assertRaises(ConnectionError) as ctx:
                get_currencies(['USD'])
            self.assertIn("Ошибка подключения", str(ctx.exception))

    def test_value_error_json(self):
        with patch('main.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 200
            mock_resp.json.side_effect = json.JSONDecodeError("bad JSON", "", 0)
            mock_get.return_value = mock_resp

            with self.assertRaises(ValueError) as ctx:
                get_currencies(['USD'])
            self.assertIn("Ошибка парсинга JSON", str(ctx.exception))

    def test_key_missing_valute(self):
        with patch('main.requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"Data": {}}
            mock_get.return_value = mock_resp

            with self.assertRaises(KeyError) as ctx:
                get_currencies(['USD'])
            self.assertIn("отсутствует ключ 'Valute'", str(ctx.exception))


class TestLoggerDecorator(unittest.TestCase):
    def test_logging_success(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def f(x, y=1):
            return x * y

        res = f(5, y=2)
        self.assertEqual(res, 10)
        logs = stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("f", logs)
        self.assertIn("Логгер отработал успешно", logs)
        self.assertNotIn("ERROR", logs)

    def test_logging_on_error(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def bad():
            raise ValueError("Test error message")

        with self.assertRaises(ValueError):
            bad()

        logs = stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Test error message", logs)


class TestStreamWrite(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://alwiest")

        self.wrapped = wrapped

    def test_logging_error(self):
        # Подменяем requests.get так, чтобы поднять ConnectionError
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("fail")
            with self.assertRaises(ConnectionError):
                self.wrapped()

            logs = self.stream.getvalue()
            self.assertIn("ERROR", logs)
            self.assertIn("ConnectionError", logs)


if __name__ == '__main__':
    unittest.main()
