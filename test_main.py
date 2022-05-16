import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/day")

    def test_nonday_404(self):
        response = requests.get(self.app_path + "?name=nonday&number=2")
        self.assertEqual(response.status_code, 400)

    def test_sunday_4_404(self):
        response = requests.get(self.app_path + "?name=sunday&number=4")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()