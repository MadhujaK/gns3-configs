'''save configs from folder structure to git folder
add to the repo
commit to repo
don't push
get project and node id from api'''
import os
import re
import pexpect

gitFolder = "/home/user/myrepos/gns3-configs/"
##change projectName to change location to store the configs of current project
projectName = "instructorlab/lab1/"
#send curl request to api and grep project id
#open file where project id stored and copy only the id
#copies config stored on server to local machine's git folder
gns3server = "server@172.30.31.159:"
servPass = "reves!3"
gns3serverIP = "172.30.31.159"
gns3serverPort = "3080"
url = "http://"+gns3serverIP+":"+gns3serverPort+"/v2/projects"
os.system("curl "+ url+" | grep project_id > /home/user/myrepos/gns3-configs/automate-script/projectids.txt")
file = open('projectids.txt','r')
for line in file:
  countNodes=0
  projectId = re.search(r'project_id": "(.*?)",', line).group(1)
  nodeUrl = url+"/"+projectId+"/nodes"
  os.system("curl "+ nodeUrl +" | grep node_id > /home/user/myrepos/gns3-configs/automate-script/nodeids.txt")
  fileX = open('nodeids.txt','r')
  for line in fileX:
    nodeId = re.search(r'node_id": "(.*?)",', line).group(1)
    configFiles = gns3server+"home/user/GNS3/projects/"+projectId+"/project-files/dynamips/"+nodeId+"/configs/*.cfg"
    #os.system('scp '+ configFiles + " " + gitFolder + projectName + nodeId)
    try:
      child = pexpect.spawn('scp '+ configFiles + ' ' + gitFolder + projectName)
      child.expect(gns3server+"'s password:")
      child.sendline(servPass)
      child.expect(pexpect.EOF, timeout=10)
    except:
      print("File for node: "+nodeId+" not found..Continuing..")
#now locally add it to git repo
#commit
os.system('cd '+gitFolder)
os.system('git add .')
os.system('git commit -m "Regular Commit"')
