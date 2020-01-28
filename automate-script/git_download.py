#configs saved on git are copied over to project
#find running project's id and look for the id in git
#each node is looped over and the corresponding config is copied over to the running project

#login into git account

import os
import re
import pexpect
import json

with open("config.json","r") as file:
  configs = json.load(file)
gitFolder = configs['gitFolder']
##change projectName to change location to store the configs of current project
projectName = configs['projectName']
#send curl request to api and grep project id
#open file where project id stored and copy only the id
#copies config stored on server to local machine's git folder
gns3server = configs['gns3server']
servPass = configs['servPass']
gns3serverIP = configs['gns3serverIP']
gns3serverPort = configs['gns3serverPort']
url = "http://"+gns3serverIP+":"+gns3serverPort+"/v2/projects"
savePath = configs['savePath']
os.system("curl "+ url+" | grep project_id > "+savePath+"projectids.txt")
file = open(savePath+'projectids.txt','r')
for line in file:
  projectId = re.search(r'project_id": "(.*?)",', line).group(1)
  nodeUrl = url+"/"+projectId+"/nodes"
  os.system("curl "+ nodeUrl +" | grep node_id > "+savePath+"nodeids.txt")
  fileX = open('nodeids.txt','r')
  for line in fileX:
    nodeId = re.search(r'node_id": "(.*?)",', line).group(1)
    dynNodePath = gns3server+":~/GNS3/projects/"+projectId+"/project-files/dynamips/"+nodeId
    vpcNodePath = gns3server+":~/GNS3/projects/"+projectId+"/project-files/vpcs/"+nodeId
    configFiles = dynNodePath+"/configs/*.cfg"
    vpcScripts = vpcNodePath+"/*.vpc"
    try:
      child = pexpect.spawn('scp ' + gitFolder + projectName + nodeId +'/*.cfg' + ' ' + dynNodePath)
      child.expect(gns3server+"'s password:")
      child.sendline(servPass)
      child.expect(pexpect.EOF, timeout=10)
    except:
      print("Config File not found for node: "+ nodeId)
    try:
      child = pexpect.spawn('scp '+ gitFolder + projectName + nodeId + '/*.vpc' + ' ' + vpcNodePath)
      child.expect(gns3server+"'s password:")
      child.sendline(servPass)
      child.expect(pexpect.EOF, timeout=10)
    except:
      print("VPC Script File not found for node: " + nodeId)
