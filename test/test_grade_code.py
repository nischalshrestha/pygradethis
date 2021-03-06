
import unittest

from pygradethis.grade_code import grade_code

from collections import namedtuple
# convenience tuple for structuring test cases
TestCase = namedtuple("TestCase", ["actual", "expected", "message"])

class GradeCodeTest(unittest.TestCase):

    def test_core(self):
        test_cases = [
            # different literals
            TestCase(
                "\"1\"", "1",
                "I expected 1, but what you wrote was interpreted as \"1\" at line 1."
            ),
            TestCase(
                "1", "\"1\"", 
                "I expected \"1\", but what you wrote was interpreted as 1 at line 1."
            ),
            TestCase(
                "[1]", "\"1\"", 
                "I expected \"1\", but what you wrote was interpreted as [1] at line 1."
            ),
            TestCase(
                "[1]", "\"1\"", 
                "I expected \"1\", but what you wrote was interpreted as [1] at line 1."
            ),
            TestCase(
                "True", "\"1\"", 
                "I expected \"1\", but what you wrote was interpreted as True at line 1."
            ),
            TestCase(
                "False", "\"1\"", 
                "I expected \"1\", but what you wrote was interpreted as False at line 1."
            ),
            # str vs str
            TestCase(
                "\"not hello\"", "\"hello\"", 
                "I expected \"hello\", but what you wrote was interpreted as \"not hello\" at line 1."
            ),
            # list vs list
            TestCase(
                "[2]", "[]", 
                "I did not expect 2 at line 1."
            ),
            TestCase(
                "[1,2]", "[1]", 
                "I did not expect 2 at line 1."
            ),
            TestCase(
                "[1]", "[1,2]", 
                "I expected 2 at line 1."
            ),
            # expr vs something else
            TestCase(
                "1 + 1", "1", 
                "I expected 1, but what you wrote was interpreted as 1 + 1 at line 1."
            ),
            TestCase(
                "1 + (2 + 2)", "1 + (2 + 3)", 
                "I expected 3, but what you wrote was interpreted as 2 in 2 + 2 at line 1."
            ),
            TestCase(
                "-1", "1", 
                "I expected 1, but what you wrote was interpreted as -1 at line 1."
            ),
        ]
        for t in test_cases:
            actual_message = grade_code(t.actual, t.expected)
            self.assertEqual(t.message, actual_message, (
                    "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                        t.actual,
                        t.expected,
                        t.message,
                        actual_message
                    )
                )
            )
    
    def test_functions(self):
        test_cases = [
            TestCase(
                "2 + sum([1,2])", "2 + sum([1,1])", 
                "I expected sum(iterable=[1, 1], start=0), but what you wrote was interpreted as sum(iterable=[1, 2], start=0) at line 1."
            ),
            TestCase(
                "sqrt(log(2))", "sqrt(log(1))", 
                "I expected 1, but what you wrote was interpreted as 2 in log(2) at line 1."
            ),
            TestCase(
                "def foo(a, b=1): pass; foo(2)", "def foo(a, b=1): pass; foo(1)", 
                "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."
            ),
            TestCase(
                "def foo(a, b=1): pass; foo(a=2)", "def foo(a, b=1): pass; foo(1)", 
                "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."
            ),
            TestCase(
                "def foo(a, b=1): pass; foo(a=[2])", "def foo(a, b=1): pass; foo(2, 2)", 
                "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=[2], b=1) at line 1."
            ),
            TestCase(
                "def foo(a, b=1): pass; foo(a=\"2\", b=2)", "def foo(a, b=1): pass; foo(2, 2)", 
                "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=\"2\", b=2) at line 1."
            ),
            TestCase(
                "def head(n=5): pass; head(12)", "def head(n=5): pass; head(n=10)", 
                "I expected head(n=10), but what you wrote was interpreted as head(n=12) at line 1."
            ),
        ]
        for t in test_cases:
            actual_message = grade_code(t.actual, t.expected)
            self.assertEqual(t.message, actual_message, (
                    "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                        t.actual,
                        t.expected,
                        t.message,
                        actual_message
                    )
                )
            )
    
if __name__ == "__main__":
    unittest.main()

