from core.models import action

from git import Repo

# import jimi plugin classes
from plugins.git.includes.git_ops import GitOps as Git
from plugins.git.includes.git_ops import GitArgs
from plugins.git.includes.git_clone import CloneGit as Clone
from plugins.git.includes.git_clone import CloneArgs


class _GitOps(action._action):

    git_path: str = "/tmp/git/backups"  # local clone path root
    git_server: str = "gitea.company.com"  # git server hostname (or IP)
    git_port: str = "443"
    git_project: str = (
        "my-project"  # "git project name e.g. git@x.y.z/my-project/xyz.git"
    )
    git_repo_name: str = "backup-repo"  # "git repo name e.g. git@x.y.z/xyz/my-repo.git"
    git_branch: str = "master"  # default git branch to push to
    git_remote: str = "origin"  # default git remote name
    git_commit_message: str = "Jimi configuration backup commit."
    git_server_type: str = (
        "gitea"  # http, https or gitea (gitea is http but runs on explicit port 3000)
    )

    git: Git

    def doAction(self, data) -> dict:

        # set the git path on the filesystem
        self.git_path = _helper.set_git_path(git_path=self.git_path, data=data)
        # setup git related arguments
        args = self._setup_args()

        # create instance of Git object
        git = Git(args)
        # run git operations
        try:
            git.generate_url()
            git.setup_fs_paths()
            git.init()
            git.remote_add()
            git.create_index()
            git.files_add()
            git.commit()
            git.set_remote_reference()
            git.push()
            git.pull()

            # put git object into eventData for further use?
            data["eventData"]["git"] = {}
            data["eventData"]["git"] = git

            return {
                "result": True,
                "rc": 0,
                "msg": "Git-Ops successfull",
                "data": "Git Operations Complete!",
                "errors": "",
            }
        except Exception as e:
            return {
                "result": False,
                "rc": 255,
                "msg": f"Git exception: {e}",
                "data": "",
                "errors": e,
            }

    def _setup_args(self) -> GitArgs:

        args = GitArgs(
            git_port=self.git_port,
            git_path=self.git_path,
            git_server=self.git_server,
            git_project=self.git_project,
            git_repo_name=self.git_repo_name,
            git_branch=self.git_branch,
            git_remote=self.git_remote,
            git_commit_message=self.git_commit_message,
            git_server_type=self.git_server_type,
        )

        return args

    def setAttribute(self, attr, value, sessionData=None) -> bool:
        # set parent class session data
        return super(_GitOps, self).setAttribute(attr, value, sessionData=sessionData)


class _GitClone(action._action):

    repo: Repo = None

    git_url: str = "https://github.com/bodleytunes/jimiplugin-batfish.git/"
    # the root of the git path, so the clone should be to a project name as a subpath of this
    git_clone_local_path: str = "/tmp/git/backups"
    git_clone_subpath: str = (
        "jimiplugin-batfish"  # generally this should match the git project name
    )

    def doAction(self, data):
        # pre flight checks
        self._pre_flights(data)
        # create instance of git repo
        git_repo = Repo()
        # do cloning
        # create clone instance
        git_clone = Clone(
            args=CloneArgs(
                git_url=self.git_url,
                git_clone_local_path=self.git_clone_local_path,
                git_clone_subpath=self.git_clone_subpath,
            ),
            git_repo=git_repo,
        )
        # clone repo return git repo instance
        self.repo = git_clone.clone()

        if self.repo is not None:
            return {
                "result": True,
                "rc": 0,
                "msg": "Git-Clone successfull",
                "data": "Git Operations Complete!",
                "errors": "",
            }
        else:
            return {
                "result": False,
                "rc": 255,
                "msg": "Clone failed",
                "data": f"Path exists {self.git_clone_local_path}",
                "errors": "Clone failed",
            }

    def _pre_flights(self, data):
        self.git_clone_local_path = _helper.set_git_path(
            git_path=self.git_clone_local_path, data=data
        )

    def _set_git_path(git_path: str, data=None) -> str:
        # set the git path to the previously set destination folder if no explicit git path was passed in
        try:
            if data["eventData"]["backup_args"]["dst_folder"] is not None:
                if git_path is None or git_path == "/tmp/git/backups":
                    git_path = data["eventData"]["backup_args"]["dst_folder"]
                    return git_path
        except Exception as e:
            print(f"{e}")
            return git_path

    def setAttribute(self, attr, value, sessionData=None) -> bool:
        # set parent class session data
        return super(_GitClone, self).setAttribute(attr, value, sessionData=sessionData)


class _helper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def set_git_path(git_path: str, data=None) -> str:
        # set the git path to the previously set destination folder if no explicit git path was passed in
        try:
            if data["eventData"]["backup_args"]["dst_folder"] is not None:
                if git_path is None or git_path == "/tmp/git/backups":
                    git_path = data["eventData"]["backup_args"]["dst_folder"]
                    return git_path
        except Exception as e:
            print(f"{e}")
            return git_path
