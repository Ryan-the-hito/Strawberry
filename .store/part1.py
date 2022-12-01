#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- encoding:UTF-8 -*-
# coding=utf-8
# coding:utf-8

import codecs
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QSystemTrayIcon, QMenu, QComboBox, QDialog,
                             QDialogButtonBox, QMenuBar, QFrame, QFileDialog,
                             QPlainTextEdit, QTabWidget, QTextEdit, QScrollBar, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QRect, QPoint, QPropertyAnimation, QObjectCleanupHandler
from PyQt6.QtGui import QAction, QIcon, QPixmap, QTextCursor, QColor, QPalette, QPainter
import PyQt6.QtGui
import sys
import webbrowser
import os
from pathlib import Path
import re
import jieba
from pypinyin import lazy_pinyin
import markdown2
import plistlib
import fire
import datetime

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("strmenu.icns")

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

action8 = QAction("📐 Restore size!")
menu.addAction(action8)

action9 = QAction("☁️ Hide dock!(reboot)")
menu.addAction(action9)
action9.setCheckable(True)
dock_st = codecs.open('dock_state.txt', 'r', encoding='utf-8').read()
if dock_st == '1':
    action9.setChecked(True)
if dock_st == '0':
    action9.setChecked(False)

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
sysmenu = QMenuBar()
file_menu = sysmenu.addMenu("&Actions")
file_menu.addAction(button_action)
file_menu.addAction(btna2)
file_menu.addAction(btna3)
file_menu.addAction(btna5)
file_menu.addAction(btna4)