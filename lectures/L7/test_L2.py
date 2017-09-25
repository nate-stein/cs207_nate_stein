
import L2
ACCEPTABLE_ERR = 0.001

def test_without_weights():
    """ Tests L2() function without a weight vector. """
    v = [1, 3, -5]
    expected = 5.91608
    actual = L2.L2(v)
    assert abs(expected - actual) <= ACCEPTABLE_ERR
    
def test_with_weights():
    """ Tests L2() function with a weight vector. """
    v = [1, 3, -5]
    w = [0.25, 0.25, 0.1]
    expected = 2.5
    actual = L2.L2(v, w)
    assert abs(expected - actual) <= ACCEPTABLE_ERR
    
def test_vector_weights_different_len():
    v = [1, 3, -5]
    w = [0.25, 0.25]
    try:
        result = L2.L2(v, w)
    except Exception as err:
        assert type(err) == TypeError
    else:
        assert 1 == 0