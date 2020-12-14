from paramiko import SSHClient, AutoAddPolicy

class SSH():
    def __init__(self, server):
        self.host = server.get('hostname')
        self.port = 22
        self.user = server.get('user')
        self.password = server.get('password')
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
    
    
    def exec_command(self, command, session):
        user = session.get('current_os_user')
        dir = session.get('current_dir')

        self._connect()
        one_line_cmd = f'cd {dir}; {command}; echo "<delimiter>"; whoami; echo "<delimiter>"; pwd'

        stdin, stdout, stderr = self.ssh.exec_command(one_line_cmd)
        str_stdout = ''.join(stdout.readlines())
        str_stderr = ''.join(stderr.readlines())
        self._close()

        if str_stderr != '':
            return str_stderr
        else:
            response = str_stdout.split('<delimiter>')[0]
            current_user = str_stdout.split('<delimiter>')[1].replace('\n' , '')
            current_dir = str_stdout.split('<delimiter>')[2].replace('\n' , '')
            return_obj = {
                "response": response,
                "current_user": current_user,
                "current_dir": current_dir
            }
            return return_obj
    
    def _connect(self):
        self.ssh.connect(
            hostname=self.host, port=self.port, username=self.user, password=self.password
        )

    def _close(self):
        self.ssh.close()
    