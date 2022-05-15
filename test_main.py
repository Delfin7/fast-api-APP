import unittest

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self._response = requests.get(HerokuApp.app_url)

    def test_url_exists(self):
        self.assertIsNotNone(HerokuApp.app_url)
        self.assertIsInstance(HerokuApp.app_url, str)
        self.assertNotEqual(HerokuApp.app_url, "")

    def test_status_code(self):
        self.assertEqual(self._response.status_code, 200)

    def test_response(self):
        self.assertEqual(
            self._response.json(),
            {"start": "1970-01-01"},
        )


if __name__ == "__main__":
    unittest.main()