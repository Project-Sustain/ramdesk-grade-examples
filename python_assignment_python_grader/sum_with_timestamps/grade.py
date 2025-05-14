import random
import sys
import subprocess
import datetime

TOTAL_POINTS = 10

print('grader started')

# the path to the student submission is the first argument
submission_path = sys.argv[1]

try:
    submitted_date = datetime.datetime.fromisoformat(sys.argv[2])
    due_date = datetime.datetime.fromisoformat(sys.argv[3])
    until_date = datetime.datetime.fromisoformat(sys.argv[4])
    
    # make a late penalty that becomes more severe after the due date, as time approaches the until date
    late_penalty = TOTAL_POINTS - TOTAL_POINTS *(until_date - submitted_date).total_seconds() / (until_date - due_date).total_seconds()
    print(f'late penalty: -{late_penalty:.2f} points')
except ValueError:
    late_penalty = 0
    print('due and/or until not found in canvas, no penalty applied')
    
    
# generate 2 random integers
first = random.randrange(0, 100)
second = random.randrange(0, 100)
tot = first + second

print('first:', first)
print('second:', second)
print('sum:', tot)

print('running student submission')
result = subprocess.run(['python3', submission_path, str(
    first), str(second)], capture_output=True, text=True, check=True)

print('student submission output:', result.stdout)

if result.stdout.strip() == str(tot):
    print('success!')
    print(10 - late_penalty)  # dynamically adjust the score based on how late the submission is
else:
    print('error!')
    print(0)  # 0 points awarded
