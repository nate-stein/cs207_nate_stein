"""
Unit Tests: chemkin
"""

import unittest

import chemkin


class TestProgressRate(unittest.TestCase):
    """ Tests progress_rate() function under various circumstances. """

    def test_unequal_dim_args (self):
        """ Ensures func raises ValueError with unequally-dimensioned args. """
        x = [1.0, 2.0, 3.0]
        v = [2.0, 1.0]
        k = 10

        try:
            rate = chemkin.progress_rate(x, v, k)
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail('Expected ValueError but caught different exception.')
            else:
                pass
        else:
            self.fail('No exception raised even though args unequally-dimensioned.')

    def test_x_not_seq (self):
        """ Ensures that TypeError is raised when x is not a sequence. """
        x = 1.0
        v = [2.0, 1.0]
        k = 10
        try:
            rate = chemkin.progress_rate(x, v, k)
        except Exception as e:
            if not isinstance(e, TypeError):
                self.fail('Expected TypeError but caught different exception.')
            else:
                pass
        else:
            self.fail('No exception raised even though x not sequence.')


class TestProgressRates(unittest.TestCase):
    """ Tests progress_rates() function under various circumstances. """

    def test_unequal_dim_args (self):
        """ Ensures func raises ValueError when number of rows in stoichiometric
        coefficient matrix is fewer than len(x).
        """
        x = [1.0, 2.0, 1.0]
        v = [[1.0, 2.0], [2.0, 0.0]]
        k = 10

        try:
            rate = chemkin.progress_rates(x, v, k)
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail('Expected ValueError but different exception caught.')
            else:
                pass
        else:
            self.fail('No exception raised even though args unequally-dimensioned.')

    def test_unequal_dim_v_cols (self):
        """ Ensures func raises ValueError when not all of the rows within v share the
        same dimension.
        """
        x = [1.0, 2.0, 1.0]
        # 3rd row has 1 fewer element than other 2 rows.
        v = [[1.0, 2.0], [2.0, 0.0], [0.0]]
        k = 10

        try:
            rate = chemkin.progress_rates(x, v, k)
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail('Expected ValueError but different exception caught.')
            else:
                pass
        else:
            self.fail(
                  'No exception raised even though not all rows within v share same '
                  'dimension.')


class TestReactionRate(unittest.TestCase):
    """ Tests reaction_rate() function under various circumstances. """

    def test_unequal_dim_stoichiometric_coeff (self):
        """ Ensures func raises ValueError when v_react and v_prod do not share the
        same dimensions, both in terms of number of rows and columns.
        """
        x = [1.0, 2.0, 1.0]
        k = 10

        # First test with v_react and v_prod having different number of rows.
        v_react = [[1.0, 0.0], [2.0, 0.0], [0.0, 2.0]]
        v_prod = [[0.0, 1.0], [0.0, 2.0]] # 1 row less than v_react

        try:
            rate = chemkin.reaction_rate(x, v_react, v_prod, k)
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail('Expected ValueError but different exception caught.')
            else:
                pass
        else:
            self.fail(
                  'No exception raised even though v_prod contains fewer rows than '
                  'v_react.')

        # Next test with v_react and v_prod having same number of rows but one of their
        # rows containing fewer elements than the rest.
        v_react = [[1.0, 0.0], [2.0], [0.0, 2.0]] # 2nd row only contains 1 element
        v_prod = [[0.0, 1.0], [0.0, 2.0], [1.0, 0.0]]

        try:
            rate = chemkin.reaction_rate(x, v_react, v_prod, k)
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail('Expected ValueError but different exception caught.')
            else:
                pass
        else:
            self.fail(
                  'No exception raised even though v_react contains fewer elements than '
                  'required in 2nd row.')
