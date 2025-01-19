# KubeCTL Command Automation Tool
This tool automates the KubeCTL commands by using the numbers in you keyboard. It ease some of the frequent and tedious commands you write in your as a developer

## Tool features
The tool can do the following:
- Port-forward to pod in kubernates cluster
- Quick port-forward for ease of access to predefined resources such as databases.
- Ability to reconnect the port-forward if the connection is lost
- Ability to detect the port in which the pod is deployed with and use this port as local machine port for port-forward
- Ability to detect which process is using a local port
- Retrieve and view the logs of a pod
- View some details about the deployments and pods in the cluster

## Requirements
- Windows OS
- Python 3.9+

## Installation and How to Use

### Installation
- Clone this repo using git
- Configure you namespaces, config files paths, quick deployments, and your text editor from constants.py file
- Run main.py

### How to use
Once configured (see [Configurations](#configurations) section) and run, you will be using the numbers to selection of the actions available to you in the command prompt.

For example, you have a database deployment called "postgres-dev" on namespace called "dev". And you set this namespace to be the first one in your "NAMESPACES" dictionary in constants.py. And you set a quick deployment with the namespace mentioned and with the database deployment name. Then you only need to enter 1 in namespaces list and enter 1 in the actions list to connect to the database.

## Configurations
All configurations explained nicely in the constatns.py file.

## Limitations
This tool is developed for Windows OS and it will not work properly with other OSs. Especially the detection of the process that uses a port.