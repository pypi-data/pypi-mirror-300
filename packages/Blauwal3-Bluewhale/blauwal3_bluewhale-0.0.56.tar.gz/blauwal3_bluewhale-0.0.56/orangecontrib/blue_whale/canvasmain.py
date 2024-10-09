from AnyQt.QtWidgets import QAction, QMenu, QMessageBox
from AnyQt.QtCore import Qt, QCoreApplication, QEvent

from Orange.canvas import config

from orangecanvas.application.canvasmain import CanvasMainWindow
from orangecanvas.registry import get_style_sheet, get_global_registry
from orangecanvas.application.outputview import TextStream

from orangecontrib.blue_whale.i18n_config import *


def __(key):
    return i18n.t("bluewhale.canvasmain." + key)

# 修改这一行

__SESSION = {"SESSION": ""}

def login(way=None):
    global __SESSION
    if __SESSION.get('SESSION'):  # 登录状态，用户点击则是退出，
        set_session({'SESSION': None}, message=__("sign_in"))
    else:
        if not way:
            get_session()


def get_user_session():
    global __SESSION
    from orangecontrib.blue_whale.widgets.utils.login import MainWindow
    window = MainWindow(__SESSION)
    window.exec_()
    return __SESSION.get('SESSION')


def set_session(value, message=__("sign_in")):
    global __SESSION, login_action
    __SESSION.update(value)
    if login_action:
        login_action.setText(message)
    message = __("sign_out") if message == __("sign_in") else __("sign_in")
    msg_box = QMessageBox(QMessageBox.Information, __("login_information"), message + __("success"), QMessageBox.Yes)
    msg_box.button(QMessageBox.Yes).setText(__("ok"))
    msg_box.exec_()


def get_session(key='SESSION'):
    global __SESSION, login_action
    if __SESSION.get(key):
        return __SESSION[key]

    if get_user_session():
        # 修改按钮信息
        login_action.setText(__("sign_out"))
        # 提示用户登录成功
        msg_box = QMessageBox(QMessageBox.Information, __("login_information"), __("sign_in") + __('success'),
                              QMessageBox.Yes)
        msg_box.button(QMessageBox.Yes).setText(__("ok"))
        msg_box.exec_()
        # 返回当前的session
        return __SESSION.get(key)

    return None


def get_session_value(key='SESSION'):
    global __SESSION
    return __SESSION.get(key)


def set_service():
    from orangecontrib.blue_whale.widgets.utils.service_window import ServiceWindow
    window = ServiceWindow()
    window.exec_()


class BWCanvasMainWindow(CanvasMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        global login_action
        login_action = QAction(
            self.tr(__("sign_in")),
            objectName="action-login",
            toolTip=self.tr(__("login")),
            triggered=login,
        )
        
        menubar = self.menuBar()
        server_menu = QMenu(
            self.tr(__("service")), menubar, objectName="server-menu"
        )
        self.settings_action = QAction(
            __("service_settings"), self,
            objectName="action-settings",
            toolTip=__("service_settings_tip"),
            triggered=set_service
        )

        server_menu.addAction(login_action)
        server_menu.addAction(self.settings_action)
        menubar.addMenu(server_menu)
        self.setMenuBar(menubar)


    def open_case(self, filename):
        """
        Open and load a '*.report' from 'filename'
        """
        widget_registry = get_global_registry()
        if self.is_transient():
            window = self
        else:
            window = self.create_new_window()
        window.setWindowModified(True)
        window.setWindowModified(False)

        window.setStyleSheet(get_style_sheet())
        window.setAttribute(Qt.WA_DeleteOnClose)
        window.setWindowIcon(config.application_icon())
        window.connect_output_stream(TextStream())
        window.set_widget_registry(widget_registry)

        window.open_example_scheme(filename)

    def closeEvent(self, event):
        super().closeEvent(event)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.update_login_action_text()
        super().changeEvent(event)
