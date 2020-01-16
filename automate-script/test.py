import pexpect

gitFolder = "/home/user/myrepos/gns3-configs/"
##change projectName to change location to store the configs of current project
projectName = "instructorlab/lab1/"
projectId = "df1c34dc-75f9-43a1-a35d-90394fded704"
nodeId = "81a8c118-de2c-44ef-9f02-603317064df0"
gns3server = "server@172.30.31.159"
configFiles = gns3server+":~/GNS3/projects/"+projectId+"/project-files/dynamips/"+nodeId+"/configs/*.cfg"
child = pexpect.spawn('scp '+ configFiles + ' ' + gitFolder + projectName)
#child.expect(gns3server+"'s password:")
child.interact()
#child.sendline('reves!3')
#child.expect(pexpect.EOF, timeout=10)
#child = pexpect.spawn('scp server@172.30.31.159:~/gns3-server/Dockerfile .')
#child.expect("server@172.30.31.159's password:")
#child.sendline('reves!3')
#child.expect(pexpect.EOF, timeout=10)
