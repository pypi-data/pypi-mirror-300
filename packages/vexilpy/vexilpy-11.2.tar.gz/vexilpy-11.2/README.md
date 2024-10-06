# Welcome to VexilPy
### This documentation including its installation guide may only be applicable to VexilPy v11

**Documentation for VexilPy**

VexilPy is a Python-based framework designed to simplify the development and management of web applications.
It provides a set of tools and utilities to streamline the development process,
enhance security, and improve performance.

**Installation**

To install VexilPy, you can use either pip or git.

***Recommended*** | Install VexilPy v11 using pip:
```commandline
pip install vexilpy
```

*Updated in v11* | Download source code for VexilPy 11 using:
```commandline
git clone https://github.com/elemenom/vexilpy.git
```

**Download Source Code

**Upgrade**

*Updated in v11* | To upgrade VexilPy, you can use either pip or git.

*Updated in v11* | Using pip:
```commandline
pip install vexilpy --upgrade
```

*Updated in v11* | Using git:
```commandline
rm -rf vexilpy

git clone https://github.com/elemenom/vexilpy.git
```

**Links**

*Updated in v11* | - GitHub: https://github.com/elemenom/vexilpy/
*Updated in v11* | - PyPI: https://pypi.org/project/vexilpy/

**Author**

- Name: Elekk aka Elemenom
- Username: elemenom
- Mail: pixilreal@gmail.com
- GitHub: https://github.com/elemenom/
- PyPI: https://pypi.org/user/elemenom/

**Command-Line Interface (CLI) Usage**

VexilPy provides a command-line interface (CLI) to perform various tasks such as running the application, cleaning pycache files, and running processes directly from the CLI.

To use the CLI, you can run the following commands:

*Updated in v11* | - Run the application with GUI:
```commandline
python -m vexilpy --RunGui
```

*Updated in v11* | - Clean pycache files:
```commandline
python -m vexilpy --Clean
```

*Updated in v11* | - Run a process directly from the CLI:
```commandline
python -m vexilpy --Run-Process "<process_command>"
```

**VexilPy Configuration**

VexilPy supports configuration in YAML.

*Updated in v11* | - To link a .yaml file, run your file like this:
```commandline
python main.py -F vexilconfig.yaml
```
or
```commandline
python main.py --File vexilconfig.yaml
```

*Updated in v11* | If you don't provide a vexilconfig file, VexilPy will automatically create (if needed) and use `vexilconfig.yaml`.
A warning will be logged if the file has to be created.

```log
WARNING | No vexilconfig.yaml file found. Creating a new one.
```

**Important Note**

Please note that the `backendutils` directory is not intended to be accessed directly. It contains internal utilities and modules used by VexilPy. Any code within this directory should not be modified or accessed directly.