import platform
import sys
import os
from pathlib import Path
import errno
from subprocess import check_call, check_output
import subprocess
import multiprocessing

################## Global Config ##################
CURRENT_DIR = os.getcwd()
INSTALL_DIR = os.path.join(CURRENT_DIR, "install")

BUILD_DIR_BU =  os.path.join(CURRENT_DIR, "build_bu")
BUILD_DIR_GCC =  os.path.join(CURRENT_DIR, "build_gcc")

IS_LINUX = platform.system() == "Linux"

MK_CPU_NUM = '-j{}'.format(multiprocessing.cpu_count())
################## Binutils Config ##################
BU_GIT_BRANCH = "binutils-2_40-branch"

BU_CONFIGURE_FLAGS = ""
BU_CONFIGURE_FLAGS += "--prefix={} ".format(INSTALL_DIR)
BU_CONFIGURE_FLAGS += "--with-sysroot=/ --with-system-zlib --enable-plugins --enable-gold --enable-threads "
BU_CONFIGURE_FLAGS += "--disable-gdb --disable-gdbserver "
# BU_CONFIGURE_FLAGS += "--disable-nls "
# BU_CONFIGURE_FLAGS += "--disable-werror "
BU_CONFIGURE_FLAGS += "--disable-multilib "

################## Gcc Config ##################
GCC_CONFIGURE_FLAGS = ""
GCC_CONFIGURE_FLAGS += "--prefix={} ".format(INSTALL_DIR)
GCC_CONFIGURE_FLAGS += "--enable-languages=c,c++,fortran,objc,obj-c++,lto,go "
GCC_CONFIGURE_FLAGS += "--enable-bootstrap "
GCC_CONFIGURE_FLAGS += "--enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array --enable-offload-targets=nvptx-none --without-cuda-driver --enable-gnu-indirect-function --enable-cet --with-tune=generic --with-arch_32=i686 --with-multilib-list=m32,m64 --with-build-config=bootstrap-lto --enable-link-serialization=1 --with-fpmath=sse "

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

    BU_SOURCE = os.path.join(CURRENT_DIR, "gnu_repos" , "binutils-gdb")

    status_code = subprocess.check_call(["git", "checkout", BU_GIT_BRANCH], cwd=BU_SOURCE)

    BU_CFG = os.path.join(BU_SOURCE, "." , "configure")

    my_env = os.environ.copy()
    my_env["CC"] = "gcc"

    status_code = subprocess.check_call([BU_CFG, BU_CONFIGURE_FLAGS], cwd=BUILD_DIR_BU, env=my_env)

    status_code = subprocess.check_call(["make", MK_CPU_NUM], cwd=BUILD_DIR_BU)

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