#!/Users/ryanshen/Documents/A-workingfilewithp3.11/.venv/bin/python
# -*- coding: utf-8 -*-
# -*- encoding:UTF-8 -*-
# coding=utf-8
# coding:utf-8

import codecs
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QSystemTrayIcon, QMenu, QComboBox, QDialog,
                             QMenuBar, QFrame, QFileDialog, QRubberBand,
                             QPlainTextEdit, QTabWidget, QTextEdit,
                             QGraphicsOpacityEffect, QCheckBox, QListView, QListWidget,
                             QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QObjectCleanupHandler, QStringListModel, QTimer, QThread, QPoint, QSize, pyqtSignal, QEvent, QObject
from PyQt6.QtGui import QAction, QIcon, QColor, QCursor, QGuiApplication, QTextCursor, QImage, QPainter
import PyQt6.QtGui
import sys
import webbrowser
import os
from pathlib import Path
import re
import jieba
from pypinyin import lazy_pinyin
import markdown2
import datetime
import subprocess
import shutil
import mistune
import urllib3
import logging
import requests
import html2text
from bs4 import BeautifulSoup
import threading
import numpy as np
import easyocr
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
# try:
#     import bibtexparser
#     from bibtexparser.bparser import BibTexParser
#     from bibtexparser.customization import convert_to_unicode
#     from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
#     from citeproc import formatter
#     from citeproc.source.json import CiteProcJSON
# except Exception:
#     missing_formats = []

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

BasePath = '/Applications/Strawberry.app/Contents/Resources/'
#BasePath = ''  # test

def reset_newarchive_path():
    with open(BasePath + 'newarchivepath.txt', 'w', encoding='utf-8') as f0:
        f0.write('')


reset_newarchive_path()

INSP_BACKUP_LIMIT_FILE = os.path.join(BasePath, 'insp_backup_limit.txt')
DEFAULT_INSP_BACKUP_LIMIT = 50

def load_inspiration_backup_limit():
    if not os.path.exists(INSP_BACKUP_LIMIT_FILE):
        save_inspiration_backup_limit(DEFAULT_INSP_BACKUP_LIMIT)
        return DEFAULT_INSP_BACKUP_LIMIT
    try:
        value = int(codecs.open(INSP_BACKUP_LIMIT_FILE, 'r', encoding='utf-8').read().strip())
        return value if value > 0 else DEFAULT_INSP_BACKUP_LIMIT
    except Exception:
        return DEFAULT_INSP_BACKUP_LIMIT


def save_inspiration_backup_limit(limit):
    try:
        value = int(limit)
        if value <= 0:
            value = DEFAULT_INSP_BACKUP_LIMIT
    except Exception:
        value = DEFAULT_INSP_BACKUP_LIMIT
    with open(INSP_BACKUP_LIMIT_FILE, 'w', encoding='utf-8') as fp:
        fp.write(str(value))
    return value

APP_DIR = os.path.join(str(Path.home()), "StrawberryAppPath")
OCR_LANG_FILE = os.path.join(APP_DIR, "ocr_language.txt")
OCR_LANGUAGE_OPTIONS = [
    ("Simplified Chinese + English", "ch_sim+en"),
    ("Japanese + English", "ja+en"),
    ("Abaza", "abq"),
    ("Adyghe", "ady"),
    ("Afrikaans", "af"),
    ("Angika", "ang"),
    ("Arabic", "ar"),
    ("Assamese", "as"),
    ("Avar", "ava"),
    ("Azerbaijani", "az"),
    ("Belarusian", "be"),
    ("Bulgarian", "bg"),
    ("Bihari", "bh"),
    ("Bhojpuri", "bho"),
    ("Bengali", "bn"),
    ("Bosnian", "bs"),
    ("Simplified Chinese", "ch_sim"),
    ("Traditional Chinese", "ch_tra"),
    ("Chechen", "che"),
    ("Czech", "cs"),
    ("Welsh", "cy"),
    ("Danish", "da"),
    ("Dargwa", "dar"),
    ("German", "de"),
    ("English", "en"),
    ("Spanish", "es"),
    ("Estonian", "et"),
    ("Persian (Farsi)", "fa"),
    ("French", "fr"),
    ("Irish", "ga"),
    ("Goan Konkani", "gom"),
    ("Hindi", "hi"),
    ("Croatian", "hr"),
    ("Hungarian", "hu"),
    ("Indonesian", "id"),
    ("Ingush", "inh"),
    ("Icelandic", "is"),
    ("Italian", "it"),
    ("Japanese", "ja"),
    ("Kabardian", "kbd"),
    ("Kannada", "kn"),
    ("Korean", "ko"),
    ("Kurdish", "ku"),
    ("Latin", "la"),
    ("Lak", "lbe"),
    ("Lezghian", "lez"),
    ("Lithuanian", "lt"),
    ("Latvian", "lv"),
    ("Magahi", "mah"),
    ("Maithili", "mai"),
    ("Maori", "mi"),
    ("Mongolian", "mn"),
    ("Marathi", "mr"),
    ("Malay", "ms"),
    ("Maltese", "mt"),
    ("Nepali", "ne"),
    ("Newari", "new"),
    ("Dutch", "nl"),
    ("Norwegian", "no"),
    ("Occitan", "oc"),
    ("Pali", "pi"),
    ("Polish", "pl"),
    ("Portuguese", "pt"),
    ("Romanian", "ro"),
    ("Russian", "ru"),
    ("Serbian (cyrillic)", "rs_cyrillic"),
    ("Serbian (latin)", "rs_latin"),
    ("Nagpuri", "sck"),
    ("Slovak", "sk"),
    ("Slovenian", "sl"),
    ("Albanian", "sq"),
    ("Swedish", "sv"),
    ("Swahili", "sw"),
    ("Tamil", "ta"),
    ("Tabassaran", "tab"),
    ("Telugu", "te"),
    ("Thai", "th"),
    ("Tajik", "tjk"),
    ("Tagalog", "tl"),
    ("Turkish", "tr"),
    ("Uyghur", "ug"),
    ("Ukranian", "uk"),
    ("Urdu", "ur"),
    ("Uzbek", "uz"),
    ("Vietnamese", "vi"),
]


def ensure_app_dir():
    if not os.path.exists(APP_DIR):
        os.mkdir(APP_DIR)
    return APP_DIR


def load_ocr_language_code():
    ensure_app_dir()
    if not os.path.exists(OCR_LANG_FILE):
        with open(OCR_LANG_FILE, 'w', encoding='utf-8') as fp:
            fp.write('en')
        return 'en'
    code = codecs.open(OCR_LANG_FILE, 'r', encoding='utf-8').read().strip()
    codes = {item[1] for item in OCR_LANGUAGE_OPTIONS}
    return code if code in codes else 'en'


def save_ocr_language_code(code):
    ensure_app_dir()
    with open(OCR_LANG_FILE, 'w', encoding='utf-8') as fp:
        fp.write(code)

# Create the icon
icon = QIcon(BasePath + "strmenu.icns")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()

action3 = QAction("📔 Let's collect!")
menu.addAction(action3)

action4 = QAction("⚙️ Settings")
menu.addAction(action4)

menu.addSeparator()

action5 = QAction("🔕 Focus mode!")
menu.addAction(action5)
action5.setCheckable(True)

action6 = QAction("🔏 Editor mode!")
menu.addAction(action6)
action6.setCheckable(True)

action7 = QAction("📺 RealTime mode!")
menu.addAction(action7)
action7.setCheckable(True)

action10 = QAction("📚 Compact mode!")
menu.addAction(action10)
action10.setCheckable(True)

menu.addSeparator()

action2 = QAction("🆕 Check for Updates")
menu.addAction(action2)

action1 = QAction("ℹ️ About")
menu.addAction(action1)

menu.addSeparator()

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

# create a system menu
button_action = QAction("&Let's collect!")
btna2 = QAction("&Focus mode!")
btna2.setCheckable(True)
btna3 = QAction("&Editor mode!")
btna3.setCheckable(True)
btna4 = QAction("&Pin!")
btna4.setCheckable(True)
btna5 = QAction("&RealTime mode!")
btna5.setCheckable(True)
btna6 = QAction("&Inspiration!")
btna6.setCheckable(True)
sysmenu = QMenuBar()
file_menu = sysmenu.addMenu("&Actions")
file_menu.addAction(button_action)
file_menu.addAction(btna2)
file_menu.addAction(btna3)
file_menu.addAction(btna5)
file_menu.addAction(btna6)
file_menu.addAction(btna4)


class window_about(QWidget):  # 增加说明页面(About)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # 说明页面内信息
        self.setUpMainWindow()
        self.resize(400, 410)
        self.center()
        self.setWindowTitle('About')
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        widg1 = QWidget()
        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'strmenu.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumWidth(100)
        l1.setMaximumHeight(100)
        l1.setScaledContents(True)
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l1)
        blay1.addStretch()
        widg1.setLayout(blay1)

        widg2 = QWidget()
        lbl0 = QLabel('Strawberry', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(20)
        lbl0.setFont(font)
        blay2 = QHBoxLayout()
        blay2.setContentsMargins(0, 0, 0, 0)
        blay2.addStretch()
        blay2.addWidget(lbl0)
        blay2.addStretch()
        widg2.setLayout(blay2)

        widg3 = QWidget()
        lbl1 = QLabel('Version 2.0.12', self)
        blay3 = QHBoxLayout()
        blay3.setContentsMargins(0, 0, 0, 0)
        blay3.addStretch()
        blay3.addWidget(lbl1)
        blay3.addStretch()
        widg3.setLayout(blay3)

        widg4 = QWidget()
        lbl2 = QLabel('This app is open-sourced.', self)
        blay4 = QHBoxLayout()
        blay4.setContentsMargins(0, 0, 0, 0)
        blay4.addStretch()
        blay4.addWidget(lbl2)
        blay4.addStretch()
        widg4.setLayout(blay4)

        widg5 = QWidget()
        lbl3 = QLabel('Thanks for your love🤟.', self)
        blay5 = QHBoxLayout()
        blay5.setContentsMargins(0, 0, 0, 0)
        blay5.addStretch()
        blay5.addWidget(lbl3)
        blay5.addStretch()
        widg5.setLayout(blay5)

        widg6 = QWidget()
        lbl4 = QLabel('本软件开源，', self)
        blay6 = QHBoxLayout()
        blay6.setContentsMargins(0, 0, 0, 0)
        blay6.addStretch()
        blay6.addWidget(lbl4)
        blay6.addStretch()
        widg6.setLayout(blay6)

        widg7 = QWidget()
        lbl5 = QLabel('感谢您的喜爱！', self)
        blay7 = QHBoxLayout()
        blay7.setContentsMargins(0, 0, 0, 0)
        blay7.addStretch()
        blay7.addWidget(lbl5)
        blay7.addStretch()
        widg7.setLayout(blay7)

        widg8 = QWidget()
        bt1 = QPushButton('The Author', self)
        bt1.setMaximumHeight(20)
        bt1.setMinimumWidth(100)
        bt1.clicked.connect(self.intro)
        bt2 = QPushButton('Github Page', self)
        bt2.setMaximumHeight(20)
        bt2.setMinimumWidth(100)
        bt2.clicked.connect(self.homepage)
        blay8 = QHBoxLayout()
        blay8.setContentsMargins(0, 0, 0, 0)
        blay8.addStretch()
        blay8.addWidget(bt1)
        blay8.addWidget(bt2)
        blay8.addStretch()
        widg8.setLayout(blay8)

        bt7 = QPushButton('Buy me a cup of coffee☕', self)
        bt7.setMaximumHeight(20)
        bt7.setMinimumWidth(215)
        bt7.clicked.connect(self.coffee)

        widg8_5 = QWidget()
        blay8_5 = QHBoxLayout()
        blay8_5.setContentsMargins(0, 0, 0, 0)
        blay8_5.addStretch()
        blay8_5.addWidget(bt7)
        blay8_5.addStretch()
        widg8_5.setLayout(blay8_5)

        widg9 = QWidget()
        bt3 = QPushButton('🍪\n¥5', self)
        bt3.setMaximumHeight(50)
        bt3.setMinimumHeight(50)
        bt3.setMinimumWidth(50)
        bt3.clicked.connect(self.donate)
        bt4 = QPushButton('🥪\n¥10', self)
        bt4.setMaximumHeight(50)
        bt4.setMinimumHeight(50)
        bt4.setMinimumWidth(50)
        bt4.clicked.connect(self.donate2)
        bt5 = QPushButton('🍜\n¥20', self)
        bt5.setMaximumHeight(50)
        bt5.setMinimumHeight(50)
        bt5.setMinimumWidth(50)
        bt5.clicked.connect(self.donate3)
        bt6 = QPushButton('🍕\n¥50', self)
        bt6.setMaximumHeight(50)
        bt6.setMinimumHeight(50)
        bt6.setMinimumWidth(50)
        bt6.clicked.connect(self.donate4)
        blay9 = QHBoxLayout()
        blay9.setContentsMargins(0, 0, 0, 0)
        blay9.addStretch()
        blay9.addWidget(bt3)
        blay9.addWidget(bt4)
        blay9.addWidget(bt5)
        blay9.addWidget(bt6)
        blay9.addStretch()
        widg9.setLayout(blay9)

        widg10 = QWidget()
        lbl6 = QLabel('© 2025 Yixiang SHEN. All rights reserved.', self)
        blay10 = QHBoxLayout()
        blay10.setContentsMargins(0, 0, 0, 0)
        blay10.addStretch()
        blay10.addWidget(lbl6)
        blay10.addStretch()
        widg10.setLayout(blay10)

        main_h_box = QVBoxLayout()
        main_h_box.addWidget(widg1)
        main_h_box.addWidget(widg2)
        main_h_box.addWidget(widg3)
        main_h_box.addWidget(widg4)
        main_h_box.addWidget(widg5)
        main_h_box.addWidget(widg6)
        main_h_box.addWidget(widg7)
        main_h_box.addWidget(widg8)
        main_h_box.addWidget(widg8_5)
        main_h_box.addWidget(widg9)
        main_h_box.addWidget(widg10)
        main_h_box.addStretch()
        self.setLayout(main_h_box)

    def intro(self):
        webbrowser.open('https://github.com/Ryan-the-hito/Ryan-the-hito')

    def homepage(self):
        webbrowser.open('https://github.com/Ryan-the-hito/Strawberry')

    def coffee(self):
        webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

    def donate(self):
        dlg = CustomDialog()
        dlg.exec()

    def donate2(self):
        dlg = CustomDialog2()
        dlg.exec()

    def donate3(self):
        dlg = CustomDialog3()
        dlg.exec()

    def donate4(self):
        dlg = CustomDialog4()
        dlg.exec()

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def activate(self):  # 设置窗口显示
        self.show()


class CustomDialog(QDialog):  # (About1)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.setWindowTitle("Thank you for your support!")
        self.center()
        self.resize(400, 390)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        widge_all = QWidget()
        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'wechat5.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumSize(160, 240)
        l1.setScaledContents(True)
        l2 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'alipay5.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l2.setMaximumSize(160, 240)
        l2.setScaledContents(True)
        bk = QHBoxLayout()
        bk.setContentsMargins(0, 0, 0, 0)
        bk.addWidget(l1)
        bk.addWidget(l2)
        widge_all.setLayout(bk)

        m1 = QLabel('Thank you for your kind support! 😊', self)
        m2 = QLabel('I will write more interesting apps! 🥳', self)

        widg_c = QWidget()
        bt1 = QPushButton('Thank you!', self)
        bt1.setMaximumHeight(20)
        bt1.setMinimumWidth(100)
        bt1.clicked.connect(self.cancel)
        bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
        bt2.setMaximumHeight(20)
        bt2.setMinimumWidth(260)
        bt2.clicked.connect(self.coffee)
        blay8 = QHBoxLayout()
        blay8.setContentsMargins(0, 0, 0, 0)
        blay8.addStretch()
        blay8.addWidget(bt1)
        blay8.addWidget(bt2)
        blay8.addStretch()
        widg_c.setLayout(blay8)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widge_all)
        self.layout.addWidget(m1)
        self.layout.addWidget(m2)
        self.layout.addStretch()
        self.layout.addWidget(widg_c)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def coffee(self):
        webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog2(QDialog):  # (About2)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.setWindowTitle("Thank you for your support!")
        self.center()
        self.resize(400, 390)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        widge_all = QWidget()
        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'wechat10.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumSize(160, 240)
        l1.setScaledContents(True)
        l2 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'alipay10.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l2.setMaximumSize(160, 240)
        l2.setScaledContents(True)
        bk = QHBoxLayout()
        bk.setContentsMargins(0, 0, 0, 0)
        bk.addWidget(l1)
        bk.addWidget(l2)
        widge_all.setLayout(bk)

        m1 = QLabel('Thank you for your kind support! 😊', self)
        m2 = QLabel('I will write more interesting apps! 🥳', self)

        widg_c = QWidget()
        bt1 = QPushButton('Thank you!', self)
        bt1.setMaximumHeight(20)
        bt1.setMinimumWidth(100)
        bt1.clicked.connect(self.cancel)
        bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
        bt2.setMaximumHeight(20)
        bt2.setMinimumWidth(260)
        bt2.clicked.connect(self.coffee)
        blay8 = QHBoxLayout()
        blay8.setContentsMargins(0, 0, 0, 0)
        blay8.addStretch()
        blay8.addWidget(bt1)
        blay8.addWidget(bt2)
        blay8.addStretch()
        widg_c.setLayout(blay8)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widge_all)
        self.layout.addWidget(m1)
        self.layout.addWidget(m2)
        self.layout.addStretch()
        self.layout.addWidget(widg_c)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def coffee(self):
        webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog3(QDialog):  # (About3)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.setWindowTitle("Thank you for your support!")
        self.center()
        self.resize(400, 390)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        widge_all = QWidget()
        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'wechat20.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumSize(160, 240)
        l1.setScaledContents(True)
        l2 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'alipay20.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l2.setMaximumSize(160, 240)
        l2.setScaledContents(True)
        bk = QHBoxLayout()
        bk.setContentsMargins(0, 0, 0, 0)
        bk.addWidget(l1)
        bk.addWidget(l2)
        widge_all.setLayout(bk)

        m1 = QLabel('Thank you for your kind support! 😊', self)
        m2 = QLabel('I will write more interesting apps! 🥳', self)

        widg_c = QWidget()
        bt1 = QPushButton('Thank you!', self)
        bt1.setMaximumHeight(20)
        bt1.setMinimumWidth(100)
        bt1.clicked.connect(self.cancel)
        bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
        bt2.setMaximumHeight(20)
        bt2.setMinimumWidth(260)
        bt2.clicked.connect(self.coffee)
        blay8 = QHBoxLayout()
        blay8.setContentsMargins(0, 0, 0, 0)
        blay8.addStretch()
        blay8.addWidget(bt1)
        blay8.addWidget(bt2)
        blay8.addStretch()
        widg_c.setLayout(blay8)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widge_all)
        self.layout.addWidget(m1)
        self.layout.addWidget(m2)
        self.layout.addStretch()
        self.layout.addWidget(widg_c)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def coffee(self):
        webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog4(QDialog):  # (About4)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.setWindowTitle("Thank you for your support!")
        self.center()
        self.resize(400, 390)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        widge_all = QWidget()
        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'wechat50.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumSize(160, 240)
        l1.setScaledContents(True)
        l2 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'alipay50.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l2.setMaximumSize(160, 240)
        l2.setScaledContents(True)
        bk = QHBoxLayout()
        bk.setContentsMargins(0, 0, 0, 0)
        bk.addWidget(l1)
        bk.addWidget(l2)
        widge_all.setLayout(bk)

        m1 = QLabel('Thank you for your kind support! 😊', self)
        m2 = QLabel('I will write more interesting apps! 🥳', self)

        widg_c = QWidget()
        bt1 = QPushButton('Thank you!', self)
        bt1.setMaximumHeight(20)
        bt1.setMinimumWidth(100)
        bt1.clicked.connect(self.cancel)
        bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
        bt2.setMaximumHeight(20)
        bt2.setMinimumWidth(260)
        bt2.clicked.connect(self.coffee)
        blay8 = QHBoxLayout()
        blay8.setContentsMargins(0, 0, 0, 0)
        blay8.addStretch()
        blay8.addWidget(bt1)
        blay8.addWidget(bt2)
        blay8.addStretch()
        widg_c.setLayout(blay8)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widge_all)
        self.layout.addWidget(m1)
        self.layout.addWidget(m2)
        self.layout.addStretch()
        self.layout.addWidget(widg_c)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def coffee(self):
        webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

    def cancel(self):  # 设置取消键的功能
        self.close()


class window_update(QWidget):  # 增加更新页面（Check for Updates）
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # 说明页面内信息

        self.lbl = QLabel('Current Version: v2.0.12', self)
        self.lbl.move(30, 45)

        lbl0 = QLabel('Download Update:', self)
        lbl0.move(30, 75)

        lbl1 = QLabel('Latest Version:', self)
        lbl1.move(30, 15)

        self.lbl2 = QLabel('', self)
        self.lbl2.move(122, 15)

        bt1 = QPushButton('Google Drive', self)
        bt1.setFixedWidth(120)
        bt1.clicked.connect(self.upd)
        bt1.move(150, 75)

        bt2 = QPushButton('Dropbox', self)
        bt2.setFixedWidth(120)
        bt2.clicked.connect(self.upd2)
        bt2.move(150, 105)

        self.resize(300, 150)
        self.center()
        self.setWindowTitle('Strawberry Updates')
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def upd(self):
        webbrowser.open('https://drive.google.com/drive/folders/16fkKeIjqUYgC_3S-iGG5aeD_KCY025lg?usp=sharing')

    def upd2(self):
        webbrowser.open('https://www.dropbox.com/scl/fo/ysb0qqhuz5yr7ikaqzjzx/h?rlkey=cl6zrxjtu7qp3yt82edgbd5fg&dl=0')

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def activate(self):  # 设置窗口显示
        self.show()
        self.checkupdate()

    def checkupdate(self):
        targetURL = 'https://github.com/Ryan-the-hito/Strawberry/releases'
        try:
            # Fetch the HTML content from the URL
            urllib3.disable_warnings()
            logging.captureWarnings(True)
            s = requests.session()
            s.keep_alive = False  # 关闭多余连接
            response = s.get(targetURL, verify=False)
            response.encoding = 'utf-8'
            html_content = response.text
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            # Remove all images from the parsed HTML
            for img in soup.find_all("img"):
                img.decompose()
            # Convert the parsed HTML to plain text using html2text
            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            text_maker.ignore_images = True
            plain_text = text_maker.handle(str(soup))
            # Convert the plain text to UTF-8
            plain_text_utf8 = plain_text.encode(response.encoding).decode("utf-8")

            for i in range(10):
                plain_text_utf8 = plain_text_utf8.replace('\n\n\n\n', '\n\n')
                plain_text_utf8 = plain_text_utf8.replace('\n\n\n', '\n\n')
                plain_text_utf8 = plain_text_utf8.replace('   ', ' ')
                plain_text_utf8 = plain_text_utf8.replace('  ', ' ')

            pattern2 = re.compile(r'(v\d+\.\d+\.\d+)\sLatest')
            result = pattern2.findall(plain_text_utf8)
            result = ''.join(result)
            nowversion = self.lbl.text().replace('Current Version: ', '')
            if result == nowversion:
                alertupdate = result + '. You are up to date!'
                self.lbl2.setText(alertupdate)
                self.lbl2.adjustSize()
            else:
                alertupdate = result + ' is ready!'
                self.lbl2.setText(alertupdate)
                self.lbl2.adjustSize()
        except:
            alertupdate = 'No Intrenet'
            self.lbl2.setText(alertupdate)
            self.lbl2.adjustSize()


class CustomDialog_warn(QDialog):  # 提醒检查路径
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(500, 490)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        l0 = QLabel('Please grant Strawberry with Accessibility and Full Disk Access\n\n'
                    'in System Preferences, then open Settings and set your paths!', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(15)
        l0.setFont(font)

        l1 = QLabel(self)
        png = PyQt6.QtGui.QPixmap(BasePath + 'setpath.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        l1.setMaximumSize(425, 250)
        l1.setScaledContents(True)

        btn_can = QPushButton('Got it!', self)
        btn_can.clicked.connect(self.cancel)
        btn_can.setFixedWidth(150)
        btn_can.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #FFFFFF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #000000
                ''')

        w0 = QWidget()
        blay0 = QHBoxLayout()
        blay0.setContentsMargins(0, 0, 0, 0)
        blay0.addStretch()
        blay0.addWidget(l0)
        blay0.addStretch()
        w0.setLayout(blay0)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l1)
        blay1.addStretch()
        w1.setLayout(blay1)

        w2 = QWidget()
        blay2 = QHBoxLayout()
        blay2.setContentsMargins(0, 0, 0, 0)
        blay2.addStretch()
        blay2.addWidget(btn_can)
        blay2.addStretch()
        w2.setLayout(blay2)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(0, 0, 0, 0)
        blay3.addStretch()
        blay3.addWidget(w0)
        blay3.addStretch()
        blay3.addWidget(w1)
        blay3.addStretch()
        blay3.addWidget(w2)
        blay3.addStretch()
        w3.setLayout(blay3)
        w3.setStyleSheet('''
            border: 1px solid #ECECEC;
            background: #ECECEC;
            border-radius: 9px;
        ''')

        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        w3.setGraphicsEffect(op)
        w3.setAutoFillBackground(True)

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_pro(QDialog):  # problem
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        self.listview = QListView()
        self.listview.setObjectName('Select')
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        path_pro = codecs.open(BasePath + 'path_pro.txt', 'r', encoding='utf-8').read()
        if path_pro != '':
            self.list_dir = os.listdir(path_pro)
            self.list_dir.sort()
            while '.DS_Store' in self.list_dir:
                self.list_dir.remove('.DS_Store')
            while '' in self.list_dir:
                self.list_dir.remove('')
            for i in range(len(self.list_dir)):
                self.list_dir[i] = self.list_dir[i].replace('.md', '')
            self.listModel.setStringList(self.list_dir)
        if path_pro == '':
            self.list_dir = ['Empty path']
            self.listModel.setStringList(self.list_dir)

        btn_can = QPushButton('Select', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.listview)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        if self.list_dir != [] and self.listview.currentIndex().isValid():
            w5.w3.text11.setPlainText(self.listModel.itemData(self.listview.currentIndex())[0])
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_excerpt(QDialog):  # excerpt
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        self.listview = QListView()
        self.listview.setObjectName('Select')
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        nowtext = w5.w3.text.toPlainText()
        if nowtext != '':
            pattern2 = re.compile(r'- (\[.*?\]「.*?」)\n')
            self.list_dir = pattern2.findall(nowtext)
            #if list_dir != []:
            self.list_dir.sort()
            while '' in self.list_dir:
                self.list_dir.remove('')
            self.listModel.setStringList(self.list_dir)
        if nowtext == '':
            self.list_dir = ['No excerpts']
            self.listModel.setStringList(self.list_dir)

        btn_can = QPushButton('Select', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.listview)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        if self.list_dir != [] and self.listview.currentIndex().isValid():
            select_text = self.listModel.itemData(self.listview.currentIndex())[0]
            pattern2 = re.compile(r'「(.*?)」')
            result = ''.join(pattern2.findall(select_text))
            w5.w3.text21.setPlainText(result)
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_con(QDialog):  # concept
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        self.listview = QListView()
        self.listview.setObjectName('Select')
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        path_pro = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if path_pro != '':
            self.list_dir = os.listdir(path_pro)
            self.list_dir.sort()
            while '.DS_Store' in self.list_dir:
                self.list_dir.remove('.DS_Store')
            while '' in self.list_dir:
                self.list_dir.remove('')
            for i in range(len(self.list_dir)):
                self.list_dir[i] = self.list_dir[i].replace('.md', '')
            self.listModel.setStringList(self.list_dir)
        if path_pro == '':
            self.list_dir = ['Empty path']
            self.listModel.setStringList(self.list_dir)

        btn_can = QPushButton('Select', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.listview)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        if self.list_dir != [] and self.listview.currentIndex().isValid():
            w5.w3.lec1.setText(self.listModel.itemData(self.listview.currentIndex())[0])
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_the(QDialog):  # theory
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        self.listview = QListView()
        self.listview.setObjectName('Select')
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        path_pro = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
        if path_pro != '':
            self.list_dir = os.listdir(path_pro)
            self.list_dir.sort()
            while '.DS_Store' in self.list_dir:
                self.list_dir.remove('.DS_Store')
            while '' in self.list_dir:
                self.list_dir.remove('')
            for i in range(len(self.list_dir)):
                self.list_dir[i] = self.list_dir[i].replace('.md', '')
            self.listModel.setStringList(self.list_dir)
        if path_pro == '':
            self.list_dir = ['Empty path']
            self.listModel.setStringList(self.list_dir)

        btn_can = QPushButton('Select', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.listview)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        if self.list_dir != [] and self.listview.currentIndex().isValid():
            w5.w3.lec0.setText(self.listModel.itemData(self.listview.currentIndex())[0])
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_met(QDialog):  # method
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        self.listview = QListView()
        self.listview.setObjectName('Select')
        self.listModel = QStringListModel()
        self.listview.setModel(self.listModel)
        path_pro = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if path_pro != '':
            self.list_dir = os.listdir(path_pro)
            self.list_dir.sort()
            while '.DS_Store' in self.list_dir:
                self.list_dir.remove('.DS_Store')
            while '' in self.list_dir:
                self.list_dir.remove('')
            for i in range(len(self.list_dir)):
                self.list_dir[i] = self.list_dir[i].replace('.md', '')
            self.listModel.setStringList(self.list_dir)
        if path_pro == '':
            self.list_dir = ['Empty path']
            self.listModel.setStringList(self.list_dir)

        btn_can = QPushButton('Select', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.listview)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        if self.list_dir != [] and self.listview.currentIndex().isValid():
            w5.w3.lem1.setText(self.listModel.itemData(self.listview.currentIndex())[0])
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_archive(QDialog):  # archive
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien Full-text database'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)

        l0 = QLabel('Full-text database', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(30)
        l0.setFont(font)

        self.btnnew = QPushButton('', self)
        self.btnnew.clicked.connect(self.newfile)
        self.btnnew.setFixedSize(100, 100)
        self.btnnew.setStyleSheet('''
            QPushButton{
            background-color: transparent;
            border-radius: 4px;
            padding: 1px;
            color: #000000;
            image: url(/Applications/Strawberry.app/Contents/Resources/archive.png);
            border: 3px dashed grey;
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        self.btnold = QPushButton('', self)
        self.btnold.clicked.connect(self.linkfile)
        self.btnold.setFixedSize(100, 100)
        self.btnold.setStyleSheet('''
            QPushButton{
            background-color: transparent;
            border-radius: 4px;
            padding: 1px;
            color: #000000;
            image: url(/Applications/Strawberry.app/Contents/Resources/archive.png);
            border: 3px dashed grey;
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        self.btnopen = QPushButton('', self)
        self.btnopen.clicked.connect(self.openfile)
        self.btnopen.setFixedSize(100, 100)
        self.btnopen.setStyleSheet('''
            QPushButton{
            background-color: transparent;
            border-radius: 4px;
            padding: 1px;
            color: #000000;
            image: url(/Applications/Strawberry.app/Contents/Resources/archive.png);
            border: 3px dashed grey;
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        l1 = QLabel('''Create a note from a local file''', self)

        l2 = QLabel('''Link this note to a local file''', self)

        l3 = QLabel('''Open the file linked to this note''', self)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w0 = QWidget()
        blay0 = QHBoxLayout()
        blay0.setContentsMargins(0, 0, 0, 0)
        blay0.addStretch()
        blay0.addWidget(l0)
        blay0.addStretch()
        w0.setLayout(blay0)

        w0_1 = QWidget()
        blay0_1 = QHBoxLayout()
        blay0_1.setContentsMargins(0, 0, 0, 0)
        blay0_1.addStretch()
        blay0_1.addWidget(self.btnnew)
        blay0_1.addStretch()
        w0_1.setLayout(blay0_1)

        w1_1 = QWidget()
        blay1_1 = QHBoxLayout()
        blay1_1.setContentsMargins(0, 0, 0, 0)
        blay1_1.addStretch()
        blay1_1.addWidget(l1)
        blay1_1.addStretch()
        w1_1.setLayout(blay1_1)

        w0_2 = QWidget()
        blay0_2 = QHBoxLayout()
        blay0_2.setContentsMargins(0, 0, 0, 0)
        blay0_2.addStretch()
        blay0_2.addWidget(self.btnold)
        blay0_2.addStretch()
        w0_2.setLayout(blay0_2)

        w1_2 = QWidget()
        blay1_2 = QHBoxLayout()
        blay1_2.setContentsMargins(0, 0, 0, 0)
        blay1_2.addStretch()
        blay1_2.addWidget(l2)
        blay1_2.addStretch()
        w1_2.setLayout(blay1_2)

        w0_3 = QWidget()
        blay0_3 = QHBoxLayout()
        blay0_3.setContentsMargins(0, 0, 0, 0)
        blay0_3.addStretch()
        blay0_3.addWidget(self.btnopen)
        blay0_3.addStretch()
        w0_3.setLayout(blay0_3)

        w1_3 = QWidget()
        blay1_3 = QHBoxLayout()
        blay1_3.setContentsMargins(0, 0, 0, 0)
        blay1_3.addStretch()
        blay1_3.addWidget(l3)
        blay1_3.addStretch()
        w1_3.setLayout(blay1_3)

        if w5.w3.le1.text() == '':
            w0_1.setVisible(True)
            w1_1.setVisible(True)
            w0_2.setVisible(False)
            w1_2.setVisible(False)
            w0_3.setVisible(False)
            w1_3.setVisible(False)
        if w5.w3.le1.text() != '':
            tarname3 = w5.w3.le3.text()
            tarname8 = w5.w3.le8.text()
            if tarname3 != '' and w5.w3.le4.text() != '' and w5.w3.le4_1.text() != '':
                fulldir3 = os.path.join(fulldir2, tarname3)
                tarnamea = w5.w3.le4.text()
                fulldira = os.path.join(fulldir3, tarnamea)
                tarnameb = w5.w3.le4_1.text()
                fulldirb = os.path.join(fulldira, tarnameb)

                if os.path.exists(fulldirb):
                    self.list_dir = os.listdir(fulldirb)
                    self.list_dir.sort()
                    while '.DS_Store' in self.list_dir:
                        self.list_dir.remove('.DS_Store')
                    while '' in self.list_dir:
                        self.list_dir.remove('')
                    for i in range(len(self.list_dir)):
                        self.list_dir[i] = re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir[i])
                    if w5.w3.le1.text() in self.list_dir:
                        w0_1.setVisible(False)
                        w1_1.setVisible(False)
                        w0_2.setVisible(False)
                        w1_2.setVisible(False)
                        w0_3.setVisible(True)
                        w1_3.setVisible(True)
                    if not w5.w3.le1.text() in self.list_dir:
                        w0_1.setVisible(False)
                        w1_1.setVisible(False)
                        w0_2.setVisible(True)
                        w1_2.setVisible(True)
                        w0_3.setVisible(False)
                        w1_3.setVisible(False)
                if not os.path.exists(fulldirb):
                    w0_1.setVisible(False)
                    w1_1.setVisible(False)
                    w0_2.setVisible(True)
                    w1_2.setVisible(True)
                    w0_3.setVisible(False)
                    w1_3.setVisible(False)
            if tarname3 == '' and tarname8 != '':
                fulldir8 = os.path.join(fulldir2, tarname8)

                if os.path.exists(fulldir8):
                    self.list_dir2 = os.listdir(fulldir8)
                    self.list_dir2.sort()
                    while '.DS_Store' in self.list_dir2:
                        self.list_dir2.remove('.DS_Store')
                    while '' in self.list_dir2:
                        self.list_dir2.remove('')
                    for i in range(len(self.list_dir2)):
                        self.list_dir2[i] = re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i])
                    if w5.w3.le1.text() in self.list_dir2:
                        w0_1.setVisible(False)
                        w1_1.setVisible(False)
                        w0_2.setVisible(False)
                        w1_2.setVisible(False)
                        w0_3.setVisible(True)
                        w1_3.setVisible(True)
                    if not w5.w3.le1.text() in self.list_dir2:
                        w0_1.setVisible(False)
                        w1_1.setVisible(False)
                        w0_2.setVisible(True)
                        w1_2.setVisible(True)
                        w0_3.setVisible(False)
                        w1_3.setVisible(False)
                if not os.path.exists(fulldir8):
                    w0_1.setVisible(False)
                    w1_1.setVisible(False)
                    w0_2.setVisible(True)
                    w1_2.setVisible(True)
                    w0_3.setVisible(False)
                    w1_3.setVisible(False)
            if tarname3 == '' and tarname8 == '':
                w0_1.setVisible(False)
                w1_1.setVisible(False)
                w0_2.setVisible(True)
                w1_2.setVisible(True)
                w0_3.setVisible(False)
                w1_3.setVisible(False)

        w1_all = QWidget()
        blay1_all = QVBoxLayout()
        blay1_all.setContentsMargins(0, 0, 0, 0)
        blay1_all.addStretch()
        blay1_all.addWidget(w0_1)
        blay1_all.addWidget(w0_2)
        blay1_all.addWidget(w0_3)
        blay1_all.addStretch()
        blay1_all.addWidget(w1_1)
        blay1_all.addWidget(w1_2)
        blay1_all.addWidget(w1_3)
        blay1_all.addStretch()
        w1_all.setLayout(blay1_all)

        w2 = QWidget()
        blay2 = QHBoxLayout()
        blay2.setContentsMargins(0, 0, 0, 0)
        blay2.addStretch()
        blay2.addWidget(btn_no)
        blay2.addStretch()
        w2.setLayout(blay2)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(w0)
        blay3.addWidget(w1_all)
        blay3.addWidget(w2)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def newfile(self):
        home_dir = str(Path.home())
        file_name, ok = QFileDialog.getOpenFileName(self, "Open File", home_dir)
        if file_name != '':
            tole1 = file_name.split('/')[-1]
            tole1 = re.sub(r"\.[a-zA-Z0-9]+$", '', tole1)
            w5.w3.le1.setText(tole1)
            with open(BasePath + 'newarchivepath.txt', 'w', encoding='utf-8') as f0:
                f0.write(file_name)
            self.close()

    def linkfile(self):
        home_dir = str(Path.home())
        archivepath_1 = "Documents"
        fulldir1 = os.path.join(home_dir, archivepath_1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        archivepath_2 = 'Obsidien Full-text database'
        fulldir2 = os.path.join(fulldir1, archivepath_2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)

        archiveempty, ok = QFileDialog.getOpenFileName(self, "Open File", home_dir)
        if archiveempty != '' and not w5.w3.le1.isEnabled():
            tole1 = archiveempty.split('/')[-1]
            patternx = re.compile(r'\.[a-zA-Z0-9]+$')
            result_ex = patternx.findall(tole1)
            tole2 = ''.join(result_ex)
            archiveempty_new = archiveempty.replace(tole1, w5.w3.le1.text()) + tole2
            os.rename(archiveempty, archiveempty_new)
            archiveempty = archiveempty_new
            if w5.w3.le3.text() != '' and w5.w3.le4.text() != '' and w5.w3.le4_1.text() != '':
                tarname3 = w5.w3.le3.text()
                fulldir3 = os.path.join(fulldir2, tarname3)
                tarnamea = w5.w3.le4.text()
                fulldira = os.path.join(fulldir3, tarnamea)
                tarnameb = w5.w3.le4_1.text()
                fulldirb = os.path.join(fulldira, tarnameb)
                if not os.path.exists(fulldirb):
                    os.makedirs(fulldirb)
                shutil.copy(archiveempty, fulldirb)
                os.remove(archiveempty)
            if w5.w3.le3.text() == '' and w5.w3.le8.text() != '':
                tarname8 = w5.w3.le8.text()
                fulldir8 = os.path.join(fulldir2, tarname8)
                if not os.path.exists(fulldir8):
                    os.makedirs(fulldir8)
                shutil.copy(archiveempty, fulldir8)
                os.remove(archiveempty)
            if w5.w3.le3.text() == '' and w5.w3.le8.text() == '':
                if w5.w3.leweb3.text() != '':
                    tarname8 = w5.w3.le1.text() + '[web]'
                    fulldir8 = os.path.join(fulldir2, tarname8)
                    if not os.path.exists(fulldir8):
                        os.makedirs(fulldir8)
                    shutil.copy(archiveempty, fulldir8)
                    os.remove(archiveempty)
                if w5.w3.leweb3.text() == '' and w5.w3.leweb8.text() != '':
                    tarname8 = w5.w3.leweb8.text()
                    fulldir8 = os.path.join(fulldir2, tarname8)
                    if not os.path.exists(fulldir8):
                        os.makedirs(fulldir8)
                    shutil.copy(archiveempty, fulldir8)
                    os.remove(archiveempty)
                if w5.w3.leweb3.text() == '' and w5.w3.leweb8.text() == '':
                    tarname8 = 'NEW FOLDER'
                    fulldir8 = os.path.join(fulldir2, tarname8)
                    if not os.path.exists(fulldir8):
                        os.makedirs(fulldir8)
                    shutil.copy(archiveempty, fulldir8)
                    os.remove(archiveempty)
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                 f"The target folder is not named so it is by default moved to the 'NEW FOLDER'.")
            self.close()

    def openfile(self):
        home_dir = str(Path.home())
        archivepath_1 = "Documents"
        fulldir1 = os.path.join(home_dir, archivepath_1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        archivepath_2 = 'Obsidien Full-text database'
        fulldir2 = os.path.join(fulldir1, archivepath_2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)

        if w5.w3.le3.text() != '' and w5.w3.le4.text() != '' and w5.w3.le4_1.text() != '':
            tarname3 = w5.w3.le3.text()
            fulldir3 = os.path.join(fulldir2, tarname3)
            tarnamea = w5.w3.le4.text()
            fulldira = os.path.join(fulldir3, tarnamea)
            tarnameb = w5.w3.le4_1.text()
            fulldirb = os.path.join(fulldira, tarnameb)

            if os.path.exists(fulldirb):
                self.list_dir2 = os.listdir(fulldirb)
                self.list_dir2.sort()
                while '.DS_Store' in self.list_dir2:
                    self.list_dir2.remove('.DS_Store')
                while '' in self.list_dir2:
                    self.list_dir2.remove('')
                self.newlist = []
                for i in range(len(self.list_dir2)):
                    self.newlist.append(re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i]))
                if w5.w3.le1.text() in self.newlist:
                    for t in range(len(self.list_dir2)):
                        if w5.w3.le1.text() in self.list_dir2[t]:
                            endfull = os.path.join(fulldirb, self.list_dir2[t])
                            os.system("open '{}'".format(endfull))
                if not w5.w3.le1.text() in self.newlist:
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                f"The target folder does not contain the correct file. Please check again!")
            if not os.path.exists(fulldir1):
                CMD = '''
                    on run argv
                        display notification (item 2 of argv) with title (item 1 of argv)
                    end run'''
                self.notify(CMD, "Strawberry: Your Literature Collector",
                            f"The target folder does not contain the correct file. Please check again!")
        if w5.w3.le3.text() == '' and w5.w3.le8.text() != '':
            tarname8 = w5.w3.le8.text()
            fulldir8 = os.path.join(fulldir2, tarname8)

            if os.path.exists(fulldir8):
                self.list_dir2 = os.listdir(fulldir8)
                self.list_dir2.sort()
                while '.DS_Store' in self.list_dir2:
                    self.list_dir2.remove('.DS_Store')
                while '' in self.list_dir2:
                    self.list_dir2.remove('')
                self.newlist = []
                for i in range(len(self.list_dir2)):
                    self.newlist.append(re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i]))
                if w5.w3.le1.text() in self.newlist:
                    for t in range(len(self.list_dir2)):
                        if w5.w3.le1.text() in self.list_dir2[t]:
                            endfull = os.path.join(fulldir8, self.list_dir2[t])
                            os.system("open '{}'".format(endfull))
                if not w5.w3.le1.text() in self.newlist:
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                f"The target folder does not contain the correct file. Please check again!")
            if not os.path.exists(fulldir8):
                CMD = '''
                    on run argv
                        display notification (item 2 of argv) with title (item 1 of argv)
                    end run'''
                self.notify(CMD, "Strawberry: Your Literature Collector",
                            f"The target folder does not contain the correct file. Please check again!")
        if w5.w3.le3.text() == '' and w5.w3.le8.text() == '':
            if w5.w3.leweb3.text() != '':
                tarname8 = w5.w3.le1.text() + '[web]'
                fulldir8 = os.path.join(fulldir2, tarname8)

                if os.path.exists(fulldir8):
                    self.list_dir2 = os.listdir(fulldir8)
                    self.list_dir2.sort()
                    while '.DS_Store' in self.list_dir2:
                        self.list_dir2.remove('.DS_Store')
                    while '' in self.list_dir2:
                        self.list_dir2.remove('')
                    self.newlist = []
                    for i in range(len(self.list_dir2)):
                        self.newlist.append(re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i]))
                    if w5.w3.le1.text() in self.newlist:
                        for t in range(len(self.list_dir2)):
                            if w5.w3.le1.text() in self.list_dir2[t]:
                                endfull = os.path.join(fulldir8, self.list_dir2[t])
                                os.system("open '{}'".format(endfull))
                    if not w5.w3.le1.text() in self.newlist:
                        CMD = '''
                            on run argv
                                display notification (item 2 of argv) with title (item 1 of argv)
                            end run'''
                        self.notify(CMD, "Strawberry: Your Literature Collector",
                                    f"The target folder does not contain the correct file. Please check again!")
                if not os.path.exists(fulldir8):
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                f"The target folder does not contain the correct file. Please check again!")
            if w5.w3.leweb3.text() == '' and w5.w3.leweb8.text() != '':
                tarname8 = w5.w3.leweb8.text()
                fulldir8 = os.path.join(fulldir2, tarname8)

                if os.path.exists(fulldir8):
                    self.list_dir2 = os.listdir(fulldir8)
                    self.list_dir2.sort()
                    while '.DS_Store' in self.list_dir2:
                        self.list_dir2.remove('.DS_Store')
                    while '' in self.list_dir2:
                        self.list_dir2.remove('')
                    self.newlist = []
                    for i in range(len(self.list_dir2)):
                        self.newlist.append(re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i]))
                    if w5.w3.le1.text() in self.newlist:
                        for t in range(len(self.list_dir2)):
                            if w5.w3.le1.text() in self.list_dir2[t]:
                                endfull = os.path.join(fulldir8, self.list_dir2[t])
                                os.system("open '{}'".format(endfull))
                    if not w5.w3.le1.text() in self.newlist:
                        CMD = '''
                            on run argv
                                display notification (item 2 of argv) with title (item 1 of argv)
                            end run'''
                        self.notify(CMD, "Strawberry: Your Literature Collector",
                                    f"The target folder does not contain the correct file. Please check again!")
                if not os.path.exists(fulldir8):
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                f"The target folder does not contain the correct file. Please check again!")
            if w5.w3.leweb3.text() == '' and w5.w3.leweb8.text() == '':
                tarname8 = 'NEW FOLDER'
                fulldir8 = os.path.join(fulldir2, tarname8)

                if os.path.exists(fulldir8):
                    self.list_dir2 = os.listdir(fulldir8)
                    self.list_dir2.sort()
                    while '.DS_Store' in self.list_dir2:
                        self.list_dir2.remove('.DS_Store')
                    while '' in self.list_dir2:
                        self.list_dir2.remove('')
                    self.newlist = []
                    for i in range(len(self.list_dir2)):
                        self.newlist.append(re.sub(r"\.[a-zA-Z0-9]+$", '', self.list_dir2[i]))
                    if w5.w3.le1.text() in self.newlist:
                        for t in range(len(self.list_dir2)):
                            if w5.w3.le1.text() in self.list_dir2[t]:
                                endfull = os.path.join(fulldir8, self.list_dir2[t])
                                os.system("open '{}'".format(endfull))
                    if not w5.w3.le1.text() in self.newlist:
                        CMD = '''
                                                        on run argv
                                                            display notification (item 2 of argv) with title (item 1 of argv)
                                                        end run'''
                        self.notify(CMD, "Strawberry: Your Literature Collector",
                                    f"The target folder does not contain the correct file. Please check again!")
                if not os.path.exists(fulldir8):
                    CMD = '''
                        on run argv
                            display notification (item 2 of argv) with title (item 1 of argv)
                        end run'''
                    self.notify(CMD, "Strawberry: Your Literature Collector",
                                f"The target folder does not contain the correct file. Please check again!")
        self.close()

    def notify(self, CMD, title, text):
        subprocess.call(['osascript', '-e', CMD, title, text])

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_cite(QDialog):  # cite1
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(500, 200)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        l0 = QLabel('Other references mentioned', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(30)
        l0.setFont(font)

        self.citething = QLineEdit(self)
        self.citething.setPlaceholderText('Notably mentioned title here')

        btn_can = QPushButton('Add', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w0 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l0)
        blay1.addStretch()
        w0.setLayout(blay1)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(w0)
        blay3.addWidget(self.citething)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if w5.w3.le1.text() != '' and self.citething.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 != '':
                if w5.w3.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                tarname1 = str(w5.w3.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = ''
                part_n = '\n' + get_rst
                if w5.w3.text12.toPlainText() != '' and w5.w3.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + 'Notable mentions: ' + str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text())))) + '\n'
                if w5.w3.text12.toPlainText() == '' and w5.w3.text13.toPlainText() != '':
                    part1 = '\n\t- ' + 'Notable mentions: ' + str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text())))) + '\n'
                if w5.w3.text12.toPlainText() != '' and w5.w3.text13.toPlainText() == '':
                    part1 = '\n\t- ' + 'Notable mentions: ' + str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text())))) + '\n'
                if w5.w3.text12.toPlainText() == '' and w5.w3.text13.toPlainText() == '':
                    part1 = '\n- ' + 'Notable mentions: ' + str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text())))) + '\n'
                if w5.w3.le1.text() != '' and self.citething.text() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                w5.w3.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # w5.w3.text.setStyleSheet('color:red')
            else:
                tarnameend = str(w5.w3.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if w5.w3.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    w5.w3.text.setPlainText(contend)
                    if w5.w3.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    w5.w3.text.ensureCursorVisible()  # 游标可用
                    cursor = w5.w3.text.textCursor()  # 设置游标
                    pos = int(len(w5.w3.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    w5.w3.text.setTextCursor(cursor)  # 滚动到游标位置
                    if w5.w3.text.verticalScrollBar().maximum() != 0:
                        proportion = w5.w3.text.verticalScrollBar().value() / w5.w3.text.verticalScrollBar().maximum()
                        tar_pro = int(w5.w3.real1.verticalScrollBar().maximum() * proportion)
                        w5.w3.real1.verticalScrollBar().setValue(tar_pro)

            itemcited = self.citething.text() + '.md'
            fulldircite = os.path.join(fulldira, itemcited)
            with open(fulldircite, 'w', encoding='utf-8') as f0:
                f0.write('')

            self.citething.clear()

            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_cite2(QDialog):  # cite2
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(500, 200)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        l0 = QLabel('Other references mentioned', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(30)
        l0.setFont(font)

        self.citething = QLineEdit(self)
        self.citething.setPlaceholderText('Notably mentioned title here')

        btn_can = QPushButton('Add', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w0 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l0)
        blay1.addStretch()
        w0.setLayout(blay1)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(w0)
        blay3.addWidget(self.citething)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if w5.w3.lec1.text() != '' and self.citething.text() != '':
            path2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if path2 != '':
                tarname2 = str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lec1.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                part1 = '\n\t- Notable mentions: ' + str(w5.w3.default_clean(self.citething.text()))
                part2 = ''
                if w5.w3.le1.text() != '':
                    part2 = '【from ' + str(w5.w3.le1.text()) + '】'
                part3 = ''
                if w5.w3.le8.text() != '':
                    part3 = '【from ' + str(w5.w3.le8.text()) + '】'
                if w5.w3.lec1.text() != '' and self.citething.text() != '':
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                w5.w3.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lec1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if w5.w3.lec1.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    w5.w3.text_s2.setPlainText(contend2)
                    w5.w3.text_s2.ensureCursorVisible()  # 游标可用
                    cursor = w5.w3.text_s2.textCursor()  # 设置游标
                    pos = len(w5.w3.text_s2.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    w5.w3.text_s2.setTextCursor(cursor)  # 滚动到游标位置

            itemcited = self.citething.text() + '.md'
            fulldircite = os.path.join(fulldira, itemcited)
            with open(fulldircite, 'w', encoding='utf-8') as f0:
                f0.write('')

            self.citething.clear()

            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_cite3(QDialog):  # cite3
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(500, 200)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        l0 = QLabel('Other references mentioned', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(30)
        l0.setFont(font)

        self.citething = QLineEdit(self)
        self.citething.setPlaceholderText('Notably mentioned title here')

        btn_can = QPushButton('Add', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w0 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l0)
        blay1.addStretch()
        w0.setLayout(blay1)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(w0)
        blay3.addWidget(self.citething)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if w5.w3.lec0.text() != '' and self.citething.text() != '':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 != '':
                tarname2 = str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Notable mentions: ' + str(
                        w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text()))))
                    part2 = ''
                    if w5.w3.le1.text() != '':
                        part2 = '【from ' + str(w5.w3.le1.text()) + '】'
                    part3 = ''
                    if w5.w3.le8.text() != '':
                        part3 = '【from ' + str(w5.w3.le8.text()) + '】'
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Notable mentions: ' + str(
                        w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(self.citething.text()))))
                    part2 = ''
                    if w5.w3.le1.text() != '':
                        part2 = '【from ' + str(w5.w3.le1.text()) + '】'
                    part3 = ''
                    if w5.w3.le8.text() != '':
                        part3 = '【from ' + str(w5.w3.le8.text()) + '】'
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                w5.w3.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(
                    w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if w5.w3.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    w5.w3.text_s3.setPlainText(contend2)
                    w5.w3.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = w5.w3.text_s3.textCursor()  # 设置游标
                    pos = len(w5.w3.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    w5.w3.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            itemcited = self.citething.text() + '.md'
            fulldircite = os.path.join(fulldira, itemcited)
            with open(fulldircite, 'w', encoding='utf-8') as f0:
                f0.write('')

            self.citething.clear()

            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()


class CustomDialog_list_cite4(QDialog):  # cite4
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(500, 200)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        l0 = QLabel('Other references mentioned', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(30)
        l0.setFont(font)

        self.citething = QLineEdit(self)
        self.citething.setPlaceholderText('Notably mentioned title here')

        btn_can = QPushButton('Add', self)
        btn_can.clicked.connect(self.list_pro)
        btn_can.setFixedWidth(120)

        btn_no = QPushButton('Cancel', self)
        btn_no.clicked.connect(self.cancel)
        btn_no.setFixedWidth(120)

        w0 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addStretch()
        blay1.addWidget(l0)
        blay1.addStretch()
        w0.setLayout(blay1)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(btn_can)
        blay1.addWidget(btn_no)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(w0)
        blay3.addWidget(self.citething)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def list_pro(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if w5.w3.lem1.text() != '' and self.citething.text() != '':
            path2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if path2 != '':
                tarname2 = str(w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lem1.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                part1 = '\n\t- Notable mentions: ' + str(w5.w3.default_clean(self.citething.text()))
                part2 = ''
                if w5.w3.le1.text() != '':
                    part2 = '【from ' + str(w5.w3.le1.text()) + '】'
                part3 = ''
                if w5.w3.le8.text() != '':
                    part3 = '【from ' + str(w5.w3.le8.text()) + '】'
                with open(fulldir2, 'a', encoding='utf-8') as f2:
                    f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                w5.w3.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(
                    w5.w3.default_clean(w5.w3.cleanlinebreak(w5.w3.cleancitmak(w5.w3.lem1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                w5.w3.text_s4.setPlainText(contend2)
                w5.w3.text_s4.ensureCursorVisible()  # 游标可用
                cursor = w5.w3.text_s4.textCursor()  # 设置游标
                pos = len(w5.w3.text_s4.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                w5.w3.text_s4.setTextCursor(cursor)  # 滚动到游标位置

            itemcited = self.citething.text() + '.md'
            fulldircite = os.path.join(fulldira, itemcited)
            with open(fulldircite, 'w', encoding='utf-8') as f0:
                f0.write('')

            self.citething.clear()

            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()
    

class CustomDialog_edit_reference(QDialog):  # cite1
    def __init__(self):
        super().__init__()
        self.bib_entries = []
        self.inline_entries = []
        self.initUI()

    def initUI(self):
        self.setUpMainWindow()
        self.center()
        self.resize(400, 400)
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):

        self.warn_lbl = QLabel('Edits here are temporary: changes will be overwritten the next time you update/insert citations. Finish all edits before modifying here.', self)
        self.warn_lbl.setWordWrap(True)
        self.warn_lbl.setVisible(False)
        self.editor = QTextEdit(self)
        self.editor.setPlainText(codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read())
        self.editor.setVisible(False)

        self.view_switch = QComboBox(self)
        self.view_switch.addItems(['BibTeX', 'In-text'])
        self.view_switch.currentIndexChanged.connect(self.toggle_view_mode)

        self.bib_list = QListWidget(self)
        self.bib_view = QTextEdit(self)
        self.bib_view.setReadOnly(False)
        self.bib_view.setPlaceholderText('BibTeX snippet')
        self.inline_view = QLineEdit(self)
        self.inline_view.setReadOnly(False)
        self.inline_view.setPlaceholderText('Inline citation')
        self.btn_delete_entry = QPushButton('Delete', self)
        self.btn_delete_entry.setStyleSheet('color: red')
        self.btn_delete_entry.clicked.connect(self.mark_delete_entry)
        self.btn_delete_entry.setEnabled(False)
        self.bib_list.itemSelectionChanged.connect(self.on_bib_selection)
        self.bib_view.textChanged.connect(self.on_bib_text_changed)
        self.inline_view.textChanged.connect(self.on_inline_text_changed)

        self.load_bib_and_inline()
        
        btn_save = QPushButton('Save', self)
        btn_save.clicked.connect(self.save_refs)
        btn_cancel = QPushButton('Cancel', self)
        btn_cancel.clicked.connect(self.cancel)

        w1 = QWidget()
        blay1 = QHBoxLayout()
        blay1.setContentsMargins(0, 0, 0, 0)
        blay1.addWidget(self.btn_delete_entry)
        blay1.addWidget(btn_save)
        blay1.addWidget(btn_cancel)
        w1.setLayout(blay1)

        w3 = QWidget()
        blay3 = QVBoxLayout()
        blay3.setContentsMargins(20, 20, 20, 20)
        blay3.addWidget(self.warn_lbl)
        blay3.addWidget(self.view_switch)
        bib_area = QHBoxLayout()
        bib_left = QVBoxLayout()
        # bib_left.addWidget(QLabel('Bib entries:', self))
        bib_left.addWidget(self.bib_list)
        # bib_left.addWidget(self.btn_delete_entry)
        bib_right = QVBoxLayout()
        # bib_right.addWidget(QLabel('BibTeX snippet:', self))
        bib_right.addWidget(self.inline_view)
        bib_right.addWidget(self.bib_view)
        # bib_right.addWidget(QLabel('Inline citation (selected format):', self))
        bib_area.addLayout(bib_left)
        bib_area.addLayout(bib_right)
        bib_wrap = QWidget()
        bib_wrap.setLayout(bib_area)
        blay3.addWidget(bib_wrap)
        blay3.addWidget(self.editor)
        blay3.addWidget(w1)
        w3.setLayout(blay3)
        w3.setObjectName("Main")

        blayend = QHBoxLayout()
        blayend.setContentsMargins(0, 0, 0, 0)
        blayend.addWidget(w3)
        self.setLayout(blayend)
    
    def save_refs(self):
        if self.view_switch.currentIndex() == 0:
            # BibTeX mode
            reply = QMessageBox.question(
                self,
                'Confirm save',
                'Save changes to BibTeX and inline citations?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            title = ''
            try:
                title = w5.w3._get_citation_title_key()
            except Exception:
                title = w5.w3.leii1.text() if hasattr(w5, 'w3') else ''
            script_dir = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if title == '' or script_dir == '':
                self.close()
                return
            cit_dir = os.path.join(script_dir, 'StrawberryCitations', title)
            os.makedirs(cit_dir, exist_ok=True)
            bib_file = os.path.join(cit_dir, f"{title}.bib")
            # write cached bib entries
            try:
                with open(bib_file, 'w', encoding='utf-8') as bf:
                    bf.write('\n\n'.join(self.bib_entries))
            except Exception:
                pass
            # clear existing format files
            for fname in os.listdir(cit_dir):
                if fname.startswith(f"{title}-") and fname.endswith('.txt'):
                    try:
                        os.remove(os.path.join(cit_dir, fname))
                    except Exception:
                        continue
            # regenerate formats per entry
            for entry in self.bib_entries:
                try:
                    w5.w3._generate_csl_citations(title, script_dir, latest_bib_block=entry)
                except Exception:
                    # ensure an empty inline file exists for the selected format if generation failed
                    home_dir = str(Path.home())
                    base_dir = os.path.join(home_dir, "StrawberryAppPath")
                    csl_dir = os.path.join(base_dir, "CitationFormat")
                    selected_file = os.path.join(csl_dir, "selected_format.txt")
                    fmt = ''
                    try:
                        fmt = codecs.open(selected_file, 'r', encoding='utf-8').read().strip()
                    except Exception:
                        fmt = ''
                    if fmt == '':
                        fmt = 'quickcite'
                    if fmt.lower().startswith('quick'):
                        fmt = 'quickcite'
                    if fmt.lower().endswith('.csl'):
                        fmt = fmt[:-4]
                    inline_file = os.path.join(script_dir, 'StrawberryCitations', title, f"{title}-{fmt}-in.txt")
                    try:
                        with open(inline_file, 'a', encoding='utf-8') as inf:
                            inf.write('')
                    except Exception:
                        pass
                    continue
            # override inline file with edited inline entries for selected format
            home_dir = str(Path.home())
            base_dir = os.path.join(home_dir, "StrawberryAppPath")
            csl_dir = os.path.join(base_dir, "CitationFormat")
            selected_file = os.path.join(csl_dir, "selected_format.txt")
            fmt = ''
            try:
                fmt = codecs.open(selected_file, 'r', encoding='utf-8').read().strip()
            except Exception:
                fmt = ''
            if fmt == '':
                fmt = 'quickcite'
            if fmt.lower().startswith('quick'):
                fmt = 'quickcite'
            if fmt.lower().endswith('.csl'):
                fmt = fmt[:-4]
            inline_file = os.path.join(cit_dir, f"{title}-{fmt}-in.txt")
            try:
                with open(inline_file, 'w', encoding='utf-8') as inf:
                    inf.write('\n'.join(self.inline_entries))
            except Exception:
                pass
            # rebuild path_ref from selected format and write back to md
            try:
                w5.w3._apply_selected_format_to_refs()
            except Exception:
                pass
        else:
            # In-text mode
            with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as fp:
                fp.write(self.editor.toPlainText())
            if w5.w3.leii1.text() != '':
                path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                if path1 != '':
                    tarname1 = str(w5.w3.leii1.text()) + ".md"
                    fulldir1 = os.path.join(path1, tarname1)
                    body_text = w5.w3._strip_inspiration_body(w5.w3.textii2.toPlainText()) if w5.w3.insp_show_full else w5.w3.textii2.toPlainText()
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(w5.w3._compose_inspiration_file(body_text))
        self.close()

    def center(self):  # 设置窗口居中
        # Get the primary screen's geometry
        screen_geometry = self.screen().availableGeometry()

        # Calculate the centered position
        x_center = int((screen_geometry.width() / 2) - (self.width() / 4))
        y_center = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center position
        self.setGeometry(QRect(x_center, y_center, self.width(), self.height()))

    def cancel(self):  # 设置取消键的功能
        self.close()

    def load_bib_and_inline(self):
        self.bib_entries = []
        self.inline_entries = []
        self.bib_list.clear()
        try:
            title = w5.w3._get_citation_title_key()
        except Exception:
            title = w5.w3.leii1.text() if hasattr(w5, 'w3') else ''
        script_dir = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if title == '' or script_dir == '':
            return
        bib_file = os.path.join(script_dir, 'StrawberryCitations', title, f"{title}.bib")
        if os.path.exists(bib_file):
            try:
                bib_txt = codecs.open(bib_file, 'r', encoding='utf-8').read()
                import re as _re
                matches = list(_re.finditer(r'@.*?\n}\s*', bib_txt, _re.DOTALL))
                for m in matches:
                    self.bib_entries.append(m.group(0).strip())
                for i in range(len(self.bib_entries)):
                    self.bib_list.addItem(str(i + 1))
            except Exception:
                pass
        # inline entries for selected format
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        csl_dir = os.path.join(base_dir, "CitationFormat")
        selected_file = os.path.join(csl_dir, "selected_format.txt")
        fmt = ''
        try:
            fmt = codecs.open(selected_file, 'r', encoding='utf-8').read().strip()
        except Exception:
            fmt = ''
        if fmt == '':
            fmt = 'quickcite'
        if fmt.lower().startswith('quick'):
            fmt = 'quickcite'
        if fmt.lower().endswith('.csl'):
            fmt = fmt[:-4]
        inline_file = os.path.join(script_dir, 'StrawberryCitations', title, f"{title}-{fmt}-in.txt")
        if os.path.exists(inline_file):
            try:
                lines = codecs.open(inline_file, 'r', encoding='utf-8').read().split('\n')
                self.inline_entries = [l for l in lines if l.strip() != '']
            except Exception:
                self.inline_entries = []
        self.btn_delete_entry.setEnabled(False)
        self.bib_view.clear()
        self.inline_view.clear()

    def on_bib_selection(self):
        idx = self.bib_list.currentRow()
        if idx < 0 or idx >= len(self.bib_entries):
            self.btn_delete_entry.setEnabled(False)
            self.bib_view.clear()
            self.inline_view.clear()
            return
        self.btn_delete_entry.setEnabled(True)
        self.bib_view.setPlainText(self.bib_entries[idx])
        if idx < len(self.inline_entries):
            self.inline_view.setText(self.inline_entries[idx])
        else:
            self.inline_view.clear()

    def on_bib_text_changed(self):
        idx = self.bib_list.currentRow()
        if idx >= 0 and idx < len(self.bib_entries):
            self.bib_entries[idx] = self.bib_view.toPlainText()

    def on_inline_text_changed(self):
        idx = self.bib_list.currentRow()
        if idx >= 0:
            while len(self.inline_entries) <= idx:
                self.inline_entries.append('')
            self.inline_entries[idx] = self.inline_view.text()

    def mark_delete_entry(self):
        idx = self.bib_list.currentRow()
        try:
            title = w5.w3._get_citation_title_key()
        except Exception:
            title = w5.w3.leii1.text() if hasattr(w5, 'w3') else ''
        script_dir = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if idx < 0 or idx >= len(self.bib_entries) or title == '' or script_dir == '':
            return
        reply = QMessageBox.question(
            self,
            'Confirm delete',
            'This will mark the selected BibTeX entry as DELETED (placeholder). Continue?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        placeholder = "@article{DELETED,\n  title = {TO_BE_DELETED}\n}\n"
        self.bib_entries[idx] = placeholder
        bib_file = os.path.join(script_dir, 'StrawberryCitations', title, f"{title}.bib")
        try:
            with open(bib_file, 'w', encoding='utf-8') as bf:
                bf.write('\n\n'.join(self.bib_entries))
        except Exception:
            pass
        self.bib_view.setPlainText(placeholder)

    def toggle_view_mode(self, i):
        show_bib = (i == 0)
        show_in = (i != 0)
        self.editor.setVisible(not show_bib)
        self.bib_list.setVisible(show_bib)
        self.bib_view.setVisible(show_bib)
        self.inline_view.setVisible(show_bib)
        self.btn_delete_entry.setVisible(show_bib)
        self.warn_lbl.setVisible(show_in)
        if show_bib:
            self.load_bib_and_inline()


class TimeoutException(Exception):
    pass


class ReaderLoader(QObject):
    """Worker that loads easyocr.Reader on a background thread."""
    finished = pyqtSignal(object, str)

    def __init__(self, languages, model_dir=None):
        super().__init__()
        self.languages = languages
        self.model_dir = model_dir or os.path.join(BasePath, "model")

    def run(self):
        try:
            os.makedirs(self.model_dir, exist_ok=True)
            reader = easyocr.Reader(self.languages, model_storage_directory=self.model_dir)
            self.finished.emit(reader, "")
        except Exception as e:
            self.finished.emit(None, str(e))


class SelectionOverlay(QWidget):
    """Full-screen translucent overlay for selecting a rectangular region."""
    regionSelected = pyqtSignal(QRect)

    def __init__(self, screen_geometry: QRect, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setGeometry(screen_geometry)
        self._screen_geometry = screen_geometry
        self._origin = QPoint()
        self._rubberband = QRubberBand(QRubberBand.Shape.Rectangle, self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 80))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._origin = event.pos()
            self._rubberband.setGeometry(QRect(self._origin, QSize()))
            self._rubberband.show()

    def mouseMoveEvent(self, event):
        if not self._origin.isNull() and self._rubberband.isVisible():
            rect = QRect(self._origin, event.pos()).normalized()
            self._rubberband.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._rubberband.isVisible():
            rect = self._rubberband.geometry()
            global_rect = QRect(
                self._screen_geometry.x() + rect.x(),
                self._screen_geometry.y() + rect.y(),
                rect.width(),
                rect.height(),
            )
            self._rubberband.hide()
            self.regionSelected.emit(global_rect)
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class window3(QWidget):  # 主程序的代码块（Find a dirty word!）
    def __init__(self):
        super().__init__()
        self.dragPosition = self.pos()
        self.insp_show_full = False
        self.insp_updating = False
        self._insp_backup_lock = threading.Lock()
        self.insp_backup_timer = None
        self._last_insp_backup_meta = None  # Track last backup to avoid redundant saves
        self.ocr_reader = None
        self.ocr_reader_loading = False
        self.ocr_reader_thread = None
        self.ocr_overlay = None
        self._ocr_current_screen = None
        self._ocr_target_widget = None
        self._ocr_last_editor = None
        self.ocr_buttons = []
        self._ocr_button_text = {}
        app.installEventFilter(self)
        self.initUI()
        self._start_inspiration_autosave()

        # Monitor screen changes for automatic window size adjustment
        if self.windowHandle():
            self.windowHandle().screenChanged.connect(self._on_screen_changed)

    def initUI(self):  # 设置窗口内布局
        self.setUpMainWindow()
        MOST_WEIGHT = int(self.screen().availableGeometry().width() * 0.75)
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        MINI_WEIGHT = int(self.screen().availableGeometry().width() / 4)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())

        DE_HEIGHT = int(self.screen().availableGeometry().height())
        HALF_HEIGHT = int(self.screen().availableGeometry().height() * 0.5)
        BIGGIST_HEIGHT = int(self.screen().availableGeometry().height())

        self.resize(HALF_WEIGHT, DE_HEIGHT)
        self.move_window2(SCREEN_WEIGHT - 10, self.pos().y())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMinimumSize(MINI_WEIGHT, HALF_HEIGHT)
        self.setMaximumSize(MOST_WEIGHT, BIGGIST_HEIGHT)
        #self.show()
        self.tab_bar.setVisible(False)
        self.cleanup_handler = QObjectCleanupHandler()
        with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
            f0.write(str(self.width()))
        self.new_width = 10
        self.resize(self.new_width, DE_HEIGHT)
        app.setStyleSheet(style_sheet_ori)
        self.pathcheck()
        self.movesysfile()
        self.assigntoall()

    def setUpMainWindow(self):
        self.tab_bar = QTabWidget()
        self.word_tab = QWidget()
        self.art_tab = QWidget()
        self.insp_tab = QWidget()

        self.tab_bar.addTab(self.word_tab, "Expressions")
        self.tab_bar.addTab(self.art_tab, "Articles")
        self.tab_bar.addTab(self.insp_tab, "Inspirations")

        self.btn_00 = QPushButton('', self)
        self.btn_00.clicked.connect(self.pin_a_tab)
        self.btn_00.setFixedHeight(100)
        self.btn_00.setFixedWidth(10)
        self.i = 1

        lbtn = QWidget()
        left_btn = QVBoxLayout()
        left_btn.setContentsMargins(0, 0, 0, 0)
        left_btn.addStretch()
        left_btn.addWidget(self.btn_00)
        left_btn.addStretch()
        lbtn.setLayout(left_btn)

        main_h_box = QHBoxLayout()
        main_h_box.setContentsMargins(0, 0, 0, 0)
        main_h_box.addWidget(lbtn)
        main_h_box.addWidget(self.tab_bar, 1)
        self.setLayout(main_h_box)

        # Call methods that contain the widgets for each tab
        self.wordTab()
        self.artTab()
        self.inspiTab()

    def move_window(self, width, height):
        animation = QPropertyAnimation(self, b"geometry", self)
        animation.setDuration(250)
        # Use current width and height to avoid size changes during animation
        current_w = self.width()
        current_h = self.height()
        new_pos = QRect(width, height, current_w, current_h)
        animation.setEndValue(new_pos)
        animation.start()
        self.i += 1

    def move_window2(self, width, height):
        animation = QPropertyAnimation(self, b"geometry", self)
        animation.setDuration(400)
        new_pos = QRect(width, height, self.width(), self.height())
        animation.setEndValue(new_pos)
        animation.start()

    def _current_screen_geometry(self):
        window_handle = self.windowHandle()
        if window_handle and window_handle.screen():
            return window_handle.screen().availableGeometry()
        geo_center = self.frameGeometry().center()
        screen = QGuiApplication.screenAt(geo_center)
        if screen:
            return screen.availableGeometry()
        screen = QGuiApplication.screenAt(QCursor.pos())
        if screen:
            return screen.availableGeometry()
        if self.screen():
            return self.screen().availableGeometry()
        primary = QGuiApplication.primaryScreen()
        return primary.availableGeometry() if primary else QRect(0, 0, 1440, 900)

    def _on_screen_changed(self, screen):
        """Handle screen changes: automatically adjust window size when moving to different screen or resolution changes"""
        if not screen:
            return

        # Use QTimer to defer reading screen geometry - this ensures we get the LATEST screen data
        # 100ms delay to ensure macOS has fully updated screen geometry after display change
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._handle_screen_change(screen))

    def _handle_screen_change(self, screen):
        """Handle screen change with proper geometry calculation"""
        if not screen:
            return

        # NOW get the screen geometry (after 100ms delay)
        screen_geo = screen.availableGeometry()

        # Debug: Print screen change information
        # print(f"\n=== Screen Changed ===")
        # print(f"Screen: {screen.name()}")
        # print(f"Available Geometry: {screen_geo.width()}x{screen_geo.height()} at ({screen_geo.x()}, {screen_geo.y()})")

        # Recalculate size limits based on new screen
        MOST_WEIGHT = int(screen_geo.width() * 0.75)
        MINI_WEIGHT = int(screen_geo.width() / 4)
        HALF_HEIGHT = int(screen_geo.height() * 0.5)
        BIGGIST_HEIGHT = int(screen_geo.height())

        # Get current dimensions
        current_width = self.width()
        current_height = self.height()
        # print(f"Current window size: {current_width}x{current_height}")

        # Check if window is currently in collapsed state by checking if tab_bar is visible
        # tab_bar is hidden when window is collapsed (only btn_00 visible)
        is_collapsed = not self.tab_bar.isVisible()

        # print(f"Window is currently {'COLLAPSED' if is_collapsed else 'EXPANDED'} (tab_bar visible: {self.tab_bar.isVisible()})")

        # Calculate screen boundaries
        screen_left = screen_geo.x()
        screen_top = screen_geo.y()
        screen_right = screen_left + screen_geo.width()
        screen_bottom = screen_top + screen_geo.height()

        # Calculate new height (always full screen height)
        new_height = BIGGIST_HEIGHT

        if is_collapsed:
            # ===== 折叠状态：btn_00 应该贴在屏幕最右侧中间 =====
            # 窗口很窄(只有btn_00可见)，把它放在屏幕右边缘
            # print("Mode: COLLAPSED - positioning btn_00 at screen right edge")

            # 保持最小宽度约束，允许窄宽度
            self.setMinimumSize(1, HALF_HEIGHT)
            self.setMaximumSize(MOST_WEIGHT, BIGGIST_HEIGHT)

            # 使用self.new_width (10) 作为折叠时的宽度，与初始化和pin_a_tab逻辑一致
            collapsed_width = self.new_width

            # 计算位置：窗口左边缘 = 屏幕右边缘 - 窗口宽度
            # 这样窗口右边缘就贴在屏幕右边缘
            target_x = screen_right - collapsed_width
            target_y = screen_top

            # print(f"Target position: ({target_x}, {target_y})")
            # print(f"Target size: {collapsed_width}x{new_height}")

            # 使用setGeometry一次性设置位置和大小，更可靠
            self.setGeometry(target_x, target_y, collapsed_width, new_height)

        else:
            # ===== 展开状态：窗口右边缘应该与屏幕右边缘对齐 =====
            # print("Mode: EXPANDED - aligning window right edge to screen right edge")

            # 应用正常约束
            self.setMinimumSize(MINI_WEIGHT, HALF_HEIGHT)
            self.setMaximumSize(MOST_WEIGHT, BIGGIST_HEIGHT)

            # 根据新屏幕尺寸重新计算窗口宽度
            # 实时检测当前选中的action来确定mode（与 _toggle_pin_tab 逻辑一致）
            if action10.isChecked():
                mode_key = "compact"
                target_width = int(screen_geo.width() / 4)
            elif action7.isChecked():
                mode_key = "realtime"
                target_width = int(screen_geo.width() * 3 / 4)
            else:
                mode_key = "normal"
                target_width = int(screen_geo.width() / 2)

            # print(f"Using mode: {mode_key} (action10: {action10.isChecked()}, action7: {action7.isChecked()})")

            # 应用最小/最大宽度约束
            target_width = max(MINI_WEIGHT, min(target_width, MOST_WEIGHT))

            # print(f"Calculated target width for mode {mode_key}: {target_width}")

            # 计算位置：窗口左边缘 = 屏幕右边缘 - 窗口宽度
            # 这样窗口右边缘就贴在屏幕右边缘
            target_x = screen_right - target_width
            target_y = screen_top

            # print(f"Target position: ({target_x}, {target_y})")
            # print(f"Target size: {target_width}x{new_height}")

            # 使用setGeometry一次性设置位置和大小，更可靠
            self.setGeometry(target_x, target_y, target_width, new_height)

        # 强制处理事件确保更新
        from PyQt6.QtCore import QCoreApplication
        QCoreApplication.processEvents()

        # 再次强制设置位置，确保窗口真的移动到了目标位置
        # 窗口右边缘应该完全贴在屏幕右边缘
        final_target_x = screen_right - self.width()

        if self.pos().x() != final_target_x:
            # print(f"Position mismatch detected, forcing move to x={final_target_x}")
            self.move(final_target_x, screen_top)
            QCoreApplication.processEvents()

        # 验证最终位置
        # final_pos = self.pos()
        # final_size = self.size()
        # print(f"Final window position: ({final_pos.x()}, {final_pos.y()})")
        # print(f"Final window size: {final_size.width()}x{final_size.height()}")
        # print(f"Window right edge at: x={final_pos.x() + final_size.width()} (screen right edge: {screen_right})")
        # print(f"Distance from right edge: {screen_right - (final_pos.x() + final_size.width())}px")

        # Debug: btn_00 位置
        # btn_pos = self.btn_00.pos()
        # btn_global = self.btn_00.mapToGlobal(btn_pos)
        # print(f"btn_00 position relative to window: ({btn_pos.x()}, {btn_pos.y()})")
        # print(f"btn_00 global position: ({btn_global.x()}, {btn_global.y()})")
        # print(f"btn_00 size: {self.btn_00.width()}x{self.btn_00.height()}")
        # print(f"=== Screen Change Complete ===\n")

    def _apply_screen_resize(self, target_width, target_height, screen_geo, was_collapsed):
        """Helper method to apply resize with proper bounds checking"""
        # print(f"Applying resize to: {target_width}x{target_height} (was_collapsed={was_collapsed})")

        # Apply the resize
        self.resize(target_width, target_height)

        # Force process pending events to ensure resize takes effect
        from PyQt6.QtCore import QCoreApplication
        QCoreApplication.processEvents()

        actual_size = self.size()
        # print(f"Actual window size AFTER resize: {actual_size.width()}x{actual_size.height()}")
        # if actual_size.width() != target_width:
        #     print(f"WARNING: Actual width ({actual_size.width()}) != target width ({target_width})")

        # Ensure window stays within screen bounds (respect x/y offsets)
        left = screen_geo.x()
        top = screen_geo.y()
        right = left + screen_geo.width()
        bottom = top + screen_geo.height()

        new_x = self.pos().x()
        new_y = self.pos().y()

        # Check if window is in collapsed/pinned state (very narrow width)
        # If collapsed, position at screen edge (x = right - 10)
        # If expanded, position so right edge is near screen edge (x = right - width - 3)
        # IMPORTANT: Use actual window width, not target width, in case resize was constrained
        actual_width = self.width()
        COLLAPSED_WIDTH_THRESHOLD = 100  # Consider widths < 100px as "collapsed"
        is_collapsed = actual_width < COLLAPSED_WIDTH_THRESHOLD

        if is_collapsed:
            # Window is collapsed (only btn_00 visible) - pin it to the right edge
            # This ensures btn_00 stays at the screen right edge for easy access
            new_x = right - 10
            # print(f"Window is collapsed (actual_width={actual_width}), pinning to right edge at x={new_x}")
        else:
            # Window is expanded - DO NOT force to right edge
            # btn_00 is at the LEFT side of the window (x=0), so forcing window right
            # would move btn_00 to the left side of screen, which is wrong!
            # Instead, keep current position and only adjust if outside screen bounds
            # print(f"Window is expanded (actual_width={actual_width}), checking bounds only")

            # Only adjust if window extends beyond screen bounds
            if new_x + actual_width > right:
                # Window right edge is off-screen, pull it back
                new_x = right - actual_width - 3
                # print(f"  Adjusting: window extends beyond right edge, moving to x={new_x}")
            elif new_x < left:
                # Window left edge is off-screen, push it right
                new_x = left
                # print(f"  Adjusting: window extends beyond left edge, moving to x={new_x}")
            # else:
                # print(f"  No adjustment needed, keeping position x={new_x}")

        # Ensure vertical position is within bounds
        if new_y + target_height > bottom:
            new_y = bottom - target_height
        if new_y < top:
            new_y = top

        if new_x != self.pos().x() or new_y != self.pos().y():
            # print(f"Moving window to: ({new_x}, {new_y})")
            self.move(new_x, new_y)

        # Verify final position after move
        from PyQt6.QtCore import QCoreApplication
        QCoreApplication.processEvents()
        # final_pos = self.pos()
        # final_geometry = self.geometry()
        # print(f"Final window position: ({final_pos.x()}, {final_pos.y()})")
        # print(f"Final window geometry: {final_geometry.x()}, {final_geometry.y()}, {final_geometry.width()}x{final_geometry.height()}")
        # print(f"Window right edge at: x={final_pos.x() + self.width()} (screen right edge: {right})")
        # print(f"Distance from right edge: {right - (final_pos.x() + self.width())}px")

        # Debug: Check btn_00 position
        # btn_pos = self.btn_00.pos()
        # btn_global = self.btn_00.mapToGlobal(btn_pos)
        # print(f"btn_00 position relative to window: ({btn_pos.x()}, {btn_pos.y()})")
        # print(f"btn_00 global position: ({btn_global.x()}, {btn_global.y()})")
        # print(f"btn_00 size: {self.btn_00.width()}x{self.btn_00.height()}")
        # print(f"=== Screen Change Complete ===\n")

    def showEvent(self, event):
        """Ensure screen change signal is connected when window is shown"""
        super().showEvent(event)
        window_handle = self.windowHandle()
        if window_handle:
            try:
                window_handle.screenChanged.disconnect(self._on_screen_changed)
            except:
                pass
            window_handle.screenChanged.connect(self._on_screen_changed)

    def pathcheck(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "DoNotDelete.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write('')
        dnd = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        dnd = dnd.rstrip('\n')
        dndl = dnd.split('\n')
        if dnd != '' and len(dndl) == 10:
            with open(BasePath + 'path_art.txt', 'w', encoding='utf-8') as f1:
                f1.write(dndl[0])
            with open(BasePath + 'path_aut.txt', 'w', encoding='utf-8') as f2:
                f2.write(dndl[1])
            with open(BasePath + 'path_ins.txt', 'w', encoding='utf-8') as f3:
                f3.write(dndl[2])
            with open(BasePath + 'path_pub.txt', 'w', encoding='utf-8') as f4:
                f4.write(dndl[3])
            with open(BasePath + 'path_pro.txt', 'w', encoding='utf-8') as f5:
                f5.write(dndl[4])
            with open(BasePath + 'path_con.txt', 'w', encoding='utf-8') as f6:
                f6.write(dndl[5])
            with open(BasePath + 'path_the.txt', 'w', encoding='utf-8') as f7:
                f7.write(dndl[6])
            with open(BasePath + 'path_met.txt', 'w', encoding='utf-8') as f8:
                f8.write(dndl[7])
            with open(BasePath + 'path_boo.txt', 'w', encoding='utf-8') as f9:
                f9.write(dndl[8])
            with open(BasePath + 'path_scr.txt', 'w', encoding='utf-8') as f10:
                f10.write(dndl[9])
        if dnd == '' or len(dndl) != 10:
            self.needpath()

    def movesysfile(self):
        path10 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path10 != '':
            tarname_cls = "elegantpaper.cls"
            fulldir_cls = os.path.join(path10, tarname_cls)
            contend_cls = codecs.open(BasePath + 'elegantpaper.cls', 'r', encoding='utf-8').read()
            with open(fulldir_cls, 'w', encoding='utf-8') as f8:
                f8.write(contend_cls)
            tarname_bib = 'reference.bib'
            fulldir_bib = os.path.join(path10, tarname_bib)
            with open(fulldir_bib, 'w', encoding='utf-8') as f8:
                f8.write('')
            tarname_not = "elegantnote.cls"
            fulldir_not = os.path.join(path10, tarname_not)
            contend_not = codecs.open(BasePath + 'elegantnote.cls', 'r', encoding='utf-8').read()
            with open(fulldir_not, 'w', encoding='utf-8') as f8:
                f8.write(contend_not)
            tarname_iee = "IEEEtran.cls"
            fulldir_iee = os.path.join(path10, tarname_iee)
            contend_iee = codecs.open(BasePath + 'IEEEtran.cls', 'r', encoding='utf-8').read()
            with open(fulldir_iee, 'w', encoding='utf-8') as f8:
                f8.write(contend_iee)
            tarname_jor1 = "journalCNdef.tex"
            fulldir_jor1 = os.path.join(path10, tarname_jor1)
            contend_jor1 = codecs.open(BasePath + 'journalCNdef.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor1, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor1)
            tarname_jor2 = "journalCNdef2.tex"
            fulldir_jor2 = os.path.join(path10, tarname_jor2)
            contend_jor2 = codecs.open(BasePath + 'journalCNdef2.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor2, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor2)
            tarname_jor3 = "journalCNpicins.sty"
            fulldir_jor3 = os.path.join(path10, tarname_jor3)
            contend_jor3 = codecs.open(BasePath + 'journalCNpicins.sty', 'r', encoding='utf-8').read()
            with open(fulldir_jor3, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor3)
            tarname_bea = "BeamerCN.sty"
            fulldir_bea = os.path.join(path10, tarname_bea)
            contend_bea = codecs.open(BasePath + 'BeamerCN.sty', 'r', encoding='utf-8').read()
            with open(fulldir_bea, 'w', encoding='utf-8') as f8:
                f8.write(contend_bea)

    def assigntoall(self):
        cmd = '''on run
        	tell application "System Events" to set activeApp to "Strawberry"
        	tell application "System Events" to tell UI element activeApp of list 1 of process "Dock"
        		perform action "AXShowMenu"
        		click menu item "Options" of menu 1
        		click menu item "All Desktops" of menu 1 of menu item "Options" of menu 1
        	end tell
        end run'''
        try:
            subprocess.call(['osascript', '-e', cmd])
        except Exception as e:
            pass

    def _register_ocr_button(self, button: QPushButton, default_text: str = 'OCR screenshot'):
        self.ocr_buttons.append(button)
        self._ocr_button_text[button] = default_text
        button.setText(default_text)

    def _set_ocr_buttons_state(self, enabled: bool, loading: bool = False):
        for btn in self.ocr_buttons:
            btn.setEnabled(enabled)
            if loading:
                btn.setText('Loading OCR model...')
            else:
                btn.setText(self._ocr_button_text.get(btn, btn.text()))

    def _ocr_language_list(self):
        code = load_ocr_language_code()
        parts = code.split('+')
        langs = []
        for p in parts:
            p = p.strip()
            if p:
                langs.append(p)
        # easyocr works best when English is included for mixed scripts
        if 'en' not in langs:
            langs.append('en')
        return list(dict.fromkeys(langs))

    def start_ocr_capture(self, fallback_widget=None):
        target = self._ocr_last_editor if isinstance(self._ocr_last_editor, (QPlainTextEdit, QTextEdit, QLineEdit)) and self._ocr_last_editor.isVisible() else fallback_widget
        self._ocr_target_widget = target
        if self.ocr_reader is None:
            if self.ocr_reader_loading:
                QMessageBox.information(self, "OCR", "OCR model is still downloading. Please wait...")
            else:
                self._load_ocr_reader()
            return
        self._start_ocr_selection()

    def _load_ocr_reader(self, show_message: bool = True):
        self.ocr_reader_loading = True
        self._set_ocr_buttons_state(False, loading=True)
        if show_message:
            QMessageBox.information(self, "OCR", "First use: downloading the OCR model in the background. Please wait...")
        self.ocr_reader_thread = QThread()
        self.ocr_reader_worker = ReaderLoader(self._ocr_language_list(), model_dir=os.path.join(BasePath, "model"))
        self.ocr_reader_worker.moveToThread(self.ocr_reader_thread)
        self.ocr_reader_thread.started.connect(self.ocr_reader_worker.run)
        self.ocr_reader_worker.finished.connect(self._on_reader_loaded)
        self.ocr_reader_worker.finished.connect(self.ocr_reader_thread.quit)
        self.ocr_reader_worker.finished.connect(self.ocr_reader_worker.deleteLater)
        self.ocr_reader_thread.finished.connect(self.ocr_reader_thread.deleteLater)
        self.ocr_reader_thread.start()

    def _on_reader_loaded(self, reader, error_message: str):
        self.ocr_reader_loading = False
        self._set_ocr_buttons_state(True, loading=False)
        if reader is None:
            QMessageBox.warning(self, "OCR", f"Failed to load OCR model: {error_message}")
            return
        self.ocr_reader = reader
        QMessageBox.information(self, "OCR", "OCR model is ready. Click OCR again to select a region.")

    def _start_ocr_selection(self):
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos)
        if screen is None:
            screen = QGuiApplication.primaryScreen()
            if screen is None:
                QMessageBox.warning(self, "OCR", "No available screen found for capturing.")
                return
        geometry = screen.geometry()
        self._ocr_current_screen = screen
        self.ocr_overlay = SelectionOverlay(geometry)
        self.ocr_overlay.regionSelected.connect(self._on_region_selected)
        self.ocr_overlay.show()

    def _on_region_selected(self, global_rect: QRect):
        self.ocr_overlay = None
        self._capture_and_ocr(global_rect)

    def _capture_and_ocr(self, rect: QRect | None = None):
        if self.ocr_reader is None:
            QMessageBox.information(self, "OCR", "OCR model is not ready yet. Please click OCR again after the model is loaded.")
            return

        screen = self._ocr_current_screen
        if screen is None:
            screen = QGuiApplication.screenAt(rect.center()) if rect is not None else QGuiApplication.screenAt(QCursor.pos())
        if screen is None:
            screen = QGuiApplication.primaryScreen()
        if screen is None:
            QMessageBox.warning(self, "OCR", "No available screen found for capturing.")
            return

        if rect is not None:
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        else:
            geometry = screen.geometry()
            x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        pixmap = screen.grabWindow(0, x, y, w, h)
        if pixmap.isNull():
            QMessageBox.warning(self, "OCR", "Screenshot failed. Please try again.")
            return

        image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.bytesPerLine() * height)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, image.bytesPerLine() // 4, 4))
        img_rgb = arr[:, :, :3]

        try:
            texts = self.ocr_reader.readtext(img_rgb, detail=0)
            result = "\n".join(texts) if texts else "[No text recognized in the selected area]"
        except Exception as e:
            result = f"OCR Error: {e}"

        self._deliver_ocr_result(result)

    def _deliver_ocr_result(self, result: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(result)
        widget = self._ocr_target_widget
        if isinstance(widget, QPlainTextEdit):
            cursor = widget.textCursor()
            cursor.insertText(result)
            widget.setTextCursor(cursor)
            QMessageBox.information(self, "OCR", "OCR result inserted into the editor and copied to clipboard.")
            return
        if isinstance(widget, QTextEdit):
            cursor = widget.textCursor()
            cursor.insertText(result)
            widget.setTextCursor(cursor)
            QMessageBox.information(self, "OCR", "OCR result inserted into the editor and copied to clipboard.")
            return
        if isinstance(widget, QLineEdit):
            widget.insert(result)
            QMessageBox.information(self, "OCR", "OCR result inserted into the field and copied to clipboard.")
            return
        QMessageBox.information(self, "OCR", result + "\n\n(The result has been copied to the clipboard.)")

    def cleanup_ocr(self):
        """Gracefully stop OCR background work before quit."""
        try:
            if self.ocr_overlay is not None:
                self.ocr_overlay.close()
                self.ocr_overlay = None
            if self.ocr_reader_thread is not None and self.ocr_reader_thread.isRunning():
                self.ocr_reader_thread.requestInterruption()
                self.ocr_reader_thread.quit()
                self.ocr_reader_thread.wait(5000)
            self.ocr_reader_thread = None
            self.ocr_reader = None
            if self.insp_backup_timer is not None:
                self.insp_backup_timer.stop()
                self.insp_backup_timer.deleteLater()
                self.insp_backup_timer = None
            try:
                app.removeEventFilter(self)
            except Exception:
                pass
        except Exception:
            pass

    def reset_ocr_state(self):
        """Force OCR to reload next time (used when language changes)."""
        try:
            if self.ocr_reader_thread is not None and self.ocr_reader_thread.isRunning():
                self.ocr_reader_thread.requestInterruption()
                self.ocr_reader_thread.quit()
                self.ocr_reader_thread.wait(2000)
            self.ocr_reader_thread = None
            self.ocr_reader = None
            self.ocr_reader_loading = False
            self._set_ocr_buttons_state(True, loading=False)
        except Exception:
            pass

    def reload_ocr_for_language_change(self):
        """Immediately drop current OCR model and reload with new language."""
        self.reset_ocr_state()
        # 直接后台重载新语言模型，避免下次点击仍用旧模型
        self._load_ocr_reader(show_message=False)

    def needpath(self):
        warn = CustomDialog_warn()
        warn.exec()

    def wordTab(self):
        self.bigwi1 = QWidget()

        t1 = QWidget()
        fontw = PyQt6.QtGui.QFont()
        fontw.setBold(True)
        lbl1 = QLabel('Just collect!', self)
        lbl1.setFont(fontw)
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addStretch()
        b1.addWidget(lbl1)
        b1.addStretch()
        t1.setLayout(b1)

        t2 = QWidget()
        self.lew1 = QLineEdit(self)
        self.lew1.setPlaceholderText('Enter your word!')
        self.lew1.setFixedHeight(60)
        self.lew1.setStyleSheet(
            '''font: 30pt;'''
        )
        btn_wa = QPushButton('Add to waiting list!', self)
        btn_wa.setShortcut('Ctrl+Return')
        btn_wa.clicked.connect(self.add_to_wait)
        btn_wa.setMaximumHeight(20)
        btn_wa.setMinimumWidth(150)
        btn_wb = QPushButton('Import from a word list (one word in one line)', self)
        btn_wb.clicked.connect(self.importlist)
        btn_wb.setMaximumHeight(20)
        btn_wb.setMinimumWidth(150)
        b2 = QVBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addWidget(self.lew1)
        b2.addWidget(btn_wa)
        b2.addWidget(btn_wb)
        t2.setLayout(b2)

        t2_5 = QWidget()
        self.lblexp_2 = QLabel('', self)
        b2_5 = QHBoxLayout()
        b2_5.setContentsMargins(0, 0, 0, 0)
        b2_5.addStretch()
        b2_5.addWidget(self.lblexp_2)
        b2_5.addStretch()
        t2_5.setLayout(b2_5)

        t3 = QWidget()
        fontw = PyQt6.QtGui.QFont()
        fontw.setBold(True)
        lbl3 = QLabel('Make cards!', self)
        lbl3.setFont(fontw)
        b3 = QHBoxLayout()
        b3.setContentsMargins(0, 0, 0, 0)
        b3.addStretch()
        b3.addWidget(lbl3)
        b3.addStretch()
        t3.setLayout(b3)

        t4 = QWidget()
        self.lew2 = QLineEdit(self)
        self.lew2.setPlaceholderText('Deck name')
        btn_wc = QPushButton('Create', self)
        btn_wc.clicked.connect(self.createdeck)
        btn_wc.setMaximumHeight(20)
        btn_wc.setMinimumWidth(100)
        b4 = QHBoxLayout()
        b4.setContentsMargins(0, 0, 0, 0)
        b4.addWidget(self.lew2)
        b4.addWidget(btn_wc)
        t4.setLayout(b4)

        t5 = QWidget()
        btn_wd = QPushButton('Open a .txt deck', self)
        btn_wd.clicked.connect(self.opendeck)
        btn_wd.setMaximumHeight(20)
        btn_we = QPushButton('Close the deck', self)
        btn_we.clicked.connect(self.closedeck)
        btn_we.setMaximumHeight(20)
        b5 = QHBoxLayout()
        b5.setContentsMargins(0, 0, 0, 0)
        b5.addWidget(btn_wd)
        b5.addWidget(btn_we)
        t5.setLayout(b5)

        t6 = QWidget()
        lbl4 = QLabel('Focusing on:', self)
        #lbl4.setMaximumWidth(80)
        self.wid_word = QComboBox(self)
        self.wid_word.setCurrentIndex(0)
        #self.wid_word.setMaximumWidth(275)
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "wordwaitinglist.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        with open(fulldir2, 'a', encoding='utf-8') as f0:
            f0.write('')
        contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        alllist = contend.split('\n')
        alllist.sort()
        while '' in alllist:
            alllist.remove('')
        if alllist == ['']:
            self.wid_word.addItems(['No expression on list'])
        if alllist != []:
            self.wid_word.addItems(alllist)
        num = len(alllist)
        wri = 'There are ' + str(num) + ' expressions on your list now!'
        self.lblexp_2.setText(wri)
        b6 = QHBoxLayout()
        b6.setContentsMargins(0, 0, 0, 0)
        b6.addWidget(lbl4)
        b6.addWidget(self.wid_word)
        t6.setLayout(b6)

        btn_sow = QPushButton('Search on Web!', self)
        btn_sow.clicked.connect(self.search_on_web)
        btn_sow.setFixedHeight(20)

        self.btn_ocr_word = QPushButton('OCR screenshot', self)
        self.btn_ocr_word.clicked.connect(lambda: self.start_ocr_capture(self.textw1))
        self.btn_ocr_word.setFixedHeight(20)
        self._register_ocr_button(self.btn_ocr_word, 'OCR screenshot')

        # self.btn_aiow = QPushButton('Search with AI!', self)
        # self.btn_aiow.clicked.connect(self.search_with_ai)
        # self.btn_aiow.setFixedHeight(20)

        self.textw1 = QPlainTextEdit(self)
        self.textw1.setReadOnly(False)
        self.textw1.setObjectName("edit")
        self.textw1.setPlaceholderText('Explanations')

        self.lew3 = QLineEdit(self)
        self.lew3.setPlaceholderText('Tags (Use 、or + if there are many)')

        t6_5 = QWidget()
        btn_makecard = QPushButton('Make a basic card!', self)
        btn_makecard.clicked.connect(self.makecard)
        btn_makecard.setMaximumHeight(20)
        btn_clearall = QPushButton('Next card!', self)
        btn_clearall.clicked.connect(self.next_card)
        btn_clearall.setMaximumHeight(20)
        b6_5 = QHBoxLayout()
        b6_5.setContentsMargins(0, 0, 0, 0)
        b6_5.addWidget(btn_makecard)
        b6_5.addWidget(btn_clearall)
        t6_5.setLayout(b6_5)

        t7 = QWidget()
        fontw = PyQt6.QtGui.QFont()
        fontw.setBold(True)
        lbl7 = QLabel('Search in deck!', self)
        lbl7.setFont(fontw)
        b7 = QHBoxLayout()
        b7.setContentsMargins(0, 0, 0, 0)
        b7.addStretch()
        b7.addWidget(lbl7)
        b7.addStretch()
        t7.setLayout(b7)

        t8 = QWidget()
        self.lew4 = QLineEdit(self)
        self.lew4.setPlaceholderText('What tag are you looking for?')
        btn_wsearch = QPushButton('Search', self)
        btn_wsearch.clicked.connect(self.searchmeaning)
        btn_wsearch.setMaximumHeight(20)
        btn_wsearch.setMinimumWidth(100)
        b8 = QHBoxLayout()
        b8.setContentsMargins(0, 0, 0, 0)
        b8.addWidget(self.lew4)
        b8.addWidget(btn_wsearch)
        t8.setLayout(b8)

        t9 = QWidget()
        vboxa = QHBoxLayout()
        vboxa.setContentsMargins(0, 0, 0, 0)
        vboxa.addWidget(btn_sow)
        # vboxa.addWidget(self.btn_ocr_word)
        # vboxa.addWidget(self.btn_aiow)
        t9.setLayout(vboxa)

        self.text_res = QPlainTextEdit(self)
        self.text_res.setReadOnly(True)
        self.text_res.setObjectName("edit")
        self.text_res.setPlaceholderText('Results will appear here.')

        btn_clearab = QPushButton('Start a new search!', self)
        btn_clearab.clicked.connect(self.newsearch)
        btn_clearab.setMaximumHeight(20)

        lay1 = QVBoxLayout()
        lay1.setContentsMargins(0, 0, 0, 0)
        lay1.addWidget(t1)
        lay1.addWidget(t2)
        lay1.addWidget(t2_5)
        lay1.addWidget(t3)
        lay1.addWidget(t4)
        lay1.addWidget(t5)
        lay1.addWidget(t6)
        lay1.addWidget(t9)
        lay1.addWidget(self.btn_ocr_word)
        lay1.addWidget(self.textw1)
        lay1.addWidget(self.lew3)
        lay1.addWidget(t6_5)
        lay1.addWidget(t7)
        lay1.addWidget(t8)
        lay1.addWidget(self.text_res)
        lay1.addWidget(btn_clearab)
        self.bigwi1.setLayout(lay1)

        self.bigwi2 = QTabWidget()
        self.word_sub = QWidget()
        self.bigwi2.addTab(self.word_sub, 'Card')

        self.word_card()

        self.bigwi3 = QTabWidget()
        self.rtm_word = QWidget()
        self.bigwi3.addTab(self.rtm_word, 'Realtime')
        self.realword()
        self.bigwi3.setVisible(False)

        self.page1_v_box = QHBoxLayout()
        self.page1_v_box.addWidget(self.bigwi1, 1)
        self.page1_v_box.addWidget(self.bigwi2, 1)
        self.page1_v_box.addWidget(self.bigwi3, 1)
        self.word_tab.setLayout(self.page1_v_box)

    def word_card(self):
        self.carda = QPlainTextEdit(self)
        self.carda.setMinimumHeight(40)
        self.carda.setStyleSheet(
            '''font: 30pt;'''
        )
        self.carda.setReadOnly(False)
        self.carda.textChanged.connect(self.card1changed)
        self.scrollbar3 = self.carda.verticalScrollBar()
        self.scrollbar3.valueChanged.connect(self.card1scroll)
        self.cardb = QPlainTextEdit(self)
        self.cardb.setMinimumHeight(40)
        self.cardb.setStyleSheet(
            '''font: 20pt;'''
        )
        self.cardb.setReadOnly(False)
        self.cardb.textChanged.connect(self.card2changed)
        self.scrollbar4 = self.cardb.verticalScrollBar()
        self.scrollbar4.valueChanged.connect(self.card2scroll)

        # self.btnbot_word = QPushButton('', self)
        # # self.btnbot_word.clicked.connect(self.showlist)
        # self.btnbot_word.setFixedSize(20, 20)
        # self.btnbot_word.setStyleSheet('''
        #     QPushButton{
        #     border: transparent;
        #     background-color: transparent;
        #     border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
        #     }
        #     QPushButton:pressed{
        #     border: 1px outset grey;
        #     background-color: #0085FF;
        #     border-radius: 4px;
        #     padding: 1px;
        #     color: #FFFFFF
        #     }
        #     ''')

        btn_exp1 = QPushButton('Hard save', self)
        btn_exp1.clicked.connect(self.editcardsave)
        btn_exp1.setMaximumHeight(20)
        btn_exp1.setShortcut('Ctrl+Shift+Return')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        # btnbox.addWidget(self.btnbot_word)
        btnbox.addWidget(btn_exp1)
        btnwid.setLayout(btnbox)

        r1 = QVBoxLayout()
        r1.addWidget(self.carda)
        r1.addWidget(self.cardb)
        r1.addWidget(btnwid)
        self.word_sub.setLayout(r1)

    def realword(self):
        self.card_rt = QTextEdit(self)
        self.card_rt.setReadOnly(True)
        self.card_rt.setStyleSheet(
            '''font: 30pt;'''
        )
        self.card_rt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_rt2 = QTextEdit(self)
        self.card_rt2.setReadOnly(True)
        self.card_rt2.setStyleSheet(
            '''font: 20pt;'''
        )
        self.card_rt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_cls = QPushButton('Close realtime window', self)
        btn_cls.clicked.connect(self.close_re)
        btn_cls.setMaximumHeight(20)
        r2 = QVBoxLayout()
        r2.addWidget(self.card_rt)
        r2.addWidget(self.card_rt2)
        r2.addWidget(btn_cls)
        self.rtm_word.setLayout(r2)

    def artTab(self):
        self.description_box = QWidget()

        self.upper1 = QWidget()

        self.read_t1 = QWidget()
        lbl1 = QLabel('Title:', self)
        self.le1 = QLineEdit(self)
        self.le1.setPlaceholderText('Enter your text')
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(lbl1)
        b1.addWidget(self.le1)
        self.read_t1.setLayout(b1)

        self.read_t2 = QWidget()
        self.lblread_2 = QLabel('Authors:', self)
        self.le2 = QLineEdit(self)
        self.le2.setPlaceholderText('Use 、or + if there are many and % after translators')
        b2 = QHBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addWidget(self.lblread_2)
        b2.addWidget(self.le2)
        self.read_t2.setLayout(b2)

        self.read_t7 = QWidget()
        lbl7 = QLabel('Institutes:', self)
        self.le7 = QLineEdit(self)
        self.le7.setPlaceholderText('Use 、or + if there are many')
        b7 = QHBoxLayout()
        b7.setContentsMargins(0, 0, 0, 0)
        b7.addWidget(lbl7)
        b7.addWidget(self.le7)
        self.read_t7.setLayout(b7)

        self.read_t3 = QWidget()
        lbl3 = QLabel('Publication:', self)
        self.le3 = QLineEdit(self)
        self.le3.setPlaceholderText('Enter your text')
        lbl3_1 = QLabel('Press:', self)
        self.le3_1 = QLineEdit(self)
        self.le3_1.setPlaceholderText('Enter your text')
        b3 = QHBoxLayout()
        b3.setContentsMargins(0, 0, 0, 0)
        b3.addWidget(lbl3)
        b3.addWidget(self.le3)
        b3.addWidget(lbl3_1)
        b3.addWidget(self.le3_1)
        self.read_t3.setLayout(b3)

        self.web_t3 = QWidget()
        lblweb3 = QLabel('URL:', self)
        self.leweb3 = QLineEdit(self)
        self.leweb3.setPlaceholderText('Enter your text')
        ba3 = QHBoxLayout()
        ba3.setContentsMargins(0, 0, 0, 0)
        ba3.addWidget(lblweb3)
        ba3.addWidget(self.leweb3)
        self.web_t3.setLayout(ba3)
        self.web_t3.setVisible(False)

        self.read_t4 = QWidget()
        lbl4 = QLabel('Year:', self)
        self.le4 = QLineEdit(self)
        self.le4.setPlaceholderText('Enter your text')
        lbl4_1 = QLabel('Vol / Mon:', self)
        self.le4_1 = QLineEdit(self)
        self.le4_1.setPlaceholderText('Enter your text')
        b4 = QHBoxLayout()
        b4.setContentsMargins(0, 0, 0, 0)
        b4.addWidget(lbl4)
        b4.addWidget(self.le4)
        b4.addWidget(lbl4_1)
        b4.addWidget(self.le4_1)
        self.read_t4.setLayout(b4)

        self.read_t4_doi = QWidget()
        lbldoi = QLabel('DOI:', self)
        self.le_doi = QLineEdit(self)
        self.le_doi.setPlaceholderText('10.xxxx/xxxxxx')
        b4_doi = QHBoxLayout()
        b4_doi.setContentsMargins(0, 0, 0, 0)
        b4_doi.addWidget(lbldoi)
        b4_doi.addWidget(self.le_doi)
        self.read_t4_doi.setLayout(b4_doi)

        self.read_t4_isbn = QWidget()
        lblisbn = QLabel('ISBN:', self)
        self.le_isbn = QLineEdit(self)
        self.le_isbn.setPlaceholderText('978-xxxxxx')
        b4_isbn = QHBoxLayout()
        b4_isbn.setContentsMargins(0, 0, 0, 0)
        b4_isbn.addWidget(lblisbn)
        b4_isbn.addWidget(self.le_isbn)
        self.read_t4_isbn.setLayout(b4_isbn)

        self.read_t5 = QWidget()
        lbl5 = QLabel('Tags:', self)
        self.le5 = QLineEdit(self)
        self.le5.setPlaceholderText('Use 、or + if there are many')
        b5 = QHBoxLayout()
        b5.setContentsMargins(0, 0, 0, 0)
        b5.addWidget(lbl5)
        b5.addWidget(self.le5)
        self.read_t5.setLayout(b5)

        self.read_t6 = QWidget()
        self.btnarc = QPushButton('', self)
        self.btnarc.clicked.connect(self.show_list_arc)
        self.btnarc.setFixedSize(20, 20)
        self.btnarc.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/input.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        btn1 = QPushButton('Open', self)
        btn1.clicked.connect(self.openextis)
        btn1.setMaximumHeight(20)
        self.btnmain2 = QPushButton('Add', self)
        self.btnmain2.clicked.connect(self.addmain)
        self.btnmain2.setMaximumHeight(20)
        btn3 = QPushButton('Clear', self)
        btn3.clicked.connect(self.clearabv)
        btn3.setMaximumHeight(20)
        self.btnx4 = QPushButton('', self)
        self.btnx4.clicked.connect(self.showlist)
        self.btnx4.setFixedSize(20, 20)
        self.btnx4.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/up.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        b6 = QHBoxLayout()
        b6.setContentsMargins(0, 0, 0, 0)
        b6.addWidget(self.btnarc)
        b6.addWidget(btn1)
        b6.addWidget(self.btnmain2)
        b6.addWidget(btn3)
        b6.addWidget(self.btnx4)
        self.read_t6.setLayout(b6)

        self.read_t8 = QWidget()
        self.le8 = QLineEdit(self)
        self.le8.setPlaceholderText('Of a book?')
        self.le9 = QLineEdit(self)
        self.le9.setPlaceholderText('Of a chapter?')
        self.le10 = QLineEdit(self)
        self.le10.setPlaceholderText('Page range')
        b8 = QHBoxLayout()
        b8.setContentsMargins(0, 0, 0, 0)
        b8.addWidget(self.le8)
        b8.addWidget(self.le9)
        b8.addWidget(self.le10)
        self.read_t8.setLayout(b8)

        self.web_t8 = QWidget()
        self.leweb8 = QLineEdit(self)
        self.leweb8.setPlaceholderText('Conference?')
        self.leweb9 = QLineEdit(self)
        self.leweb9.setPlaceholderText('Host Institution?')
        self.leweb10 = QLineEdit(self)
        self.leweb10.setPlaceholderText('Place?')
        ba8 = QHBoxLayout()
        ba8.setContentsMargins(0, 0, 0, 0)
        ba8.addWidget(self.leweb8)
        ba8.addWidget(self.leweb9)
        ba8.addWidget(self.leweb10)
        self.web_t8.setLayout(ba8)
        self.web_t8.setVisible(False)

        supper1 = QVBoxLayout()
        supper1.setContentsMargins(0, 10, 0, 0)
        supper1.addWidget(self.read_t1)
        supper1.addWidget(self.read_t2)
        supper1.addWidget(self.read_t7)
        supper1.addWidget(self.read_t3)
        supper1.addWidget(self.web_t3)
        supper1.addWidget(self.read_t8)
        supper1.addWidget(self.web_t8)
        supper1.addWidget(self.read_t4)
        supper1.addWidget(self.read_t4_doi)
        supper1.addWidget(self.read_t4_isbn)
        supper1.addWidget(self.read_t5)
        supper1.addWidget(self.read_t6)
        self.upper1.setLayout(supper1)

        self.widget0 = QComboBox(self)
        self.widget0.setCurrentIndex(0)
        self.widget0.currentIndexChanged.connect(self.index_changed)
        defalist = ['Append at the end (default)', 'Append at the current cursor']
        if self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
            if result != []:
                result = '☆'.join(result)
                result = result.replace('#', '')
                result = result.replace('# ', '')
                result = result.replace('Q/P: ', '')
                result = result.split('☆')
                for i in range(len(result)):
                    result[i] = 'After ' + result[i]
                    result[i] = ''.join(result[i])
                defalist = defalist + result
        self.widget0.addItems(defalist)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.one_tab = QWidget()
        self.two_tab = QWidget()
        self.three_tab = QWidget()
        self.four_tab = QWidget()
        self.five_tab = QWidget()
        self.six_tab = QWidget()
        self.tabs.addTab(self.one_tab, 'Extensive')
        self.tabs.addTab(self.two_tab, 'Intensive')
        self.tabs.addTab(self.three_tab, 'Concepts')
        self.tabs.addTab(self.four_tab, 'Theories')
        self.tabs.addTab(self.five_tab, 'Methods')
        self.tabs.addTab(self.six_tab, 'Tools')

        self.ext_r()
        self.int_r()
        self.concep()
        self.theors()
        self.meths()
        self.toolkit()

        self.btn_ocr_art = QPushButton('OCR screenshot', self)
        self.btn_ocr_art.clicked.connect(lambda: self.start_ocr_capture(self.text11))
        self.btn_ocr_art.setMaximumHeight(20)
        self._register_ocr_button(self.btn_ocr_art, 'OCR screenshot')
        self.art_ocr_row = QWidget()
        art_ocr_layout = QHBoxLayout()
        art_ocr_layout.setContentsMargins(0, 0, 0, 0)
        #art_ocr_layout.addStretch()
        art_ocr_layout.addWidget(self.btn_ocr_art)
        #art_ocr_layout.addStretch()
        self.art_ocr_row.setLayout(art_ocr_layout)

        self.wings_h_box = QVBoxLayout()
        self.wings_h_box.setContentsMargins(0, 0, 0, 0)
        self.wings_h_box.addWidget(self.upper1)
        self.wings_h_box.addWidget(self.widget0)
        self.wings_h_box.addWidget(self.art_ocr_row)
        self.wings_h_box.addWidget(self.tabs)
        self.description_box.setLayout(self.wings_h_box)

        self.main2 = QTabWidget()
        self.sub1_tab = QWidget()
        self.sub2_tab = QWidget()
        self.sub3_tab = QWidget()
        self.sub4_tab = QWidget()
        self.main2.addTab(self.sub1_tab, 'Articles')
        self.main2.addTab(self.sub2_tab, 'Concepts')
        self.main2.addTab(self.sub3_tab, 'Theories')
        self.main2.addTab(self.sub4_tab, 'Methods')
        self.main2.currentChanged.connect(self.on_realclick)

        self.sub1()
        self.sub2()
        self.sub3()
        self.sub4()

        # home_dir = str(Path.home())
        # tarname1 = "BroccoliAppPath"
        # self.fulldir1 = os.path.join(home_dir, tarname1)
        # if not os.path.exists(self.fulldir1):
        #     os.mkdir(self.fulldir1)
        # tarname3 = "lang.txt"
        # fulldir3 = os.path.join(self.fulldir1, tarname3)
        # if not os.path.exists(fulldir3):
        #     with open(fulldir3, 'a', encoding='utf-8') as f0:
        #         f0.write('')
        # tarname4 = "model.txt"
        # fulldir4 = os.path.join(self.fulldir1, tarname4)
        # if not os.path.exists(fulldir4):
        #     with open(fulldir4, 'a', encoding='utf-8') as f0:
        #         f0.write('')

        # self.sub_real1 = QTextEdit(self)
        # self.sub_real1.setReadOnly(True)

        # self.sub_text1 = QPlainTextEdit(self)
        # self.sub_text1.setReadOnly(False)
        # self.sub_text1.setObjectName('edit')
        # self.sub_text1.setMaximumHeight(100)
        # self.sub_text1.setPlaceholderText('Your prompts here...')

        # self.sub_btn_sub1 = QPushButton('🔺 Send', self)
        # self.sub_btn_sub1.clicked.connect(self.bot1send)
        # self.sub_btn_sub1.setFixedSize(80, 20)

        # self.sub_btn_sub2 = QPushButton('🔸 Clear', self)
        # self.sub_btn_sub2.clicked.connect(self.bot1clear)
        # self.sub_btn_sub2.setFixedSize(80, 20)

        # self.sub_btn_sub3 = QPushButton('🔻 Close', self)
        # self.sub_btn_sub3.clicked.connect(self.bot1close)
        # self.sub_btn_sub3.setFixedSize(80, 20)

        # self.sub_widget0 = QComboBox(self)
        # self.sub_widget0.setCurrentIndex(0)
        # self.sub_widget0.addItems(
        #     ['Chat and ask', 'Translate', 'Polish', 'Summarize', 'Grammatically analyze',
        #      'Explain code', 'Customize'])
        # self.sub_widget0.currentIndexChanged.connect(self.bot1mode)
        # self.sub_widget0.setMaximumWidth(370)

        # self.sub_widget1 = QComboBox(self)
        # self.sub_widget1.setCurrentIndex(0)
        # langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
        # fulllanglist = []
        # langs_list = ['English', '中文', '日本語']
        # if langs != '':
        #     langs_list = langs.split('\n')
        #     while '' in langs_list:
        #         langs_list.remove('')
        #     for i in range(len(langs_list)):
        #         fulllanglist.append(langs_list[i])
        # if langs == '':
        #     for i in range(len(langs_list)):
        #         fulllanglist.append(langs_list[i])
        # self.sub_widget1.addItems(langs_list)
        # self.sub_widget1.setVisible(False)
        # self.sub_widget1.currentIndexChanged.connect(self.bot1trans)

        # self.sub_lbl1 = QLabel('▶', self)
        # self.sub_lbl1.setVisible(False)

        # self.sub_widget2 = QComboBox(self)
        # self.sub_widget2.setCurrentIndex(0)
        # currentlang = self.sub_widget1.currentText()
        # while currentlang in langs_list:
        #     langs_list.remove(currentlang)
        # self.sub_widget2.addItems(langs_list)
        # self.sub_widget2.setVisible(False)

        # self.sub_widget4 = QComboBox(self)
        # self.sub_widget4.setCurrentIndex(0)
        # self.sub_widget4.addItems(fulllanglist)
        # self.sub_widget4.setVisible(False)
        # self.sub_widget4.setFixedWidth(170)

        # self.sub_widget5 = QComboBox(self)
        # self.sub_widget5.setCurrentIndex(0)
        # home_dir = str(Path.home())
        # tarname1 = "BroccoliAppPath"
        # fulldir1 = os.path.join(home_dir, tarname1)
        # if not os.path.exists(fulldir1):
        #     os.mkdir(fulldir1)
        # tarname2 = "CustomPrompt.txt"
        # fulldir2 = os.path.join(fulldir1, tarname2)
        # if not os.path.exists(fulldir2):
        #     with open(fulldir2, 'a', encoding='utf-8') as f0:
        #         f0.write('')
        # customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        # promptlist = customprompt.split('---')
        # while '' in promptlist:
        #     promptlist.remove('')
        # itemlist = []
        # for i in range(len(promptlist)):
        #     itemlist.append(promptlist[i].split('|><|')[0].replace('<|', '').replace('\n', ''))
        # if itemlist != []:
        #     self.sub_widget5.addItems(itemlist)
        # if itemlist == []:
        #     self.sub_widget5.addItems(['No customized prompts, please add one in Settings'])
        # self.sub_widget5.setVisible(False)
        # self.sub_widget5.setFixedWidth(170)
        # self.sub_widget5.currentIndexChanged.connect(self.bot1custom)

        # qw1 = QWidget()
        # vbox1 = QVBoxLayout()
        # vbox1.setContentsMargins(0, 0, 0, 0)
        # vbox1.addWidget(self.sub_btn_sub1)
        # vbox1.addWidget(self.sub_btn_sub2)
        # vbox1.addWidget(self.sub_btn_sub3)
        # qw1.setLayout(vbox1)

        # qw1_3 = QWidget()
        # vbox1_3 = QHBoxLayout()
        # vbox1_3.setContentsMargins(0, 0, 0, 0)
        # vbox1_3.addWidget(self.sub_widget0)
        # vbox1_3.addWidget(self.sub_widget1)
        # vbox1_3.addWidget(self.sub_lbl1)
        # vbox1_3.addWidget(self.sub_widget2)
        # vbox1_3.addWidget(self.sub_widget4)
        # vbox1_3.addWidget(self.sub_widget5)
        # qw1_3.setLayout(vbox1_3)

        # qw2 = QWidget()
        # vbox2 = QHBoxLayout()
        # vbox2.setContentsMargins(0, 0, 0, 0)
        # vbox2.addWidget(self.sub_text1)
        # vbox2.addWidget(qw1)
        # qw2.setLayout(vbox2)

        # self.bot1 = QWidget()
        # vbox2_1 = QVBoxLayout()
        # vbox2_1.setContentsMargins(20, 0, 20, 0)
        # vbox2_1.addWidget(self.sub_real1)
        # vbox2_1.addWidget(qw1_3)
        # vbox2_1.addWidget(qw2)
        # self.bot1.setLayout(vbox2_1)
        # self.bot1.setFixedHeight(300)
        # self.bot1.setVisible(False)

        # self.qwbotbox = QWidget()
        # botbox = QVBoxLayout()
        # botbox.setContentsMargins(3, 0, 0, 0)
        # botbox.addWidget(self.main2)
        # # botbox.addWidget(self.bot1)
        # self.qwbotbox.setLayout(botbox)

        self.main3 = QTabWidget()
        self.real_tab1 = QWidget()
        self.main3.addTab(self.real_tab1, 'Realtime Markdown')
        self.ret1()
        self.main3.setVisible(False)

        self.page2_box_h = QHBoxLayout()
        self.page2_box_h.addWidget(self.description_box, 1)
        self.page2_box_h.addWidget(self.main2, 1)
        self.page2_box_h.addWidget(self.main3, 1)
        self.art_tab.setLayout(self.page2_box_h)

    def show_list_arc(self):
        warn = CustomDialog_list_archive()
        warn.exec()

    def ret1(self):
        self.real1 = QTextEdit(self)
        self.real1.setReadOnly(True)
        btn_sub1 = QPushButton('Close realtime window', self)
        btn_sub1.clicked.connect(self.close_re)
        btn_sub1.setMaximumHeight(20)
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.real1)
        page3_box_h.addWidget(btn_sub1)
        self.real_tab1.setLayout(page3_box_h)

    def ret2(self):
        self.real2 = QTextEdit(self)
        self.real2.setReadOnly(True)
        btn_sub1 = QPushButton('Close realtime window', self)
        btn_sub1.clicked.connect(self.close_re)
        btn_sub1.setMaximumHeight(20)
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.real2)
        page3_box_h.addWidget(btn_sub1)
        self.real_tab2.setLayout(page3_box_h)

    def index_changed(self, i):
        if i == 0 and self.le1.text() != '':
            with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                f0.write('')
        if i != 0 and i != 1 and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            if i < self.widget0.count() - 1:
                tarnum = int(self.widget0.currentIndex() + 1)
                searcde = str(self.widget0.itemText(tarnum))
                searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]').replace('.', '\.').replace('*', '\*').replace('+', '\+').replace('?', '\?').replace('|', '\|').replace('(', '\(').replace(')', '\)').replace('{', '\{').replace('}', '\}').replace('^', '\^').replace('$', '\$')
                sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                if sst != None:
                    with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                        f0.write(sst.group())
            if i == self.widget0.count() - 1:
                with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')

    def cursorchanged(self):
        if self.text.toPlainText() != '' and self.le1.text() != '':
            if self.widget0.currentIndex() == 0:
                with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')
            if self.widget0.currentIndex() == 1:
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                position = cursor.position()
                path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                fullcontent = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                list_fullcontent = list(fullcontent)
                remove_list = list_fullcontent[position:]
                remove_str = ''.join(remove_list)
                with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                    f0.write(remove_str)
            if self.widget0.currentIndex() != 0 and self.widget0.currentIndex() != 1:
                path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                if self.widget0.currentIndex() < self.widget0.count() - 1:
                    tarnum = int(self.widget0.currentIndex() + 1)
                    searcde = str(self.widget0.itemText(tarnum))
                    searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]').replace('.',
                                                                                                          '\.').replace(
                        '*', '\*').replace('+', '\+').replace('?', '\?').replace('|', '\|').replace('(', '\(').replace(
                        ')', '\)').replace('{', '\{').replace('}', '\}').replace('^', '\^').replace('$', '\$')
                    sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                    if sst != None:
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(sst.group())
                if self.widget0.currentIndex() == self.widget0.count() - 1:
                    with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                        f0.write('')

    def inspiTab(self):
        t1 = QWidget()
        lbl1 = QLabel('Title:', self)
        self.leii1 = QLineEdit(self)
        self.leii1.setPlaceholderText('Enter your text')
        self.btn_a = QPushButton('Create', self)
        self.btn_a.clicked.connect(self.createscr)
        self.btn_a.setMaximumHeight(20)
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(lbl1)
        b1.addWidget(self.leii1, 2)
        b1.addWidget(self.btn_a, 1)
        t1.setLayout(b1)

        self.choosepart = QComboBox(self)
        self.choosepart.setCurrentIndex(0)
        self.choosepart.currentIndexChanged.connect(self.chooseind)
        defalist = ['Append at the end (default)', 'Append at the current cursor']
        if self.leii1.text() != '':
            pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".md"
            fulldir1 = os.path.join(pathscr, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
            result2 = '☆'.join(result)
            if result != []:
                result = result2.replace('#', '')
                result = result.replace('# ', '')
                result = result.replace('Q/P: ', '')
                result = result.split('☆')
                if 'References ' in result:
                    result.remove('References ')
                for i in range(len(result)):
                    result[i] = 'After ' + result[i]
                    result[i] = ''.join(result[i])
                defalist = defalist + result
        self.choosepart.addItems(defalist)

        self.widgettem = QComboBox(self)
        self.widgettem.setCurrentIndex(0)
        defalist = ['ElegentPaper_Chinese (default)', 'ElegentPaper_English',
                    'ElegentNote_Chinese', 'ElegentNote_English', 'IEEE Conference_English',
                    'JournalPaper_Chinese', 'Beamer_Chinese', 'TexpadTexGeneral_Chinese', 'Customize']
        self.widgettem.addItems(defalist)
        self.widgettem.currentIndexChanged.connect(self.showtemplate)
        self.btn_template = QPushButton('Open a template', self)
        self.btn_template.clicked.connect(self.opentemplate)
        self.btn_template.setMaximumHeight(20)
        self.btn_template.setVisible(False)
        t1_4 = QWidget()
        b1_4 = QHBoxLayout()
        b1_4.setContentsMargins(0, 0, 0, 0)
        b1_4.addWidget(self.widgettem)
        b1_4.addWidget(self.btn_template)
        t1_4.setLayout(b1_4)

        # self.csl_label = QLabel('Citation format:', self)
        self.csl_combo = QComboBox(self)
        csl_options, csl_selected = self.load_csl_options()
        self.csl_combo.addItems(csl_options)
        if self.csl_combo.findText(csl_selected) != -1:
            self.csl_combo.setCurrentIndex(self.csl_combo.findText(csl_selected))
        self.csl_combo.currentIndexChanged.connect(self.csl_index_changed)
        self.csl_combo.showPopup = self._csl_show_popup
        # t1_4_csl = QWidget()
        # b1_4_csl = QHBoxLayout()
        # b1_4_csl.setContentsMargins(0, 0, 0, 0)
        # # b1_4_csl.addWidget(self.csl_label)
        # b1_4_csl.addWidget(self.csl_combo)
        # t1_4_csl.setLayout(b1_4_csl)

        self.leiinote = QLineEdit(self)
        self.leiinote.setPlaceholderText('Always-on remarks (blank = none)')

        t1_5 = QWidget()
        self.leii2 = QLineEdit(self)
        self.leii2.setPlaceholderText('Number (blank = auto mode)')
        self.btn_ia = QPushButton('Insert citation', self)
        self.btn_ia.clicked.connect(self.addcit)
        self.btn_ia.setMaximumHeight(20)
        sm = QHBoxLayout()
        sm.setContentsMargins(0, 0, 0, 0)
        sm.addWidget(self.leii2, 1)
        sm.addWidget(self.btn_ia, 1)
        t1_5.setLayout(sm)

        t1_5_1 = QWidget()
        self.btn_toggle_insp_view = QPushButton('Show header and footer', self)
        self.btn_toggle_insp_view.setMaximumHeight(20)
        self.btn_toggle_insp_view.clicked.connect(self.toggle_inspiration_view)
        self.btn_edit_refs = QPushButton('Edit references', self)
        self.btn_edit_refs.setMaximumHeight(20)
        self.btn_edit_refs.clicked.connect(self.edit_references_dialog)
        sm1 = QHBoxLayout()
        sm1.setContentsMargins(0, 0, 0, 0)
        sm1.addWidget(self.btn_toggle_insp_view, 1)
        sm1.addWidget(self.btn_edit_refs, 1)
        t1_5_1.setLayout(sm1)

        t1_6 = QWidget()
        self.leii3 = QLineEdit(self)
        self.leii3.setPlaceholderText('Row')
        lbl1 = QLabel('×', self)
        self.leii4 = QLineEdit(self)
        self.leii4.setPlaceholderText('Column')
        sm2 = QHBoxLayout()
        sm2.setContentsMargins(0, 0, 0, 0)
        sm2.addWidget(self.leii3, 1)
        sm2.addWidget(lbl1)
        sm2.addWidget(self.leii4, 1)
        t1_6.setLayout(sm2)

        t1_7 = QWidget() # 嵌套了上一组
        btn_ib = QPushButton('Insert table', self)
        btn_ib.clicked.connect(self.addtable)
        btn_ib.setMaximumHeight(20)
        sm3 = QHBoxLayout()
        sm3.setContentsMargins(0, 0, 0, 0)
        sm3.addWidget(t1_6, 1)
        sm3.addWidget(btn_ib, 1)
        t1_7.setLayout(sm3)

        t1_8 = QWidget()
        self.leii5 = QLineEdit(self)
        self.leii5.setPlaceholderText('Caption (blank = auto mode)')
        btn_ic = QPushButton('Insert image', self)
        btn_ic.clicked.connect(self.addimage)
        btn_ic.setMaximumHeight(20)
        sm4 = QHBoxLayout()
        sm4.setContentsMargins(0, 0, 0, 0)
        sm4.addWidget(self.leii5, 1)
        sm4.addWidget(btn_ic, 1)
        t1_8.setLayout(sm4)

        self.btn_ocr_insp = QPushButton('OCR screenshot', self)
        self.btn_ocr_insp.clicked.connect(lambda: self.start_ocr_capture(self.textii1))
        self.btn_ocr_insp.setMaximumHeight(20)
        self._register_ocr_button(self.btn_ocr_insp, 'OCR screenshot')
        t1_ocr = QWidget()
        ocr_layout = QHBoxLayout()
        ocr_layout.setContentsMargins(0, 0, 0, 0)
        #ocr_layout.addStretch()
        ocr_layout.addWidget(self.btn_ocr_insp)
        #ocr_layout.addStretch()
        t1_ocr.setLayout(ocr_layout)

        t2_5 = QWidget()
        self.btn_ia1 = QPushButton('Open a script', self)
        self.btn_ia1.clicked.connect(self.openascr)
        self.btn_ia1.setMaximumHeight(20)
        btn_ib1 = QPushButton('Close current file', self)
        btn_ib1.clicked.connect(self.clinp)
        btn_ib1.setMaximumHeight(20)
        sm0 = QHBoxLayout()
        sm0.setContentsMargins(0, 0, 0, 0)
        sm0.addWidget(self.btn_ia1, 1)
        sm0.addWidget(btn_ib1, 1)
        t2_5.setLayout(sm0)

        t3 = QWidget()
        btn_i1 = QPushButton('Add and clear', self)
        btn_i1.clicked.connect(self.addinssc)
        btn_i1.setMaximumHeight(20)
        btn_i1.setShortcut("Ctrl+Return")
        sm1 = QHBoxLayout()
        sm1.setContentsMargins(0, 0, 0, 0)
        sm1.addWidget(btn_i1)
        t3.setLayout(sm1)

        self.t2 = QWidget()
        self.textii1 = QPlainTextEdit(self)
        self.textii1.setReadOnly(False)
        self.textii1.setObjectName('edit')
        b2 = QVBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addWidget(t1)
        b2.addWidget(self.choosepart)
        b2.addWidget(t1_ocr)
        b2.addWidget(self.textii1)
        b2.addWidget(t3)
        b2.addWidget(t1_4)
        b2.addWidget(self.csl_combo)
        b2.addWidget(self.leiinote)
        b2.addWidget(t1_5)
        b2.addWidget(t1_5_1)
        b2.addWidget(t1_7)
        b2.addWidget(t1_8)
        b2.addWidget(t2_5)
        self.t2.setLayout(b2)

        self.mainii2 = QTabWidget()
        self.ii1_tab = QWidget()
        self.ii2_tab = QWidget()
        self.mainii2.addTab(self.ii1_tab, 'Markdown')
        self.mainii2.addTab(self.ii2_tab, 'LaTeX')
        self.inps1()
        self.inps2()

        # home_dir = str(Path.home())
        # tarname1 = "BroccoliAppPath"
        # self.fulldir1 = os.path.join(home_dir, tarname1)
        # if not os.path.exists(self.fulldir1):
        #     os.mkdir(self.fulldir1)
        # tarname3 = "lang.txt"
        # fulldir3 = os.path.join(self.fulldir1, tarname3)
        # if not os.path.exists(fulldir3):
        #     with open(fulldir3, 'a', encoding='utf-8') as f0:
        #         f0.write('')
        # tarname4 = "model.txt"
        # fulldir4 = os.path.join(self.fulldir1, tarname4)
        # if not os.path.exists(fulldir4):
        #     with open(fulldir4, 'a', encoding='utf-8') as f0:
        #         f0.write('')

        # self.sub2_real1 = QTextEdit(self)
        # self.sub2_real1.setReadOnly(True)

        # self.sub2_text1 = QPlainTextEdit(self)
        # self.sub2_text1.setReadOnly(False)
        # self.sub2_text1.setObjectName('edit')
        # self.sub2_text1.setMaximumHeight(100)
        # self.sub2_text1.setPlaceholderText('Your prompts here...')

        # self.sub2_btn_sub21 = QPushButton('🔺 Send', self)
        # self.sub2_btn_sub21.clicked.connect(self.bot2send)
        # self.sub2_btn_sub21.setFixedSize(80, 20)

        # self.sub2_btn_sub22 = QPushButton('🔸 Clear', self)
        # self.sub2_btn_sub22.clicked.connect(self.bot2clear)
        # self.sub2_btn_sub22.setFixedSize(80, 20)

        # self.sub2_btn_sub23 = QPushButton('🔻 Close', self)
        # self.sub2_btn_sub23.clicked.connect(self.bot2close)
        # self.sub2_btn_sub23.setFixedSize(80, 20)

        # self.sub2_widget0 = QComboBox(self)
        # self.sub2_widget0.setCurrentIndex(0)
        # self.sub2_widget0.addItems(
        #     ['Chat and ask', 'Translate', 'Polish', 'Summarize', 'Grammatically analyze',
        #      'Explain code', 'Customize'])
        # self.sub2_widget0.currentIndexChanged.connect(self.bot2mode)
        # self.sub2_widget0.setMaximumWidth(370)

        # self.sub2_widget1 = QComboBox(self)
        # self.sub2_widget1.setCurrentIndex(0)
        # langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
        # fulllanglist = []
        # langs_list = ['English', '中文', '日本語']
        # if langs != '':
        #     langs_list = langs.split('\n')
        #     while '' in langs_list:
        #         langs_list.remove('')
        #     for i in range(len(langs_list)):
        #         fulllanglist.append(langs_list[i])
        # if langs == '':
        #     for i in range(len(langs_list)):
        #         fulllanglist.append(langs_list[i])
        # self.sub2_widget1.addItems(langs_list)
        # self.sub2_widget1.setVisible(False)
        # self.sub2_widget1.currentIndexChanged.connect(self.bot2trans)

        # self.sub2_lbl1 = QLabel('▶', self)
        # self.sub2_lbl1.setVisible(False)

        # self.sub2_widget2 = QComboBox(self)
        # self.sub2_widget2.setCurrentIndex(0)
        # currentlang = self.sub2_widget1.currentText()
        # while currentlang in langs_list:
        #     langs_list.remove(currentlang)
        # self.sub2_widget2.addItems(langs_list)
        # self.sub2_widget2.setVisible(False)

        # self.sub2_widget4 = QComboBox(self)
        # self.sub2_widget4.setCurrentIndex(0)
        # self.sub2_widget4.addItems(fulllanglist)
        # self.sub2_widget4.setVisible(False)
        # self.sub2_widget4.setFixedWidth(170)

        # self.sub2_widget5 = QComboBox(self)
        # self.sub2_widget5.setCurrentIndex(0)
        # home_dir = str(Path.home())
        # tarname1 = "BroccoliAppPath"
        # fulldir1 = os.path.join(home_dir, tarname1)
        # if not os.path.exists(fulldir1):
        #     os.mkdir(fulldir1)
        # tarname2 = "CustomPrompt.txt"
        # fulldir2 = os.path.join(fulldir1, tarname2)
        # if not os.path.exists(fulldir2):
        #     with open(fulldir2, 'a', encoding='utf-8') as f0:
        #         f0.write('')
        # customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        # promptlist = customprompt.split('---')
        # while '' in promptlist:
        #     promptlist.remove('')
        # itemlist = []
        # for i in range(len(promptlist)):
        #     itemlist.append(promptlist[i].split('|><|')[0].replace('<|', '').replace('\n', ''))
        # if itemlist != []:
        #     self.sub2_widget5.addItems(itemlist)
        # if itemlist == []:
        #     self.sub2_widget5.addItems(['No customized prompts, please add one in Settings'])
        # self.sub2_widget5.setVisible(False)
        # self.sub2_widget5.setFixedWidth(170)
        # self.sub2_widget5.currentIndexChanged.connect(self.bot2custom)

        # qa1 = QWidget()
        # vbox1 = QVBoxLayout()
        # vbox1.setContentsMargins(0, 0, 0, 0)
        # vbox1.addWidget(self.sub2_btn_sub21)
        # vbox1.addWidget(self.sub2_btn_sub22)
        # vbox1.addWidget(self.sub2_btn_sub23)
        # qa1.setLayout(vbox1)

        # qa1_3 = QWidget()
        # vbox1_3 = QHBoxLayout()
        # vbox1_3.setContentsMargins(0, 0, 0, 0)
        # vbox1_3.addWidget(self.sub2_widget0)
        # vbox1_3.addWidget(self.sub2_widget1)
        # vbox1_3.addWidget(self.sub2_lbl1)
        # vbox1_3.addWidget(self.sub2_widget2)
        # vbox1_3.addWidget(self.sub2_widget4)
        # vbox1_3.addWidget(self.sub2_widget5)
        # qa1_3.setLayout(vbox1_3)

        # qa2 = QWidget()
        # vbox2 = QHBoxLayout()
        # vbox2.setContentsMargins(0, 0, 0, 0)
        # vbox2.addWidget(self.sub2_text1)
        # vbox2.addWidget(qa1)
        # qa2.setLayout(vbox2)

        # self.bot2 = QWidget()
        # vbox2_1 = QVBoxLayout()
        # vbox2_1.setContentsMargins(20, 0, 20, 0)
        # vbox2_1.addWidget(self.sub2_real1)
        # vbox2_1.addWidget(qa1_3)
        # vbox2_1.addWidget(qa2)
        # self.bot2.setLayout(vbox2_1)
        # self.bot2.setFixedHeight(300)
        # self.bot2.setVisible(False)

        # self.qabotbox2 = QWidget()
        # botbox = QVBoxLayout()
        # botbox.setContentsMargins(3, 0, 0, 0)
        # botbox.addWidget(self.mainii2)
        # # botbox.addWidget(self.bot2)
        # self.qabotbox2.setLayout(botbox)

        self.mainii3 = QTabWidget()
        self.real_tab2 = QWidget()
        self.mainii3.addTab(self.real_tab2, 'Realtime Markdown')
        self.ret2()
        self.mainii3.setVisible(False)

        self.page3_v_box = QHBoxLayout()
        self.page3_v_box.addWidget(self.t2, 1)
        self.page3_v_box.addWidget(self.mainii2, 1)
        self.page3_v_box.addWidget(self.mainii3, 1)
        self.insp_tab.setLayout(self.page3_v_box)

    def showtemplate(self, i):
        if i == 8:
            self.btn_template.setVisible(True)
            self.btn_template.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
            self.btn_template.setText('Open a template')
            self.template_p1 = ''
            self.template_p2 = ''
            self.template_p3 = ''
            self.template_p4 = ''
            self.template_p5 = ''
            self.template_p6 = ''
        if i != 8:
            self.btn_template.setVisible(False)

    def _ensure_csl_files(self):
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        csl_dir = os.path.join(base_dir, "CitationFormat")
        if not os.path.exists(csl_dir):
            os.mkdir(csl_dir)
        formats_file = os.path.join(csl_dir, "formats.txt")
        if not os.path.exists(formats_file):
            with open(formats_file, 'a', encoding='utf-8') as f0:
                f0.write('')
        selected_file = os.path.join(csl_dir, "selected_format.txt")
        if not os.path.exists(selected_file):
            with open(selected_file, 'w', encoding='utf-8') as f0:
                f0.write('Quick cite (defaut)')
        return formats_file, selected_file

    def load_csl_options(self):
        formats_file, selected_file = self._ensure_csl_files()
        formats = codecs.open(formats_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '']
        selected = codecs.open(selected_file, 'r', encoding='utf-8').read().strip()
        if selected == '':
            selected = 'Quick cite (defaut)'
        options = ['Quick cite (defaut)'] + formats
        if selected not in options:
            selected = 'Quick cite (defaut)'
        return options, selected

    def csl_index_changed(self, idx):
        _, selected_file = self._ensure_csl_files()
        with open(selected_file, 'w', encoding='utf-8') as f0:
            f0.write(self.csl_combo.currentText())

    def _csl_show_popup(self):
        csl_options, csl_selected = self.load_csl_options()
        current_text = self.csl_combo.currentText()
        self.csl_combo.blockSignals(True)
        self.csl_combo.clear()
        self.csl_combo.addItems(csl_options)
        if self.csl_combo.findText(current_text) != -1:
            self.csl_combo.setCurrentIndex(self.csl_combo.findText(current_text))
        elif self.csl_combo.findText(csl_selected) != -1:
            self.csl_combo.setCurrentIndex(self.csl_combo.findText(csl_selected))
        else:
            self.csl_combo.setCurrentIndex(0)
        self.csl_combo.blockSignals(False)
        QComboBox.showPopup(self.csl_combo)

    def _ensure_citation_format_list(self):
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        csl_dir = os.path.join(base_dir, "CitationFormat")
        if not os.path.exists(csl_dir):
            os.mkdir(csl_dir)
        list_file = os.path.join(csl_dir, "formats.txt")
        if not os.path.exists(list_file):
            with open(list_file, 'a', encoding='utf-8') as f0:
                f0.write('')
        formats = codecs.open(list_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '']
        return formats

    def _init_citation_files(self, title, script_dir):
        title = title or self._get_citation_title_key()
        if title == '' or script_dir == '':
            return
        cit_dir = os.path.join(script_dir, 'StrawberryCitations')
        if not os.path.exists(cit_dir):
            os.mkdir(cit_dir)
        sub_dir = os.path.join(cit_dir, title)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        formats = ['quickcite'] + self._ensure_citation_format_list()
        for fmt in formats:
            base_name = f"{title}-{fmt}.txt"
            base_path = os.path.join(sub_dir, base_name)
            if not os.path.exists(base_path):
                with open(base_path, 'a', encoding='utf-8') as f0:
                    f0.write('')
            inline_name = f"{title}-{fmt}-in.txt"
            inline_path = os.path.join(sub_dir, inline_name)
            if not os.path.exists(inline_path):
                with open(inline_path, 'a', encoding='utf-8') as f0:
                    f0.write('')
        bib_path = os.path.join(sub_dir, f"{title}.bib")
        if not os.path.exists(bib_path):
            with open(bib_path, 'a', encoding='utf-8') as f0:
                f0.write('')

    def opentemplate(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = 'Templates'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.mkdir(fulldir2)

        fj = QFileDialog.getExistingDirectory(self, 'Open', fulldir2)
        if fj != '':
            # part1
            tarname_p1 = " part1.txt"
            fulldir_p1 = os.path.join(fj, tarname_p1)
            # part2
            tarname_p2 = " part2.txt"
            fulldir_p2 = os.path.join(fj, tarname_p2)
            # part3
            tarname_p3 = " part3.txt"
            fulldir_p3 = os.path.join(fj, tarname_p3)
            # part4
            tarname_p4 = " part4.txt"
            fulldir_p4 = os.path.join(fj, tarname_p4)
            # part5
            tarname_p5 = " part5.txt"
            fulldir_p5 = os.path.join(fj, tarname_p5)
            # part6
            tarname_p6 = " part6.txt"
            fulldir_p6 = os.path.join(fj, tarname_p6)
            if os.path.exists(fulldir_p1) and os.path.exists(fulldir_p2) and os.path.exists(fulldir_p3) and os.path.exists(fulldir_p4) and os.path.exists(fulldir_p5) and os.path.exists(fulldir_p6):
                self.template_p1 = codecs.open(fulldir_p1, 'r', encoding='utf-8').read()
                self.template_p2 = codecs.open(fulldir_p2, 'r', encoding='utf-8').read()
                self.template_p3 = codecs.open(fulldir_p3, 'r', encoding='utf-8').read()
                self.template_p4 = codecs.open(fulldir_p4, 'r', encoding='utf-8').read()
                self.template_p5 = codecs.open(fulldir_p5, 'r', encoding='utf-8').read()
                self.template_p6 = codecs.open(fulldir_p6, 'r', encoding='utf-8').read()
                self.btn_template.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
                self.btn_template.setText('Opened')
            else:
                CMD = '''
                    on run argv
                        display notification (item 2 of argv) with title (item 1 of argv)
                    end run'''
                self.notify(CMD, "Strawberry: Your Literature Collector",
                            f"The template file is broken. Please set it again!")

    def notify(self, CMD, title, text):
        subprocess.call(['osascript', '-e', CMD, title, text])

    def _set_citation_controls_enabled(self, enabled: bool):
        for ctl_name in ['csl_combo', 'btn_insia', 'btn_edit_refsa', 'btn_ia', 'btn_edit_refs']:
            ctl = getattr(self, ctl_name, None)
            if ctl is not None:
                ctl.setEnabled(enabled)

    def chooseind(self, i):
        if i == 0 and self.leii1.text() != '':
            with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                f0.write('')
        if i != 0 and i != 1 and self.leii1.text() != '':
            path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            def _candidate_names(raw):
                cands = [raw]
                try:
                    import re as _re
                    base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                    if base1 and base1 not in cands:
                        cands.append(base1)
                    base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                    if base2 and base2 not in cands:
                        cands.append(base2)
                except Exception:
                    pass
                return cands

            fulldir1 = ''
            for nm in _candidate_names(str(self.leii1.text())):
                tarname1 = nm + ".md"
                candidate = os.path.join(path1, tarname1)
                if os.path.exists(candidate):
                    fulldir1 = candidate
                    break
            if fulldir1 == '':
                tarname1 = str(self.leii1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            if i < self.choosepart.count() - 1:
                tarnum = int(self.choosepart.currentIndex() + 1)
                searcde = str(self.choosepart.itemText(tarnum))
                searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]').replace('.', '\.').replace('*', '\*').replace('+', '\+').replace('?', '\?').replace('|', '\|').replace('(', '\(').replace(')', '\)').replace('{', '\{').replace('}', '\}').replace('^', '\^').replace('$', '\$')
                sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                if sst != None:
                    with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                        f0.write(sst.group())
            if i == self.choosepart.count() - 1:
                with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')

    def inps1(self):
        self.textii2_head = QTextEdit(self)
        self.textii2_head.setReadOnly(True)
        self.textii2_head.setMaximumHeight(40)
        self.textii2_head.setMinimumHeight(20)
        self.textii2 = QTextEdit(self)
        self.textii2.setReadOnly(False)
        self.textii2.textChanged.connect(self.on_text2_textChanged)
        self.textii2.cursorPositionChanged.connect(self.cursortemp)
        self.textii2_foot = QTextEdit(self)
        self.textii2_foot.setReadOnly(True)
        #self.textii2_foot.setMaximumHeight(0)
        self.textii2_foot.setMinimumHeight(20)
        self.scrollbar2 = self.textii2.verticalScrollBar()
        self.scrollbar2.valueChanged.connect(self.scr_cha2)

        tvt1 = QWidget()
        self.btnbot_ins = QPushButton('', self)
        self.btnbot_ins.clicked.connect(self.bot2show)
        self.btnbot_ins.setFixedSize(20, 20)
        self.btnbot_ins.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_insia = QPushButton('Insert citation', self)
        self.btn_insia.clicked.connect(self.addcit)
        self.btn_insia.setMaximumHeight(20)
        self.btn_insia.setVisible(False)
        self.btn_toggle_insp_viewa = QPushButton('Show header and footer', self)
        self.btn_toggle_insp_viewa.setMaximumHeight(20)
        self.btn_toggle_insp_viewa.clicked.connect(self.toggle_inspiration_view)
        self.btn_toggle_insp_viewa.setVisible(False)
        self.btn_edit_refsa = QPushButton('Edit references', self)
        self.btn_edit_refsa.setMaximumHeight(20)
        self.btn_edit_refsa.clicked.connect(self.edit_references_dialog)
        self.btn_edit_refsa.setVisible(False)
        btn_ins1 = QPushButton('Hard save and generate LaTeX', self)
        btn_ins1.clicked.connect(self.saveinsp)
        btn_ins1.setMaximumHeight(20)
        btn_ins1.setShortcut('Ctrl+Shift+Return')
        # self.btnbot_card = QPushButton('', self)
        # # self.btnbot_card.clicked.connect(self.showlist)
        # self.btnbot_card.setFixedSize(20, 20)
        # self.btnbot_card.setStyleSheet('''
        #     QPushButton{
        #     border: transparent;
        #     background-color: transparent;
        #     border-image: url(/Applications/Strawberry.app/Contents/Resources/card.png);
        #     }
        #     QPushButton:pressed{
        #     border: 1px outset grey;
        #     background-color: #0085FF;
        #     border-radius: 4px;
        #     padding: 1px;
        #     color: #FFFFFF
        #     }
        #     ''')
        stvt1 = QHBoxLayout()
        stvt1.setContentsMargins(0, 4, 0, 0)
        stvt1.addWidget(self.btnbot_ins)
        stvt1.addWidget(self.btn_insia, 1)
        stvt1.addWidget(self.btn_toggle_insp_viewa, 1)
        stvt1.addWidget(self.btn_edit_refsa, 1)
        stvt1.addWidget(btn_ins1, 2)
        # stvt1.addWidget(self.btnbot_card)
        tvt1.setLayout(stvt1)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.textii2_head)
        splitter.addWidget(self.textii2)
        splitter.addWidget(self.textii2_foot)
        splitter.setSizes([40, 600, 200])

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(splitter)
        page3_box_h.addWidget(tvt1)
        self.ii1_tab.setLayout(page3_box_h)
        self.insp_show_full = False
        self._apply_inspiration_view()

    def inps2(self):
        self.textii3 = QTextEdit(self)
        self.textii3.setReadOnly(False)
        self.textii3.textChanged.connect(self.on_text_textChanged_latex)

        self.btnbot_ins2 = QPushButton('', self)
        self.btnbot_ins2.clicked.connect(self.bot2show)
        self.btnbot_ins2.setFixedSize(20, 20)
        self.btnbot_ins2.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btn_ins2 = QPushButton('Hard save', self)
        btn_ins2.clicked.connect(self.savelat)
        btn_ins2.setMaximumHeight(20)
        btn_ins2.setShortcut('Ctrl+Shift+Return')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        btnbox.addWidget(self.btnbot_ins2)
        btnbox.addWidget(btn_ins2)
        btnwid.setLayout(btnbox)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.textii3)
        page3_box_h.addWidget(btnwid)
        self.ii2_tab.setLayout(page3_box_h)

    def cursortemp(self):
        if getattr(self, '_suppress_cursor_capture', False):
            return
        if self.textii2.toPlainText() != '' and self.leii1.text() != '':
            self.textii2.ensureCursorVisible()
            cursor = self.textii2.textCursor()
            current_text = self.textii2.toPlainText()
            position = max(0, min(cursor.position(), len(current_text)))
            remove_str = current_text[position:]
            with open(BasePath + 'cite_position.txt', 'w', encoding='utf-8') as f0:
                f0.write(remove_str)
            with open(BasePath + 'cite_position_idx.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(position))

            if self.choosepart.currentIndex() == 0:
                with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')
            if self.choosepart.currentIndex() == 1:
                with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                    f0.write(remove_str)
                with open(BasePath + 'currentcursor2.txt', 'w', encoding='utf-8') as f0:
                    f0.write(remove_str)
            if self.choosepart.currentIndex() != 0 and self.choosepart.currentIndex() != 1:
                maintxt = current_text
                if self.choosepart.currentIndex() < self.choosepart.count() - 1:
                    tarnum = int(self.choosepart.currentIndex() + 1)
                    searcde = str(self.choosepart.itemText(tarnum))
                    searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]').replace('.',
                                                                                                          '\.').replace(
                        '*', '\*').replace('+', '\+').replace('?', '\?').replace('|', '\|').replace('(', '\(').replace(
                        ')', '\)').replace('{', '\{').replace('}', '\}').replace('^', '\^').replace('$', '\$')
                    sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                    if sst != None:
                        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                            f0.write(sst.group())
            if self.choosepart.currentIndex() == self.choosepart.count() - 1:
                with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')

    def _strip_inspiration_body(self, full_text):
        body = full_text.replace('\r', '')
        # strip header even if slightly malformed (e.g., {!--Title: ...--})
        body = re.sub(r'^\s*<document-start>\s*[\n\r]*', '', body, count=1)
        body = re.sub(r'^\s*[<{]!--Title:.*?--[>}]?\s*', '', body, count=1)
        ref_idx = body.find('\n## References ')
        if ref_idx != -1:
            body = body[:ref_idx]
        return body.lstrip('\n')

    def _build_inspiration_header(self):
        def _candidate_names(raw):
            cands = [raw]
            try:
                import re as _re
                base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                if base1 and base1 not in cands:
                    cands.append(base1)
                base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                if base2 and base2 not in cands:
                    cands.append(base2)
            except Exception:
                pass
            return cands

        def _resolve_path(dir_path, raw_name, ext):
            for nm in _candidate_names(raw_name):
                cand = os.path.join(dir_path, nm + ext)
                if os.path.exists(cand):
                    return cand
            return os.path.join(dir_path, raw_name + ext)

        existing_title = ''
        try:
            path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path_scr != '' and self.leii1.text() != '':
                fulldir = _resolve_path(path_scr, str(self.leii1.text()), ".md")
                if os.path.exists(fulldir):
                    contend = codecs.open(fulldir, 'r', encoding='utf-8').read()
                    patt = re.compile(r'<!--Title: (.*?)-->')
                    res = patt.findall(contend)
                    res = ''.join(res).strip()
                    if res != '':
                        existing_title = res
        except Exception:
            existing_title = ''
        if existing_title != '':
            self._cached_title_key = existing_title
            return '<document-start>\n<!--Title: ' + existing_title + '-->'
        cached_title = getattr(self, '_cached_title_key', '')
        if cached_title != '':
            return '<document-start>\n<!--Title: ' + cached_title + '-->'
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        base_title = str(self.leii1.text()).strip()
        new_title = (base_title + ' ' + ts).strip() if base_title != '' else ts
        self._cached_title_key = new_title
        return '<document-start>\n<!--Title: ' + new_title + '-->'

    def _get_citation_title_key(self):
        title_plain = str(self.leii1.text())
        path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if title_plain != '' and path1 != '':
            tarname = title_plain + ".md"
            fulldir = os.path.join(path1, tarname)
            if os.path.exists(fulldir):
                try:
                    contend = codecs.open(fulldir, 'r', encoding='utf-8').read()
                    patt = re.compile(r'<!--Title: (.*?)-->')
                    res = patt.findall(contend)
                    res = ''.join(res).strip()
                    if res != '':
                        return res
                except Exception:
                    pass
        return title_plain

    def _build_inspiration_references(self):
        tcy = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').readlines()
        i = 0
        while i >= 0 and i <= len(tcy) - 1:
            ref_line = tcy[i].replace('\r', '').rstrip('\n')
            ref_line = re.sub(r'<e>\s*$', '', ref_line)
            tcy[i] = ref_line + '<e>'
            i = i + 1
            continue
        tcq = ''.join(tcy)
        tcq = tcq.replace('\n', '')
        tcq = tcq.replace('<e>', '<e>\n')
        tcq = tcq.rstrip('\n')
        qiam = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
        partb = '\n\n\n\n' + '## References '
        partc = '\n\n' + tcq if qiam != '' else '\n' + tcq
        partd = '\n\n<document-end>'
        return partb + partc + partd

    def _compose_inspiration_file(self, body_text):
        header = self._build_inspiration_header()
        body = body_text.rstrip('\n')
        return header + '\n' + body + self._build_inspiration_references()

    def _write_inspiration_body(self, body_text):
        if self.leii1.text() == '':
            return
        path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            return
        cursor = self.textii2.textCursor()
        current_pos = cursor.position()
        vbar = self.textii2.verticalScrollBar()
        old_scroll_value = vbar.value()
        old_scroll_max = vbar.maximum()
        tarname1 = str(self.leii1.text()) + ".md"
        fulldir1 = os.path.join(path1, tarname1)
        composed = self._compose_inspiration_file(body_text)
        with open(fulldir1, 'w', encoding='utf-8') as f1:
            f1.write(composed)
        prev_suppress = getattr(self, '_suppress_cursor_capture', False)
        if not prev_suppress:
            self._suppress_cursor_capture = True
        self._show_inspiration_content(composed)
        body_len = len(self.textii2.toPlainText())
        restore_pos = max(0, min(body_len, current_pos))
        cursor = self.textii2.textCursor()
        cursor.setPosition(restore_pos)
        self.textii2.setTextCursor(cursor)
        if not prev_suppress:
            self._suppress_cursor_capture = False
        def _restore_scroll():
            vbar = self.textii2.verticalScrollBar()
            new_scroll_max = vbar.maximum()
            if new_scroll_max <= 0:
                return
            target = old_scroll_value
            if old_scroll_max > 0 and old_scroll_value >= old_scroll_max - 2:
                target = new_scroll_max
            vbar.setValue(max(0, min(new_scroll_max, target)))

        QTimer.singleShot(0, _restore_scroll)

    def _start_inspiration_autosave(self):
        if self.insp_backup_timer:
            self.insp_backup_timer.stop()
        self.insp_backup_timer = QTimer(self)
        self.insp_backup_timer.setInterval(60 * 1000)
        self.insp_backup_timer.timeout.connect(self._trigger_inspiration_backup)
        self.insp_backup_timer.start()

    def _trigger_inspiration_backup(self):
        if self.insp_updating:
            return
        title_raw = self.leii1.text().strip()
        if title_raw == '':
            return
        path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path_scr == '':
            return
        source_path = os.path.join(path_scr, f"{title_raw}.md")
        if not os.path.exists(source_path):
            return

        # Check file modification time to avoid redundant backups
        try:
            current_mtime = os.path.getmtime(source_path)
            current_size = os.path.getsize(source_path)
            current_meta = (source_path, current_mtime, current_size)

            # Skip backup if file hasn't changed since last backup
            if self._last_insp_backup_meta == current_meta:
                return

            # Update metadata record
            self._last_insp_backup_meta = current_meta
        except Exception:
            return

        try:
            with open(source_path, 'r', encoding='utf-8') as fp:
                content = fp.read()
        except Exception:
            return
        safe_title = re.sub(r'[\\\\/:*?"<>|]', '_', title_raw)
        backup_dir = self._inspiration_backup_target_dir(path_scr, safe_title)
        threading.Thread(
            target=self._perform_inspiration_backup,
            args=(backup_dir, content),
            daemon=True
        ).start()

    def _inspiration_backup_target_dir(self, base_path, safe_title):
        backup_root = os.path.join(base_path, 'StrawberryBackups')
        os.makedirs(backup_root, exist_ok=True)
        target_dir = os.path.join(backup_root, safe_title)
        os.makedirs(target_dir, exist_ok=True)
        return target_dir

    def _perform_inspiration_backup(self, target_dir, content):
        with self._insp_backup_lock:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(target_dir, f"{timestamp}.md")
            try:
                with open(backup_path, 'w', encoding='utf-8') as fp:
                    fp.write(content)
            except Exception:
                return
            limit = load_inspiration_backup_limit()
            self._enforce_inspiration_backup_limit(target_dir, limit)

    def _enforce_inspiration_backup_limit(self, target_dir, limit):
        if limit <= 0:
            return
        try:
            md_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith('.md')]
        except Exception:
            return
        if len(md_files) <= limit:
            return
        md_files.sort(key=os.path.getmtime)
        for old_file in md_files[:-limit]:
            try:
                os.remove(old_file)
            except Exception:
                continue

    # def _insert_inspiration_at_choice(self, insertion_text):
    #     body_now = self.textii2.toPlainText()
    #     if body_now.strip() == '' and self.leii1.text() != '':
    #         body_now = '# ' + str(self.leii1.text())
    #     tail = codecs.open(BasePath + 'path_pat.txt', 'r', encoding='utf-8').read()
    #     idx = self.choosepart.currentIndex()
    #     last = self.choosepart.count() - 1
    #     # 针对只有“末尾/当前光标”两个选项的场景，idx==1应视为当前光标
    #     if idx == 1 and self.choosepart.count() == 2:
    #         if tail != '' and tail in body_now:
    #             head = body_now[:-len(tail)]
    #             new_body = head + insertion_text + tail
    #         else:
    #             # 若未捕获到尾部，退化为按照当前位置（cite_position_idx）插入
    #             try:
    #                 pos_str = codecs.open(BasePath + 'cite_position_idx.txt', 'r', encoding='utf-8').read().strip()
    #                 pos = int(pos_str) if pos_str != '' else len(body_now)
    #             except Exception:
    #                 pos = len(body_now)
    #             pos = max(0, min(len(body_now), pos))
    #             new_body = body_now[:pos] + insertion_text + body_now[pos:]
    #     elif idx == 1 and tail != '' and tail in body_now:
    #         head = body_now[:-len(tail)]
    #         new_body = head + insertion_text + tail
    #     elif idx == 1 and (tail == '' or tail not in body_now):
    #         new_body = body_now + insertion_text
    #     elif idx == 0 or idx == last:
    #         new_body = body_now + insertion_text
    #     else:
    #         new_body = body_now.replace(tail, insertion_text + tail, 1) if tail in body_now else body_now + insertion_text
    #     self._write_inspiration_body(new_body)

    def _apply_inspiration_view(self):
        self.textii2_head.setVisible(self.insp_show_full)
        self.textii2_foot.setVisible(self.insp_show_full)
        self.btn_toggle_insp_view.setText('Hide header and footer' if self.insp_show_full else 'Show header and footer')

    def _show_inspiration_content(self, full_text):
        self.insp_updating = True
        body = self._strip_inspiration_body(full_text)
        self.textii2_head.setPlainText(self._build_inspiration_header())
        self.textii2.setPlainText(body)
        self.textii2_foot.setPlainText(self._build_inspiration_references())
        self._apply_inspiration_view()
        self.insp_updating = False

    def toggle_inspiration_view(self):
        self.insp_show_full = not self.insp_show_full
        self._apply_inspiration_view()

    def edit_references_dialog(self):
        warn = CustomDialog_edit_reference()
        warn.exec()
        # dlg = QDialog(self)
        # dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # #dlg.setAttribute(Qt.WA_TranslucentBackground, True)  # 允许透明背景以显示圆角
        # dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # # 用一个容器部件来承载内容并加圆角背景
        # container = QWidget(dlg)
        # container.setStyleSheet("""
        #     QWidget {
        #         border: 1px solid #ECECEC;
        #         background: #ECECEC;
        #         border-radius: 9px;
        #     }
        #     QPushButton{
        #         border: 1px outset grey;
        #         background-color: #FFFFFF;
        #         border-radius: 4px;
        #         padding: 1px;
        #         color: #000000
        #     }
        #     QPushButton:pressed{
        #         border: 1px outset grey;
        #         background-color: #0085FF;
        #         border-radius: 4px;
        #         padding: 1px;
        #         color: #FFFFFF
        #     }
        #     QTextEdit{
        #         border: 1px solid grey;  
        #         border-radius:4px;
        #         padding: 1px 5px 1px 3px; 
        #         background-clip: border;
        #         background-color: #F3F2EE;
        #         color: #000000;
        #         font: 14pt Times New Roman;
        #     }
        # """)

        # lay = QVBoxLayout(container)
        # editor = QTextEdit(container)
        # editor.setPlainText(codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read())
        # editor.setStyleSheet('''
        #     QTextEdit{
        #         border: 1px solid grey;  
        #         border-radius:4px;
        #         padding: 1px 5px 1px 3px; 
        #         background-clip: border;
        #         background-color: #F3F2EE;
        #         color: #000000;
        #         font: 14pt Times New Roman;
        #     }
        #     QTextEdit QScrollBar:vertical {
        #         width: 6px;
        #         background: transparent;
        #         margin: 2px 1px 2px 1px;
        #     }
        #     QTextEdit QScrollBar::handle:vertical {
        #         background: rgba(0,0,0,0.18);
        #         border-radius: 3px;
        #         min-height: 30px;
        #     }
        #     QTextEdit QScrollBar::handle:vertical:hover,
        #     QTextEdit QScrollBar::handle:vertical:pressed {
        #         background: rgba(0,0,0,0.35);
        #         border-radius: 3px;
        #     }
        #     QTextEdit QScrollBar::add-line:vertical,
        #     QTextEdit QScrollBar::sub-line:vertical {
        #         height: 0;
        #         border: none;
        #         background: transparent;
        #     }
        #     QTextEdit QScrollBar::add-page:vertical,
        #     QTextEdit QScrollBar::sub-page:vertical {
        #         background: transparent;
        #     }
        #     /* 悬停时稍微变宽，模拟“滑动才出现” */
        #     QTextEdit:hover QScrollBar:vertical {
        #         width: 8px;
        #     }
        #     QTextEdit:hover QScrollBar:horizontal {
        #         height: 8px;
        #     }
        # ''')
        # lay.addWidget(editor)

        # btn_box = QHBoxLayout()
        # btn_save = QPushButton('Save', container)
        # btn_cancel = QPushButton('Cancel', container)
        # btn_box.addWidget(btn_save)
        # btn_box.addWidget(btn_cancel)
        # lay.addLayout(btn_box)

        # outer = QVBoxLayout(dlg)
        # outer.setContentsMargins(0, 0, 0, 0)
        # outer.addWidget(container)
        # dlg.setLayout(outer)

        # def save_refs():
        #     with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as fp:
        #         fp.write(editor.toPlainText())
        #     if self.leii1.text() != '':
        #         path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        #         if path1 != '':
        #             tarname1 = str(self.leii1.text()) + ".md"
        #             fulldir1 = os.path.join(path1, tarname1)
        #             body_text = self._strip_inspiration_body(self.textii2.toPlainText()) if self.insp_show_full else self.textii2.toPlainText()
        #             with open(fulldir1, 'w', encoding='utf-8') as f1:
        #                 f1.write(self._compose_inspiration_file(body_text))
        #     dlg.accept()

        # btn_save.clicked.connect(save_refs)
        # btn_cancel.clicked.connect(dlg.reject)
        # dlg.exec()

    def sub1(self):
        self.text = QTextEdit(self)
        self.text.setReadOnly(False)
        self.text.setMinimumHeight(140)
        self.text.textChanged.connect(self.on_text_textChanged)
        self.text.cursorPositionChanged.connect(self.cursorchanged)
        self.scrollbar = self.text.verticalScrollBar()
        self.scrollbar.valueChanged.connect(self.scr_cha)

        self.btnbot_text1 = QPushButton('', self)
        self.btnbot_text1.clicked.connect(self.bot1show)
        self.btnbot_text1.setFixedSize(20, 20)
        self.btnbot_text1.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btn_sub1 = QPushButton('Hard save', self)
        btn_sub1.clicked.connect(self.save1)
        btn_sub1.setMaximumHeight(20)
        btn_sub1.setShortcut('Ctrl+Shift+Return')

        self.btnbot_cite1 = QPushButton('', self)
        self.btnbot_cite1.clicked.connect(self.cite1)
        self.btnbot_cite1.setFixedSize(20, 20)
        self.btnbot_cite1.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/cite.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        btnbox.addWidget(self.btnbot_text1)
        btnbox.addWidget(btn_sub1)
        btnbox.addWidget(self.btnbot_cite1)
        btnwid.setLayout(btnbox)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text)
        page3_box_h.addWidget(btnwid)
        self.sub1_tab.setLayout(page3_box_h)

    def sub2(self):
        self.text_s2 = QTextEdit(self)
        self.text_s2.setReadOnly(False)
        self.text_s2.setMinimumHeight(140)
        self.text_s2.textChanged.connect(self.on_text_textChanged_concept)

        self.btnbot_text2 = QPushButton('', self)
        self.btnbot_text2.clicked.connect(self.bot1show)
        self.btnbot_text2.setFixedSize(20, 20)
        self.btnbot_text2.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btn_sub2 = QPushButton('Hard save', self)
        btn_sub2.clicked.connect(self.save2)
        btn_sub2.setMaximumHeight(20)
        btn_sub2.setShortcut('Ctrl+Shift+Return')

        self.btnbot_cite2 = QPushButton('', self)
        self.btnbot_cite2.clicked.connect(self.cite2)
        self.btnbot_cite2.setFixedSize(20, 20)
        self.btnbot_cite2.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/cite.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        btnbox.addWidget(self.btnbot_text2)
        btnbox.addWidget(btn_sub2)
        btnbox.addWidget(self.btnbot_cite2)
        btnwid.setLayout(btnbox)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s2)
        page3_box_h.addWidget(btnwid)
        self.sub2_tab.setLayout(page3_box_h)

    def sub3(self):
        self.text_s3 = QTextEdit(self)
        self.text_s3.setReadOnly(False)
        self.text_s3.setMinimumHeight(140)
        self.text_s3.textChanged.connect(self.on_text_textChanged_theory)

        self.btnbot_text3 = QPushButton('', self)
        self.btnbot_text3.clicked.connect(self.bot1show)
        self.btnbot_text3.setFixedSize(20, 20)
        self.btnbot_text3.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btn_sub3 = QPushButton('Hard save', self)
        btn_sub3.clicked.connect(self.save3)
        btn_sub3.setMaximumHeight(20)
        btn_sub3.setShortcut('Ctrl+Shift+Return')

        self.btnbot_cite3 = QPushButton('', self)
        self.btnbot_cite3.clicked.connect(self.cite3)
        self.btnbot_cite3.setFixedSize(20, 20)
        self.btnbot_cite3.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/cite.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        btnbox.addWidget(self.btnbot_text3)
        btnbox.addWidget(btn_sub3)
        btnbox.addWidget(self.btnbot_cite3)
        btnwid.setLayout(btnbox)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s3)
        page3_box_h.addWidget(btnwid)
        self.sub3_tab.setLayout(page3_box_h)

    def sub4(self):
        self.text_s4 = QTextEdit(self)
        self.text_s4.setReadOnly(False)
        self.text_s4.setMinimumHeight(140)
        self.text_s4.textChanged.connect(self.on_text_textChanged_method)

        self.btnbot_text4 = QPushButton('', self)
        self.btnbot_text4.clicked.connect(self.bot1show)
        self.btnbot_text4.setFixedSize(20, 20)
        self.btnbot_text4.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/bot.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btn_sub4 = QPushButton('Hard save', self)
        btn_sub4.clicked.connect(self.save4)
        btn_sub4.setMaximumHeight(20)
        btn_sub4.setShortcut('Ctrl+Shift+Return')

        self.btnbot_cite4 = QPushButton('', self)
        self.btnbot_cite4.clicked.connect(self.cite4)
        self.btnbot_cite4.setFixedSize(20, 20)
        self.btnbot_cite4.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/cite.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')

        btnwid = QWidget()
        btnbox = QHBoxLayout()
        btnbox.setContentsMargins(0, 4, 0, 0)
        btnbox.addWidget(self.btnbot_text4)
        btnbox.addWidget(btn_sub4)
        btnbox.addWidget(self.btnbot_cite4)
        btnwid.setLayout(btnbox)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s4)
        page3_box_h.addWidget(btnwid)
        self.sub4_tab.setLayout(page3_box_h)

    def ext_r(self):
        self.speaker = QLineEdit(self)
        self.speaker.setPlaceholderText('Speaker')
        self.speaker.setVisible(False)

        self.text11 = QPlainTextEdit(self)
        self.text11.setReadOnly(False)
        self.text11.setObjectName("edit")
        self.text11.setPlaceholderText('Problems / questions')
        sl1 = QWidget()
        self.btnoldpro = QPushButton('', self)
        self.btnoldpro.clicked.connect(self.show_list_pro)
        self.btnoldpro.setFixedSize(20, 20)
        self.btnoldpro.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/grid.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_ex11 = QPushButton('Add', self)
        self.btn_ex11.clicked.connect(self.addprob)
        self.btn_ex11.setMaximumHeight(20)
        btn_111 = QPushButton('Clear', self)
        btn_111.clicked.connect(self.clearpro)
        btn_111.setMaximumHeight(20)
        sm1 = QHBoxLayout()
        sm1.setContentsMargins(0, 0, 0, 0)
        sm1.addWidget(self.btnoldpro)
        sm1.addWidget(self.btn_ex11)
        sm1.addWidget(btn_111)
        sl1.setLayout(sm1)

        self.text12 = QPlainTextEdit(self)
        self.text12.setReadOnly(False)
        self.text12.setObjectName("edit")
        self.text12.setPlaceholderText('Claims')
        sl2 = QWidget()
        self.btn_cl12 = QPushButton('Add', self)
        self.btn_cl12.clicked.connect(self.addcla)
        self.btn_cl12.setMaximumHeight(20)
        btn_121 = QPushButton('Clear', self)
        btn_121.clicked.connect(self.clearcla)
        btn_121.setMaximumHeight(20)
        sm2 = QHBoxLayout()
        sm2.setContentsMargins(0, 0, 0, 0)
        sm2.addWidget(self.btn_cl12)
        sm2.addWidget(btn_121)
        sl2.setLayout(sm2)

        self.text13 = QPlainTextEdit(self)
        self.text13.setReadOnly(False)
        self.text13.setObjectName("edit")
        self.text13.setPlaceholderText('Analysis')
        sl3 = QWidget()
        self.btn_ana13 = QPushButton('Add', self)
        self.btn_ana13.clicked.connect(self.addana)
        self.btn_ana13.setMaximumHeight(20)
        btn_131 = QPushButton('Clear', self)
        btn_131.clicked.connect(self.clearana)
        btn_131.setMaximumHeight(20)
        sm3 = QHBoxLayout()
        sm3.setContentsMargins(0, 0, 0, 0)
        sm3.addWidget(self.btn_ana13)
        sm3.addWidget(btn_131)
        sl3.setLayout(sm3)

        self.text14 = QPlainTextEdit(self)
        self.text14.setReadOnly(False)
        self.text14.setObjectName("edit")
        self.text14.setPlaceholderText('My views')
        sl4 = QWidget()
        btn_14 = QPushButton('Add and clear', self)
        btn_14.clicked.connect(self.addmy)
        btn_14.setMaximumHeight(20)
        btn_14.setShortcut("Ctrl+Return")
        '''btn_141 = QPushButton('Clear', self)
        btn_141.clicked.connect(self.clearmy)
        btn_141.setMaximumHeight(20)'''
        sm4 = QHBoxLayout()
        sm4.setContentsMargins(0, 0, 0, 0)
        sm4.addWidget(btn_14)
        # sm4.addWidget(btn_141)
        sl4.setLayout(sm4)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.speaker)
        page3_box_h.addWidget(self.text11)
        page3_box_h.addWidget(sl1)
        page3_box_h.addWidget(self.text12)
        page3_box_h.addWidget(sl2)
        page3_box_h.addWidget(self.text13)
        page3_box_h.addWidget(sl3)
        page3_box_h.addWidget(self.text14)
        page3_box_h.addWidget(sl4)
        self.one_tab.setLayout(page3_box_h)

    def show_list_pro(self):
        warn = CustomDialog_list_pro()
        warn.exec()

    def cite1(self):
        warn = CustomDialog_list_cite()
        warn.exec()

    def int_r(self):
        top_box = QWidget()
        self.le20 = QLineEdit(self)
        self.le20.setPlaceholderText('Part')
        self.le21 = QLineEdit(self)
        self.le21.setPlaceholderText('Page')
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(self.le20)
        b1.addWidget(self.le21)
        top_box.setLayout(b1)

        self.text21 = QPlainTextEdit(self)
        self.text21.setReadOnly(False)
        self.text21.setObjectName("edit")
        self.text21.setPlaceholderText('Excerpts')
        ex1 = QWidget()
        self.btnoldexcerpt = QPushButton('', self)
        self.btnoldexcerpt.clicked.connect(self.show_list_excerpt)
        self.btnoldexcerpt.setFixedSize(20, 20)
        self.btnoldexcerpt.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/grid.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_2k1 = QPushButton('Add', self)
        self.btn_2k1.clicked.connect(self.addexc)
        self.btn_2k1.setMaximumHeight(20)
        btn_211 = QPushButton('Clear', self)
        btn_211.clicked.connect(self.clearexc)
        btn_211.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
        ec1.addWidget(self.btnoldexcerpt)
        ec1.addWidget(self.btn_2k1)
        ec1.addWidget(btn_211)
        ex1.setLayout(ec1)

        self.text22 = QPlainTextEdit(self)
        self.text22.setReadOnly(False)
        self.text22.setObjectName("edit")
        self.text22.setPlaceholderText('My views')
        ex2 = QWidget()
        btn_22 = QPushButton('Add and clear', self)
        btn_22.clicked.connect(self.addmv)
        btn_22.setMaximumHeight(20)
        btn_22.setShortcut("Ctrl+Return")
        '''btn_221 = QPushButton('Clear', self)
        btn_221.clicked.connect(self.clearmv)
        btn_221.setMaximumHeight(20)'''
        ec2 = QHBoxLayout()
        ec2.setContentsMargins(0, 0, 0, 0)
        ec2.addWidget(btn_22)
        # ec2.addWidget(btn_221)
        ex2.setLayout(ec2)

        page4_box_h = QVBoxLayout()
        page4_box_h.addWidget(top_box)
        page4_box_h.addWidget(self.text21)
        page4_box_h.addWidget(ex1)
        page4_box_h.addWidget(self.text22)
        page4_box_h.addWidget(ex2)
        self.two_tab.setLayout(page4_box_h)

    def show_list_excerpt(self):
        warn = CustomDialog_list_excerpt()
        warn.exec()

    def concep(self):
        self.lec1 = QLineEdit(self)
        self.lec1.setPlaceholderText('Name of the concept')
        ex1 = QWidget()
        self.btnoldconcept = QPushButton('', self)
        self.btnoldconcept.clicked.connect(self.show_list_con)
        self.btnoldconcept.setFixedSize(20, 20)
        self.btnoldconcept.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/grid.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_ce31 = QPushButton('Add', self)
        self.btn_ce31.clicked.connect(self.addcon)
        self.btn_ce31.setMaximumHeight(20)
        btn_311 = QPushButton('Clear', self)
        btn_311.clicked.connect(self.clearnam)
        btn_311.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
        ec1.addWidget(self.btnoldconcept)
        ec1.addWidget(self.btn_ce31)
        ec1.addWidget(btn_311)
        ex1.setLayout(ec1)

        self.lec2 = QLineEdit(self)
        self.lec2.setPlaceholderText('Perspective')
        ex2 = QWidget()
        self.btn_ce32 = QPushButton('Add', self)
        self.btn_ce32.clicked.connect(self.addpers)
        self.btn_ce32.setMaximumHeight(20)
        btn_321 = QPushButton('Clear', self)
        btn_321.clicked.connect(self.cleanpers)
        btn_321.setMaximumHeight(20)
        ec2 = QHBoxLayout()
        ec2.setContentsMargins(0, 0, 0, 0)
        ec2.addWidget(self.btn_ce32)
        ec2.addWidget(btn_321)
        ex2.setLayout(ec2)

        self.text31 = QPlainTextEdit(self)
        self.text31.setReadOnly(False)
        self.text31.setObjectName("edit")
        self.text31.setPlaceholderText('Explanations')
        ex3 = QWidget()
        btn_33 = QPushButton('Add and clear', self)
        btn_33.clicked.connect(self.addconexp)
        btn_33.setMaximumHeight(20)
        btn_33.setShortcut("Ctrl+Return")
        '''btn_331 = QPushButton('Clear', self)
        btn_331.clicked.connect(self.clearconex)
        btn_331.setMaximumHeight(20)'''
        ec3 = QHBoxLayout()
        ec3.setContentsMargins(0, 0, 0, 0)
        ec3.addWidget(btn_33)
        # ec3.addWidget(btn_331)
        ex3.setLayout(ec3)

        df_box = QVBoxLayout()
        df_box.addWidget(self.lec1)
        df_box.addWidget(ex1)
        df_box.addWidget(self.lec2)
        df_box.addWidget(ex2)
        df_box.addWidget(self.text31)
        df_box.addWidget(ex3)
        self.three_tab.setLayout(df_box)

    def show_list_con(self):
        warn = CustomDialog_list_con()
        warn.exec()

    def cite2(self):
        warn = CustomDialog_list_cite2()
        warn.exec()

    def theors(self):
        self.lec0 = QLineEdit(self)
        self.lec0.setPlaceholderText('Name of the theory')
        ex0 = QWidget()
        self.btnoldtheory = QPushButton('', self)
        self.btnoldtheory.clicked.connect(self.show_list_the)
        self.btnoldtheory.setFixedSize(20, 20)
        self.btnoldtheory.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/grid.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_the30 = QPushButton('Add', self)
        self.btn_the30.clicked.connect(self.addthero)
        self.btn_the30.setMaximumHeight(20)
        btn_300 = QPushButton('Clear', self)
        btn_300.clicked.connect(self.clthen)
        btn_300.setMaximumHeight(20)
        ec0 = QHBoxLayout()
        ec0.setContentsMargins(0, 0, 0, 0)
        ec0.addWidget(self.btnoldtheory)
        ec0.addWidget(self.btn_the30)
        ec0.addWidget(btn_300)
        ex0.setLayout(ec0)

        tt1 = QWidget()
        self.text41 = QPlainTextEdit(self)
        self.text41.setReadOnly(False)
        self.text41.setObjectName("edit")
        self.text41.setPlaceholderText('Question preferences')
        ex1 = QWidget()
        self.btn_the41 = QPushButton('+', self)
        self.btn_the41.clicked.connect(self.addpoprefe)
        self.btn_the41.setMaximumHeight(20)
        self.btn_the41.setMinimumHeight(20)
        self.btn_the41.setMinimumWidth(20)
        btn_411 = QPushButton('-', self)
        btn_411.clicked.connect(self.clearpropref)
        btn_411.setMaximumHeight(20)
        btn_411.setMinimumHeight(20)
        btn_411.setMinimumWidth(20)
        ec1 = QVBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
        ec1.addWidget(self.btn_the41)
        ec1.addWidget(btn_411)
        ex1.setLayout(ec1)
        btt1 = QHBoxLayout()
        btt1.setContentsMargins(0, 0, 0, 0)
        btt1.addWidget(self.text41)
        btt1.addWidget(ex1)
        tt1.setLayout(btt1)

        tt2 = QWidget()
        self.text42 = QPlainTextEdit(self)
        self.text42.setReadOnly(False)
        self.text42.setObjectName("edit")
        self.text42.setPlaceholderText('Method preferences')
        ex2 = QWidget()
        self.btn_the42 = QPushButton('+', self)
        self.btn_the42.clicked.connect(self.addmetpref)
        self.btn_the42.setMaximumHeight(20)
        self.btn_the42.setMinimumHeight(20)
        self.btn_the42.setMinimumWidth(20)
        btn_421 = QPushButton('-', self)
        btn_421.clicked.connect(self.clearmedpref)
        btn_421.setMaximumHeight(20)
        btn_421.setMinimumHeight(20)
        btn_421.setMinimumWidth(20)
        ec2 = QVBoxLayout()
        ec2.setContentsMargins(0, 0, 0, 0)
        ec2.addWidget(self.btn_the42)
        ec2.addWidget(btn_421)
        ex2.setLayout(ec2)
        btt2 = QHBoxLayout()
        btt2.setContentsMargins(0, 0, 0, 0)
        btt2.addWidget(self.text42)
        btt2.addWidget(ex2)
        tt2.setLayout(btt2)

        tt3 = QWidget()
        self.text43 = QPlainTextEdit(self)
        self.text43.setReadOnly(False)
        self.text43.setObjectName("edit")
        self.text43.setPlaceholderText('Thinking patterns')
        ex3 = QWidget()
        self.btn_the43 = QPushButton('+', self)
        self.btn_the43.clicked.connect(self.thnpatt)
        self.btn_the43.setMaximumHeight(20)
        self.btn_the43.setMinimumHeight(20)
        self.btn_the43.setMinimumWidth(20)
        btn_431 = QPushButton('-', self)
        btn_431.clicked.connect(self.clearthnptn)
        btn_431.setMaximumHeight(20)
        btn_431.setMinimumHeight(20)
        btn_431.setMinimumWidth(20)
        ec3 = QVBoxLayout()
        ec3.setContentsMargins(0, 0, 0, 0)
        ec3.addWidget(self.btn_the43)
        ec3.addWidget(btn_431)
        ex3.setLayout(ec3)
        btt3 = QHBoxLayout()
        btt3.setContentsMargins(0, 0, 0, 0)
        btt3.addWidget(self.text43)
        btt3.addWidget(ex3)
        tt3.setLayout(btt3)

        tt4 = QWidget()
        self.text44 = QPlainTextEdit(self)
        self.text44.setReadOnly(False)
        self.text44.setObjectName("edit")
        self.text44.setPlaceholderText('Basic views')
        ex4 = QWidget()
        self.btn_the44 = QPushButton('+', self)
        self.btn_the44.clicked.connect(self.thnbasv)
        self.btn_the44.setMaximumHeight(20)
        self.btn_the44.setMinimumHeight(20)
        self.btn_the44.setMinimumWidth(20)
        btn_441 = QPushButton('-', self)
        btn_441.clicked.connect(self.clearbscpv)
        btn_441.setMaximumHeight(20)
        btn_441.setMinimumHeight(20)
        btn_441.setMinimumWidth(20)
        ec4 = QVBoxLayout()
        ec4.setContentsMargins(0, 0, 0, 0)
        ec4.addWidget(self.btn_the44)
        ec4.addWidget(btn_441)
        ex4.setLayout(ec4)
        btt4 = QHBoxLayout()
        btt4.setContentsMargins(0, 0, 0, 0)
        btt4.addWidget(self.text44)
        btt4.addWidget(ex4)
        tt4.setLayout(btt4)

        tt5 = QWidget()
        self.text45 = QPlainTextEdit(self)
        self.text45.setReadOnly(False)
        self.text45.setObjectName("edit")
        self.text45.setPlaceholderText('Empirical examples')
        ex5 = QWidget()
        self.btn_the45 = QPushButton('+', self)
        self.btn_the45.clicked.connect(self.emexpls)
        self.btn_the45.setMaximumHeight(20)
        self.btn_the45.setMinimumHeight(20)
        self.btn_the45.setMinimumWidth(20)
        btn_451 = QPushButton('-', self)
        btn_451.clicked.connect(self.clearemepls)
        btn_451.setMaximumHeight(20)
        btn_451.setMinimumHeight(20)
        btn_451.setMinimumWidth(20)
        ec5 = QVBoxLayout()
        ec5.setContentsMargins(0, 0, 0, 0)
        ec5.addWidget(self.btn_the45)
        ec5.addWidget(btn_451)
        ex5.setLayout(ec5)
        btt5 = QHBoxLayout()
        btt5.setContentsMargins(0, 0, 0, 0)
        btt5.addWidget(self.text45)
        btt5.addWidget(ex5)
        tt5.setLayout(btt5)

        tt6 = QWidget()
        self.text46 = QPlainTextEdit(self)
        self.text46.setReadOnly(False)
        self.text46.setObjectName("edit")
        self.text46.setPlaceholderText('Review: pros and cons')
        ex6 = QWidget()
        self.btn_the46 = QPushButton('+', self)
        self.btn_the46.clicked.connect(self.addreviwcmts)
        self.btn_the46.setMaximumHeight(20)
        self.btn_the46.setMinimumHeight(20)
        self.btn_the46.setMinimumWidth(20)
        btn_461 = QPushButton('-', self)
        btn_461.clicked.connect(self.clearecmt)
        btn_461.setMaximumHeight(20)
        btn_461.setMinimumHeight(20)
        btn_461.setMinimumWidth(20)
        ec6 = QVBoxLayout()
        ec6.setContentsMargins(0, 0, 0, 0)
        ec6.addWidget(self.btn_the46)
        ec6.addWidget(btn_461)
        ex6.setLayout(ec6)
        btt6 = QHBoxLayout()
        btt6.setContentsMargins(0, 0, 0, 0)
        btt6.addWidget(self.text46)
        btt6.addWidget(ex6)
        tt6.setLayout(btt6)

        tt7 = QWidget()
        self.text47 = QPlainTextEdit(self)
        self.text47.setReadOnly(False)
        self.text47.setObjectName("edit")
        self.text47.setPlaceholderText('Evolution and trends')
        ex7 = QWidget()
        self.btn_the47 = QPushButton('+', self)
        self.btn_the47.clicked.connect(self.addevotr)
        self.btn_the47.setMaximumHeight(20)
        self.btn_the47.setMinimumHeight(20)
        self.btn_the47.setMinimumWidth(20)
        btn_471 = QPushButton('-', self)
        btn_471.clicked.connect(self.clearevotr)
        btn_471.setMaximumHeight(20)
        btn_471.setMinimumHeight(20)
        btn_471.setMinimumWidth(20)
        ec7 = QVBoxLayout()
        ec7.setContentsMargins(0, 0, 0, 0)
        ec7.addWidget(self.btn_the47)
        ec7.addWidget(btn_471)
        ex7.setLayout(ec7)
        btt7 = QHBoxLayout()
        btt7.setContentsMargins(0, 0, 0, 0)
        btt7.addWidget(self.text47)
        btt7.addWidget(ex7)
        tt7.setLayout(btt7)

        df_box = QVBoxLayout()
        df_box.addWidget(self.lec0)
        df_box.addWidget(ex0)
        # df_box.addWidget(self.text41)
        df_box.addWidget(tt1)
        # df_box.addWidget(self.text42)
        df_box.addWidget(tt2)
        # df_box.addWidget(self.text43)
        df_box.addWidget(tt3)
        # df_box.addWidget(self.text44)
        df_box.addWidget(tt4)
        # df_box.addWidget(self.text45)
        df_box.addWidget(tt5)
        # df_box.addWidget(self.text46)
        df_box.addWidget(tt6)
        # df_box.addWidget(self.text47)
        df_box.addWidget(tt7)
        self.four_tab.setLayout(df_box)

    def show_list_the(self):
        warn = CustomDialog_list_the()
        warn.exec()

    def cite3(self):
        warn = CustomDialog_list_cite3()
        warn.exec()

    def meths(self):
        self.lem1 = QLineEdit(self)
        self.lem1.setPlaceholderText('Name of the method')
        ex1 = QWidget()
        self.btnoldmethod = QPushButton('', self)
        self.btnoldmethod.clicked.connect(self.show_list_met)
        self.btnoldmethod.setFixedSize(20, 20)
        self.btnoldmethod.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/grid.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        self.btn_51 = QPushButton('Add', self)
        self.btn_51.clicked.connect(self.addmetds)
        self.btn_51.setMaximumHeight(20)
        btn_511 = QPushButton('Clear', self)
        btn_511.clicked.connect(self.clearmetnm)
        btn_511.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
        ec1.addWidget(self.btnoldmethod)
        ec1.addWidget(self.btn_51)
        ec1.addWidget(btn_511)
        ex1.setLayout(ec1)

        self.lem2 = QLineEdit(self)
        self.lem2.setPlaceholderText('Needs to be met')
        ex2 = QWidget()
        self.btn_52 = QPushButton('Add', self)
        self.btn_52.clicked.connect(self.addmetneeds)
        self.btn_52.setMaximumHeight(20)
        btn_521 = QPushButton('Clear', self)
        btn_521.clicked.connect(self.clearmetneeds)
        btn_521.setMaximumHeight(20)
        ec2 = QHBoxLayout()
        ec2.setContentsMargins(0, 0, 0, 0)
        ec2.addWidget(self.btn_52)
        ec2.addWidget(btn_521)
        ex2.setLayout(ec2)

        self.text51 = QPlainTextEdit(self)
        self.text51.setReadOnly(False)
        self.text51.setObjectName("edit")
        self.text51.setPlaceholderText('Explanations')
        ex3 = QWidget()
        btn_53 = QPushButton('Add and clear', self)
        btn_53.clicked.connect(self.addmetdets)
        btn_53.setMaximumHeight(20)
        btn_53.setShortcut("Ctrl+Return")
        '''btn_531 = QPushButton('Clear', self)
        # btn_211.clicked.connect(self.clearexc)
        btn_531.setMaximumHeight(20)'''
        ec3 = QHBoxLayout()
        ec3.setContentsMargins(0, 0, 0, 0)
        ec3.addWidget(btn_53)
        # ec3.addWidget(btn_531)
        ex3.setLayout(ec3)

        df_box = QVBoxLayout()
        df_box.addWidget(self.lem1)
        df_box.addWidget(ex1)
        df_box.addWidget(self.lem2)
        df_box.addWidget(ex2)
        df_box.addWidget(self.text51)
        df_box.addWidget(ex3)
        self.five_tab.setLayout(df_box)

    def show_list_met(self):
        warn = CustomDialog_list_met()
        warn.exec()

    def cite4(self):
        warn = CustomDialog_list_cite4()
        warn.exec()

    def toolkit(self):
        lbl0 = QLabel('1. Find and replacement', self)
        font = PyQt6.QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(15)
        lbl0.setFont(font)

        t1 = QWidget()
        lbl1 = QLabel('Use:', self)
        self.tool1 = QLineEdit(self)
        self.tool1.setPlaceholderText('Enter your text')
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(lbl1)
        b1.addWidget(self.tool1)
        t1.setLayout(b1)

        t1_5 = QWidget()
        lbl1_5 = QLabel('To replece:', self)
        self.tool1_5 = QLineEdit(self)
        self.tool1_5.setPlaceholderText('Enter your text')
        b1_5 = QHBoxLayout()
        b1_5.setContentsMargins(0, 0, 0, 0)
        b1_5.addWidget(lbl1_5)
        b1_5.addWidget(self.tool1_5)
        t1_5.setLayout(b1_5)

        t1_6 = QWidget()
        btn_t1 = QPushButton('Start!', self)
        btn_t1.clicked.connect(self.fanrep)
        btn_t1.setMaximumHeight(20)
        btn_t1.setMinimumWidth(50)
        btn_t0 = QPushButton('Not in this article?', self)
        btn_t0.clicked.connect(self.findandrepopen)
        btn_t0.setMaximumHeight(20)
        btn_t0.setMinimumWidth(50)
        b1_6 = QHBoxLayout()
        b1_6.setContentsMargins(0, 0, 0, 0)
        b1_6.addWidget(btn_t1)
        b1_6.addWidget(btn_t0)
        t1_6.setLayout(b1_6)

        lbl02 = QLabel('2. Redirect a word', self)
        lbl02.setFont(font)

        t2 = QWidget()
        lbl2 = QLabel('Redirect:', self)
        self.tool2 = QLineEdit(self)
        self.tool2.setPlaceholderText('Enter your text')
        b2 = QHBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addWidget(lbl2)
        b2.addWidget(self.tool2)
        t2.setLayout(b2)

        t3 = QWidget()
        lbl3 = QLabel('To:', self)
        self.tool3 = QLineEdit(self)
        self.tool3.setPlaceholderText('Enter your text')
        b3 = QHBoxLayout()
        b3.setContentsMargins(0, 0, 0, 0)
        b3.addWidget(lbl3)
        b3.addWidget(self.tool3)
        t3.setLayout(b3)

        t3_5 = QWidget()
        btn_t2 = QPushButton('Redirect!', self)
        btn_t2.clicked.connect(self.redirtname)
        btn_t2.setMaximumHeight(20)
        btn_t2.setMinimumWidth(50)
        btn_tq = QPushButton('Not in this article?', self)
        btn_tq.clicked.connect(self.anotred)
        btn_tq.setMaximumHeight(20)
        btn_tq.setMinimumWidth(50)
        b3_5 = QHBoxLayout()
        b3_5.setContentsMargins(0, 0, 0, 0)
        b3_5.addWidget(btn_t2)
        b3_5.addWidget(btn_tq)
        t3_5.setLayout(b3_5)

        lbl03 = QLabel('3. Article bionic reading', self)
        lbl03.setFont(font)

        t4 = QWidget()
        btn_t3 = QPushButton('On!', self)
        btn_t3.clicked.connect(self.bioarton)
        btn_t3.setMaximumHeight(20)
        btn_t3.setMinimumWidth(50)
        btn_t4 = QPushButton('Off!', self)
        btn_t4.clicked.connect(self.bioartoff)
        btn_t4.setMaximumHeight(20)
        btn_t4.setMinimumWidth(50)
        b4 = QHBoxLayout()
        b4.setContentsMargins(0, 0, 0, 0)
        b4.addWidget(btn_t3)
        b4.addWidget(btn_t4)
        t4.setLayout(b4)

        t5 = QWidget()
        btn_t30 = QPushButton('Another article on', self)
        btn_t30.clicked.connect(self.anobioon)
        btn_t30.setMaximumHeight(20)
        btn_t30.setMinimumWidth(50)
        btn_t39 = QPushButton('Another article off', self)
        btn_t39.clicked.connect(self.anobiooff)
        btn_t39.setMaximumHeight(20)
        btn_t39.setMinimumWidth(50)
        b5 = QHBoxLayout()
        b5.setContentsMargins(0, 0, 0, 0)
        b5.addWidget(btn_t30)
        b5.addWidget(btn_t39)
        t5.setLayout(b5)

        lbl04 = QLabel('4. Extract my views', self)
        lbl04.setFont(font)

        t6 = QWidget()
        self.btn_t5 = QPushButton('From', self)
        self.btn_t5.clicked.connect(self.from_ext)
        self.btn_t5.setMaximumHeight(20)
        self.btn_t5.setMinimumWidth(50)
        self.btn_t6 = QPushButton('To', self)
        self.btn_t6.clicked.connect(self.to_ext)
        self.btn_t6.setMaximumHeight(20)
        self.btn_t6.setMinimumWidth(50)
        b6 = QHBoxLayout()
        b6.setContentsMargins(0, 0, 0, 0)
        b6.addWidget(self.btn_t5)
        b6.addWidget(self.btn_t6)
        t6.setLayout(b6)

        btn_t7 = QPushButton('Start!', self)
        btn_t7.clicked.connect(self.start_ext)
        btn_t7.setMaximumHeight(20)
        btn_t7.setMinimumWidth(50)

        lbl05 = QLabel('5. Import citations from RIS files', self)
        lbl05.setFont(font)

        t7 = QWidget()
        self.btn_t7 = QPushButton('Open .ris and start!', self)
        self.btn_t7.clicked.connect(self.openris)
        self.btn_t7.setMaximumHeight(20)
        self.btn_t7.setMinimumWidth(50)
        self.btn_t8 = QPushButton('Move to Articles', self)
        self.btn_t8.clicked.connect(self.moveris)
        self.btn_t8.setMaximumHeight(20)
        self.btn_t8.setMinimumWidth(50)
        b7 = QHBoxLayout()
        b7.setContentsMargins(0, 0, 0, 0)
        b7.addWidget(self.btn_t7)
        b7.addWidget(self.btn_t8)
        t7.setLayout(b7)

        self.lbltool06 = QLabel('6. Web & Conference Mode', self)
        self.lbltool06.setFont(font)

        self.tool8 = QWidget()
        self.btn_t9 = QPushButton('Turn on!', self)
        self.btn_t9.clicked.connect(self.webconmode_on)
        self.btn_t9.setMaximumHeight(20)
        self.btn_t9.setMinimumWidth(50)
        self.btn_t10 = QPushButton('Turn off!', self)
        self.btn_t10.clicked.connect(self.webconmode_off)
        self.btn_t10.setMaximumHeight(20)
        self.btn_t10.setMinimumWidth(50)
        b8 = QHBoxLayout()
        b8.setContentsMargins(0, 0, 0, 0)
        b8.addWidget(self.btn_t9)
        b8.addWidget(self.btn_t10)
        self.tool8.setLayout(b8)

        df_box = QVBoxLayout()
        df_box.addStretch()
        df_box.addWidget(lbl0)
        # df_box.addWidget(btn_t0)
        df_box.addWidget(t1)
        df_box.addWidget(t1_5)
        df_box.addWidget(t1_6)
        df_box.addStretch()
        df_box.addWidget(lbl02)
        # df_box.addWidget(btn_tq)
        df_box.addWidget(t2)
        df_box.addWidget(t3)
        df_box.addWidget(t3_5)
        df_box.addStretch()
        df_box.addWidget(lbl03)
        # df_box.addWidget(btn_t30)
        df_box.addWidget(t4)
        df_box.addWidget(t5)
        df_box.addStretch()
        df_box.addWidget(lbl04)
        df_box.addWidget(t6)
        df_box.addWidget(btn_t7)
        df_box.addStretch()
        df_box.addWidget(lbl05)
        df_box.addWidget(t7)
        df_box.addStretch()
        df_box.addWidget(self.lbltool06)
        df_box.addWidget(self.tool8)
        df_box.addStretch()
        self.six_tab.setLayout(df_box)

    def openextis(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text.setPlainText('Please check your path settings!')
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path1, "Markdown Files (*.md)")
            if file_name != '':
                reset_newarchive_path()
                if path1 in file_name:
                    contend = codecs.open(file_name, 'r', encoding='utf-8').read()

                    pattern = re.compile(r'Title: (.*?)\n')
                    result = pattern.findall(contend)
                    result = ''.join(result)
                    pretc = result.replace('Title: ', '')
                    pretc = pretc.replace('\n', '')
                    pretc = pretc.replace('[', '')
                    pretc = pretc.replace(']', '')
                    if '|' in pretc:
                        pass
                        patt = re.compile(r'\|(.*?)\]')
                        res2 = patt.findall(result)
                        res2 = ''.join(res2)
                        self.le1.setText(res2)
                    else:
                        self.le1.setText(pretc)

                    pattern2 = re.compile(r'Authors: (.*?)\n')
                    result2 = pattern2.findall(contend)
                    result2 = ''.join(result2)
                    pretc2 = result2.replace('Authors: ', '')
                    pretc2 = pretc2.replace('\n', '')
                    pretc2 = pretc2.replace('[', '')
                    pretc2 = pretc2.replace(']', '')
                    self.le2.setText(pretc2)

                    pattern3 = re.compile(r'Institutes: (.*?)\n')
                    result3 = pattern3.findall(contend)
                    result3 = ''.join(result3)
                    pretc3 = result3.replace('Institutes: ', '')
                    pretc3 = pretc3.replace('\n', '')
                    pretc3 = pretc3.replace('[', '')
                    pretc3 = pretc3.replace(']', '')
                    self.le7.setText(pretc3)

                    pattern4 = re.compile(r'Publication: (.*?)\n')
                    result4 = pattern4.findall(contend)
                    result4 = ''.join(result4)
                    pretc4 = result4.replace('Publication: ', '')
                    pretc4 = pretc4.replace('\n', '')
                    pretc4 = pretc4.replace('[', '')
                    pretc4 = pretc4.replace(']', '')
                    self.le3.setText(pretc4)

                    pattern5 = re.compile(r'Press: (.*?)\n')
                    result5 = pattern5.findall(contend)
                    result5 = ''.join(result5)
                    pretc5 = result5.replace('Press: ', '')
                    pretc5 = pretc5.replace('\n', '')
                    pretc5 = pretc5.replace('[', '')
                    pretc5 = pretc5.replace(']', '')
                    self.le3_1.setText(pretc5)

                    pattern6 = re.compile(r'Year: (.*?)\n')
                    result6 = pattern6.findall(contend)
                    result6 = ''.join(result6)
                    pretc6 = result6.replace('Year: ', '')
                    pretc6 = pretc6.replace('\n', '')
                    pretc6 = pretc6.replace('#AD', '')
                    self.le4.setText(pretc6)

                    pattern7 = re.compile(r'Vol / Mon: (.*?)\n')
                    result7 = pattern7.findall(contend)
                    result7 = ''.join(result7)
                    pretc7 = result7.replace('Vol / Mon: ', '')
                    pretc7 = pretc7.replace('\n', '')
                    self.le4_1.setText(pretc7)

                    pattern7_1 = re.compile(r'DOI: (.*?)\n')
                    result7_1 = pattern7_1.findall(contend)
                    result7_1 = ''.join(result7_1)
                    pretc7_1 = result7_1.replace('DOI: ', '')
                    pretc7_1 = pretc7_1.replace('\n', '')
                    pretc7_1 = pretc7_1.replace('[', '')
                    pretc7_1 = pretc7_1.replace(']', '')
                    self.le_doi.setText(pretc7_1)

                    pattern7_2 = re.compile(r'ISBN: (.*?)\n')
                    result7_2 = pattern7_2.findall(contend)
                    result7_2 = ''.join(result7_2)
                    pretc7_2 = result7_2.replace('ISBN: ', '')
                    pretc7_2 = pretc7_2.replace('\n', '')
                    pretc7_2 = pretc7_2.replace('[', '')
                    pretc7_2 = pretc7_2.replace(']', '')
                    self.le_isbn.setText(pretc7_2)

                    pattern8 = re.compile(r'Tags: (.*?)\n')
                    result8 = pattern8.findall(contend)
                    result8 = ''.join(result8)
                    pretc8 = result8.replace('Tags: ', '')
                    pretc8 = pretc8.replace('\n', '')
                    pretc8 = pretc8.replace('#', '')
                    pretc8 = pretc8.replace(' ', '、')
                    pretc8 = pretc8.replace('[', '')
                    pretc8 = pretc8.replace(']', '')
                    self.le5.setText(pretc8)

                    pattern9 = re.compile(r'From book: (.*?),')
                    result9 = pattern9.findall(contend)
                    result9 = ''.join(result9)
                    pretc9 = result9.replace('From book: ', '')
                    pretc9 = pretc9.replace(',', '')
                    pretc9 = pretc9.replace('[', '')
                    pretc9 = pretc9.replace(']', '')
                    self.le8.setText(pretc9)

                    pattern10 = re.compile(r', Chapter (.*?),')
                    result10 = pattern10.findall(contend)
                    result10 = ''.join(result10)
                    pretc10 = result10.replace(', Chapter ', '')
                    pretc10 = pretc10.replace(',', '')
                    pretc10 = pretc10.replace('[', '')
                    pretc10 = pretc10.replace(']', '')
                    self.le9.setText(pretc10)

                    pattern11 = re.compile(r', Page range: (.*?)\n')
                    result11 = pattern11.findall(contend)
                    result11 = ''.join(result11)
                    pretc11 = result11.replace(', Page range: ', '')
                    pretc11 = pretc11.replace('\n', '')
                    self.le10.setText(pretc11)

                    if self.le1.text() != '':
                        self.text.setPlainText(contend)
                        self.le1.setEnabled(False)
                        self.btnmain2.setStyleSheet('''
                                border: 1px outset grey;
                                background-color: #0085FF;
                                border-radius: 4px;
                                padding: 1px;
                                color: #FFFFFF''')
                        self.btnmain2.setText('Added')

                        self.widget0.clear()
                        self.widget0.addItems(['Append at the end (default)', 'Append at the current cursor'])
                        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
                        tarname1 = str(self.le1.text()) + ".md"
                        fulldir1 = os.path.join(path1, tarname1)
                        maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                        pattern = re.compile(r'## (.*?)\n')
                        result = pattern.findall(maintxt)
                        if result != []:
                            result = '☆'.join(result)
                            result = result.replace('#', '')
                            result = result.replace('# ', '')
                            result = result.replace('Q/P: ', '')
                            result = result.split('☆')
                            for i in range(len(result)):
                                result[i] = 'After ' + result[i]
                                result[i] = ''.join(result[i])
                            self.widget0.addItems(result)

                        with open(BasePath + 'path_ttl.txt', 'w', encoding='utf-8') as f0:
                            f0.write(pretc)

                    self.read_t1.setVisible(False)
                    self.read_t2.setVisible(False)
                    self.read_t7.setVisible(False)
                    self.read_t3.setVisible(False)
                    self.read_t8.setVisible(False)
                    self.read_t4.setVisible(False)
                    self.read_t4_doi.setVisible(False)
                    self.read_t4_isbn.setVisible(False)
                    self.read_t5.setVisible(False)
                    self.lbltool06.setVisible(False)
                    self.tool8.setVisible(False)
                    self.btnx4.setStyleSheet('''
                        QPushButton{
                        border: transparent;
                        background-color: transparent;
                        border-image: url(/Applications/Strawberry.app/Contents/Resources/down.png);
                        }
                        QPushButton:pressed{
                        border: 1px outset grey;
                        background-color: #0085FF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #FFFFFF
                        }
                        ''')
                    if self.btn_t9.text() == 'Turned on!':
                        self.web_t3.setVisible(False)
                        self.web_t8.setVisible(False)

                    if self.le1.text() == '':
                        self.text.setPlainText('It is not a standard file for article.')
                if path1 not in file_name:
                    self.text.setPlainText('This file is not under the target folder.')

    def cleaninput(self, a):
        a = a.replace('\n', ' ')
        a = a.replace('\r', ' ')
        a = a.replace('/', ' ')
        a = a.replace(':', '').replace('：', ' ')
        a = a.replace('-', ' ')
        a = a.replace('[', '')
        a = a.replace(']', '')
        a = a.replace('   ', ' ')
        a = a.replace('  ', ' ')
        a = a.lstrip(' ').rstrip(' ')
        return a

    def addmain(self):
        if self.btnmain2.text() != 'Added' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                self.le1.setText(self.cleaninput(str(self.le1.text())))
                self.le2.setText(self.cleaninput(str(self.le2.text())))
                self.le7.setText(self.cleaninput(str(self.le7.text())))
                self.le3.setText(self.cleaninput(str(self.le3.text())))
                self.le3_1.setText(self.cleaninput(str(self.le3_1.text())))
                self.le4.setText(self.cleaninput(str(self.le4.text())))
                self.le4_1.setText(self.cleaninput(str(self.le4_1.text())))
                self.le_doi.setText(str(self.le_doi.text()).strip())
                self.le_isbn.setText(str(self.le_isbn.text()).strip())
                self.le5.setText(self.cleaninput(str(self.le5.text())))
                self.le8.setText(self.cleaninput(str(self.le8.text())))
                self.le9.setText(self.cleaninput(str(self.le9.text())))
                #self.le10.setText(self.cleaninput(str(self.le10.text())))

                tarname1 = str(self.le1.text())+".md"
                fulldir1 = os.path.join(path1, tarname1)
                part1 = '# Metadata'
                part2 = '\n- ' + 'Title: ' + str(self.le1.text())
                part3 = ''
                if '%' not in self.le2.text():
                    part3 = '\n- ' + 'Authors: ' + str(self.le2.text())
                if '%' in self.le2.text():
                    p3end = str(self.le2.text()).replace('%', '(translator)')
                    part3 = '\n- ' + 'Authors: ' + p3end

                part4 = ''
                if self.le7.text() != '':
                    part4 = '\n- ' + 'Institutes: ' + str(self.le7.text())

                part5 = ''
                if self.le3.text() != '':
                    part5 = '\n- ' + 'Publication: ' + str(self.le3.text())

                part5_1 = ''
                if self.le3_1.text() != '':
                    part5_1 = '\n- ' + 'Press: ' + str(self.le3_1.text())

                part5_5 = ''
                if not self.web_t3.isVisible():
                    if str(self.le8.text()) == '' or str(self.le9.text()) == '':
                        part5_5 = '\n- ' + 'Page range: ' + str(self.le10.text())
                    if str(self.le8.text()) != '' and str(self.le9.text()) != '' and self.le10.text() != '':
                        part5_5 = '\n- ' + 'From book: ' + str(self.le8.text()) + ', Chapter ' + str(
                            self.le9.text()) + ', Page range: ' + str(self.le10.text())

                part6 = '\n- ' + 'Year: ' + '#AD' + str(self.le4.text())
                part6_5 = ''
                if self.le4_1.text() != '':
                    part6_5 = '\n- ' + 'Vol / Mon: ' + str(self.le4_1.text())

                part6_6 = ''
                if self.le_doi.text() != '':
                    part6_6 = '\n- ' + 'DOI: ' + str(self.le_doi.text())

                part6_7 = ''
                if self.le_isbn.text() != '':
                    part6_7 = '\n- ' + 'ISBN: ' + str(self.le_isbn.text())

                part7 = ''
                if self.le5.text() != '':
                    exptag = str(self.le5.text()).replace('+', '、')
                    listtag = exptag.split('、')
                    i = 0
                    while i >= 0 and i <= len(listtag) - 1:
                        listtag[i] = '#' + str(listtag[i]) + ' '
                        listtag[i] = ''.join(listtag[i])
                        i += 1
                        continue
                    endtag = ''.join(listtag)
                    part7 = '\n- ' + 'Tags: ' + str(endtag)

                part7_5 = ''
                def is_contain_english(str0):  # 判断是否包含英文字母
                    import re
                    return bool(re.search('[a-zA-Zａ-ｚＡ-Ｚ]', str0))

                def is_contain_chinese(check_str):  # 判断是否包含中文字
                    for ch in check_str:
                        if u'\u4e00' <= ch <= u'\u9fff':
                            return True
                    return False

                if is_contain_chinese(str(self.le1.text())) or is_contain_chinese(str(self.le3.text())) or is_contain_chinese(str(self.le8.text())):
                    if not self.web_t3.isVisible():
                        if '%' not in self.le2.text():
                            if self.le3.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()) + '：《' + str(self.le1.text()) + '》，载《' + \
                                    str(self.le3.text()) + '》，' + str(self.le4.text()) + ' 年第 ' + \
                                    str(self.le4_1.text()) + ' 期，第 ' + str(self.le10.text()) + ' 页。'
                            if self.le3.text() == '' and self.le8.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()) + '：《' + \
                                    str(self.le8.text()) + '》，' + str(self.le3_1.text()) + '，' + str(self.le4.text()) + ' 年 ' + \
                                    str(self.le4_1.text()) + ' 月版，第 ' + str(self.le10.text()) + ' 页。'
                        if '%' in self.le2.text():
                            zove = str(self.le2.text()).replace('+', '、').split('、')
                            for i in range(len(zove)):
                                if '%' in zove[i]:
                                    zove[i] = zove[i].replace('%', '译')
                                    i = i + 1
                                    continue
                                if '%' not in zove[i]:
                                    zove[i] = zove[i] + '著'
                                    zove[i] = ''.join(zove[i])
                                    i = i + 1
                                    continue
                            zoveend = '，'.join(zove)
                            zoveend = zoveend.replace('译，', '、')
                            if self.le3.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + zoveend + '：《' + str(self.le1.text()) + '》，载《' + \
                                    str(self.le3.text()) + '》，' + str(self.le4.text()) + ' 年第 ' + \
                                    str(self.le4_1.text()) + ' 期，第 ' + str(self.le10.text()) + ' 页。'
                            if self.le3.text() == '' and self.le8.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + zoveend + '：《' + \
                                        str(self.le8.text()) + '》，' + str(self.le3_1.text()) + '，' + str(self.le4.text()) + ' 年 ' + \
                                        str(self.le4_1.text()) + ' 月版，第 ' + str(self.le10.text()) + ' 页。'
                    if self.web_t3.isVisible():
                        ISOTIMEFORMAT = '%Y 年 %m 月 %d 日'
                        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                        if '%' not in self.le2.text():
                            if self.leweb3.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()) + '：《' + str(
                                self.le1.text()) + '》，' + str(self.leweb3.text()) + '，访问时间：' + theTime + ' 。'
                            if self.leweb3.text() == '':
                                part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()) + '：《' + str(
                                    self.le1.text()) + '》，提交给“' + str(self.leweb8.text()) + '”的论文，' + str(self.leweb10.text()) + '，' + str(self.leweb9.text()) + '，' + str(self.le4.text()) + ' 年 ' + \
                                            str(self.le4_1.text()) + ' 月。'
                        if '%' in self.le2.text():
                            zove = str(self.le2.text()).replace('+', '、').split('、')
                            for i in range(len(zove)):
                                if '%' in zove[i]:
                                    zove[i] = zove[i].replace('%', '译')
                                    i = i + 1
                                    continue
                                if '%' not in zove[i]:
                                    zove[i] = zove[i] + '著'
                                    zove[i] = ''.join(zove[i])
                                    i = i + 1
                                    continue
                            zoveend = '，'.join(zove)
                            zoveend = zoveend.replace('译，', '、')
                            if self.leweb3.text() != '':
                                part7_5 = '\n- ' + 'Citation: ' + zoveend + '：《' + str(self.le1.text()) + '》，' + \
                                    str(self.leweb3.text()) + '，访问时间：' + theTime + ' 。'
                            if self.leweb3.text() == '':
                                part7_5 = '\n- ' + 'Citation: ' + zoveend + '：《' + str(
                                    self.le1.text()) + '》，提交给“' + str(self.leweb8.text()) + '”的论文，' + str(self.leweb10.text()) + '，' + str(self.leweb9.text()) + '，' + str(self.le4.text()) + ' 年 ' + \
                                            str(self.le4_1.text()) + ' 月。'
                if is_contain_english(str(self.le1.text())) and not is_contain_chinese(str(self.le1.text())):
                    if not self.web_t3.isVisible():
                        if self.le3.text() != '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('+', '、').replace('、', ', ') + ', “' + str(self.le1.text()) + ',” *' + \
                                str(self.le3.text()) + '*, ' + str(self.le4_1.text()) + ', ' + str(self.le4.text()) + ', pp.' + \
                                str(self.le10.text()) + '.'
                        if self.le3.text() == '' and self.le8.text() != '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('+', '、').replace('、', ', ') + ', ' + \
                                      str(self.le8.text()) + ', ' + str(self.le3_1.text()) + ', ' + str(self.le4.text()) + ', pp. ' + \
                                      str(self.le10.text()) + '.'
                    if self.web_t3.isVisible():
                        ISOTIMEFORMAT = '%B %d, %Y'
                        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                        if self.leweb3.text() != '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('+', '、').replace('、', ', ') + ', “' + str(self.le1.text()) + ',” retrieved ' + \
                            theTime + ', from ' + str(self.leweb3.text())
                        if self.leweb3.text() == '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('+', '、').replace('、', ', ') + ', “' + str(self.le1.text()) + ',” paper delivered to ' + \
                                str(self.leweb8.text()) + ', sponsored by ' + str(self.leweb9.text()) + ', ' + str(self.leweb10.text()) + ', ' + str(self.le4_1.text()) + ', ' + str(self.le4.text()) + '.'

                def _safe_num(val):
                    return str(val).strip() if str(val).strip() != '' else '000'

                def _safe_str(val):
                    return str(val).strip() if str(val).strip() != '' else 'UNKNOWN'

                def _clean_key(src):
                    key = re.sub('[^A-Za-z0-9]', '', str(src))
                    return key if key != '' else 'Unknown'

                def _build_citekey():
                    authors_raw = _safe_str(self.le2.text()).replace('+', '、').split('、')
                    first_author = authors_raw[0] if authors_raw else 'Unknown'
                    author_key = _clean_key(first_author.split(' ')[0])
                    year_key = _safe_num(self.le4.text())
                    title_key = _clean_key(self.le1.text())
                    return f"{author_key}{year_key}{title_key}"

                def _bibtex_article():
                    vol_val = _safe_str(self.le4_1.text())
                    num_val = _safe_num('000')
                    if '(' in vol_val or '（' in vol_val:
                        import re as _re
                        m = _re.search(r'[\(（](.*?)[\)）]', vol_val)
                        if m:
                            num_val = _safe_num(m.group(1))
                        vol_val = _re.sub(r'[\(（].*?[\)）]', '', vol_val).strip()
                    citekey = _build_citekey()
                    doi_val = _safe_str(self.le_doi.text())
                    journal = _safe_str(self.le3.text())
                    volume = _safe_num(vol_val)
                    number = num_val
                    pages = _safe_str(self.le10.text())
                    publisher = _safe_str(self.le3_1.text())
                    url_val = f"https://doi.org/{doi_val}" if doi_val != 'UNKNOWN' else _safe_str(self.leweb3.text())
                    return f'''@article{{{citekey},
  doi = "{doi_val}",
  title = "{_safe_str(self.le1.text())}",
  author = "{_safe_str(self.le2.text()).replace('、', ' and ')}",
  journal = "{journal}",
  year = {_safe_num(self.le4.text())},
  volume = {volume},
  number = {number},
  pages = "{pages}",
  publisher = "{publisher}",
  url = "{url_val}",
  type = "journal-article",
}}'''

                def _bibtex_misc():
                    citekey = _build_citekey()
                    today = datetime.datetime.now().strftime('%Y-%m-%d')
                    year_val = _safe_num(self.le4.text())
                    month_val = _safe_str(self.le4_1.text())
                    date_val = f"{year_val}-{month_val}" if month_val != 'UNKNOWN' else f"{year_val}-00-00"
                    howpublished = _safe_str(self.leweb8.text() if self.leweb8.text() != '' else self.le3.text())
                    url_val = _safe_str(self.leweb3.text())
                    return f'''@misc{{{citekey},
  author    = {{{_safe_str(self.le2.text()).replace('、', ' and ')}}},
  title     = {{{_safe_str(self.le1.text())}}},
  year      = {{{year_val}}},
  date      = {{{date_val}}},
  howpublished = {{{howpublished}}},
  url       = {{{url_val}}},
  urldate   = {{{today}}},
  language  = {{{_safe_str('en')}}}
}}'''

                def _bibtex_inproceedings():
                    vol_val = _safe_str(self.le4_1.text())
                    num_val = _safe_num('000')
                    if '(' in vol_val or '（' in vol_val:
                        import re as _re
                        m = _re.search(r'[\(（](.*?)[\)）]', vol_val)
                        if m:
                            num_val = _safe_num(m.group(1))
                        vol_val = _re.sub(r'[\(（].*?[\)）]', '', vol_val).strip()
                    citekey = _build_citekey()
                    booktitle = _safe_str(self.leweb8.text())
                    editor = _safe_str(self.leweb9.text())
                    volume = _safe_num(vol_val)
                    pages = _safe_str(self.le10.text())
                    publisher = _safe_str(self.le3_1.text())
                    address = _safe_str(self.leweb10.text())
                    doi_val = _safe_str(self.le_doi.text())
                    url_val = f"https://doi.org/{doi_val}" if doi_val != 'UNKNOWN' else _safe_str(self.leweb3.text())
                    return f'''@inproceedings{{{citekey},
  author    = {{{_safe_str(self.le2.text()).replace('、', ' and ')}}},
  title     = {{{_safe_str(self.le1.text())}}},
  booktitle = {{{booktitle}}},
  editor    = {{{editor}}},
  volume    = {{{volume}}},
  series    = {{{_safe_str('UNKNOWN')}}},
  pages     = {{{pages.replace('-', '--')}}},
  publisher = {{{publisher}}},
  address   = {{{address}}},
  year      = {{{_safe_num(self.le4.text())}}},
  month     = {{{_safe_str('UNKNOWN').lower()}}},
  doi       = {{{doi_val}}},
  url       = {{{url_val}}},
  language  = {{{_safe_str('en')}}}
}}'''

                def _bibtex_book():
                    citekey = _build_citekey()
                    title_val = _safe_str(self.le8.text() if self.le8.text() != '' else self.le1.text())
                    pages_val = _safe_str(self.le10.text())
                    url_val = _safe_str(self.leweb3.text())
                    return f'''@book{{{citekey},
  doi = "{_safe_str(self.le_doi.text())}",
  title = "{title_val}",
  author = "{_safe_str(self.le2.text()).replace('、', ' and ')}",
  publisher = "{_safe_str(self.le3_1.text())}",
  year = {_safe_num(self.le4.text())},
  isbn = "{_safe_str(self.le_isbn.text())}",
  url = "{url_val}",
  pages = "{pages_val}",
}}'''

                def _pick_bibtex():
                    if self.leweb3.text() != '':
                        return _bibtex_misc()
                    if self.leweb3.text() == '' and self.leweb8.text() != '':
                        return _bibtex_inproceedings()
                    if self.le3.text() != '' and self.le3_1.text() == '' and self.leweb3.text() == '' and self.leweb8.text() == '':
                        return _bibtex_article()
                    if self.le3_1.text() != '' and self.le3.text() == '':
                        return _bibtex_book()
                    return _bibtex_article()

                part7_6 = '\n- BibTeX:\n```bibtex\n' + _pick_bibtex() + '\n```'

                part8 = '\n\n---' + '\n\n# Notes'

                with open(fulldir1, 'a', encoding='utf-8') as f1:
                    f1.write(part1+part2+part3+part4+part5+part5_1+part5_5+part6+part6_5+part6_6+part6_7+part7+part7_5+part7_6+part8)
                with open(BasePath + 'path_ttl.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.le1.text())

                archiveempty = codecs.open(BasePath + 'newarchivepath.txt', 'r', encoding='utf-8').read()
                if archiveempty != '':
                    tole1 = archiveempty.split('/')[-1]
                    patternx = re.compile(r'\.[a-zA-Z0-9]+$')
                    result_ex = patternx.findall(tole1)
                    tole2 = ''.join(result_ex)
                    archiveempty_new = archiveempty.replace(tole1, self.le1.text()) + tole2
                    os.rename(archiveempty, archiveempty_new)
                    archiveempty = archiveempty_new

                    home_dir = str(Path.home())
                    archivepath_1 = "Documents"
                    fulldir1 = os.path.join(home_dir, archivepath_1)
                    if not os.path.exists(fulldir1):
                        os.makedirs(fulldir1)
                    archivepath_2 = 'Obsidien Full-text database'
                    fulldir2 = os.path.join(fulldir1, archivepath_2)
                    if not os.path.exists(fulldir2):
                        os.makedirs(fulldir2)
                    if self.le3.text() != '' and self.le4.text() != '' and self.le4_1.text() != '':
                        tarname3 = self.le3.text()
                        fulldir3 = os.path.join(fulldir2, tarname3)
                        tarnamea = self.le4.text()
                        fulldira = os.path.join(fulldir3, tarnamea)
                        tarnameb = self.le4_1.text()
                        fulldirb = os.path.join(fulldira, tarnameb)
                        if not os.path.exists(fulldirb):
                            os.makedirs(fulldirb)
                        shutil.copy(archiveempty, fulldirb)
                        os.remove(archiveempty)
                    if self.le3.text() == '' and self.le8.text() != '':
                        tarname8 = self.le8.text()
                        fulldir8 = os.path.join(fulldir2, tarname8)
                        if not os.path.exists(fulldir8):
                            os.makedirs(fulldir8)
                        shutil.copy(archiveempty, fulldir8)
                        os.remove(archiveempty)
                    if self.le3.text() == '' and self.le8.text() == '':
                        if self.leweb3.text() != '':
                            tarname8 = self.le1.text() + '[web]'
                            fulldir8 = os.path.join(fulldir2, tarname8)
                            if not os.path.exists(fulldir8):
                                os.makedirs(fulldir8)
                            shutil.copy(archiveempty, fulldir8)
                            os.remove(archiveempty)
                        if self.leweb3.text() == '' and self.leweb8.text() != '':
                            tarname8 = self.leweb8.text()
                            fulldir8 = os.path.join(fulldir2, tarname8)
                            if not os.path.exists(fulldir8):
                                os.makedirs(fulldir8)
                            shutil.copy(archiveempty, fulldir8)
                            os.remove(archiveempty)
                        if self.leweb3.text() == '' and self.leweb8.text() == '':
                            tarname8 = 'NEW FOLDER'
                            fulldir8 = os.path.join(fulldir2, tarname8)
                            if not os.path.exists(fulldir8):
                                os.makedirs(fulldir8)
                            shutil.copy(archiveempty, fulldir8)
                            os.remove(archiveempty)
                            CMD = '''
                                on run argv
                                    display notification (item 2 of argv) with title (item 1 of argv)
                                end run'''
                            self.notify(CMD, "Strawberry: Your Literature Collector",
                                        f"The target folder is not named so it is by default moved to the 'NEW FOLDER'.")
            path2 = codecs.open(BasePath + 'path_aut.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                if self.le2.text() != '':
                    expname2 = str(self.le2.text()).replace('+', '、')
                    listexpn2 = expname2.split('、')
                    i = 0
                    while i >= 0 and i <= len(listexpn2) - 1:
                        if '%' not in listexpn2[i]:
                            tarname2 = str(listexpn2[i]) + ".md"
                            fulldir2 = os.path.join(path2, tarname2)
                            with open(fulldir2, 'a', encoding='utf-8') as f0:
                                f0.write('')
                            contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                            if contm != '':
                                part22 = '\n- ' + 'Article: ' + str(self.le1.text())
                                part23 = ''
                                if self.le3.text() != '':
                                    part23 = '【' + 'Publication: ' + str(self.le3.text()) + '】'
                                part24 = ''
                                if self.le8.text() != '':
                                    part24 = '【' + 'Book: ' + str(self.le8.text()) + '】'
                                with open(fulldir2, 'a', encoding='utf-8') as f2:
                                    f2.write(part22 + part23 + part24)
                                i = i + 1
                                continue
                            if contm == '':
                                part22 = '- ' + 'Article: ' + str(self.le1.text())
                                part23 = ''
                                if self.le3.text() != '':
                                    part23 = '【' + 'Publication: ' + str(self.le3.text()) + '】'
                                part24 = ''
                                if self.le8.text() != '':
                                    part24 = '【' + 'Book: ' + str(self.le8.text()) + '】'
                                with open(fulldir2, 'a', encoding='utf-8') as f2:
                                    f2.write(part22 + part23 + part24)
                                i = i + 1
                                continue
                        if '%' in listexpn2[i]:
                            lcname = str(listexpn2[i]).replace('%', '')
                            tarname2 = str(lcname) + ".md"
                            fulldir2 = os.path.join(path2, tarname2)
                            with open(fulldir2, 'a', encoding='utf-8') as f0:
                                f0.write('')
                            contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                            if contm != '':
                                part22 = '\n- ' + 'Translated: ' + str(self.le1.text())
                                part23 = ''
                                if self.le3.text() != '':
                                    part23 = '【' + 'Publication: ' + str(self.le3.text()) + '】'
                                part24 = ''
                                if self.le8.text() != '':
                                    part24 = '【' + 'Book: ' + str(self.le8.text()) + '】'
                                with open(fulldir2, 'a', encoding='utf-8') as f2:
                                    f2.write(part22 + part23 + part24)
                                i = i + 1
                                continue
                            if contm == "":
                                part22 = '- ' + 'Translated: ' + str(self.le1.text())
                                part23 = ''
                                if self.le3.text() != '':
                                    part23 = '【' + 'Publication: ' + str(self.le3.text()) + '】'
                                part24 = ''
                                if self.le8.text() != '':
                                    part24 = '【' + 'Book: ' + str(self.le8.text()) + '】'
                                with open(fulldir2, 'a', encoding='utf-8') as f2:
                                    f2.write(part22 + part23 + part24)
                                i = i + 1
                                continue
                #if self.le2.text() == '':
                    #self.text.setPlainText('Your input is empty!')

            path3 = codecs.open(BasePath + 'path_ins.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.le7.text() != '':
                    expname3 = str(self.le7.text()).replace('+', '、')
                    listexpn3 = expname3.split('、')
                    le7i = 0
                    while le7i >= 0 and le7i <= len(listexpn3) - 1:
                        tarname3 = str(listexpn3[le7i]) + ".md"
                        fulldir3 = os.path.join(path3, tarname3)
                        with open(fulldir3, 'a', encoding='utf-8') as f0:
                            f0.write('')
                        contm = codecs.open(fulldir3, 'r', encoding='utf-8').read()
                        if contm != '':
                            part32 = '\n- ' + 'Title: ' + str(self.le1.text())
                            part33 = ''
                            if '%' not in self.le2.text():
                                part33 = '【Authors: ' + str(self.le2.text() + '】')
                            if '%' in self.le2.text():
                                p3end = str(self.le2.text()).replace('%', '(translator)')
                                part33 = '【Authors: ' + p3end + '】'
                            with open(fulldir3, 'a', encoding='utf-8') as f3:
                                f3.write(part32 + part33)
                            le7i = le7i + 1
                            continue
                        if contm == '':
                            part32 = '- ' + 'Title: ' + str(self.le1.text())
                            part33 = ''
                            if '%' not in self.le2.text():
                                part33 = '【Authors: ' + str(self.le2.text() + '】')
                            if '%' in self.le2.text():
                                p3end = str(self.le2.text()).replace('%', '(translator)')
                                part33 = '【Authors: ' + p3end + '】'
                            with open(fulldir3, 'a', encoding='utf-8') as f3:
                                f3.write(part32 + part33)
                            le7i = le7i + 1
                            continue
                #if self.le7.text() == '':
                    #self.text.setPlainText('Your input is empty!')

            path4 = codecs.open(BasePath + 'path_pub.txt', 'r', encoding='utf-8').read()
            if path4 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.le3.text() != '':
                    tarname4 = str(self.le3.text()) + ".md"
                    fulldir4 = os.path.join(path4, tarname4)
                    with open(fulldir4, 'a', encoding='utf-8') as f0:
                        f0.write('')
                    contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                    if contm != '':
                        part41 = '\n- ' + 'Title: ' + str(self.le1.text())
                        part42 = ''
                        if "%" not in self.le2.text():
                            part42 = '【Authors: ' + str(self.le2.text() + '】')
                        if '%' in self.le2.text():
                            rende = str(self.le2.text()).replace('%', '(translator)')
                            part42 = '【Authors: ' + rende + '】'
                        part43 = '【Vol / Mon: ' + str(self.le4_1.text()) + '】'
                        with open(fulldir4, 'a', encoding='utf-8') as f4:
                            f4.write(part41 + part42 + part43)
                    if contm == '':
                        part41 = '- ' + 'Title: ' + str(self.le1.text())
                        part42 = ''
                        if "%" not in self.le2.text():
                            part42 = '【Authors: ' + str(self.le2.text() + '】')
                        if '%' in self.le2.text():
                            rende = str(self.le2.text()).replace('%', '(translator)')
                            part42 = '【Authors: ' + rende + '】'
                        part43 = '【Vol / Mon: ' + str(self.le4_1.text()) + '】'
                        with open(fulldir4, 'a', encoding='utf-8') as f4:
                            f4.write(part41 + part42 + part43)
                #if self.le3.text() == '':
                    #self.text.setPlainText('Your input is empty!')

            path5 = codecs.open(BasePath + 'path_boo.txt', 'r', encoding='utf-8').read()
            if path5 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                if self.le8.text() != '':
                    tarname5 = str(self.le8.text()) + ".md"
                    fulldir5 = os.path.join(path5, tarname5)
                    with open(fulldir5, 'a', encoding='utf-8') as f0:
                        f0.write('')
                    contm = codecs.open(fulldir5, 'r', encoding='utf-8').read()
                    if contm != '':
                        part51 = '\n- ' + 'Chapter ' + str(self.le9.text())
                        part52 = '【' + str(self.le1.text() + '】')
                        with open(fulldir5, 'a', encoding='utf-8') as f5:
                            f5.write(part51 + part52)
                    if contm == '':
                        part51 = '- ' + 'Chapter ' + str(self.le9.text())
                        part52 = '【' + str(self.le1.text() + '】')
                        with open(fulldir5, 'a', encoding='utf-8') as f5:
                            f5.write(part51 + part52)
                #if self.le8.text() == '':
                    #self.text.setPlainText('Your input is empty!')

            if self.web_t3.isVisible():
                home_dir = str(Path.home())
                tarname1 = "Documents"
                fulldir1 = os.path.join(home_dir, tarname1)
                tarname2 = 'Obsidien'
                fulldir2 = os.path.join(fulldir1, tarname2)
                tarname3 = 'Database'
                fulldir3 = os.path.join(fulldir2, tarname3)
                tarnamea = 'Conference'
                fulldira = os.path.join(fulldir3, tarnamea)
                if self.leweb8.text() != '':
                    tarname6 = str(self.leweb8.text()) + ".md"
                    fulldirb = os.path.join(fulldira, tarname6)
                    with open(fulldirb, 'a', encoding='utf-8') as f0:
                        f0.write('')
                    contm = codecs.open(fulldirb, 'r', encoding='utf-8').read()
                    if contm != '':
                        part61 = '\n- Title: ' + str(self.le1.text())
                        part62 = '【Speakers: ' + str(self.le2.text() + '】')
                        part63 = '【Institutes: ' + str(self.le7.text() + '】')
                        part64 = '【Hosted by: ' + str(self.leweb9.text() + '】')
                        part65 = '【' + str(self.le4.text()) + ' 年 ' + str(self.le4_1.text()) + ' 月'
                        part66 = ''
                        if self.leweb10.text() != '':
                            part66 = '于#' + str(self.leweb10.text())
                        part67 = '】'
                        with open(fulldirb, 'a', encoding='utf-8') as f5:
                            f5.write(part61 + part62 + part63 + part64 + part65 + part66 + part67)
                    if contm == '':
                        part61 = '- Title: ' + str(self.le1.text())
                        part62 = '【Speakers: ' + str(self.le2.text() + '】')
                        part63 = '【Institutes: ' + str(self.le7.text() + '】')
                        part64 = '【Hosted by: ' + str(self.leweb9.text() + '】')
                        part65 = '【' + str(self.le4.text()) + ' 年 ' + str(self.le4_1.text()) + ' 月'
                        part66 = ''
                        if self.leweb10.text() != '':
                            part66 = '于#' + str(self.leweb10.text())
                        part67 = '】'
                        with open(fulldirb, 'a', encoding='utf-8') as f5:
                            f5.write(part61 + part62 + part63 + part64 + part65 + part66 + part67)
                tarnamec = 'Institutes'
                fulldirc = os.path.join(fulldir3, tarnamec)
                if self.leweb9.text() != '':
                    tarname7 = str(self.leweb9.text()) + ".md"
                    fulldird = os.path.join(fulldirc, tarname7)
                    with open(fulldird, 'a', encoding='utf-8') as f0:
                        f0.write('')
                    contm = codecs.open(fulldird, 'r', encoding='utf-8').read()
                    if contm != '':
                        part71 = '\n- Hosted: ' + str(self.leweb8.text())
                        part72 = ''
                        if self.leweb8.text() == '':
                            part72 = '【' + str(self.le1.text()) + '】'
                        with open(fulldird, 'a', encoding='utf-8') as f5:
                            f5.write(part71 + part72)
                    if contm == '':
                        part71 = '- Hosted: ' + str(self.leweb8.text())
                        part72 = ''
                        if self.leweb8.text() == '':
                            part72 = '【' + str(self.le1.text()) + '】'
                        with open(fulldird, 'a', encoding='utf-8') as f5:
                            f5.write(part71 + part72)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                pos = len(self.text.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text.setTextCursor(cursor)  # 滚动到游标位置

            self.read_t1.setVisible(False)
            self.read_t2.setVisible(False)
            self.read_t7.setVisible(False)
            self.read_t3.setVisible(False)
            self.read_t8.setVisible(False)
            self.read_t4.setVisible(False)
            self.read_t4_doi.setVisible(False)
            self.read_t4_isbn.setVisible(False)
            self.read_t5.setVisible(False)
            self.lbltool06.setVisible(False)
            self.tool8.setVisible(False)
            self.btnx4.setStyleSheet('''
                QPushButton{
                border: transparent;
                background-color: transparent;
                border-image: url(/Applications/Strawberry.app/Contents/Resources/down.png);
                }
                QPushButton:pressed{
                border: 1px outset grey;
                background-color: #0085FF;
                border-radius: 4px;
                padding: 1px;
                color: #FFFFFF
                }
                ''')
            if self.btn_t9.text() == 'Turned on!':
                self.web_t3.setVisible(False)
                self.web_t8.setVisible(False)

            self.btnmain2.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
            self.btnmain2.setText('Added')
            self.le1.setEnabled(False)
            reset_newarchive_path()

    def clearabv(self):
        if self.text.toPlainText() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text.toPlainText()
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)
        self.le1.clear()
        self.le2.clear()
        self.le7.clear()
        self.le3.clear()
        self.le3_1.clear()
        self.le4.clear()
        self.le4_1.clear()
        self.le_doi.clear()
        self.le_isbn.clear()
        self.le5.clear()
        self.le8.clear()
        self.le9.clear()
        self.le10.clear()
        self.text.clear()
        self.text11.clear()
        self.text12.clear()
        self.text13.clear()
        self.text14.clear()
        self.le20.clear()
        self.le21.clear()
        self.text21.clear()
        self.text22.clear()
        self.lec1.clear()
        self.lec2.clear()
        self.text31.clear()
        self.lec0.clear()
        self.text41.clear()
        self.text42.clear()
        self.text43.clear()
        self.text44.clear()
        self.text45.clear()
        self.text46.clear()
        self.text47.clear()
        self.lem1.clear()
        self.lem2.clear()
        self.text51.clear()
        self.text_s2.clear()
        self.text_s3.clear()
        self.text_s4.clear()
        self.btnmain2.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btnmain2.setText('Add')
        self.btn_ex11.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #FFFFFF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #000000''')
        self.btn_ex11.setText('Add')
        self.btn_cl12.setStyleSheet('''
                                border: 1px outset grey;
                                background-color: #FFFFFF;
                                border-radius: 4px;
                                padding: 1px;
                                color: #000000''')
        self.btn_cl12.setText('Add')
        self.btn_ana13.setStyleSheet('''
                                border: 1px outset grey;
                                background-color: #FFFFFF;
                                border-radius: 4px;
                                padding: 1px;
                                color: #000000''')
        self.btn_ana13.setText('Add')
        self.btn_2k1.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #FFFFFF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #000000''')
        self.btn_2k1.setText('Add')
        self.btn_ce31.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_ce31.setText('Add')
        self.btn_ce32.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_ce32.setText('Add')
        self.btn_the30.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the30.setText('Add')
        self.btn_the41.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the41.setText('+')
        self.btn_the42.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the42.setText('+')
        self.btn_the43.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the43.setText('+')
        self.btn_the44.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the44.setText('+')
        self.btn_the45.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the45.setText('+')
        self.btn_the46.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the46.setText('+')
        self.btn_the47.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_the47.setText('+')
        self.btn_51.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_51.setText('Add')
        self.btn_52.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_52.setText('Add')
        self.widget0.clear()
        self.widget0.addItems(['Append at the end (default)', 'Append at the current cursor'])
        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
            f0.write('')
        self.le1.setEnabled(True)
        with open(BasePath + 'path_ttl.txt', 'w', encoding='utf-8') as fz:
            fz.write('')
        self.leweb3.clear()
        self.read_t1.setVisible(True)
        self.read_t2.setVisible(True)
        self.read_t7.setVisible(True)
        self.read_t3.setVisible(True)
        self.read_t8.setVisible(True)
        self.read_t4.setVisible(True)
        self.read_t4_doi.setVisible(True)
        self.read_t4_isbn.setVisible(True)
        self.read_t5.setVisible(True)
        self.lbltool06.setVisible(True)
        self.tool8.setVisible(True)
        self.btnx4.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/up.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        if self.btn_t9.text() == 'Turned on!':
            self.web_t3.setVisible(True)
            self.web_t8.setVisible(True)
            self.read_t3.setVisible(False)
            self.read_t8.setVisible(False)
        reset_newarchive_path()

    def addprob(self):
        if self.btn_ex11.text() != 'Added and renewed list' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text11.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text11.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                speaker_name = ''
                if self.speaker.isVisible() and self.speaker.text() != '':
                    speaker_name = 'From ' + self.speaker.text() + ' - '

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = '\n\n## ' + 'Q/P: ' + speaker_name + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text11.toPlainText())))) + '\n'
                part_n = '\n' + get_rst
                if self.le1.text() != '' and self.text11.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            path2 = codecs.open(BasePath + 'path_pro.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text11.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text11.setStyleSheet('color:red')
            else:
                if self.text11.toPlainText() != '':
                    tarname2 = str(self.cleaninput(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text11.toPlainText()))))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    with open(fulldir2, 'a', encoding='utf-8') as f0:
                        f0.write('')
                    contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                    if contm != '':
                        part21 = ''
                        if self.le1.text() != '':
                            part21 = '\n- ' + 'Title: ' + str(self.le1.text())
                        part22 = ''
                        if self.le2.text() != '':
                            if '%' not in self.le2.text():
                                part22 = '【Authors: ' + str(self.le2.text() + '】')
                            if '%' in self.le2.text():
                                p3end = str(self.le2.text()).replace('%', '(translator)')
                                part22 = '【Authors: ' + p3end + '】'
                        part23 = ''
                        if self.le1.text() == '' and self.le2.text() == '':
                            part23 = 'This P / Q is formed by mere thinking.'
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part21 + part22 + part23)
                    if contm == '':
                        part21 = ''
                        if self.le1.text() != '':
                            part21 = '- ' + 'Title: ' + str(self.le1.text())
                        part22 = ''
                        if self.le2.text() != '':
                            if '%' not in self.le2.text():
                                part22 = '【Authors: ' + str(self.le2.text() + '】')
                            if '%' in self.le2.text():
                                p3end = str(self.le2.text()).replace('%', '(translator)')
                                part22 = '【Authors: ' + p3end + '】'
                        part23 = ''
                        if self.le1.text() == '' and self.le2.text() == '':
                            part23 = 'This P / Q is formed by mere thinking.'
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part21 + part22 + part23)
                #if self.text11.toPlainText() == '':
                    #self.text.setPlainText('Your input is empty!')

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            if self.text11.toPlainText() != '':
                self.btn_ex11.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #0085FF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #FFFFFF''')
                self.btn_ex11.setText('Added and renewed list')
                self.text11.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text11.toPlainText()))))

            itemold = self.widget0.currentText()
            self.widget0.clear()
            self.widget0.addItems(['Append at the end (default)', 'Append at the current cursor'])
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            if self.le1.text() != '':
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                pattern = re.compile(r'## (.*?)\n')
                result = pattern.findall(maintxt)
                result2 = '☆'.join(result)
                if result != []:
                    result = result2.replace('#', '')
                    result = result.replace('# ', '')
                    result = result.replace('Q/P: ', '')
                    result = result.split('☆')
                    for i in range(len(result)):
                        result[i] = 'After ' + result[i]
                        result[i] = ''.join(result[i])
                    self.widget0.addItems(result)
                    if itemold in result:
                        itemnub = result.index(itemold) + 2
                        self.widget0.setCurrentIndex(itemnub)
                    if itemold not in result:
                        self.widget0.setCurrentIndex(0)

    def clearpro(self):
        self.text11.clear()
        self.text12.clear()
        self.text13.clear()
        self.text14.clear()
        self.btn_ex11.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btn_ex11.setText('Add')
        self.btn_cl12.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #FFFFFF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #000000''')
        self.btn_cl12.setText('Add')
        self.btn_ana13.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #FFFFFF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #000000''')
        self.btn_ana13.setText('Add')

    def addcla(self):
        if self.btn_cl12.text() != 'Added' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text12.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text12.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                speaker_name = ''
                if self.speaker.isVisible() and self.speaker.text() != '':
                    speaker_name = 'From ' + self.speaker.text() + ' - '

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = '\n- ' + 'Claim: ' + speaker_name + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text12.toPlainText())))) + '\n'
                part_n = '\n' + get_rst
                if self.le1.text() != '' and self.text12.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            if self.text12.toPlainText() != '':
                self.btn_cl12.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #0085FF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #FFFFFF''')
                self.btn_cl12.setText('Added')
                self.text12.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text12.toPlainText()))))

    def clearcla(self):
        self.text12.clear()
        self.text13.clear()
        self.text14.clear()
        self.btn_cl12.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btn_cl12.setText('Add')
        self.btn_ana13.setStyleSheet('''
                        border: 1px outset grey;
                        background-color: #FFFFFF;
                        border-radius: 4px;
                        padding: 1px;
                        color: #000000''')
        self.btn_ana13.setText('Add')

    def addana(self):
        if self.btn_ana13.text() != 'Added' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text13.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text13.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                speaker_name = ''
                if self.speaker.isVisible() and self.speaker.text() != '':
                    speaker_name = 'From ' + self.speaker.text() + ' - '

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = ''
                part_n = '\n' + get_rst
                if self.text12.toPlainText() != "":
                    part1 = '\n\t- ' + 'Analysis: ' + speaker_name + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text13.toPlainText())))) + '\n'
                if self.text12.toPlainText() == "":
                    part1 = '\n- ' + 'Analysis: ' + speaker_name + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text13.toPlainText())))) + '\n'
                if self.le1.text() != '' and self.text13.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

        if self.text13.toPlainText() != '':
            self.btn_ana13.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
            self.btn_ana13.setText('Added')
            self.text13.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text13.toPlainText()))))

    def clearana(self):
        self.text13.clear()
        self.text14.clear()
        self.btn_ana13.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btn_ana13.setText('Add')

    def addmy(self):
        if self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text14.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text14.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                speaker_name = ''
                if self.speaker.isVisible() and self.speaker.text() != '':
                    speaker_name = 'From ' + self.speaker.text() + ' - '

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = ''
                part_n = '\n' + get_rst
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + speaker_name + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part1 = '\n\t- ' + speaker_name + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part1 = '\n\t- ' + speaker_name + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part1 = '\n- ' + speaker_name + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.le1.text() != '' and self.text14.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            self.text14.clear()

    def addexc(self):
        if self.btn_2k1.text() != 'Added' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text21.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text21.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part0 = ''
                part_n = '\n' + get_rst
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part0 = '\n\t\t- '
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part0 = '\n\t- '
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part0 = '\n\t- '
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part0 = '\n- '
                part1 = '[Excerpt]'
                if self.le9.text() != '' and self.le20.text() != '' and self.le21.text() != '':
                    part1 = '[Chapter ' + str(self.le9.text()) + ', Part ' + str(self.le20.text()) + ', Page ' + str(self.le21.text()) + ']'
                if self.le9.text() == '' and (self.le20.text() and self.le21.text() != ''):
                    part1 = '[Part ' + str(self.le20.text()) + ', Page ' + str(self.le21.text()) + ']'
                if self.le9.text() != '' and self.le20.text() == '' and self.le21.text() != '':
                    part1 = '[Chapter ' + str(self.le9.text()) + ', Page ' + str(self.le21.text()) + ']'
                if self.le9.text() != '' and self.le20.text() != '' and self.le21.text() == '':
                    part1 = '[Chapter ' + str(self.le9.text()) + ', Part ' + str(self.le20.text()) + ']'
                if self.le9.text() == '' and self.le20.text() == '' and self.le21.text() != '':
                    part1 = '[Page ' + str(self.le21.text()) + ']'
                if self.le9.text() == '' and self.le20.text() != '' and self.le21.text() == '' :
                    part1 = '[Part ' + str(self.le20.text()) + ']'
                if self.le9.text() != '' and self.le20.text() == ''and self.le21.text() == '':
                    part1 = '[Chapter ' + str(self.le9.text()) + ']'
                if self.le9.text() == '' and self.le20.text() == '' and self.le21.text() == '':
                    part1 = '[Excerpt]'

                part2 = '「' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text21.toPlainText())))) + '」\n'
                if self.le1.text() != '' and self.text21.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part0 + part1 + part2 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            if self.text21.toPlainText() != '':
                self.btn_2k1.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
                self.btn_2k1.setText('Added')
                self.text21.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text21.toPlainText()))))

    def clearexc(self):
        # self.le20.clear()
        self.le21.clear()
        self.text21.clear()
        self.text22.clear()
        self.btn_2k1.setStyleSheet('''
            border: 1px outset grey;
            background-color: #FFFFFF;
            border-radius: 4px;
            padding: 1px;
            color: #000000''')
        self.btn_2k1.setText('Add')

    def addmv(self):
        if self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text22.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text22.setStyleSheet('color:red')
            else:
                if self.widget0.currentIndex() == 1:
                    keepsave = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    with open(BasePath + 'currentcursor.txt', 'w', encoding='utf-8') as f0:
                        f0.write(keepsave)

                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part_n = '\n' + get_rst
                part0 = ''
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part0 = '\n\t\t'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part0 = '\n\t'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part0 = '\n\t'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part0 = '\n'
                part1 = '\t- ' + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text22.toPlainText())))) + '】\n'
                if self.le1.text() != '' and self.text22.toPlainText() != '' and self.text21.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part0 + part1 + part_n)
                    self.text22.clear()

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    if self.widget0.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_rst.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

    def addcon(self):
        if self.btn_ce31.text() != 'Added' and self.le1.text() != '' and self.lec1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lec1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part_n = '\n' + get_rst
                part1 = ''
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + '【The article explained a concept: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part1 = '\n\t- ' + '【The article explained a concept: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part1 = '\n\t- ' + '【The article explained a concept: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part1 = '\n- ' + '【The article explained a concept: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + '.】' + '\n'
                if self.le1.text() != '' and self.lec1.text() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lec1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lec1.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    with open(fulldir2, 'a', encoding='utf-8') as f0:
                        f0.write('')
                #if self.lec1.text() == '':
                    #self.text_s2.setPlainText('Your input is empty!')

            pathend2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec1.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s2.setPlainText(contend2)
                    self.text_s2.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s2.textCursor()  # 设置游标
                    pos = len(self.text_s2.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s2.setTextCursor(cursor)  # 滚动到游标位置

            if self.lec1.text() != '':
                self.btn_ce31.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_ce31.setText('Added')
                self.lec1.setText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text()))))
                self.lec1.setEnabled(False)

    def clearnam(self):
        self.lec1.clear()
        self.text_s2.clear()
        self.lec2.clear()
        self.text31.clear()
        self.btn_ce31.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #FFFFFF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #000000''')
        self.btn_ce31.setText('Add')
        self.btn_ce32.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_ce32.setText('Add')
        self.lec1.setEnabled(True)

    def addpers(self):
        if self.btn_ce32.text() != 'Added' and self.lec1.text() != '':
            path2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lec2.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                part1 = ''
                if contm != '':
                    part1 = '\n- ' + 'Perspective: '
                if contm == '':
                    part1 = '- ' + 'Perspective: '
                part2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec2.text()))))
                if self.lec1.text() != '' and self.lec2.text() != '':
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1 + part2)

            pathend2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec1.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s2.setPlainText(contend2)
                    self.text_s2.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s2.textCursor()  # 设置游标
                    pos = len(self.text_s2.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s2.setTextCursor(cursor)  # 滚动到游标位置

            if self.lec2.text() != '':
                self.btn_ce32.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_ce32.setText('Added')
                self.lec2.setText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec2.text()))))

    def cleanpers(self):
        self.lec2.clear()
        self.text31.clear()
        self.btn_ce32.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #FFFFFF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #000000''')
        self.btn_ce32.setText('Add')

    def addconexp(self):
        path2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if path2 == '':
            self.text31.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            part1 = '\n\t- Explanation: ' + str(self.default_clean(self.text31.toPlainText()))
            part2 = ''
            if self.le1.text() != '':
                part2 = '【from ' + str(self.le1.text()) + '】'
            part3 = ''
            if self.le8.text() != '':
                part3 = '【from ' + str(self.le8.text()) + '】'
            if self.lec1.text() != '' and self.text31.toPlainText() != '':
                with open(fulldir2, 'a', encoding='utf-8') as f2:
                    f2.write(part1 + part2 + part3)

        pathend2 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if pathend2 == '':
            self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
            fulldirend2 = os.path.join(pathend2, tarnameend2)
            if self.lec1.text() != '':
                contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                self.text_s2.setPlainText(contend2)
                self.text_s2.ensureCursorVisible()  # 游标可用
                cursor = self.text_s2.textCursor()  # 设置游标
                pos = len(self.text_s2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text_s2.setTextCursor(cursor)  # 滚动到游标位置

        self.text31.clear()

    def addthero(self):
        if self.btn_the30.text() != 'Added' and self.le1.text() != '' and self.lec0.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lec0.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part_n = '\n' + get_rst
                part1 = ''
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + '【The article explained a theory: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part1 = '\n\t- ' + '【The article explained a theory: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + '.】' + '\n'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part1 = '\n\t- ' + '【The article explained a theory: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part1 = '\n- ' + '【The article explained a theory: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + '.】' + '\n'
                if self.le1.text() != '' and self.lec0.text() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lec0.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lec0.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    part1 = ''
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1)
                #if self.lec0.text() == '':
                    #self.text_s3.setPlainText('Your input is empty!')

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.lec0.text() != '':
                self.btn_the30.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_the30.setText('Added')
                self.lec0.setText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text()))))
                self.lec0.setEnabled(False)

    def clthen(self):
        self.lec0.clear()
        self.text_s3.clear()
        self.btn_the30.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the30.setText('Add')

        self.text41.clear()
        self.btn_the41.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the41.setText('+')

        self.text42.clear()
        self.btn_the42.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the42.setText('+')

        self.text43.clear()
        self.btn_the43.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the43.setText('+')

        self.text44.clear()
        self.btn_the44.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the44.setText('+')

        self.text45.clear()
        self.btn_the45.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the45.setText('+')

        self.text46.clear()
        self.btn_the46.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the46.setText('+')

        self.text47.clear()
        self.btn_the47.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_the47.setText('+')
        self.lec0.setEnabled(True)

    def addpoprefe(self):
        if self.btn_the41.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text41.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Question preferences: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text41.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text41.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 +part3)
                if contm == '':
                    part1 = '- Question preferences: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text41.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text41.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text41.toPlainText() != '':
                self.btn_the41.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_the41.setText('✓')
                self.text41.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text41.toPlainText()))))

    def clearpropref(self):
        self.text41.clear()
        self.btn_the41.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the41.setText('+')

    def addmetpref(self):
        if self.btn_the42.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text42.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Method preferences: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text42.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text42.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Method preferences: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text42.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text42.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text42.toPlainText() != '':
                self.btn_the42.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the42.setText('✓')
                self.text42.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text42.toPlainText()))))

    def clearmedpref(self):
        self.text42.clear()
        self.btn_the42.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the42.setText('+')

    def thnpatt(self):
        if self.btn_the43.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text43.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Thinking patterns: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text43.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text43.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Thinking patterns: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text43.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text43.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text43.toPlainText() != '':
                self.btn_the43.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the43.setText('✓')
                self.text43.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text43.toPlainText()))))

    def clearthnptn(self):
        self.text43.clear()
        self.btn_the43.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the43.setText('+')

    def thnbasv(self):
        if self.btn_the44.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text44.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Basic views: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text44.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text44.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Basic views: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text44.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text44.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text44.toPlainText() != '':
                self.btn_the44.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the44.setText('✓')
                self.text44.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text44.toPlainText()))))

    def clearbscpv(self):
        self.text44.clear()
        self.btn_the44.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the44.setText('+')

    def emexpls(self):
        if self.btn_the45.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text45.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Empirical examples: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text45.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text45.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Empirical examples: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text45.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text45.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text45.toPlainText() != '':
                self.btn_the45.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the45.setText('✓')
                self.text45.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text45.toPlainText()))))

    def clearemepls(self):
        self.text45.clear()
        self.btn_the45.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the45.setText('+')

    def addreviwcmts(self):
        if self.btn_the46.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text46.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Reviews and comments: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text46.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text46.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Reviews and comments: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text46.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text46.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text46.toPlainText() != '':
                self.btn_the46.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the46.setText('✓')
                self.text46.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text46.toPlainText()))))

    def clearecmt(self):
        self.text46.clear()
        self.btn_the46.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the46.setText('+')

    def addevotr(self):
        if self.btn_the47.text() != '✓':
            path2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text47.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                if contm != '':
                    part1 = '\n- Evolution and trends: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text47.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text47.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)
                if contm == '':
                    part1 = '- Evolution and trends: ' + str(
                        self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text47.toPlainText()))))
                    part2 = ''
                    if self.le1.text() != '':
                        part2 = '【from ' + str(self.le1.text()) + '】'
                    part3 = ''
                    if self.le8.text() != '':
                        part3 = '【from ' + str(self.le8.text()) + '】'
                    if self.lec0.text() != '' and self.text47.toPlainText() != '':
                        with open(fulldir2, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + part2 + part3)

            pathend2 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lec0.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s3.setPlainText(contend2)
                    self.text_s3.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s3.textCursor()  # 设置游标
                    pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

            if self.text47.toPlainText() != '':
                self.btn_the47.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_the47.setText('✓')
                self.text47.setPlainText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text47.toPlainText()))))

    def clearevotr(self):
        self.text47.clear()
        self.btn_the47.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_the47.setText('+')

    def addmetds(self):
        if self.btn_51.text() != 'Added' and self.le1.text() != '' and self.lem1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lem1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part_n = '\n' + get_rst
                part1 = ''
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + '【The article used a method: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part1 = '\n\t- ' + '【The article used a method: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part1 = '\n\t- ' + '【The article used a method: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + '.】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part1 = '\n- ' + '【The article used a method: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + '.】' + '\n'
                if self.le1.text() != '' and self.lem1.text() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open(BasePath + 'path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lem1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lem1.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    with open(fulldir2, 'a', encoding='utf-8') as f0:
                        f0.write('')
                #if self.lem1.text() == '':
                    #self.text_s4.setPlainText('Your input is empty!')

            pathend2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lem1.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s4.setPlainText(contend2)
                    self.text_s4.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s4.textCursor()  # 设置游标
                    pos = len(self.text_s4.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s4.setTextCursor(cursor)  # 滚动到游标位置

            if self.lem1.text() != '':
                self.btn_51.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_51.setText('Added')
                self.lem1.setText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text()))))
                self.lem1.setEnabled(False)

    def clearmetnm(self):
        self.lem1.clear()
        self.text_s4.clear()
        self.btn_51.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_51.setText('Add')
        self.lem2.clear()
        self.btn_52.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_52.setText('Add')
        self.text51.clear()
        self.lem1.setEnabled(True)

    def addmetneeds(self):
        if self.btn_52.text() != 'Added' and self.lem1.text() != '':
            path2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lem2.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
                fulldir2 = os.path.join(path2, tarname2)
                contm = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                part1 = ''
                if contm != '':
                    part1 = '\n- ' + 'Needs to be met: '
                if contm == '':
                    part1 = '- ' + 'Needs to be met: '
                part2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem2.text()))))
                if self.lem1.text() != '' and self.lem2.text() != '':
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1 + part2)

            pathend2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
                fulldirend2 = os.path.join(pathend2, tarnameend2)
                if self.lem1.text() != '':
                    contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                    self.text_s4.setPlainText(contend2)
                    self.text_s4.ensureCursorVisible()  # 游标可用
                    cursor = self.text_s4.textCursor()  # 设置游标
                    pos = len(self.text_s4.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text_s4.setTextCursor(cursor)  # 滚动到游标位置

            if self.lem2.text() != '':
                self.btn_52.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.btn_52.setText('Added')
                self.lem2.setText(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem2.text()))))

    def clearmetneeds(self):
        self.lem2.clear()
        self.text51.clear()
        self.btn_52.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
        self.btn_52.setText('Add')

    def addmetdets(self):
        path2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if path2 == '':
            self.text51.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            part1 = '\n\t- Explanation: ' + str(self.default_clean(self.text51.toPlainText()))
            part2 = ''
            if self.le1.text() != '':
                part2 = '【from ' + str(self.le1.text()) + '】'
            part3 = ''
            if self.le8.text() != '':
                part3 = '【from ' + str(self.le8.text()) + '】'
            if self.lem1.text() != '' and self.text51.toPlainText() != '':
                with open(fulldir2, 'a', encoding='utf-8') as f2:
                    f2.write(part1 + part2 +part3)

        pathend2 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if pathend2 == '':
            self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
            fulldirend2 = os.path.join(pathend2, tarnameend2)
            if self.lem1.text() != '':
                contend2 = codecs.open(fulldirend2, 'r', encoding='utf-8').read()
                self.text_s4.setPlainText(contend2)
                self.text_s4.ensureCursorVisible()  # 游标可用
                cursor = self.text_s4.textCursor()  # 设置游标
                pos = len(self.text_s4.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text_s4.setTextCursor(cursor)  # 滚动到游标位置

        self.text51.clear()

    def findandrepopen(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Start replacement!", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                contend = contend.replace(self.tool1_5.text(), self.tool1.text())
                with open(file_name, 'w', encoding='utf-8') as f2:
                    f2.write(contend)
                self.tool1.clear()
                self.tool1_5.clear()

    def fanrep(self):
        if self.le1.text() != '':
            path2 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = contend.replace(self.tool1_5.text(), self.tool1.text())
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)
            self.tool1.clear()
            self.tool1_5.clear()

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                pos = len(self.text.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text.setTextCursor(cursor)  # 滚动到游标位置
        if self.le1.text() == '':
            self.tool1.setText('The article file is not open, please open a file!')

    def redirtname(self):
        if self.le1.text() != '':
            path2 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            targ = '[[' + self.tool3.text() + '|' + self.tool2.text() + ']]'
            contend = contend.replace(self.tool2.text(), targ)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)
            self.tool2.clear()
            self.tool3.clear()

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                pos = len(self.text.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text.setTextCursor(cursor)  # 滚动到游标位置
        if self.le1.text() == '':
            self.tool2.setText('The article file is not open, please open a file!')

    def anotred(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Start redirection!", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                targ = '[[' + self.tool3.text() + '|' + self.tool2.text() + ']]'
                contend = contend.replace(self.tool2.text(), targ)
                with open(file_name, 'w', encoding='utf-8') as f2:
                    f2.write(contend)
                self.tool2.clear()
                self.tool3.clear()

    def bioarton(self):
        if self.le1.text() != '':
            path2 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = self.addb(contend)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                pos = len(self.text.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text.setTextCursor(cursor)  # 滚动到游标位置

    def bioartoff(self):
        if self.le1.text() != '':
            path2 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = self.remb(contend)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)

            pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.ensureCursorVisible()  # 游标可用
                cursor = self.text.textCursor()  # 设置游标
                pos = len(self.text.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text.setTextCursor(cursor)  # 滚动到游标位置

    def anobioon(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Start redirection!", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                contend = self.addb(contend)
                with open(file_name, 'w', encoding='utf-8') as f2:
                    f2.write(contend)

    def anobiooff(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Start redirection!", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                contend = self.remb(contend)
                with open(file_name, 'w', encoding='utf-8') as f2:
                    f2.write(contend)

    def addb(self, a):
        if a != None and a != '':
            a = str(a)
            aj = jieba.cut(a, cut_all=False)
            paj = '/'.join(aj)
            saj = paj.split('/')

            def containenglish(str0):  # 判断是否包含英文字母
                import re
                return bool(re.search('[a-zA-Zａ-ｚＡ-Ｚ]', str0))

            def is_contain_chinese(check_str):  # 判断是否包含中文字
                for ch in check_str:
                    if u'\u4e00' <= ch <= u'\u9fff':
                        return True
                return False

            def is_contain_num(str0):  # 判断是否包含数字
                import re
                return bool(re.search('[0-9０-９]', str0))

            def is_contain_symbol(keyword):
                if re.search(r"\W", keyword):
                    return True
                else:
                    return False

            for i in range(len(saj)):
                if containenglish(str(saj[i])) or is_contain_chinese(str(saj[i])) or is_contain_num(str(saj[i])):
                    if len(saj[i]) == 1:
                        saj[i] = '**' + saj[i] + '**'
                        i = i + 1
                        continue
                    if len(saj[i]) >= 2:
                        if 'ing' in saj[i]:
                            saj[i] = saj[i].replace('ing', '**ing')
                            saj[i] = saj[i].replace('**ing**ing', 'ing**ing')
                            laj = list(saj[i])
                            laj.insert(0, '**')
                            saj[i] = ''.join(laj)
                            i = i + 1
                            continue
                        else:
                            if len(saj[i]) % 2 == 0:
                                laj = list(saj[i])
                                uu = len(saj[i]) / 2
                                laj.insert(int(uu), '**')
                                laj.insert(0, '**')
                                saj[i] = ''.join(laj)
                                i = i + 1
                                continue
                            if len(saj[i]) % 2 != 0:
                                laj = list(saj[i])
                                laj.insert(0, '**')
                                uu = len(saj[i]) + 1
                                laj.insert(int(uu / 2) + 1, '**')
                                saj[i] = ''.join(laj)
                                i = i + 1
                                continue

            esj = ''.join(saj)

            def find_this(q, i):
                result = q[i]
                return result

            def find_next(q, i):
                result = q[i + 1]
                return result

            i = 0
            while i <= len(esj) - 1:
                if esj[i] == '¥' and not is_contain_symbol(str(esj[i - 1])):
                    esj = list(esj)
                    esj.insert(i, ' ')
                    esj = ''.join(esj)
                    i = i + 2
                    continue
                if esj[i] == '$' and not is_contain_symbol(str(esj[i - 1])):
                    esj = list(esj)
                    esj.insert(i, ' ')
                    esj = ''.join(esj)
                    i = i + 2
                    continue
                if esj[i] == "%":
                    if esj[i - 1] == ' ':
                        esj = list(esj)
                        del esj[i - 1]
                        esj = ''.join(esj)
                        i = i - 1
                        continue
                    else:
                        esj = list(esj)
                        esj.insert(i + 1, ' ')
                        esj = ''.join(esj)
                        i = i + 2
                        continue
                if esj[i] == "°":
                    if esj[i - 1] == ' ':
                        esj = list(esj)
                        del esj[i - 1]
                        esj = ''.join(esj)
                        i = i - 1
                        continue
                    else:
                        esj = list(esj)
                        esj.insert(i + 1, ' ')
                        esj = ''.join(esj)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            i = 0
            while i >= 0 and i < len(esj) - 1:
                if is_contain_chinese(str(find_this(esj, i))) and containenglish(str(find_next(esj, i))):  # 从中文转英文
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_this(esj, i))) and is_contain_num(str(find_next(esj, i))):  # 从中文转数字
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(esj, i))) and is_contain_num(str(find_this(esj, i))):  # 从数字转中文
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                if is_contain_num(str(find_this(esj, i))) and containenglish(str(find_next(esj, i))):  # 从数字转英文
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(esj, i))) and containenglish(str(find_this(esj, i))):  # 从英文转数字
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(esj, i))) and containenglish(str(find_this(esj, i))):  # 从英文转中文
                    esj = list(esj)
                    esj.insert(i + 1, ' ')
                    esj = ''.join(esj)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 清除连续空格
            esj = esj.replace('  ', ' ')
            esj = esj.replace('****', '')

            return str(esj)

    def remb(self, a):
        if a != None and a != '':
            zui = a.replace('*', '')

            def containenglish(str0):  # 判断是否包含英文字母
                import re
                return bool(re.search('[a-zA-Zａ-ｚＡ-Ｚ]', str0))

            def is_contain_chinese(check_str):  # 判断是否包含中文字
                for ch in check_str:
                    if u'\u4e00' <= ch <= u'\u9fff':
                        return True
                return False

            def is_contain_num(str0):  # 判断是否包含数字
                import re
                return bool(re.search('[0-9０-９]', str0))

            def is_contain_symbol(keyword):
                if re.search(r"\W", keyword):
                    return True
                else:
                    return False

            def find_this(q, i):
                result = q[i]
                return result

            def find_next(q, i):
                result = q[i + 1]
                return result

            i = 0
            while i <= len(zui) - 1:
                if zui[i] == '¥' and not is_contain_symbol(str(zui[i - 1])):
                    zui = list(zui)
                    zui.insert(i, ' ')
                    zui = ''.join(zui)
                    i = i + 2
                    continue
                if zui[i] == '$' and not is_contain_symbol(str(zui[i - 1])):
                    zui = list(zui)
                    zui.insert(i, ' ')
                    zui = ''.join(zui)
                    i = i + 2
                    continue
                if zui[i] == "%":
                    if zui[i - 1] == ' ':
                        zui = list(zui)
                        del zui[i - 1]
                        zui = ''.join(zui)
                        i = i - 1
                        continue
                    else:
                        zui = list(zui)
                        zui.insert(i + 1, ' ')
                        zui = ''.join(zui)
                        i = i + 2
                        continue
                if zui[i] == "°":
                    if zui[i - 1] == ' ':
                        zui = list(zui)
                        del zui[i - 1]
                        zui = ''.join(zui)
                        i = i - 1
                        continue
                    else:
                        zui = list(zui)
                        zui.insert(i + 1, ' ')
                        zui = ''.join(zui)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            i = 0
            while i >= 0 and i < len(zui) - 1:
                if is_contain_chinese(str(find_this(zui, i))) and containenglish(str(find_next(zui, i))):  # 从中文转英文
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_this(zui, i))) and is_contain_num(str(find_next(zui, i))):  # 从中文转数字
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(zui, i))) and is_contain_num(str(find_this(zui, i))):  # 从数字转中文
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                if is_contain_num(str(find_this(zui, i))) and containenglish(str(find_next(zui, i))):  # 从数字转英文
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(zui, i))) and containenglish(str(find_this(zui, i))):  # 从英文转数字
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(zui, i))) and containenglish(str(find_this(zui, i))):  # 从英文转中文
                    zui = list(zui)
                    zui.insert(i + 1, ' ')
                    zui = ''.join(zui)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 清除连续空格
            zui = zui.replace('  ', ' ')
            return str(zui)

    def from_ext(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                patterna = re.compile(r'【.*?】')
                resultp = patterna.findall(contend)
                resultp = '\n\n'.join(resultp)
                resultp = resultp.replace('【', '')
                resultp = resultp.replace('】', '')
                self.fromtext = resultp
                self.btn_t5.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #0085FF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #FFFFFF''')
                self.btn_t5.setText('Added')

    def to_ext(self):
        pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if pathscr != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", pathscr, "Markdown Files (*.md)")
            if file_name != '':
                self.to = file_name
                contm = codecs.open(file_name, 'r', encoding='utf-8').read()
                patterna = re.compile(r'\n\n\n\n## References[\s\S]*')
                resultp = patterna.findall(contm)
                self.oric = ''.join(resultp)
                a = re.sub(r"\n\n\n\n## References[\s\S]*", '', contm)
                for i in range(10):
                    a = a.replace('\r', '☆')
                    a = a.replace('\n', '☆')
                    a = a.replace('☆☆☆☆', '☆☆')
                    a = a.replace('☆☆☆', '☆☆')
                self.ori = a.replace('☆', '\n')
                self.btn_t6.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')
                self.btn_t6.setText('Added')

    def start_ext(self):
        with open(self.to, 'w', encoding='utf-8') as fp:
            fp.write(self.ori + '\n\n' + self.fromtext + self.oric)
        self.btn_t5.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        self.btn_t5.setText('From')
        self.btn_t6.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #FFFFFF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #000000''')
        self.btn_t6.setText('To')
        oldv = self.textii2.verticalScrollBar().value()
        oldmax = self.textii2.verticalScrollBar().maximum()
        pathend = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.leii1.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.leii1.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self._show_inspiration_content(contend)
                newbar = self.textii2.verticalScrollBar()
                if oldmax != 0 and newbar.maximum() != 0:
                    proportion_old = oldv / oldmax
                    newbar.setValue(int(newbar.maximum() * proportion_old))
                if newbar.maximum() != 0:
                    proportion = newbar.value() / newbar.maximum()
                    tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
                    self.real2.verticalScrollBar().setValue(tar_pro)
        self.textii3.setPlainText('')

    def openris(self):
        home_dir = str(Path.home())
        file_name, ok = QFileDialog.getOpenFileName(self, "Open File", home_dir,
                                                    "RIS Files (*.ris)")
        if file_name != '':
            contend = codecs.open(file_name, 'r', encoding='utf-8').read()
            home_dir = str(Path.home())
            tarname1 = "Documents"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.makedirs(fulldir1)
            tarname2 = 'Obsidien'
            fulldir2 = os.path.join(fulldir1, tarname2)
            if not os.path.exists(fulldir2):
                os.makedirs(fulldir2)
            tarname3 = 'Database'
            fulldir3 = os.path.join(fulldir2, tarname3)
            if not os.path.exists(fulldir3):
                os.makedirs(fulldir3)
            tarnamea = 'RIS'
            fulldira = os.path.join(fulldir3, tarnamea)
            if not os.path.exists(fulldira):
                os.makedirs(fulldira)

            contend = contend.replace(';;', '\n')

            regex = r"^((?!\s\s-\s).)+$"
            subst = "KW  - \\g<0>"
            newdata = re.sub(regex, subst, contend, 0, re.MULTILINE)
            newdata = newdata.replace('\r', '')
            newdata = newdata.replace('KW  - \n', '\n')

            ris_list = newdata.split('\n\n')
            while '' in ris_list:
                ris_list.remove('')
            i = 0
            while i >= 0 and i <= len(ris_list) - 1:
                pattern0 = re.compile(r'ST  - (.*?)\n')
                result0 = pattern0.findall(ris_list[i])
                title = ''.join(result0)
                tarnameb = 'Untitled.md'
                fulldirb = os.path.join(fulldira, tarnameb)
                if title != '':
                    tarnameb = self.cleaninput(str(title).replace('ST  - ', '')) + '.md'
                    fulldirb = os.path.join(fulldira, tarnameb)
                    with open(fulldirb, 'a', encoding='utf-8') as f2:
                        f2.write('')
                if title == '':
                    pattern02 = re.compile(r'TI  - (.*?)\n')
                    result0 = pattern02.findall(ris_list[i])
                    title2 = ''.join(result0)
                    if title2 == '':
                        pattern03 = re.compile(r'T1  - (.*?)\n')
                        result0 = pattern03.findall(ris_list[i])
                        title2 = ''.join(result0)
                    if title2 != '':
                        tarnameb = self.cleaninput(str(title2).replace('TI  - ', '').replace('T1  - ', '')) + '.md'
                        fulldirb = os.path.join(fulldira, tarnameb)
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write('')

                ris_each = ris_list[i].split('\n')
                for m in range(len(ris_each)):
                    if 'ST  - ' in ris_each[m]:
                        part1 = '# Metadata\n- Title: ' + self.cleaninput(str(ris_each[m]).replace('ST  - ', ''))
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + '\n')
                    if 'ST  - ' not in ris_list[i] and 'TI  - ' in ris_each[m]:
                        part1 = '# Metadata\n- Title: ' + self.cleaninput(str(ris_each[m]).replace('TI  - ', ''))
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + '\n')
                    if 'ST  - ' not in ris_list[i] and 'TI  - ' not in ris_list[i] and 'T1  - ' in ris_each[m]:
                        part1 = '# Metadata\n- Title: ' + self.cleaninput(str(ris_each[m]).replace('T1  - ', ''))
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part1 + '\n')
                for n in range(len(ris_each)):
                    if 'AU  - ' in ris_each[n]:
                        part2 = '\n- Authors: ' + str(ris_each[n]).replace('AU  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part2 + '\n')
                for o in range(len(ris_each)):
                    if 'AD  - ' in ris_each[o]:
                        part3 = '\n- Institutes: ' + str(ris_each[o]).replace('AD  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part3)
                for pp in range(len(ris_each)):
                    if 'T2  - ' in ris_each[pp]:
                        part4 = '\n- Publication: ' + str(ris_each[pp]).replace('T2  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part4 + '\n')
                    if 'T2  - ' not in ris_list[i] and 'JF  - ' in ris_each[pp]:
                        part4 = '\n- Publication: ' + str(ris_each[pp]).replace('JF  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part4 + '\n')
                    if 'T2  - ' not in ris_list[i] and 'JF  - ' not in ris_list[i] and 'JO  - ' in ris_each[pp]:
                        part4 = '\n- Publication: ' + str(ris_each[pp]).replace('JO  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part4 + '\n')
                    if 'T2  - ' not in ris_list[i] and 'JF  - ' not in ris_list[i] and 'JO  - ' not in ris_list[i] and 'PB  - ' in ris_each[pp]:
                        part4 = '\n- Publication: ' + str(ris_each[pp]).replace('PB  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part4 + '\n')
                for q in range(len(ris_each)):
                    if 'SP  - ' in ris_each[q]:
                        part5 = '\n- Page range: ' + str(ris_each[q]).replace('SP  - ', '')
                        if 'EP  - ' not in ris_list[i]:
                            with open(fulldirb, 'a', encoding='utf-8') as f2:
                                f2.write(part5 + '\n')
                        if 'EP  - ' in ris_list[i]:
                            with open(fulldirb, 'a', encoding='utf-8') as f2:
                                f2.write(part5)
                for qr in range(len(ris_each)):
                    if 'EP  - ' in ris_each[qr]:
                        part5 = '-' + str(ris_each[qr]).replace('EP  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part5 + '\n')
                for r in range(len(ris_each)):
                    if 'PY  - ' in ris_each[r]:
                        part6 = '\n- Year: #AD' + str(ris_each[r]).replace('PY  - ', '').replace('/', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part6 + '\n')
                for r_doi in range(len(ris_each)):
                    if 'DO  - ' in ris_each[r_doi]:
                        part6_6 = '\n- DOI: ' + str(ris_each[r_doi]).replace('DO  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part6_6 + '\n')
                for r_isbn in range(len(ris_each)):
                    if 'SN  - ' in ris_each[r_isbn]:
                        part6_7 = '\n- ISBN: ' + str(ris_each[r_isbn]).replace('SN  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part6_7 + '\n')
                for s in range(len(ris_each)):
                    if 'VL  - ' in ris_each[s]:
                        part8 = '\n- Vol / Mon: ' + str(ris_each[s]).replace('VL  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part8 + '\n')
                for t in range(len(ris_each)):
                    if 'IS  - ' in ris_each[t]:
                        part9 = '\n- Vol / Mon: (' + str(ris_each[t]).replace('IS  - ', '') + ')'
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part9 + '\n')
                for u in range(len(ris_each)):
                    if 'KW  - ' in ris_each[u]:
                        part10 = '\n- Tags: #' + str(ris_each[u]).replace('KW  - ', '')
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part10)
                for v in range(len(ris_each)):
                    if 'AB  - ' in ris_each[v]:
                        part11 = '\n- Abstract: ' + str(ris_each[v]).replace('AB  - ', '') + ')'
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part11)
                if fulldirb != '':
                    half_scr = codecs.open(fulldirb, 'r', encoding='utf-8').read()
                    pattern = re.compile(r'Title: (.*?)\n')
                    result = pattern.findall(half_scr)
                    result = ''.join(result)
                    pretc = result.replace('Title: ', '')
                    pretc = pretc.replace('\n', '')
                    pretc = pretc.replace('[', '')
                    pretc = pretc.replace(']', '')

                    pattern2 = re.compile(r'Authors: (.*?)\n')
                    result2 = pattern2.findall(half_scr)
                    result2 = '、'.join(result2)
                    pretc2 = result2.replace('Authors: ', '')
                    pretc2 = pretc2.replace('\n', '')
                    pretc2 = pretc2.replace('[', '')
                    pretc2 = pretc2.replace(']', '')

                    pattern4 = re.compile(r'Publication: (.*?)\n')
                    result4 = pattern4.findall(half_scr)
                    result4 = ''.join(result4)
                    pretc4 = result4.replace('Publication: ', '')
                    pretc4 = pretc4.replace('\n', '')
                    pretc4 = pretc4.replace('[', '')
                    pretc4 = pretc4.replace(']', '')

                    pattern6 = re.compile(r'Year: (.*?)\n')
                    result6 = pattern6.findall(half_scr)
                    result6 = ''.join(result6)
                    pretc6 = result6.replace('Year: ', '')
                    pretc6 = pretc6.replace('\n', '')
                    pretc6 = pretc6.replace('#AD', '')

                    pattern7 = re.compile(r'Vol / Mon: (.*?)\n')
                    result7 = pattern7.findall(half_scr)
                    result7 = ''.join(result7)
                    pretc7 = result7.replace('Vol / Mon: ', '')

                    pattern11 = re.compile(r'Page range: (.*?)\n')
                    result11 = pattern11.findall(half_scr)
                    result11 = ''.join(result11)
                    pretc11 = result11.replace('Page range: ', '')
                    pretc11 = pretc11.replace('\n', '')

                    if self.is_contain_chinese(pretc):
                        part12 = '\n- ' + 'Citation: ' + str(pretc2) + '：《' + str(pretc) + '》，载《' + \
                                  str(pretc4) + '》，' + str(pretc6) + ' 年第 ' + \
                                  str(pretc7) + ' 期，第 ' + str(pretc11) + ' 页。'
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part12)
                    if self.is_contain_english(pretc):
                        part13 = '\n- ' + 'Citation: ' + str(pretc2).replace('+', '、').replace('、', ', ') + ', “' + str(pretc) + ',” *' + \
                            str(pretc4) + '*, ' + str(pretc7) + ', ' + str(pretc6) + ', pp.' + \
                            str(pretc11) + '.'
                        with open(fulldirb, 'a', encoding='utf-8') as f2:
                            f2.write(part13)

                    remove2n = codecs.open(fulldirb, 'r', encoding='utf-8').read()
                    rem = remove2n.replace('\n\n', '\n')
                    with open(fulldirb, 'w', encoding='utf-8') as f2:
                        f2.write(rem)

                    partrispls = '\n\n---' + '\n\n# Notes'
                    with open(fulldirb, 'a', encoding='utf-8') as f2:
                        f2.write(partrispls)
                i = i + 1
                continue

    def is_contain_english(self, str0):  # 判断是否包含英文字母
        import re
        return bool(re.search('[a-zA-Zａ-ｚＡ-Ｚ]', str0))

    def is_contain_chinese(self, check_str):  # 判断是否包含中文字
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def moveris(self):
        home_dir = str(Path.home())
        tarname11 = "Documents"
        fulldir11 = os.path.join(home_dir, tarname11)
        if not os.path.exists(fulldir11):
            os.makedirs(fulldir11)
        tarname22 = 'Obsidien'
        fulldir22 = os.path.join(fulldir11, tarname22)
        if not os.path.exists(fulldir22):
            os.makedirs(fulldir22)
        tarname33 = 'Database'
        fulldir33 = os.path.join(fulldir22, tarname33)
        if not os.path.exists(fulldir33):
            os.makedirs(fulldir33)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir33, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        file_name, ok = QFileDialog.getOpenFileName(self, "Open File", fulldira, "Markdown Files (*.md)")
        if file_name != '' and fulldira in file_name:
            contend = codecs.open(file_name, 'r', encoding='utf-8').read()

            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            pattern = re.compile(r'Title: (.*?)\n')
            result = pattern.findall(contend)
            result = ''.join(result)
            pretc = result.replace('Title: ', '')
            pretc = pretc.replace('\n', '')
            pretc = pretc.replace('[', '')
            pretc = pretc.replace(']', '')
            tarnameb = pretc + '.md'
            fulldirb = os.path.join(path1, tarnameb)
            if pretc != '':
                with open(fulldirb, 'a', encoding='utf-8') as rism:
                    rism.write(contend)

            pattern = re.compile(r'Title: (.*?)\n')
            result = pattern.findall(contend)
            result = ''.join(result)
            pretc = result.replace('Title: ', '')
            pretc = pretc.replace('\n', '')
            pretc = pretc.replace('[', '')
            pretc = pretc.replace(']', '')
            if '|' in pretc:
                pass
                patt = re.compile(r'\|(.*?)\]')
                res2 = patt.findall(result)
                res2 = ''.join(res2)
                self.le1.setText(res2)
            else:
                self.le1.setText(pretc)

            pattern2 = re.compile(r'Authors: (.*?)\n')
            result2 = pattern2.findall(contend)
            result2 = '、'.join(result2)
            pretc2 = result2.replace('Authors: ', '')
            pretc2 = pretc2.replace('\n', '')
            pretc2 = pretc2.replace('[', '')
            pretc2 = pretc2.replace(']', '')
            self.le2.setText(pretc2)

            pattern3 = re.compile(r'Institutes: (.*?)\n')
            result3 = pattern3.findall(contend)
            result3 = '、'.join(result3)
            pretc3 = result3.replace('Institutes: ', '')
            pretc3 = pretc3.replace('\n', '')
            pretc3 = pretc3.replace('[', '')
            pretc3 = pretc3.replace(']', '')
            self.le7.setText(pretc3)

            pattern4 = re.compile(r'Publication: (.*?)\n')
            result4 = pattern4.findall(contend)
            result4 = ''.join(result4)
            pretc4 = result4.replace('Publication: ', '')
            pretc4 = pretc4.replace('\n', '')
            pretc4 = pretc4.replace('[', '')
            pretc4 = pretc4.replace(']', '')
            self.le3.setText(pretc4)

            pattern5 = re.compile(r'Press: (.*?)\n')
            result5 = pattern5.findall(contend)
            result5 = ''.join(result5)
            pretc5 = result5.replace('Press: ', '')
            pretc5 = pretc5.replace('\n', '')
            pretc5 = pretc5.replace('[', '')
            pretc5 = pretc5.replace(']', '')
            self.le3_1.setText(pretc5)

            pattern6 = re.compile(r'Year: (.*?)\n')
            result6 = pattern6.findall(contend)
            result6 = ''.join(result6)
            pretc6 = result6.replace('Year: ', '')
            pretc6 = pretc6.replace('\n', '')
            pretc6 = pretc6.replace('#AD', '')
            self.le4.setText(pretc6)

            pattern7 = re.compile(r'Vol / Mon: (.*?)\n')
            result7 = pattern7.findall(contend)
            result7 = ''.join(result7)
            pretc7 = result7.replace('Vol / Mon: ', '')
            pretc7 = pretc7.replace('\n', '')
            self.le4_1.setText(pretc7)

            pattern8 = re.compile(r'Tags: (.*?)\n')
            result8 = pattern8.findall(contend)
            result8 = '、'.join(result8)
            pretc8 = result8.replace('Tags: ', '')
            pretc8 = pretc8.replace('\n', '')
            pretc8 = pretc8.replace('#', '')
            pretc8 = pretc8.replace(' ', '、')
            pretc8 = pretc8.replace('[', '')
            pretc8 = pretc8.replace(']', '')
            self.le5.setText(pretc8)

            pattern9 = re.compile(r'From book: (.*?),')
            result9 = pattern9.findall(contend)
            result9 = ''.join(result9)
            pretc9 = result9.replace('From book: ', '')
            pretc9 = pretc9.replace(',', '')
            pretc9 = pretc9.replace('[', '')
            pretc9 = pretc9.replace(']', '')
            self.le8.setText(pretc9)

            pattern10 = re.compile(r'Chapter (.*?),')
            result10 = pattern10.findall(contend)
            result10 = ''.join(result10)
            pretc10 = result10.replace(', Chapter ', '')
            pretc10 = pretc10.replace(',', '')
            pretc10 = pretc10.replace('[', '')
            pretc10 = pretc10.replace(']', '')
            self.le9.setText(pretc10)

            pattern11 = re.compile(r'Page range: (.*?)\n')
            result11 = pattern11.findall(contend)
            result11 = ''.join(result11)
            pretc11 = result11.replace(', Page range: ', '')
            pretc11 = pretc11.replace('\n', '')
            self.le10.setText(pretc11)

            if self.le1.text() != '':
                self.text.setPlainText(contend)
                self.widget0.clear()
                self.widget0.addItems(['Append at the end (default)', 'Append at the current cursor'])
                path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                pattern = re.compile(r'## (.*?)\n')
                result = pattern.findall(maintxt)
                if result != []:
                    result = '☆'.join(result)
                    result = result.replace('#', '')
                    result = result.replace('# ', '')
                    result = result.replace('Q/P: ', '')
                    result = result.split('☆')
                    for i in range(len(result)):
                        result[i] = 'After ' + result[i]
                        result[i] = ''.join(result[i])
                    self.widget0.addItems(result)
                self.widget0.setCurrentIndex(0)

                with open(BasePath + 'path_ttl.txt', 'w', encoding='utf-8') as f0:
                    f0.write(pretc)

                os.remove(fulldir1)
                os.remove(file_name)

    def webconmode_on(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'Conference'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        self.read_t3.setVisible(False)
        self.read_t8.setVisible(False)
        self.web_t3.setVisible(True)
        self.web_t8.setVisible(True)
        self.speaker.setVisible(True)
        self.btn_t9.setStyleSheet('''
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF''')
        self.btn_t9.setText('Turned on!')
        self.lblread_2.setText('Authors/Speakers:')

    def webconmode_off(self):
        self.read_t3.setVisible(True)
        self.read_t8.setVisible(True)
        self.web_t3.setVisible(False)
        self.web_t8.setVisible(False)
        self.speaker.setVisible(False)
        self.btn_t9.setStyleSheet('''
            border: 1px outset grey;
            background-color: #FFFFFF;
            border-radius: 4px;
            padding: 1px;
            color: #000000''')
        self.btn_t9.setText('Turn on!')
        self.leweb3.clear()
        self.leweb8.clear()
        self.leweb9.clear()
        self.leweb10.clear()
        self.lblread_2.setText('Authors:')

    def showlist(self):
        a = True
        a2 = False
        self.btnx4.setStyleSheet('''
            QPushButton{
            border: transparent;
            background-color: transparent;
            border-image: url(/Applications/Strawberry.app/Contents/Resources/up.png);
            }
            QPushButton:pressed{
            border: 1px outset grey;
            background-color: #0085FF;
            border-radius: 4px;
            padding: 1px;
            color: #FFFFFF
            }
            ''')
        if not self.read_t1.isVisible():
            a = True
        if self.read_t1.isVisible():
            a = False
            self.btnx4.setStyleSheet('''
                QPushButton{
                border: transparent;
                background-color: transparent;
                border-image: url(/Applications/Strawberry.app/Contents/Resources/down.png);
                }
                QPushButton:pressed{
                border: 1px outset grey;
                background-color: #0085FF;
                border-radius: 4px;
                padding: 1px;
                color: #FFFFFF
                }
                ''')
        self.read_t1.setVisible(a)
        self.read_t2.setVisible(a)
        self.read_t7.setVisible(a)
        self.read_t3.setVisible(a)
        self.read_t8.setVisible(a)
        self.read_t4.setVisible(a)
        self.read_t4_doi.setVisible(a)
        self.read_t4_isbn.setVisible(a)
        self.read_t5.setVisible(a)
        self.lbltool06.setVisible(a)
        self.tool8.setVisible(a)
        if self.btn_t9.text() == 'Turned on!':
            self.web_t3.setVisible(a)
            self.web_t8.setVisible(a)
            self.read_t3.setVisible(a2)
            self.read_t8.setVisible(a2)

    def openascr(self):
        self.btn_ia1.setEnabled(False)
        w4.csl_open_btn.setEnabled(False)
        w4.csl_add_btn.setEnabled(False)
        w4.csl_delete_btn.setVisible(False)
        self.widgettem.setCurrentIndex(0)
        pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if pathscr == '':
            self.textii2.setPlainText('Please check your path settings!')
        if pathscr != '':
            # file_name, ok = QFileDialog.getOpenFileName(self, "Open File", pathscr, "Markdown Files (*.md);;LaTeX Files (*.tex)")
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", pathscr, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                def _strip_tail(name):
                    import re as _re
                    return _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', name.strip())

                if pathscr in file_name:
                    if '.md' in file_name:
                        patterna = re.compile(r'\[.*<e>\n')
                        resultp = patterna.findall(contend)
                        resultp = ''.join(resultp)
                        resultp = resultp.rstrip('\n')
                        resultp = resultp.replace('<e>', '')
                        resultp = resultp.replace('<e>\n<e>', '')
                        resultp = resultp.replace('<e><e>', '')
                        with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as fp:
                            fp.write(resultp)

                        pattern = re.compile(r'<!--Title: (.*?)-->')
                        result = pattern.findall(contend)
                        result = ''.join(result)
                        pretc = result.replace('<!--Title: ', '')
                        pretc = pretc.replace('-->', '')
                        pretc = pretc.replace('[', '')
                        pretc = pretc.replace(']', '')
                        title_full = pretc.strip()
                        file_base = os.path.splitext(os.path.basename(file_name))[0]
                        title_base = _strip_tail(title_full)
                        file_base_clean = _strip_tail(file_base)
                        # use filename (cleaned) for leii1; cache full header (if any)
                        chosen_base = file_base_clean if file_base_clean != '' else (title_base if title_base != '' else file_base)
                        cache_key = title_full if title_full != '' else file_base
                        self._cached_title_key = cache_key
                        self.leii1.setText(chosen_base)
                        # verify citation folder exists
                        cit_dir = os.path.join(pathscr, 'StrawberryCitations', cache_key)
                        if not os.path.exists(cit_dir):
                            QMessageBox.warning(self, 'Citation formats unavailable',
                                                'Current file lacks a matching StrawberryCitations folder. '
                                                'Automatic citation generation is unavailable. Please recreate the file.')
                            self._set_citation_controls_enabled(False)
                        else:
                            self._set_citation_controls_enabled(True)
                            # Generate missing formats if new CSLs were added
                            try:
                                home_dir = str(Path.home())
                                base_dir = os.path.join(home_dir, "StrawberryAppPath")
                                csl_dir = os.path.join(base_dir, "CitationFormat")
                                formats_file = os.path.join(csl_dir, "formats.txt")
                                fmt_list = []
                                if os.path.exists(formats_file):
                                    fmt_list = [x.strip() for x in codecs.open(formats_file, 'r', encoding='utf-8').read().split('\n') if x.strip() != '' and x.strip().lower() != 'quickcite']
                                existing = set()
                                for fname in os.listdir(cit_dir):
                                    if fname.startswith(f"{cache_key}-") and fname.endswith('.txt'):
                                        name_part = fname[len(cache_key)+1:-4]  # strip title and .txt
                                        if name_part.endswith('-in'):
                                            name_part = name_part[:-3]
                                        existing.add(name_part.lower())
                                missing_formats = []
                                for fmt in fmt_list:
                                    basefmt = fmt[:-4] if fmt.lower().endswith('.csl') else fmt
                                    if basefmt.lower() not in existing:
                                        missing_formats.append(basefmt)
                                if missing_formats:
                                    bib_file = os.path.join(cit_dir, f"{cache_key}.bib")
                                    if os.path.exists(bib_file):
                                        # try:
                                        #     import bibtexparser
                                        #     from bibtexparser.bparser import BibTexParser
                                        #     from bibtexparser.customization import convert_to_unicode
                                        #     from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
                                        #     from citeproc import formatter
                                        #     from citeproc.source.json import CiteProcJSON
                                        # except Exception:
                                        #     missing_formats = []
                                        if missing_formats:
                                            parser = BibTexParser(common_strings=True)
                                            parser.customization = convert_to_unicode
                                            try:
                                                with open(bib_file, 'r', encoding='utf-8') as bf:
                                                    bib_db = bibtexparser.load(bf, parser=parser)
                                                    entries = bib_db.entries
                                            except Exception:
                                                entries = []
                                            def _append_line(path, text):
                                                if text is None or text.strip() == '':
                                                    return
                                                os.makedirs(os.path.dirname(path), exist_ok=True)
                                                needs_newline = os.path.exists(path) and os.path.getsize(path) > 0
                                                with open(path, 'a', encoding='utf-8') as f0:
                                                    if needs_newline:
                                                        f0.write('\n')
                                                    f0.write(text.strip())
                                            for fmt in missing_formats:
                                                style_path = os.path.join(csl_dir, fmt if fmt.endswith('.csl') else f"{fmt}.csl")
                                                if not os.path.exists(style_path):
                                                    continue
                                                for entry in entries:
                                                    try:
                                                        csl_item = self._convert_entry_to_csl(entry)
                                                        style = CitationStylesStyle(style_path, validate=False)
                                                        bib_source = CiteProcJSON([csl_item])
                                                        bibliography = CitationStylesBibliography(style, bib_source, formatter.plain)
                                                        citation = Citation([CitationItem(csl_item['id'])])
                                                        bibliography.register(citation)
                                                        inline_cite = str(bibliography.cite(citation, lambda x: None))
                                                        biblio_entries = [str(item) for item in bibliography.bibliography()]
                                                        biblio_text = '\n'.join(biblio_entries).strip()
                                                    except Exception:
                                                        continue
                                                    inline_file = os.path.join(cit_dir, f"{cache_key}-{fmt}-in.txt")
                                                    biblio_file = os.path.join(cit_dir, f"{cache_key}-{fmt}.txt")
                                                    _append_line(inline_file, inline_cite)
                                                    _append_line(biblio_file, biblio_text)
                            except Exception:
                                pass
                            # remove obsolete formats not in formats.txt (except quickcite)
                            try:
                                allowed = set([ (f[:-4] if f.lower().endswith('.csl') else f).lower() for f in fmt_list ])
                                allowed.add('quickcite')
                                for fname in list(os.listdir(cit_dir)):
                                    if not fname.startswith(f"{cache_key}-") or not fname.endswith('.txt'):
                                        continue
                                    name_part = fname[len(cache_key)+1:-4]
                                    fmt_key = name_part.lower().replace('-in', '')
                                    if fmt_key not in allowed:
                                        try:
                                            os.remove(os.path.join(cit_dir, fname))
                                        except Exception:
                                            continue
                            except Exception:
                                pass

                        if self.leii1.text() != '':
                            self._show_inspiration_content(contend)
                            self.btn_a.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #0085FF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #FFFFFF''')
                            self.btn_a.setText('Created')
                            self.leii1.setEnabled(False)
                            with open(BasePath + 'path_ste.txt', 'w', encoding='utf-8') as f0:
                                f0.write(self.leii1.text())
                        if self.leii1.text() == '':
                            self.textii2.setPlainText('Not a standard file produced by Strawberry. \nCan not find title within.')

                        oldref = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
                        pretc7 = '0'
                        if oldref != '':
                            pattern7 = re.compile(r'\[.\d*\]')
                            result7 = pattern7.findall(oldref)
                            i = 0
                            while i >= 0 and i <= len(result7) - 1:
                                result7[i] = result7[i].replace('[^', '')
                                result7[i] = result7[i].replace(']', '')
                                result7[i] = ''.join(result7[i])
                                i = i + 1
                                continue
                            result7.sort(key=int, reverse=True)
                            pretc7 = str(result7[0])
                        if oldref == '':
                            pretc7 = '0'
                        promptnum = str(int(pretc7) + 1)
                        self.leii2.setPlaceholderText(promptnum)

                        if action7.isChecked():
                            full_md = ''
                            path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                            if path_scr != '' and self.leii1.text() != '':
                                tarname = str(self.leii1.text()) + ".md"
                                fulldir = os.path.join(path_scr, tarname)
                                if os.path.exists(fulldir):
                                    full_md = codecs.open(fulldir, 'r', encoding='utf-8').read()
                            if full_md == '':
                                head_md = self._build_inspiration_header()
                                body_md = self.textii2.toPlainText().rstrip('\n')
                                foot_md = self._build_inspiration_references()
                                full_md = head_md + '\n' + body_md + foot_md
                            newhtml = self.md2html(full_md)
                            self.real2.setHtml(newhtml)
                    # if '.tex' in file_name:
                    #     patterna = re.compile(r'title\{.*}')
                    #     resultq = patterna.findall(contend)
                    #     resultq = ''.join(resultq)
                    #     resultq = resultq.replace('title{', '')
                    #     resultq = resultq.replace('}', '')
                    #     resultq = resultq.replace('[', '')
                    #     resultq = resultq.replace(']', '')
                    #     self.leii1.setText(resultq)

                    #     if self.leii1.text() != '':
                    #         self.textii3.setPlainText(contend)
                    #         self.btn_a.setStyleSheet('''
                    #                         border: 1px outset grey;
                    #                         background-color: #0085FF;
                    #                         border-radius: 4px;
                    #                         padding: 1px;
                    #                         color: #FFFFFF''')
                    #         self.btn_a.setText('Created')
                    #         self.leii1.setEnabled(False)
                    #         with open(BasePath + 'path_std.txt', 'w', encoding='utf-8') as f0:
                    #             f0.write(self.leii1.text())
                    #     if self.leii1.text() == '':
                    #         self.textii3.setPlainText('Not a standard file produced by Strawberry. \nCan not find title within.')
                    if self.leii1.text() != '':
                        self.choosepart.clear()
                        self.choosepart.addItems(['Append at the end (default)', 'Append at the current cursor'])
                        pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                        def _candidate_names(raw):
                            cands = [raw]
                            try:
                                import re as _re
                                base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                                if base1 and base1 not in cands:
                                    cands.append(base1)
                                base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                                if base2 and base2 not in cands:
                                    cands.append(base2)
                            except Exception:
                                pass
                            return cands

                        fulldir1 = ''
                        for nm in _candidate_names(str(self.leii1.text())):
                            tarname1 = nm + ".md"
                            candidate = os.path.join(pathscr, tarname1)
                            if os.path.exists(candidate):
                                fulldir1 = candidate
                                break
                        if fulldir1 == '' and pathscr in file_name:
                            fulldir1 = file_name
                        if fulldir1 == '':
                            tarname1 = str(self.leii1.text()) + ".md"
                            fulldir1 = os.path.join(pathscr, tarname1)
                        maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                        pattern = re.compile(r'## (.*?)\n')
                        result = pattern.findall(maintxt)
                        if result != []:
                            result = '☆'.join(result)
                            result = result.replace('#', '')
                            result = result.replace('# ', '')
                            result = result.replace('Q/P: ', '')
                            result = result.split('☆')
                            if 'References ' in result:
                                result.remove('References ')
                            for i in range(len(result)):
                                result[i] = 'After ' + result[i]
                                result[i] = ''.join(result[i])
                            self.choosepart.addItems(result)
                if pathscr not in file_name:
                    self.textii2.setPlainText('The file is not under your script path.')
                    self.leii1.clear()

    def createscr(self):
        if self.btn_a.text() != 'Created' and self.leii1.text() != '':
            path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname4 = str(self.leii1.text()) + ".md"
                fulldir4 = os.path.join(path3, tarname4)
                if os.path.exists(fulldir4):
                    QMessageBox.warning(self, 'Duplicate title', 'A file with this title already exists. Please choose a new name.')
                    return
                ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                parta = '<document-start>'
                partb = '\n<!--Title: ' + str(self.leii1.text()) + ' ' + ts + '-->'
                partc = '\n\n# ' + str(self.leii1.text())
                with open(fulldir4, 'a', encoding='utf-8') as f3:
                    f3.write(parta + partb + partc)
                self._init_citation_files(str(self.leii1.text()) + ' ' + ts, path3)
                self.btn_a.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_a.setText('Created')
                self.leii1.setEnabled(False)
                with open(BasePath + 'path_ste.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.leii1.text())

            with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as citpat:
                citpat.write('')

            pathend = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.leii1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self._show_inspiration_content(contend)
                self.textii2.ensureCursorVisible()  # 游标可用
                cursor = self.textii2.textCursor()  # 设置游标
                pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.textii2.setTextCursor(cursor)  # 滚动到游标位置

    def addinssc(self):
        poslast = 0
        path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path3 == '':
            self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname4 = 'blank'
            if self.leii1.text() != '':
                tarname4 = str(self.leii1.text()) + ".md"
            if self.leii1.text() == '' and self.textii1.toPlainText() != '':
                # default new doc name with "record"
                ISOTIMEFORMAT = '%Y%m%d %H-%M-%S-%f'
                theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                base_name = f"{theTime} record"
                tarname4 = base_name + ".md"
                self.leii1.setText(base_name)
                self.leii1.setEnabled(False)
                self.btn_a.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
                self.btn_a.setText('Created')
            if self.leii1.text() != '':
                def _candidate_names(raw):
                    cands = [raw]
                    try:
                        import re as _re
                        base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                        if base1 and base1 not in cands:
                            cands.append(base1)
                        base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                        if base2 and base2 not in cands:
                            cands.append(base2)
                    except Exception:
                        pass
                    return cands

                fulldir4 = ''
                tarname4_use = ''
                for nm in _candidate_names(str(self.leii1.text())):
                    cand = os.path.join(path3, nm + ".md")
                    if os.path.exists(cand):
                        fulldir4 = cand
                        tarname4_use = nm + ".md"
                        # sync title to stripped version if matched stripped one
                        self.leii1.setText(nm)
                        break
                if fulldir4 == '':
                    tarname4_use = tarname4
                    fulldir4 = os.path.join(path3, tarname4_use)
                    if os.path.exists(fulldir4):
                        QMessageBox.warning(self, 'Duplicate title', 'A file with this title already exists. Please choose a new name.')
                        return
                is_new_file = not os.path.exists(fulldir4)
                with open(fulldir4, 'a', encoding='utf-8') as f0:
                    f0.write('')
                if is_new_file:
                    try:
                        header_preview = self._build_inspiration_header()
                        m_title = re.search(r'<!--Title: (.*?)-->', header_preview)
                        title_key = m_title.group(1).strip() if m_title else self.leii1.text()
                    except Exception:
                        title_key = self.leii1.text()
                    self._init_citation_files(title_key, path3)
                contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                body_now = self._strip_inspiration_body(contm).rstrip('\n')
                if body_now.strip() == '':
                    body_now = '# ' + str(self.leii1.text())
                partnotes = ''
                if self.leiinote.text() != '':
                    partnotes = ' [' +self.leiinote.text() + ']'
                insertion = ''
                if self.textii1.toPlainText() != '':
                    insertion = '\n\n' + str(self.default_clean(self.textii1.toPlainText())) + partnotes
                tail = codecs.open(BasePath + 'path_pat.txt', 'r', encoding='utf-8').read()
                tail_body = self._strip_inspiration_body(tail).rstrip('\n')
                tail_cursor = codecs.open(BasePath + 'currentcursor2.txt', 'r', encoding='utf-8').read()
                idx = self.choosepart.currentIndex()
                last = self.choosepart.count() - 1
                if idx == 1:
                    # Prefer the tail captured into currentcursor2 (manual cursor); fall back to cite_position_idx
                    insert_pos = None
                    if tail_cursor != '' and len(tail_cursor) <= len(body_now):
                        # If the saved tail is still present, place insertion right before it
                        if body_now.endswith(tail_cursor):
                            insert_pos = len(body_now) - len(tail_cursor)
                        else:
                            candidate = body_now.rfind(tail_cursor)
                            if candidate != -1:
                                insert_pos = candidate
                    if insert_pos is None:
                        try:
                            pos_str = codecs.open(BasePath + 'cite_position_idx.txt', 'r', encoding='utf-8').read().strip()
                            insert_pos = int(pos_str) if pos_str != '' else len(body_now)
                        except Exception:
                            insert_pos = len(body_now)
                    insert_pos = max(0, min(len(body_now), insert_pos))
                    suffix = body_now[insert_pos:]
                    with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                        f0.write(suffix)
                    self._suppress_cursor_capture = True
                    try:
                        new_body = body_now[:insert_pos] + insertion + suffix
                        new_cursor_pos = insert_pos + len(insertion)
                    finally:
                        self._suppress_cursor_capture = False
                elif idx == 0 or idx == last:
                    new_body = body_now + insertion
                else:
                    # For "After <section>" options, match against stripped body
                    if tail_body != '' and tail_body in body_now:
                        insert_block = insertion.rstrip('\n').lstrip('\n')
                        if insert_block != '' and not insert_block.endswith('\n\n'):
                            insert_block = insert_block.rstrip('\n').lstrip('\n') + '\n\n'
                        new_body = body_now.replace(tail_body, insert_block + tail_body, 1)
                    else:
                        new_body = body_now + insertion
                if idx == 0 or idx == last:
                    new_body = new_body.rstrip('\n')
                prev_suppress = getattr(self, '_suppress_cursor_capture', False)
                self._suppress_cursor_capture = True
                try:
                    self._write_inspiration_body(new_body)
                    if idx == 1:
                        # Keep cursor at the new insertion point to support consecutive inserts
                        body_len = len(self.textii2.toPlainText())
                        new_cursor_pos = max(0, min(body_len, new_cursor_pos))
                        cursor = self.textii2.textCursor()
                        cursor.setPosition(new_cursor_pos)
                        self.textii2.setTextCursor(cursor)
                        with open(BasePath + 'cite_position_idx.txt', 'w', encoding='utf-8') as f0:
                            f0.write(str(new_cursor_pos))
                        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                            f0.write(self.textii2.toPlainText()[new_cursor_pos:])
                finally:
                    self._suppress_cursor_capture = prev_suppress

                itemold = self.choosepart.currentText()
                self.choosepart.clear()
                self.choosepart.addItems(['Append at the end (default)', 'Append at the current cursor'])
                pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.leii1.text()) + ".md"
                fulldir1 = os.path.join(pathscr, tarname1)
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                pattern = re.compile(r'## (.*?)\n')
                result = pattern.findall(maintxt)
                result2 = '☆'.join(result)
                if result != []:
                    result = result2.replace('#', '')
                    result = result.replace('# ', '')
                    result = result.replace('Q/P: ', '')
                    result = result.split('☆')
                    if 'References ' in result:
                        result.remove('References ')
                    for i in range(len(result)):
                        result[i] = 'After ' + result[i]
                        result[i] = ''.join(result[i])
                    self.choosepart.addItems(result)
                    if itemold in result:
                        itemnub = result.index(itemold) + 2
                        self.choosepart.setCurrentIndex(itemnub)
                    if itemold not in result and itemold != 'Append at the current cursor':
                        self.choosepart.setCurrentIndex(0)
                if itemold == 'Append at the current cursor':
                    self.choosepart.setCurrentIndex(1)

                pathend = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                if pathend == '':
                    self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
                else:
                    tarnameend = str(self.leii1.text()) + ".md"
                    fulldirend = os.path.join(pathend, tarnameend)
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    if self.choosepart.currentIndex() == 1:
                        keepsave = codecs.open(BasePath + 'currentcursor2.txt', 'r', encoding='utf-8').read()
                        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                            f0.write(keepsave)
                    posnu = codecs.open(BasePath + 'path_pat.txt', 'r', encoding='utf-8').read()
                    self._show_inspiration_content(contend)
                    self.textii2.ensureCursorVisible()  # 游标可用
                    cursor = self.textii2.textCursor()  # 设置游标
                    pos = len(self.textii2.toPlainText())
                    if posnu != '':
                        pos = len(self.textii2.toPlainText()) - len(posnu)  # 获取文本尾部的位置
                    if posnu == '':
                        pos = len(self.textii2.toPlainText()) - poslast
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.textii2.setTextCursor(cursor)  # 滚动到游标位置
                    if self.textii2.verticalScrollBar().maximum() != 0:
                        proportion = self.textii2.verticalScrollBar().value() / self.textii2.verticalScrollBar().maximum()
                        tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
                        self.real2.verticalScrollBar().setValue(tar_pro)

                self.textii1.clear()
            
            if action7.isChecked():
                full_md = ''
                path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                if path_scr != '' and self.leii1.text() != '':
                    tarname = str(self.leii1.text()) + ".md"
                    fulldir = os.path.join(path_scr, tarname)
                    if os.path.exists(fulldir):
                        full_md = codecs.open(fulldir, 'r', encoding='utf-8').read()
                if full_md == '':
                    head_md = self._build_inspiration_header()
                    body_md = self.textii2.toPlainText().rstrip('\n')
                    foot_md = self._build_inspiration_references()
                    full_md = head_md + '\n' + body_md + foot_md
                newhtml = self.md2html(full_md)
                self.real2.setHtml(newhtml)
                # set position
                QTimer.singleShot(100, self.scr_cha2)

    def addcit(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        home_dir = str(Path.home())
        tarname11 = "Documents"
        fulldir11 = os.path.join(home_dir, tarname11)
        if not os.path.exists(fulldir11):
            os.makedirs(fulldir11)
        tarname22 = 'Obsidien'
        fulldir22 = os.path.join(fulldir11, tarname22)
        if not os.path.exists(fulldir22):
            os.makedirs(fulldir22)
        tarname33 = 'Database'
        fulldir33 = os.path.join(fulldir22, tarname33)
        if not os.path.exists(fulldir33):
            os.makedirs(fulldir33)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir33, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if path1 != '' and self.leii1.text() != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path1, "Markdown Files (*.md)")
            if file_name != '' and (path1 in file_name or fulldira in file_name):
                try:
                    title_key = self._get_citation_title_key()
                    self._cached_title_key = title_key
                except Exception:
                    title_key = self.leii1.text()
                oldref = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
                pretc7 = '0'
                if oldref != '':
                    pattern7 = re.compile(r'\[.\d*\]')
                    result7 = pattern7.findall(oldref)
                    i = 0
                    while i >= 0 and i <= len(result7) - 1:
                        result7[i] = result7[i].replace('[^', '')
                        result7[i] = result7[i].replace(']', '')
                        result7[i] = ''.join(result7[i])
                        i = i + 1
                        continue
                    result7.sort(key=int, reverse=True)
                    pretc7 = str(result7[0])
                if oldref == '':
                    pretc7 = '0'
                copynum = '[^' + str(int(pretc7) + 1) + ']'
                promptnum = str(int(pretc7) + 2)
                self.leii2.setPlaceholderText(promptnum)
                ResultEnd = copynum.encode('utf-8').decode('utf-8', 'ignore')
                uid = os.getuid()
                env = os.environ.copy()
                env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
                p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
                p.communicate(input=ResultEnd.encode('utf-8'))

                path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.leii1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                current_text = self.textii2.toPlainText()
                try:
                    position_str = codecs.open(BasePath + 'cite_position_idx.txt', 'r', encoding='utf-8').read()
                    position_idx = int(position_str) if position_str.strip() != '' else None
                except Exception:
                    position_idx = None
                doc_len = len(current_text)
                if position_idx is None:
                    position_idx = doc_len
                position_idx = max(0, min(position_idx, doc_len))

                need_confirm = (doc_len == 0) or (position_idx == 0) or (position_idx == doc_len)
                if need_confirm:
                    reply = QMessageBox.question(
                        self,
                        'Add citation',
                        'No valid cursor position was detected, or the cursor was at the beginning/end.\n'
                        'Please click on the desired insertion point first before attempting.\n'
                        'Are you still inserting the citation at the current display position?',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if reply != QMessageBox.StandardButton.Yes:
                        return

                body_text = self._strip_inspiration_body(current_text)
                body_text = body_text[:position_idx] + ResultEnd + body_text[position_idx:]
                composed_text = self._compose_inspiration_file(body_text)
                with open(fulldir1, 'w', encoding='utf-8') as f0:
                    f0.write(composed_text)
            with open(BasePath + 'filename.txt', 'w', encoding='utf-8') as f0:
                f0.write(file_name)

        QTimer.singleShot(100, self.addcit2)

    def _populate_article_fields_from_content(self, contend):
        def _set_if_empty(widget, value):
            if hasattr(widget, 'setText'):
                if str(widget.text()).strip() == '':
                    widget.setText(value)

        pattern_map = {
            'title': (re.compile(r'Title: (.*?)\n'), self.le1),
            'authors': (re.compile(r'Authors: (.*?)\n'), self.le2),
            'pub': (re.compile(r'Publication: (.*?)\n'), self.le3),
            'press': (re.compile(r'Press: (.*?)\n'), self.le3_1),
            'year': (re.compile(r'Year: (.*?)\n'), self.le4),
            'vol': (re.compile(r'Vol / Mon: (.*?)\n'), self.le4_1),
            'tags': (re.compile(r'Tags: (.*?)\n'), self.le5),
            'from_book': (re.compile(r'From book: (.*?),'), self.le8),
            'chapter': (re.compile(r', Chapter (.*?),'), self.le9),
            'pages': (re.compile(r'Page range: (.*?)\n'), self.le10),
            'doi': (re.compile(r'DOI: (.*?)\n'), self.le_doi),
            'isbn': (re.compile(r'ISBN: (.*?)\n'), self.le_isbn),
        }
        for key, (pat, widget) in pattern_map.items():
            res = pat.findall(contend)
            value = ''.join(res).replace('[', '').replace(']', '').replace('#AD', '').strip()
            if key == 'tags':
                value = value.replace('#', '').replace(' ', '、')
            if key == 'chapter':
                value = value.replace(', ', '')
            if key == 'pages':
                value = value.replace(', Page range: ', '')
            _set_if_empty(widget, value)

        # handle URL-like info in web mode if present
        if 'URL:' in contend and hasattr(self, 'leweb3'):
            patt = re.compile(r'URL: (.*?)\n')
            res = patt.findall(contend)
            url_val = ''.join(res).strip()
            _set_if_empty(self.leweb3, url_val)

    def _clear_article_temp_fields(self):
        fields = ['le1', 'le2', 'le7', 'le3', 'le3_1', 'le4', 'le4_1',
                  'le5', 'le8', 'le9', 'le10', 'le_doi', 'le_isbn',
                  'leweb3', 'leweb8', 'leweb9', 'leweb10']
        for fname in fields:
            w = getattr(self, fname, None)
            if hasattr(w, 'clear'):
                w.clear()

    def addcit2(self):
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        home_dir = str(Path.home())
        tarname11 = "Documents"
        fulldir11 = os.path.join(home_dir, tarname11)
        if not os.path.exists(fulldir11):
            os.makedirs(fulldir11)
        tarname22 = 'Obsidien'
        fulldir22 = os.path.join(fulldir11, tarname22)
        if not os.path.exists(fulldir22):
            os.makedirs(fulldir22)
        tarname33 = 'Database'
        fulldir33 = os.path.join(fulldir22, tarname33)
        if not os.path.exists(fulldir33):
            os.makedirs(fulldir33)
        tarnamea = 'RIS'
        fulldira = os.path.join(fulldir33, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)

        if path1 != '' and self.leii1.text() != '':
            file_name = codecs.open(BasePath + 'filename.txt', 'r', encoding='utf-8').read()
            if file_name != '' and (path1 in file_name or fulldira in file_name):
                try:
                    title_key = self._get_citation_title_key()
                except Exception:
                    title_key = self.leii1.text()
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                bibtex_block = ''
                pattern_bib = re.compile(r'```(?:\s*bibtex)?(.*?)```', re.DOTALL | re.IGNORECASE)
                match_bib = pattern_bib.search(contend)
                if match_bib:
                    bibtex_block = match_bib.group(1).strip()
                if bibtex_block == '':
                    # populate article fields from metadata to build bibtex on the fly
                    self._populate_article_fields_from_content(contend)
                    def _safe_num(val):
                        return str(val).strip() if str(val).strip() != '' else '000'
                    def _safe_str(val):
                        return str(val).strip() if str(val).strip() != '' else 'UNKNOWN'
                    def _clean_key(src):
                        key = re.sub('[^A-Za-z0-9]', '', str(src))
                        return key if key != '' else 'Unknown'
                    def _build_citekey():
                        authors_raw = _safe_str(self.le2.text()).replace('+', '、').split('、')
                        first_author = authors_raw[0] if authors_raw else 'Unknown'
                        author_key = _clean_key(first_author.split(' ')[0])
                        year_key = _safe_num(self.le4.text())
                        title_key = _clean_key(self.le1.text())
                        return f"{author_key}{year_key}{title_key}"
                    def _bibtex_article():
                        vol_val = _safe_str(self.le4_1.text())
                        num_val = _safe_num('000')
                        if '(' in vol_val or '（' in vol_val:
                            import re as _re
                            m = _re.search(r'[\(（](.*?)[\)）]', vol_val)
                            if m:
                                num_val = _safe_num(m.group(1))
                            vol_val = _re.sub(r'[\(（].*?[\)）]', '', vol_val).strip()
                        citekey = _build_citekey()
                        doi_val = _safe_str(self.le_doi.text())
                        journal = _safe_str(self.le3.text())
                        volume = _safe_num(vol_val)
                        number = num_val
                        pages = _safe_str(self.le10.text())
                        publisher = _safe_str(self.le3_1.text())
                        url_val = f"https://doi.org/{doi_val}" if doi_val != 'UNKNOWN' else _safe_str(self.leweb3.text())
                        return f'''@article{{{citekey},
  doi = "{doi_val}",
  title = "{_safe_str(self.le1.text())}",
  author = "{_safe_str(self.le2.text()).replace('、', ' and ')}",
  journal = "{journal}",
  year = {_safe_num(self.le4.text())},
  volume = {volume},
  number = {number},
  pages = "{pages}",
  publisher = "{publisher}",
  url = "{url_val}",
  type = "journal-article",
}}'''
                    def _bibtex_misc():
                        citekey = _build_citekey()
                        today = datetime.datetime.now().strftime('%Y-%m-%d')
                        year_val = _safe_num(self.le4.text())
                        month_val = _safe_str(self.le4_1.text())
                        date_val = f"{year_val}-{month_val}" if month_val != 'UNKNOWN' else f"{year_val}-00-00"
                        howpublished = _safe_str(self.leweb8.text() if self.leweb8.text() != '' else self.le3.text())
                        url_val = _safe_str(self.leweb3.text())
                        return f'''@misc{{{citekey},
  author    = {{{_safe_str(self.le2.text()).replace('、', ' and ')}}},
  title     = {{{_safe_str(self.le1.text())}}},
  year      = {{{year_val}}},
  date      = {{{date_val}}},
  howpublished = {{{howpublished}}},
  url       = {{{url_val}}},
  urldate   = {{{today}}},
  language  = {{{_safe_str('en')}}}
}}'''
                    def _bibtex_inproceedings():
                        vol_val = _safe_str(self.le4_1.text())
                        num_val = _safe_num('000')
                        if '(' in vol_val or '（' in vol_val:
                            import re as _re
                            m = _re.search(r'[\(（](.*?)[\)）]', vol_val)
                            if m:
                                num_val = _safe_num(m.group(1))
                            vol_val = _re.sub(r'[\(（].*?[\)）]', '', vol_val).strip()
                        citekey = _build_citekey()
                        booktitle = _safe_str(self.leweb8.text())
                        editor = _safe_str(self.leweb9.text())
                        volume = _safe_num(vol_val)
                        pages = _safe_str(self.le10.text())
                        publisher = _safe_str(self.le3_1.text())
                        address = _safe_str(self.leweb10.text())
                        doi_val = _safe_str(self.le_doi.text())
                        url_val = f"https://doi.org/{doi_val}" if doi_val != 'UNKNOWN' else _safe_str(self.leweb3.text())
                        return f'''@inproceedings{{{citekey},
  author    = {{{_safe_str(self.le2.text()).replace('、', ' and ')}}},
  title     = {{{_safe_str(self.le1.text())}}},
  booktitle = {{{booktitle}}},
  editor    = {{{editor}}},
  volume    = {{{volume}}},
  series    = {{{_safe_str('UNKNOWN')}}},
  pages     = {{{pages.replace('-', '--')}}},
  publisher = {{{publisher}}},
  address   = {{{address}}},
  year      = {{{_safe_num(self.le4.text())}}},
  month     = {{{_safe_str('UNKNOWN').lower()}}},
  doi       = {{{doi_val}}},
  url       = {{{url_val}}},
  language  = {{{_safe_str('en')}}}
}}'''
                    def _bibtex_book():
                        citekey = _build_citekey()
                        title_val = _safe_str(self.le8.text() if self.le8.text() != '' else self.le1.text())
                        pages_val = _safe_str(self.le10.text())
                        url_val = _safe_str(self.leweb3.text())
                        return f'''@book{{{citekey},
  doi = "{_safe_str(self.le_doi.text())}",
  title = "{title_val}",
  author = "{_safe_str(self.le2.text()).replace('、', ' and ')}",
  publisher = "{_safe_str(self.le3_1.text())}",
  year = {_safe_num(self.le4.text())},
  isbn = "{_safe_str(self.le_isbn.text())}",
  url = "{url_val}",
  pages = "{pages_val}",
}}'''
                    def _pick_bibtex():
                        if self.leweb3.text() != '':
                            return _bibtex_misc()
                        if self.leweb3.text() == '' and self.leweb8.text() != '':
                            return _bibtex_inproceedings()
                        if self.le3.text() != '' and self.le3_1.text() == '' and self.leweb3.text() == '' and self.leweb8.text() == '':
                            return _bibtex_article()
                        if self.le3_1.text() != '' and self.le3.text() == '':
                            return _bibtex_book()
                        return _bibtex_article()
                    bibtex_block = _pick_bibtex()
                    # write into article metadata before notes
                    marker = '\n\n---\n\n# Notes'
                    if marker in contend:
                        contend = contend.replace(marker, '\n- BibTeX:\n```bibtex\n' + bibtex_block + '\n```' + marker, 1)
                    else:
                        contend = contend + '\n- BibTeX:\n```bibtex\n' + bibtex_block + '\n```\n'
                    with open(file_name, 'w', encoding='utf-8') as wf:
                        wf.write(contend)
                if bibtex_block != '':
                    path3_cit = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
                    if path3_cit != '' and title_key != '':
                        cit_dir = os.path.join(path3_cit, 'StrawberryCitations', title_key)
                        os.makedirs(cit_dir, exist_ok=True)
                        bib_file = os.path.join(cit_dir, f"{title_key}.bib")
                        existing_bib = ''
                        if os.path.exists(bib_file):
                            existing_bib = codecs.open(bib_file, 'r', encoding='utf-8').read()
                        with open(bib_file, 'a', encoding='utf-8') as bf:
                            if existing_bib != '' and not existing_bib.endswith('\n'):
                                bf.write('\n')
                            bf.write(bibtex_block)
                            if not bibtex_block.endswith('\n'):
                                bf.write('\n')
                        self._generate_csl_citations(title_key, path3_cit, latest_bib_block=bibtex_block)

                # Citation block from original Markdown is no longer used; path_ref is now built from generated formats
                # pattern6 = re.compile(r'Citation: (.*?)\n')
                # result6 = pattern6.findall(contend)
                # result6 = ''.join(result6)
                # pretc6 = result6.replace('Citation: ', '')
                # pretc6 = pretc6.replace('\n', '')
                # pretc6 = pretc6.replace('[[', '')
                # pretc6 = pretc6.replace(']]', '')
                # oldref = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
                # pretc7 = '0'
                # if oldref != '':
                    # pattern7 = re.compile(r'\[.\d*\]')
                    # result7 = pattern7.findall(oldref)
                    # i = 0
                    # while i >= 0 and i <= len(result7) - 1:
                    #     result7[i] = result7[i].replace('[^', '')
                    #     result7[i] = result7[i].replace(']', '')
                    #     result7[i] = ''.join(result7[i])
                    #     i = i + 1
                    #     continue
                    # result7.sort(key=int, reverse=True)
                    # pretc7 = str(result7[0])
                # if oldref == '':
                #     pretc7 = '0'

                # if self.leii2.text() != '':
                #     if pretc6 != '':
                #         partt1 = '\n[^' + str(self.leii2.text()) + ']: ' + pretc6
                #         with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #             citpat.write(partt1)
                #     if pretc6 == '':
                #         partt1 = '\n[^' + str(self.leii2.text()) + ']: ' + 'Cannot find citation for ' + file_name
                #         with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #             citpat.write(partt1)
                # if self.leii2.text() == '':
                #     # tarnumb = '1'
                #     if pretc7 == '0':
                #         tarnumb = '1'
                #         if pretc6 != '':
                #             partt1 = '[^' + str(tarnumb) + ']: ' + pretc6
                #             with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #                 citpat.write(partt1)
                #         if pretc6 == '':
                #             partt1 = '[^' + str(tarnumb) + ']: ' + 'Cannot find citation for ' + file_name
                #             with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #                 citpat.write(partt1)
                #     if pretc7 != '0':
                #         tarnumb = str(int(pretc7) + 1)
                #         if pretc6 != '':
                #             partt1 = '\n[^' + str(tarnumb) + ']: ' + pretc6
                #             with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #                 citpat.write(partt1)
                #         if pretc6 == '':
                #             partt1 = '\n[^' + str(tarnumb) + ']: ' + 'Cannot find citation for ' + file_name
                #             with open(BasePath + 'path_ref.txt', 'a', encoding='utf-8') as citpat:
                #                 citpat.write(partt1)

            path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            if path3 != '' and file_name != '' and (path1 in file_name or fulldira in file_name):
                tarname4 = str(self.leii1.text()) + ".md"
                fulldir4 = os.path.join(path3, tarname4)
                with open(fulldir4, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                body_text = self._strip_inspiration_body(contm)
                partb = self._build_inspiration_references()
                if self.leii1.text() != '':
                    with open(fulldir4, 'w', encoding='utf-8') as f3:
                        f3.write(self._compose_inspiration_file(body_text))

            pathend = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.leii1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self._show_inspiration_content(contend)
                self.textii2.ensureCursorVisible()  # 游标可用
                cursor = self.textii2.textCursor()  # 设置游标
                pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.textii2.setTextCursor(cursor)  # 滚动到游标位置

            self.leii2.clear()

            with open(BasePath + 'filename.txt', 'w', encoding='utf-8') as f0:
                f0.write('')
            self._clear_article_temp_fields()
            self._apply_selected_format_to_refs()

    def _parse_author(self, author_string):
        authors = []
        for name_str in author_string.split(' and '):
            name_str = name_str.strip()
            if name_str == '':
                continue
            if ',' in name_str:
                parts = [p.strip() for p in name_str.split(',', 1)]
                authors.append({'family': parts[0], 'given': parts[1] if len(parts) > 1 else ''})
            else:
                parts = name_str.split()
                authors.append({'family': parts[-1], 'given': ' '.join(parts[:-1])})
        return authors

    def _convert_entry_to_csl(self, entry):
        csl_item = {'id': entry.get('ID', entry.get('id', 'item'))}
        type_mapping = {
            'article': 'article-journal',
            'book': 'book',
            'incollection': 'chapter',
            'inproceedings': 'paper-conference',
            'conference': 'paper-conference',
            'phdthesis': 'thesis',
            'mastersthesis': 'thesis',
            'techreport': 'report',
            'misc': 'document',
            'unpublished': 'manuscript',
        }
        entrytype = entry.get('ENTRYTYPE', entry.get('entrytype', 'document')).lower()
        csl_item['type'] = type_mapping.get(entrytype, 'document')

        field_mapping = {
            'title': 'title', 'journal': 'container-title', 'booktitle': 'container-title',
            'volume': 'volume', 'number': 'issue', 'pages': 'page', 'publisher': 'publisher',
            'url': 'URL', 'doi': 'DOI', 'abstract': 'abstract', 'issn': 'ISSN',
            'school': 'publisher', 'institution': 'publisher', 'howpublished': 'medium',
        }
        for bib_field, csl_field in field_mapping.items():
            if bib_field in entry:
                csl_item[csl_field] = entry[bib_field]

        if 'author' in entry:
            csl_item['author'] = self._parse_author(entry['author'])
        if 'year' in entry:
            try:
                csl_item['issued'] = {'date-parts': [[int(entry['year'])]]}
            except Exception:
                csl_item['issued'] = {'date-parts': [[0]]}
        return csl_item

    def _ensure_csl_styles(self):
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        csl_dir = os.path.join(base_dir, "CitationFormat")
        if not os.path.exists(csl_dir):
            os.mkdir(csl_dir)
        list_file = os.path.join(csl_dir, "formats.txt")
        if not os.path.exists(list_file):
            with open(list_file, 'a', encoding='utf-8') as f0:
                f0.write('')
        formats = codecs.open(list_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '' and i.strip().lower() != 'quickcite']
        style_map = {}
        for fmt in formats:
            name = fmt.strip()
            filename = name if name.endswith('.csl') else f"{name}.csl"
            style_path = os.path.join(csl_dir, filename)
            if os.path.exists(style_path):
                style_map[name] = style_path
        return style_map

    def _generate_csl_citations(self, title, script_dir, latest_bib_block=None):
        # try:
        #     import bibtexparser
        #     from bibtexparser.bparser import BibTexParser
        #     from bibtexparser.customization import convert_to_unicode
        #     from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
        #     from citeproc import formatter
        #     from citeproc.source.json import CiteProcJSON
        # except Exception:
        #     return

        if title == '' or script_dir == '':
            return
        bib_file = os.path.join(script_dir, 'StrawberryCitations', title, f"{title}.bib")
        if not os.path.exists(bib_file):
            return
        style_map = self._ensure_csl_styles()
        if not style_map:
            return
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        entries = []
        # Prefer parsing the latest block directly to avoid malformed older entries
        if latest_bib_block:
            try:
                bib_db_latest = bibtexparser.loads(latest_bib_block, parser=parser)
                entries = bib_db_latest.entries
            except Exception:
                entries = []
        if not entries:
            try:
                with open(bib_file, 'r', encoding='utf-8') as bf:
                    bib_db = bibtexparser.load(bf, parser=parser)
                    entries = bib_db.entries
            except Exception:
                return
        if not entries:
            return

        cit_dir = os.path.join(script_dir, 'StrawberryCitations', title)

        def _append_line(path, text):
            if text is None or text.strip() == '':
                return
            os.makedirs(os.path.dirname(path), exist_ok=True)
            needs_newline = os.path.exists(path) and os.path.getsize(path) > 0
            with open(path, 'a', encoding='utf-8') as f0:
                if needs_newline:
                    f0.write('\n')
                f0.write(text.strip())

        # Only process the most recently added entry (parsed from latest_bib_block if available)
        latest_entry = entries[-1]
        csl_item = self._convert_entry_to_csl(latest_entry)
        for fmt, style_path in style_map.items():
            if not os.path.exists(style_path):
                continue
            try:
                style = CitationStylesStyle(style_path, validate=False)
                bib_source = CiteProcJSON([csl_item])
                bibliography = CitationStylesBibliography(style, bib_source, formatter.plain)
                citation = Citation([CitationItem(csl_item['id'])])
                bibliography.register(citation)
                inline_cite = str(bibliography.cite(citation, lambda x: None))
                biblio_entries = [str(item) for item in bibliography.bibliography()]
                biblio_text = '\n'.join(biblio_entries).strip()
            except Exception:
                continue

            inline_file = os.path.join(cit_dir, f"{title}-{fmt}-in.txt")
            biblio_file = os.path.join(cit_dir, f"{title}-{fmt}.txt")
            _append_line(inline_file, inline_cite)
            _append_line(biblio_file, biblio_text)

        # quickcite generation using basic fields
        try:
            is_cn = self.is_contain_chinese
        except Exception:
            def is_cn(x): return False

        author_raw = latest_entry.get('author', 'UNKNOWN')
        authors = [a.strip() for a in author_raw.replace(' and ', '、').split('、') if a.strip() != '']
        if not authors:
            authors = ['UNKNOWN']
        first_author = authors[0]
        title_val = latest_entry.get('title', 'UNKNOWN')
        pub_val = latest_entry.get('journal') or latest_entry.get('booktitle') or latest_entry.get('publisher') or latest_entry.get('howpublished') or 'UNKNOWN'
        year_val = latest_entry.get('year', '0')
        pages_val = latest_entry.get('pages', '').replace('--', '-')
        volume_val = str(latest_entry.get('volume', '')).strip()
        number_val = str(latest_entry.get('number', '')).strip()
        entry_type = latest_entry.get('ENTRYTYPE', '').lower()

        # build vol/num text
        vol_text = ''
        if volume_val and volume_val.upper() != 'UNKNOWN':
            vol_text = volume_val
        if number_val and number_val.upper() != 'UNKNOWN' and number_val != '000':
            if vol_text != '':
                vol_text = f"{vol_text}({number_val})"
            else:
                vol_text = f"{number_val}"

        cn_flag = is_cn(str(title_val)) or is_cn(str(pub_val))
        inline_qc = ''
        biblio_qc = ''
        if cn_flag:
            if latest_entry.get('journal') or latest_entry.get('booktitle'):
                # 中文文章
                biblio_qc = f"{'、'.join(authors)}：《{title_val}》，载《{pub_val}》，"
                biblio_qc += f"{year_val} 年"
                if vol_text != '':
                    biblio_qc += f"第 {vol_text} 期，"
                if pages_val and pages_val.upper() != 'UNKNOWN':
                    biblio_qc += f"第 {pages_val} 页。"
                else:
                    biblio_qc = biblio_qc.rstrip('，')
                    if not biblio_qc.endswith('。'):
                        biblio_qc += '。'
                inline_qc = f'（{first_author}，{year_val}）'
            else:
                # 中文书籍
                biblio_qc = f"{'、'.join(authors)}：《{title_val}》，{pub_val}"
                if year_val and year_val != '0':
                    biblio_qc += f"，{year_val} 年"
                if number_val and number_val.upper() != 'UNKNOWN' and number_val != '000':
                    biblio_qc += f" {number_val} 月版"
                else:
                    biblio_qc += "版"
                biblio_qc += ''
                if pages_val and pages_val.upper() != 'UNKNOWN':
                    biblio_qc += f"，第 {pages_val} 页。"
                else:
                    if not biblio_qc.endswith('。'):
                        biblio_qc += '。'
                inline_qc = f'（{first_author}，{year_val}）'
        else:
            # English formatting mirroring addmain citation style
            if entry_type == 'book' or (pub_val != 'UNKNOWN' and latest_entry.get('journal') is None and latest_entry.get('booktitle') is None):
                biblio_qc = f"{', '.join(authors)}, {title_val}, {pub_val}, {year_val}"
                if pages_val and pages_val.upper() != 'UNKNOWN':
                    biblio_qc += f", pp. {pages_val}"
                if not biblio_qc.endswith('.'):
                    biblio_qc += '.'
            else:
                biblio_qc = f"{', '.join(authors)}, “{title_val},” *{pub_val}*"
                if vol_text != '':
                    biblio_qc += f", {vol_text}"
                biblio_qc += f", {year_val}"
                if pages_val and pages_val.upper() != 'UNKNOWN':
                    biblio_qc += f", pp. {pages_val}"
                if not biblio_qc.endswith('.'):
                    biblio_qc += '.'
            inline_qc = ''  # keep inline quickcite empty by design

        inline_file = os.path.join(cit_dir, f"{title}-quickcite-in.txt")
        biblio_file = os.path.join(cit_dir, f"{title}-quickcite.txt")
        if not os.path.exists(inline_file):
            with open(inline_file, 'a', encoding='utf-8') as _tmp:
                _tmp.write('')
        if biblio_qc.strip() != '':
            _append_line(biblio_file, biblio_qc)

    def _apply_selected_format_to_refs(self):
        if self.leii1.text() == '':
            return
        try:
            title = self._get_citation_title_key()
        except Exception:
            title = self.leii1.text()
        base_filename = str(self.leii1.text())
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        csl_dir = os.path.join(base_dir, "CitationFormat")
        selected_file = os.path.join(csl_dir, "selected_format.txt")
        try:
            selected_fmt = codecs.open(selected_file, 'r', encoding='utf-8').read().strip()
        except Exception:
            selected_fmt = ''
        if selected_fmt == '':
            selected_fmt = 'Quick cite (defaut)'
        script_dir = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if script_dir == '':
            return
        cit_dir = os.path.join(script_dir, 'StrawberryCitations', title)
        # only use selected format file (non-inline)
        fmt_key = selected_fmt.strip()
        if fmt_key.lower().startswith('quick'):
            fmt_key = 'quickcite'
        if fmt_key.lower().endswith('.csl'):
            fmt_key = fmt_key[:-4]
        fmt_name = fmt_key
        fmt_file = os.path.join(cit_dir, f"{title}-{fmt_name}.txt")
        if not os.path.exists(fmt_file):
            alt_file = os.path.join(cit_dir, f"{title}-{fmt_name.lower()}.txt")
            if os.path.exists(alt_file):
                fmt_file = alt_file
            else:
                qc_file = os.path.join(cit_dir, f"{title}-quickcite.txt")
                if os.path.exists(qc_file):
                    fmt_file = qc_file
                else:
                    return
        try:
            lines = codecs.open(fmt_file, 'r', encoding='utf-8').read().split('\n')
        except Exception:
            return
        lines = [l for l in lines if l.strip() != '']
        prefixed = []
        for idx, line in enumerate(lines, 1):
            # strip leading [number] artifacts
            clean_line = re.sub(r'^\s*\[\s*\d+\s*\]\s*', '', line).strip()
            prefixed.append(f"[^{idx}]: {clean_line}")
        with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as rf:
            rf.write('\n'.join(prefixed))
        # write back to current inspiration markdown
        path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path3 == '':
            return
        tarname4 = base_filename + ".md"
        fulldir4 = os.path.join(path3, tarname4)
        if os.path.exists(fulldir4):
            contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
            body_text = self._strip_inspiration_body(contm)
            composed = self._compose_inspiration_file(body_text)
            with open(fulldir4, 'w', encoding='utf-8') as f3:
                f3.write(composed)
            # refresh UI
            self._show_inspiration_content(composed)
            self.textii2.ensureCursorVisible()
            cursor = self.textii2.textCursor()
            pos = len(self.textii2.toPlainText())
            cursor.setPosition(pos)
            self.textii2.setTextCursor(cursor)
    def clinp(self):
        self.btn_ia1.setEnabled(True)
        w4.csl_open_btn.setEnabled(True)
        w4.csl_add_btn.setEnabled(True)
        w4.csl_delete_btn.setVisible(True)
        if self.textii2.toPlainText() != '' and self.leii1.text() != '':
            path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            body_text = self._strip_inspiration_body(self.textii2.toPlainText())
            saved = self._compose_inspiration_file(body_text)
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)
        self.textii1.clear()
        self.textii2.clear()
        self.textii3.clear()
        self.leii1.clear()
        self.textii2_head.clear()
        self.textii2_foot.clear()
        self.real2.clear()
        self._set_citation_controls_enabled(True)
        with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as citpat:
            citpat.write('')
        with open(BasePath + 'path_lat.txt', 'w', encoding='utf-8') as reflat:
            reflat.write('')
        self.btn_a.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btn_a.setText('Create')
        self.leii1.setEnabled(True)
        with open(BasePath + 'path_ste.txt', 'w', encoding='utf-8') as r0:
            r0.write('')
        with open(BasePath + 'path_std.txt', 'w', encoding='utf-8') as r1:
            r1.write('')
        self.widgettem.setCurrentIndex(0)
        self.choosepart.clear()
        self.choosepart.addItems(['Append at the end (default)', 'Append at the current cursor'])
        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as r1:
            r1.write('')
        self.leiinote.clear()
        self.leii2.setPlaceholderText('Number (blank = auto mode)')
        self._cached_title_key = ''
        reset_newarchive_path()

    def save1(self):
        oldv = self.text.verticalScrollBar().value()
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            pattern = re.compile(r'Title: (.*?)\n')
            result = pattern.findall(self.text.toPlainText())
            result = ''.join(result)
            pretc = result.replace('Title: ', '')
            pretc = pretc.replace('\n', '')
            pretc = pretc.replace('[', '')
            pretc = pretc.replace(']', '')
            oldnam = codecs.open(BasePath + 'path_ttl.txt', 'r', encoding='utf-8').read()
            if oldnam != pretc:
                self.le1.setText(pretc)
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text.toPlainText()
            if self.le1.text() != '' and self.text.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.le1.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.le1.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text.setPlainText(contend)
                self.text.verticalScrollBar().setValue(oldv)
                if self.text.verticalScrollBar().maximum() != 0:
                    proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                    tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                    self.real1.verticalScrollBar().setValue(tar_pro)

        itemold = self.widget0.currentText()
        self.widget0.clear()
        self.widget0.addItems(['Append at the end (default)', 'Append at the current cursor'])
        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        tarname1 = str(self.le1.text()) + ".md"
        fulldir1 = os.path.join(path1, tarname1)
        if self.le1.text() != '':
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
            result = '☆'.join(result)
            if result != '':
                result = result.replace('#', '')
                result = result.replace('# ', '')
                result = result.replace('Q/P: ', '')
                result = result.split('☆')
                for i in range(len(result)):
                    result[i] = 'After ' + result[i]
                    result[i] = ''.join(result[i])
                self.widget0.addItems(result)
                if itemold in result:
                    itemnub = result.index(itemold) + 2
                    self.widget0.setCurrentIndex(itemnub)
                if itemold not in result:
                    self.widget0.setCurrentIndex(0)

    def save2(self):
        path1 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lec1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s2.toPlainText()
            if self.lec1.text() != '' and self.text_s2.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.lec1.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.lec1.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text_s2.setPlainText(contend)
                self.text_s2.ensureCursorVisible()  # 游标可用
                cursor = self.text_s2.textCursor()  # 设置游标
                pos = len(self.text_s2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text_s2.setTextCursor(cursor)  # 滚动到游标位置

    def saveinsp(self):
        if self.leii1.text() != '' and self.textii2.toPlainText() != '':
            path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                with open(BasePath + 'path_std.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.leii1.text())
                def _candidate_names(raw):
                    cands = [raw]
                    try:
                        import re as _re
                        base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                        if base1 and base1 not in cands:
                            cands.append(base1)
                        base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                        if base2 and base2 not in cands:
                            cands.append(base2)
                    except Exception:
                        pass
                    return cands

                def _resolve_path(dir_path, raw_name, ext):
                    for nm in _candidate_names(raw_name):
                        cand = os.path.join(dir_path, nm + ext)
                        if os.path.exists(cand):
                            return cand, nm + ext
                    return os.path.join(dir_path, raw_name + ext), raw_name + ext

                fulldir1 = ''
                tarname1 = ''
                fulldir1, tarname1 = _resolve_path(path1, str(self.leii1.text()), ".md")
                base_name_noext = os.path.splitext(os.path.basename(fulldir1))[0]
                # Only persist body; header/footer are composed later
                body_text = self.textii2.toPlainText()
                body_text = self._strip_inspiration_body(body_text).rstrip('\n')
                # If footer is visible and edited, persist it back to path_ref.txt
                if self.insp_show_full:
                    foot_text = self.textii2_foot.toPlainText().replace('\r', '')
                    ref_block = ''
                    ref_idx = foot_text.find('## References')
                    if ref_idx != -1:
                        ref_block = foot_text[ref_idx + len('## References'):].replace('<document-end>', '').strip()
                    cleaned_refs = []
                    for line in ref_block.splitlines():
                        line = line.rstrip('\n').rstrip()
                        line = re.sub(r'<e>\s*$', '', line)
                        if line != '':
                            cleaned_refs.append(line)
                    with open(BasePath + 'path_ref.txt', 'w', encoding='utf-8') as fp:
                        fp.write('\n'.join(cleaned_refs).rstrip('\n'))
                saved = self._compose_inspiration_file(body_text)
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

                oldtext = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                oldtext = oldtext.replace('[[', '')
                oldtext = oldtext.replace(']]', '')
                pattern = re.compile(r'<!--Title: (.*?)-->')
                result = pattern.findall(oldtext)
                result = ''.join(result)
                pretc = result.replace('<!--Title: ', '')
                prettle = pretc.replace('-->', '')
                prettle = re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', prettle).rstrip()
                part_a = '''%!TEX program = xelatex
% 完整编译: xelatex -> biber/bibtex -> xelatex -> xelatex
\\documentclass[lang=cn,11pt,a4paper]{elegantpaper}'''
                if self.widgettem.currentIndex() == 1:
                    part_a = '''%!TEX program = pdflatex
% Full chain: pdflatex -> biber/bibtex -> pdflatex -> pdflatex
\\documentclass[11pt,en]{elegantpaper}'''
                if self.widgettem.currentIndex() == 2:
                    part_a = '''%!TEX program = xelatex
\\documentclass[cn,hazy,blue,14pt,screen]{elegantnote}'''
                if self.widgettem.currentIndex() == 3:
                    part_a = '''%!TEX program = xelatex
\\documentclass[en,hazy,screen,blue,14pt]{elegantnote}'''
                if self.widgettem.currentIndex() == 4:
                    part_a = '''\\documentclass[conference]{IEEEtran}
\\IEEEoverridecommandlockouts

\\usepackage{cite}
\\usepackage{amsmath,amssymb,amsfonts}
\\usepackage{algorithmic}
\\usepackage{graphicx}
\\usepackage{textcomp}
\\usepackage{xcolor}
\\def\\BibTeX{{\\rm B\\kern-.05em{\\sc i\\kern-.025em b}\\kern-.08em
    T\\kern-.1667em\\lower.7ex\\hbox{E}\\kern-.125emX}}
\\begin{document}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 5:
                    part_a = '''%!TEX program = xelatex
\\documentclass[a4paper,12pt]{article}
\\usepackage[left=2.2cm,right=2.2cm,top=2.0cm,bottom=2.5cm,foot=0.7cm,headsep=0.5cm]{geometry}%页边距设置
\\usepackage[UTF8, scheme = plain]{ctex}%UTF8编译中文
\\usepackage{times}\\usepackage{mathptmx}%数学公式字体time
\\usepackage{multicol}%文本栏数,例如：双栏
\\usepackage{color}%颜色宏包
\\usepackage{enumerate}
\\usepackage{colortbl}%颜色宏包
\\usepackage{cite}%引用文献
\\newcommand{\\ucite}[1]{\\textsuperscript{\\cite{#1}}}
\\usepackage{palatino}%美赛英文字体
\\usepackage[font=small,labelfont=bf]{caption}%[font=small,labelfont=bf,labelsep=none]
\\usepackage{lipsum}%引入例子
\\usepackage{journalCNpicins}%图文并排
\\usepackage{booktabs}%三线表
\\usepackage{tabularx}%表格环境
\\usepackage{multirow}%表格并列
\\usepackage[
                       colorlinks,
                       linkcolor=red,
                       anchorcolor=blue,
                       citecolor=blue]{hyperref}%超链接设置
\\usepackage{url}%网址宏包
\\usepackage{bm,amsmath,amsfonts}%数学公式及字体加粗
\\usepackage{amssymb}%数学符号
\\usepackage{graphicx}%图片环境
\\usepackage{float}%图片强制固定H
%每行间距
\\baselineskip 12pt 
%%自定义命令
\\input{journalCNdef}%文本格式设置
\\usepackage[hang,flushmargin]{footmisc}
\\usepackage{zhnumber}
\\renewcommand\\thesection{\\zhnum{section}、\\hspace{-1em}}
\\renewcommand\\thesubsection {（\\zhnum{subsection}）\\hspace{-1em}}
\\renewcommand{\\thesubsubsection}{\\hspace{0.5em}\\arabic{subsubsection}.\\hspace{-0.5em}}
\\begin{document}
\\input{journalCNdef2}%脚注等格式设置
\\renewcommand{\\thefootnote}{\\arabic{footnote}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 6:
                    part_a = '''% !Mode:: "TeX:UTF-8"
% !TEX program  = XeLaTeX
\\documentclass[aspectratio=169]{beamer} % 设置长宽比为 16:9
\\usepackage{ctex, hyperref}
\\usepackage[T1]{fontenc}

% other packages
\\usepackage{latexsym,amsmath,xcolor,multicol,booktabs,calligra}
\\usepackage{graphicx,pstricks,listings,stackengine}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 7:
                    part_a = '''\\documentclass[11pt,a4paper]{article}
\\usepackage{CJK}
\\usepackage{type1cm}
\\usepackage{times}
\\usepackage[marginal]{footmisc}
\\usepackage{indentfirst}
\\setlength{\\parindent}{2em}
%\\renewcommand{\\thefootnote}{}
\\begin{CJK*}{UTF8}{gbsn}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 8:
                    part_a = self.template_p1

                part_b = '\n\n' + '''\\title{''' + prettle + '}'
                if self.widgettem.currentIndex() == 4:
                    part_b = '\n\n' + '\\title{' + prettle + '*\\thanks{Special thanks to funding agency here. If none, delete this.}}'
                if self.widgettem.currentIndex() == 5:
                    part_b = '\n\n' + '\\SEC{\\songti  ' + prettle + '}'
                if self.widgettem.currentIndex() == 6:
                    part_b = '\n\n' + '\\title{' + prettle + '}'
                if self.widgettem.currentIndex() == 7:
                    part_b = '\n\n' + '\\title{\\textbf{' + prettle + '}}'
                if self.widgettem.currentIndex() == 8:
                    part_b = '\n\n' + self.template_p2 + prettle + self.template_p3

                part_c = '\n' + '''\\author{人名}
\\institute{单位}
\\date{}
    
    
% 本文档命令
\\usepackage{array}
\\newcommand{\\ccr}[1]{\\makecell{{\\color{#1}\\rule{1cm}{1cm}}}}
\\usepackage{zhnumber}
\\renewcommand\\thesection{\\zhnum{section}、\\hspace{-1em}}
\\renewcommand\\thesubsection {（\\zhnum{subsection}）\\hspace{-1em}}
\\renewcommand{\\thesubsubsection}{\\hspace{0.5em}\\arabic{subsubsection}.\\hspace{-0.5em}}
    
\\begin{document}
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
\\maketitle
    
\\begin{abstract}
文字。
\\keywords{关键词1，关键词2}
\\end{abstract}
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 1:
                    part_c = '\n' + '''\\author{Name}
\\institute{Institute}
\\date{}


% cmd for this doc
\\usepackage{array}
\\newcommand{\\ccr}[1]{\\makecell{{\\color{#1}\\rule{1cm}{1cm}}}}

\\begin{document}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\maketitle

\\begin{abstract}
Words.
\\keywords{Keywords}
\\end{abstract}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 2:
                    part_c = '\n' + '''\\author{人名}
\\institute{单位}
\\date{\\zhtoday}


\\usepackage{array}

\\begin{document}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\maketitle
\\newpage

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 3:
                    part_c = '\n' + '''\\author{Name}
\\institute{Institute}
\\date{\\today}

\\begin{document}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\maketitle
\\newpage

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 4:
                    part_c = '\n' + '''\\author{\\IEEEauthorblockN{1\\textsuperscript{st} Given Name Surname}
\\IEEEauthorblockA{\\textit{dept. name of organization (of Aff.)} \\\\
\\textit{name of organization (of Aff.)}\\\\
City, Country \\\\
email address or ORCID}
\\and
\\IEEEauthorblockN{2\\textsuperscript{nd} Given Name Surname}
\\IEEEauthorblockA{\\textit{dept. name of organization (of Aff.)} \\\\
\\textit{name of organization (of Aff.)}\\\\
City, Country \\\\
email address or ORCID}
\\and
\\IEEEauthorblockN{3\\textsuperscript{rd} Given Name Surname}
\\IEEEauthorblockA{\\textit{dept. name of organization (of Aff.)} \\\\
\\textit{name of organization (of Aff.)}\\\\
City, Country \\\\
email address or ORCID}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\maketitle

\\begin{abstract}
Words.
\\end{abstract}

\\begin{IEEEkeywords}
Keywords.
\\end{IEEEkeywords}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 5:
                    part_c = '\n' + '''{\\songti 作者} 
{(~机构~)}

\\begin{minipage}[b]{0.9\\linewidth}
\\narrower\\zihao{5}\\noindent {\\songti \\textbf{摘}\\quad\\textbf{要}}\\ \\ 
文字
\\end{minipage}

\\normalsize \\normalsize \\abovedisplayskip=2.0pt plus 2.0pt minus
2.0pt \\belowdisplayskip=2.0pt plus 2.0pt minus 2.0pt \\baselineskip
16pt

\\begin{multicols}{2}\\songti \\zihao{5}%宋体字

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 6:
                    part_c = '\n' + '''\\subtitle{副标题}
\\author{人名}
\\institute{学校机构}
\\date{\\zhtoday}
\\usepackage{BeamerCN}

% defs
\\def\\cmd#1{\\texttt{\\color{red}\\footnotesize $\\backslash$#1}}
\\def\\env#1{\\texttt{\\color{blue}\\footnotesize #1}}
\\definecolor{deepblue}{rgb}{0,0,0.5}
\\definecolor{deepred}{rgb}{0.5,0,0}
\\definecolor{deepgreen}{rgb}{0,0.5,0}
\\definecolor{halfgray}{gray}{0.45}

\\lstset{
    basicstyle=\\ttfamily\\small,
    keywordstyle=\\bfseries\\color{deepblue},
    emphstyle=\\ttfamily\\color{deepred},    % Custom highlighting style
    stringstyle=\\color{deepgreen},
    numbers=left,
    numberstyle=\\small\\color{halfgray},
    rulesepcolor=\\color{red!20!green!20!blue!20},
    frame=shadowbox,
}


\\begin{document}

\\kaishu
\\begin{frame}
    \\titlepage
    %\\begin{figure}[htpb]
        %\\begin{center}
            %\\includegraphics[width=0.1\\linewidth]{School.png}
        %\\end{center}
    %\\end{figure}
\\end{frame}

\\begin{frame}
    \\tableofcontents[sectionstyle=show,subsectionstyle=show/shaded/hide,subsubsectionstyle=show/shaded/hide]
\\end{frame}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 7:
                    part_c = '\n' + '''\\author{人名}
\\date{}

\\begin{document}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\maketitle
%\\tableofcontents

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\renewcommand{\\abstractname}{摘\\ \\ \\ 要}
\\begin{abstract}
摘要。
\\paragraph{}
\\textbf{关键词：}关键词1、关键词2
\\end{abstract}

\\paragraph{\\ \\ \\ \\ }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
                if self.widgettem.currentIndex() == 8:
                    part_c = '\n' + self.template_p4

                savelatex = re.sub(r"<document-start>", '', oldtext)
                savelatex = re.sub(r"\n<document-end>", '', savelatex)
                savelatex = re.sub(r"<!--Title: .*-->\n\n", '', savelatex)
                savelatex = re.sub(r"# " + prettle + '\n\n', '', savelatex)
                savelatex = re.sub(r"\[.*<e>\n", '', savelatex)
                savelatex = re.sub(r"\n\n\n\n", '', savelatex)
                savelatex = re.sub(r"## References \n\n", '', savelatex)
                savelatex = savelatex.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}')
                pattern2 = re.compile(r'\[.[0-9]+]')
                result = pattern2.findall(savelatex)
                result.sort()
                # load selected format and inline list
                home_dir = str(Path.home())
                base_dir = os.path.join(home_dir, "StrawberryAppPath")
                csl_dir = os.path.join(base_dir, "CitationFormat")
                selected_fmt = 'quickcite'
                try:
                    selected_fmt = codecs.open(os.path.join(csl_dir, "selected_format.txt"), 'r', encoding='utf-8').read().strip() or 'quickcite'
                except Exception:
                    selected_fmt = 'quickcite'
                fmt_key = selected_fmt
                if fmt_key.lower().startswith('quick'):
                    fmt_key = 'quickcite'
                if fmt_key.lower().endswith('.csl'):
                    fmt_key = fmt_key[:-4]
                inline_entries = []
                if fmt_key != 'quickcite':
                    title_key = ''
                    try:
                        title_key = self._get_citation_title_key()
                    except Exception:
                        title_key = self.leii1.text()
                    inline_file = os.path.join(path1, 'StrawberryCitations', title_key, f"{title_key}-{fmt_key}-in.txt")
                    if os.path.exists(inline_file):
                        try:
                            inline_entries = [l for l in codecs.open(inline_file, 'r', encoding='utf-8').read().split('\n') if l.strip() != '']
                        except Exception:
                            inline_entries = []
                cajref = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
                cajref = cajref.replace('[[', '')
                cajref = cajref.replace(']]', '')
                cajref = cajref.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}')
                cajref = cajref.split('\n')
                i = 0
                n = 0
                while i >= 0 and i <= len(result) - 1 and n >= 0 and n <= len(cajref) - 1:
                    #while n >= 0 and n <= len(cajref) - 1:
                    if result[i] in cajref[n]:
                        stripednum = result[i].replace('[^', '')
                        stripednum = stripednum.replace(']', '')
                        if fmt_key == 'quickcite':
                            stripedref = re.sub(r"\[.*]: ", '', cajref[n])
                            stripedref = re.sub(r"<e>", '', stripedref)
                            savelatex = re.sub(r"\[." + stripednum + "]", "\\footnote{" + stripedref + '}', savelatex)
                        else:
                            idx_num = 0
                            try:
                                idx_num = int(stripednum) - 1
                            except Exception:
                                idx_num = -1
                            replacement = ''
                            if idx_num >= 0 and idx_num < len(inline_entries):
                                replacement = inline_entries[idx_num]
                            else:
                                replacement = f"\\cite{{ref{stripednum}}}"
                            savelatex = re.sub(r"\[\^" + stripednum + r"\]", lambda m: replacement, savelatex)
                        i = i + 1
                        n = 0
                        continue
                    if result[i] not in cajref[n]:
                        n = n + 1
                        continue
                savelatex = re.sub("(####.*)", r'\1}', savelatex)
                savelatex = savelatex.replace('#### ', '\\subsubsection{')
                savelatex = re.sub("(###.*)", r'\1}', savelatex)
                savelatex = savelatex.replace('### ', '\\subsection{')
                savelatex = re.sub("(##.*)", r'\1}', savelatex)
                savelatex = savelatex.replace('## ', '\\section{')
                savelatex = savelatex.replace('# ', '')
                savelatex = savelatex.replace('ootnote', '\\footnote')
                savelatex = savelatex.replace('', '')

                pattern_cha = re.compile(r'\n\n\|[\s\S]*?\|\n\n')
                result_cha = pattern_cha.findall(savelatex)
                if result_cha != []:
                    new_cha = []
                    for i in range(len(result_cha)):
                        hang = result_cha[i].split('\n')
                        while '' in hang:
                            hang.remove('')
                        n = 0
                        shu = 3
                        while n >= 0 and n <= len(hang) - 1:
                            if '-' in hang[n]:
                                hang.remove(hang[n])
                            else:
                                shu = int(hang[n].count('|')) - 1
                                hang[n] = hang[n].lstrip('|')
                                hang[n] = hang[n].rstrip('|')
                                hang[n] = hang[n] + '\\\\ \\midrule'
                                hang[n] = hang[n].replace('|', '&')
                                n += 1
                            continue
                        hang[0] = hang[0].replace('\\\\ \\midrule', '\\\\ \\toprule')
                        hang[-1] = hang[-1].replace('\\\\ \\midrule', '\\\\ \\bottomrule')
                        hang[0] = '\n\n\\begin{table}[!ht]\n\\centering\n\\caption{Table caption}\n\\begin{tabular}{' + 'c'*shu + '}\n' + hang[0]
                        hang[-1] = hang[-1] + '\n\\end{tabular}\n\\end{table}\n\n'
                        hang_end = '\n'.join(hang)
                        new_cha.append(hang_end)
                    for m in range(len(result_cha)):
                        savelatex = savelatex.replace(result_cha[m], new_cha[m])

                pattern_pic = re.compile(r'!\[.*?\]\(.*?\)')
                result_pic = pattern_pic.findall(savelatex)
                pic_new = []
                for i in range(len(result_pic)):
                    pa_ttl = re.compile(r'\[(.*?)\]')
                    rt_ttl = pa_ttl.findall(result_pic[i])
                    str_ttl = ''.join(rt_ttl)
                    ttl = 'Image caption'
                    if str_ttl != '':
                        ttl = str_ttl
                    pattern_pic1 = re.compile(r'\(.*?\.[a-zA-Z]+\)')
                    result_pic1 = pattern_pic1.findall(result_pic[i])
                    pic1 = ''.join(result_pic1)
                    pic1 = pic1.replace('(', '')
                    pic1 = pic1.replace(')', '')
                    pic_full = '\\begin{figure}[!htb]\n\\centering\n\\includegraphics[width=0.9\\textwidth]{' + pic1 + '}\n\\caption{'+ ttl +'}\n\\end{figure}'
                    pic_new.append(pic_full)
                    continue
                for i in range(len(result_pic)):
                    savelatex = savelatex.replace(result_pic[i], pic_new[i])

                pattern_url = re.compile(r'\[.*?\]\(.*?\)')
                result_url = pattern_url.findall(savelatex)
                ideal_new = []
                for i in range(len(result_url)):
                    pattern_url1 = re.compile(r'\[.*?\]')
                    result_url1 = pattern_url1.findall(result_url[i])
                    result_back = ''.join(result_url1)
                    result_back = result_back.replace('[', '{')
                    result_back = result_back.replace(']', '}')
                    pattern_url2 = re.compile(r'\(.*?\)')
                    result_url2 = pattern_url2.findall(result_url[i])
                    result_front = ''.join(result_url2)
                    result_front = result_front.replace('(', '\\href{')
                    result_front = result_front.replace(')', '}')
                    ideal_full = result_front + result_back
                    ideal_new.append(ideal_full)
                    continue
                for i in range(len(result_url)):
                    savelatex = savelatex.replace(result_url[i], ideal_new[i])

                savelatex = re.sub("\*\*(.*?)\*\*", r'\\textbf{\1}', savelatex)
                savelatex = re.sub("\*(.*?)\*", r'\\textit{\1}', savelatex)
                savelatex = re.sub("```([\s\S]*?)```", r'\\begin{lstlisting}\1\\end{lstlisting}', savelatex)
                savelatex = re.sub("`(.*?)`", r'\\lstinline{\1}', savelatex)
                savelatex = re.sub("<(.*?)>", r'\\href{\1}{\1}', savelatex)

                pattern_emu = re.compile(r'\n(\d+\.\s.*?\n)')
                result_emu = pattern_emu.findall(savelatex)
                mae_emu = '\\begin{enumerate}\n\n\n'
                end_emu = '\n\\end{enumerate}\n'
                mid_emu = '\n\\end{enumerate}\n\n\\begin{enumerate}\n\n\n'
                if result_emu != []:
                    for i in range(len(result_emu)):
                        savelatex = savelatex.replace(result_emu[i], mae_emu + result_emu[i] + end_emu)
                    savelatex = savelatex.replace(mid_emu, '\n')
                    savelatex = re.sub("\n\d+\..", r'\\item ', savelatex)

                savelatex = savelatex.replace('---', '{\\noindent}	 \\rule[-10pt]{17.5cm}{0.05em}\\\\')

                pattern_ite = re.compile(r'\n(-\s.*?\n)')
                result_ite = pattern_ite.findall(savelatex)
                mae_ite = '\\begin{itemize}\n\n\n'
                end_ite = '\n\\end{itemize}\n'
                mid_ite = '\n\\end{itemize}\n\n\\begin{itemize}\n\n\n'
                if result_ite != []:
                    for i in range(len(result_ite)):
                        savelatex = savelatex.replace(result_ite[i], mae_ite + result_ite[i] + end_ite)
                    savelatex = savelatex.replace(mid_ite, '\n')
                    savelatex = savelatex.replace('\n- ', '\\item ')

                chapterrep = codecs.open(BasePath + 'chapterreplacesection.txt', 'r', encoding='utf-8').read()
                if chapterrep == '1':
                    savelatex = savelatex.replace('\\section', '\\chapter')
                    savelatex = savelatex.replace('\\subsection', '\\section')
                    savelatex = savelatex.replace('\\subsubsection', '\\subsection')
                    savelatex = savelatex.replace('\\paragraph', '\\subsubsection')

                part_d = '\n' + savelatex
                if self.widgettem.currentIndex() == 5:
                    savelatex = savelatex.replace('\\begin{figure}', '\\begin{figure*}')
                    savelatex = savelatex.replace('\\end{figure}', '\\end{figure*}')
                    part_d = '\n' + savelatex
                if self.widgettem.currentIndex() == 6:
                    savelatex = savelatex.replace('\\section', '\\newpage\n\n\\section')
                    savelatex = savelatex.replace('\\subsection', '\\newpage\n\n\\subsection')
                    savelatex = savelatex.replace('\\subsubsection', '\\newpage\n\n\\subsubsection')
                    part_d = '\n' + savelatex

                part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
\\renewcommand\\refname{参考文献}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 1:
                    part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
\\renewcommand\\refname{References}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 2:
                    part_e = ''
                if self.widgettem.currentIndex() == 3:
                    part_e = ''
                if self.widgettem.currentIndex() == 4:
                    part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\renewcommand\\refname{References}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 5:
                    part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{multicols}
\\newpage%新一页

\\begin{multicols}{2}\\songti \\zihao{5}%宋体字
\\renewcommand\\refname{参考文献}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 6:
                    part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\newpage
\\section{参考文献}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 7:
                    part_e = '\n\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\renewcommand\\refname{参考文献}
\\begin{thebibliography}{99}'''
                if self.widgettem.currentIndex() == 8:
                    part_e = '\n\n' + self.template_p5

                preref = codecs.open(BasePath + 'path_ref.txt', 'r', encoding='utf-8').read()
                preref = preref.replace('[[', '')
                preref = preref.replace(']]', '')
                preref = preref.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('{', '\\{').replace('}', '\\}')
                if preref != '':
                    ref2 = re.sub(r"\[.*]: ", '', preref)
                    reflist = ref2.split('\n')
                    i = 0
                    while i >= 0 and i <= len(reflist) - 1:
                        reflist[i] = ''.join(lazy_pinyin(reflist[i][0])) + '☆' + reflist[i]
                        reflist[i] = ''.join(reflist[i])
                        i = i + 1
                        continue
                    reflist2 = sorted(reflist, reverse=False, key=str.lower)
                    reftostr = '\n'.join(reflist2)
                    reftostr = re.sub(r"[a-zA-Z]+☆", '', reftostr)
                    reftostrli = reftostr.split('\n')
                    i = 0
                    while i >= 0 and i <= len(reftostrli) - 1:
                        reftostrli[i] = "\\" + 'bibitem{ref' + str(i + 1) + '}' + reftostrli[i]
                        reftostrli[i] = ''.join(reftostrli[i])
                        i = i + 1
                        continue
                    reflat = '\n'.join(reftostrli)
                    reflat = re.sub("\*(.*?)\*", r'\\textit{\1}', reflat)
                    with open(BasePath + 'path_lat.txt', 'w', encoding='utf-8') as flat:
                        flat.write(reflat)
                if preref == '':
                    with open(BasePath + 'path_lat.txt', 'w', encoding='utf-8') as flat:
                        flat.write('')
                biblat = codecs.open(BasePath + 'path_lat.txt', 'r', encoding='utf-8').read()
                part_f = '\n' + biblat
                if self.widgettem.currentIndex() == 2:
                    part_f = ''
                if self.widgettem.currentIndex() == 3:
                    part_f = ''

                part_g = '\n' + '''\\end{thebibliography} 
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
\\end{document}'''
                if self.widgettem.currentIndex() == 1:
                    part_g = '\n' + '''\\end{thebibliography}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{document}'''
                if self.widgettem.currentIndex() == 2:
                    part_g = '\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{document}'''
                if self.widgettem.currentIndex() == 3:
                    part_g = '\n' + '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{document}'''
                if self.widgettem.currentIndex() == 4:
                    part_g = '\n' + '''\\end{thebibliography}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
\\end{document}'''
                if self.widgettem.currentIndex() == 5:
                    part_g = '\n' + '''\\end{thebibliography} 
\\end{multicols} 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{document}'''
                if self.widgettem.currentIndex() == 6:
                    part_g = '\n' + '''\\end{thebibliography} 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{document}'''
                if self.widgettem.currentIndex() == 7:
                    part_g = '\n' + '''\\end{thebibliography}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\end{CJK*}
\\end{document}'''
                if self.widgettem.currentIndex() == 8:
                    part_g = '\n' + self.template_p6

                tarname10 = base_name_noext + ".tex"
                fulldir10 = os.path.join(path1, tarname10)
                lattex = part_a + part_b + part_c + part_d + part_e + part_f + part_g
                with open(fulldir10, 'a', encoding='utf-8') as f0:
                    f0.write('')
                with open(fulldir10, 'w', encoding='utf-8') as f1:
                    f1.write(lattex)

            itemold = self.choosepart.currentText()
            self.choosepart.clear()
            self.choosepart.addItems(['Append at the end (default)', 'Append at the current cursor'])
            pathscr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            fulldir1, tarname1 = _resolve_path(pathscr, str(self.leii1.text()), ".md")
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
            result2 = '☆'.join(result)
            if result != []:
                result = result2.replace('#', '')
                result = result.replace('# ', '')
                result = result.replace('Q/P: ', '')
                result = result.split('☆')
                if 'References ' in result:
                    result.remove('References ')
                for i in range(len(result)):
                    result[i] = 'After ' + result[i]
                    result[i] = ''.join(result[i])
                self.choosepart.addItems(result)
                if itemold in result:
                    itemnub = result.index(itemold) + 2
                    self.choosepart.setCurrentIndex(itemnub)
                if itemold not in result:
                    self.choosepart.setCurrentIndex(0)

            oldv = self.textii2.verticalScrollBar().value()
            oldmax = self.textii2.verticalScrollBar().maximum()
            pathend = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                fulldirend, tarnameend = _resolve_path(pathend, str(self.leii1.text()), ".md")
                if self.leii1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self._show_inspiration_content(contend)
                    newbar = self.textii2.verticalScrollBar()
                    if oldmax != 0 and newbar.maximum() != 0:
                        proportion_old = oldv / oldmax
                        newbar.setValue(int(newbar.maximum() * proportion_old))
                    if newbar.maximum() != 0:
                        proportion = newbar.value() / newbar.maximum()
                        tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
                        self.real2.verticalScrollBar().setValue(tar_pro)

            pathend2 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.textii3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                fulldirend, tarnameend = _resolve_path(pathend2, str(self.leii1.text()), ".tex")
                if self.leii1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.textii3.setPlainText(contend)
                    self.textii3.ensureCursorVisible()  # 游标可用
                    cursor = self.textii3.textCursor()  # 设置游标
                    pos = len(self.textii3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.textii3.setTextCursor(cursor)  # 滚动到游标位置

    def savelat(self):
        if self.leii1.text() != '' and self.textii3.toPlainText() != '':
            path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.textii3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                patterna = re.compile(r'title\{.*}')
                resultq = patterna.findall(self.textii3.toPlainText())
                resultq = ''.join(resultq)
                resultq = resultq.replace('title{', '')
                resultq = resultq.replace('}', '')
                oldnam = codecs.open(BasePath + 'path_std.txt', 'r', encoding='utf-8').read()
                if oldnam != resultq:
                    self.leii1.setText(resultq)
                tarname1 = str(self.leii1.text()) + ".tex"
                fulldir1 = os.path.join(path1, tarname1)
                saved = self.textii3.toPlainText()
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

            pathend2 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if pathend2 == '':
                self.textii3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.leii1.text()) + ".tex"
                fulldirend = os.path.join(pathend2, tarnameend)
                if self.leii1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.textii3.setPlainText(contend)
                    self.textii3.ensureCursorVisible()  # 游标可用
                    cursor = self.textii3.textCursor()  # 设置游标
                    pos = len(self.textii3.toPlainText())  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.textii3.setTextCursor(cursor)  # 滚动到游标位置

    def save3(self):
        path1 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lec0.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s3.toPlainText()
            if self.lec0.text() != '' and self.text_s3.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.lec0.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.lec0.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text_s3.setPlainText(contend)
                self.text_s3.ensureCursorVisible()  # 游标可用
                cursor = self.text_s3.textCursor()  # 设置游标
                pos = len(self.text_s3.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text_s3.setTextCursor(cursor)  # 滚动到游标位置

    def save4(self):
        path1 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lem1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s4.toPlainText()
            if self.lem1.text() != '' and self.text_s4.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.lem1.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.lem1.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.text_s4.setPlainText(contend)
                self.text_s4.ensureCursorVisible()  # 游标可用
                cursor = self.text_s4.textCursor()  # 设置游标
                pos = len(self.text_s4.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.text_s4.setTextCursor(cursor)  # 滚动到游标位置

    def focuson(self):
        if action5.isChecked():
            action10.setChecked(False)
            action10.setVisible(False)
            self.main2.setVisible(False)
            self.mainii2.setVisible(False)
            # self.mainii3.setVisible(False)
            # self.main3.setVisible(False)
            action5.setChecked(True)
            btna2.setChecked(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
        else:
            action10.setVisible(True)
            self.main2.setVisible(True)
            self.mainii2.setVisible(True)
            #self.mainii3.setVisible(True)
            #self.main3.setVisible(True)
            action5.setChecked(False)
            btna2.setChecked(False)

    def focuson2(self):
        if btna2.isChecked():
            action10.setChecked(False)
            action10.setVisible(False)
            self.mainii2.setVisible(False)
            self.main2.setVisible(False)
            # self.mainii3.setVisible(False)
            # self.main3.setVisible(False)
            action5.setChecked(True)
            btna2.setChecked(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
        else:
            action10.setVisible(True)
            self.mainii2.setVisible(True)
            self.main2.setVisible(True)
            #self.mainii3.setVisible(True)
            #self.main3.setVisible(True)
            action5.setChecked(False)
            btna2.setChecked(False)

    def editoron(self):
        if action6.isChecked():
            action10.setChecked(False)
            action10.setVisible(False)
            self.description_box.setVisible(False)
            self.t2.setVisible(False)
            action6.setChecked(True)
            btna3.setChecked(True)
            action5.setChecked(False)
            btna2.setChecked(False)
            self.mainii2.setVisible(True)
            self.main2.setVisible(True)
            # self.main3.setVisible(True)
            # self.mainii3.setVisible(True)
            self.btn_insia.setVisible(True)
            self.btn_edit_refsa.setVisible(True)
            self.btn_toggle_insp_viewa.setVisible(True)
        else:
            action10.setVisible(True)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            # self.main3.setVisible(True)
            # self.mainii3.setVisible(True)
            self.btn_insia.setVisible(False)
            self.btn_edit_refsa.setVisible(False)
            self.btn_toggle_insp_viewa.setVisible(False)

    def editoron2(self):
        if btna3.isChecked():
            action10.setChecked(False)
            action10.setVisible(False)
            self.description_box.setVisible(False)
            self.t2.setVisible(False)
            action6.setChecked(True)
            btna3.setChecked(True)
            action5.setChecked(False)
            btna2.setChecked(False)
            self.mainii2.setVisible(True)
            self.main2.setVisible(True)
            # self.main3.setVisible(True)
            # self.mainii3.setVisible(True)
            self.btn_insia.setVisible(True)
            self.btn_edit_refsa.setVisible(True)
            self.btn_toggle_insp_viewa.setVisible(True)
        else:
            action10.setVisible(True)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            # self.main3.setVisible(True)
            # self.mainii3.setVisible(True)
            self.btn_insia.setVisible(False)
            self.btn_edit_refsa.setVisible(False)
            self.btn_toggle_insp_viewa.setVisible(False)

    def realon(self):
        MOST_WEIGHT = int(self.screen().availableGeometry().width() * 0.75)
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())

        if action7.isChecked():
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            full_md = ''
            path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if self.leii1.text() == '':
                full_md = ''
            else:
                if path_scr != '' and self.leii1.text() != '':
                    tarname = str(self.leii1.text()) + ".md"
                    fulldir = os.path.join(path_scr, tarname)
                    if os.path.exists(fulldir):
                        full_md = codecs.open(fulldir, 'r', encoding='utf-8').read()
                if full_md == '':
                    head_md = self._build_inspiration_header()
                    body_md = self.textii2.toPlainText().rstrip('\n')
                    foot_md = self._build_inspiration_references()
                    full_md = head_md + '\n' + body_md + foot_md
            newhtml2 = self.md2html(full_md)
            self.real2.setHtml(newhtml2)
            md = self.carda.toPlainText()
            self.card_rt.setText(md)
            self.card_rt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            md = self.cardb.toPlainText()
            self.card_rt2.setText(md)
            self.card_rt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            action10.setChecked(False)
            action10.setVisible(False)
            btna5.setChecked(True)
            self.mainii3.setVisible(True)
            self.main3.setVisible(True)
            self.bigwi3.setVisible(True)
            self.resize(MOST_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.btn_00.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')
        else:
            action10.setVisible(True)
            self.mainii3.setVisible(False)
            self.main3.setVisible(False)
            self.bigwi3.setVisible(False)
            btna5.setChecked(False)
            self.resize(HALF_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.btn_00.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')

    def realon2(self):
        MOST_WEIGHT = int(self.screen().availableGeometry().width() * 0.75)
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())

        if btna5.isChecked():
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            full_md = ''
            path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if self.leii1.text() == '':
                full_md = ''
            else:
                if path_scr != '' and self.leii1.text() != '':
                    tarname = str(self.leii1.text()) + ".md"
                    fulldir = os.path.join(path_scr, tarname)
                    if os.path.exists(fulldir):
                        full_md = codecs.open(fulldir, 'r', encoding='utf-8').read()
                if full_md == '':
                    head_md = self._build_inspiration_header()
                    body_md = self.textii2.toPlainText().rstrip('\n')
                    foot_md = self._build_inspiration_references()
                    full_md = head_md + '\n' + body_md + foot_md
            newhtml2 = self.md2html(full_md)
            self.real2.setHtml(newhtml2)
            md = self.carda.toPlainText()
            self.card_rt.setText(md)
            self.card_rt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            md = self.cardb.toPlainText()
            self.card_rt2.setText(md)
            self.card_rt2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            action10.setChecked(False)
            action10.setVisible(False)
            action7.setChecked(True)
            self.mainii3.setVisible(True)
            self.main3.setVisible(True)
            self.bigwi3.setVisible(True)
            self.resize(MOST_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.btn_00.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')
        else:
            action10.setVisible(True)
            self.mainii3.setVisible(False)
            self.main3.setVisible(False)
            self.bigwi3.setVisible(False)
            action7.setChecked(False)
            self.resize(HALF_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.btn_00.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')

    def close_re(self):
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())

        self.mainii3.setVisible(False)
        self.main3.setVisible(False)
        self.bigwi3.setVisible(False)
        self.resize(HALF_WEIGHT, DE_HEIGHT)
        with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
            f0.write(str(self.width()))
        action7.setChecked(False)
        btna5.setChecked(False)
        action10.setVisible(True)
        self.tab_bar.setVisible(True)
        if self.i % 2 == 0:
            self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
        if self.i % 2 == 1:
            self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
        btna4.setChecked(True)
        self.btn_00.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #0085FF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #FFFFFF''')

    def compact_mode_on(self):
        QUARTER_WEIGHT = int(self.screen().availableGeometry().width() * 0.25)  # 1/4 screen width
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        if action10.isChecked():
            action5.setChecked(False)
            action5.setVisible(False)
            action6.setChecked(False)
            action6.setVisible(False)
            action7.setChecked(False)
            action7.setVisible(False)
            btna2.setChecked(False)
            btna2.setVisible(False)
            btna3.setChecked(False)
            btna3.setVisible(False)
            self.btnbot_text1.setVisible(False)
            self.btnbot_text2.setVisible(False)
            self.btnbot_text3.setVisible(False)
            self.btnbot_text4.setVisible(False)
            self.btnbot_ins.setVisible(False)
            self.btnbot_ins2.setVisible(False)

            self.cleanup_handler.add(self.page2_box_h)
            self.cleanup_handler.add(self.wings_h_box)
            self.cleanup_handler.add(self.page1_v_box)
            self.cleanup_handler.add(self.page3_v_box)
            self.cleanup_handler.clear()

            self.main2.addTab(self.upper1, 'Info')
            self.newbox = QVBoxLayout()
            self.newbox.addWidget(self.main2)
            self.newbox.addWidget(self.widget0)
            self.newbox.addWidget(self.art_ocr_row)
            self.newbox.addWidget(self.tabs)
            self.art_tab.setLayout(self.newbox)

            self.lew1.setFixedHeight(20)
            self.lew1.setStyleSheet(
                '''font: 13pt;'''
            )
            self.carda.setStyleSheet(
                '''font: 10pt;'''
            )
            self.cardb.setStyleSheet(
                '''font: 10pt;'''
            )
            self.page1_new = QVBoxLayout()
            self.page1_new.addWidget(self.bigwi2)
            self.page1_new.addWidget(self.bigwi1)
            self.word_tab.setLayout(self.page1_new)

            self.page3_new = QVBoxLayout()
            self.page3_new.addWidget(self.mainii2)
            self.page3_new.addWidget(self.t2)
            self.insp_tab.setLayout(self.page3_new)

            self.resize(QUARTER_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.read_t1.setVisible(True)
            self.read_t2.setVisible(True)
            self.read_t7.setVisible(True)
            self.read_t3.setVisible(True)
            self.read_t8.setVisible(True)
            self.read_t4.setVisible(True)
            self.read_t4_doi.setVisible(True)
            self.read_t4_isbn.setVisible(True)
            self.read_t5.setVisible(True)
            self.lbltool06.setVisible(True)
            self.tool8.setVisible(True)
            self.btnx4.setVisible(False)
            self.btn_00.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
        else:
            action5.setVisible(True)
            action6.setVisible(True)
            action7.setVisible(True)
            btna2.setVisible(True)
            btna3.setVisible(True)
            self.btnbot_text1.setVisible(True)
            self.btnbot_text2.setVisible(True)
            self.btnbot_text3.setVisible(True)
            self.btnbot_text4.setVisible(True)
            self.btnbot_ins.setVisible(True)
            self.btnbot_ins2.setVisible(True)

            self.cleanup_handler.add(self.newbox)
            self.cleanup_handler.add(self.page1_new)
            self.cleanup_handler.add(self.page3_new)
            self.cleanup_handler.clear()

            self.main2.removeTab(4)
            self.upper1 = QWidget()
            supper1 = QVBoxLayout()
            supper1.setContentsMargins(0, 10, 0, 0)
            supper1.addWidget(self.read_t1)
            supper1.addWidget(self.read_t2)
            supper1.addWidget(self.read_t7)
            supper1.addWidget(self.read_t3)
            supper1.addWidget(self.web_t3)
            supper1.addWidget(self.read_t8)
            supper1.addWidget(self.web_t8)
            supper1.addWidget(self.read_t4)
            supper1.addWidget(self.read_t5)
            supper1.addWidget(self.read_t6)
            self.upper1.setLayout(supper1)
            self.wings_h_box = QVBoxLayout()
            self.wings_h_box.setContentsMargins(0, 0, 0, 0)
            self.wings_h_box.addWidget(self.upper1)
            self.wings_h_box.addWidget(self.widget0)
            self.wings_h_box.addWidget(self.art_ocr_row)
            self.wings_h_box.addWidget(self.tabs)
            self.description_box.setLayout(self.wings_h_box)

            # qw1 = QWidget()
            # vbox1 = QVBoxLayout()
            # vbox1.setContentsMargins(0, 0, 0, 0)
            # vbox1.addWidget(self.sub_btn_sub1)
            # vbox1.addWidget(self.sub_btn_sub2)
            # vbox1.addWidget(self.sub_btn_sub3)
            # qw1.setLayout(vbox1)

            # qw1_3 = QWidget()
            # vbox1_3 = QHBoxLayout()
            # vbox1_3.setContentsMargins(0, 0, 0, 0)
            # vbox1_3.addWidget(self.sub_widget0)
            # vbox1_3.addWidget(self.sub_widget1)
            # vbox1_3.addWidget(self.sub_lbl1)
            # vbox1_3.addWidget(self.sub_widget2)
            # vbox1_3.addWidget(self.sub_widget4)
            # vbox1_3.addWidget(self.sub_widget5)
            # qw1_3.setLayout(vbox1_3)

            # qw2 = QWidget()
            # vbox2 = QHBoxLayout()
            # vbox2.setContentsMargins(0, 0, 0, 0)
            # vbox2.addWidget(self.sub_text1)
            # vbox2.addWidget(qw1)
            # qw2.setLayout(vbox2)

            # self.bot1 = QWidget()
            # vbox2_1 = QVBoxLayout()
            # vbox2_1.setContentsMargins(20, 0, 20, 0)
            # vbox2_1.addWidget(self.sub_real1)
            # vbox2_1.addWidget(qw1_3)
            # vbox2_1.addWidget(qw2)
            # self.bot1.setLayout(vbox2_1)
            # self.bot1.setFixedHeight(300)
            # self.bot1.setVisible(False)

            # self.qwbotbox = QWidget()
            # botbox = QVBoxLayout()
            # botbox.setContentsMargins(3, 0, 0, 0)
            # botbox.addWidget(self.main2)
            # # botbox.addWidget(self.bot1)
            # self.qwbotbox.setLayout(botbox)

            self.page2_box_h = QHBoxLayout()
            self.page2_box_h.addWidget(self.description_box, 1)
            self.page2_box_h.addWidget(self.main2, 1)
            self.page2_box_h.addWidget(self.main3, 1)
            self.art_tab.setLayout(self.page2_box_h)

            self.lew1.setFixedHeight(60)
            self.lew1.setStyleSheet(
                '''font: 30pt;'''
            )
            self.carda.setStyleSheet(
                '''font: 30pt;'''
            )
            self.cardb.setStyleSheet(
                '''font: 30pt;'''
            )
            self.page1_v_box = QHBoxLayout()
            self.page1_v_box.addWidget(self.bigwi1, 1)
            self.page1_v_box.addWidget(self.bigwi2, 1)
            self.page1_v_box.addWidget(self.bigwi3, 1)
            self.word_tab.setLayout(self.page1_v_box)

            # qa1 = QWidget()
            # vbox1 = QVBoxLayout()
            # vbox1.setContentsMargins(0, 0, 0, 0)
            # vbox1.addWidget(self.sub2_btn_sub21)
            # vbox1.addWidget(self.sub2_btn_sub22)
            # vbox1.addWidget(self.sub2_btn_sub23)
            # qa1.setLayout(vbox1)

            # qa1_3 = QWidget()
            # vbox1_3 = QHBoxLayout()
            # vbox1_3.setContentsMargins(0, 0, 0, 0)
            # vbox1_3.addWidget(self.sub2_widget0)
            # vbox1_3.addWidget(self.sub2_widget1)
            # vbox1_3.addWidget(self.sub2_lbl1)
            # vbox1_3.addWidget(self.sub2_widget2)
            # vbox1_3.addWidget(self.sub2_widget4)
            # vbox1_3.addWidget(self.sub2_widget5)
            # qa1_3.setLayout(vbox1_3)

            # qa2 = QWidget()
            # vbox2 = QHBoxLayout()
            # vbox2.setContentsMargins(0, 0, 0, 0)
            # vbox2.addWidget(self.sub2_text1)
            # vbox2.addWidget(qa1)
            # qa2.setLayout(vbox2)

            # self.bot2 = QWidget()
            # vbox2_1 = QVBoxLayout()
            # vbox2_1.setContentsMargins(20, 0, 20, 0)
            # vbox2_1.addWidget(self.sub2_real1)
            # vbox2_1.addWidget(qa1_3)
            # vbox2_1.addWidget(qa2)
            # self.bot2.setLayout(vbox2_1)
            # self.bot2.setFixedHeight(300)
            # self.bot2.setVisible(False)

            # self.qabotbox2 = QWidget()
            # botbox = QVBoxLayout()
            # botbox.setContentsMargins(3, 0, 0, 0)
            # botbox.addWidget(self.mainii2)
            # # botbox.addWidget(self.bot2)
            # self.qabotbox2.setLayout(botbox)

            self.page3_v_box = QHBoxLayout()
            self.page3_v_box.addWidget(self.t2, 1)
            self.page3_v_box.addWidget(self.mainii2, 1)
            self.page3_v_box.addWidget(self.mainii3, 1)
            self.insp_tab.setLayout(self.page3_v_box)

            self.resize(HALF_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(str(self.width()))
            if self.i % 2 == 0:
                self.move_window(SCREEN_WEIGHT - 10, self.pos().y())
            if self.i % 2 ==1:
                self.move_window(SCREEN_WEIGHT - self.width() - 3, self.pos().y())
            btna4.setChecked(True)
            self.read_t1.setVisible(True)
            self.read_t2.setVisible(True)
            self.read_t7.setVisible(True)
            self.read_t3.setVisible(True)
            self.read_t8.setVisible(True)
            self.read_t4.setVisible(True)
            self.read_t4_doi.setVisible(True)
            self.read_t4_isbn.setVisible(True)
            self.read_t5.setVisible(True)
            self.lbltool06.setVisible(True)
            self.tool8.setVisible(True)
            self.btnx4.setVisible(True)
            self.btnx4.setStyleSheet('''
                QPushButton{
                border: transparent;
                background-color: transparent;
                border-image: url(/Applications/Strawberry.app/Contents/Resources/up.png);
                }
                QPushButton:pressed{
                border: 1px outset grey;
                background-color: #0085FF;
                border-radius: 4px;
                padding: 1px;
                color: #FFFFFF
                }
                ''')
            self.btn_00.setStyleSheet('''
                border: 1px outset grey;
                background-color: #0085FF;
                border-radius: 4px;
                padding: 1px;
                color: #FFFFFF''')
            self.mainii3.setVisible(False)
            self.main3.setVisible(False)

    def addtable(self):
        if self.leii3.text() != '' and self.leii4.text() != '':
            path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path3 != '' and self.leii1.text() != '':
                def _candidate_names(raw):
                    cands = [raw]
                    try:
                        import re as _re
                        base1 = _re.sub(r'\s*\d{8,20}$', '', raw).rstrip()
                        if base1 and base1 not in cands:
                            cands.append(base1)
                        base2 = _re.sub(r'\s*\d{8,20}$', '', base1).rstrip()
                        if base2 and base2 not in cands:
                            cands.append(base2)
                    except Exception:
                        pass
                    return cands
                fulldir4 = ''
                for nm in _candidate_names(str(self.leii1.text())):
                    cand = os.path.join(path3, nm + ".md")
                    if os.path.exists(cand):
                        fulldir4 = cand
                        break
                if fulldir4 == '':
                    tarname4 = str(self.leii1.text()) + ".md"
                    fulldir4 = os.path.join(path3, tarname4)
                with open(fulldir4, 'a', encoding='utf-8') as f0:
                    f0.write('')

                # 构造表格 Markdown，遵循原始列/行逻辑
                c_part1 = '| x |'
                c_part2 = '|:-:|'
                colomn_num = 1
                if int(self.leii4.text()) <= 1:
                    colomn_num = 1
                if int(self.leii4.text()) > 1:
                    colomn_num = int(self.leii4.text())
                row_num = 1
                if int(self.leii3.text()) <= 1:
                    row_num = 1
                if int(self.leii3.text()) > 1:
                    row_num = int(self.leii3.text()) - 1

                part0 = '\n'
                part1 = c_part1 * colomn_num
                part1 = part1.replace('||', '|')
                part1 = '\n' + part1
                part2 = c_part2 * colomn_num
                part2 = part2.replace('||', '|')
                part2 = '\n' + part2
                table_md = part0 + part1 + part2 + part1 * row_num

                contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                body_now = self._strip_inspiration_body(contm).rstrip('\n')
                if body_now.strip() == '':
                    body_now = '# ' + str(self.leii1.text())

                tail = codecs.open(BasePath + 'path_pat.txt', 'r', encoding='utf-8').read()
                tail_cursor = codecs.open(BasePath + 'currentcursor2.txt', 'r', encoding='utf-8').read()
                idx = self.choosepart.currentIndex()
                last = self.choosepart.count() - 1
                if idx == 1:
                    insert_pos = None
                    if tail_cursor != '' and len(tail_cursor) <= len(body_now):
                        if body_now.endswith(tail_cursor):
                            insert_pos = len(body_now) - len(tail_cursor)
                        else:
                            candidate = body_now.rfind(tail_cursor)
                            if candidate != -1:
                                insert_pos = candidate
                    if insert_pos is None:
                        try:
                            pos_str = codecs.open(BasePath + 'cite_position_idx.txt', 'r', encoding='utf-8').read().strip()
                            insert_pos = int(pos_str) if pos_str != '' else len(body_now)
                        except Exception:
                            insert_pos = len(body_now)
                    insert_pos = max(0, min(len(body_now), insert_pos))
                    suffix = body_now[insert_pos:]
                    with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                        f0.write(suffix)
                    prev_suppress = getattr(self, '_suppress_cursor_capture', False)
                    self._suppress_cursor_capture = True
                    try:
                        new_body = body_now[:insert_pos] + table_md + suffix
                        new_cursor_pos = insert_pos + len(table_md)
                    finally:
                        self._suppress_cursor_capture = prev_suppress
                elif idx == 0 or idx == last:
                    new_body = body_now + table_md
                else:
                    new_body = body_now.replace(tail, table_md + tail, 1) if tail in body_now else body_now + table_md

                new_body = new_body.rstrip('\n')
                prev_suppress = getattr(self, '_suppress_cursor_capture', False)
                self._suppress_cursor_capture = True
                try:
                    self._write_inspiration_body(new_body)
                    if idx == 1:
                        body_len = len(self.textii2.toPlainText())
                        new_cursor_pos = max(0, min(body_len, new_cursor_pos))
                        cursor = self.textii2.textCursor()
                        cursor.setPosition(new_cursor_pos)
                        self.textii2.setTextCursor(cursor)
                        with open(BasePath + 'cite_position_idx.txt', 'w', encoding='utf-8') as f0:
                            f0.write(str(new_cursor_pos))
                        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                            f0.write(self.textii2.toPlainText()[new_cursor_pos:])
                finally:
                    self._suppress_cursor_capture = prev_suppress

                self.leii3.clear()
                self.leii4.clear()

    def addimage(self):
        path3 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path3 != '' and self.leii1.text() != '':
            def _candidate_names(raw):
                cands = [raw]
                try:
                    import re as _re
                    base1 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', raw).rstrip()
                    if base1 and base1 not in cands:
                        cands.append(base1)
                    base2 = _re.sub(r'\s+(?:record\s*)?\d{8,20}$', '', base1).rstrip()
                    if base2 and base2 not in cands:
                        cands.append(base2)
                except Exception:
                    pass
                return cands
            fulldir4 = ''
            for nm in _candidate_names(str(self.leii1.text())):
                cand = os.path.join(path3, nm + ".md")
                if os.path.exists(cand):
                    fulldir4 = cand
                    break
            if fulldir4 == '':
                tarname4 = str(self.leii1.text()) + ".md"
                fulldir4 = os.path.join(path3, tarname4)
            with open(fulldir4, 'a', encoding='utf-8') as f0:
                f0.write('')
            contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path3)
            if file_name != '':
                caption = 'Image caption'
                if self.leii5.text() != '':
                    caption = str(self.leii5.text())
                insertion = '\n\n![' + caption + '](' + str(file_name) + ')'

                body_now = self._strip_inspiration_body(contm).rstrip('\n')
                if body_now.strip() == '':
                    body_now = '# ' + str(self.leii1.text())

                tail = codecs.open(BasePath + 'path_pat.txt', 'r', encoding='utf-8').read()
                tail_cursor = codecs.open(BasePath + 'currentcursor2.txt', 'r', encoding='utf-8').read()
                idx = self.choosepart.currentIndex()
                last = self.choosepart.count() - 1
                if idx == 1:
                    insert_pos = None
                    if tail_cursor != '' and len(tail_cursor) <= len(body_now):
                        if body_now.endswith(tail_cursor):
                            insert_pos = len(body_now) - len(tail_cursor)
                        else:
                            candidate = body_now.rfind(tail_cursor)
                            if candidate != -1:
                                insert_pos = candidate
                    if insert_pos is None:
                        try:
                            pos_str = codecs.open(BasePath + 'cite_position_idx.txt', 'r', encoding='utf-8').read().strip()
                            insert_pos = int(pos_str) if pos_str != '' else len(body_now)
                        except Exception:
                            insert_pos = len(body_now)
                    insert_pos = max(0, min(len(body_now), insert_pos))
                    suffix = body_now[insert_pos:]
                    with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                        f0.write(suffix)
                    prev_suppress = getattr(self, '_suppress_cursor_capture', False)
                    self._suppress_cursor_capture = True
                    try:
                        new_body = body_now[:insert_pos] + insertion + suffix
                        new_cursor_pos = insert_pos + len(insertion)
                    finally:
                        self._suppress_cursor_capture = prev_suppress
                elif idx == 0 or idx == last:
                    new_body = body_now + insertion
                else:
                    new_body = body_now.replace(tail, insertion + tail, 1) if tail in body_now else body_now + insertion

                new_body = new_body.rstrip('\n')
                prev_suppress = getattr(self, '_suppress_cursor_capture', False)
                self._suppress_cursor_capture = True
                try:
                    self._write_inspiration_body(new_body)
                    if idx == 1:
                        body_len = len(self.textii2.toPlainText())
                        new_cursor_pos = max(0, min(body_len, new_cursor_pos))
                        cursor = self.textii2.textCursor()
                        cursor.setPosition(new_cursor_pos)
                        self.textii2.setTextCursor(cursor)
                        with open(BasePath + 'cite_position_idx.txt', 'w', encoding='utf-8') as f0:
                            f0.write(str(new_cursor_pos))
                        with open(BasePath + 'path_pat.txt', 'w', encoding='utf-8') as f0:
                            f0.write(self.textii2.toPlainText()[new_cursor_pos:])
                finally:
                    self._suppress_cursor_capture = prev_suppress

                self.leii5.clear()

    def md2html(self, mdstr):
        extras = ['code-friendly', 'fenced-code-blocks', 'footnotes', 'tables', 'code-color', 'pyshell', 'nofollow',
                  'cuddled-lists', 'header ids', 'nofollow']

        html = """
        <html>
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <style>
            .hll { background-color: #ffffcc }
            .c { color: #0099FF; font-style: italic } /* Comment */
            .err { color: #AA0000; background-color: #FFAAAA } /* Error */
            .k { color: #006699; font-weight: bold } /* Keyword */
            .o { color: #555555 } /* Operator */
            .ch { color: #0099FF; font-style: italic } /* Comment.Hashbang */
            .cm { color: #0099FF; font-style: italic } /* Comment.Multiline */
            .cp { color: #009999 } /* Comment.Preproc */
            .cpf { color: #0099FF; font-style: italic } /* Comment.PreprocFile */
            .c1 { color: #0099FF; font-style: italic } /* Comment.Single */
            .cs { color: #0099FF; font-weight: bold; font-style: italic } /* Comment.Special */
            .gd { background-color: #FFCCCC; border: 1px solid #CC0000 } /* Generic.Deleted */
            .ge { font-style: italic } /* Generic.Emph */
            .gr { color: #FF0000 } /* Generic.Error */
            .gh { color: #003300; font-weight: bold } /* Generic.Heading */
            .gi { background-color: #CCFFCC; border: 1px solid #00CC00 } /* Generic.Inserted */
            .go { color: #AAAAAA } /* Generic.Output */
            .gp { color: #000099; font-weight: bold } /* Generic.Prompt */
            .gs { font-weight: bold } /* Generic.Strong */
            .gu { color: #003300; font-weight: bold } /* Generic.Subheading */
            .gt { color: #99CC66 } /* Generic.Traceback */
            .kc { color: #006699; font-weight: bold } /* Keyword.Constant */
            .kd { color: #006699; font-weight: bold } /* Keyword.Declaration */
            .kn { color: #006699; font-weight: bold } /* Keyword.Namespace */
            .kp { color: #006699 } /* Keyword.Pseudo */
            .kr { color: #006699; font-weight: bold } /* Keyword.Reserved */
            .kt { color: #007788; font-weight: bold } /* Keyword.Type */
            .m { color: #FF6600 } /* Literal.Number */
            .s { color: #CC3300 } /* Literal.String */
            .na { color: #330099 } /* Name.Attribute */
            .nb { color: #336666 } /* Name.Builtin */
            .nc { color: #00AA88; font-weight: bold } /* Name.Class */
            .no { color: #336600 } /* Name.Constant */
            .nd { color: #9999FF } /* Name.Decorator */
            .ni { color: #999999; font-weight: bold } /* Name.Entity */
            .ne { color: #CC0000; font-weight: bold } /* Name.Exception */
            .nf { color: #CC00FF } /* Name.Function */
            .nl { color: #9999FF } /* Name.Label */
            .nn { color: #00CCFF; font-weight: bold } /* Name.Namespace */
            .nt { color: #330099; font-weight: bold } /* Name.Tag */
            .nv { color: #003333 } /* Name.Variable */
            .ow { color: #000000; font-weight: bold } /* Operator.Word */
            .w { color: #bbbbbb } /* Text.Whitespace */
            .mb { color: #FF6600 } /* Literal.Number.Bin */
            .mf { color: #FF6600 } /* Literal.Number.Float */
            .mh { color: #FF6600 } /* Literal.Number.Hex */
            .mi { color: #FF6600 } /* Literal.Number.Integer */
            .mo { color: #FF6600 } /* Literal.Number.Oct */
            .sa { color: #CC3300 } /* Literal.String.Affix */
            .sb { color: #CC3300 } /* Literal.String.Backtick */
            .sc { color: #CC3300 } /* Literal.String.Char */
            .dl { color: #CC3300 } /* Literal.String.Delimiter */
            .sd { color: #CC3300; font-style: italic } /* Literal.String.Doc */
            .s2 { color: #CC3300 } /* Literal.String.Double */
            .se { color: #CC3300; font-weight: bold } /* Literal.String.Escape */
            .sh { color: #CC3300 } /* Literal.String.Heredoc */
            .si { color: #AA0000 } /* Literal.String.Interpol */
            .sx { color: #CC3300 } /* Literal.String.Other */
            .sr { color: #33AAAA } /* Literal.String.Regex */
            .s1 { color: #CC3300 } /* Literal.String.Single */
            .ss { color: #FFCC33 } /* Literal.String.Symbol */
            .bp { color: #336666 } /* Name.Builtin.Pseudo */
            .fm { color: #CC00FF } /* Name.Function.Magic */
            .vc { color: #003333 } /* Name.Variable.Class */
            .vg { color: #003333 } /* Name.Variable.Global */
            .vi { color: #003333 } /* Name.Variable.Instance */
            .vm { color: #003333 } /* Name.Variable.Magic */
            .il { color: #FF6600 } /* Literal.Number.Integer.Long */
            table {
                    font-family: verdana,arial,sans-serif;
                    font-size:11px;
                    color:#333333;
                    border-width: 1px;
                    border-color: #999999;
                    border-collapse: collapse;
                    }
            th {
                background:#b5cfd2 url('cell-blue.jpg');
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #999999;
                }
            td {
                background:#dcddc0 url('cell-grey.jpg');
                border-width: 1px;
                padding: 8px;
                border-style: solid;
                border-color: #999999;
                }
        </style>
        </head>
        <body>
            %s
        </body>
        </html>
        """
        clean_one = mdstr.replace('\\(', '$').replace('\\)', '$').replace('\\[', '$').replace('\\]', '$')
        clean_two = re.sub(r'\$(.*?)\$', lambda m: '$' + re.sub(r'[\n\t ]+', '', m.group(1)) + '$', clean_one,
                           flags=re.DOTALL)
        clean_three = re.sub(r'\|(\n(\t)*\n(\t)*)\|', '|\n|', clean_two)
        ret = markdown2.markdown(clean_three, extras=extras)
        middlehtml = html % ret
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                body {
                    margin-right: 20px;
                    font-size: 14px;
                    padding: 0;
                    background-color: #F3F2EE;
                }
            </style>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>   
        </head>
        <body>
            %s
            <script type='text/x-mathjax-config'>
            MathJax.Hub.Config({
                displayAlign: 'left',
                displayIndent: '4em',
                tex2jax: {
                    inlineMath: [['$','$'], ['\\\\(','\\\\)']],
                    displayMath: [['$$','$$'], ['\\[','\\]']]
                },
                TeX:{
                    equationNumbers:{
                        autoNumber:"AMS"
                    }
                }
            });
            </script>
        </body>
        </html>
        """ % middlehtml
        return html_content

    def on_text_textChanged(self):
        if self.text.toPlainText() != '' and self.le1.text() != '':
            path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text.toPlainText()
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)
        if action7.isChecked() and self.main2.currentIndex() == 0:
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            # set position
            QTimer.singleShot(100, self.scr_cha)

    def scr_cha(self):
        if self.text.verticalScrollBar().maximum() != 0 and action7.isChecked():
            proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
            tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
            self.real1.verticalScrollBar().setValue(tar_pro)

    def on_text2_textChanged(self):
        if self.insp_updating:
            return
        if self.textii2.toPlainText() != '' and self.leii1.text() != '':
            body_text = self.textii2.toPlainText()
            self._write_inspiration_body(body_text)
        if action7.isChecked():
            full_md = ''
            path_scr = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            if path_scr != '' and self.leii1.text() != '':
                tarname = str(self.leii1.text()) + ".md"
                fulldir = os.path.join(path_scr, tarname)
                if os.path.exists(fulldir):
                    full_md = codecs.open(fulldir, 'r', encoding='utf-8').read()
            if full_md == '':
                head_md = self._build_inspiration_header()
                body_md = self.textii2.toPlainText().rstrip('\n')
                foot_md = self._build_inspiration_references()
                full_md = head_md + '\n' + body_md + foot_md
            newhtml = self.md2html(full_md)
            self.real2.setHtml(newhtml)
            # set position
            QTimer.singleShot(100, self.scr_cha2)

    def scr_cha2(self):
        if self.textii2.verticalScrollBar().maximum() != 0 and action7.isChecked():
            proportion = self.textii2.verticalScrollBar().value() / self.textii2.verticalScrollBar().maximum()
            tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
            self.real2.verticalScrollBar().setValue(tar_pro)

    def on_text_textChanged_concept(self):
        if self.text_s2.toPlainText() != '' and self.lec1.text() != '':
            path1 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lec1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s2.toPlainText()
            if self.lec1.text() != '' and self.text_s2.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)
        if action7.isChecked() and self.main2.currentIndex() == 1:
            md = self.text_s2.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            # set position
            QTimer.singleShot(100, self.scr_cha_concept)

    def scr_cha_concept(self):
        if self.text_s2.verticalScrollBar().maximum() != 0:
            proportion = self.text_s2.verticalScrollBar().value() / self.text_s2.verticalScrollBar().maximum()
            tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
            self.real1.verticalScrollBar().setValue(tar_pro)

    def on_text_textChanged_theory(self):
        if self.text_s3.toPlainText() != '' and self.lec0.text() != '':
            path1 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lec0.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s3.toPlainText()
            if self.lec0.text() != '' and self.text_s3.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)
        if action7.isChecked() and self.main2.currentIndex() == 2:
            md = self.text_s3.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            # set position
            QTimer.singleShot(100, self.scr_cha_theory)

    def scr_cha_theory(self):
        if self.text_s3.verticalScrollBar().maximum() != 0:
            proportion = self.text_s3.verticalScrollBar().value() / self.text_s3.verticalScrollBar().maximum()
            tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
            self.real1.verticalScrollBar().setValue(tar_pro)

    def on_text_textChanged_method(self):
        if self.text_s4.toPlainText() != '' and self.lem1.text() != '':
            path1 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lem1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s4.toPlainText()
            if self.lem1.text() != '' and self.text_s4.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)
        if action7.isChecked() and self.main2.currentIndex() == 3:
            md = self.text_s4.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            # set position
            QTimer.singleShot(100, self.scr_cha_method)

    def scr_cha_method(self):
        if self.text_s4.verticalScrollBar().maximum() != 0:
            proportion = self.text_s4.verticalScrollBar().value() / self.text_s4.verticalScrollBar().maximum()
            tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
            self.real1.verticalScrollBar().setValue(tar_pro)

    def on_realclick(self):
        if action7.isChecked() and self.main2.currentIndex() == 0:
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            if self.text.verticalScrollBar().maximum() != 0:
                proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                self.real1.verticalScrollBar().setValue(tar_pro)
        if action7.isChecked() and self.main2.currentIndex() == 1:
            md = self.text_s2.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            if self.text_s2.verticalScrollBar().maximum() != 0:
                proportion = self.text_s2.verticalScrollBar().value() / self.text_s2.verticalScrollBar().maximum()
                tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                self.real1.verticalScrollBar().setValue(tar_pro)
        if action7.isChecked() and self.main2.currentIndex() == 2:
            md = self.text_s3.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            if self.text_s3.verticalScrollBar().maximum() != 0:
                proportion = self.text_s3.verticalScrollBar().value() / self.text_s3.verticalScrollBar().maximum()
                tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                self.real1.verticalScrollBar().setValue(tar_pro)
        if action7.isChecked() and self.main2.currentIndex() == 3:
            md = self.text_s4.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            if self.text_s4.verticalScrollBar().maximum() != 0:
                proportion = self.text_s4.verticalScrollBar().value() / self.text_s4.verticalScrollBar().maximum()
                tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                self.real1.verticalScrollBar().setValue(tar_pro)
        if self.main2.currentIndex() == 0:
            self.widget0.setVisible(True)
        if self.main2.currentIndex() == 1:
            self.widget0.setVisible(False)
        if self.main2.currentIndex() == 2:
            self.widget0.setVisible(False)
        if self.main2.currentIndex() == 3:
            self.widget0.setVisible(False)
    
    def on_text_textChanged_latex(self):
        if self.textii3.toPlainText() != '' and self.leii1.text() != '':
            path1 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".tex"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.textii3.toPlainText()
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)

    def card1changed(self):
        if self.carda.toPlainText() != '' and self.cardb.toPlainText() != '':
            deck_path = codecs.open(BasePath + 'path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            while '' in ori_lst:
                ori_lst.remove('')
            ori_lst.remove(ori_lst[-1])
            new_cont = '\n'.join(ori_lst) + '\n'
            with open(deck_path, 'w', encoding='utf-8') as f0:
                f0.write(new_cont)
            title = self.carda.toPlainText() + '\t'
            content = self.cardb.toPlainText()
            with open(deck_path, 'a', encoding='utf-8') as f0:
                f0.write(title + content + '\n')
        if action7.isChecked():
            md = self.carda.toPlainText()
            self.card_rt.setText(md)
            self.card_rt.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if self.carda.verticalScrollBar().maximum() != 0:
                proportion = self.carda.verticalScrollBar().value() / self.carda.verticalScrollBar().maximum()
                tar_pro = int(self.card_rt.verticalScrollBar().maximum() * proportion)
                self.card_rt.verticalScrollBar().setValue(tar_pro)

    def card1scroll(self):
        if self.carda.verticalScrollBar().maximum() != 0:
            proportion = self.carda.verticalScrollBar().value() / self.carda.verticalScrollBar().maximum()
            tar_pro = int(self.card_rt.verticalScrollBar().maximum() * proportion)
            self.card_rt.verticalScrollBar().setValue(tar_pro)

    def card2changed(self):
        if self.carda.toPlainText() != '' and self.cardb.toPlainText() != '':
            deck_path = codecs.open(BasePath + 'path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            while '' in ori_lst:
                ori_lst.remove('')
            ori_lst.remove(ori_lst[-1])
            new_cont = '\n'.join(ori_lst) + '\n'
            with open(deck_path, 'w', encoding='utf-8') as f0:
                f0.write(new_cont)
            title = self.carda.toPlainText() + '\t'
            content = self.cardb.toPlainText()
            with open(deck_path, 'a', encoding='utf-8') as f0:
                f0.write(title + content + '\n')
        if action7.isChecked():
            md = self.cardb.toPlainText()
            self.card_rt2.setText(md)
            self.card_rt2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if self.cardb.verticalScrollBar().maximum() != 0:
                proportion = self.cardb.verticalScrollBar().value() / self.cardb.verticalScrollBar().maximum()
                tar_pro = int(self.card_rt2.verticalScrollBar().maximum() * proportion)
                self.card_rt2.verticalScrollBar().setValue(tar_pro)

    def card2scroll(self):
        if self.cardb.verticalScrollBar().maximum() != 0:
            proportion = self.cardb.verticalScrollBar().value() / self.cardb.verticalScrollBar().maximum()
            tar_pro = int(self.card_rt2.verticalScrollBar().maximum() * proportion)
            self.card_rt2.verticalScrollBar().setValue(tar_pro)

    def add_to_wait(self):
        if self.lew1.text() != '':
            home_dir = str(Path.home())
            tarname1 = "StrawberryAppPath"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.mkdir(fulldir1)
            tarname2 = "wordwaitinglist.txt"
            fulldir2 = os.path.join(fulldir1, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            alllist = contend.split('\n')
            for i in range(len(alllist)):
                if alllist[i].lower() == str(self.lew1.text().lower()):
                    wri0 = 'This expression has been on the list!'
                    self.lblexp_2.setText(wri0)
                    self.lew1.clear()
                    continue
                else:
                    continue
            corepart = self.lew1.text().replace('\n', '') + '\n'
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write(corepart)
            contend2 = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            alllist2 = contend2.split('\n')
            alllist2.sort()
            while '' in alllist2:
                alllist2.remove('')
            self.wid_word.clear()
            self.wid_word.addItems(alllist2)
            num = len(alllist2)
            wri = 'There are ' + str(num) + ' expressions on your list now!'
            self.lblexp_2.setText(wri)
            self.lew1.clear()

    def importlist(self):
        home_dir = str(Path.home())
        file_name, ok = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Text Files (*.txt)")
        if file_name != '':
            contend = codecs.open(file_name, 'r', encoding='utf-8').read()
            tarname1 = "StrawberryAppPath"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.mkdir(fulldir1)
            tarname2 = "wordwaitinglist.txt"
            fulldir2 = os.path.join(fulldir1, tarname2)
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write(contend + '\n')
            contend2 = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            alllist2 = contend2.split('\n')
            alllist2.sort()
            while '' in alllist2:
                alllist2.remove('')
            num = len(alllist2)
            wri = 'There are ' + str(num) + ' expressions on your list now!'
            self.lblexp_2.setText(wri)
            self.wid_word.clear()
            self.wid_word.addItems(alllist2)

    def createdeck(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = 'MyDecks'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.mkdir(fulldir2)
        if self.lew2.text() != '':
            endname = self.lew2.text() + '.txt'
            fulldir3 = os.path.join(fulldir2, endname)
            with open(fulldir3, 'w', encoding='utf-8') as f0:
                f0.write('')
            with open(BasePath + 'path_dec.txt', 'w', encoding='utf-8') as f0:
                f0.write(fulldir3)
            self.lew2.setText(endname.replace('.txt', ''))
            self.lew2.setEnabled(False)

    def opendeck(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = 'MyDecks'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.mkdir(fulldir2)
        fj = QFileDialog.getOpenFileName(self, "Open File", fulldir2, "Text Files (*.txt)")
        if fj != '':
            str_fj = ''.join(fj)
            str_fj = str_fj.replace('Text Files (*.txt)', '')
            lst_fj = str_fj.split('/')
            if '.txt' in lst_fj[-1]:
                endname = lst_fj[-1].replace('.txt', '')
                self.lew2.setText(endname)
                self.lew2.setEnabled(False)
                with open(BasePath + 'path_dec.txt', 'w', encoding='utf-8') as f0:
                    f0.write(str_fj)

    def closedeck(self):
        with open(BasePath + 'path_dec.txt', 'w', encoding='utf-8') as f0:
            f0.write('')
        self.lew2.clear()
        self.lew2.setEnabled(True)
        self.carda.clear()
        self.cardb.clear()

    def search_on_web(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "default_link.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write('https://www.collinsdictionary.com/dictionary/english/')

        pre_link = ''
        default_link = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        if default_link != '':
            pre_link = default_link

        searchcon = self.wid_word.currentText()
        fullurl = pre_link + str(searchcon.lower())
        webbrowser.open(fullurl)

    # def search_with_ai(self):
    #     self.btn_aiow.setDisabled(True)
    #     modelnow = codecs.open(BasePath + 'modelnow.txt', 'r', encoding='utf-8').read()
    #     Which = codecs.open(BasePath + 'which.txt', 'r', encoding='utf-8').read()
    #     if Which == '0':
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '':
    #             QApplication.processEvents()
    #             QApplication.restoreOverrideCursor()

    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             try:
    #                 openai.api_key = AccountGPT
    #                 searchcon = str(self.wid_word.currentText().lower())
    #                 conversation_history = """user: You are an expert in the semantic syntax, and you are teaching me expressions.
    #                                         assistant: Yes, I understand. Please give me the expression."""
    #                 prompt = f"""You are an expert in semantics and grammar teaching me how to learn an expression. You should do as follows: 
    #                     1. Explain in {w4.other_3.text()} every meaning of {searchcon} in numeric list;
    #                     2. Provide at least one example sentence after each meaning above accordingly;
    #                     3. If a word is part of an idiom, explain the idiom and a few examples;
    #                     4. Give the synonym, along with their differences and usage scenarios.
    #                     5. The answer should follow the format below:
    #                     ```
    #                     - Meanings:
    #                         1. <part of speech> **meaning1**e.g.: examples
    #                         2. <part of speech> **meaning2**e.g.: examples
    #                     - Idioms: idiom and its meaning
    #                     - Synonyms: synonym and their differences
    #                     ```
    #                     All replies should be in Markdown format. Before it starts, must exactly write "「「start」」" and write "「「end」」" after it ends."""

    #                 tutr = 0.5
    #                 temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                    encoding='utf-8').read()
    #                 if temp != '':
    #                     tutr = float(temp)

    #                 maxt = 1024
    #                 maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                        encoding='utf-8').read()
    #                 if maxtoken != '':
    #                     maxt = int(maxtoken)

    #                 completion = openai.ChatCompletion.create(
    #                     model=modelnow,
    #                     messages=[{"role": "user", "content": conversation_history + prompt}],
    #                     max_tokens=maxt,
    #                     n=1,
    #                     stop=None,
    #                     temperature=tutr,
    #                 )
    #                 message = completion.choices[0].message["content"].strip()
    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()
    #                 pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                 result = pattern.findall(message)
    #                 ResultEnd = ''.join(result)
    #                 ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                 uid = os.getuid()
    #                 env = os.environ.copy()
    #                 env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                 p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                 p.communicate(input=ResultEnd.encode('utf-8'))
    #                 message = ResultEnd
    #                 message = message.lstrip('\n')
    #                 message = message.replace('\n', '\n\n\t')
    #                 message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                 message = '\n\t' + message

    #                 EndMess = '- AI: ' + message
    #                 self.textw1.appendPlainText(EndMess)

    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()
    #             except TimeoutException:
    #                 self.textw1.appendPlainText('Timed out, please try again!')
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 self.textw1.appendPlainText('Error, please try again!')
    #             signal.alarm(0)  # reset timer
    #         if AccountGPT == '':
    #             self.textw1.appendPlainText('You should set your accounts in Settings.')
    #     if Which == '1':
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '':
    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             # Set up your API key
    #             ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    #             api2 = codecs.open(BasePath + 'api2.txt', 'r',
    #                                encoding='utf-8').read()
    #             bear = codecs.open(BasePath + 'bear.txt', 'r',
    #                                encoding='utf-8').read()
    #             thirdp = codecs.open(BasePath + 'third.txt', 'r',
    #                                  encoding='utf-8').read()
    #             if bear != '' and api2 != '' and thirdp == '1':
    #                 ENDPOINT = bear + '/v1/chat/completions'
    #                 AccountGPT = api2
    #             HEADERS = {"Authorization": f"Bearer {AccountGPT}"}
    #             totaltoken = codecs.open(BasePath + 'total.txt', 'r',
    #                                      encoding='utf-8').read()
    #             maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                    encoding='utf-8').read()
    #             prompttoken = int(totaltoken) - int(maxtoken)
    #             try:
    #                 async def chat_gpt(message, conversation_history=None, tokens_limit=prompttoken):
    #                     if conversation_history is None:
    #                         conversation_history = []

    #                     conversation_history.append({"role": "user", "content": message})

    #                     input_text = "".join([f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])

    #                     # Truncate or shorten the input text if it exceeds the token limit
    #                     encoded_input_text = input_text.encode("utf-8")
    #                     while len(encoded_input_text) > tokens_limit:
    #                         conversation_history.pop(0)
    #                         input_text = "".join(
    #                             [f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])
    #                         encoded_input_text = input_text.encode("utf-8")

    #                     tutr = 0.5
    #                     temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                        encoding='utf-8').read()
    #                     if temp != '':
    #                         tutr = float(temp)

    #                     maxt = 1024
    #                     if maxtoken != '':
    #                         maxt = int(maxtoken)

    #                     # Set up the API call data
    #                     data = {
    #                         "model": modelnow,
    #                         "messages": [{"role": "user", "content": input_text}],
    #                         "max_tokens": maxt,
    #                         "temperature": tutr,
    #                         "n": 1,
    #                         "stop": None,
    #                     }

    #                     # Make the API call asynchronously
    #                     async with httpx.AsyncClient() as client:
    #                         response = await client.post(ENDPOINT, json=data, headers=HEADERS, timeout=60.0)

    #                     # Process the API response
    #                     if response.status_code == 200:
    #                         response_data = response.json()
    #                         chat_output = response_data["choices"][0]["message"]["content"].strip()
    #                         return chat_output
    #                     else:
    #                         raise Exception(
    #                             f"API call failed with status code {response.status_code}: {response.text}")

    #                 async def main():
    #                     conversation_history = [{"role": "user", "content": "You are an expert in the semantic syntax, and you are teaching me expressions."},
    #                                    {"role": "assistant", "content": "Yes, I understand. Please give me the expression."}]
    #                     searchcon = str(self.wid_word.currentText().lower())
    #                     prompt = f"""You are an expert in semantics and grammar teaching me how to learn an expression. You should do as follows: 
    #                         1. Explain in {w4.other_3.text()} every meaning of {searchcon} in numeric list;
    #                         2. Provide at least one example sentence after each meaning above accordingly;
    #                         3. If a word is part of an idiom, explain the idiom and a few examples;
    #                         4. Give the synonym, along with their differences and usage scenarios.
    #                         5. The answer should follow the format below:
    #                         ```
    #                         - Meanings:
    #                             1. <part of speech> **meaning1**e.g.: examples
    #                             2. <part of speech> **meaning2**e.g.: examples
    #                         - Idioms: idiom and its meaning
    #                         - Synonyms: synonym and their differences
    #                         ```
    #                         All replies should be in Markdown format. Before it starts, must exactly write "「「start」」" and write "「「end」」" after it ends."""

    #                     response = await chat_gpt(prompt, conversation_history)
    #                     message = response.lstrip('assistant:').strip()
    #                     pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                     result = pattern.findall(message)
    #                     ResultEnd = ''.join(result)
    #                     ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                     uid = os.getuid()
    #                     env = os.environ.copy()
    #                     env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                     p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                     p.communicate(input=ResultEnd.encode('utf-8'))
    #                     message = ResultEnd
    #                     message = message.lstrip('\n')
    #                     message = message.replace('\n', '\n\n\t')
    #                     message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                     message = '\n\t' + message

    #                     EndMess = '- AI: ' + message
    #                     self.textw1.appendPlainText(EndMess)

    #                     QApplication.processEvents()
    #                     QApplication.restoreOverrideCursor()

    #                 asyncio.run(main())
    #             except TimeoutException:
    #                 self.textw1.appendPlainText('Timed out, please try again!')
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 self.textw1.appendPlainText('Error, please try again!')
    #             signal.alarm(0)  # reset timer
    #         if AccountGPT == '':
    #             self.textw1.appendPlainText('You should set your accounts in Settings.')
    #     self.btn_aiow.setDisabled(False)

    def makecard(self):
        if self.textw1.toPlainText() != '' and self.lew2.text() != '' and self.wid_word.currentText() != 'None' and self.wid_word.currentText() != '':
            deck_path = codecs.open(BasePath + 'path_dec.txt', 'r', encoding='utf-8').read()
            part1 = str(self.wid_word.currentText().lower())
            part1_5 = '\t'
            tags = str(self.lew3.text()).replace('、', ' #')
            # 创建一个 markdown 解析器
            markdown = mistune.create_markdown()
            # 将 Markdown 转换为 HTML
            main_part = markdown(self.textw1.toPlainText())
            part2 = main_part.replace('\n', '') + '<br>#' + tags + '\t'
            with open(deck_path, 'a', encoding='utf-8') as f0:
                f0.write(part1 + part1_5 + part2 + '\n')
            home_dir = str(Path.home())
            tarname1 = "StrawberryAppPath"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.mkdir(fulldir1)
            tarname2 = "wordwaitinglist.txt"
            fulldir2 = os.path.join(fulldir1, tarname2)
            ori_con = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            lst_ori = ori_con.split('\n')
            if str(self.wid_word.currentText()) in lst_ori:
                lst_ori.remove(str(self.wid_word.currentText()))
            new_con = '\n'.join(lst_ori)
            with open(fulldir2, 'w', encoding='utf-8') as f0:
                f0.write(new_con)
            contend2 = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            alllist2 = contend2.split('\n')
            alllist2.sort()
            while '' in alllist2:
                alllist2.remove('')
            num = len(alllist2)
            wri = 'There are ' + str(num) + ' words on your list now!'
            self.lblexp_2.setText(wri)
            wlstnum = self.wid_word.currentIndex()
            wlstmax = self.wid_word.count()
            self.wid_word.clear()
            self.wid_word.addItems(alllist2)
            self.textw1.clear()
            self.lew3.clear()
            self.carda.setPlainText(part1)
            self.cardb.setPlainText(part2)
            tarnum = 0
            if wlstnum > 0 and wlstnum < wlstmax - 1:
                tarnum = wlstnum
            if wlstnum == 0:
                tarnum = 0
            if wlstnum != 0 and wlstnum == wlstmax - 1:
                tarnum = wlstnum - 1
            self.wid_word.setCurrentIndex(tarnum)

    def next_card(self):
        self.carda.clear()
        self.cardb.clear()

    def searchmeaning(self):
        if self.lew2.text() != '' and self.lew4.text() != '':
            searchnote = '#' + str(self.lew4.text())
            home_dir = str(Path.home())
            tarname1 = "StrawberryAppPath"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.mkdir(fulldir1)
            tarname2 = 'MyDecks'
            fulldir2 = os.path.join(fulldir1, tarname2)
            tarname3 = str(self.lew2.text()) + ".txt"
            fulldir3 = os.path.join(fulldir2, tarname3)
            ori_dek = codecs.open(fulldir3, 'r', encoding='utf-8').read()
            ori_lst = ori_dek.split('\n')
            new_lst = []
            for i in range(len(ori_lst)):
                if searchnote in ori_lst[i]:
                    new_lst.append(ori_lst[i])
                    continue
                else:
                    continue
            new_lst2 = []
            for i in range(len(new_lst)):
                new_lst[i] = new_lst[i].split('\t')
                while '' in new_lst[i]:
                    new_lst[i].remove('')
                new_lst2.append(new_lst[i])
            new_dict = dict(new_lst2)
            waittopri = str(new_dict.keys())
            waittopri = waittopri.replace('dict_keys([', '')
            waittopri = waittopri.replace('])', '')
            waittopri = waittopri.replace("'", '')
            waittopri = waittopri.replace(', ', '\n')
            self.text_res.setPlainText(waittopri)

    def newsearch(self):
        self.lew4.clear()
        self.text_res.clear()

    def editcardsave(self):
        if self.carda.toPlainText() != '' and self.cardb.toPlainText() != '':
            deck_path = codecs.open(BasePath + 'path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            while '' in ori_lst:
                ori_lst.remove('')
            ori_lst.remove(ori_lst[-1])
            new_cont = '\n'.join(ori_lst) + '\n'
            with open(deck_path, 'w', encoding='utf-8') as f0:
                f0.write(new_cont)
            title = self.carda.toPlainText() + '\t'
            content = self.cardb.toPlainText()
            with open(deck_path, 'a', encoding='utf-8') as f0:
                f0.write(title + content + '\n')

    def timeout_handler(self, signum, frame):
        raise TimeoutException("Timeout")

    def bot1show(self):
        pass
        # self.bot1.setVisible(True)

    # def bot1close(self):
    #     self.bot1.setVisible(False)

    # def bot1send(self):
    #     self.sub_btn_sub1.setDisabled(True)
    #     modelnow = codecs.open(BasePath + 'modelnow.txt', 'r', encoding='utf-8').read()
    #     Which = codecs.open(BasePath + 'which.txt', 'r', encoding='utf-8').read()
    #     if Which == '0':
    #         if self.sub_text1.toPlainText() == '':
    #             a = ''
    #             if self.main2.currentIndex() == 0:
    #                 a = self.text.textCursor().selectedText()
    #             if self.main2.currentIndex() == 1:
    #                 a = self.text_s2.textCursor().selectedText()
    #             if self.main2.currentIndex() == 2:
    #                 a = self.text_s3.textCursor().selectedText()
    #             if self.main2.currentIndex() == 3:
    #                 a = self.text_s4.textCursor().selectedText()
    #             if a == '':
    #                 a = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    #             self.sub_text1.setPlainText(a)
    #         QuesText = self.sub_text1.toPlainText()
    #         QuesText = QuesText.lstrip('\n')
    #         QuesText = QuesText.replace('\n', '\n\n\t')
    #         QuesText = QuesText.replace('\n\n\t\n\n\t', '\n\n\t')
    #         self.sub_LastQ = str(self.sub_text1.toPlainText())
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '' and self.sub_text1.toPlainText() != '':
    #             QApplication.processEvents()
    #             QApplication.restoreOverrideCursor()
    #             self.sub_text1.setReadOnly(True)
    #             md = '- Q: ' + QuesText + '\n\n'
    #             with open(BasePath + 'output.txt', 'a', encoding='utf-8') as f1:
    #                 f1.write(md)
    #             PromText = codecs.open(BasePath + 'output.txt', 'r',
    #                                    encoding='utf-8').read()
    #             newhtml = self.md2html(PromText)
    #             self.sub_real1.setHtml(newhtml)
    #             self.sub_real1.ensureCursorVisible()  # 游标可用
    #             cursor = self.sub_real1.textCursor()  # 设置游标
    #             pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #             cursor.setPosition(pos)  # 游标位置设置为尾部
    #             self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #             QApplication.processEvents()
    #             QApplication.restoreOverrideCursor()
    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             try:
    #                 openai.api_key = AccountGPT
    #                 history = ''
    #                 showhistory = codecs.open(BasePath + 'history.txt', 'r',
    #                                           encoding='utf-8').read()
    #                 if showhistory == '1':
    #                     history = codecs.open(BasePath + 'output.txt', 'r',
    #                                           encoding='utf-8').read().replace('- A: ', '').replace('- Q: ', '')
    #                 prompt = str(self.sub_text1.toPlainText())
    #                 reststr = history + '---' + prompt
    #                 tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-2.7B')
    #                 A = tokenizer.encode(reststr, add_special_tokens=True)
    #                 totaltoken = codecs.open(BasePath + 'total.txt', 'r',
    #                                          encoding='utf-8').read()
    #                 maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                        encoding='utf-8').read()
    #                 prompttoken = int(totaltoken) - int(maxtoken)
    #                 while len(A) >= prompttoken:
    #                     AllList = reststr.split('---')
    #                     while '' in AllList:
    #                         AllList.remove('')
    #                     while '\n\n' in AllList:
    #                         AllList.remove('\n\n')
    #                     del AllList[0]
    #                     reststr = '---'.join(AllList)
    #                     A = tokenizer.encode(reststr, add_special_tokens=True)
    #                     continue
    #                 if self.sub_widget0.currentIndex() == 0:
    #                     prompt = reststr
    #                 if self.sub_widget0.currentIndex() == 1:
    #                     prompt = f"""You are a translation engine that can only translate text and cannot interpret it. Translate this text from {self.sub_widget1.currentText()} to {self.sub_widget2.currentText()}. Don’t reply any other explanations. Before the translated text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                 if self.sub_widget0.currentIndex() == 2:
    #                     prompt = f"""Revise the text in {self.sub_widget4.currentText()} to remove grammar mistakes and make it more clear, concise, and coherent. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                 if self.sub_widget0.currentIndex() == 3:
    #                     prompt = f"""You are a text summarizer, you can only summarize the text, don't interpret it. Summarize this text in {self.sub_widget4.currentText()} to make it shorter, logical and clear. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                 if self.sub_widget0.currentIndex() == 4:
    #                     prompt = f"""You are an expert in semantics and grammar, teaching me how to learn. Please explain in {self.sub_widget4.currentText()} the meaning of every word in the text above and the meaning and the grammar structure of the text. If a word is part of an idiom, please explain the idiom and provide a few examples in {self.sub_widget4.currentText()} with similar meanings, along with their explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                 if self.sub_widget0.currentIndex() == 5:
    #                     prompt = f"""You are a code explanation engine, you can only explain the code, do not interpret or translate it. Also, please report any bugs you find in the code to the author of the code. Must repeat in {self.sub_widget4.currentText()}. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Code: {str(self.sub_text1.toPlainText())}. """

    #                 selectedtext = ''
    #                 if self.main2.currentIndex() == 0:
    #                     selectedtext = self.text.textCursor().selectedText()
    #                 if self.main2.currentIndex() == 1:
    #                     selectedtext = self.text_s2.textCursor().selectedText()
    #                 if self.main2.currentIndex() == 2:
    #                     selectedtext = self.text_s3.textCursor().selectedText()
    #                 if self.main2.currentIndex() == 3:
    #                     selectedtext = self.text_s4.textCursor().selectedText()
    #                 if selectedtext != '':
    #                     prompt = 'Please answer the prompt according to the context. <context starts> ' + selectedtext + '<context ends>. The prompt: ' + prompt

    #                 tutr = 0.5
    #                 temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                    encoding='utf-8').read()
    #                 if temp != '':
    #                     tutr = float(temp)

    #                 maxt = 1024
    #                 if maxtoken != '':
    #                     maxt = int(maxtoken)

    #                 completion = openai.ChatCompletion.create(
    #                     model=modelnow,
    #                     messages=[{"role": "user", "content": prompt}],
    #                     max_tokens=maxt,
    #                     n=1,
    #                     stop=None,
    #                     temperature=tutr,
    #                 )
    #                 message = completion.choices[0].message["content"].strip()
    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()
    #                 if self.sub_widget0.currentIndex() == 0 or self.sub_widget0.currentIndex() == 6:
    #                     message = message.lstrip('\n')
    #                     message = message.replace('\n', '\n\n\t')
    #                     message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                     message = '\n\t' + message
    #                     QApplication.processEvents()
    #                     QApplication.restoreOverrideCursor()
    #                 if self.sub_widget0.currentIndex() == 1 or self.sub_widget0.currentIndex() == 2 or \
    #                         self.sub_widget0.currentIndex() == 3 or self.sub_widget0.currentIndex() == 4 or \
    #                         self.sub_widget0.currentIndex() == 5:
    #                     pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                     result = pattern.findall(message)
    #                     ResultEnd = ''.join(result)
    #                     ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                     uid = os.getuid()
    #                     env = os.environ.copy()
    #                     env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                     p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                     p.communicate(input=ResultEnd.encode('utf-8'))
    #                     message = ResultEnd
    #                     message = message.lstrip('\n')
    #                     message = message.replace('\n', '\n\n\t')
    #                     message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                     message = '\n\t' + message

    #                 EndMess = '- A: ' + message + '\n\n---\n\n'
    #                 with open(BasePath + 'output.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write(EndMess)
    #                 ProcessText = codecs.open(BasePath + 'output.txt', 'r',
    #                                           encoding='utf-8').read()
    #                 midhtml = self.md2html(ProcessText)
    #                 self.sub_real1.setHtml(midhtml)
    #                 self.sub_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()

    #                 self.sub_text1.clear()
    #             except TimeoutException:
    #                 with open(BasePath + 'output.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Timed out, please try again!' + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub_real1.setHtml(endhtml)
    #                 self.sub_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub_text1.setPlainText(self.sub_LastQ)
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 with open(BasePath + 'output.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Error, please try again!' + str(e) + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub_real1.setHtml(endhtml)
    #                 self.sub_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub_text1.setPlainText(self.sub_LastQ)
    #             signal.alarm(0)  # reset timer
    #             self.sub_text1.setReadOnly(False)
    #         if AccountGPT == '':
    #             self.sub_real1.setText('You should set your accounts in Settings.')
    #     if Which == '1':
    #         if self.sub_text1.toPlainText() == '':
    #             a = ''
    #             if self.main2.currentIndex() == 0:
    #                 a = self.text.textCursor().selectedText()
    #             if self.main2.currentIndex() == 1:
    #                 a = self.text_s2.textCursor().selectedText()
    #             if self.main2.currentIndex() == 2:
    #                 a = self.text_s3.textCursor().selectedText()
    #             if self.main2.currentIndex() == 3:
    #                 a = self.text_s4.textCursor().selectedText()
    #             if a == '':
    #                 a = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    #             self.sub_text1.setPlainText(a)
    #         QuesText = self.sub_text1.toPlainText()
    #         QuesText = QuesText.lstrip('\n')
    #         QuesText = QuesText.replace('\n', '\n\n\t')
    #         QuesText = QuesText.replace('\n\n\t\n\n\t', '\n\n\t')
    #         self.sub_LastQ = str(self.sub_text1.toPlainText())
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '' and self.sub_text1.toPlainText() != '':
    #             self.sub_text1.setReadOnly(True)
    #             md = '- Q: ' + QuesText + '\n\n'
    #             with open(BasePath + 'output.txt', 'a', encoding='utf-8') as f1:
    #                 f1.write(md)
    #             PromText = codecs.open(BasePath + 'output.txt', 'r',
    #                                    encoding='utf-8').read()
    #             newhtml = self.md2html(PromText)
    #             self.sub_real1.setHtml(newhtml)
    #             self.sub_real1.ensureCursorVisible()  # 游标可用
    #             cursor = self.sub_real1.textCursor()  # 设置游标
    #             pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #             cursor.setPosition(pos)  # 游标位置设置为尾部
    #             self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             # Set up your API key
    #             ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    #             api2 = codecs.open(BasePath + 'api2.txt', 'r',
    #                                encoding='utf-8').read()
    #             bear = codecs.open(BasePath + 'bear.txt', 'r',
    #                                encoding='utf-8').read()
    #             thirdp = codecs.open(BasePath + 'third.txt', 'r',
    #                                  encoding='utf-8').read()
    #             if bear != '' and api2 != '' and thirdp == '1':
    #                 ENDPOINT = bear + '/v1/chat/completions'
    #                 AccountGPT = api2
    #             HEADERS = {"Authorization": f"Bearer {AccountGPT}"}
    #             totaltoken = codecs.open(BasePath + 'total.txt', 'r',
    #                                      encoding='utf-8').read()
    #             maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                    encoding='utf-8').read()
    #             prompttoken = int(totaltoken) - int(maxtoken)
    #             try:
    #                 async def chat_gpt(message, conversation_history=None, tokens_limit=prompttoken):
    #                     if conversation_history is None:
    #                         conversation_history = []

    #                     conversation_history.append({"role": "user", "content": message})

    #                     input_text = "".join([f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])

    #                     # Truncate or shorten the input text if it exceeds the token limit
    #                     encoded_input_text = input_text.encode("utf-8")
    #                     while len(encoded_input_text) > tokens_limit:
    #                         conversation_history.pop(0)
    #                         input_text = "".join(
    #                             [f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])
    #                         encoded_input_text = input_text.encode("utf-8")

    #                     tutr = 0.5
    #                     temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                        encoding='utf-8').read()
    #                     if temp != '':
    #                         tutr = float(temp)

    #                     maxt = 1024
    #                     if maxtoken != '':
    #                         maxt = int(maxtoken)

    #                     # Set up the API call data
    #                     data = {
    #                         "model": modelnow,
    #                         "messages": [{"role": "user", "content": input_text}],
    #                         "max_tokens": maxt,
    #                         "temperature": tutr,
    #                         "n": 1,
    #                         "stop": None,
    #                     }

    #                     # Make the API call asynchronously
    #                     async with httpx.AsyncClient() as client:
    #                         response = await client.post(ENDPOINT, json=data, headers=HEADERS, timeout=60.0)

    #                     # Process the API response
    #                     if response.status_code == 200:
    #                         response_data = response.json()
    #                         chat_output = response_data["choices"][0]["message"]["content"].strip()
    #                         return chat_output
    #                     else:
    #                         raise Exception(
    #                             f"API call failed with status code {response.status_code}: {response.text}")

    #                 async def main():
    #                     conversation_history = []
    #                     prompt = str(self.sub_text1.toPlainText())
    #                     if self.sub_widget0.currentIndex() == 0:
    #                         ori_history = [{"role": "user", "content": "Hey."},
    #                                        {"role": "assistant", "content": "Hello! I'm happy to help you."}]
    #                         conversation_history = ori_history
    #                         showhistory = codecs.open(BasePath + 'history.txt',
    #                                                   'r',
    #                                                   encoding='utf-8').read()
    #                         if showhistory == '1':
    #                             try:
    #                                 history = codecs.open(
    #                                     BasePath + 'output.txt', 'r',
    #                                     encoding='utf-8').read().replace('"', '').replace(
    #                                     '- Q: ', '''{"role": "user", "content": "'''). \
    #                                     replace('- A: ', '''"}✡{"role": "assistant", "content": "''') \
    #                                     .replace('---', '''"}✡''').replace('\n', '').replace('\t', '').rstrip()
    #                                 historylist = history.split('✡')
    #                                 while '' in historylist:
    #                                     historylist.remove('')
    #                                 for hili in historylist:
    #                                     my_dict = json.loads(hili)
    #                                     conversation_history.append(my_dict)
    #                             except Exception as e:
    #                                 pass
    #                     if self.sub_widget0.currentIndex() == 1:
    #                         prompt = f"""You are a translation engine that can only translate text and cannot interpret it. Translate this text from {self.sub_widget1.currentText()} to {self.sub_widget2.currentText()}. Don’t reply any other explanations. Before the translated text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                     if self.sub_widget0.currentIndex() == 2:
    #                         prompt = f"""Revise the text in {self.sub_widget4.currentText()} to remove grammar mistakes and make it more clear, concise, and coherent. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                     if self.sub_widget0.currentIndex() == 3:
    #                         prompt = f"""You are a text summarizer, you can only summarize the text, don't interpret it. Summarize this text in {self.sub_widget4.currentText()} to make it shorter, logical and clear. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                     if self.sub_widget0.currentIndex() == 4:
    #                         prompt = f"""You are an expert in semantics and grammar, teaching me how to learn. Please explain in {self.sub_widget4.currentText()} the meaning of every word in the text above and the meaning and the grammar structure of the text. If a word is part of an idiom, please explain the idiom and provide a few examples in {self.sub_widget4.currentText()} with similar meanings, along with their explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub_text1.toPlainText())}. """
    #                     if self.sub_widget0.currentIndex() == 5:
    #                         prompt = f"""You are a code explanation engine, you can only explain the code, do not interpret or translate it. Also, please report any bugs you find in the code to the author of the code. Must repeat in {self.sub_widget4.currentText()}. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Code: {str(self.sub_text1.toPlainText())}. """

    #                     selectedtext = ''
    #                     if self.main2.currentIndex() == 0:
    #                         selectedtext = self.text.textCursor().selectedText()
    #                     if self.main2.currentIndex() == 1:
    #                         selectedtext = self.text_s2.textCursor().selectedText()
    #                     if self.main2.currentIndex() == 2:
    #                         selectedtext = self.text_s3.textCursor().selectedText()
    #                     if self.main2.currentIndex() == 3:
    #                         selectedtext = self.text_s4.textCursor().selectedText()
    #                     if selectedtext != '':
    #                         prompt = 'Please answer the prompt according to the context. <context starts> ' + selectedtext + '<context ends>. The prompt: ' + prompt

    #                     response = await chat_gpt(prompt, conversation_history)
    #                     message = response.lstrip('assistant:').strip()
    #                     if self.sub_widget0.currentIndex() == 0 or self.sub_widget0.currentIndex() == 6:
    #                         message = message.lstrip('\n')
    #                         message = message.replace('\n', '\n\n\t')
    #                         message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                         message = '\n\t' + message
    #                         QApplication.processEvents()
    #                         QApplication.restoreOverrideCursor()
    #                     if self.sub_widget0.currentIndex() == 1 or self.sub_widget0.currentIndex() == 2 or \
    #                             self.sub_widget0.currentIndex() == 3 or self.sub_widget0.currentIndex() == 4 or \
    #                             self.sub_widget0.currentIndex() == 5:
    #                         pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                         result = pattern.findall(message)
    #                         ResultEnd = ''.join(result)
    #                         ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                         uid = os.getuid()
    #                         env = os.environ.copy()
    #                         env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                         p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                         p.communicate(input=ResultEnd.encode('utf-8'))
    #                         message = ResultEnd
    #                         message = message.lstrip('\n')
    #                         message = message.replace('\n', '\n\n\t')
    #                         message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                         message = '\n\t' + message

    #                     EndMess = '- A: ' + message + '\n\n---\n\n'
    #                     with open(BasePath + 'output.txt', 'a',
    #                               encoding='utf-8') as f1:
    #                         f1.write(EndMess)
    #                     ProcessText = codecs.open(BasePath + 'output.txt', 'r',
    #                                               encoding='utf-8').read()
    #                     midhtml = self.md2html(ProcessText)
    #                     self.sub_real1.setHtml(midhtml)
    #                     self.sub_real1.ensureCursorVisible()  # 游标可用
    #                     cursor = self.sub_real1.textCursor()  # 设置游标
    #                     pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                     cursor.setPosition(pos)  # 游标位置设置为尾部
    #                     self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                     QApplication.processEvents()
    #                     QApplication.restoreOverrideCursor()
    #                     self.sub_text1.clear()

    #                 asyncio.run(main())
    #             except TimeoutException:
    #                 with open(BasePath + 'output.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Timed out, please try again!' + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub_real1.setHtml(endhtml)
    #                 self.sub_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub_text1.setPlainText(self.sub_LastQ)
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 with open(BasePath + 'output.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Error, please try again!' + str(e) + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub_real1.setHtml(endhtml)
    #                 self.sub_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub_text1.setPlainText(self.sub_LastQ)
    #             signal.alarm(0)  # reset timer
    #             self.sub_text1.setReadOnly(False)
    #         if AccountGPT == '':
    #             self.sub_real1.setText('You should set your accounts in Settings.')
    #     self.sub_btn_sub1.setDisabled(False)

    # def bot1clear(self):
    #     self.sub_text1.clear()
    #     self.sub_text1.setReadOnly(False)
    #     self.sub_real1.clear()
    #     with open(BasePath + 'output.txt', 'w', encoding='utf-8') as f1:
    #         f1.write('')

    # def bot1mode(self, i):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     self.sub_fulldir1 = os.path.join(home_dir, tarname1)
    #     tarname3 = "lang.txt"
    #     fulldir3 = os.path.join(self.sub_fulldir1, tarname3)
    #     langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
    #     fulllanglist = []
    #     langs_list = ['English', '中文', '日本語']
    #     if langs != '':
    #         langs_list = langs.split('\n')
    #         while '' in langs_list:
    #             langs_list.remove('')
    #         for x in range(len(langs_list)):
    #             fulllanglist.append(langs_list[x])
    #     if langs == '':
    #         for x in range(len(langs_list)):
    #             fulllanglist.append(langs_list[x])
    #     if i == 0:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(False)
    #         self.sub_widget4.setVisible(False)
    #         self.sub_widget5.setVisible(False)
    #     if i == 1:
    #         self.sub_widget1.setVisible(True)
    #         self.sub_widget2.setVisible(True)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(False)
    #         self.sub_widget5.setVisible(False)
    #         # renew 1
    #         self.sub_widget1.clear()
    #         self.sub_widget1.addItems(langs_list)
    #     if i == 2:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(True)
    #         self.sub_widget5.setVisible(False)
    #         # renew 4
    #         self.sub_widget4.clear()
    #         self.sub_widget4.addItems(fulllanglist)
    #     if i == 3:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(True)
    #         self.sub_widget5.setVisible(False)
    #         # renew 4
    #         self.sub_widget4.clear()
    #         self.sub_widget4.addItems(fulllanglist)
    #     if i == 4:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(True)
    #         self.sub_widget5.setVisible(False)
    #         # renew 4
    #         self.sub_widget4.clear()
    #         self.sub_widget4.addItems(fulllanglist)
    #     if i == 5:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(True)
    #         self.sub_widget5.setVisible(False)
    #         # renew 4
    #         self.sub_widget4.clear()
    #         self.sub_widget4.addItems(fulllanglist)
    #     if i == 6:
    #         self.sub_widget1.setVisible(False)
    #         self.sub_widget2.setVisible(False)
    #         self.sub_lbl1.setVisible(True)
    #         self.sub_widget4.setVisible(False)
    #         self.sub_widget5.setVisible(True)
    #         self.sub_widget5.clear()
    #         home_dir = str(Path.home())
    #         tarname1 = "BroccoliAppPath"
    #         fulldir1 = os.path.join(home_dir, tarname1)
    #         if not os.path.exists(fulldir1):
    #             os.mkdir(fulldir1)
    #         tarname2 = "CustomPrompt.txt"
    #         fulldir2 = os.path.join(fulldir1, tarname2)
    #         if not os.path.exists(fulldir2):
    #             with open(fulldir2, 'a', encoding='utf-8') as f0:
    #                 f0.write('')
    #         customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
    #         promptlist = customprompt.split('---')
    #         while '' in promptlist:
    #             promptlist.remove('')
    #         itemlist = []
    #         for i in range(len(promptlist)):
    #             itemlist.append(promptlist[i].split('|><|')[0].replace('<|', '').replace('\n', ''))
    #         if itemlist != []:
    #             self.sub_widget5.addItems(itemlist)
    #         if itemlist == []:
    #             self.sub_widget5.addItems(['No customized prompts, please add one in Settings'])

    # def bot1trans(self):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     fulldir1 = os.path.join(home_dir, tarname1)
    #     tarname3 = "lang.txt"
    #     fulldir3 = os.path.join(fulldir1, tarname3)
    #     currentlang = self.sub_widget1.currentText()
    #     self.sub_widget2.clear()
    #     langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
    #     if langs != '':
    #         langs_list = langs.split('\n')
    #         while '' in langs_list:
    #             langs_list.remove('')
    #         while currentlang in langs_list:
    #             langs_list.remove(currentlang)
    #         self.sub_widget2.addItems(langs_list)
    #         self.sub_widget2.setCurrentIndex(0)
    #     if langs == '':
    #         langs_list = ['English', '中文', '日本語']
    #         while currentlang in langs_list:
    #             langs_list.remove(currentlang)
    #         self.sub_widget2.addItems(langs_list)
    #         self.sub_widget2.setCurrentIndex(0)

    # def bot1custom(self, i):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     fulldir1 = os.path.join(home_dir, tarname1)
    #     if not os.path.exists(fulldir1):
    #         os.mkdir(fulldir1)
    #     tarname2 = "CustomPrompt.txt"
    #     fulldir2 = os.path.join(fulldir1, tarname2)
    #     if not os.path.exists(fulldir2):
    #         with open(fulldir2, 'a', encoding='utf-8') as f0:
    #             f0.write('')
    #     customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
    #     promptlist = customprompt.split('---')
    #     while '' in promptlist:
    #         promptlist.remove('')
    #     itemlist = []
    #     for n in range(len(promptlist)):
    #         itemlist.append(promptlist[n].split('|><|')[1].replace('|>', ''))
    #     if itemlist != []:
    #         try:
    #             self.sub_text1.clear()
    #             self.sub_text1.setPlainText(itemlist[i])
    #         except Exception as e:
    #             self.sub_text1.clear()
    #             self.sub_text1.setPlainText(e)

    def bot2show(self):
        pass
        # self.bot2.setVisible(True)

    # def bot2close(self):
    #     self.bot2.setVisible(False)

    # def bot2send(self):
    #     self.sub2_btn_sub21.setDisabled(True)
    #     modelnow = codecs.open(BasePath + 'modelnow.txt', 'r', encoding='utf-8').read()
    #     Which = codecs.open(BasePath + 'which.txt', 'r', encoding='utf-8').read()
    #     if Which == '0':
    #         if self.sub2_text1.toPlainText() == '':
    #             a = ''
    #             if self.mainii2.currentIndex() == 0:
    #                 a = self.textii2.textCursor().selectedText()
    #             if self.mainii2.currentIndex() == 1:
    #                 a = self.textii3.textCursor().selectedText()
    #             if a == '':
    #                 a = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    #             self.sub2_text1.setPlainText(a)
    #         QuesText = self.sub2_text1.toPlainText()
    #         QuesText = QuesText.lstrip('\n')
    #         QuesText = QuesText.replace('\n', '\n\n\t')
    #         QuesText = QuesText.replace('\n\n\t\n\n\t', '\n\n\t')
    #         self.sub2_LastQ = str(self.sub2_text1.toPlainText())
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '' and self.sub2_text1.toPlainText() != '':
    #             QApplication.processEvents()
    #             QApplication.restoreOverrideCursor()
    #             self.sub2_text1.setReadOnly(True)
    #             md = '- Q: ' + QuesText + '\n\n'
    #             with open(BasePath + 'output2.txt', 'a', encoding='utf-8') as f1:
    #                 f1.write(md)
    #             PromText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                    encoding='utf-8').read()
    #             newhtml = self.md2html(PromText)
    #             self.sub2_real1.setHtml(newhtml)
    #             self.sub2_real1.ensureCursorVisible()  # 游标可用
    #             cursor = self.sub2_real1.textCursor()  # 设置游标
    #             pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #             cursor.setPosition(pos)  # 游标位置设置为尾部
    #             self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #             QApplication.processEvents()
    #             QApplication.restoreOverrideCursor()
    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             try:
    #                 openai.api_key = AccountGPT
    #                 history = ''
    #                 showhistory = codecs.open(BasePath + 'history.txt', 'r',
    #                                           encoding='utf-8').read()
    #                 if showhistory == '1':
    #                     history = codecs.open(BasePath + 'output2.txt', 'r',
    #                                           encoding='utf-8').read().replace('- A: ', '').replace('- Q: ', '')
    #                 prompt = str(self.sub2_text1.toPlainText())
    #                 reststr = history + '---' + prompt
    #                 tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-2.7B')
    #                 A = tokenizer.encode(reststr, add_special_tokens=True)
    #                 totaltoken = codecs.open(BasePath + 'total.txt', 'r',
    #                                          encoding='utf-8').read()
    #                 maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                        encoding='utf-8').read()
    #                 prompttoken = int(totaltoken) - int(maxtoken)
    #                 while len(A) >= prompttoken:
    #                     AllList = reststr.split('---')
    #                     while '' in AllList:
    #                         AllList.remove('')
    #                     while '\n\n' in AllList:
    #                         AllList.remove('\n\n')
    #                     del AllList[0]
    #                     reststr = '---'.join(AllList)
    #                     A = tokenizer.encode(reststr, add_special_tokens=True)
    #                     continue
    #                 if self.sub2_widget0.currentIndex() == 0:
    #                     prompt = reststr
    #                 if self.sub2_widget0.currentIndex() == 1:
    #                     prompt = f"""You are a translation engine that can only translate text and cannot interpret it. Translate this text from {self.sub2_widget1.currentText()} to {self.sub2_widget2.currentText()}. Don’t reply any other explanations. Before the translated text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                 if self.sub2_widget0.currentIndex() == 2:
    #                     prompt = f"""Revise the text in {self.sub2_widget4.currentText()} to remove grammar mistakes and make it more clear, concise, and coherent. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                 if self.sub2_widget0.currentIndex() == 3:
    #                     prompt = f"""You are a text summarizer, you can only summarize the text, don't interpret it. Summarize this text in {self.sub2_widget4.currentText()} to make it shorter, logical and clear. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                 if self.sub2_widget0.currentIndex() == 4:
    #                     prompt = f"""You are an expert in semantics and grammar, teaching me how to learn. Please explain in {self.sub2_widget4.currentText()} the meaning of every word in the text above and the meaning and the grammar structure of the text. If a word is part of an idiom, please explain the idiom and provide a few examples in {self.sub2_widget4.currentText()} with similar meanings, along with their explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                 if self.sub2_widget0.currentIndex() == 5:
    #                     prompt = f"""You are a code explanation engine, you can only explain the code, do not interpret or translate it. Also, please report any bugs you find in the code to the author of the code. Must repeat in {self.sub2_widget4.currentText()}. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Code: {str(self.sub2_text1.toPlainText())}. """

    #                 selectedtext = ''
    #                 if self.mainii2.currentIndex() == 0:
    #                     selectedtext = self.textii2.textCursor().selectedText()
    #                 if self.mainii2.currentIndex() == 1:
    #                     selectedtext = self.textii3.textCursor().selectedText()
    #                 if selectedtext != '':
    #                     prompt = 'Please answer the prompt according to the context. <context starts> ' + selectedtext + '<context ends>. The prompt: ' + prompt

    #                 tutr = 0.5
    #                 temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                    encoding='utf-8').read()
    #                 if temp != '':
    #                     tutr = float(temp)

    #                 maxt = 1024
    #                 if maxtoken != '':
    #                     maxt = int(maxtoken)

    #                 completion = openai.ChatCompletion.create(
    #                     model=modelnow,
    #                     messages=[{"role": "user", "content": prompt}],
    #                     max_tokens=maxt,
    #                     n=1,
    #                     stop=None,
    #                     temperature=tutr,
    #                 )
    #                 message = completion.choices[0].message["content"].strip()
    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()
    #                 if self.sub2_widget0.currentIndex() == 0 or self.sub2_widget0.currentIndex() == 6:
    #                     message = message.lstrip('\n')
    #                     message = message.replace('\n', '\n\n\t')
    #                     message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                     message = '\n\t' + message
    #                     QApplication.processEvents()
    #                     QApplication.restoreOverrideCursor()
    #                 if self.sub2_widget0.currentIndex() == 1 or self.sub2_widget0.currentIndex() == 2 or \
    #                         self.sub2_widget0.currentIndex() == 3 or self.sub2_widget0.currentIndex() == 4 or \
    #                         self.sub2_widget0.currentIndex() == 5:
    #                     pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                     result = pattern.findall(message)
    #                     ResultEnd = ''.join(result)
    #                     ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                     uid = os.getuid()
    #                     env = os.environ.copy()
    #                     env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                     p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                     p.communicate(input=ResultEnd.encode('utf-8'))
    #                     message = ResultEnd
    #                     message = message.lstrip('\n')
    #                     message = message.replace('\n', '\n\n\t')
    #                     message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                     message = '\n\t' + message

    #                 EndMess = '- A: ' + message + '\n\n---\n\n'
    #                 with open(BasePath + 'output2.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write(EndMess)
    #                 ProcessText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                           encoding='utf-8').read()
    #                 midhtml = self.md2html(ProcessText)
    #                 self.sub2_real1.setHtml(midhtml)
    #                 self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub2_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 QApplication.processEvents()
    #                 QApplication.restoreOverrideCursor()

    #                 self.sub2_text1.clear()
    #             except TimeoutException:
    #                 with open(BasePath + 'output2.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Timed out, please try again!' + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub2_real1.setHtml(endhtml)
    #                 self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub2_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub2_text1.setPlainText(self.sub2_LastQ)
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 with open(BasePath + 'output2.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Error, please try again!' + str(e) + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub2_real1.setHtml(endhtml)
    #                 self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub2_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub2_text1.setPlainText(self.sub2_LastQ)
    #             signal.alarm(0)  # reset timer
    #             self.sub2_text1.setReadOnly(False)
    #         if AccountGPT == '':
    #             self.sub2_real1.setText('You should set your accounts in Settings.')
    #     if Which == '1':
    #         if self.sub2_text1.toPlainText() == '':
    #             a = ''
    #             if self.mainii2.currentIndex() == 0:
    #                 a = self.textii2.textCursor().selectedText()
    #             if self.mainii2.currentIndex() == 1:
    #                 a = self.textii3.textCursor().selectedText()
    #             if a == '':
    #                 a = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
    #             self.sub2_text1.setPlainText(a)
    #         QuesText = self.sub2_text1.toPlainText()
    #         QuesText = QuesText.lstrip('\n')
    #         QuesText = QuesText.replace('\n', '\n\n\t')
    #         QuesText = QuesText.replace('\n\n\t\n\n\t', '\n\n\t')
    #         self.sub2_LastQ = str(self.sub2_text1.toPlainText())
    #         AccountGPT = codecs.open(BasePath + 'api.txt', 'r',
    #                                  encoding='utf-8').read()
    #         if AccountGPT != '' and self.sub2_text1.toPlainText() != '':
    #             self.sub2_text1.setReadOnly(True)
    #             md = '- Q: ' + QuesText + '\n\n'
    #             with open(BasePath + 'output2.txt', 'a', encoding='utf-8') as f1:
    #                 f1.write(md)
    #             PromText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                    encoding='utf-8').read()
    #             newhtml = self.md2html(PromText)
    #             self.sub2_real1.setHtml(newhtml)
    #             self.sub2_real1.ensureCursorVisible()  # 游标可用
    #             cursor = self.sub2_real1.textCursor()  # 设置游标
    #             pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #             cursor.setPosition(pos)  # 游标位置设置为尾部
    #             self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #             timeout = 60
    #             timeset = codecs.open(BasePath + 'timeout.txt', 'r',
    #                                   encoding='utf-8').read()
    #             if timeset != '':
    #                 timeout = int(timeset)
    #             signal.signal(signal.SIGALRM, self.timeout_handler)
    #             signal.alarm(timeout)  # set timer to 15 seconds
    #             # Set up your API key
    #             ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    #             api2 = codecs.open(BasePath + 'api2.txt', 'r',
    #                                encoding='utf-8').read()
    #             bear = codecs.open(BasePath + 'bear.txt', 'r',
    #                                encoding='utf-8').read()
    #             thirdp = codecs.open(BasePath + 'third.txt', 'r',
    #                                  encoding='utf-8').read()
    #             if bear != '' and api2 != '' and thirdp == '1':
    #                 ENDPOINT = bear + '/v1/chat/completions'
    #                 AccountGPT = api2
    #             HEADERS = {"Authorization": f"Bearer {AccountGPT}"}
    #             totaltoken = codecs.open(BasePath + 'total.txt', 'r',
    #                                      encoding='utf-8').read()
    #             maxtoken = codecs.open(BasePath + 'max.txt', 'r',
    #                                    encoding='utf-8').read()
    #             prompttoken = int(totaltoken) - int(maxtoken)
    #             try:
    #                 async def chat_gpt(message, conversation_history=None, tokens_limit=prompttoken):
    #                     if conversation_history is None:
    #                         conversation_history = []

    #                     conversation_history.append({"role": "user", "content": message})

    #                     input_text = "".join([f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])

    #                     # Truncate or shorten the input text if it exceeds the token limit
    #                     encoded_input_text = input_text.encode("utf-8")
    #                     while len(encoded_input_text) > tokens_limit:
    #                         conversation_history.pop(0)
    #                         input_text = "".join(
    #                             [f"{msg['role']}:{msg['content']}\n" for msg in conversation_history])
    #                         encoded_input_text = input_text.encode("utf-8")

    #                     tutr = 0.5
    #                     temp = codecs.open(BasePath + 'temp.txt', 'r',
    #                                        encoding='utf-8').read()
    #                     if temp != '':
    #                         tutr = float(temp)

    #                     maxt = 1024
    #                     if maxtoken != '':
    #                         maxt = int(maxtoken)

    #                     # Set up the API call data
    #                     data = {
    #                         "model": modelnow,
    #                         "messages": [{"role": "user", "content": input_text}],
    #                         "max_tokens": maxt,
    #                         "temperature": tutr,
    #                         "n": 1,
    #                         "stop": None,
    #                     }

    #                     # Make the API call asynchronously
    #                     async with httpx.AsyncClient() as client:
    #                         response = await client.post(ENDPOINT, json=data, headers=HEADERS, timeout=60.0)

    #                     # Process the API response
    #                     if response.status_code == 200:
    #                         response_data = response.json()
    #                         chat_output = response_data["choices"][0]["message"]["content"].strip()
    #                         return chat_output
    #                     else:
    #                         raise Exception(
    #                             f"API call failed with status code {response.status_code}: {response.text}")

    #                 async def main():
    #                     conversation_history = []
    #                     prompt = str(self.sub2_text1.toPlainText())
    #                     if self.sub2_widget0.currentIndex() == 0:
    #                         ori_history = [{"role": "user", "content": "Hey."},
    #                                        {"role": "assistant", "content": "Hello! I'm happy to help you."}]
    #                         conversation_history = ori_history
    #                         showhistory = codecs.open(BasePath + 'history.txt',
    #                                                   'r',
    #                                                   encoding='utf-8').read()
    #                         if showhistory == '1':
    #                             try:
    #                                 history = codecs.open(
    #                                     BasePath + 'output2.txt', 'r',
    #                                     encoding='utf-8').read().replace('"', '').replace(
    #                                     '- Q: ', '''{"role": "user", "content": "'''). \
    #                                     replace('- A: ', '''"}✡{"role": "assistant", "content": "''') \
    #                                     .replace('---', '''"}✡''').replace('\n', '').replace('\t', '').rstrip()
    #                                 historylist = history.split('✡')
    #                                 while '' in historylist:
    #                                     historylist.remove('')
    #                                 for hili in historylist:
    #                                     my_dict = json.loads(hili)
    #                                     conversation_history.append(my_dict)
    #                             except Exception as e:
    #                                 pass
    #                     if self.sub2_widget0.currentIndex() == 1:
    #                         prompt = f"""You are a translation engine that can only translate text and cannot interpret it. Translate this text from {self.sub2_widget1.currentText()} to {self.sub2_widget2.currentText()}. Don’t reply any other explanations. Before the translated text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                     if self.sub2_widget0.currentIndex() == 2:
    #                         prompt = f"""Revise the text in {self.sub2_widget4.currentText()} to remove grammar mistakes and make it more clear, concise, and coherent. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                     if self.sub2_widget0.currentIndex() == 3:
    #                         prompt = f"""You are a text summarizer, you can only summarize the text, don't interpret it. Summarize this text in {self.sub2_widget4.currentText()} to make it shorter, logical and clear. Don’t reply any other explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                     if self.sub2_widget0.currentIndex() == 4:
    #                         prompt = f"""You are an expert in semantics and grammar, teaching me how to learn. Please explain in {self.sub2_widget4.currentText()} the meaning of every word in the text above and the meaning and the grammar structure of the text. If a word is part of an idiom, please explain the idiom and provide a few examples in {self.sub2_widget4.currentText()} with similar meanings, along with their explanations. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Text: {str(self.sub2_text1.toPlainText())}. """
    #                     if self.sub2_widget0.currentIndex() == 5:
    #                         prompt = f"""You are a code explanation engine, you can only explain the code, do not interpret or translate it. Also, please report any bugs you find in the code to the author of the code. Must repeat in {self.sub2_widget4.currentText()}. Before the text starts, write "「「start」」" and write "「「end」」" after it ends. Code: {str(self.sub2_text1.toPlainText())}. """

    #                     selectedtext = ''
    #                     if self.mainii2.currentIndex() == 0:
    #                         selectedtext = self.textii2.textCursor().selectedText()
    #                     if self.mainii2.currentIndex() == 1:
    #                         selectedtext = self.textii3.textCursor().selectedText()
    #                     if selectedtext != '':
    #                         prompt = 'Please answer the prompt according to the context. <context starts> ' + selectedtext + '<context ends>. The prompt: ' + prompt

    #                     response = await chat_gpt(prompt, conversation_history)
    #                     message = response.lstrip('assistant:').strip()
    #                     if self.sub2_widget0.currentIndex() == 0 or self.sub2_widget0.currentIndex() == 6:
    #                         message = message.lstrip('\n')
    #                         message = message.replace('\n', '\n\n\t')
    #                         message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                         message = '\n\t' + message
    #                         QApplication.processEvents()
    #                         QApplication.restoreOverrideCursor()
    #                     if self.sub2_widget0.currentIndex() == 1 or self.sub2_widget0.currentIndex() == 2 or \
    #                             self.sub2_widget0.currentIndex() == 3 or self.sub2_widget0.currentIndex() == 4 or \
    #                             self.sub2_widget0.currentIndex() == 5:
    #                         pattern = re.compile(r'「「start」」([\s\S]*?)「「end」」')
    #                         result = pattern.findall(message)
    #                         ResultEnd = ''.join(result)
    #                         ResultEnd = ResultEnd.encode('utf-8').decode('utf-8', 'ignore')
    #                         uid = os.getuid()
    #                         env = os.environ.copy()
    #                         env['__CF_USER_TEXT_ENCODING'] = f'{uid}:0x8000100:0x8000100'
    #                         p = subprocess.Popen(['pbcopy', 'w'], stdin=subprocess.PIPE, env=env)
    #                         p.communicate(input=ResultEnd.encode('utf-8'))
    #                         message = ResultEnd
    #                         message = message.lstrip('\n')
    #                         message = message.replace('\n', '\n\n\t')
    #                         message = message.replace('\n\n\t\n\n\t', '\n\n\t')
    #                         message = '\n\t' + message

    #                     EndMess = '- A: ' + message + '\n\n---\n\n'
    #                     with open(BasePath + 'output2.txt', 'a',
    #                               encoding='utf-8') as f1:
    #                         f1.write(EndMess)
    #                     ProcessText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                               encoding='utf-8').read()
    #                     midhtml = self.md2html(ProcessText)
    #                     self.sub2_real1.setHtml(midhtml)
    #                     self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                     cursor = self.sub2_real1.textCursor()  # 设置游标
    #                     pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                     cursor.setPosition(pos)  # 游标位置设置为尾部
    #                     self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                     QApplication.processEvents()
    #                     QApplication.restoreOverrideCursor()
    #                     self.sub2_text1.clear()

    #                 asyncio.run(main())
    #             except TimeoutException:
    #                 with open(BasePath + 'output2.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Timed out, please try again!' + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub2_real1.setHtml(endhtml)
    #                 self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub2_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub2_text1.setPlainText(self.sub2_LastQ)
    #             except Exception as e:
    #                 with open(BasePath + 'errorfile.txt', 'w', encoding='utf-8') as f0:
    #                     f0.write(str(e))
    #                 with open(BasePath + 'output2.txt', 'a',
    #                           encoding='utf-8') as f1:
    #                     f1.write('- A: Error, please try again!' + str(e) + '\n\n---\n\n')
    #                 AllText = codecs.open(BasePath + 'output2.txt', 'r',
    #                                       encoding='utf-8').read()
    #                 endhtml = self.md2html(AllText)
    #                 self.sub2_real1.setHtml(endhtml)
    #                 self.sub2_real1.ensureCursorVisible()  # 游标可用
    #                 cursor = self.sub2_real1.textCursor()  # 设置游标
    #                 pos = len(self.sub2_real1.toPlainText())  # 获取文本尾部的位置
    #                 cursor.setPosition(pos)  # 游标位置设置为尾部
    #                 self.sub2_real1.setTextCursor(cursor)  # 滚动到游标位置
    #                 self.sub2_text1.setPlainText(self.sub2_LastQ)
    #             signal.alarm(0)  # reset timer
    #             self.sub2_text1.setReadOnly(False)
    #         if AccountGPT == '':
    #             self.sub2_real1.setText('You should set your accounts in Settings.')
    #     self.sub2_btn_sub21.setDisabled(False)

    # def bot2clear(self):
    #     self.sub2_text1.clear()
    #     self.sub2_text1.setReadOnly(False)
    #     self.sub2_real1.clear()
    #     with open(BasePath + 'output2.txt', 'w', encoding='utf-8') as f1:
    #         f1.write('')

    # def bot2mode(self, i):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     self.sub2_fulldir1 = os.path.join(home_dir, tarname1)
    #     tarname3 = "lang.txt"
    #     fulldir3 = os.path.join(self.sub2_fulldir1, tarname3)
    #     langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
    #     fulllanglist = []
    #     langs_list = ['English', '中文', '日本語']
    #     if langs != '':
    #         langs_list = langs.split('\n')
    #         while '' in langs_list:
    #             langs_list.remove('')
    #         for x in range(len(langs_list)):
    #             fulllanglist.append(langs_list[x])
    #     if langs == '':
    #         for x in range(len(langs_list)):
    #             fulllanglist.append(langs_list[x])
    #     if i == 0:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(False)
    #         self.sub2_widget4.setVisible(False)
    #         self.sub2_widget5.setVisible(False)
    #     if i == 1:
    #         self.sub2_widget1.setVisible(True)
    #         self.sub2_widget2.setVisible(True)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(False)
    #         self.sub2_widget5.setVisible(False)
    #         # renew 1
    #         self.sub2_widget1.clear()
    #         self.sub2_widget1.addItems(langs_list)
    #     if i == 2:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(True)
    #         self.sub2_widget5.setVisible(False)
    #         # renew 4
    #         self.sub2_widget4.clear()
    #         self.sub2_widget4.addItems(fulllanglist)
    #     if i == 3:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(True)
    #         self.sub2_widget5.setVisible(False)
    #         # renew 4
    #         self.sub2_widget4.clear()
    #         self.sub2_widget4.addItems(fulllanglist)
    #     if i == 4:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(True)
    #         self.sub2_widget5.setVisible(False)
    #         # renew 4
    #         self.sub2_widget4.clear()
    #         self.sub2_widget4.addItems(fulllanglist)
    #     if i == 5:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(True)
    #         self.sub2_widget5.setVisible(False)
    #         # renew 4
    #         self.sub2_widget4.clear()
    #         self.sub2_widget4.addItems(fulllanglist)
    #     if i == 6:
    #         self.sub2_widget1.setVisible(False)
    #         self.sub2_widget2.setVisible(False)
    #         self.sub2_lbl1.setVisible(True)
    #         self.sub2_widget4.setVisible(False)
    #         self.sub2_widget5.setVisible(True)
    #         self.sub2_widget5.clear()
    #         home_dir = str(Path.home())
    #         tarname1 = "BroccoliAppPath"
    #         fulldir1 = os.path.join(home_dir, tarname1)
    #         if not os.path.exists(fulldir1):
    #             os.mkdir(fulldir1)
    #         tarname2 = "CustomPrompt.txt"
    #         fulldir2 = os.path.join(fulldir1, tarname2)
    #         if not os.path.exists(fulldir2):
    #             with open(fulldir2, 'a', encoding='utf-8') as f0:
    #                 f0.write('')
    #         customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
    #         promptlist = customprompt.split('---')
    #         while '' in promptlist:
    #             promptlist.remove('')
    #         itemlist = []
    #         for i in range(len(promptlist)):
    #             itemlist.append(promptlist[i].split('|><|')[0].replace('<|', '').replace('\n', ''))
    #         if itemlist != []:
    #             self.sub2_widget5.addItems(itemlist)
    #         if itemlist == []:
    #             self.sub2_widget5.addItems(['No customized prompts, please add one in Settings'])

    # def bot2trans(self):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     fulldir1 = os.path.join(home_dir, tarname1)
    #     tarname3 = "lang.txt"
    #     fulldir3 = os.path.join(fulldir1, tarname3)
    #     currentlang = self.sub2_widget1.currentText()
    #     self.sub2_widget2.clear()
    #     langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
    #     if langs != '':
    #         langs_list = langs.split('\n')
    #         while '' in langs_list:
    #             langs_list.remove('')
    #         while currentlang in langs_list:
    #             langs_list.remove(currentlang)
    #         self.sub2_widget2.addItems(langs_list)
    #         self.sub2_widget2.setCurrentIndex(0)
    #     if langs == '':
    #         langs_list = ['English', '中文', '日本語']
    #         while currentlang in langs_list:
    #             langs_list.remove(currentlang)
    #         self.sub2_widget2.addItems(langs_list)
    #         self.sub2_widget2.setCurrentIndex(0)

    # def bot2custom(self, i):
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     fulldir1 = os.path.join(home_dir, tarname1)
    #     if not os.path.exists(fulldir1):
    #         os.mkdir(fulldir1)
    #     tarname2 = "CustomPrompt.txt"
    #     fulldir2 = os.path.join(fulldir1, tarname2)
    #     if not os.path.exists(fulldir2):
    #         with open(fulldir2, 'a', encoding='utf-8') as f0:
    #             f0.write('')
    #     customprompt = codecs.open(fulldir2, 'r', encoding='utf-8').read()
    #     promptlist = customprompt.split('---')
    #     while '' in promptlist:
    #         promptlist.remove('')
    #     itemlist = []
    #     for n in range(len(promptlist)):
    #         itemlist.append(promptlist[n].split('|><|')[1].replace('|>', ''))
    #     if itemlist != []:
    #         try:
    #             self.sub2_text1.clear()
    #             self.sub2_text1.setPlainText(itemlist[i])
    #         except Exception as e:
    #             self.sub2_text1.clear()
    #             self.sub2_text1.setPlainText(e)

    def pin_a_tab(self):
        self._toggle_pin_tab()

    def pin_a_tab2(self):
        self._toggle_pin_tab()

    def _toggle_pin_tab(self):
        screen_geom = self._current_screen_geometry()
        screen_width = int(screen_geom.width())
        screen_left = int(screen_geom.x())
        screen_right = screen_left + screen_width
        de_height = int(screen_geom.height())
        target_y = min(max(self.pos().y(), screen_geom.y()), screen_geom.y() + screen_geom.height() - de_height)

        # Determine mode key for caching
        if action10.isChecked():
            mode_key = "compact"
            default_width = int(screen_width / 4)
        elif action7.isChecked():
            mode_key = "realtime"
            default_width = int(screen_width * 3 / 4)
        else:
            mode_key = "normal"
            default_width = int(screen_width / 2)

        # Try to read cached width for current mode and screen size
        try:
            cache_data = codecs.open(BasePath + 'win_width.txt', 'r', encoding='utf-8').read().strip()
            if cache_data:
                parts = cache_data.split('|')
                if len(parts) == 3:
                    cached_mode, cached_screen, cached_width = parts
                    # Use cached width if mode and screen size match
                    if cached_mode == mode_key and int(cached_screen) == screen_width:
                        target_width_open = int(cached_width)
                    else:
                        target_width_open = default_width
                else:
                    target_width_open = default_width
            else:
                target_width_open = default_width
        except:
            target_width_open = default_width

        if self.i % 2 == 1:
            # Opening: expand to target width based on current mode
            target_width = target_width_open
            target_x = screen_right - target_width - 3

            # Disable updates during initial setup
            self.setUpdatesEnabled(False)

            btna4.setChecked(True)
            self.btn_00.setStyleSheet('''
                                border: 1px outset grey;
                                background-color: #0085FF;
                                border-radius: 4px;
                                padding: 1px;
                                color: #FFFFFF''')
            self.tab_bar.setVisible(True)

            # Set the correct WIDTH at current position (off-screen right)
            # This prevents Qt from resizing during animation
            current_x = self.pos().x()
            start_geometry = QRect(current_x, target_y, int(target_width), de_height)
            self.setGeometry(start_geometry)

            # Re-enable updates - now window has correct size
            self.setUpdatesEnabled(True)

            # Save cache with mode and screen info
            cache_str = f"{mode_key}|{screen_width}|{target_width}"
            with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
                f0.write(cache_str)

            # Delay animation start to ensure layout is fully calculated
            # This prevents flicker by giving Qt time to complete internal layout
            def start_slide_animation():
                animation = QPropertyAnimation(self, b"geometry", self)
                animation.setDuration(250)
                end_geometry = QRect(target_x, target_y, int(target_width), de_height)
                animation.setEndValue(end_geometry)
                animation.start()

            QTimer.singleShot(100, start_slide_animation)
        else:
            # Closing: collapse to minimal width
            target_width = self.new_width
            target_x = screen_right - target_width - 3

            btna4.setChecked(False)
            self.btn_00.setStyleSheet('''
                                border: 1px outset grey;
                                background-color: #FFFFFF;
                                border-radius: 4px;
                                padding: 1px;
                                color: #000000''')
            self.tab_bar.setVisible(False)

            # Animate both position AND size change together
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setDuration(250)
            end_geometry = QRect(target_x, target_y, target_width, de_height)
            animation.setEndValue(end_geometry)
            animation.start()

        # Toggle state
        self.i += 1

    def cleanlinebreak(self, a):  # 设置清除断行的基本代码块
        for i in range(10):
            a = a.replace('\r', ' ')
            a = a.replace('\n', ' ')
        return a

    def cleancitmak(self, a):
        a = re.sub(r"\{(\s)*(\d+\s)*(\d)*?\}|\[(\s)*(\d+\s)*(\d)*?\]|〔(\s)*(\d+\s)*(\d)*?〕|﹝(\s)*(\d+\s)*(\d)*?﹞", "",
                   a)
        a = re.sub(
            r"\[(\s)*(\d+\s)*(\d)*?〕|\[(\s)*(\d+\s)*(\d)*?﹞|〔(\s)*(\d+\s)*(\d)*?\]|〔(\s)*(\d+\s)*(\d)*?﹞|﹝(\s)*(\d+\s)*(\d)*?\]|﹝(\s)*(\d+\s)*(\d)*?〕",
            "", a)
        a = re.sub(
            r"（(\s)*(\d+\s)*(\d)*?）|\[(\s)*(\d+\s)*(\d)*?）|（(\s)*(\d+\s)*(\d)*?\]|（(\s)*(\d+\s)*(\d)*?】|【(\s)*(\d+\s)*(\d)*?）",
            "", a)
        a = re.sub(
            r"\((\s)*(\d+\s)*(\d)*?〕|\((\s)*(\d+\s)*(\d)*?﹞|〔(\s)*(\d+\s)*(\d)*?\)|﹝(\s)*(\d+\s)*(\d)*?\)|\((\s)*(\d+\s)*(\d)*?\)|\[(\s)*(\d+\s)*(\d)*?\)|\((\s)*(\d+\s)*(\d)*?\]",
            "", a)
        a = re.sub(r"\<(\s)*(\d+\s)*(\d)*?\>|\《(\s)*(\d+\s)*(\d)*?\》|\〈(\s)*(\d+\s)*(\d)*?\〉|\＜(\s)*(\d+\s)*(\d)*?\＞",
                   "", a)
        a = re.sub(r"\<(\s)*(\d+\s)*(\d)*?\》|\<(\s)*(\d+\s)*(\d)*?\〉|\<(\s)*(\d+\s)*(\d)*?\＞",
                   "", a)
        a = re.sub(r"\《(\s)*(\d+\s)*(\d)*?\>|\《(\s)*(\d+\s)*(\d)*?\〉|\《(\s)*(\d+\s)*(\d)*?\＞",
                   "", a)
        a = re.sub(r"\〈(\s)*(\d+\s)*(\d)*?\>|\〈(\s)*(\d+\s)*(\d)*?\》|\〈(\s)*(\d+\s)*(\d)*?\＞",
                   "", a)
        a = re.sub(r"\＜(\s)*(\d+\s)*(\d)*?\>|\＜(\s)*(\d+\s)*(\d)*?\》|\＜(\s)*(\d+\s)*(\d)*?\〉",
                   "", a)
        return a

    def default_clean(self, a):  # 最基本功能块
        # 【共同块】不管是全中文/全英文/中英混排，都需要清除的不规范的符号与排版
        # 清除文档排版符号
        a = a.replace('\t', '')

        # 清除连续空格（如连续两个和三个空格）
        for i in range(10):
            a = a.replace('   ', ' ')
            a = a.replace('  ', ' ')
            a = a.replace('，，，', '，')
            a = a.replace('，，', '，')
            a = a.replace(',,,', ',')
            a = a.replace(',,', ',')

        # 清除那些引用标记（括号内为纯数字），如圈圈数字和方括号引用，同时由于方括号和六角括号混用较多，清理前后不搭的情况中的引用符号
        a = re.sub(u'\u24EA|[\u2460-\u2473]|[\u3251-\u325F]|[\u32B1-\u32BF]|[\u2776-\u277F]|\u24FF|[\u24EB-\u24F4]',
                   "", a)
        a = a.replace('◎', '')
        a = a.replace('®', '')
        a = a.replace('*', '')

        # 错误标点纠正：将奇怪的弯引号换为正常的弯引号，为下面执行弯引号与直引号的清除提供条件
        a = a.replace('〞', '”')
        a = a.replace('〝', '“')

        # 错误标点纠正：将角分符号（′）替换为弯引号（若需要使用角分符号则不运行此条）
        a = a.replace('′', "’")
        # 错误标点纠正：将角秒符号（″）替换为弯引号（若需要使用角秒符号则不运行此条）
        a = a.replace('″', '”')

        # 错误标点纠正1（两个同向单引号变成一个双引号<前>，改为前后弯双引号）
        pattern = re.compile(r'‘‘(.*?)”')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('‘‘{}”'.format(i), '“{}”'.format(i))

        # 错误标点纠正2（两个同向单引号变成一个双引号<后>，改为前后弯双引号）
        p1 = r"(?<=“).+?(?=’’)"
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace('“{}’’'.format(i), '“{}”'.format(i))

        # 错误标点纠正3（前后两个单引号变成一组双引号）
        pattern = re.compile(r'‘‘(.*?)’’')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('‘‘{}’’'.format(i), '“{}”'.format(i))

        # 错误标点纠正4（两个同向双引号去掉一个<前>）
        pattern = re.compile(r'““(.*?)”')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('““{}”'.format(i), '“{}”'.format(i))

        # 错误标点纠正5（两个同向双引号去掉一个<后>）
        p1 = r"(?<=“).+?(?=””)"
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace('“{}””'.format(i), '“{}”'.format(i))

        # 错误标点纠正6（两组双引号变成一组双引号）
        pattern = re.compile(r'““(.*?)””')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('““{}””'.format(i), '“{}”'.format(i))

        # 错误标点纠正7（前直单引号<前>，后弯双引号<后>，改为前后弯双引号）
        pattern = re.compile(r"'(.*?)”")
        result = pattern.findall(a)
        for i in result:
            a = a.replace("'{}”".format(i), '“{}”'.format(i))

        # 错误标点纠正8（前直双引号<前>，后弯双引号<后>，改为前后弯双引号）
        pattern = re.compile(r'"(.*?)”')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('"{}”'.format(i), '“{}”'.format(i))

        # 错误标点纠正9（前弯双引号<前>，后直单引号<后>，改为前后弯双引号）
        p1 = r"(?<=“).+?(?=')"
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace("“{}'".format(i), '“{}”'.format(i))

        # 错误标点纠正10（前弯双引号<前>，后直双引号<后>，改为前后弯双引号）
        p1 = r'(?<=“).+?(?=")'
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace('“{}"'.format(i), '“{}”'.format(i))

        # 将成对的直双引号改为成对的弯双引号
        pattern = re.compile(r'"(.*?)"')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('"{}"'.format(i), '“{}”'.format(i))

        # 将成对的直单引号改为成对的弯单引号
        pattern = re.compile(r"'(.*?)'")
        result = pattern.findall(a)
        for i in result:
            a = a.replace("'{}'".format(i), "‘{}’".format(i))

        # 对文段进行再次多余部分的清洗
        # 错误标点纠正1（两个同向单引号变成一个双引号<前>，改为前后弯双引号）
        pattern = re.compile(r'‘‘(.*?)”')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('‘‘{}”'.format(i), '“{}”'.format(i))

        # 错误标点纠正2（两个同向单引号变成一个双引号<后>，改为前后弯双引号）
        p1 = r"(?<=“).+?(?=’’)"
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace('“{}’’'.format(i), '“{}”'.format(i))

        # 错误标点纠正3（前后两个单引号变成一组双引号）
        pattern = re.compile(r'‘‘(.*?)’’')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('‘‘{}’’'.format(i), '“{}”'.format(i))

        # 错误标点纠正4（两个同向双引号去掉一个<前>）
        pattern = re.compile(r'““(.*?)”')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('““{}”'.format(i), '“{}”'.format(i))

        # 错误标点纠正5（两个同向双引号去掉一个<后>）
        p1 = r"(?<=“).+?(?=””)"
        pattern1 = re.compile(p1)
        result = pattern1.findall(a)
        for i in result:
            a = a.replace('“{}””'.format(i), '“{}”'.format(i))

        # 错误标点纠正6（两组双引号变成一组双引号）
        pattern = re.compile(r'““(.*?)””')
        result = pattern.findall(a)
        for i in result:
            a = a.replace('““{}””'.format(i), '“{}”'.format(i))

        # 将单独的单双直引号替换为空(清除剩余的直引号)
        a = a.replace("'", '')
        a = a.replace('"', '')

        # 【判断块】判断文段是全中文、全英文还是中英混排。
        def containenglish(str0):  # 判断是否包含英文字母
            import re
            return bool(re.search('[a-zA-Zａ-ｚＡ-Ｚ]', str0))

        def is_contain_chinese(check_str):  # 判断是否包含中文字
            for ch in check_str:
                if u'\u4e00' <= ch <= u'\u9fff':
                    return True
            return False

        def is_contain_num(str0):  # 判断是否包含数字
            import re
            return bool(re.search('[0-9０-９]', str0))

        def is_contain_symbol(keyword):
            if re.search(r"\W", keyword):
                return True
            else:
                return False

        if is_contain_num(str(a)) and not containenglish(str(a)) and not is_contain_chinese(str(a)):
            # 【全数块】清除数字中的空格，将全角数字转为半角数字
            a = a.replace(' ', '')

            def is_Qnumber(uchar):
                """判断一个unicode是否是全角数字"""
                if uchar >= u'\uff10' and uchar <= u'\uff19':
                    return True
                else:
                    return False

            def Q2B(uchar):
                """单个字符 全角转半角"""
                inside_code = ord(uchar)
                if inside_code == 0x3000:
                    inside_code = 0x0020
                else:
                    inside_code -= 0xfee0
                if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                    return uchar
                return chr(inside_code)

            def stringpartQ2B(ustring):
                """把字符串中数字全角转半角"""
                return "".join(
                    [Q2B(uchar) if is_Qnumber(uchar) else uchar for uchar in ustring])

            a = stringpartQ2B(a)

            # 对全数字文段的货币符号、百分号和度数这三个符号进行专门处理
            i = 0
            while i <= len(a) - 1:
                if a[i] == '¥' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == '$' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == "%":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                if a[i] == "°":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            a = a.replace('  ', ' ')
            return a

        elif not containenglish(str(a)) and is_contain_chinese(str(a)):
            # 【中（数）块】
            # 去除不必要的中英文符号及空格
            a = a.replace('*', '')
            a = a.replace(' ', '')
            a = a.replace('#', '')
            # a = a.replace('^', '')
            a = a.replace('~', '')
            a = a.replace('～', '')

            # 修改一些排版中常见的符号错误
            a = a.replace('。。', '。')
            a = a.replace('。。。', '……')
            a = a.replace('—', "——")
            a = a.replace('一一', "——")
            # Black Circle, Katakana Middle Dot, Bullet, Bullet Operator 替换为标准中间点（U+00B7 MIDDLE DOT）
            a = a.replace('●', "·")
            a = a.replace('・', "·")
            a = a.replace('•', "·")
            a = a.replace('∙', "·")
            # U+2027 HYPHENATION POINT 替换为中间点（U+00B7 MIDDLE DOT）
            a = a.replace('‧', "·")
            # 加重符号、乘号、点号替换为中间点（U+00B7 MIDDLE DOT）【如果使用乘号，应使用叉号乘，慎用点乘】
            a = a.replace('•', "·")
            a = a.replace('·', "·")
            a = a.replace('▪', "·")
            # Phoenician Word Separator (U+1091F) to middle dot
            a = a.replace('𐤟', "·")
            for i in range(10):
                a = a.replace('————————', "——")
                a = a.replace('——————', "——")
                a = a.replace('————', "——")

            # 将中文和数字混排中的全角数字转为半角数字，不改变标点的全半角情况
            def is_Qnumber(uchar):
                """判断一个unicode是否是全角数字"""
                if uchar >= u'\uff10' and uchar <= u'\uff19':
                    return True
                else:
                    return False

            def Q2B(uchar):
                """单个字符 全角转半角"""
                inside_code = ord(uchar)
                if inside_code == 0x3000:
                    inside_code = 0x0020
                else:
                    inside_code -= 0xfee0
                if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                    return uchar
                return chr(inside_code)

            def stringpartQ2B(ustring):
                """把字符串中数字全角转半角"""
                return "".join(
                    [Q2B(uchar) if is_Qnumber(uchar) else uchar for uchar in ustring])

            a = stringpartQ2B(a)

            # 给中文和数字的混排增加空格
            def find_this(q, i):
                result = q[i]
                return result

            def find_next(q, i):
                result = q[i + 1]
                return result

            i = 0
            while i >= 0 and i < len(a) - 1:
                if is_contain_chinese(str(find_this(a, i))) and is_contain_num(str(find_next(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 1, ' ')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(a, i))) and is_contain_num(str(find_this(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 1, ' ')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 将常用英文标点转换为中文标点
            def E_trans_to_C(string):
                E_pun = u',.;:!?()<>'
                C_pun = u'，。；：！？（）《》'
                table = {ord(f): ord(t) for f, t in zip(E_pun, C_pun)}
                return string.translate(table)

            a = E_trans_to_C(str(a))

            # 对特殊数字符号进行处理
            i = 0
            while i <= len(a) - 1:
                if a[i] == '¥' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == '$' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == "%":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                if a[i] == "°":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            a = a.replace('  ', ' ')
            return a

        elif containenglish(str(a)) and not is_contain_chinese(str(a)):
            # 【英（数）块】给英文和数字混排的情况增加空格
            def find_this(q, i):
                result = q[i]
                return result

            def find_next(q, i):
                result = q[i + 1]
                return result

            i = 0
            while i >= 0 and i < len(a) - 1:
                if is_contain_num(str(find_this(a, i))) and containenglish(str(find_next(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 1, ' ')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(a, i))) and containenglish(str(find_this(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 1, ' ')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 将全角英文字符和数字转为半角英文和半角数字
            def is_Qnumber(uchar):
                """判断一个unicode是否是全角数字"""
                if uchar >= u'\uff10' and uchar <= u'\uff19':
                    return True
                else:
                    return False

            def is_Qalphabet(uchar):
                """判断一个unicode是否是全角英文字母"""
                if (uchar >= u'\uff21' and uchar <= u'\uff3a') or (uchar >= u'\uff41' and uchar <= u'\uff5a'):
                    return True
                else:
                    return False

            def Q2B(uchar):
                """单个字符 全角转半角"""
                inside_code = ord(uchar)
                if inside_code == 0x3000:
                    inside_code = 0x0020
                else:
                    inside_code -= 0xfee0
                if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                    return uchar
                return chr(inside_code)

            def stringpartQ2B(ustring):
                """把字符串中字母和数字全角转半角"""
                return "".join(
                    [Q2B(uchar) if is_Qnumber(uchar) or is_Qalphabet(uchar) else uchar for uchar in ustring])

            a = stringpartQ2B(a)

            # 将文段中的中文符号转换为英文符号
            def C_trans_to_E(string):
                E_pun = u',.;:!?[]()<>'
                C_pun = u'，。；：！？【】（）《》'
                table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
                return string.translate(table)

            a = C_trans_to_E(str(a))

            # One Dot Leader (U+2024) to full stop (U+002E) （句号）
            a = a.replace('․', ".")

            # 清除英文标点符号前面的空格（,.;:?!）
            a = list(a)
            i = 0
            while i >= 0 and i < len(a) - 1:
                if a[i] == ',':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if a[i] == '.':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if a[i] == ';':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if a[i] == ':':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if a[i] == '?':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if a[i] == '!':
                    if a[i - 1] == ' ':
                        del a[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                else:
                    i = i + 1
                    continue
            a = ''.join(a)

            # 对全数字文段的货币符号、百分号和度数这三个符号进行专门处理
            i = 0
            while i <= len(a) - 1:
                if a[i] == '¥' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == '$' and not is_contain_symbol(str(a[i - 1])):
                    a = list(a)
                    a.insert(i, ' ')
                    a = ''.join(a)
                    i = i + 2
                    continue
                if a[i] == "%":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                if a[i] == "°":
                    if a[i - 1] == ' ':
                        a = list(a)
                        del a[i - 1]
                        a = ''.join(a)
                        i = i - 1
                        continue
                    else:
                        a = list(a)
                        a.insert(i + 1, ' ')
                        a = ''.join(a)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            a = a.replace('  ', ' ')
            return a

        elif containenglish(str(a)) and is_contain_chinese(str(a)) or \
                containenglish(str(a)) and is_contain_chinese(str(a)) and is_contain_num(str(a)):
            # 【中英（数）混排块】识别中英文字符，对英文字符保留空格，对中文字符去掉空格。标点默认使用原文标点，以中文为主（默认使用情况为在中文中引用英文）。
            def find_this(q, i):
                result = q[i]
                return result

            def find_pre(q, i):
                result = q[i - 1]
                return result

            def find_next(q, i):
                result = q[i + 1]
                return result

            def find_pre2(q, i):
                result = q[i - 2]
                return result

            def find_next2(q, i):
                result = q[i + 2]
                return result

            def find_next3(q, i):
                result = q[i + 3]
                return result

            # 首先来一遍此一后一的精准筛查
            i = 0
            while i >= 0 and i < len(a) - 1:
                if is_contain_chinese(str(find_this(a, i))) and containenglish(str(find_next(a, i))):  # 从中文转英文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_this(a, i))) and is_contain_num(str(find_next(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(a, i))) and is_contain_num(str(find_this(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_this(a, i))) and containenglish(str(find_next(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(a, i))) and containenglish(str(find_this(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(a, i))) and containenglish(str(find_this(a, i))):  # 从英文转中文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 再进行前一后一的插入
            i = 1
            while i > 0 and i < len(a) - 1:
                if is_contain_chinese(str(find_pre(a, i))) and containenglish(str(find_next(a, i))):  # 从中文转英文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_pre(a, i))) and is_contain_num(str(find_next(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(a, i))) and is_contain_num(str(find_pre(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_pre(a, i))) and containenglish(str(find_next(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(a, i))) and containenglish(str(find_pre(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(a, i))) and containenglish(str(find_pre(a, i))):  # 从英文转中文
                    a = list(a)
                    a.insert(i + 1, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 进行前一后二的筛查
            i = 1
            while i > 0 and i < len(a) - 2:
                if is_contain_chinese(str(find_pre(a, i))) and containenglish(str(find_next2(a, i))):  # 从中文转英文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_pre(a, i))) and is_contain_num(str(find_next2(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next2(a, i))) and is_contain_num(str(find_pre(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_pre(a, i))) and containenglish(str(find_next2(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next2(a, i))) and containenglish(str(find_pre(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next2(a, i))) and containenglish(str(find_pre(a, i))):  # 从英文转中文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 再进行前二后二的筛查
            i = 1
            while i > 0 and i < len(a) - 2:
                if is_contain_chinese(str(find_pre2(a, i))) and containenglish(str(find_next2(a, i))):  # 从中文转英文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_pre2(a, i))) and is_contain_num(str(find_next2(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next2(a, i))) and is_contain_num(str(find_pre2(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_pre2(a, i))) and containenglish(str(find_next2(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next2(a, i))) and containenglish(str(find_pre2(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next2(a, i))) and containenglish(str(find_pre2(a, i))):  # 从英文转中文
                    a = list(a)
                    a.insert(i + 2, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 最后进行一次前二后三的检查，这个比较少见，只在「武力⋯⋯”(1974」这个情况中存在
            i = 1
            while i > 0 and i < len(a) - 3:
                if is_contain_chinese(str(find_pre2(a, i))) and containenglish(str(find_next3(a, i))):  # 从中文转英文
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_pre2(a, i))) and is_contain_num(str(find_next3(a, i))):  # 从中文转数字
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next3(a, i))) and is_contain_num(str(find_pre2(a, i))):  # 从数字转中文
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_pre2(a, i))) and containenglish(str(find_next3(a, i))):  # 从数字转英文
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next3(a, i))) and containenglish(str(find_pre2(a, i))):  # 从英文转数字
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next3(a, i))) and containenglish(str(find_pre2(a, i))):  # 从英文转中文
                    a = list(a)
                    a.insert(i + 3, '*')
                    a = ''.join(a)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 将多个*号替换成一个*。
            a = a.replace('*****', "*")
            a = a.replace('****', "*")
            a = a.replace('***', "*")
            a = a.replace("**", "*")

            # 转换为三个列表（考虑在每个星号之后打上顺序，这样成为了列表后每个元素有一个代码i☆
            b = a.split('*')
            i = 0
            while i >= 0 and i <= len(b) - 1:
                b[i] = str(i + 1), '☆', b[i], '*'
                b[i] = ''.join(b[i])
                i = i + 1
                continue

            b_ch = []  # 中文（待清理）
            for i in range(len(b)):
                b_ch.append(b[i])
            c_en = []  # 英文（待清理）
            for i in range(len(b)):
                c_en.append(b[i])
            d_nu = []  # 数字（待清理）
            for i in range(len(b)):
                d_nu.append(b[i])

            # 读取列表元素中☆之后的元素，定义一个函数
            def qingli(k, i):
                x = k[i]
                z = x.index("☆") + 1
                y = x[z: len(x)]
                return y

            # 执行清理
            n = 0
            while n <= len(b_ch) - 1:
                if containenglish(str(qingli(b_ch, n))) or is_contain_num(str(qingli(b_ch, n))):
                    del b_ch[n]  # 中文，除掉英文和数字
                    n = n
                    continue
                else:
                    n = n + 1
                    continue

            n = 0
            while n <= len(c_en) - 1:
                if is_contain_chinese(str(qingli(c_en, n))) or is_contain_num(str(qingli(c_en, n))):
                    del c_en[n]  # 英文，除掉中文和数字
                    n = n
                    continue
                else:
                    n = n + 1
                    continue

            n = 0
            while n <= len(d_nu) - 1:
                if is_contain_chinese(str(qingli(d_nu, n))) or containenglish(str(qingli(d_nu, n))):
                    del d_nu[n]  # 数字，除掉中文和英文
                    n = n
                    continue
                else:
                    n = n + 1
                    continue

            # 【对中文处理】
            zh = ''.join(b_ch)
            # 去除不必要的中英文符号及空格
            zh = zh.replace(' ', '')
            zh = zh.replace('#', '')
            zh = zh.replace('^', '')
            zh = zh.replace('~', '')
            zh = zh.replace('～', '')

            # 修改一些排版中常见的符号错误
            zh = zh.replace('。。', '。')
            zh = zh.replace('。。。', '……')
            zh = zh.replace('—', "——")
            zh = zh.replace('一一', "——")
            # Black Circle, Katakana Middle Dot, Bullet, Bullet Operator 替换为标准中间点（U+00B7 MIDDLE DOT）
            zh = zh.replace('●', "·")
            zh = zh.replace('・', "·")
            zh = zh.replace('•', "·")
            zh = zh.replace('∙', "·")
            # U+2027 HYPHENATION POINT 替换为中间点（U+00B7 MIDDLE DOT）
            zh = zh.replace('‧', "·")
            # 加重符号、乘号、点号替换为中间点（U+00B7 MIDDLE DOT）
            zh = zh.replace('•', "·")
            zh = zh.replace('·', "·")
            zh = zh.replace('▪', "·")
            # Phoenician Word Separator (U+1091F) to middle dot
            zh = zh.replace('𐤟', "·")
            for i in range(10):
                zh = zh.replace('————————', "——")
                zh = zh.replace('——————', "——")
                zh = zh.replace('————', "——")

            # 将常用英文标点转换为中文标点
            def E_trans_to_C(string):
                E_pun = u',.;:!?()<>'
                C_pun = u'，。；：！？（）《》'
                table = {ord(f): ord(t) for f, t in zip(E_pun, C_pun)}
                return string.translate(table)

            zh = E_trans_to_C(str(zh))

            # 合成待整合的中文列表
            zh_he = zh.split('*')

            def Q2B(uchar):
                """单个字符 全角转半角"""
                inside_code = ord(uchar)
                if inside_code == 0x3000:
                    inside_code = 0x0020
                else:
                    inside_code -= 0xfee0
                if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                    return uchar
                return chr(inside_code)

            # 【对英文处理】将全角英文字母转为半角英文字母，不改变符号的全半角，标点符号（,.;:?!）前面去空格。
            en = ''.join(c_en)

            def is_Qalphabet(uchar):
                """判断一个unicode是否是全角英文字母"""
                if (uchar >= u'\uff21' and uchar <= u'\uff3a') or (uchar >= u'\uff41' and uchar <= u'\uff5a'):
                    return True
                else:
                    return False

            def stringpartQ2B(ustring):
                """把字符串中字母全角转半角"""
                return "".join([Q2B(uchar) if is_Qalphabet(uchar) else uchar for uchar in ustring])

            en = stringpartQ2B(en)

            # One Dot Leader (U+2024) to full stop (U+002E) （句号）
            en = en.replace('․', ".")

            # 去除标点符号前面的空格
            en = list(en)
            i = 0
            while i >= 0 and i < len(en) - 1:
                if en[i] == ',':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if en[i] == '.':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if en[i] == ';':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if en[i] == ':':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if en[i] == '?':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if en[i] == '!':
                    if en[i - 1] == ' ':
                        del en[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                else:
                    i = i + 1
                    continue
            en = ''.join(en)

            en_he = en.split('*')

            # 【对数字处理】将全角数字转为半角数字，不改变符号的全半角
            shu = ''.join(d_nu)

            def is_Qnumber(uchar):
                """判断一个unicode是否是全角数字"""
                if uchar >= u'\uff10' and uchar <= u'\uff19':
                    return True
                else:
                    return False

            def stringpartQ2B(ustring):
                """把字符串中数字全角转半角"""
                return "".join(
                    [Q2B(uchar) if is_Qnumber(uchar) else uchar for uchar in ustring])

            shu = stringpartQ2B(shu)

            shu_he = shu.split('*')

            # 合在一起（存在大于10的数变成小于2的问题，后面解决）
            he = zh_he + en_he + shu_he

            # 清掉空以及前面的顺序符号
            n = 0
            while n >= 0 and n <= len(he) - 1:
                if he[n] == '':
                    he.remove('')
                    continue
                else:
                    n = n + 1
                    continue

            he.sort(key=lambda x: int(x.split('☆')[0]))

            m = 0
            while m >= 0 and m <= len(he) - 1:
                f = he[m]
                g = f.index('☆') + 1
                h = f[g: len(f)]
                he[m] = h
                m = m + 1

            # 将列表转化为字符串相连，这里本可以转化成空格，但是这样会因为分割点问题产生问题，故先整体以"空"合并
            zhong = ''.join(he)

            # 解决因为分块不当带来的括号问题（当括号分到英文块的时候没有被处理到），此处默认全部换成中文括号
            zhong = zhong.replace('(', '（')
            zhong = zhong.replace(')', '）')
            #zhong = zhong.replace('[', '【')
            #zhong = zhong.replace(']', '】')
            zhong = zhong.replace('<', '《')
            zhong = zhong.replace('>', '》')

            # 清除因为分块不当带来的括号、引号、顿号前后的空格
            zhong = list(zhong)
            i = 0
            while i >= 0 and i < len(zhong) - 1:
                if zhong[i] == '（':
                    if zhong[i - 1] == ' ':
                        del zhong[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '）':
                    if zhong[i - 1] == ' ':
                        del zhong[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '、':
                    if zhong[i - 1] == ' ':
                        del zhong[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '“':
                    if zhong[i - 1] == ' ':
                        del zhong[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '”':
                    if zhong[i - 1] == ' ':
                        del zhong[i - 1]
                        continue
                    else:
                        i = i + 1
                        continue
                else:
                    i = i + 1
                    continue

            i = 0
            while i >= 0 and i < len(zhong) - 1:
                if zhong[i] == '（':
                    if zhong[i + 1] == ' ':
                        del zhong[i + 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '）':
                    if zhong[i + 1] == ' ':
                        del zhong[i + 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '、':
                    if zhong[i + 1] == ' ':
                        del zhong[i + 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '“':
                    if zhong[i + 1] == ' ':
                        del zhong[i + 1]
                        continue
                    else:
                        i = i + 1
                        continue
                if zhong[i] == '”':
                    if zhong[i + 1] == ' ':
                        del zhong[i + 1]
                        continue
                    else:
                        i = i + 1
                        continue
                else:
                    i = i + 1
                    continue

            zhong = ''.join(zhong)

            # 给中英数三者相邻的文本插入空格，给特定的单位符号前后增减空格（注意，如果是探索，不能等号，如果是全局修改，必须<=）
            i = 0
            while i <= len(zhong) - 1:
                if zhong[i] == '¥' and not is_contain_symbol(str(zhong[i - 1])):
                    zhong = list(zhong)
                    zhong.insert(i, ' ')
                    zhong = ''.join(zhong)
                    i = i + 2
                    continue
                if zhong[i] == '$' and not is_contain_symbol(str(zhong[i - 1])):
                    zhong = list(zhong)
                    zhong.insert(i, ' ')
                    zhong = ''.join(zhong)
                    i = i + 2
                    continue
                if zhong[i] == "%":
                    if zhong[i - 1] == ' ':
                        zhong = list(zhong)
                        del zhong[i - 1]
                        zhong = ''.join(zhong)
                        i = i - 1
                        continue
                    else:
                        zhong = list(zhong)
                        zhong.insert(i + 1, ' ')
                        zhong = ''.join(zhong)
                        i = i + 2
                        continue
                if zhong[i] == "°":
                    if zhong[i - 1] == ' ':
                        zhong = list(zhong)
                        del zhong[i - 1]
                        zhong = ''.join(zhong)
                        i = i - 1
                        continue
                    else:
                        zhong = list(zhong)
                        zhong.insert(i + 1, ' ')
                        zhong = ''.join(zhong)
                        i = i + 2
                        continue
                else:
                    i = i + 1
                    continue

            i = 0
            while i >= 0 and i < len(zhong) - 1:
                if is_contain_chinese(str(find_this(zhong, i))) and containenglish(str(find_next(zhong, i))):  # 从中文转英文
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_this(zhong, i))) and is_contain_num(str(find_next(zhong, i))):  # 从中文转数字
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(zhong, i))) and is_contain_num(str(find_this(zhong, i))):  # 从数字转中文
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                if is_contain_num(str(find_this(zhong, i))) and containenglish(str(find_next(zhong, i))):  # 从数字转英文
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                if is_contain_num(str(find_next(zhong, i))) and containenglish(str(find_this(zhong, i))):  # 从英文转数字
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                if is_contain_chinese(str(find_next(zhong, i))) and containenglish(str(find_this(zhong, i))):  # 从英文转中文
                    zhong = list(zhong)
                    zhong.insert(i + 1, ' ')
                    zhong = ''.join(zhong)
                    i = i + 1
                    continue
                else:
                    i = i + 1
                    continue

            # 清除连续空格
            zhong = zhong.replace('  ', ' ')
            return zhong

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.FocusIn and isinstance(obj, (QPlainTextEdit, QTextEdit, QLineEdit)):
            self._ocr_last_editor = obj
        return super().eventFilter(obj, event)

    def activate(self):  # 设置窗口显示
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())

        # Determine mode key
        if action10.isChecked():
            mode_key = "compact"
            default_width = int(SCREEN_WEIGHT / 4)
        elif action7.isChecked():
            mode_key = "realtime"
            default_width = int(SCREEN_WEIGHT * 3 / 4)
        else:
            mode_key = "normal"
            default_width = int(SCREEN_WEIGHT / 2)

        # Try to read cached width for current mode and screen size
        try:
            cache_data = codecs.open(BasePath + 'win_width.txt', 'r', encoding='utf-8').read().strip()
            if cache_data:
                parts = cache_data.split('|')
                if len(parts) == 3:
                    cached_mode, cached_screen, cached_width = parts
                    # Use cached width if mode and screen size match
                    if cached_mode == mode_key and int(cached_screen) == SCREEN_WEIGHT:
                        target_width = int(cached_width)
                    else:
                        target_width = default_width
                else:
                    target_width = default_width
            else:
                target_width = default_width
        except:
            target_width = default_width

        # Calculate target position
        target_x = SCREEN_WEIGHT - target_width - 3
        target_y = self.pos().y()

        # Disable updates during setup
        self.setUpdatesEnabled(False)

        # Set everything BEFORE showing window
        self.tab_bar.setVisible(True)
        btna4.setChecked(True)
        self.btn_00.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')

        # Set the correct WIDTH at off-screen position (right edge)
        start_x = SCREEN_WEIGHT - 10
        start_geometry = QRect(start_x, target_y, target_width, DE_HEIGHT)
        self.setGeometry(start_geometry)

        # Re-enable updates
        self.setUpdatesEnabled(True)

        # Save cache with mode and screen info
        cache_str = f"{mode_key}|{SCREEN_WEIGHT}|{target_width}"
        with open(BasePath + 'win_width.txt', 'w', encoding='utf-8') as f0:
            f0.write(cache_str)

        # Show window first (at right edge with correct width)
        self.show()

        # Update self.i to indicate window is now expanded
        # If i is even (collapsed), make it odd (expanded)
        #if self.i % 2 == 0:
        self.i += 1

        # Delay animation to ensure layout is complete, then slide in
        def start_slide_animation():
            animation = QPropertyAnimation(self, b"geometry", self)
            animation.setDuration(250)
            end_geometry = QRect(target_x, target_y, target_width, DE_HEIGHT)
            animation.setEndValue(end_geometry)
            animation.start()

        QTimer.singleShot(100, start_slide_animation)

    def cancel(self):  # 设置取消键的功能
        self.close()


class window4(QWidget):  # Customization settings
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # 设置窗口内布局
        self.setUpMainWindow()
        self.setFixedSize(900, 475)
        self.move(20, 20)
        self.setWindowTitle('Customization settings')
        self.setFocus()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        self.setbar = QTabWidget()
        self.pathbar = QWidget()
        self.latexbar = QWidget()
        # self.aibar = QWidget()
        self.otherbar = QWidget()

        self.setbar.addTab(self.pathbar, "Set Your Paths")
        self.setbar.addTab(self.latexbar, "LaTeX Templates")
        # self.setbar.addTab(self.aibar, "AI settings")
        self.setbar.addTab(self.otherbar, "Others")
        self.setbar.tabBarClicked.connect(self.barclick)

        main_h_box = QHBoxLayout()
        main_h_box.setContentsMargins(0, 20, 0, 0)
        main_h_box.addWidget(self.setbar)
        self.setLayout(main_h_box)

        # Call methods that contain the widgets for each tab
        self.PathBar()
        self.LatexBar()
        # self.AisBar()
        self.OtherBar()

    def PathBar(self):
        wid0_5 = QWidget()
        btn_oneclickmake = QPushButton('Automatically create my path with one click!', self)
        btn_oneclickmake.setMaximumHeight(20)
        btn_oneclickmake.setFixedWidth(360)
        btn_oneclickmake.clicked.connect(self.oneclickmake)
        font = PyQt6.QtGui.QFont()
        font.setBold(True)
        #btn_oneclickmake.setFont(font)
        b0_5 = QHBoxLayout()
        b0_5.setContentsMargins(10, 10, 10, 10)
        b0_5.addStretch()
        b0_5.addWidget(btn_oneclickmake)
        b0_5.addStretch()
        wid0_5.setLayout(b0_5)

        wid1 = QWidget()
        lbl4_1 = QLabel('Articles:', self)
        btn4_1 = QPushButton('Open', self)
        btn4_1.setMaximumHeight(20)
        btn4_1.setMinimumWidth(80)
        btn4_1.clicked.connect(self.locatefile1)
        self.lbl4_11 = QLabel(self)
        b41 = QHBoxLayout()
        b41.setContentsMargins(0, 0, 0, 0)
        b41.addWidget(btn4_1)
        b41.addWidget(lbl4_1)
        b41.addWidget(self.lbl4_11)
        b41.addStretch()
        wid1.setLayout(b41)

        wid2 = QWidget()
        lbl4_2 = QLabel('Authors:', self)
        btn4_2 = QPushButton('Open', self)
        btn4_2.setMaximumHeight(20)
        btn4_2.setMinimumWidth(80)
        btn4_2.clicked.connect(self.locatefile2)
        self.lbl4_21 = QLabel(self)
        b42 = QHBoxLayout()
        b42.setContentsMargins(0, 0, 0, 0)
        b42.addWidget(btn4_2)
        b42.addWidget(lbl4_2)
        b42.addWidget(self.lbl4_21)
        b42.addStretch()
        wid2.setLayout(b42)

        wid3 = QWidget()
        lbl4_3 = QLabel('Institutes:', self)
        btn4_3 = QPushButton('Open', self)
        btn4_3.setMaximumHeight(20)
        btn4_3.setMinimumWidth(80)
        btn4_3.clicked.connect(self.locatefile3)
        self.lbl4_31 = QLabel(self)
        b43 = QHBoxLayout()
        b43.setContentsMargins(0, 0, 0, 0)
        b43.addWidget(btn4_3)
        b43.addWidget(lbl4_3)
        b43.addWidget(self.lbl4_31)
        b43.addStretch()
        wid3.setLayout(b43)

        wid4 = QWidget()
        lbl4_4 = QLabel('Publications:', self)
        btn4_4 = QPushButton('Open', self)
        btn4_4.setMaximumHeight(20)
        btn4_4.setMinimumWidth(80)
        btn4_4.clicked.connect(self.locatefile4)
        self.lbl4_41 = QLabel(self)
        b44 = QHBoxLayout()
        b44.setContentsMargins(0, 0, 0, 0)
        b44.addWidget(btn4_4)
        b44.addWidget(lbl4_4)
        b44.addWidget(self.lbl4_41)
        b44.addStretch()
        wid4.setLayout(b44)

        wid5 = QWidget()
        lbl4_5 = QLabel('Problems:', self)
        btn4_5 = QPushButton('Open', self)
        btn4_5.setMaximumHeight(20)
        btn4_5.setMinimumWidth(80)
        btn4_5.clicked.connect(self.locatefile5)
        self.lbl4_51 = QLabel(self)
        b45 = QHBoxLayout()
        b45.setContentsMargins(0, 0, 0, 0)
        b45.addWidget(btn4_5)
        b45.addWidget(lbl4_5)
        b45.addWidget(self.lbl4_51)
        b45.addStretch()
        wid5.setLayout(b45)

        wid6 = QWidget()
        lbl4_6 = QLabel('Concepts:', self)
        btn4_6 = QPushButton('Open', self)
        btn4_6.setMaximumHeight(20)
        btn4_6.setMinimumWidth(80)
        btn4_6.clicked.connect(self.locatefile6)
        self.lbl4_61 = QLabel(self)
        b46 = QHBoxLayout()
        b46.setContentsMargins(0, 0, 0, 0)
        b46.addWidget(btn4_6)
        b46.addWidget(lbl4_6)
        b46.addWidget(self.lbl4_61)
        b46.addStretch()
        wid6.setLayout(b46)

        wid7 = QWidget()
        lbl4_7 = QLabel('Theories:', self)
        btn4_7 = QPushButton('Open', self)
        btn4_7.setMaximumHeight(20)
        btn4_7.setMinimumWidth(80)
        btn4_7.clicked.connect(self.locatefile7)
        self.lbl4_71 = QLabel(self)
        b47 = QHBoxLayout()
        b47.setContentsMargins(0, 0, 0, 0)
        b47.addWidget(btn4_7)
        b47.addWidget(lbl4_7)
        b47.addWidget(self.lbl4_71)
        b47.addStretch()
        wid7.setLayout(b47)

        wid8 = QWidget()
        lbl4_8 = QLabel('Methods:', self)
        btn4_8 = QPushButton('Open', self)
        btn4_8.setMaximumHeight(20)
        btn4_8.setMinimumWidth(80)
        btn4_8.clicked.connect(self.locatefile8)
        self.lbl4_81 = QLabel(self)
        b48 = QHBoxLayout()
        b48.setContentsMargins(0, 0, 0, 0)
        b48.addWidget(btn4_8)
        b48.addWidget(lbl4_8)
        b48.addWidget(self.lbl4_81)
        b48.addStretch()
        wid8.setLayout(b48)

        wid9 = QWidget()
        lbl4_9 = QLabel('Books:', self)
        btn4_9 = QPushButton('Open', self)
        btn4_9.setMaximumHeight(20)
        btn4_9.setMinimumWidth(80)
        btn4_9.clicked.connect(self.locatefile9)
        self.lbl4_91 = QLabel(self)
        b49 = QHBoxLayout()
        b49.setContentsMargins(0, 0, 0, 0)
        b49.addWidget(btn4_9)
        b49.addWidget(lbl4_9)
        b49.addWidget(self.lbl4_91)
        b49.addStretch()
        wid9.setLayout(b49)

        wid10 = QWidget()
        lbl4_10 = QLabel('My Scripts:', self)
        btn4_10 = QPushButton('Open', self)
        btn4_10.setMaximumHeight(20)
        btn4_10.setMinimumWidth(80)
        btn4_10.clicked.connect(self.locatefile10)
        self.lbl4_101 = QLabel(self)
        b410 = QHBoxLayout()
        b410.setContentsMargins(0, 0, 0, 0)
        b410.addWidget(btn4_10)
        b410.addWidget(lbl4_10)
        b410.addWidget(self.lbl4_101)
        b410.addStretch()
        wid10.setLayout(b410)

        wid11 = QWidget()
        btn4_11 = QPushButton('Save settings and start collecting!', self)
        btn4_11.clicked.connect(self.fullsave)
        btn4_11.setMaximumHeight(20)
        btn4_11.setFixedWidth(360)
        font = PyQt6.QtGui.QFont()
        font.setBold(True)
        btn4_11.setFont(font)
        b411 = QHBoxLayout()
        b411.setContentsMargins(10, 10, 10, 10)
        b411.addStretch()
        b411.addWidget(btn4_11)
        b411.addStretch()
        wid11.setLayout(b411)

        main_h_box = QVBoxLayout()
        main_h_box.addStretch()
        main_h_box.addWidget(wid0_5)
        main_h_box.addWidget(wid5)
        main_h_box.addWidget(wid6)
        main_h_box.addWidget(wid7)
        main_h_box.addWidget(wid8)
        main_h_box.addWidget(wid2)
        main_h_box.addWidget(wid3)
        main_h_box.addWidget(wid4)
        main_h_box.addWidget(wid1)
        main_h_box.addWidget(wid9)
        main_h_box.addWidget(wid10)
        main_h_box.addStretch()
        main_h_box.addWidget(wid11)
        main_h_box.addStretch()
        self.pathbar.setLayout(main_h_box)

    def LatexBar(self):
        self.le_0 = QLineEdit(self)
        self.le_0.setPlaceholderText('Template name')

        self.te_part1 = QTextEdit(self)
        self.te_part1.setFixedHeight(90)
        self.te_part1.setPlaceholderText('''STARTING PART - E.g.: 
%!TEX program = xelatex
% 完整编译: xelatex -> biber/bibtex -> xelatex -> xelatex
\\documentclass[lang=cn,11pt,a4paper]{elegantpaper}''')

        self.te_part2 = QTextEdit(self)
        self.te_part2.setFixedHeight(40)
        self.te_part2.setPlaceholderText('TITLE PART 1 - E.g.: \\title{')

        self.lbl_part2_5 = QLabel('{Your title}', self)

        self.te_part3 = QTextEdit(self)
        self.te_part3.setFixedHeight(40)
        self.te_part3.setPlaceholderText('TITLE PART 2 - E.g.: }')

        self.te_part4 = QTextEdit(self)
        self.te_part4.setFixedHeight(350)
        self.te_part4.setPlaceholderText('''PREAMBULATORY PART - E.g.:
\\author{人名}
\\institute{单位}
\\date{}
% 本文档命令
\\usepackage{array}
\\newcommand{\\ccr}[1]{\\makecell{{\\color{#1}\\rule{1cm}{1cm}}}}
\\usepackage{zhnumber}
\\renewcommand\\thesection{\\zhnum{section}、\\hspace{-1em}}
\\renewcommand\\thesubsection {（\\zhnum{subsection}）\\hspace{-1em}}
\\renewcommand{\\thesubsubsection}{\\hspace{0.5em}\\arabic{subsubsection}.\\hspace{-0.5em}}
\\begin{document}
\\maketitle
\\begin{abstract}
文字。
\\keywords{关键词1，关键词2}
\\end{abstract}''')

        self.te_part5 = QTextEdit(self)
        self.te_part5.setFixedHeight(80)
        self.te_part5.setPlaceholderText('''BIBLIOGRAPHY PART 1 - E.g.:
\\renewcommand\\refname{参考文献}
\\begin{thebibliography}{99}''')

        self.te_part6 = QTextEdit(self)
        self.te_part6.setFixedHeight(80)
        self.te_part6.setPlaceholderText('''BIBLIOGRAPHY PART 2 - E.g.:
\\end{thebibliography} 
\\end{document}''')

        self.checkBox_charep = QCheckBox('Use \\chapter to replace \\section', self)
        self.checkBox_charep.clicked.connect(self.chapterrepsection)
        chapterrep = codecs.open(BasePath + 'chapterreplacesection.txt', 'r', encoding='utf-8').read()
        if chapterrep == '1':
            self.checkBox_charep.setChecked(True)
        if chapterrep == '0':
            self.checkBox_charep.setChecked(False)

        self.btn_set0 = QPushButton('Clear', self)
        self.btn_set0.clicked.connect(self.clearalltemplate)
        self.btn_set0.setFixedSize(120, 20)

        self.btn_set1 = QPushButton('Save and Clear', self)
        self.btn_set1.clicked.connect(self.saveandclear)
        self.btn_set1.setFixedSize(120, 20)

        wid1 = QWidget()
        b1 = QHBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(self.te_part2)
        b1.addWidget(self.lbl_part2_5)
        b1.addWidget(self.te_part3)
        wid1.setLayout(b1)

        wid2 = QWidget()
        b2 = QHBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addStretch()
        b2.addWidget(self.btn_set0)
        b2.addWidget(self.btn_set1)
        b2.addStretch()
        wid2.setLayout(b2)

        main_h_box = QVBoxLayout()
        main_h_box.addStretch()
        main_h_box.addWidget(self.le_0)
        main_h_box.addWidget(self.te_part1)
        main_h_box.addWidget(wid1)
        main_h_box.addWidget(self.te_part4)
        main_h_box.addWidget(self.te_part5)
        main_h_box.addWidget(self.te_part6)
        main_h_box.addWidget(self.checkBox_charep)
        main_h_box.addStretch()
        main_h_box.addWidget(wid2)
        main_h_box.addStretch()
        self.latexbar.setLayout(main_h_box)

    # def AisBar(self):
    #     self.bot_widget1 = QComboBox(self)
    #     self.bot_widget1.setEditable(False)
    #     defalist = ['GPT 3.5 (API - openai)', 'GPT 3.5 (API - httpx)']
    #     self.bot_widget1.addItems(defalist)
    #     Which = codecs.open(BasePath + 'which.txt', 'r', encoding='utf-8').read()
    #     if Which == '0':
    #         self.bot_widget1.setCurrentIndex(0)
    #     if Which == '1':
    #         self.bot_widget1.setCurrentIndex(1)
    #     self.bot_widget1.currentIndexChanged.connect(self.bot_IndexChange)

    #     self.bot_le5 = QLineEdit(self)
    #     self.bot_le5.setPlaceholderText('Temperature here...(how creative you want it to be: from 0 to 1)')
    #     temp = codecs.open(BasePath + 'temp.txt', 'r', encoding='utf-8').read()
    #     if temp != '':
    #         self.bot_le5.setText(temp)
    #     if temp == '':
    #         self.bot_le5.setText('0.5')

    #     self.bot_le6 = QLineEdit(self)
    #     self.bot_le6.setPlaceholderText('Max tokens here...(1024 by default)')
    #     max = codecs.open(BasePath + 'max.txt', 'r', encoding='utf-8').read()
    #     if max != '':
    #         self.bot_le6.setText(max)
    #     if max == '':
    #         self.bot_le6.setText('1024')

    #     self.bot_le8 = QLineEdit(self)
    #     self.bot_le8.setPlaceholderText('Total tokens of a model here...(4096 by default)')
    #     total = codecs.open(BasePath + 'total.txt', 'r', encoding='utf-8').read()
    #     if total != '':
    #         self.bot_le8.setText(total)
    #     if total == '':
    #         self.bot_le8.setText('4096')

    #     self.bot_le7 = QLineEdit(self)
    #     self.bot_le7.setPlaceholderText('Time out after...seconds')
    #     max = codecs.open(BasePath + 'timeout.txt', 'r', encoding='utf-8').read()
    #     if max != '':
    #         self.bot_le7.setText(max)
    #     if max == '':
    #         self.bot_le7.setText('60')

    #     self.bot_checkBox0 = QCheckBox('Show references when chatting with a file', self)
    #     self.bot_checkBox0.clicked.connect(self.bot_showref)
    #     showref = codecs.open(BasePath + 'showref.txt', 'r', encoding='utf-8').read()
    #     if showref == '1':
    #         self.bot_checkBox0.setChecked(True)
    #     if showref == '0':
    #         self.bot_checkBox0.setChecked(False)

    #     self.bot_frame1 = QFrame(self)
    #     self.bot_frame1.setFrameShape(QFrame.Shape.HLine)
    #     self.bot_frame1.setFrameShadow(QFrame.Shadow.Sunken)

    #     self.bot_le1 = QLineEdit(self)
    #     self.bot_le1.setPlaceholderText('API here...')
    #     Apis = codecs.open(BasePath + 'api.txt', 'r', encoding='utf-8').read()
    #     if Apis != '':
    #         self.bot_le1.setText(Apis)

    #     self.bot_checkBox1 = QCheckBox('Third-party:', self)
    #     self.bot_checkBox1.clicked.connect(self.bot_thirdp)
    #     thirdp = codecs.open(BasePath + 'third.txt', 'r',
    #                          encoding='utf-8').read()
    #     if thirdp == '1':
    #         self.bot_checkBox1.setChecked(True)
    #     if thirdp == '0':
    #         self.bot_checkBox1.setChecked(False)

    #     self.bot_le1_1 = QLineEdit(self)
    #     self.bot_le1_1.setPlaceholderText('Third-party API here...only for ChatGPT (API - httpx)')
    #     Apis2 = codecs.open(BasePath + 'api2.txt', 'r', encoding='utf-8').read()
    #     if Apis2 != '':
    #         self.bot_le1_1.setText(Apis2)

    #     self.bot_le1_2 = QLineEdit(self)
    #     self.bot_le1_2.setPlaceholderText('Third-party Endpoint here...only for ChatGPT (API - httpx)')
    #     bear = codecs.open(BasePath + 'bear.txt', 'r', encoding='utf-8').read()
    #     if bear != '':
    #         self.bot_le1_2.setText(bear)

    #     self.bot_frame2 = QFrame(self)
    #     self.bot_frame2.setFrameShape(QFrame.Shape.HLine)
    #     self.bot_frame2.setFrameShadow(QFrame.Shadow.Sunken)

    #     self.bot_te1 = QTextEdit(self)
    #     home_dir = str(Path.home())
    #     tarname1 = "BroccoliAppPath"
    #     fulldir1 = os.path.join(home_dir, tarname1)
    #     if not os.path.exists(fulldir1):
    #         os.mkdir(fulldir1)
    #     tarname2 = "CustomPrompt.txt"
    #     fulldir2 = os.path.join(fulldir1, tarname2)
    #     if not os.path.exists(fulldir2):
    #         with open(fulldir2, 'a', encoding='utf-8') as f0:
    #             f0.write('')
    #     cont = codecs.open(fulldir2, 'r', encoding='utf-8').read()
    #     self.bot_te1.setText(cont)
    #     self.bot_te1.setPlaceholderText(
    #         'This is your storage for prompts. Use {text} to represent parameters and "---" to '
    #         'seperate each other. In <|NAME|><|PROMPT|> format.')

    #     self.bot_te0 = QTextEdit(self)
    #     tarname3 = "lang.txt"
    #     fulldir3 = os.path.join(fulldir1, tarname3)
    #     langs = codecs.open(fulldir3, 'r', encoding='utf-8').read()
    #     self.bot_te0.setText(langs)
    #     self.bot_te0.setPlaceholderText(
    #         'These are languages you want to see in your use. One language name a line, better in original language.')

    #     self.bot_te2 = QTextEdit(self)
    #     tarname4 = "model.txt"
    #     fulldir4 = os.path.join(fulldir1, tarname4)
    #     models = codecs.open(fulldir4, 'r', encoding='utf-8').read()
    #     self.bot_te2.setText(models)
    #     self.bot_te2.setPlaceholderText(
    #         'These are models you would like to use. One model a line.')

    #     self.bot_widget2 = QComboBox(self)
    #     self.bot_widget2.setEditable(False)
    #     if models == '':
    #         modellist = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k-0613']
    #         self.bot_widget2.addItems(modellist)
    #     if models != '':
    #         modellist = models.split('\n')
    #         while '' in modellist:
    #             modellist.remove('')
    #         self.bot_widget2.addItems(modellist)
    #     wp = codecs.open(BasePath + 'wp.txt', 'r', encoding='utf-8').read()
    #     self.bot_widget2.currentIndexChanged.connect(self.bot_IndexChange2)
    #     self.bot_widget2.setCurrentIndex(int(wp))

    #     self.bot_checkBox2 = QCheckBox('Remember chat history when asking new questions', self)
    #     self.bot_checkBox2.clicked.connect(self.bot_rememberhistory)
    #     showhistory = codecs.open(BasePath + 'history.txt', 'r',
    #                               encoding='utf-8').read()
    #     if showhistory == '1':
    #         self.bot_checkBox2.setChecked(True)
    #     if showhistory == '0':
    #         self.bot_checkBox2.setChecked(False)

    #     btn_1 = QPushButton('Save', self)
    #     btn_1.clicked.connect(self.bot_SaveAPI)
    #     btn_1.setFixedSize(80, 20)

    #     qw2 = QWidget()
    #     vbox2 = QHBoxLayout()
    #     vbox2.setContentsMargins(0, 0, 0, 0)
    #     vbox2.addStretch()
    #     vbox2.addWidget(btn_1)
    #     vbox2.addStretch()
    #     qw2.setLayout(vbox2)

    #     self.bot_qw3 = QWidget()
    #     vbox3 = QHBoxLayout()
    #     vbox3.setContentsMargins(0, 0, 0, 0)
    #     vbox3.addWidget(self.bot_le6)
    #     vbox3.addWidget(self.bot_le8)
    #     self.bot_qw3.setLayout(vbox3)

    #     qw4 = QWidget()
    #     vbox4 = QVBoxLayout()
    #     vbox4.setContentsMargins(0, 0, 0, 0)
    #     vbox4.addWidget(self.bot_le1_1)
    #     vbox4.addWidget(self.bot_le1_2)
    #     qw4.setLayout(vbox4)

    #     qw5 = QWidget()
    #     vbox5 = QVBoxLayout()
    #     vbox5.setContentsMargins(0, 0, 0, 0)
    #     vbox5.addWidget(self.bot_checkBox1)
    #     vbox5.addStretch()
    #     qw5.setLayout(vbox5)

    #     self.bot_qw6 = QWidget()
    #     vbox6 = QHBoxLayout()
    #     vbox6.setContentsMargins(0, 0, 0, 0)
    #     vbox6.addWidget(qw5)
    #     vbox6.addWidget(qw4)
    #     self.bot_qw6.setLayout(vbox6)

    #     vbox1 = QVBoxLayout()
    #     vbox1.setContentsMargins(20, 20, 20, 20)
    #     vbox1.addWidget(self.bot_widget1)
    #     vbox1.addWidget(self.bot_widget2)
    #     vbox1.addWidget(self.bot_le5)
    #     vbox1.addWidget(self.bot_qw3)
    #     vbox1.addWidget(self.bot_le7)
    #     vbox1.addWidget(self.bot_checkBox0)
    #     vbox1.addWidget(self.bot_checkBox2)
    #     vbox1.addWidget(self.bot_frame1)
    #     vbox1.addWidget(self.bot_le1)
    #     vbox1.addWidget(self.bot_qw6)
    #     vbox1.addWidget(self.bot_frame2)
    #     vbox1.addWidget(self.bot_te2)
    #     vbox1.addWidget(self.bot_te0)
    #     vbox1.addWidget(self.bot_te1)
    #     vbox1.addWidget(qw2)
    #     self.aibar.setLayout(vbox1)

    #     self.bot_le1.setVisible(True)
    #     self.bot_qw6.setVisible(True)
    #     if self.bot_widget1.currentIndex() == 0:
    #         self.bot_qw6.setVisible(False)

    def OtherBar(self):
        self.other_0 = QLabel('Search link for the Expression tab:', self)

        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "default_link.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write('https://www.collinsdictionary.com/dictionary/english/')
        # ensure citation format dir and list file
        self._ensure_citation_dir()

        self.other_1 = QLineEdit(self)
        self.other_1.setPlaceholderText('The default is Collins Dictionary')

        default_link = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        if default_link != '':
            self.other_1.setText(default_link)

        btn_1 = QPushButton('Save', self)
        btn_1.setFixedWidth(120)
        btn_1.clicked.connect(self.savesearchlink)
        btn_1.setMaximumHeight(20)

        self.other_2 = QLabel('Target language used in explaining the expression:', self)

        self.other_3 = QLineEdit(self)
        self.other_3.setText('English')
        self.other_3.setPlaceholderText('The default is English')

        self.ocr_lang_label = QLabel('OCR language:', self)
        self.ocr_lang_combo = QComboBox(self)
        for name, code in OCR_LANGUAGE_OPTIONS:
            self.ocr_lang_combo.addItem(name, code)
        saved_code = load_ocr_language_code()
        idx = self.ocr_lang_combo.findData(saved_code)
        if idx != -1:
            self.ocr_lang_combo.setCurrentIndex(idx)
        self.ocr_lang_combo.currentIndexChanged.connect(self.ocr_language_changed)

        self.insp_autosave_label = QLabel('Max autosave files for Inspirations:', self)
        self.insp_autosave_combo = QComboBox(self)
        self.insp_autosave_combo.addItems(['30', '50', '100'])
        current_limit = load_inspiration_backup_limit()
        if self.insp_autosave_combo.findText(str(current_limit)) == -1:
            self.insp_autosave_combo.addItem(str(current_limit))
        self.insp_autosave_combo.setCurrentIndex(self.insp_autosave_combo.findText(str(current_limit)))
        self.insp_autosave_combo.currentIndexChanged.connect(self.save_inspiration_autosave_limit)

        # CSL formats
        self.csl_selected_path = ''
        self.csl_btn_style_default = ''
        self.csl_info = QLabel('Citation formats (.csl):', self)
        self.csl_open_btn = QPushButton('Open .csl', self)
        self.csl_open_btn.setFixedWidth(120)
        self.csl_open_btn.clicked.connect(self.open_csl_file)
        self.csl_btn_style_default = self.csl_open_btn.styleSheet()
        self.csl_name_input = QLineEdit(self)
        self.csl_name_input.setPlaceholderText('Name this format')
        self.csl_add_btn = QPushButton('Add', self)
        self.csl_add_btn.setFixedWidth(80)
        self.csl_add_btn.clicked.connect(self.add_csl_format)
        self.csl_list = QListWidget(self)
        self.csl_list.setMaximumHeight(150)
        self.csl_list.itemSelectionChanged.connect(self.csl_selection_changed)
        self.csl_delete_btn = QPushButton('Delete', self)
        self.csl_delete_btn.setFixedWidth(80)
        self.csl_delete_btn.setStyleSheet('color: red')
        self.csl_delete_btn.setEnabled(False)
        self.csl_delete_btn.clicked.connect(self.delete_csl_format)
        self.load_csl_formats()

        t1 = QWidget()
        vboxa = QHBoxLayout()
        vboxa.setContentsMargins(0, 0, 0, 0)
        vboxa.addWidget(self.other_0)
        vboxa.addWidget(self.other_1)
        vboxa.addWidget(btn_1)
        t1.setLayout(vboxa)

        t2 = QWidget()
        vboxa = QHBoxLayout()
        vboxa.setContentsMargins(0, 0, 0, 0)
        vboxa.addWidget(self.other_2)
        vboxa.addWidget(self.other_3)
        t2.setLayout(vboxa)

        t2_ocr = QWidget()
        ocr_box = QHBoxLayout()
        ocr_box.setContentsMargins(0, 0, 0, 0)
        ocr_box.addWidget(self.ocr_lang_label)
        ocr_box.addWidget(self.ocr_lang_combo)
        t2_ocr.setLayout(ocr_box)

        t3 = QWidget()
        vboxb = QHBoxLayout()
        vboxb.setContentsMargins(0, 0, 0, 0)
        vboxb.addWidget(self.insp_autosave_label)
        vboxb.addWidget(self.insp_autosave_combo)
        t3.setLayout(vboxb)

        t4 = QWidget()
        csl_row1 = QHBoxLayout()
        csl_row1.setContentsMargins(0, 0, 0, 0)
        csl_row1.addWidget(self.csl_info)
        csl_row1.addWidget(self.csl_open_btn)
        csl_row1.addWidget(self.csl_name_input)
        csl_row1.addWidget(self.csl_add_btn)
        t4.setLayout(csl_row1)

        t5 = QWidget()
        csl_row2 = QHBoxLayout()
        csl_row2.setContentsMargins(0, 0, 0, 0)
        csl_row2.addWidget(self.csl_list)
        csl_row2.addWidget(self.csl_delete_btn)
        t5.setLayout(csl_row2)

        vbox1 = QVBoxLayout()
        vbox1.setContentsMargins(20, 20, 20, 20)
        vbox1.addWidget(t1)
        vbox1.addWidget(t2)
        vbox1.addWidget(t2_ocr)
        vbox1.addWidget(t3)
        vbox1.addWidget(t4)
        vbox1.addWidget(t5)
        vbox1.addStretch()
        self.otherbar.setLayout(vbox1)

    def savesearchlink(self):
        if self.other_1 != '':
            home_dir = str(Path.home())
            tarname1 = "StrawberryAppPath"
            fulldir1 = os.path.join(home_dir, tarname1)
            if not os.path.exists(fulldir1):
                os.mkdir(fulldir1)
            tarname2 = "default_link.txt"
            fulldir2 = os.path.join(fulldir1, tarname2)
            with open(fulldir2, 'w', encoding='utf-8') as f0:
                f0.write(self.other_1.text().replace('\n', ''))

    def ocr_language_changed(self, index):
        code = self.ocr_lang_combo.currentData()
        if not code:
            return
        save_ocr_language_code(code)
        if 'w3' in globals():
            try:
                w3.reload_ocr_for_language_change()
            except Exception:
                try:
                    w3.reset_ocr_state()
                    w3._load_ocr_reader(show_message=False)
                except Exception:
                    pass

    def save_inspiration_autosave_limit(self):
        save_inspiration_backup_limit(self.insp_autosave_combo.currentText())

    def bot_IndexChange(self, i):
        self.bot_le1.setVisible(True)
        self.bot_qw6.setVisible(True)
        if i == 0:
            with open(BasePath + 'which.txt', 'w', encoding='utf-8') as f0:
                f0.write('0')
            self.bot_qw6.setVisible(False)
        if i == 1:
            with open(BasePath + 'which.txt', 'w', encoding='utf-8') as f0:
                f0.write('1')

    def bot_IndexChange2(self, h):
        with open(BasePath + 'wp.txt', 'w', encoding='utf-8') as f0:
            f0.write(str(h))
        with open(BasePath + 'modelnow.txt', 'w', encoding='utf-8') as f0:
            f0.write(self.bot_widget2.itemText(h))

    def bot_SaveAPI(self):
        with open(BasePath + 'api.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le1.text())
        with open(BasePath + 'api2.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le1_1.text())
        with open(BasePath + 'bear.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le1_2.text())
        with open(BasePath + 'temp.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le5.text())
        with open(BasePath + 'max.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le6.text())
        with open(BasePath + 'timeout.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le7.text())
        with open(BasePath + 'total.txt', 'w', encoding='utf-8') as f1:
            f1.write(self.bot_le8.text())
        home_dir = str(Path.home())
        tarname1 = "BroccoliAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "CustomPrompt.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        with open(fulldir2, 'w', encoding='utf-8') as f0:
            f0.write(self.bot_te1.toPlainText())
        tarname3 = "lang.txt"
        fulldir3 = os.path.join(fulldir1, tarname3)
        with open(fulldir3, 'w', encoding='utf-8') as f0:
            f0.write(self.bot_te0.toPlainText())
        tarname4 = "model.txt"
        fulldir4 = os.path.join(fulldir1, tarname4)
        with open(fulldir4, 'w', encoding='utf-8') as f0:
            f0.write(self.bot_te2.toPlainText())
        self.bot_widget2.clear()
        models = codecs.open(fulldir4, 'r', encoding='utf-8').read()
        if models == '':
            modellist = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k-0613']
            self.bot_widget2.addItems(modellist)
        if models != '':
            modellist = models.split('\n')
            while '' in modellist:
                modellist.remove('')
            self.bot_widget2.addItems(modellist)
        self.close()

    def bot_thirdp(self):
        if self.bot_checkBox1.isChecked():
            with open(BasePath + 'third.txt', 'w', encoding='utf-8') as f0:
                f0.write('1')
        if not self.bot_checkBox1.isChecked():
            with open(BasePath + 'third.txt', 'w', encoding='utf-8') as f0:
                f0.write('0')

    def bot_showref(self):
        if self.bot_checkBox0.isChecked():
            with open(BasePath + 'showref.txt', 'w', encoding='utf-8') as f0:
                f0.write('1')
        if not self.bot_checkBox0.isChecked():
            with open(BasePath + 'showref.txt', 'w', encoding='utf-8') as f0:
                f0.write('0')

    def _ensure_citation_dir(self):
        home_dir = str(Path.home())
        base_dir = os.path.join(home_dir, "StrawberryAppPath")
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        csl_dir = os.path.join(base_dir, "CitationFormat")
        if not os.path.exists(csl_dir):
            os.mkdir(csl_dir)
        list_file = os.path.join(csl_dir, "formats.txt")
        if not os.path.exists(list_file):
            with open(list_file, 'a', encoding='utf-8') as f0:
                f0.write('')
        return csl_dir, list_file

    def load_csl_formats(self):
        csl_dir, list_file = self._ensure_citation_dir()
        formats = codecs.open(list_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '']
        self.csl_list.clear()
        self.csl_list.addItems(formats)
        self.csl_delete_btn.setEnabled(False)
        return csl_dir, list_file

    def open_csl_file(self):
        file_name, ok = QFileDialog.getOpenFileName(self, "Open File", str(Path.home()),
                                                    "CSL Files (*.csl)")
        if file_name != '':
            self.csl_selected_path = file_name
            self.csl_open_btn.setStyleSheet('''border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
        else:
            self.csl_selected_path = ''
            self.csl_open_btn.setStyleSheet(self.csl_btn_style_default)

    def add_csl_format(self):
        csl_dir, list_file = self._ensure_citation_dir()
        name = self.csl_name_input.text().strip()
        if self.csl_selected_path == '' or name == '':
            return
        dest_name = name if name.lower().endswith('.csl') else name + '.csl'
        dest_path = os.path.join(csl_dir, dest_name)
        shutil.copy(self.csl_selected_path, dest_path)
        formats = codecs.open(list_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '']
        if name not in formats:
            formats.append(name)
        with open(list_file, 'w', encoding='utf-8') as f0:
            f0.write('\n'.join(formats))
        self.csl_selected_path = ''
        self.csl_open_btn.setStyleSheet(self.csl_btn_style_default)
        self.csl_name_input.clear()
        self.load_csl_formats()

    def csl_selection_changed(self):
        self.csl_delete_btn.setEnabled(self.csl_list.currentItem() is not None)

    def delete_csl_format(self):
        current = self.csl_list.currentItem()
        if current is None:
            return
        name = current.text()
        csl_dir, list_file = self._ensure_citation_dir()
        formats = codecs.open(list_file, 'r', encoding='utf-8').read().split('\n')
        formats = [i for i in formats if i.strip() != '' and i != name]
        with open(list_file, 'w', encoding='utf-8') as f0:
            f0.write('\n'.join(formats))
        file_candidates = [os.path.join(csl_dir, name),
                           os.path.join(csl_dir, name + '.csl')]
        for fp in file_candidates:
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception:
                    pass
        self.load_csl_formats()

    def bot_rememberhistory(self):
        if self.bot_checkBox2.isChecked():
            with open(BasePath + 'history.txt', 'w', encoding='utf-8') as f0:
                f0.write('1')
        if not self.bot_checkBox2.isChecked():
            with open(BasePath + 'history.txt', 'w', encoding='utf-8') as f0:
                f0.write('0')

    def barclick(self, inex):
        if inex == 0:
            self.setFixedSize(900, 475)
        if inex == 1:
            self.setFixedSize(900, 840)
        # if inex == 2:
        #     self.setFixedSize(900, 840)
        if inex == 2:
            self.setFixedSize(900, 340)

    def saveandclear(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = 'Templates'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.mkdir(fulldir2)

        if self.le_0.text() != '':
            fulldir3 = os.path.join(fulldir2, self.le_0.text())
            os.mkdir(fulldir3)
            # part1
            tarname_p1 = " part1.txt"
            fulldir_p1 = os.path.join(fulldir3, tarname_p1)
            # part2
            tarname_p2 = " part2.txt"
            fulldir_p2 = os.path.join(fulldir3, tarname_p2)
            # part3
            tarname_p3 = " part3.txt"
            fulldir_p3 = os.path.join(fulldir3, tarname_p3)
            # part4
            tarname_p4 = " part4.txt"
            fulldir_p4 = os.path.join(fulldir3, tarname_p4)
            # part5
            tarname_p5 = " part5.txt"
            fulldir_p5 = os.path.join(fulldir3, tarname_p5)
            # part6
            tarname_p6 = " part6.txt"
            fulldir_p6 = os.path.join(fulldir3, tarname_p6)
            with open(fulldir_p1, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part1.toPlainText())
            with open(fulldir_p2, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part2.toPlainText())
            with open(fulldir_p3, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part3.toPlainText())
            with open(fulldir_p4, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part4.toPlainText())
            with open(fulldir_p5, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part5.toPlainText())
            with open(fulldir_p6, 'w', encoding='utf-8') as f0:
                f0.write(self.te_part6.toPlainText())
            self.le_0.clear()
            self.te_part1.clear()
            self.te_part2.clear()
            self.te_part3.clear()
            self.te_part4.clear()
            self.te_part5.clear()
            self.te_part6.clear()

    def clearalltemplate(self):
        self.le_0.clear()
        self.te_part1.clear()
        self.te_part2.clear()
        self.te_part3.clear()
        self.te_part4.clear()
        self.te_part5.clear()
        self.te_part6.clear()

    def chapterrepsection(self):
        if self.checkBox_charep.isChecked():
            with open(BasePath + 'chapterreplacesection.txt', 'w', encoding='utf-8') as f0:
                f0.write('1')
        if not self.checkBox_charep.isChecked():
            with open(BasePath + 'chapterreplacesection.txt', 'w', encoding='utf-8') as f0:
                f0.write('0')

    def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()

    def activate(self):  # 设置窗口显示
        self.show()
        current_limit = load_inspiration_backup_limit()
        if self.insp_autosave_combo.findText(str(current_limit)) == -1:
            self.insp_autosave_combo.addItem(str(current_limit))
        self.insp_autosave_combo.setCurrentIndex(self.insp_autosave_combo.findText(str(current_limit)))
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "DoNotDelete.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            with open(fulldir2, 'a', encoding='utf-8') as f0:
                f0.write('')
        dnd = codecs.open(fulldir2, 'r', encoding='utf-8').read()
        if dnd != '':
            dnd = dnd.rstrip('\n')
            dndl = dnd.split('\n')
            if len(dndl) == 10:
                with open(BasePath + 'path_art.txt', 'w', encoding='utf-8') as f1:
                    f1.write(dndl[0])
                with open(BasePath + 'path_aut.txt', 'w', encoding='utf-8') as f2:
                    f2.write(dndl[1])
                with open(BasePath + 'path_ins.txt', 'w', encoding='utf-8') as f3:
                    f3.write(dndl[2])
                with open(BasePath + 'path_pub.txt', 'w', encoding='utf-8') as f4:
                    f4.write(dndl[3])
                with open(BasePath + 'path_pro.txt', 'w', encoding='utf-8') as f5:
                    f5.write(dndl[4])
                with open(BasePath + 'path_con.txt', 'w', encoding='utf-8') as f6:
                    f6.write(dndl[5])
                with open(BasePath + 'path_the.txt', 'w', encoding='utf-8') as f7:
                    f7.write(dndl[6])
                with open(BasePath + 'path_met.txt', 'w', encoding='utf-8') as f8:
                    f8.write(dndl[7])
                with open(BasePath + 'path_boo.txt', 'w', encoding='utf-8') as f9:
                    f9.write(dndl[8])
                with open(BasePath + 'path_scr.txt', 'w', encoding='utf-8') as f10:
                    f10.write(dndl[9])

        path1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.lbl4_11.setText('The directory is empty. Please check!')
            self.lbl4_11.setStyleSheet('color:red')
        else:
            self.lbl4_11.setText(path1)
            self.lbl4_11.setStyleSheet('color:black')

        path2 = codecs.open(BasePath + 'path_aut.txt', 'r', encoding='utf-8').read()
        if path2 == '':
            self.lbl4_21.setText('The directory is empty. Please check!')
            self.lbl4_21.setStyleSheet('color:red')
        else:
            self.lbl4_21.setText(path2)
            self.lbl4_21.setStyleSheet('color:black')

        path3 = codecs.open(BasePath + 'path_ins.txt', 'r', encoding='utf-8').read()
        if path3 == '':
            self.lbl4_31.setText('The directory is empty. Please check!')
            self.lbl4_31.setStyleSheet('color:red')
        else:
            self.lbl4_31.setText(path3)
            self.lbl4_31.setStyleSheet('color:black')

        path4 = codecs.open(BasePath + 'path_pub.txt', 'r', encoding='utf-8').read()
        if path4 == '':
            self.lbl4_41.setText('The directory is empty. Please check!')
            self.lbl4_41.setStyleSheet('color:red')
        else:
            self.lbl4_41.setText(path4)
            self.lbl4_41.setStyleSheet('color:black')

        path5 = codecs.open(BasePath + 'path_pro.txt', 'r', encoding='utf-8').read()
        if path5 == '':
            self.lbl4_51.setText('The directory is empty. Please check!')
            self.lbl4_51.setStyleSheet('color:red')
        else:
            self.lbl4_51.setText(path5)
            self.lbl4_51.setStyleSheet('color:black')

        path6 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if path6 == '':
            self.lbl4_61.setText('The directory is empty. Please check!')
            self.lbl4_61.setStyleSheet('color:red')
        else:
            self.lbl4_61.setText(path6)
            self.lbl4_61.setStyleSheet('color:black')

        path7 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
        if path7 == '':
            self.lbl4_71.setText('The directory is empty. Please check!')
            self.lbl4_71.setStyleSheet('color:red')
        else:
            self.lbl4_71.setText(path7)
            self.lbl4_71.setStyleSheet('color:black')

        path8 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if path8 == '':
            self.lbl4_81.setText('The directory is empty. Please check!')
            self.lbl4_81.setStyleSheet('color:red')
        else:
            self.lbl4_81.setText(path8)
            self.lbl4_81.setStyleSheet('color:black')

        path9 = codecs.open(BasePath + 'path_boo.txt', 'r', encoding='utf-8').read()
        if path9 == '':
            self.lbl4_91.setText('The directory is empty. Please check!')
            self.lbl4_91.setStyleSheet('color:red')
        else:
            self.lbl4_91.setText(path9)
            self.lbl4_91.setStyleSheet('color:black')

        path10 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path10 == '':
            self.lbl4_101.setText('The directory is empty. Please check!')
            self.lbl4_101.setStyleSheet('color:red')
        else:
            self.lbl4_101.setText(path10)
            self.lbl4_101.setStyleSheet('color:black')
        self.load_csl_formats()

    def fullsave(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "DoNotDelete.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        part1 = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read() + '\n'
        part2 = codecs.open(BasePath + 'path_aut.txt', 'r', encoding='utf-8').read() + '\n'
        part3 = codecs.open(BasePath + 'path_ins.txt', 'r', encoding='utf-8').read() + '\n'
        part4 = codecs.open(BasePath + 'path_pub.txt', 'r', encoding='utf-8').read() + '\n'
        part5 = codecs.open(BasePath + 'path_pro.txt', 'r', encoding='utf-8').read() + '\n'
        part6 = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read() + '\n'
        part7 = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read() + '\n'
        part8 = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read() + '\n'
        part9 = codecs.open(BasePath + 'path_boo.txt', 'r', encoding='utf-8').read() + '\n'
        part10 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read() + '\n'
        with open(fulldir2, 'w', encoding='utf-8') as f0:
            f0.write(part1 + part2 + part3 + part4 + part5 + part6 + part7 +
                     part8 + part9 + part10)
        path10 = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path10 != '':
            tarname_cls = "elegantpaper.cls"
            fulldir_cls = os.path.join(path10, tarname_cls)
            contend_cls = codecs.open(BasePath + 'elegantpaper.cls', 'r', encoding='utf-8').read()
            with open(fulldir_cls, 'w', encoding='utf-8') as f8:
                f8.write(contend_cls)
            tarname_bib = 'reference.bib'
            fulldir_bib = os.path.join(path10, tarname_bib)
            with open(fulldir_bib, 'w', encoding='utf-8') as f8:
                f8.write('')
            tarname_not = "elegantnote.cls"
            fulldir_not = os.path.join(path10, tarname_not)
            contend_not = codecs.open(BasePath + 'elegantnote.cls', 'r', encoding='utf-8').read()
            with open(fulldir_not, 'w', encoding='utf-8') as f8:
                f8.write(contend_not)
            tarname_iee = "IEEEtran.cls"
            fulldir_iee = os.path.join(path10, tarname_iee)
            contend_iee = codecs.open(BasePath + 'IEEEtran.cls', 'r', encoding='utf-8').read()
            with open(fulldir_iee, 'w', encoding='utf-8') as f8:
                f8.write(contend_iee)
            tarname_jor1 = "journalCNdef.tex"
            fulldir_jor1 = os.path.join(path10, tarname_jor1)
            contend_jor1 = codecs.open(BasePath + 'journalCNdef.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor1, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor1)
            tarname_jor2 = "journalCNdef2.tex"
            fulldir_jor2 = os.path.join(path10, tarname_jor2)
            contend_jor2 = codecs.open(BasePath + 'journalCNdef2.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor2, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor2)
            tarname_jor3 = "journalCNpicins.sty"
            fulldir_jor3 = os.path.join(path10, tarname_jor3)
            contend_jor3 = codecs.open(BasePath + 'journalCNpicins.sty', 'r', encoding='utf-8').read()
            with open(fulldir_jor3, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor3)
            tarname_bea = "BeamerCN.sty"
            fulldir_bea = os.path.join(path10, tarname_bea)
            contend_bea = codecs.open(BasePath + 'BeamerCN.sty', 'r', encoding='utf-8').read()
            with open(fulldir_bea, 'w', encoding='utf-8') as f8:
                f8.write(contend_bea)
        self.close()

    def oneclickmake(self):
        home_dir = str(Path.home())
        tarname1 = "Documents"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.makedirs(fulldir1)
        tarname2 = 'Obsidien'
        fulldir2 = os.path.join(fulldir1, tarname2)
        if not os.path.exists(fulldir2):
            os.makedirs(fulldir2)
        tarname3 = 'Database'
        fulldir3 = os.path.join(fulldir2, tarname3)
        if not os.path.exists(fulldir3):
            os.makedirs(fulldir3)
        tarnamea = 'Problems'
        fulldira = os.path.join(fulldir3, tarnamea)
        if not os.path.exists(fulldira):
            os.makedirs(fulldira)
        self.lbl4_51.setText(fulldira)
        self.lbl4_51.setStyleSheet('color:black')
        with open(BasePath + 'path_pro.txt', 'w', encoding='utf-8') as f5:
            f5.write(fulldira)
        tarnameb = 'Concepts'
        fulldirb = os.path.join(fulldir3, tarnameb)
        if not os.path.exists(fulldirb):
            os.makedirs(fulldirb)
        self.lbl4_61.setText(fulldirb)
        self.lbl4_61.setStyleSheet('color:black')
        with open(BasePath + 'path_con.txt', 'w', encoding='utf-8') as f6:
            f6.write(fulldirb)
        tarnamec = 'Theories'
        fulldirc = os.path.join(fulldir3, tarnamec)
        if not os.path.exists(fulldirc):
            os.makedirs(fulldirc)
        self.lbl4_71.setText(fulldirc)
        self.lbl4_71.setStyleSheet('color:black')
        with open(BasePath + 'path_the.txt', 'w', encoding='utf-8') as f7:
            f7.write(fulldirc)
        tarnamed = 'Methods'
        fulldird = os.path.join(fulldir3, tarnamed)
        if not os.path.exists(fulldird):
            os.makedirs(fulldird)
        self.lbl4_81.setText(fulldird)
        self.lbl4_81.setStyleSheet('color:black')
        with open(BasePath + 'path_met.txt', 'w', encoding='utf-8') as f8:
            f8.write(fulldird)
        tarnamee = 'Authors'
        fulldire = os.path.join(fulldir3, tarnamee)
        if not os.path.exists(fulldire):
            os.makedirs(fulldire)
        self.lbl4_21.setText(fulldire)
        self.lbl4_21.setStyleSheet('color:black')
        with open(BasePath + 'path_aut.txt', 'w', encoding='utf-8') as f2:
            f2.write(fulldire)
        tarnamef = 'Institutes'
        fulldirf = os.path.join(fulldir3, tarnamef)
        if not os.path.exists(fulldirf):
            os.makedirs(fulldirf)
        self.lbl4_31.setText(fulldirf)
        self.lbl4_31.setStyleSheet('color:black')
        with open(BasePath + 'path_ins.txt', 'w', encoding='utf-8') as f3:
            f3.write(fulldirf)
        tarnameg = 'Publications'
        fulldirg = os.path.join(fulldir3, tarnameg)
        if not os.path.exists(fulldirg):
            os.makedirs(fulldirg)
        self.lbl4_41.setText(fulldirg)
        self.lbl4_41.setStyleSheet('color:black')
        with open(BasePath + 'path_pub.txt', 'w', encoding='utf-8') as f4:
            f4.write(fulldirg)
        tarnameh = 'Articles'
        fulldirh = os.path.join(fulldir3, tarnameh)
        if not os.path.exists(fulldirh):
            os.makedirs(fulldirh)
        self.lbl4_11.setText(fulldirh)
        self.lbl4_11.setStyleSheet('color:black')
        with open(BasePath + 'path_art.txt', 'w', encoding='utf-8') as f1:
            f1.write(fulldirh)
        tarnamei = 'Books'
        fulldiri = os.path.join(fulldir3, tarnamei)
        if not os.path.exists(fulldiri):
            os.makedirs(fulldiri)
        self.lbl4_91.setText(fulldiri)
        self.lbl4_91.setStyleSheet('color:black')
        with open(BasePath + 'path_boo.txt', 'w', encoding='utf-8') as f9:
            f9.write(fulldiri)
        tarnamej = 'My Scripts'
        fulldirj = os.path.join(fulldir3, tarnamej)
        if not os.path.exists(fulldirj):
            os.makedirs(fulldirj)
        self.lbl4_101.setText(fulldirj)
        self.lbl4_101.setStyleSheet('color:black')
        with open(BasePath + 'path_scr.txt', 'w', encoding='utf-8') as f10:
            f10.write(fulldirj)

    def locatefile1(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_art.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_art.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_11.setText('The directory is empty. Please check!')
            self.lbl4_11.setStyleSheet('color:red')
        else:
            self.lbl4_11.setText(path)
            self.lbl4_11.setStyleSheet('color:black')

    def locatefile2(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_aut.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_aut.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_21.setText('The directory is empty. Please check!')
            self.lbl4_21.setStyleSheet('color:red')
        else:
            self.lbl4_21.setText(path)
            self.lbl4_21.setStyleSheet('color:black')

    def locatefile3(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_ins.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_ins.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_31.setText('The directory is empty. Please check!')
            self.lbl4_31.setStyleSheet('color:red')
        else:
            self.lbl4_31.setText(path)
            self.lbl4_31.setStyleSheet('color:black')

    def locatefile4(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_pub.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_pub.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_41.setText('The directory is empty. Please check!')
            self.lbl4_41.setStyleSheet('color:red')
        else:
            self.lbl4_41.setText(path)
            self.lbl4_41.setStyleSheet('color:black')

    def locatefile5(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_pro.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_pro.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_51.setText('The directory is empty. Please check!')
            self.lbl4_51.setStyleSheet('color:red')
        else:
            self.lbl4_51.setText(path)
            self.lbl4_51.setStyleSheet('color:black')

    def locatefile6(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_con.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_con.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_61.setText('The directory is empty. Please check!')
            self.lbl4_61.setStyleSheet('color:red')
        else:
            self.lbl4_61.setText(path)
            self.lbl4_61.setStyleSheet('color:black')

    def locatefile7(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_the.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_the.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_71.setText('The directory is empty. Please check!')
            self.lbl4_71.setStyleSheet('color:red')
        else:
            self.lbl4_71.setText(path)
            self.lbl4_71.setStyleSheet('color:black')

    def locatefile8(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_met.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_met.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_81.setText('The directory is empty. Please check!')
            self.lbl4_81.setStyleSheet('color:red')
        else:
            self.lbl4_81.setText(path)
            self.lbl4_81.setStyleSheet('color:black')

    def locatefile9(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_boo.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_boo.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_91.setText('The directory is empty. Please check!')
            self.lbl4_91.setStyleSheet('color:red')
        else:
            self.lbl4_91.setText(path)
            self.lbl4_91.setStyleSheet('color:black')

    def locatefile10(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open(BasePath + 'path_scr.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open(BasePath + 'path_scr.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_101.setText('The directory is empty. Please check!')
            self.lbl4_101.setStyleSheet('color:red')
        else:
            self.lbl4_101.setText(path)
            self.lbl4_101.setStyleSheet('color:black')


class window5(QWidget):  # Floating window
    def __init__(self, main_window):
        super().__init__()
        self.w3 = main_window
        self.initUI()
        self.w3.show()

    def initUI(self):  # 设置窗口内布局
        self.setUpMainWindow()
        WEIGHT = int(self.screen().availableGeometry().width() / 2.5)
        HEIGHT = int(50)
        self.resize(WEIGHT, HEIGHT)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width() / 2) - int(WEIGHT / 2)
        SCREEN_HEIGHT = int(self.screen().availableGeometry().height() / 4)
        self.move(SCREEN_WEIGHT, SCREEN_HEIGHT)
        self.setFocus()
        self.raise_()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        WEIGHT = int(self.screen().availableGeometry().width() / 2.5)
        t0 = QWidget()
        self.inputA = QLineEdit(self)
        self.inputA.setPlaceholderText('Press ⌘+⇧+↩ to save and esc to close!')
        self.inputA.setFixedHeight(50)
        self.inputA.setFixedWidth(WEIGHT)
        self.inputA.setStyleSheet('''
            font: 25pt;
            background-color: #ECECEC;
            border: 1px solid #ECECEC;  
            border-radius:9px;
            padding: 0px 10px 0px 10px;
        ''')
        self.btn_ent1 = QPushButton('', self)
        self.btn_ent1.clicked.connect(self.returntext)
        self.btn_ent1.setFixedHeight(1)
        self.btn_ent1.setStyleSheet('''
            border: transparent;
            background-color: transparent;
        ''')
        self.btn_ent1.setShortcut('Ctrl+Shift+Return')

        b0 = QVBoxLayout()
        b0.setContentsMargins(0, 0, 0, 0)
        b0.addWidget(self.inputA)
        b0.addWidget(self.btn_ent1)
        t0.setLayout(b0)

        b1 = QVBoxLayout()
        b1.setContentsMargins(0, 0, 0, 0)
        b1.addWidget(t0)
        self.setLayout(b1)

    def returntext(self):
        towrite = str(self.inputA.text())
        self.w3.textii1.setPlainText(towrite)
        self.w3.addinssc()
        self.inputA.clear()

    def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
            btna6.setChecked(False)

    def cancel(self):  # 设置取消键的功能
        self.close()

    def activate(self):  # 设置窗口显示
        if btna6.isChecked():
            self.show()
            self.setFocus()
            self.raise_()
            self.inputA.setFocus()
        if not btna6.isChecked():
            self.cancel()


style_sheet_ori = '''
    QTabWidget::pane {
        border: 1px solid #ECECEC;
        background: #ECECEC;
        border-radius: 9px;
}
    QWidget#Main {
        border: 1px solid #ECECEC;
        background: #ECECEC;
        border-radius: 9px;
}
    QListView#Select{
        border: 1px solid grey;  
        border-radius:4px;
        padding: 1px 5px 1px 3px; 
        background-clip: border;
        background-color: #FFFFFF;
        color: rgb(113, 113, 113);
        font: 14pt Helvetica;
}
    QPushButton{
        border: 1px outset grey;
        background-color: #FFFFFF;
        border-radius: 4px;
        padding: 1px;
        color: #000000
}
    QPushButton:pressed{
        border: 1px outset grey;
        background-color: #0085FF;
        border-radius: 4px;
        padding: 1px;
        color: #FFFFFF
}
    QPlainTextEdit{
        border: 1px solid grey;  
        border-radius:4px;
        padding: 1px 5px 1px 3px; 
        background-clip: border;
        background-color: #F3F2EE;
        color: #000000;
        font: 14pt Times New Roman;
}
    QPlainTextEdit#edit{
        border: 1px solid grey;  
        border-radius:4px;
        padding: 1px 5px 1px 3px; 
        background-clip: border;
        background-color: #FFFFFF;
        color: rgb(113, 113, 113);
        font: 14pt Helvetica;
}
    QLineEdit{
        border-radius:4px;
        border: 1px solid gray;
        background-color: #FFFFFF;
}
    QTextEdit{
        border: 1px solid grey;  
        border-radius:4px;
        padding: 1px 5px 1px 3px; 
        background-clip: border;
        background-color: #F3F2EE;
        color: #000000;
        font: 14pt Times New Roman;
}
    QListWidget{
        border: 1px solid grey;  
        border-radius:4px;
        padding: 1px 5px 1px 3px; 
        background-clip: border;
        background-color: #F3F2EE;
        color: #000000;
        font: 14pt Times New Roman;
}
    QMessageBox QPushButton {
		min-width: 100px;
		height: 20px;
}
'''


w1 = window_about()  # about
w2 = window_update()  # update
w3 = window3()  # main1
w3.setAutoFillBackground(True)
p = w3.palette()
p.setColor(w3.backgroundRole(), QColor('#ECECEC'))
w3.setPalette(p)
w4 = window4()  # main2
w5 = window5(w3)
action1.triggered.connect(w1.activate)
action2.triggered.connect(w2.activate)
action3.triggered.connect(w5.w3.activate)
action4.triggered.connect(w4.activate)
action5.triggered.connect(w5.w3.focuson)
action6.triggered.connect(w5.w3.editoron)
action7.triggered.connect(w5.w3.realon)
action10.triggered.connect(w5.w3.compact_mode_on)
# tray.activated.connect(w3.activate)
button_action.triggered.connect(w5.w3.activate)
btna2.triggered.connect(w5.w3.focuson2)
btna3.triggered.connect(w5.w3.editoron2)
btna4.triggered.connect(w5.w3.pin_a_tab)
btna5.triggered.connect(w5.w3.realon2)
btna6.triggered.connect(w5.activate)
app.aboutToQuit.connect(w5.w3.cleanup_ocr)
app.setStyleSheet(style_sheet_ori)
app.exec()
