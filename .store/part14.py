class window5(QWidget):  # Floating window
    def __init__(self):
        super().__init__()
        self.initUI()
        self.w3 = window3()
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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def setUpMainWindow(self):
        WEIGHT = int(self.screen().availableGeometry().width() / 2.5)
        t0 = QWidget()
        self.inputA = QLineEdit(self)
        self.inputA.setPlaceholderText('Enter inspirations and press ⌘+⇧+↩!')
        self.inputA.setFixedHeight(50)
        self.inputA.setFixedWidth(WEIGHT)
        self.inputA.setStyleSheet('''
            font: 25pt;
            background-color: #ECECEC;
            border: 1px solid #ECECEC;  
            border-radius:9px;
            padding: 0px 0px 0px 10px;
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
        # self.w3.processtext()
        self.inputA.clear()

    def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()

    def activate(self):  # 设置窗口显示
        if btna6.isChecked():
            self.show()
        if not btna6.isChecked():
            self.cancel()