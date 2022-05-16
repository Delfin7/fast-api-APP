import datetime
import unittest
import urllib.parse

import requests

from heroku import HerokuApp


class HerokuSetupTest(unittest.TestCase):
    def setUp(self):
        self.app_path = urllib.parse.urljoin(HerokuApp.app_url, "/events")

    def test_add_correct(self):
        response = requests.put(
            self.app_path, json={"date": "2022-03-01", "event": "Dzień Balearów"}
        )
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        # Not caring about those in this test
        del response_json["id"]
        del response_json["date_added"]
        self.assertEqual(
            response_json,
            {
                "name": "Dzień Balearów",
                "date": "2022-03-01",
            },
        )


if __name__ == "__main__":
    unittest.main()