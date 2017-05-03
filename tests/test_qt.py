
from unittest import TestCase

from labelImg import get_main_app


class TestMainWindow(TestCase):

    app = None
    win = None

    def setUp(self):
        self.app, self.win = get_main_app()

    def tearDown(self):
        self.win.close()
        self.app.quit()

    def test_noop(self):
        pass
