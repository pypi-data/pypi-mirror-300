from urllib.parse import urljoin
from AnyQt.QtWidgets import QLineEdit, QGridLayout, QPushButton, QMessageBox, QSizePolicy as Policy, QLabel, QCheckBox

from AnyQt.QtCore import Qt, QSettings

from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.settings import Setting

from orangecontrib.blue_whale.widgets.utils.config import get_url, DEFAULT_URL
from orangecontrib.blue_whale.canvasmain import login
from orangecontrib.blue_whale.i18n_config import *


def __(key):
    return i18n.t("bluewhale.service_window." + key)


def set_style(button, param=None):
    if param == 'ok':
        button.setStyleSheet(
            "QPushButton{color:black}"
            "QPushButton{height:30px}"
            "QPushButton{line-height:30px}"
            "QPushButton{border-radius:4px}"
            "QPushButton{font-size:14px}"
            "QPushButton{margin-top:0px}"
            "QPushButton{background:#1890ff}"
            "QPushButton:hover{background:#00a9fd}"
            "QPushButton{color:#fff}"
        )
    else:
        button.setStyleSheet(
            "QPushButton{color:black}"
            "QPushButton{height:30px}"
            "QPushButton{line-height:30px}"
            "QPushButton{border-radius:4px}"
            "QPushButton{font-size:14px}"
            "QPushButton{margin-top:0px}"
            "QPushButton{background:#ccc}"
            "QPushButton:hover{background:#e9e9e9}"
        )


class ServiceWindow(OWWidget):
    name = __("name")
    want_basic_layout = False
    want_main_area = True
    want_control_area = False
    auto_commit = Setting(True)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.__mainLayout = True
        self.__feedbackUrl = None
        self.__feedbackLabel = None

        self.setStyleSheet(
            "QLineEdit{background-color:rgb(255,255,255) !important}"
            'QLineEdit{padding:3px 2px}'
            'QLineEdit{border-radius: 4px}'
            'QLineEdit{border: 1px solid #e9e9e9}'
            'QLineEdit{font-size: 14px}'
            'QLabel{font-size:14px}'
            'QLabel{color: #000 !important}'
            'QCheckBox{font-size:14px}'
        )

        layout = QGridLayout()

        self.serverCheck = QCheckBox(
            __("check_btn"), self,
            toolTip=__("check_btn_tip")
        )
        self.serverCheck.stateChanged.connect(self.clickBox)

        layout.layout().addWidget(self.serverCheck, 0, 0, 1, 2)
        self.serverCheck.setSizePolicy(Policy.MinimumExpanding, Policy.MinimumExpanding)

        hbox = gui.hBox(self)
        self.tip_text = QLabel(__("input_address"))
        hbox.layout().addWidget(self.tip_text)

        self.serverLineEdit = QLineEdit()
        # self.serverLineEdit.setAlignment(Qt.AlignLeft)
        self.serverLineEdit.setPlaceholderText('http or https://')

        hbox.layout().addWidget(self.serverLineEdit)
        layout.addWidget(hbox, 1, 0, 1, 2)

        self.okBtn = QPushButton(__("save"))
        set_style(self.okBtn, 'ok')
        # okBtn.setFixedSize(100, 30)
        self.cancelBtn = QPushButton(__("cancel"))
        set_style(self.cancelBtn)
        # cancelBtn.setFixedSize(100,30)
        layout.layout().addWidget(self.okBtn, 2, 0, 1, 1)
        layout.layout().addWidget(self.cancelBtn, 2, 1, 1, 1)

        if self.status():
            self.serverCheck.setCheckState(False)
            self.serverLineEdit.setEnabled(False)
            set_style(self.okBtn)
        else:
            self.serverCheck.setCheckState(2)
            self.serverLineEdit.setText(get_url())
            set_style(self.okBtn, 'ok')

        self.okBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)

        self.setLayout(layout)
        self.setWindowTitle(__("login_set"))

        self.setFixedSize(465, 140)

    def status(self):
        if get_url() == DEFAULT_URL:
            return True
        else:
            return False

    def save_url(self, url):
        settings = QSettings()
        settings.setValue('account/service', url)
        login(way=1)

    def clickBox(self, state):
        if state == Qt.Checked:
            self.serverLineEdit.setEnabled(True)
            self.serverLineEdit.setFocus()
            set_style(self.okBtn, 'ok')
            if not self.status():
                self.serverLineEdit.setText(get_url())
        else:
            if self.status():
                self.serverLineEdit.setText('')
                self.serverLineEdit.setEnabled(False)
                set_style(self.okBtn)
            else:
                net = QMessageBox(
                    parent=self, windowTitle=self.tr(__("tip")),
                    icon=QMessageBox.Question,
                    standardButtons=QMessageBox.Yes | QMessageBox.Cancel,
                    text=self.tr(__("default_address"))
                )
                net.button(QMessageBox.Yes).setText(__("ok"))
                net.button(QMessageBox.Cancel).setText(__("cancel"))
                status = net.exec()
                if status == QMessageBox.Yes:
                    self.save_url(DEFAULT_URL)
                    net = QMessageBox(
                        self, windowTitle=self.tr(__("tip")),
                        icon=QMessageBox.Information,
                        standardButtons=QMessageBox.Yes,
                        text=self.tr(__("change_address")),
                    )
                    net.button(QMessageBox.Yes).setText(__("ok"))
                    net.exec_()
                    self.close()
                elif status == QMessageBox.Cancel:
                    self.serverCheck.setCheckState(2)

    def show_error(self):
        net = QMessageBox(
            self, windowTitle=self.tr(__('ok')),
            icon=QMessageBox.Question,
            standardButtons=QMessageBox.Yes,
            text=self.tr(__("error_address")),
        )
        net.button(QMessageBox.Yes).setText(__("reenter"))
        self.serverLineEdit.setFocus()
        net.show()

    def accept(self):
        if self.serverCheck.isChecked():
            url = self.serverLineEdit.text().strip()
            try:
                import requests
                response = requests.get(urljoin(url, '/api/open/client_id'), timeout=7)
                if response.status_code == 200 and response.text == 'onion-ring-service':
                    self.save_url(url)
                    net = QMessageBox(
                        self, windowTitle=self.tr(__("tip")),
                        icon=QMessageBox.Information,
                        standardButtons=QMessageBox.Yes,
                        text=self.tr(__("change_success")),
                    )
                    net.button(QMessageBox.Yes).setText(__("ok"))
                    self.serverLineEdit.setFocus()
                    net.exec_()
                    self.close()
                else:
                    self.show_error()
            except Exception as e:
                self.show_error()



if __name__ == "__main__":
    WidgetPreview(ServiceWindow).run()
    # app = QApplication(sys.argv)
    # mainWin = ExampleWindow()
    # mainWin.show()
    # sys.exit(app.exec_())
