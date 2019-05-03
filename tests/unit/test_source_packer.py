from unittest import TestCase


class SourcePackerTest(TestCase):
    def test_tor(self):
        print('helllo')
        import pydevd_pycharm
        pydevd_pycharm.settrace('host.docker.internal', port=3758, stdoutToServer=True, stderrToServer=True)
        print('helllo')
        print('helllo')
        self.assertTrue(True)