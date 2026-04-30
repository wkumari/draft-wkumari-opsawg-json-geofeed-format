import unittest
import io
import json
from convert import process_csv


class TestCSVParser(unittest.TestCase):

    # Examples from the RFC8805 document
    def test_standard_ipv4_parsing(self):
        csv_data = "192.0.2.5,US,US-AL,Alabaster,\n"
        # Simulate an input stream
        stream = io.StringIO(csv_data)

        result_json = process_csv(stream)
        data = json.loads(result_json)

        # Verify we got exactly one record
        self.assertEqual(len(data), 1)

        # Verify the dynamically parsed fields
        self.assertEqual(data[0]["ip_prefix"], "192.0.2.5")
        self.assertEqual(data[0]["alpha2code"], "US")
        self.assertEqual(data[0]["region"], "US-AL")
        self.assertEqual(data[0]["city"], "Alabaster")

        # Verify static/injected fields
        self.assertTrue("T" in data[0]["last_updated"])  # Quick check for date format

    def test_ipv6_and_empty_fields(self):
        csv_data = "2001:db8::1,US,,,\n"
        stream = io.StringIO(csv_data)

        result_json = process_csv(stream)
        data = json.loads(result_json)

        self.assertEqual(data[0]["ip_prefix"], "2001:db8::1")
        self.assertEqual(data[0]["alpha2code"], "US")
        # Ensure missing fields evaluate to empty strings
        self.assertEqual(data[0]["region"], "")
        self.assertEqual(data[0]["city"], "")

    def test_ignore_comment_records(self):
        csv_data = (
            "# IETF106 (Singapore) - November 2019 - Singapore, SG\n"
            "130.129.0.0/16,SG,SG-01,Singapore,"
        )
        stream = io.StringIO(csv_data)

        result_json = process_csv(stream)
        data = json.loads(result_json)

        # Data should contain only the non-comment record
        self.assertEqual(len(data), 1)

        # And the fields should be correctly parsed. 2 tests for the price of one!
        self.assertEqual(data[0]["ip_prefix"], "130.129.0.0/16")
        self.assertEqual(data[0]["alpha2code"], "SG")
        self.assertEqual(data[0]["region"], "SG-01")
        self.assertEqual(data[0]["city"], "Singapore")

    def test_empty_input(self):
        stream = io.StringIO("")
        result_json = process_csv(stream)
        data = json.loads(result_json)

        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
