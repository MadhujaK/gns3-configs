'''save configs from folder structure to git folder
add to the repo
commit to repo
don't push
get project and node id from api'''
import os
import re
import pexpect

gitFolder = "~/myrepos/gns3-configs/"
projectName = "instructor-lab/lab1"
#send curl request to api and grep project id
#open file where project id stored and copy only the id
#copies config stored on server to local machine's git folder
gns3server = "server@172.30.31.159:"
servPass = "reves!3"
gns3serverIP = "172.30.31.159"
gns3serverPort = "3080"
url = "http://"+gns3serverIP+":"+gns3serverPort+"/v2/projects"
os.system("curl "+ url+" | grep project_id > projectids.txt")
file = open('projectids.txt','r')
for line in file:
  countNodes=0
  projectId = re.search(r'project_id": "(.*?)",', line).group(1)
  nodeUrl = url+"/"+projectId+"/nodes"
  os.system("curl "+ nodeUrl +" | grep node_id > nodeids.txt")
  fileX = open('nodeids.txt','r')
  for line in fileX:
    nodeId = re.search(r'node_id": "(.*?)",', line).group(1)
    print(nodeId)
    configFiles = gns3server+"~/GNS3/projects/"+projectId+"/project-files/dynamips/"+nodeId+"/configs/*.cfg"
    #os.system('scp '+ configFiles + " " + gitFolder + projectName + nodeId)
    child = pexpect.spawn('scp '+ configFiles + " " + gitFolder + projectName + nodeId)
    child.sendline(servPass)
#now locally add it to git repo
#commit
os.system('cd '+gitFolder)
os.system('git add .')
os.system('git commit -m "Regular Commit"')
