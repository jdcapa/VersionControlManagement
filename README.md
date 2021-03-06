# Version control management – `vcm`
This is a Python script managing local version-controlled repositories.
It currently works for GIT and SVN.
The main goal was to have the dot-folders centralised at a common place
 (default: `$HOME/.vcs_dots/`) and have a small YAML database of
 existing projects.
The script can move a local dot_folder and create a symlink in its stead as
 well as write and obtain details from a database file
 `($HOME/.version_controlled_software/projects.yaml).`

## Install

Requirements: Python3.5 or newer, pyyaml

Just copy the vcm script to a folder contained in your ```$PATH``` environment
 variable.


## Example

For example, if we want to add a git project shared on Github to the database file
 and move the .git folder (creating a .git symlink to the actual folder):

 ```bash
 $ vcm -g -m
 ```
This will try to locate a .git (or .svn) folder in the **current directory**
 and move it.


## Usage

```Text
usage: vcm [-h] [-m] [-md] [-d] [-c] [-g GITREPO] [-p PROJECT_NAME]
           [-vc VC_SYSTEM] [-pa PATH] [-sa SERVER_ADDRESS] [-u USER_NAME]
           [-i IDENTIFIER] [-a ALT_PATHS [ALT_PATHS ...]]

This is a management program for svn or git version-controlled projects.

optional arguments:
  -h, --help            show this help message and exit
  -m, --move            Moves the Folder to a predefined VCS_PATH (defined in
                        $HOME/.config/vcm/config.yaml) and creates a
                        symlink in its stead.
  -md, --move-dot       Moves the dotFolder (.svn or .git to {} and creates a
                        symlink in its stead.
  -d, --delete          Removes the project data from the internal database
                        [Default: False].
  -c, --check           Checks the status of the repository and compares it to
                        the remote origin.
  -g GITREPO, --git-repo GITREPO
                        Is it online? (provide address, e.g. server.gitlab.org
                        or github.com)
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
  -a ALT_PATHS [ALT_PATHS ...], --alt-paths ALT_PATHS [ALT_PATHS ...]
                        Add alternative path roots where symlinks should
                        appear.

```
