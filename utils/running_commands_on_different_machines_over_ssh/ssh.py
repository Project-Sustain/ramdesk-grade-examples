import paramiko
import time


class SSH:
    # This class allows you to run commands on a different machine over SSH
    # It supports passwordless login with SSH keys if pwd is None
    # You can start a long-running command with "execute_command"
    # Then you can send input to it with "send" and read output with "recv"
    # You can also send Ctrl-C and Ctrl-D signals with "ctrl_c" and "ctrl_d"
    # Finally, you can close the connection with "stop"
    # Feel free to use this class as is or modify it to suit your needs

    def __init__(self,
                 host: str,
                 user: str | None = None,
                 pwd: str | None = None,
                 command: str | None = None,
                 cwd: str | None = None,
                 modules: list[str] = [],
                 reset_output_before_commands: bool = False) -> None:
        # Initialize the SSH connection
        # Supports passwordless login with SSH keys if pwd is None
        self.reset_output_before_commands = reset_output_before_commands
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=user, password=pwd)
        self.channel = None
        self.modules = modules
        self.cwd = cwd

        if command:
            self.execute_command(command)

    def execute_command(self, command: str) -> None:
        # Execute a command on the remote machine
        # For example start a long-running command like a Java server
        cmds = []
        if self.modules:
            cmds.append('. /etc/profile &> /dev/null')
            cmds.append('module purge')
            for module in self.modules:
                cmds.append(f'module load {module}')
        if self.cwd:
            cmds.append(f'cd {self.cwd}')
        cmds.append(command)
        command = ' && '.join(cmds)
        try:
            transport = self.client.get_transport()
            self.channel = transport.open_session()
            self.channel.exec_command(command)
        except Exception as e:
            raise Exception(f"Failed to execute command: {str(e)}")

    def send(self, msg: str, sleep: float = 0.0) -> None:
        # Send a message to the remote command that you have already started with "execute_command"
        if self.reset_output_before_commands:
            self.recv()
        try:
            if self.channel:
                self.channel.send(msg + '\n')
        except Exception:
            pass
        self.sleep(sleep)

    def recv(self, sleep: float = 0.0) -> str:
        # Read output from the remote command that you have already started with "execute_command"
        self.sleep(sleep)
        output = ''
        try:
            if self.channel.recv_ready():
                data = self.channel.recv(9999)
                if data:
                    output += data.decode('utf-8')
            if self.channel.recv_stderr_ready():
                data = self.channel.recv_stderr(9999)
                if data:
                    output += data.decode('utf-8')
            return output
        except Exception:
            return output

    def get_exit_code(self) -> int | None:
        # Return the exit status of the last command if it has finished
        try:
            if self.channel and self.channel.exit_status_ready():
                return self.channel.recv_exit_status()
            return None
        except Exception:
            return None

    def ctrl_c(self) -> None:
        # Send interrupt (Ctrl-C)
        try:
            if self.channel:
                self.channel.send('\x03')
        except Exception:
            pass

    def ctrl_d(self) -> None:
        # Send EOF (Ctrl-D)
        try:
            if self.channel:
                self.channel.send('\x04')
        except Exception:
            pass

    def stop(self) -> None:
        # Close the channel and client connection
        try:
            if self.channel:
                self.channel.close()
        except Exception:
            pass
        try:
            if self.client:
                self.client.close()
        except Exception:
            pass

    def sleep(self, duration: float = 1.0) -> None:
        # Sleep for a specified duration
        time.sleep(duration)


# Example usage:
# Connect to the denver machine as user 'cs250' using SSH keys
ssh = SSH('denver.cs.colostate.edu', user='cs250')

# Start a long-running Java server command
ssh.execute_command('java -jar /path/to/your/server.jar')

# Send commands to the server and read output
ssh.send('list nodes')
ssh.sleep(2)
output = ssh.recv()
print(output)
