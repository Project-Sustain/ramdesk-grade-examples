import sys
import unittest
import signal
import time
import random
import string
import sol

# This will be populated by the main grade.py script
student_func = None


class TimeoutException(Exception):
    """Custom exception for timeouts."""

    pass


def timeout_handler(signum, frame):
    """Handler to raise an exception on timeout."""
    raise TimeoutException


class Lab3Tests(unittest.TestCase):
    """Test cases for the countPermStr function, organized by category."""

    @classmethod
    def setUpClass(cls):
        """Ensure student function has been loaded before running tests."""
        if not callable(student_func):
            print(
                "Make sure you have defined the function 'countPermStr' in your submission."
            )
            raise unittest.SkipTest("Student function 'countPermStr' not loaded.")

    def _check_return_value(self, result):
        """Helper function to validate return values when expecting integers."""
        if result is None:
            print(
                "Function returned None. Make sure your function has a return statement.",
                flush=True,
            )
            self.fail("Missing return statement")

        if not isinstance(result, int):
            print(
                f"Function returned {type(result).__name__} instead of int. Expected integer return value.",
                flush=True,
            )
            self.fail("Wrong return type")

    # Category 1: Input Validation
    def test_validation_errors(self):
        """Tests if the function correctly raises ValueError for invalid inputs."""
        error_cases = [
            (None, "abc"),  # None string1
            ("abc", None),  # None string2
            ("abc", ""),  # Empty pattern
            ("", ""),  # Both empty
            (None, None),  # Both None
            ("ab", "abc"),  # Pattern longer than text
        ]
        for s1, s2 in error_cases:
            with self.subTest(string1=s1, string2=s2):
                with self.assertRaises(ValueError):
                    student_func(s1, s2)

    # Category 2: Basic Correctness
    def test_basic_functionality(self):
        """Tests basic cases with clear, non-overlapping results."""
        test_cases = [
            ("listen", "silent"),  # Classic anagram match - 1 result
            ("abcdef", "xyz"),  # No matches - different characters
            ("xyzabc", "bac"),  # Single match at end
            ("abcxyz", "cba"),  # Single match at start
            ("a", "a"),  # Single character match
        ]

        for s1, s2 in test_cases:
            with self.subTest(string1=s1, string2=s2):
                self._check_return_value(student_func(s1, s2))
                expected = sol.countPermStr(s1, s2)
                self.assertEqual(student_func(s1, s2), expected)

    # Category 3: Complex Scenarios
    def test_overlapping_and_repeated_chars(self):
        """Tests more complex cases with overlapping matches and repeated characters."""
        test_cases = [
            ("abab", "ab"),  # Overlapping matches: positions 0, 1, 2 = 3 total
            ("aaabaaa", "aaa"),  # Multiple matches with repeated chars
            ("ababa", "aba"),  # Overlapping pattern matches
            ("aabacabaa", "aab"),  # Complex string with single match
            ("zzzyxwzzyx", "xyz"),  # No anagram matches despite same chars
        ]

        for s1, s2 in test_cases:
            with self.subTest(string1=s1, string2=s2):
                self._check_return_value(student_func(s1, s2))
                expected = sol.countPermStr(s1, s2)
                self.assertEqual(student_func(s1, s2), expected)

    # Category 4: Edge & Special Cases
    def test_edge_and_special_cases(self):
        """Tests edge cases and non-alphanumeric characters."""
        test_cases = [
            # ("", "a"),  # Empty string1 - 0 results, no longer valid input
            # ("ab", "abc"),  # Pattern longer than string1 - 0 results, no longer valid input
            ("aAbB", "ab"),  # Case sensitivity - no matches
            ("abAB", "AB"),  # Case sensitivity - uppercase match
            ("a1b$c_a$b1", "$1b"),  # Special characters and numbers
            ("  ", " "),  # Whitespace characters - 2 matches
        ]

        for s1, s2 in test_cases:
            with self.subTest(string1=s1, string2=s2):
                self._check_return_value(student_func(s1, s2))
                expected = sol.countPermStr(s1, s2)
                self.assertEqual(student_func(s1, s2), expected)

    # Category 5: Performance and Stress Test
    def test_performance(self):
        """
        Comprehensive timed test with varied large inputs to verify O(n) performance.
        Includes high-overlap, no-match, and random scenarios.
        """
        # Defines generators for different types of large-scale test cases
        test_case_generators = [
            ("High Overlap", lambda: ("a" * 200_000, "a" * 10_000)),
            ("No Matches", lambda: ("a" * 200_000, "b" * 10_000)),
            (
                "Random Data",
                lambda: (
                    "".join(
                        random.Random(42).choices(string.ascii_lowercase, k=500_000)
                    ),
                    "".join(random.Random(42).choices(string.ascii_lowercase, k=5)),
                ),
            ),
            (
                "Many Small Matches",
                lambda: ("ab" * 100_000, "ba"),
            ),  # Many overlapping matches
            ("Large Pattern", lambda: ("abc" * 100_000, "abc" * 50)),  # Large pattern
            (
                "Worst Case O(n*m)",
                lambda: ("a" * 199_999 + "b", "a" * 10_000),
            ),  # full scan for worst case
        ]

        signal.signal(signal.SIGALRM, timeout_handler)

        for name, generator in test_case_generators:
            with self.subTest(case=name):
                s1, s2 = generator()

                # use running time of reference solution as a baseline
                start_time = time.perf_counter()
                expected_result = sol.countPermStr(s1, s2)
                reference_time = time.perf_counter() - start_time

                # give minimum 10 seconds for timeout
                timeout_limit = max(int(reference_time * 5 + 2), 10)

                print(
                    f"Timeout limit: {timeout_limit}s, Reference time: {reference_time}s, Expected result: {expected_result}",
                    file=sys.stderr,
                )

                signal.alarm(timeout_limit)

                try:
                    student_result = student_func(s1, s2)
                    self._check_return_value(student_result)
                    self.assertEqual(
                        student_result,
                        expected_result,
                        f"Incorrect result on performance test case: {name}",
                    )
                except TimeoutException:
                    self.fail(
                        f"Solution timed out after {timeout_limit} seconds on case: {name}. "
                        "This indicates an inefficient O(n*m) algorithm."
                    )
                finally:
                    signal.alarm(0)
