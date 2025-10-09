import os
import sys
import unittest
import importlib.util
import pycodestyle
import time

import tests

# --- CONFIGURATION ---
TOTAL_SCORE = 45
PEP8_POINTS = 5

# Points and hints are allocated per test category
# Format: { 'Category Name': (Points, 'test_function_name', 'Hint for students') }
TEST_CATEGORIES = {
    "Input Validation": (
        5,
        "test_validation_errors",
        "Hint: Does your function raise a ValueError when appropriate?",
    ),
    "Basic Correctness": (
        5,
        "test_basic_functionality",
        "Hint: Does your function work for simple, non-overlapping cases?",
    ),
    "Complex Scenarios": (
        5,
        "test_overlapping_and_repeated_chars",
        "Hint: Does your function work for overlapping patterns or strings with many repeated characters?",
    ),
    "Edge & Special Cases": (
        5,
        "test_edge_and_special_cases",
        "Hint: Does your function consider edge cases like empty search strings, case sensitivity, or special characters?",
    ),
    "Performance and Stress Test": (
        20,
        "test_performance",
        "Hint: Your solution is too slow on large inputs. Make sure you are using an efficient algorithm that runs in linear time.",
    ),
}
# ---


def load_student_function(path):
    """Loads the 'countPermStr' function from a student's submission file."""
    try:
        spec = importlib.util.spec_from_file_location("solution", path)
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        return student_module.countPermStr
    except AttributeError:
        print(f"The required function 'countPermStr' was not found in the submission.")
        return None
    except FileNotFoundError:
        print(f"The file was not found at {path}")
        return None
    except SyntaxError:
        print(f"Syntax error in the submission.")
        return None
    except Exception as e:
        print(f"Error loading student module: {e}")
        return None


def check_pep8_compliance(path):
    """Checks PEP8 style and prints feedback to stdout."""
    print("\n--- Running PEP8 Style Check ---", flush=True)
    style_guide = pycodestyle.StyleGuide(
        quiet=False,
        ignore=['W291', 'W293'],  # ignore whitespace errors from tox.ini
        max_line_length=100       # max-line-length from tox.ini
    )
    report = style_guide.check_files([path])
    if report.total_errors == 0:
        print("No PEP8 issues found. Good job!")
        return True
    else:
        print(f"Found {report.total_errors} PEP8 issue(s). Review your code style.")
        try:
            # print only first 3 issues
            with open("pycodestyle_output", "r") as f:
                issues = [line.strip() for line in f if line.strip()]
                issues_to_print = issues[: min(3, len(issues))]
                if len(issues_to_print) < 3:
                    print("Showing all issues found:")
                else:
                    print("Showing the first 3 issues found:")
                print(*issues_to_print, sep="\n", end="\n\n")
        except FileNotFoundError:
            print("Could not read detailed violations from pycodestyle_output file.")

        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python grade.py <path_to_student_solution.py>", file=sys.stderr)
        sys.exit(1)

    # Start total timing
    total_start_time = time.perf_counter()

    student_file_path = sys.argv[1]
    print(
        f"--- Grading Student Submission: {os.path.basename(student_file_path)} ---\n",
        flush=True,
    )

    student_func = load_student_function(student_file_path)

    if student_func is None:
        print(f"Final Score: 0 / {TOTAL_SCORE}")
        print(0)
        return

    tests.student_func = student_func
    total_score = 0

    loader = unittest.TestLoader()
    # detailed test runner output to stderr (only GTA can see this in ramdesk)
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=2)

    for category, (points, test_name, hint) in TEST_CATEGORIES.items():
        # Print category headers to stdout (for students)
        print(f"\n--- Testing Category: {category} ({points} points) ---", flush=True)

        # Time each test category
        category_start_time = time.perf_counter()

        suite = loader.loadTestsFromName(f"tests.Lab3Tests.{test_name}")
        result = runner.run(suite)

        category_end_time = time.perf_counter()
        category_duration = category_end_time - category_start_time

        # Print timing info to stderr for debugging
        print(f"Category '{category}' completed in {category_duration:.4f}s", file=sys.stderr)

        if result.wasSuccessful():
            total_score += points
            print(
                f"Result: PASSED.  Score += {points} (Current Score: {total_score}/{TOTAL_SCORE})"
            )
        else:
            print(
                f"Result: FAILED.  Score += 0 (Current Score: {total_score}/{TOTAL_SCORE})"
            )
            print(hint)  # hint for the student

    # Check PEP8 compliance and print results to stdout
    pep8_start_time = time.perf_counter()
    if check_pep8_compliance(student_file_path):
        total_score += PEP8_POINTS
        pep8_end_time = time.perf_counter()
        pep8_duration = pep8_end_time - pep8_start_time
        print(f"PEP8 check completed in {pep8_duration:.4f}s", file=sys.stderr)
        print(
            f"Result: PASSED.  Score += {PEP8_POINTS} (Current Score: {total_score}/{TOTAL_SCORE})"
        )
    else:
        pep8_end_time = time.perf_counter()
        pep8_duration = pep8_end_time - pep8_start_time
        print(f"PEP8 check completed in {pep8_duration:.4f}s", file=sys.stderr)
        print(
            f"Result: PEP8 compliance check FAILED.  Score += 0 (Current Score: {total_score}/{TOTAL_SCORE})"
        )

    # Calculate total time
    total_end_time = time.perf_counter()
    total_duration = total_end_time - total_start_time
    print(f"Grading completed in {total_duration:.4f}s", file=sys.stderr)

    print("\n---------------------------------")
    print(f"Final Score: {total_score} / {TOTAL_SCORE}")
    print("---------------------------------")

    # score for Canvas
    print(total_score)


if __name__ == "__main__":
    main()
