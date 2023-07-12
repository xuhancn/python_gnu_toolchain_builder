# python_gnu_toolchain_builder

## install build depends
```cmd
sudo apt-get install gcc build-essential bison flex libgmp3-dev libmpc-dev libmpfr-dev texinfo gcc-multilib
```

## sync gnu repos
```cmd
git submodule sync
git submodule update --init --recursive
```