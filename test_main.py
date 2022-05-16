import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/method")

    def test_post(self):
        post_response = requests.post(self.app_path)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(
            post_response.json(),
            {"method": "POST"},
        )


if __name__ == "__main__":
    unittest.main()