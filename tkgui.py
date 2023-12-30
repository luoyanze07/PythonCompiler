## -*- coding: utf-8 -*-
from os import popen, system
from sys import exit as sys_exit
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

__version__ = "1.20"
__project__ = "PythonCompiler"

dpkgl = popen("dpkg -l").read()

commander = "PythonCompiler"
title = "{} {}".format(__project__, __version__)
notbool = lambda b: bool(1 - b)
response = {False: "no", True: "yes"}

def on_checkbox_changed(wins, wins_opposite, var):
    for win in wins:
        if var.get() == True:
            win.config(state="normal")
        if var.get() == False:
            win.config(state="disabled")
    for win in wins_opposite:
        if var.get() == False:
            win.config(state="normal")
        if var.get() == True:
            win.config(state="disabled")

def get_data():
    global root, data, download_url_entry, cc_switch, selection, mirror, download, version_selection, mirror_selection, download_url, optimizations_var, shared_var, lto_var, ssl_var, prefix_var, cc_var, optimizations, shared, lto, ssl, prefix, cc
    selection = version_selection.get()
    mirror = mirror_selection.get()
    download = download_url.get()
    optimizations = optimizations_var.get()
    shared = shared_var.get()
    lto  = lto_var.get()
    ssl = ssl_var.get()
    prefix = prefix_var.get()
    cc = cc_var.get()
    url_status = download_url_entry.get()
    cc_status = cc_switch.get()


    if cc_status: 
        shown_cc = cc
    else:
        shown_cc = "(default)"
    if mirror.lower() in data['mirrors'].keys():
        url = data['mirrors'][mirror].format(version=selection)
        # selection = download.split("/")[-1].split("-")[-1][:-4]
    elif mirror.lower() not in data['mirrors'].keys():
        url = (mirror + "/{version}/Python-{version}.tgz").format(version=selection)
    else:
        pass
    if download not in [None, ""] and url_status == True:
        url = download
    filename = url.split("/")[-1]
    filename_without_suffix = filename.replace(".tgz", "").replace(".tar.gz", "").replace(".tar.xz", "")
    certain_ver = selection
    if download not in [None, ""]:
        certain_ver = filename_without_suffix.split("-")[-1]
    if "." not in certain_ver and sum([(str(i) in certain_ver) for i in range(10)]) == 0:
        certain_ver = selection
    
    print("Wait for a confirmation. ")
    ask = messagebox.askquestion(title=title, message="Check configurations", icon='info', 
                        detail="Download link: {url}\nRequired version: {pyver}\nEnable optimizations: {opt}\nEnable shared libraries: {shared}\nBuild with LTO: {lto}\nBuild with SSL: {ssl}\nPrefix: {prefix}\nCPython Compiler: {cc}\n".format(
        url=url, pyver=certain_ver, opt=response[optimizations], shared=response[shared], lto=response[lto], ssl=response[ssl], prefix=prefix, cc=shown_cc
    ))
    if ask == 'yes':
        print("\n")
        root.destroy()
        system("{commander} --skip --hide-confirmation -s {ver} -d {url} --prefix {prefix} {advanced}".format(commander=commander, ver=certain_ver, url=url, prefix=prefix, 
                                                                                           advanced=((notbool(optimizations) * " --disable-optimizations") + (notbool(shared) * " --disable-shared") + (notbool(lto) * " --without-lto") + (notbool(ssl) * " --without-ssl") + (int(cc_status) * (" -C {cc}".format(cc=cc))))))

def about(root):
    messagebox.showinfo(title=title, message="About PythonCompiler GUI", detail="Name: {project}\nVersion: {version}\nBuilt on Python 3.12 with Tcl/Tk 8.6.12 and Tk 8.6.13".format(project=__project__, version=__version__) )


if __name__ == "__main__":
    global root, data, download_url_entry, cc_entry, selection, mirror, download, version_selection, mirror_selection, download_url, optimizations_var, shared_var, lto_var, ssl_var, prefix_var, cc_var, optimizations, shared, lto, ssl, prefix, cc
    get = popen("{commander} --gapi".format(commander=commander))
    data = eval(get.read())
    all_versions = data['versions']

    root = tk.Tk()
    im = Image.open(data['icons']['ico'])
    img = ImageTk.PhotoImage(im)
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.geometry('720x320')
    root.title("{} {}".format(__project__, __version__))
    root.resizable(False, False)

    version_label = tk.Label(root, text="Required Python version: ")
    version_selection = tk.StringVar()
    version_selection.set(all_versions[0])
    select_version = ttk.Combobox(root, textvariable=version_selection, values=all_versions, width=8)
    version_label.place(x=16, y=16)
    select_version.place(x=256, y=12)

    mirror_label = tk.Label(root, text="Mirror site:")
    mirror_selection = tk.StringVar()
    mirror_site = ttk.Combobox(root, textvariable=mirror_selection, values=list(data['mirrors'].keys()), width=14)
    mirror_site.current(1)
    mirror_label.place(x=416, y=16)
    mirror_site.place(x=528, y=16)

    download_url = tk.StringVar()
    download_url_entry  = tk.Entry(root, width=36, textvariable=download_url)
    url_switch = tk.IntVar()
    url_switcher_command = lambda: on_checkbox_changed([download_url_entry], [mirror_site], url_switch)
    url_switcher = tk.Checkbutton(root, text="Specify download link: ", variable=url_switch, command=url_switcher_command)
    download_url_entry.config(state="disabled")
    download_url_entry.place(x=288, y=64)
    url_switcher.place(x=16, y=64)

    optimizations_var, shared_var, lto_var, ssl_var = tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()
    enable_optimizations = tk.Checkbutton(root, text="Enable optimizations", variable=optimizations_var)
    enable_shared = tk.Checkbutton(root, text="Enabled shared libraries", variable=shared_var)
    with_lto = tk.Checkbutton(root, text="Enable Link-Time-Optimizations (LTO)", variable=lto_var)
    with_ssl = tk.Checkbutton(root, text="Enable SSL", variable=ssl_var)
    enable_optimizations.select()
    enable_shared.select()
    with_lto.select()
    with_ssl.select()
    enable_optimizations.place(x=16, y=128)
    enable_shared.place(x=416, y=128)
    with_lto.place(x=16, y=160)
    with_ssl.place(x=416, y=160)

    prefix_label = tk.Label(root, text="Prefix: ")
    prefix_var = tk.StringVar(value="/usr")
    prefix_entry = tk.Entry(root, width=12, textvariable=prefix_var)
    prefix_label.place(x=16, y=216)
    prefix_entry.place(x=96, y=216)

    cc_var = tk.StringVar()
    cc_entry = tk.Entry(root, width=12, textvariable=cc_var)
    cc_switch = tk.IntVar()
    cc_switcher_command = lambda: on_checkbox_changed([cc_entry], [], cc_switch)
    cc_switcher = tk.Checkbutton(root, text="Specify C Compiler: ", variable=cc_switch, command=cc_switcher_command)
    cc_entry.config(state="disabled")
    cc_switcher.place(x=288, y=216)
    cc_entry.place(x=528, y=216)

    about_button = tk.Button(root, text="About", command=lambda: about(root))
    about_button.place(x=192, y=264)
    run_button = tk.Button(root, text="Run", command=get_data)
    run_button.place(x=324, y=264)
    close_button = tk.Button(root, text="Close", command=sys_exit)
    close_button.place(x=480, y=264)

    print("GUI Started! ")
    root.mainloop()
