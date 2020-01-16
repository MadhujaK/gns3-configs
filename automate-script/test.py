import pexpect
import time
child = pexpect.spawn('scp server@172.30.31.159:~/gns3-server/Dockerfile .')
child.expect("server@172.30.31.159's password:")
child.sendline('reves!3')
child.expect(pexpect.EOF, timeout=10)
