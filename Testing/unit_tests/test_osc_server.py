import unittest
from unittest.mock import MagicMock, call
from Utility_Tools.osc_server import OSCBootServer


class TestOSCBootServer(unittest.TestCase):
    def setUp(self):
        self.dispatcher = MagicMock()
        self.osc_server = OSCBootServer('127.0.0.1', 12456, self.dispatcher)

    def test_constructor(self):
        self.assertEqual(self.osc_server.ip_address, '127.0.0.1')
        self.assertEqual(self.osc_server.port, 12456)
        self.assertEqual(self.osc_server.dispatcher, self.dispatcher)
        self.assertFalse(self.osc_server.supercollider_ready)
        self.assertFalse(self.osc_server.processing_ready)

    def test_print_processing_ready(self):
        self.osc_server.print_processing_ready('/some/address', 1, 2, 3)
        self.assertTrue(self.osc_server.processing_ready)
        self.assertTrue(self.osc_server.shut_down.called)

    def test_print_supercollider_ready(self):
        self.osc_server.print_supercollider_ready('/some/address', 1, 2, 3)
        self.assertTrue(self.osc_server.supercollider_ready)
        self.assertTrue(self.osc_server.shut_down.called)

    def test_shut_down(self):
        # When neither processing_ready nor supercollider_ready are True, shut_down() should not do anything
        self.osc_server.shut_down()
        self.assertFalse(self.osc_server.threading_server.shutdown.called)

        # When processing_ready is True but supercollider_ready is False, shut_down() should not do anything
        self.osc_server.processing_ready = True
        self.osc_server.shut_down()
        self.assertFalse(self.osc_server.threading_server.shutdown.called)

        # When supercollider_ready is True but processing_ready is False, shut_down() should not do anything
        self.osc_server.processing_ready = False
        self.osc_server.supercollider_ready = True
        self.osc_server.shut_down()
        self.assertFalse(self.osc_server.threading_server.shutdown.called)

        # When both processing_ready and supercollider_ready are True, shut_down() should call threading_server.shutdown()
        self.osc_server.processing_ready = True
        self.osc_server.supercollider_ready = True
        self.osc_server.shut_down()
        self.assertTrue(self.osc_server.threading_server.shutdown.called)

    def test_handle_request(self):
        self.osc_server.threading_server.handle_request.assert_not_called()
        self.osc_server.handle_request()
        self.osc_server.threading_server.handle_request.assert_called_once()

    def test_serve_forever(self):
        self.osc_server.threading_server.serve_forever.assert_not_called()
        self.osc_server.serve_forever()
        self.osc_server.threading_server.serve_forever.assert_called_once()


if __name__ == '__main__':
    unittest.main()
