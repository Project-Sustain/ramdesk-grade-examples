import subprocess


# run a simple command and print the output
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# check the return code
if result.returncode == 0:
    print('Command succeeded')
else:
    print('Command failed')

# run a command using a shell, this allows shell features like globbing and pipes
result = subprocess.run('ls -l | grep py', shell=True,
                        capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# run a command and raise an exception if it fails
try:
    result = subprocess.run(['false'], check=True,
                            capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    print(f'Command failed with return code {e.returncode}')
    print(e.output)
    print(e.stderr)
else:
    print('Command succeeded')

# run a command with a timeout in seconds
try:
    result = subprocess.run(['sleep', '5'], timeout=2)
except subprocess.TimeoutExpired as e:
    print('Command timed out after 2 seconds')
