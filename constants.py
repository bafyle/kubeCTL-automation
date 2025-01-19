from model.namespace import Namespace
from model.quick_deployment import QuickDeployment
"""
Static namespaces name set by the user
here you can put your namespaces that you usually use
"""
namespace_name1 = "namespace_name1"
namespace_name2 = "namespace_name2"

"""
Here you create new Namespace instances with its name, description and the path for its config file
"""
namespace_instance1 = Namespace(namespace_name1, "namespace1 description", r"C:\Users\<your username>\.kube\config")
namespace_instance2 = Namespace(namespace_name2, "namespace2 description", r"C:\Users\<your username>\.kube\config")

"""
All namespaces in a dictionary (HashMap) to be viewed in the console
Add or remove namespace instances created to the dictionary here to be viewed for the user and select them with their number
"""
NAMESPACES = {
    1: namespace_instance1,
    2: namespace_instance2
}
"""
Quick deployments dictionary here is used to quickly port-forward to well defined deployment, such as database
each namespace can have list of quick deployment instances (notice the square brackets, it means this is a list or array)
The code in main.py file will prompt the user to select one of the quick deployment in the list for the chosen namespace.
if only one item in the list, then it will be selected automatically by the code and proceed with port-forward

The QuickDeployment class has 3 mandatory parameters and 1 optional
1- resource name. A String containing a resource that a will be quickly used to port-forward to
    format: deploy/<deployment name>
2- description. A string which will be viewed to the user to know what is this deployment for
    it will only showed when more then one item in the list
3- local machine port
4- pod port: if not provided, then local machine port will be used
"""
QUICK_DEPLOYMENTS = {
    namespace_name1: [
            QuickDeployment("deploy/example", "description", 1521, 1521),  QuickDeployment("deploy/example2", "description2", 1234, 1234)
        ],
    namespace_name1: [
            QuickDeployment("deploy/example3", "description3", 4556, 4556)
        ],
}

"""
The executable file that will run and open the log file when getting the logs.
the default is Visual Studio code (code)
When providing your text editor, please put in the full path. e.g: C:/path/to/editor.exe
"""
TEXT_EDITOR_COMMAND = "code"

LOGFILE_NAME = "logfile.log"