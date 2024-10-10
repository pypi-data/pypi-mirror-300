import unittest
import swmm

from .data import ORIGINAL_HOTSTART_INPUT_FILE


class TestSwmmOutput(unittest.TestCase):

    def test_version(self):
        swmm.sin(10)

    def test_swmm_output(self):
        swmm.swmm_run(
            ORIGINAL_HOTSTART_INPUT_FILE,
            ORIGINAL_HOTSTART_INPUT_FILE.replace(".inp", '.rpt'),
            ORIGINAL_HOTSTART_INPUT_FILE.replace(".inp", '.out'),
        )

        print("test")
