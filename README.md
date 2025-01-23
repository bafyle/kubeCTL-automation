# KubeCTL Command Automation Tool
This tool automates the KubeCTL commands by using the numbers on your keyboard. It eases some of the frequent and tedious commands you write in your as a developer

## Tool Features
The tool can do the following:
- Port-forward to pod in Kubernetes cluster
- Quick port-forward for ease of access to predefined resources such as databases.
- Ability to reconnect the port-forward if the connection is lost
- Ability to detect the port in which the pod is deployed and use this port as a local machine port for port-forward
- Ability to detect which process is using a local port
- Retrieve and view the logs of a pod
- View some details about the deployments and pods in the cluster

## Requirements
- Windows OS
- Python 3.9+

## Installation and How to Use

### Installation
- Clone this repo using git
- Configure your namespaces, config file paths, quick deployments, and your text editor from the constants.py file
- Run main.py

### How to use
Once configured (see [Configurations](#configurations) section) and run, you will be using the numbers to select the actions available to you in the command prompt.

For example, you have a database deployment called "postgres-dev" on a namespace called "dev". You set this namespace to be the first one in your "NAMESPACES" dictionary in constants.py. You set a quick deployment with the namespace mentioned and with the database deployment name. Then you only need to enter 1 in the namespaces list and enter 1 in the actions list to connect to the database.

## Configurations
All configurations are in the constants.py file. There are examples configs in the file show how you can set your namespaces, description for the namespace, config file paths, and quick deployment.

- Create a string variable with the namespace name in your Kubernetes cluster in the first section of the file.
- Create a Namespace object instance and parameterize the contractor with the namespace variable created, a description string, and a config file.
- Add the Namespace object instance into the "NAMESPACES" hashmap with an integer as a key. The integer key will be your indicator of how you choose this namespace from the CMD
- If you have a resource you would like to quickly port-forward to it, you can set it in the "QUICK_DEPLOYMENTS" hashmap. The key is the namespace string variable and the value is a list of the QuickDeployment instances. instances can be parameterized with 
    - Resource name (deploy/XYZ)
    - Description
    - Local machine port
    - Resource port (if omitted, the script will use the local machine port)
- If you have a favorite text editor or a program to view the logs other can VSCode, you can put its full path in TEXT_EDITOR_COMMAND constant. Please make sure this program opens the file passed to it as a command parameter. 
- e.g: ```/path/to/your/program.exe logfile.log```
- Finally, the logs will be saved in a file first before running using the command in TEXT_EDITOR_COMMAND. The file will be saved in the same path as where you run main.py. The file name and extension can be configured by changing the LOGFILE_NAME constants.

## Limitations
This tool is developed for Windows OS and will not work properly with other OSs, especially the detection of the process using a port.
