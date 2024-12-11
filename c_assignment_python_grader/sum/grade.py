import random
import sys
import subprocess

print('grader started')

# the path to the student submission is the first argument
submission_path = sys.argv[1]

# generate 2 random integers
first = random.randrange(0, 100)
second = random.randrange(0, 100)
tot = first + second

print('first:', first)
print('second:', second)
print('sum:', tot)

print('compiling student submission')
result = subprocess.run(['gcc', submission_path, '-o',
                        'submission'], capture_output=True, text=True)
if result.returncode != 0:
    print('compilation error!')
    print(result.stdout)
    print(result.stderr)
    print(0)
    sys.exit(0)

print('running student submission')
result = subprocess.run(['./submission', str(first), str(second)],
                        capture_output=True, text=True, check=True)

print('student submission output:', result.stdout)

if result.stdout.strip() == str(tot):
    print('success!')
    print(10)  # 10 points awarded
else:
    print('error!')
    print(0)  # 0 points awarded
