import os
import shutil
import sys


GITHUB_USER = 'jdcapa'
HOME = os.path.expanduser("~")
VCM_PATH = os.path.join(HOME, ".VersionControl")


github_https = "https://github.com/{}/{}copy".format(GITHUB_USER)
github_git = 'git@github.com:{}/{}.git'.formtat(GITHUB_USER)





class VC_Project(object):
    """
    VC_Project contains details and methods for a version-controlled project.
    """
    def __init__(self, project_path, vc_system='git', **kwargs):
        super(VC_Project, self).__init__()
        self.path = project_path
        self.vc_system = vc_system
        if vc_system == 'git':
            self.dotFolder = '.git'
        elif vc_system == 'git':
            self.dotFolder = '.svn'
        else:
            sys.exit("VC_Project.__init__(): " +
                     "Unknown Version control system.")
        self.kwargs = self.set_defaults(kwargs)

    def set_defaults(self, kwargs):
        """
        Sets default parameters for the version-controlled project.
        """
        def check_kwargs_for(keyword, default):
            if keyword in kwargs:
                return kwargs[keyword]
            else:
                return default

        if self.vc_system == 'git':
            self.use_github = check_kwargs_for('use_github', False)
        self.user = check_kwargs_for('user_name', '')
        self.project_name = check_kwargs_for('project_name',
                                             os.path.basename(self.path))
        self.vcm_path = check_kwargs_for('vcm_path',
                                         os.path.join(HOME, ".VersionControl"))

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

    def add_project_to_datfile(self):
        """
        Writes the the project details to a data file in the vcm_path
        """
        self.datfile = os.path.join(self.vcm_path, 'projects.yaml')

