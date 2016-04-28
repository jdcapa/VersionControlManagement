# VersionControlManagement – vcm
This is a Python script managing local version-controlled repositories.
It currently works for GIT and SVN.
The main goal was to have the dot-folders centralised at a common place
 (default: `HOME/.VersionControl/`) and have a small YAML database of
 existing projects.
The script can move a local dot_folder and create a symlink in its stead as
 well as write and obtain details from a database file
 `($HOME/.VersionControl/projects.yaml).`

Install
=======

Requirements: pyyaml

Just copy the vcm script to a folder contained in your ```$PATH``` environment
 variable.

Example
=======

For example, if we want to add a git project shared on Github to the database file
 and move the .git folder (creating a .git symlink to the actual folder):

 ```bash
 $ vcm -g -m
 ```
This will try to locate a .git (or .svn) folder in the **current directory**
 and move it.


Usage
=====

```Text
vcm [-h] [-m] [-g] [-p PROJECT_NAME] [-vc VC_SYSTEM] [-pa PATH]
           [-sa SERVER_ADDRESS] [-u USER_NAME] [-i IDENTIFIER]

This is a management program for svn or git version-controlled projects.

optional arguments:
  -h, --help            show this help message and exit
  -m, --move            Moves the dotFolder (.svn or .git to
                        /home/kettner/.VersionControl and creates a symlink in its stead.
  -g, --git-hub         Is this on github?
  -p PROJECT_NAME, --project PROJECT_NAME
                        Custom project name [default: root folder name]
  -vc VC_SYSTEM, --version-control VC_SYSTEM
                        Version Control system [default: git]
  -pa PATH, --path PATH
                        Directory path [default: current directory]
  -sa SERVER_ADDRESS, --server-address SERVER_ADDRESS
                        Git or Svn server address
  -u USER_NAME, --user-name USER_NAME
                        User name for the git or svn server
  -i IDENTIFIER, --identifier IDENTIFIER
                        Internal database identifier, e.g. projectname-git
```
