from skbuild import setup
import platform
import subprocess
from setuptools import Command

platform_system = platform.system()


def get_version():
    """
    Get version from toolkit
    TODO: This should be revised to get version information     from the toolkit
    """
    return "5.3.0.dev0"


#
class CleanCommand(Command):
    """ Cleans project tree """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = []
        exe = ""
        if platform_system == "Windows":
            cmd = ['del' '/Q', 'tests\\data\\temp_*.*' '&&' 'rd' '/s/q',
                   '_cmake_test_compile', '_skbuild', 'dist', '.pytest_cache',
                   'src\\swmm\\toolkit\\swmm_toolkit.egg-info', 'tests\\__pycache__']
            exe = "C:\\Windows\\System32\\cmd.exe"

        elif platform_system == "Linux":
            cmd = ["rm -vrf _skbuild/ dist/ **/build .pytest_cache/ **/__pycache__  \
            **/*.egg-info **/data/temp_*.* **/data/en* **/.DS_Store MANIFEST"]
            exe = "/bin/bash"

        elif platform_system == "Darwin":
            cmd = ['setopt extended_glob nullglob; rm -vrf _skbuild dist **/build .pytest_cache \
            **/__pycache__ **/*.egg-info **/data/(^test_*).* **/data/en* **/.DS_Store MANIFEST']
            exe = '/bin/zsh'

        p = subprocess.Popen(cmd, shell=True, executable=exe)
        p.wait()


# if platform_system == "Windows":
#     cmake_args = ["-GVisual Studio 17 2022", "-Ax64"]
#
# elif platform_system == "Darwin":
#     cmake_args = ["-GNinja", "-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9", "-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64"]
#
# else:
#     cmake_args = ["-GUnix Makefiles"]

setup(
    cmdclass={"clean": CleanCommand},
    version=get_version(),
    packages=["epaswmm"],
    # package_dir={"swmm": "bin"},
    # cmake_args=[
    #     *cmake_args,
    # ],
    python_requires=">=3.7",
)
