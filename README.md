Automate the installation of HDP Hortonworks Ambari Clusters 

### Technology used
Python - To automate the process
Ambari Blueprint - To automate the Hadoop cluster installation

### About the files
There are two main python files and 5 other configuration files. 

1. The `automate_agent.py` is to automate the installation of the ambari agent and must be ran in the agent VM. 
2. The `automate_server.py` is to automate the installation of the ambari server and must be ran in the server VM.
3. The `config.json` must have the FQDNs of the server and the agents.
4. The `cluster_configuration.json` must have the components of the hadoop eco system that are needed to be installed.

### Steps to run on the Server

1. Edit the `config.json` and mention the server and the agents
2. Edit the `hostmapping.json` and mention the server and the agents
3. Edit the `cluster_configuration.json` and mention the components of the hadoop ecoystem needed.
4. Run `sudo python automate_server.py`

### Steps to run on the Agent

1. Edit the `config.json` and mention the server and the agents
2. Edit the `hostmapping.json` and mention the server and the agents
3. Edit the `cluster_configuration.json` and mention the components of the hadoop ecoystem needed.
4. Run `sudo python automate_agent.py`