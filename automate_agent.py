from __future__ import print_function
from subprocess import call
import json
import re
import os


def prerequisites():
    call('apt-get update', shell=True)
    call('apt-get install python-pip -y', shell=True)
    call('pip install wget', shell=True)

def download_ambari_repo():
   import wget
   with open('./config.json') as f:
        data = json.load(f)
        hdp_version = data['hdp_version']
        ambari_version = "2.6.2.0"
        if hdp_version == "3.1":
            ambari_version = "2.7.3.0"
        url = "http://public-repo-1.hortonworks.com/ambari/ubuntu16/2.x/updates/"+ambari_version+"/ambari.list"
        wget.download(url, '/etc/apt/sources.list.d/')
        call('apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 B9733A7A07513CAD', shell=True)
        call('apt-get update', shell=True)

# run the commands to install packages
def ambari_installation_function():
    call('apt-get install ambari-agent -y', shell=True)
    call('unset http_proxy', shell=True)
    call('unset https_proxy', shell=True)

def edit_ambari_config():
    with open('./config.json') as f:
        data = json.load(f)
        ambari_server_host = data['ambari_server_host']
        ambari_server_host_ip = data['ambari_server_host_ip']
        ambari_agent_1 = data['ambari_agent_1']
        ambari_agent_1_ip = data['ambari_agent_1_ip']
        ambari_agent_2 = data['ambari_agent_2']
        ambari_agent_2_ip = data['ambari_agent_2_ip']
        ambari_agent_3 = data['ambari_agent_3']
        ambari_agent_3_ip = data['ambari_agent_3_ip']
        f = open("/etc/ambari-agent/conf/ambari-agent.ini", 'r+') # open file with r+b (allow write and binary mode)  
        f_content = f.read() # read entire content of file into memory
        f_content = re.sub(r'(hostname=localhost)', r'hostname='+ambari_server_host, f_content)  # basically match middle line and replace it with itself and the extra line
        f.seek(0)   # return pointer to top of file so we can re-write the content with replaced string
        f.truncate() # clear file content 
        f.write(f_content)  # re-write the content with the updated content
        f.close()   # close file
        # edit the /etc/hosts
        f = open("/etc/hosts", "a+")
        f.write("\n" + ambari_server_host_ip + " " + ambari_server_host + "\n")
        f.write(ambari_agent_1_ip + " " + ambari_agent_1 + "\n")
        f.write(ambari_agent_2_ip + " " + ambari_agent_2 + "\n")
        f.write(ambari_agent_3_ip + " " + ambari_agent_3 + "\n")
        f.close
        dirName = '/hdptest/data01/data'
        try:
            # Create target Directory
            os.makedirs(dirName)  
        except OSError as error:
            print(error)
        dirName = '/hdptest/data02/data'
        try:
            # Create target Directory
            os.makedirs(dirName) 
        except FileExistsError:
            print(error)
        
#start the agent and server
def ambari_agent_start():
    call('ambari-agent start', shell=True)

# prerequisites()
# download_ambari_repo()
# ambari_installation_function()
edit_ambari_config()
ambari_agent_start()
