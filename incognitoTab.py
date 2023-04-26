from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import QWebEngineProfile
import qtawesome as qta
from PyQt6.QtNetwork import QNetworkProxy
from normalTab import NormalTab


class IncognitoTab(NormalTab):
    def __init__(self, url=""):
        
        super(IncognitoTab, self).__init__(url)
        self.layout = QVBoxLayout()
        self.webview.page().loadStarted.disconnect()
        self.webview.page().loadFinished.disconnect()
        self.webview.page().titleChanged.disconnect()

        self.vpn_button = QPushButton()
        self.vpn_button.setIcon(QIcon(qta.icon("fa5s.globe")))
        self.vpn_button.clicked.connect(self.enableProxy)

        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.removeAction(self.toolbar.actions()[3])
        self.toolbar.addWidget(self.vpn_button)

        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search term")
        self.url_bar.setText(url)
        self.toolbar.addWidget(self.url_bar)
        
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        profile = QWebEngineProfile()



    def enableProxy(self):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.ProxyType.HttpProxy)
        proxy.setHostName("159.89.203.35")
        proxy.setPort(3128)
        QNetworkProxy.setApplicationProxy(proxy)
        # QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.DefaultProxy))
