import unittest

from clairview import Clairview


class TestModule(unittest.TestCase):
    clairview = None

    def _assert_enqueue_result(self, result):
        self.assertEqual(type(result[0]), bool)
        self.assertEqual(type(result[1]), dict)

    def failed(self):
        self.failed = True

    def setUp(self):
        self.failed = False
        self.clairview = Clairview("testsecret", host="http://localhost:8000", on_error=self.failed)

    def test_no_api_key(self):
        self.clairview.api_key = None
        self.assertRaises(Exception, self.clairview.capture)

    def test_no_host(self):
        self.clairview.host = None
        self.assertRaises(Exception, self.clairview.capture)

    def test_track(self):
        res = self.clairview.capture("distinct_id", "python module event")
        self._assert_enqueue_result(res)
        self.clairview.flush()

    def test_identify(self):
        res = self.clairview.identify("distinct_id", {"email": "user@email.com"})
        self._assert_enqueue_result(res)
        self.clairview.flush()

    def test_alias(self):
        res = self.clairview.alias("previousId", "distinct_id")
        self._assert_enqueue_result(res)
        self.clairview.flush()

    def test_page(self):
        self.clairview.page("distinct_id", "https://clairview.com/contact")
        self.clairview.flush()

    def test_flush(self):
        self.clairview.flush()
