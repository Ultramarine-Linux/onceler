import subprocess

from .log import get_logger

logger = get_logger(__name__)

class MockBuild:
    def __init__(self, buildroot: str = "default"):
        self.buildroot = buildroot
        self.command = ["mock", "-r", self.buildroot, "--enable-network"]
        self.add_packages()


    def add_file(self,file: str):
        cmds = self.command.copy()
        cmds.extend([
            "--copyin", file, "/"
        ])
        return subprocess.run(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    def export_file(self,file: str, dest: str):
        cmds = self.command.copy()
        cmds.extend([
            "--copyout", file, dest
        ])

        return subprocess.run(cmds)

    def run(self,cmd: list[str]):
        cmds = self.command.copy()
        cmds.extend([
            "--chroot",
            "--",
        ])
        cmds.extend(cmd)

        return subprocess.run(cmds)

    def check_packages(self,pkgs: list[str]):
        cmds = self.command.copy()
        cmds.extend([
            "--chroot",
            "--",
        ])
        cmds.extend(["rpm", "-q"] + pkgs)

        pkgs_installed = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if pkgs_installed contains the text "not installed" then the package is not installed
        logger.debug(f"pkgs_installed: {pkgs_installed}")
        if "not installed" in pkgs_installed.stdout.decode("utf-8"):
            return False
        else:
            return True
    
    def delete(self, path: str):
        logger.info(f"Deleting {path} in chroot")
        return self.run(["rm", "-rf", path])

    def add_packages(self,pkgs: list[str]=["lorax-lmc-novirt", "nano", "sed"]):
        if self.check_packages(pkgs) == True:
            return
        cmds = self.command.copy()
        cmds.extend([
            "--install",
        ])
        cmds.extend(pkgs)

        return subprocess.run(cmds)



