import random
import sys
import subprocess

print('grader started')

# the path to the student submission is the first argument
submission_path = sys.argv[1]

first = random.randrange(0, 100)
second = random.randrange(0, 100)

print('first:', first)
print('second:', second)
print('sum:', first + second)

print('running student submission')
result = subprocess.run(['python3', submission_path, str(first), str(second)], capture_output=True, text=True, check=True)

print('student submission output:', result.stdout)

if result.stdout.strip() == str(first + second):
    print('success!')
    print(10) # 10 points awarded
else:
    print('error!')
    print(0) # 0 points awarded
