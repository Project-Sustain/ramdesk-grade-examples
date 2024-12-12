import math
import random
import sys
import subprocess


# the path to the student submission is the first argument
submission_path = sys.argv[1]


def test(number):
    factorial = str(math.factorial(number))
    result = subprocess.run(['./submission', str(
        number)], capture_output=True, text=True)
    students_output = result.stdout.strip()

    print('number:', number)
    print('factorial:', factorial)
    print('students output:', students_output)

    if students_output == factorial:
        return 1  # 1 point awarded
    else:
        return 0  # 0 points awarded


def main():
    print('grader started')

    print('compiling student submission')
    result = subprocess.run(['gcc', submission_path, '-o',
                            'submission'], capture_output=True, text=True)
    if result.returncode != 0:
        print('compilation error!')
        print(result.stdout)
        print(result.stderr)
        print(0)
        exit()

    score = 0

    # 10 tests
    for i in range(1, 11):
        print('running test: ', i)
        number = random.randint(1, 10)
        score += test(number)

    print('grader finished')
    # print the final score that will be uploaded to Canvas
    print(score)


if __name__ == '__main__':
    main()
