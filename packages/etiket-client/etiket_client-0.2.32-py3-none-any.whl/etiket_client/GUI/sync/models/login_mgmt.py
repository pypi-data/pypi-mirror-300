from etiket_client.remote.authenticate import check_internet_connection, _is_logged_in, login, logout, get_institutions_urls
from etiket_client.settings.user_settings import user_settings

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QTimer, QVariant

try:
    import win32gui
    import win32con
except ImportError:
    pass

import logging

logger = logging.getLogger(__name__)

class login_manager(QObject):
    loginChanged = pyqtSignal(name="loginChanged")
    institutionsChanged = pyqtSignal()
    _is_loggedIn = False
    _is_online = False
    
    def __init__(self, parent: 'QObject | None' = None):
        super().__init__(parent)
        
        self._is_online = check_internet_connection()
        
        if not self._is_online:
            print("Host is offline. Please check your internet connection.")
        if self._is_online:
            self.institutions_urls = get_institutions_urls()
            self._is_loggedIn = _is_logged_in()

            self.login_status_timer = QTimer()
            self.login_status_timer.setInterval(5*1000)
            self.login_status_timer.timeout.connect(self.__check_state)
            self.login_status_timer.start()        
    
    @pyqtProperty(bool, notify=loginChanged)
    def loggedIn(self):
        return self._is_loggedIn

    @pyqtProperty(QVariant, notify=institutionsChanged)
    def institutions(self):
        return list(self.institutions_urls.keys())
    
    @pyqtSlot(result = str)
    def getCurrentUser(self):
        return user_settings.user_name

    def __check_state(self):
        try:
            is_logged_in = _is_logged_in()
            # Update the login state if it has changed
            if is_logged_in != self._is_loggedIn:
                self._is_loggedIn = is_logged_in
                self.loginChanged.emit()

            # try:
            #     # Bring the settings manager window to the foreground if it exists
            #     hwnd = win32gui.FindWindow(None, "eTiKet settings manager")
            #     if hwnd:
            #         win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            #         win32gui.SetForegroundWindow(hwnd)
            # except Exception as e:
            #     logger.error("Error bringing settings manager window to foreground: %s", e)
        except Exception:
            pass
    
    def change_state(self, _is_loggedIn):
        if self._is_loggedIn == _is_loggedIn:
            return
        self._is_loggedIn = _is_loggedIn
        self.loginChanged.emit()

    @pyqtSlot(str, str, str, result=bool)
    def login(self, username, password, institution):
        try:
            login(username, password, self.institutions_urls[institution])
            self.change_state(True)
            return True
        except Exception as e:
            print("Login in failed. Please try again.")
            print(e)
            return False

    @pyqtSlot()
    def logout(self):
        logout()
        self.change_state(False)