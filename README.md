
# PythonCompiler
## Overview
PythonCompiler is a sophisticated software tool **designed to address the challenge of dependency conflicts** when installing new versions of Python on domestic, open-source operating systems. It enhances the efficiency of local compilation and installation processes **by leveraging the Python programming language**. The tool features a command-line interface **crafted with argparse**, and offers both graphical interfaces **designed using Tkinter and PyQt6**. These interfaces streamline the entire compilation and installation process, allowing users to accomplish tasks with a single command or through a simple, visual configuration interface. Extensive testing has been conducted to ensure the software's functionality, reliability, and security, **validating its capability to fulfill its intended purpose**.
## Current Version
**Version 1.20+rb16**
## Features
- **Multi-mirror site support** for downloading Python source code
- **Rich configuration options** for customizing the compilation process
- Two sets of **graphical interfaces** developed using Tk (simple) and Qt (simple)
## System Dependencies
PythonCompiler utilizes several system libraries during the compilation process. These dependencies should be available in your system's package repositories. Users can install these packages through their system's package manager. The main dependencies include:
- g++
- openssl
- automake
- ncurses
- sqlite
## Installation
1. Visit the [Releases page](https://gitee.com/luoyanze07/PythonCompiler/releases) to download the latest *deb packages*.
2. Install the packages using the following command:
```
sudo apt install <package_name>.deb
```
**Note:** PythonCompiler is currently compatible with *amd64* architecture. Support for *arm64* and *loongarch64* architectures, as well as *rpm* and *uab* (Deepin Linglong) packages, is planned for future releases.
## Usage
After installation, you can use PythonCompiler from the command line with the following options:
```
usage: PythonCompiler [-h] [--version] [--latest] [--mirror MIRROR] [--download LINK] [--skip-update]
                      [--select SELECTION] [--config CONFIG] [--disable-optimizations] [--disable-shared]
                      [--without-lto] [--without-ssl] [--prefix PREFIX] [--compiler CC]

A tool for Python compilement on Linux.

options:
  -h, --help            show this help message and exit
  --version, -V, -v     show the version information and exit
  --latest, -l          show the latest version of Python and exit
  --mirror MIRROR, -m MIRROR
                        select a mirror site (huaweicloud, python.org, taobao-npm, bjtu, or specified) to get  
                        the source code of python
  --download LINK, --link LINK, -d LINK
                        specify the download link for the source code
  --skip-update, --skip
                        discard checking whether the version is valid
  --select SELECTION, --version-selection SELECTION, -s SELECTION
                        select a Python version (like "x.x.x"), for the latest stable version. When the link   
                        is provided, this will help me get the exact version number if the file name format    
                        is irregular.
  --config CONFIG       customize configurations for ./configure, e.g. --config='--with-ssl' (DO NOT FORGET
                        TO ADD THE EQUAL SIGN = AND APOSTROPHES '')
  --disable-optimizations
                        disable expensive, stable optimizations (PGO, etc.)
  --disable-shared      disable building a shared Python library
  --without-lto         disable Link-Time-Optimization in any build
  --without-ssl         disable SSL in any build
  --prefix PREFIX       installation location
  --compiler CC, -C CC  (EXPERIMENTAL) select a C compiler for CPython
```
## Contribution
Contributions to PythonCompiler are welcome! If you would like to contribute, please follow these steps:
1. Fork the repository on Gitee.
2. Create a feature branch and make your changes.
3. Submit a pull request to the main branch.
## Reporting Issues
If you encounter any issues or have suggestions for improvement, please file an issue on the [issue tracker](https://gitee.com/luoyanze07/issues).
