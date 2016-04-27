import os
import shutil
import sys
import yaml
import argparse

program_description = """
This is a management program for svn or git version-controlled projects.
"""

GITHUB_USER = 'jdcapa'
HOME = os.path.expanduser("~")
VCM_PATH = os.path.join(HOME, ".VersionControl")
PROJECT_DATA_FN = os.path.join(VCM_PATH, 'projects.yaml')
GITHUB_https = "https://github.com/{}/{}copy"
GITHUB_git = 'git@github.com:{}/{}.git'


# parser set-up
parser = argparse.ArgumentParser(description=program_description)

# parser.add_argument('action',
#                     metavar='vcm action',
#                     type=str, default="innit",
#                     help='Action you want performed [init|move]')

parser.add_argument('-m', "--move",
                    action="store_true",
                    default='',
                    dest="move",
                    help=('Moves the dotFolder (.svn or .git to {} and ' +
                          'creates a symlink in its stead.').format(VCM_PATH))

parser.add_argument('-g', "--git-hub",
                    action="store_true",
                    default=False,
                    dest="use_github",
                    help='Is this on github?')

parser.add_argument('-p', "--project",
                    action='store',
                    type=str, default="",
                    dest="project_name",
                    help='Custom project name [default: root folder name]')

parser.add_argument('-vc', "--version-control",
                    action='store',
                    type=str, default="git",
                    dest='vc_system',
                    help='Version Control system [default: git]')

parser.add_argument('-pa', "--path",
                    action='store',
                    type=str, default="",
                    dest='path',
                    help='Directory path [default: current directory]')

parser.add_argument('-sa', "--server-address",
                    action='store',
                    type=str, default="",
                    dest="server_address",
                    help='Git or Svn server address')

parser.add_argument('-u', "--user-name",
                    action='store',
                    type=str, default="",
                    dest="user",
                    help='User name for the git or svn server')

parser.add_argument('-i', "--identifier",
                    action='store',
                    type=str, default="",
                    dest="identifier",
                    help='Internal database identifier, e.g. projectname-git')

args = parser.parse_args()


class VC_Project(object):
    """
    VC_Project contains details and methods for a version-controlled project.
    """

    def __init__(self, **kwargs):
        super(VC_Project, self).__init__()
        if (len(kwargs) == 1 and 'identifier' in kwargs):
            self.project_details_from_data(kwargs['identifier'])
        else:
            self.set_defaults(kwargs)

    def set_defaults(self, kwargs):
        """
        Sets default parameters for the version-controlled project.
        """
        def check_kwargs_for(keyword, default):
            if keyword in kwargs:
                return kwargs[keyword]
            else:
                return default

        self.project_path = check_kwargs_for('project_path', '')
        self.vc_system = check_kwargs_for('vc_system', 'git')
        if self.vc_system == 'git':
            self.dotFolder = '.git'
        elif self.vc_system == 'svn':
            self.dotFolder = '.svn'
        else:
            sys.exit("VC_Project.__init__(): " +
                     "Unknown Version control system.")

        self.user = check_kwargs_for('user_name', '')
        self.server_address = check_kwargs_for('server_address', '')
        self.project_name = check_kwargs_for('project_name',
                                             os.path.basename(self.path))
        self.identifier = self.project_name + '-' + self.vc_system

        if self.vc_system == 'git':
            self.use_github = check_kwargs_for('use_github', False)
            if self.use_github:
                self.github_https = GITHUB_https.format(self.user,
                                                        self.project_name)
                self.github_git = GITHUB_git.format(self.user,
                                                    self.project_name)

    def project_from_data(self, identifier):
        """
        Gets project data from data file
        """
        projects_data = self.read_project_data()
        if identifier in projects_data:
            print ("Reading {} project data".format(self.identifier))
            return projects_data[identifier]
        else:
            error_msg = "No project named {} in {}.".format(identifier,
                                                            PROJECT_DATA_FN)
            sys.exit("VC_Project.project_from_data(): {}".format(error_msg))

    def move_VC_dotFolder(self):
        """
        Moves a local dot-folder (.git, .svn) to the VCM_PATH and links the
         folder.
        """
        dotFolder_path = os.path.join(self.project_path, self.dotFolder)
        # Check if the dot-folder is already a symbolic link
        if os.path.islink(dotFolder_path):
            sys.exit("VC_Project.move_VC_dotfolder(): " +
                     "The dot-folder is a sym-link already.")
        # Check if the vcm_path folder exists
        if not os.path.exists(self.vc_path):
            os.mkdir(self.vc_path)
        # Check if there is no other folder with the same name in the vcm_path
        new_dotFolder_path = os.path.join(self.vcm_path, self.project_name)
        if os.path.exists(new_dotFolder_path):
            error_msg = "The path {} already exists."
            sys.exit("VC_Project.move_VC_dotfolder(): {}".format(error_msg))
        # Move the dot-folder
        shutil.move(dotFolder_path, new_dotFolder_path)
        # Create symlink
        if self.dotFolder in os.listdir(self.path):
            error_msg = "Moving unsuccessful, {} still exists.".format(
                dotFolder_path)
            sys.exit("VC_Project.move_VC_dotfolder(): {}".format(error_msg))
        os.symlink(new_dotFolder_path, dotFolder_path)

    def read_project_data(self):
        """
        Reads the already existing yaml data file which contains all
         version-controlled projects and saves them to a dictionary.
        """
        # We first need to check if the projects.yaml exists
        if not os.path.exists(PROJECT_DATA_FN):
            return {}
        # Slurping in the yaml
        with open(PROJECT_DATA_FN) as projects:
            project_data = yaml.load(projects)
        return project_data

    def write_project_data(self):
        """
        Writes the the project details to a data file in the vcm_path.
        """
        project_data = self.read_project_data()
        if self.identifier in project_data:
            print ("The {} project is already in the "
                   "local database.".format(self.project_name))
        else:
            data_set = {"project_name": self.project_name,
                        "path": self.path,
                        "vc_system": self.vc_system,
                        "user": self.user,
                        "use_github": self.use_github,
                        "server_address": self.server_address}
            project_data[self.identifier] = data_set
            with open(PROJECT_DATA_FN) as projects_yaml:
                projects_yaml.dump(project_data)


if __name__ == '__main__':
    if not args.path:
        path = os.getcwd()
    else:
        path = args.path

    if args.identifier:
        project = VC_Project(identifier=args.identifier)
    elif ('.git' in os.listdir() or '.svn' in os.listdir()):
        project = VC_Project(path=args.path,
                             vc_system=args.vc_system,
                             project_name=args.project_name,
                             user=args.user,
                             use_github=args.use_github,
                             server_address=args.server_address)
    # Actions
    project.write_project_data()
    if args.move:
        project.move_VC_dotFolder()
