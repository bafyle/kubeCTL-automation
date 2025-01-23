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
All configurations explained nicely in the constatns.py file.

## Limitations
This tool is developed for Windows OS and will not work properly with other OSs, especially the detection of the process using a port.
