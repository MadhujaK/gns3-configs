##Ping test PC1 to PC2
import os
import json
import pexpect
import sys

nodeData = {}
#get telnet ip and port for nodes
gns3serverIP = "172.30.31.159"
gns3serverPort = "3080"
projectId="df1c34dc-75f9-43a1-a35d-90394fded704"
url = "http://"+gns3serverIP+":"+gns3serverPort+"/v2/projects/"+projectId+"/nodes"
os.system('curl '+url +'> node.json')
with open("node.json","r") as jsonFile:
  nodeData = json.load(jsonFile)
for node in nodeData:
  if(node['name']=="VPCS1"):
    console_type = node['console_type']
    console = node['console']
child = pexpect.spawn(console_type+" "+gns3serverIP+" "+str(console))
try:
  child.send('\n')
  child.expect('VPCS>')
  child.sendline('ping 192.168.0.3')
  child.expect('VPCS>')
  output = child.before
  output = str(output).split("\\r\\n")
  if "bytes from" in output[3]:
    print('ping successful')
except Exception as ex:
  print('test failed: '+str(ex))
