from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta
from helper.urlHelper import is_valid_domain
import requests
from PyQt6.QtWebEngineWidgets import QWebEngineView
from addressBar import AddressBar
try:
    from main import Main
except ImportError:
    pass


class NormalTab(QWidget):
    def __init__(self, url="about:blank"):
        super().__init__()

        self.layout = QVBoxLayout()

        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))
        self.layout.addWidget(self.toolbar)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(qta.icon("fa5s.chevron-left")))
        self.toolbar.addWidget(self.back_button)

        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon(qta.icon("fa5s.chevron-right")))
        self.toolbar.addWidget(self.forward_button)

        self.reload_button = QPushButton()
        self.reload_button.setIcon(QIcon(qta.icon("fa5s.redo-alt")))
        self.toolbar.addWidget(self.reload_button)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon(qta.icon("fa5s.home")))
        self.toolbar.addWidget(self.stop_button)

        self.incognito_button = QPushButton()
        self.incognito_button.setIcon(QIcon(qta.icon("fa5s.hat-cowboy")))
        self.toolbar.addWidget(self.incognito_button)


        self.url_bar = AddressBar()
        self.url_bar.setPlaceholderText("Enter URL or search term")
        self.url_bar.setText(url)
        self.toolbar.addWidget(self.url_bar)

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)

        self.setLayout(self.layout)

        self.back_button.clicked.connect(self.webview.back)
        self.forward_button.clicked.connect(self.webview.forward)
        self.reload_button.clicked.connect(self.webview.reload)
        self.stop_button.clicked.connect(self.webview.stop)
        self.incognito_button.clicked.connect(self.open_incognito_tab)

        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.webview.load(QUrl(url))

        self.webview.urlChanged.connect(self.update_url)
        self.webview.page().titleChanged.connect(self.update_title)

        self.icon = QMovie('resources/images/spinner.gif')
        self.icon.frameChanged.connect(self.set_icon)
        self.webview.page().loadStarted.connect(self.start_loading)
        self.webview.page().loadFinished.connect(self.stop_loading)

        # self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # self.webview.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        # self.webview.page().profile().settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        # self.webview.page().profile().settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

    def open_incognito_tab(self):
        self.parent().parent().parent().open_new_incognito_window()

    def start_loading(self):
        self.icon.start()

    def stop_loading(self):
        self.icon.stop()
        self.icon.jumpToFrame(0)
        self.set_icon()
        self.update_tab_icon()
    def set_icon(self):
        self.parent().parent().setTabIcon(self.parent().indexOf(self), QIcon(self.icon.currentPixmap()))

    def update_title(self, title):
        # Update the title of the tab to match the web view's title
        self.parent().parent().setTabText(self.parent().indexOf(self), title)
    def update_tab_icon(self):
        # get the favicon of the website
        url = self.webview.url().toString()
        if not url.startswith('http'):
            return
        domain = url.split('/')[2]
        favicon_url = f'https://www.google.com/s2/favicons?domain={domain}'
        response = requests.get(favicon_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        # set the tab icon
        icon = QIcon(pixmap)
        # icon.addPixmap(response.content)
        self.parent().parent().setTabIcon(self.parent().indexOf(self), icon)

    def navigate_to_url(self):
        url_text = self.url_bar.text().strip()
        print(url_text)     
        is_valid = is_valid_domain(url_text)
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            if is_valid:
                url_text = "http://" + url_text
            else:
                # Construct a Google search URL with the entered query
                url_text = "https://www.google.com/search?q=" + url_text.replace(" ", "+")

        url = QUrl(url_text)

        self.webview.load(url)
        self.url_bar.clearFocus()
    def update_url(self, q):
        url = q.toString()
        # url_obj = QUrl(url)
        # url_obj.setQuery("")  # remove query parameters
        if '?' in url:
            url = url.split('?')[0]
        self.url_bar.setText(url)