## -*- coding: utf-8 -*-
import requests
import re
import argparse
from os import system
from sys import exit as sys_exit


__version__ = "1.20"
__project__ = "PythonCompiler"
__svg__ = r"/opt/apps/com.gitee.andrewluo.pythoncompiler/icons/favicon.svg"
__ico__ = r"/opt/apps/com.gitee.andrewluo.pythoncompiler/icons/favicon.ico"

terminal_code = """
cd /usr/src
wget {url} -O {filename}
tar xvf {filename}
cd {filename_without_suffix}
./configure {configure_options}
make -j$(nproc)
make install
cd /usr/src
tar zvcf Python-{python_version}-compiled.tgz Python-{python_version}
rm -rf {filename}
"""

destroy_code = """
sudo rm -rf /usr/src/Python-{python_version} /tmp/install_python_{python_version}.sh
echo 'The remaining files are placed at /usr/src/Python-{python_version}-compiled.tgz'
"""

url = {
    'python.org': "https://www.python.org/ftp/python/{version}/Python-{version}.tgz", 
    'huaweicloud': "https://mirrors.huaweicloud.com/python/{version}/Python-{version}.tgz", 
    'taobao-npm': "https://registry.npmmirror.com/-/binary/python/{version}/Python-{version}.tgz", 
    'bjtu': "https://mirror.bjtu.edu.cn/{version}/Python-{version}.tgz"
}

response = {False: "no", True: "yes"}

def version_info():
    try:
        python_org = requests.get("https://python.org/downloads/").text
    except:
        print('''Perhaps there's something wrong with the connection towards python.org. Try "--skip" to discard the process of checking the newest version of Python. Exit.''')
        sys_exit()
    text = [i[1] for i in re.findall("""<span class="release-number"><a href="(.*?)">Python (.*?)</a></span>""", python_org)]


    v_list = [[int(j) for j in i.split('.')] for i in text]
    all_versions = ['.'.join([str(j) for j in i]) for i in v_list]
    versions = {}
    for i in v_list:
        versions[i[0]] = {}
    for i in v_list:
        versions[i[0]][i[1]] = []
    for i in v_list:
        versions[i[0]][i[1]].append(i[2])

    latest_versions = [['.'.join([str(x) for x in [i, j, max(versions[i][j])]]) for j in versions[i]] for i in versions]
    latest_versions = latest_versions[0] + latest_versions[1]
    return all_versions, latest_versions

