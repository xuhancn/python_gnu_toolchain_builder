# python_gnu_toolchain_builder

## Install Build Depends
```cmd
sudo apt-get install gcc build-essential bison flex libgmp3-dev libmpc-dev libmpfr-dev texinfo gcc-multilib
```

## Sync GNU Repos
```cmd
git submodule sync
git submodule update --init --recursive
```

## Build toolchain
```cmd
python toolchain_builder.py
```

## Output
The toolchains will be installed in `"install"` sub-folder.