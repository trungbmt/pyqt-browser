from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import *
import qtawesome as qta
from helper.urlHelper import is_valid_domain
import sys
import requests
from helper.googleSuggestModel import GoogleSuggestModel
import asyncio
from PyQt6.QtNetwork import QNetworkProxy
from PyQt6.QtWidgets import QApplication, QMainWindow
from incognitoTab import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile

# for key in Qt.Key.__dict__.items():
#     print(key[0])