def main():
    parser = argparse.ArgumentParser(prog="PythonCompiler", description="A tool for Python compilement on Linux. ")
    # parser.add_argument("--gui", "-G", help="Run with GUI", action="store_true")
    parser.add_argument("--version", "-V", "-v", help="show the version information and exit", action="store_true")
    parser.add_argument("--latest", "-l", help="show the latest version of Python and exit", action="store_true")
    parser.add_argument("--gapi", help=argparse.SUPPRESS, action="store_true", dest="gapi")
    parser.add_argument("--mirror", "-m", help="select a mirror site (huaweicloud, python.org, taobao-npm, bjtu, or specified) to get the source code of python", type=str, default='huaweicloud')
    parser.add_argument("--download", "--link", "-d", help='specify the download link for the source code', dest="link", type=str, required=False)
    parser.add_argument("--yes", "-y", help=argparse.SUPPRESS, action="store_true")
    parser.add_argument("--skip-update", "--skip", help="discard checking whether the version is valid", dest="skip", action="store_true")
    parser.add_argument("--select", "--version-selection", "-s", type=str, help='select a Python version (like "x.x.x"), for the latest stable version. When the link is provided, this will help me get the exact version number if the file name format is irregular. ', dest="selection", required=False)
    parser.add_argument("--config", help="customize configurations for ./configure, e.g. --config='--with-ssl' (DO NOT FORGET TO ADD THE EQUAL SIGN = AND APOSTROPHES '')", required=False, type=str, dest='config')
    parser.add_argument("--disable-optimizations", help="disable expensive, stable optimizations (PGO, etc.)", action="store_true", dest="optimizations")
    parser.add_argument("--disable-shared", help="disable building a shared Python library", action="store_true", dest="shared")
    parser.add_argument("--without-lto", help="disable Link-Time-Optimization in any build", action="store_true", dest="lto")
    parser.add_argument("--without-ssl", help="disable SSL in any build", action="store_true", dest="ssl")
    parser.add_argument("--prefix", help="installation location", type=str, default="/usr", dest="prefix")
    parser.add_argument("--compiler", "-C", help="(EXPERIMENTAL) select a C compiler for CPython", dest="cc", type=str, required=False)
    parser.add_argument("--hide-confirmation", help=argparse.SUPPRESS, action="store_true", dest="hide")
    args = parser.parse_args()
    skip = args.skip
    latest = args.latest
    version = args.version
    config = args.config
    mirror = args.mirror
    selection = args.selection
    download = args.link
    optimizations = not args.optimizations
    shared = not args.shared
    lto = not args.lto
    ssl = not args.ssl
    cc = args.cc
    yes = args.yes
    prefix = args.prefix
    gapi = args.gapi
    hide = args.hide

    if skip and latest:
        print("There is a conflict of logic. Exit. ")
        sys_exit()

    if version:
        print("{} {}".format(__project__, __version__)) 
        sys_exit()

    if (selection == None) and (latest == False) and (download == None) and (gapi == False):
        parser.print_usage()
        sys_exit()
    
    if gapi:
        print("# These are for the GUI apps. ")
        print({"versions": version_info()[0], "mirrors": url, "icons": {"ico": __ico__, "svg": __svg__}})
        sys_exit()
    if skip == False:
        if latest:
            print("These are the latest stable versions of Python. ")
            [print('Python {}'.format(i)) for i in version_info()[1]]
            sys_exit()
        if ((selection != None) and ((selection in version_info()[0])) == False):
            print('Perhaps the required version is not correct. Use "-l" to see the latest versions. Please try again. Exit. '.format())
            sys_exit()
    
    if config in [None, '']:
        configurations = "--prefix={}".format(prefix) + optimizations * " --enable-optimizations" + shared * " --enabled-shared" + lto * " --with-lto" + ssl * " --with-ssl"
    else:
        configurations = config
    
    if cc != None and cc != "": 
        configurations += " CC={}".format(cc)
        shown_cc = cc
    else:
        shown_cc = "(default)"
    if mirror.lower() in url.keys():
        download_url = url[mirror].format(version=selection)
        # selection = download.split("/")[-1].split("-")[-1][:-4]
    elif '://' not in mirror.lower():
        print("It seems that it's not a correct link. Please check you configurations. ")
        sys_exit()
    elif mirror.lower() not in url.keys():
        print("Your mirror site is not involved. Remember to check the download link!")
        download_url = (mirror + "/{version}/Python-{version}.tgz").format(version=selection)
    else:
        pass

    if download != None:
        download_url = download
    filename = download_url.split("/")[-1]
    filename_without_suffix = filename.replace(".tgz", "").replace(".tar.gz", "").replace(".tar.xz", "")
    if selection == None:
        selection = filename_without_suffix.split("-")[-1]
    
    if not hide:
        print("\nBefore running the script, please check the following information. \n")
        print("Download link: {url}\nRequired version: {pyver}\nConfiguration: {config}".format(
            url=download_url, pyver=selection, config=configurations
        ))
        if yes:
            print("\nReady to install? [y/n] yes")
        else:
            is_ready = input("\nReady to install? [y/n] ")
            if (is_ready.lower() in ['y', 'yes']) == False:
                print("It seems that you are not prepared well. Exit. ")
                sys_exit()

    final_code = terminal_code.format(url=download_url, python_version=selection, configure_options=configurations, filename=filename, filename_without_suffix=filename_without_suffix)
    with open("/tmp/install_python_{}.sh".format(selection), encoding='utf-8', mode="w+") as file:
        file.write(final_code)
        file.close()
    with open("/tmp/destroy_installer_pythoncompiler.sh", encoding="utf-8", mode="w+") as file:
        file.write(destroy_code.format(python_version=selection))
    
    system('sudo sh /tmp/install_python_{}.sh'.format(selection))
    system("sudo sh /tmp/destroy_installer_pythoncompiler.sh")
    system("sudo rm -rf /tmp/destroy_installer_pythoncompiler.sh")

if __name__ == "__main__":
    main()