"""
Sample tests
"""

from django.test import SimpleTestCase

from app import calc_func


class CalcTest(SimpleTestCase):
    """test calc module"""

    def test_add_numbers(self):
        """test adding numbers together"""
        res = calc_func.sum(5, 6)
        self.assertEqual(res, 11)
