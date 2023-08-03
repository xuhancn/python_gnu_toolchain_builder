import platform
import sys
import os
from pathlib import Path
import errno
from subprocess import check_call, check_output
import subprocess
import multiprocessing
import shutil

################## Version Control ##################
BU_GIT_BRANCH = "binutils-2_40"
GCC_GIT_BRANCH = "releases/gcc-12.3.0"

################## Global Config ##################
CURRENT_DIR = os.getcwd()
INSTALL_DIR = os.path.join(CURRENT_DIR, "install")

INSTALL_DIR_BU = os.path.join(INSTALL_DIR, "binutils")
INSTALL_DIR_GCC = os.path.join(INSTALL_DIR, "gcc")

BUILD_DIR_BU =  os.path.join(CURRENT_DIR, "build_bu")
BUILD_DIR_GCC =  os.path.join(CURRENT_DIR, "build_gcc")

IS_LINUX = platform.system() == "Linux"

MK_CPU_NUM = '-j{}'.format(multiprocessing.cpu_count())
################## Binutils Config ##################

BU_CONFIGURE_FLAGS = ""
BU_CONFIGURE_FLAGS += "--prefix={} ".format(INSTALL_DIR_BU)
BU_CONFIGURE_FLAGS += "--with-sysroot=/ --with-system-zlib --enable-plugins --enable-gold --enable-threads "
BU_CONFIGURE_FLAGS += "--disable-gdb --disable-gdbserver "

################## Gcc Config ##################

GCC_CONFIGURE_FLAGS = ""
GCC_CONFIGURE_FLAGS += "--prefix={} ".format(INSTALL_DIR_GCC)
GCC_CONFIGURE_FLAGS += "--enable-languages=c,c++,fortran,objc,obj-c++,lto,go "
GCC_CONFIGURE_FLAGS += "--enable-bootstrap "
GCC_CONFIGURE_FLAGS += "--enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib "
GCC_CONFIGURE_FLAGS += "--enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id "
GCC_CONFIGURE_FLAGS += "--with-gcc-major-version-only --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array "
GCC_CONFIGURE_FLAGS += "--enable-offload-targets=nvptx-none --without-cuda-driver --enable-gnu-indirect-function --enable-cet "
GCC_CONFIGURE_FLAGS += "--with-tune=generic --with-arch_32=i686 --with-multilib-list=m32,m64 --with-build-config=bootstrap-lto "
GCC_CONFIGURE_FLAGS += "--enable-link-serialization=1 --with-fpmath=sse "
GCC_CONFIGURE_FLAGS += "--with-default-libstdcxx-abi=gcc4-compatible "

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
        shutil.rmtree(path_dir)
            
    try:
        Path(path_dir).mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise RuntimeError("Fail to create path {}".format(path_dir))

################## Build Function ##################


def build_binutils():
    recreate_if_exist(BUILD_DIR_BU)

    BU_SOURCE = os.path.join(CURRENT_DIR, "gnu_repos" , "binutils-gdb")

    subprocess.check_call(["git", "reset", "--hard"], cwd=BU_SOURCE)
    subprocess.check_call(["git", "checkout", BU_GIT_BRANCH], cwd=BU_SOURCE)
    subprocess.check_call(["git", "pull"], cwd=BU_SOURCE)

    BU_CFG = os.path.join(BU_SOURCE, "." , "configure")

    my_env = os.environ.copy()
    # my_env["CC"] = "gcc"

    subprocess.check_call(["sh", "-c" ,"{} {}".format(BU_CFG, BU_CONFIGURE_FLAGS)], cwd=BUILD_DIR_BU, env=my_env)

    subprocess.check_call(["make", MK_CPU_NUM], cwd=BUILD_DIR_BU)

    subprocess.check_call(["make", "install"], cwd=BUILD_DIR_BU)

    return 0

def build_gcc():
    recreate_if_exist(BUILD_DIR_GCC)

    GCC_SOURCE = os.path.join(CURRENT_DIR, "gnu_repos" , "gcc")

    subprocess.check_call(["git", "reset", "--hard"], cwd=GCC_SOURCE)
    subprocess.check_call(["git", "checkout", GCC_GIT_BRANCH], cwd=GCC_SOURCE)
    subprocess.check_call(["git", "pull"], cwd=GCC_SOURCE)

    GCC_DOWNLOAD_DEPENDS = os.path.join(GCC_SOURCE, "contrib" , "download_prerequisites")
    subprocess.check_call([GCC_DOWNLOAD_DEPENDS], cwd=GCC_SOURCE)

    GCC_CFG = os.path.join(GCC_SOURCE, "." , "configure")

    my_env = os.environ.copy()
    bu_path = os.path.join(INSTALL_DIR_BU, "bin")
    cur_path = bu_path + ":" + my_env["PATH"]
    my_env["PATH"] = cur_path

    subprocess.check_call(["sh", "-c" ,"{} {}".format(GCC_CFG, GCC_CONFIGURE_FLAGS)], cwd=BUILD_DIR_GCC, env=my_env)

    subprocess.check_call(["make", MK_CPU_NUM], cwd=BUILD_DIR_GCC)

    subprocess.check_call(["make", "install"], cwd=BUILD_DIR_GCC)

    return 0

if __name__ == '__main__':
    if IS_LINUX is False:
        raise("Only support Linux OS")
    
    recreate_if_exist(INSTALL_DIR)
    
    status_code = build_binutils()

    status_code = build_gcc()

    sys.exit()
