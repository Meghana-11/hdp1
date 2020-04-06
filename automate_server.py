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
    call('apt-get install ambari-server -y', shell=True)
    call('apt-get install ambari-agent -y', shell=True)
    call('apt-get install apache2 -y', shell=True)
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
        hdp_version = data['hdp_version']
        namenode_directories = data['namenode_directories']
        datanode_directories = data['datanode_directories']
        cluster_name = data['cluster_name']
        f = open("/etc/ambari-agent/conf/ambari-agent.ini", 'r+') # open file with r+b (allow write and binary mode)  
        f_content = f.read() # read entire content of file into memory
        f_content = re.sub(r'(hostname=localhost)', r'hostname='+ambari_server_host, f_content)  # basically match middle line and replace it with itself and the extra line
        f.seek(0)   # return pointer to top of file so we can re-write the content with replaced string
        f.truncate() # clear file content 
        f.write(f_content)  # re-write the content with the updated content
        f.close()   # close file
        # edit hdputils-repo file
        f = open("./hdputils-repo.json", "r+")
        f_content = f.read()
        f_content = re.sub(r'<ambari-server-fqdn>', ambari_server_host, f_content)
        f.seek(0)
        f.truncate()
        f.write(f_content)
        f.close()
        # edit repo file
        repoName = 'repo'+hdp_version+'.json'
        f = open(repoName, "r+")
        f_content = f.read()
        f_content = re.sub(r'<ambari-server-fqdn>', ambari_server_host, f_content)
        f.seek(0)
        f.truncate()
        f.write(f_content)
        f.close()
        # edit the hostmapping.json
        f = open("./hostmapping.json", "r+")
        f_content = f.read()
        f_content = re.sub(r'<host1-fqdn>',ambari_server_host, f_content)
        f_content = re.sub(r'<host2-fqdn>',ambari_agent_2, f_content)
        f_content = re.sub(r'<host3-fqdn>',ambari_agent_3, f_content)
        f_content = re.sub(r'<cluster-name>',cluster_name, f_content)
        f.seek(0)
        f.truncate()
        f.write(f_content)
        f.close()
        # edit the /etc/hosts
        f = open("/etc/hosts", "a+")
        #f.write("\n" + ambari_server_host_ip + " " + ambari_server_host + "\n")
        f.write(ambari_agent_1_ip + " " + ambari_agent_1 + "\n")
        f.write(ambari_agent_2_ip + " " + ambari_agent_2 + "\n")
        f.write(ambari_agent_3_ip + " " + ambari_agent_3 + "\n")
        f.close()
        # edit the cluster_configurations to add the directories 
        namenode_dir_list = ""
        datanode_dir_list = ""
        for index, directory in enumerate(namenode_directories):
            if index == len(namenode_directories)-1:
                namenode_dir_list+=str(directory)
            else:
                directory= str(directory) + ","
                namenode_dir_list+=directory    
        for index, directory in enumerate(datanode_directories):
            if index == len(datanode_directories)-1:
                datanode_dir_list+=str(directory)
            else:
                directory= str(directory) + ","
                datanode_dir_list+=directory 
        # edit the cluster_configuration.json
        cluster_config_file = "./cluster_configuration"+hdp_version+".json"
        f = open(cluster_config_file, "r+")
        f_content = f.read()
        f_content = re.sub(r'<namenode-directories>', namenode_dir_list, f_content)
        f_content = re.sub(r'<datanode-directories>', datanode_dir_list, f_content)
        f_content = re.sub(r'<cluster-name>', cluster_name, f_content)
        f.seek(0)
        f.truncate()
        f.write(f_content)
        f.close()
        

# run setup in silent mode
def ambari_server_setup():
    call('ambari-server setup -s', shell=True)
    
#start the agent and server
def ambari_server_agent_start():
    call('ambari-server start', shell=True)
    call('ambari-agent start', shell=True)

def download_hdp_and_hdp_utils():
    import wget
    with open('./config.json') as f:
        data = json.load(f)
        hdp_version = data['hdp_version']
        if hdp_version == '3.1':
            # download the HDP tar files
            url = "http://public-repo-1.hortonworks.com/HDP/ubuntu16/3.x/updates/3.1.0.0/HDP-3.1.0.0-ubuntu16-deb.tar.gz"
            wget.download(url, '/var/www/html/')
            url = "http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.22/repos/ubuntu16/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz"
            wget.download(url, '/var/www/html/')
            # extract files
            call('tar xvf /var/www/html/HDP-3.1.0.0-ubuntu16-deb.tar.gz -C /var/www/html/', shell=True)
            call('tar xvf /var/www/html/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz -C /var/www/html/', shell=True)
            # remove the tar files
            os.remove('/var/www/html/HDP-3.1.0.0-ubuntu16-deb.tar.gz')
            os.remove('/var/www/html/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz')
        else:
            # download the HDP tar files
            url = "http://public-repo-1.hortonworks.com/HDP/ubuntu16/2.x/updates/2.6.5.0/HDP-2.6.5.0-ubuntu16-deb.tar.gz"
            wget.download(url, '/var/www/html/')
            url = "http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.22/repos/ubuntu16/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz"
            wget.download(url, '/var/www/html/')
            # extract files
            call('tar xvf /var/www/html/HDP-2.6.5.0-ubuntu16-deb.tar.gz -C /var/www/html/', shell=True)
            call('tar xvf /var/www/html/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz -C /var/www/html/', shell=True)
            # remove the tar files
            os.remove('/var/www/html/HDP-2.6.5.0-ubuntu16-deb.tar.gz')
            os.remove('/var/www/html/HDP-UTILS-1.1.0.22-ubuntu16.tar.gz')
       

def register_setup_start_installation():
    with open('./config.json') as f:
        data = json.load(f)
        ambari_server_host = data['ambari_server_host']
        hdp_version = data['hdp_version']
        cluster_name = data['cluster_name']
        # register blueprint
        command = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin http://'+ ambari_server_host + ':8080/api/v1/blueprints/'+cluster_name+' -d @cluster_configuration'+hdp_version+'.json'
        call(command, shell=True)
        # setup HDP Repository
        command =  'curl -H "X-Requested-By: ambari" -X PUT -u admin:admin http://'+ ambari_server_host + ':8080/api/v1/stacks/HDP/versions/'+hdp_version+'/operating_systems/ubuntu16/repositories/HDP-'+hdp_version+' -d @repo'+hdp_version+'.json'
        call(command, shell=True)
        # setup HDP-UTILS Repository
        command = 'curl -H "X-Requested-By: ambari" -X PUT -u admin:admin http://'+ ambari_server_host + ':8080/api/v1/stacks/HDP-UTILS/versions/'+hdp_version+'/operating_systems/ubuntu16/repositories/HDP-UTILS-1.1.0.22 -d @hdputils-repo.json'
        call(command, shell=True)
        # start installation
        command = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin http://'+ ambari_server_host +':8080/api/v1/clusters/'+cluster_name+' -d @hostmapping.json'
        call(command, shell=True)
       
# prerequisites()
# download_ambari_repo()
# ambari_installation_function()
edit_ambari_config()
ambari_server_setup()
ambari_server_agent_start()
# download_hdp_and_hdp_utils()
register_setup_start_installation()


