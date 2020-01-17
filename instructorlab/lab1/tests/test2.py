##Ping test PC1 to PC2
import os
import json
import pexpect
import sys
import time

nodeData = {}
#get telnet ip and port for nodes
gns3serverIP = "172.30.31.159"
gns3serverPort = "3080"
consolePass = 'ciscoconpass'
projectId="df1c34dc-75f9-43a1-a35d-90394fded704"
url = "http://"+gns3serverIP+":"+gns3serverPort+"/v2/projects/"+projectId+"/nodes"
os.system('curl '+url +'> node.json')
with open("node.json","r") as jsonFile:
  nodeData = json.load(jsonFile)
for node in nodeData:
  if(node['node_type']=="dynamips"):
    console_type = node['console_type']
    console = node['console']
child = pexpect.spawn(console_type+" "+gns3serverIP+" "+str(console))
try:
  time.sleep(6)
  child.send('\n')
  child.send('\n')
  time.sleep(6)
  #child.expect('[pP]+: ')
  child.expect('Password: ')
  print("Passed first breakpoint")
except:
  print("Error on first breakpoint")
try:
  child.sendline(consolePass)
  child.expect('R1#')
  print("Passed second breakpoint")
except:
  print("Error on second breakpoint")
try:
  child.sendline('sh ip int brief')
  child.expect('R1#')
  print(child.before)
  print("Passed third breakpoint")
except:
  print("Error on third breakpoint")
try:
  child.close()
  #output = str(output).split("\\r\\n")
  #if "bytes from" in output[3]:
  #  print('ping successful')
except Exception as ex:
  print('test failed: '+str(ex))
