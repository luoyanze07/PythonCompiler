import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from os import popen, system



import qt6gui_new

__version__ = "1.20"
__project__ = "PythonCompiler"

dpkgl = popen("dpkg -l").read()

commander = "PythonCompiler"
title = "{} {}".format(__project__, __version__)
notbool = lambda b: bool(1 - b)
response = {False: "no", True: "yes"}

class Window(QWidget, qt6gui_new.Ui_PythonCompiler):
    def __init__(self):
        global data
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(title)
        get = popen("{commander} --gapi".format(commander=commander))
        data = eval(get.read())
        self.setWindowIcon(QIcon(data['icons']['ico']))
        self.selection.addItems(data['versions'])
        self.mirror.addItems(data['mirrors'].keys())
        self.mirror.setCurrentIndex(1)
        self.buttonBox.rejected.connect(app.exit)
        self.buttonBox.accepted.connect(self.get)
        self.pushButton.pressed.connect(self.about)

    def about(self):
        QMessageBox.about(self, title, "<b>About PythonCompiler GUI</b><br /><br /><b>Name</b>: {}<br /><b>Version</b>: {}<br />Built on Python 3.12 with Qt 6.6.1".format(__project__, __version__))
    def get(self):
        selection = self.selection.currentText()
        mirror = self.mirror.currentText()
        download = self.download.text()
        optimizations = self.opt.isChecked()
        lto = self.lto.isChecked()
        ssl = self.ssl.isChecked()
        shared = self.shared.isChecked()
        prefix = self.prefix.text()
        cc = self.cc.text()
        url_status = self.specify_link.isChecked()
        cc_status = self.specify_c.isChecked()
        config_status = self.customize.isChecked()
        config = self.configuration.text()

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
        if "." not in certain_ver or sum([(str(i) in certain_ver) for i in range(10)]) == 0:
            certain_ver = selection
        
        print("Wait for a confirmation. ")
        if config_status:
            self.ask = QMessageBox.question(self, title, "<b>Check configurations</b><br /><br /><b>Download link: </b>{url}<br /><b>Required version: </b>{pyver}<br /><b>Configuration: </b>{config}<br />".format(
            url=url, pyver=certain_ver, config=config
        ))
        else:
            self.ask = QMessageBox.question(self, title, "<b>Check configurations</b><br /><br /><b>Download link: </b>{url}<br /><b>Required version: </b>{pyver}<br /><b>Enable optimizations: </b>{opt}<br /><b>Enable shared libraries: </b>{shared}<br /><b>Build with LTO: </b>{lto}<br /><b>Build with SSL: </b>{ssl}<br /><b>Prefix: </b>{prefix}<br /><b>CPython Compiler: </b>{cc}".format(
            url=url, pyver=certain_ver, opt=response[optimizations], shared=response[shared], lto=response[lto], ssl=response[ssl], prefix=prefix, cc=shown_cc
        ))
        if self.ask == QMessageBox.StandardButton.Yes:
            window.close()
            window.destroy()
            print("\n")
            if config_status:
                system('{commander} --skip --hide-confirmation -s {ver} -d {url} --config=" {config}"'.format(commander=commander, ver=certain_ver, url=url, config=config))
            
            else: 
                system("{commander} --skip --hide-confirmation -s {ver} -d {url} --prefix {prefix} {advanced}".format(commander=commander, ver=certain_ver, url=url, prefix=prefix, 
                                                                                           advanced=((notbool(optimizations) * " --disable-optimizations") + (notbool(shared) * " --disable-shared") + (notbool(lto) * " --without-lto") + (notbool(ssl) * " --without-ssl") + (int(cc_status) * (" -C {cc}".format(cc=cc))))))
            app.exit()


if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Window()
    print("GUI Started! ")
    window.show()
    sys.exit(app.exec())