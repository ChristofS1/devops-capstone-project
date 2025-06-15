import unittest
from flask import Flask
from werkzeug.exceptions import NotFound, InternalServerError
# Importiere die Fehlerhandler aus deiner Anwendung
# Angenommen, die Funktionen heißen not_found_error, internal_error, handle_http_exception
# und sind in service.common.error_handlers definiert
from service.common.error_handlers import not_found, internal_server_error


class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        # Erstelle eine Test-App und registriere die Fehlerhandler
        self.app = Flask(__name__)
        self.app.register_error_handler(404, not_found)
        self.app.register_error_handler(500, internal_server_error)
        self.client = self.app.test_client()

    def test_404_error_handler(self):
        # Simuliere einen 404-Fehler
        @self.app.route('/not-found')
        def trigger_404():
            raise NotFound()
        resp = self.client.get('/not-found')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content_type, 'application/json')
        # Prüfe, ob die Antwort das erwartete JSON enthält
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not Found")

    def test_500_error_handler(self):
        # Simuliere einen 500-Fehler
        @self.app.route('/internal-error')
        def trigger_500():
            raise InternalServerError()
        resp = self.client.get('/internal-error')
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.content_type, 'application/json')
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Internal Server Error")


if __name__ == '__main__':
    unittest.main()
