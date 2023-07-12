import platform
import sys
import os
from pathlib import Path
import errno

################## Global Config ##################
CURRENT_DIR = os.getcwd()
INSTALL_DIR = os.path.join(CURRENT_DIR, "install")

BUILD_DIR_BU =  os.path.join(CURRENT_DIR, "build_bu")
BUILD_DIR_GCC =  os.path.join(CURRENT_DIR, "build_gcc")

IS_LINUX = platform.system() == "Linux"
################## Basic Function ##################
def create_if_not_exist(path_dir):
    if not os.path.exists(path_dir):
        try:
            Path(path_dir).mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise RuntimeError("Fail to create path {}".format(path_dir))

def recreate_if_exist(path_dir):
    if os.path.exists(path_dir):
        try:
            Path(path_dir).rmdir()
        except OSError as exc:  # Guard against race condition
            if exc.errno == errno.EEXIST:
                raise RuntimeError("Fail to remove path {}".format(path_dir))
            
    try:
        Path(path_dir).mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise RuntimeError("Fail to create path {}".format(path_dir))

################## Build Function ##################


def build_binutils():
    recreate_if_exist(BUILD_DIR_BU)

    return 0

def build_gcc():
    return 0

if __name__ == '__main__':
    if IS_LINUX is False:
        raise("Only support Linux OS")
    
    recreate_if_exist(INSTALL_DIR)
    
    status_code = build_binutils()

    status_code = build_gcc()

    sys.exit()