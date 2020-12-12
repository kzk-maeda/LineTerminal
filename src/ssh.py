from paramiko import SSHClient, AutoAddPolicy

class SSH():
    def __init__(self, host, port=22, user='root', password='password'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
    
    
    def exec_command(self, command, user='root', dir='/root'):
        self._connect()
        # one_line_cmd = f'su - {user} && cd {dir} && {command}'
        one_line_cmd = f'{command}'

        stdin, stdout, stderr = self.ssh.exec_command(one_line_cmd)
        str_stdout = ''.join(stdout.readlines())
        str_stderr = ''.join(stderr.readlines())
        self._close()

        if str_stderr != '':
            return str_stderr
        else:
            return str_stdout
    
    def _connect(self):
        self.ssh.connect(
            hostname=self.host, port=self.port, username=self.user, password=self.password
        )

    def _close(self):
        self.ssh.close()
    