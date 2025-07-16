import unittest
from math_utils import multiply #import the function you are testing
from parameterized import parameterized

class TestMultiplyFunction(unittest.TestCase):
    @parameterized.expand([
        (2,3,6),
        (0,5,0),
        (-2,-4,8),
        (-3,6,-18),
        (2.5,4,10.0),
        (0.1,0.2,0.02),
        (10000, 10000, 100000000),
    ])
    
    def test_multiplication_cases(self,a,b,expected):
        self.assertAlmostEqual(multiply(a,b),expected)
    
    @parameterized.expand([
        ("string-input","a",2),
        ("both-strings","x","y"),
        ("list-mult",[1,2],3),
    ])
    
    def test_invalid_types(self,name,a,b):
        with self.assertRaises(TypeError):
            multiply(a,b)

if __name__ == '__main__':
    unittest.main()
    
 