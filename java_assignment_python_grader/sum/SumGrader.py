import subprocess
import sys
import random
import os
from functools import reduce

def post_grade(msg: str, grade: float):
    print(msg)
    print(f'{grade:.2f}')
    exit(0)
    
def run_test(num_args: int, dir: str, seed: int = None) -> tuple[bool, str]:
    random.seed(seed)
    args = [str(random.randint(1, 100)) for _ in range(num_args)]
    cmd = ['java', 'Sum']
    cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, cwd=dir)
        if result.returncode != 0:
            return (0, f'Test with {num_args} args failed to run.\n')
        
        correct_sum = reduce(lambda x, y: int(x) + int(y), args, 0)
        if correct_sum == int(result.stdout):
            return (1, f'Test with {num_args} args: PASS\n')
        else:
            return (0, f'Test with {num_args} args: FAIL\n')

    except subprocess.TimeoutExpired:
        return (0, f'Test with {num_args} args timed out when running.\n')
    except TypeError:
        return (0, f'Test with {num_args} returned a non integer.\n')
    

def grade(file_path: str) -> None:
    message = ''
    overall_grade = 0
    
    # compile the submission
    compile_cmd = ['javac', file_path]
    output = subprocess.run(compile_cmd)
    
    if output.returncode != 0:
        message += 'Sum.java did not compile...\n'
        post_grade(message, overall_grade)
    else:
        overall_grade += 1
        message += 'Sum.java compiled successfully\n'
    
    file_dir = os.path.join(os.path.dirname(file_path))
    
    # test 1: 0 args
    test_grade, msg = run_test(0, file_dir)
    overall_grade += test_grade
    message += msg
    
    # test 2: 1 arg
    test_grade, msg = run_test(1, file_dir)
    overall_grade += test_grade
    message += msg
    
    # test 3: 10 args
    test_grade, msg = run_test(10, file_dir, seed=42)
    overall_grade += test_grade
    message += msg
    
    # test 4: random args
    test_grade, msg = run_test(random.randint(10, 25), file_dir)
    overall_grade += test_grade
    message += msg
    
    if overall_grade == 5:
        message += 'Good job!\n'
    post_grade(message, overall_grade)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('The args must contains the file path to the student submission!')

    file_path = list(filter(lambda x: '/Sum.java' in x, sys.argv))[0]
    grade(file_path)