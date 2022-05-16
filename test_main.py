import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/day")

    def test_monday_correct(self):
        response = requests.get(self.app_path + "?name=monday&number=1")
        self.assertEqual(response.status_code, 200)

    def test_tuesday_correct(self):
        response = requests.get(self.app_path + "?name=tuesday&number=2")
        self.assertEqual(response.status_code, 200)

    def test_saturday_correct(self):
        response = requests.get(self.app_path + "?name=saturday&number=6")
        self.assertEqual(response.status_code, 200)

    def test_sunday_correct(self):
        response = requests.get(self.app_path + "?name=sunday&number=7")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()