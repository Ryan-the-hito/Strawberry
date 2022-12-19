class window3(QWidget):  # 主程序的代码块（Find a dirty word!）
    def __init__(self):
        super().__init__()
        self.dragPosition = self.pos()
        self.initUI()

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
        self.show()
        self.tab_bar.setVisible(False)
        with open('win_width.txt', 'w', encoding='utf-8') as f0:
            f0.write(str(self.width()))
        self.new_width = 10
        self.resize(self.new_width, DE_HEIGHT)
        app.setStyleSheet(style_sheet_ori)
        self.pathcheck()
        self.movesysfile()
        if not action9.isChecked():
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
        new_pos = QRect(width, height, self.width(), self.height())
        animation.setEndValue(new_pos)
        animation.start()
        self.i += 1

    def move_window2(self, width, height):
        animation = QPropertyAnimation(self, b"geometry", self)
        animation.setDuration(400)
        new_pos = QRect(width, height, self.width(), self.height())
        animation.setEndValue(new_pos)
        animation.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)

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
            with open('path_art.txt', 'w', encoding='utf-8') as f1:
                f1.write(dndl[0])
            with open('path_aut.txt', 'w', encoding='utf-8') as f2:
                f2.write(dndl[1])
            with open('path_ins.txt', 'w', encoding='utf-8') as f3:
                f3.write(dndl[2])
            with open('path_pub.txt', 'w', encoding='utf-8') as f4:
                f4.write(dndl[3])
            with open('path_pro.txt', 'w', encoding='utf-8') as f5:
                f5.write(dndl[4])
            with open('path_con.txt', 'w', encoding='utf-8') as f6:
                f6.write(dndl[5])
            with open('path_the.txt', 'w', encoding='utf-8') as f7:
                f7.write(dndl[6])
            with open('path_met.txt', 'w', encoding='utf-8') as f8:
                f8.write(dndl[7])
            with open('path_boo.txt', 'w', encoding='utf-8') as f9:
                f9.write(dndl[8])
            with open('path_scr.txt', 'w', encoding='utf-8') as f10:
                f10.write(dndl[9])
        if dnd == '' or len(dndl) != 10:
            self.needpath()

    def movesysfile(self):
        path10 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if path10 != '':
            tarname_cls = "elegantpaper.cls"
            fulldir_cls = os.path.join(path10, tarname_cls)
            contend_cls = codecs.open('elegantpaper.cls', 'r', encoding='utf-8').read()
            with open(fulldir_cls, 'w', encoding='utf-8') as f8:
                f8.write(contend_cls)
            tarname_bib = 'reference.bib'
            fulldir_bib = os.path.join(path10, tarname_bib)
            with open(fulldir_bib, 'w', encoding='utf-8') as f8:
                f8.write('')
            tarname_not = "elegantnote.cls"
            fulldir_not = os.path.join(path10, tarname_not)
            contend_not = codecs.open('elegantnote.cls', 'r', encoding='utf-8').read()
            with open(fulldir_not, 'w', encoding='utf-8') as f8:
                f8.write(contend_not)
            tarname_iee = "IEEEtran.cls"
            fulldir_iee = os.path.join(path10, tarname_iee)
            contend_iee = codecs.open('IEEEtran.cls', 'r', encoding='utf-8').read()
            with open(fulldir_iee, 'w', encoding='utf-8') as f8:
                f8.write(contend_iee)
            tarname_jor1 = "journalCNdef.tex"
            fulldir_jor1 = os.path.join(path10, tarname_jor1)
            contend_jor1 = codecs.open('journalCNdef.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor1, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor1)
            tarname_jor2 = "journalCNdef2.tex"
            fulldir_jor2 = os.path.join(path10, tarname_jor2)
            contend_jor2 = codecs.open('journalCNdef2.tex', 'r', encoding='utf-8').read()
            with open(fulldir_jor2, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor2)
            tarname_jor3 = "journalCNpicins.sty"
            fulldir_jor3 = os.path.join(path10, tarname_jor3)
            contend_jor3 = codecs.open('journalCNpicins.sty', 'r', encoding='utf-8').read()
            with open(fulldir_jor3, 'w', encoding='utf-8') as f8:
                f8.write(contend_jor3)
            tarname_bea = "BeamerCN.sty"
            fulldir_bea = os.path.join(path10, tarname_bea)
            contend_bea = codecs.open('BeamerCN.sty', 'r', encoding='utf-8').read()
            with open(fulldir_bea, 'w', encoding='utf-8') as f8:
                f8.write(contend_bea)

    def assigntoall(self):
        cmd = """osascript -e '''on run
	tell application "System Events" to set activeApp to "Strawberry"
	tell application "System Events" to tell UI element activeApp of list 1 of process "Dock"
		perform action "AXShowMenu"
		click menu item "Options" of menu 1
		click menu item "All Desktops" of menu 1 of menu item "Options" of menu 1
	end tell
end run'''"""
        try:
            os.system(cmd)
        except Exception as e:
            pass

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
        lbl4.setMaximumWidth(80)
        self.wid_word = QComboBox(self)
        self.wid_word.setCurrentIndex(0)
        self.wid_word.setMaximumWidth(275)
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
        if '' in alllist:
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

        btn_sow = QPushButton('Search the expression on Collins Dictionary!', self)
        btn_sow.clicked.connect(self.search_on_web)
        btn_sow.setMaximumHeight(20)

        self.textw1 = QPlainTextEdit(self)
        self.textw1.setReadOnly(False)
        self.textw1.setObjectName("edit")
        self.textw1.setPlaceholderText('Explanations')

        self.lew3 = QLineEdit(self)
        self.lew3.setPlaceholderText('Tags (Use 、if there are many)')

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
        lay1.addWidget(btn_sow)
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
        btn_exp1 = QPushButton('Save edits', self)
        btn_exp1.clicked.connect(self.editcardsave)
        btn_exp1.setMaximumHeight(20)
        btn_exp1.setShortcut('Ctrl+Shift+Return')
        r1 = QVBoxLayout()
        r1.addWidget(self.carda)
        r1.addWidget(self.cardb)
        r1.addWidget(btn_exp1)
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
        self.le2.setPlaceholderText('Use 、if there are many and % after translators')
        b2 = QHBoxLayout()
        b2.setContentsMargins(0, 0, 0, 0)
        b2.addWidget(self.lblread_2)
        b2.addWidget(self.le2)
        self.read_t2.setLayout(b2)

        self.read_t7 = QWidget()
        lbl7 = QLabel('Institutes:', self)
        self.le7 = QLineEdit(self)
        self.le7.setPlaceholderText('Use 、if there are many')
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

        self.read_t5 = QWidget()
        lbl5 = QLabel('Tags:', self)
        self.le5 = QLineEdit(self)
        self.le5.setPlaceholderText('Use 、if there are many')
        b5 = QHBoxLayout()
        b5.setContentsMargins(0, 0, 0, 0)
        b5.addWidget(lbl5)
        b5.addWidget(self.le5)
        self.read_t5.setLayout(b5)

        self.read_t6 = QWidget()
        btn1 = QPushButton('Open', self)
        btn1.clicked.connect(self.openextis)
        btn1.setMaximumHeight(20)
        self.btnmain2 = QPushButton('Add', self)
        self.btnmain2.clicked.connect(self.addmain)
        self.btnmain2.setMaximumHeight(20)
        btn3 = QPushButton('Clear', self)
        btn3.clicked.connect(self.clearabv)
        btn3.setMaximumHeight(20)
        self.btnx4 = QPushButton('🔼', self)
        self.btnx4.clicked.connect(self.showlist)
        self.btnx4.setFixedHeight(20)
        self.btnx4.setFixedWidth(20)
        b6 = QHBoxLayout()
        b6.setContentsMargins(0, 0, 0, 0)
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
        supper1.addWidget(self.read_t5)
        supper1.addWidget(self.read_t6)
        self.upper1.setLayout(supper1)

        self.widget0 = QComboBox(self)
        self.widget0.setCurrentIndex(0)
        self.widget0.currentIndexChanged.connect(self.index_changed)
        defalist = ['Append at the end (default)']
        if self.le1.text() != '':
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
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

        self.wings_h_box = QVBoxLayout()
        self.wings_h_box.setContentsMargins(0, 0, 0, 0)
        self.wings_h_box.addWidget(self.upper1)
        self.wings_h_box.addWidget(self.widget0)
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

        self.sub1()
        self.sub2()
        self.sub3()
        self.sub4()

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
            with open('path_rst.txt', 'w', encoding='utf-8') as f0:
                f0.write('')
        if i != 0 and self.le1.text() != '':
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            if i <= self.widget0.count() - 1:
                tarnum = int(self.widget0.currentIndex() + 1)
                searcde = str(self.widget0.itemText(tarnum))
                searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]')
                sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                if sst != None:
                    with open('path_rst.txt', 'w', encoding='utf-8') as f0:
                        f0.write(sst.group())
            if i == self.widget0.count() - 1:
                with open('path_rst.txt', 'w', encoding='utf-8') as f0:
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
        defalist = ['Append at the end (default)']
        if self.leii1.text() != '':
            pathscr = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".md"
            fulldir1 = os.path.join(pathscr, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            pattern = re.compile(r'## (.*?)\n')
            result = pattern.findall(maintxt)
            result = '☆'.join(result)
            if result != '':
                result = result.replace('#', '')
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
                    'JournalPaper_Chinese', 'Beamer_Chinese', 'TexpadTexGeneral_Chinese']
        self.widgettem.addItems(defalist)

        self.leiinote = QLineEdit(self)
        self.leiinote.setPlaceholderText('Always-on remarks (blank = none)')

        t1_5 = QWidget()
        self.leii2 = QLineEdit(self)
        self.leii2.setPlaceholderText('Number (blank = auto mode)')
        btn_ia = QPushButton('Insert citation', self)
        btn_ia.clicked.connect(self.addcit)
        btn_ia.setMaximumHeight(20)
        sm = QHBoxLayout()
        sm.setContentsMargins(0, 0, 0, 0)
        sm.addWidget(self.leii2, 1)
        sm.addWidget(btn_ia, 1)
        t1_5.setLayout(sm)

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

        t2_5 = QWidget()
        btn_ia1 = QPushButton('Open a script', self)
        btn_ia1.clicked.connect(self.openascr)
        btn_ia1.setMaximumHeight(20)
        btn_ib1 = QPushButton('Close current file', self)
        btn_ib1.clicked.connect(self.clinp)
        btn_ib1.setMaximumHeight(20)
        sm0 = QHBoxLayout()
        sm0.setContentsMargins(0, 0, 0, 0)
        sm0.addWidget(btn_ia1, 1)
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
        b2.addWidget(self.textii1)
        b2.addWidget(t3)
        b2.addWidget(self.widgettem)
        b2.addWidget(self.leiinote)
        b2.addWidget(t1_5)
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

    def chooseind(self, i):
        if i == 0 and self.leii1.text() != '':
            with open('path_pat.txt', 'w', encoding='utf-8') as f0:
                f0.write('')
        if i != 0 and self.leii1.text() != '':
            path1 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
            if i <= self.choosepart.count() - 1:
                tarnum = int(self.choosepart.currentIndex() + 1)
                searcde = str(self.choosepart.itemText(tarnum))
                searcde = searcde.replace('After ', '').replace('[', '\[').replace(']', '\]')
                sst = re.search(r'#(.*?)' + searcde + '[\s\S]*', maintxt)
                if sst != None:
                    with open('path_pat.txt', 'w', encoding='utf-8') as f0:
                        f0.write(sst.group())
            if i == self.choosepart.count() - 1:
                with open('path_pat.txt', 'w', encoding='utf-8') as f0:
                    f0.write('')

    def inps1(self):
        self.textii2 = QTextEdit(self)
        self.textii2.setReadOnly(False)
        self.textii2.textChanged.connect(self.on_text2_textChanged)
        self.scrollbar2 = self.textii2.verticalScrollBar()
        self.scrollbar2.valueChanged.connect(self.scr_cha2)

        tvt1 = QWidget()
        self.btn_insia = QPushButton('Insert citation', self)
        self.btn_insia.clicked.connect(self.addcit)
        self.btn_insia.setMaximumHeight(20)
        self.btn_insia.setVisible(False)
        btn_ins1 = QPushButton('Save edits and generate LaTeX', self)
        btn_ins1.clicked.connect(self.saveinsp)
        btn_ins1.setMaximumHeight(20)
        btn_ins1.setShortcut('Ctrl+Shift+Return')
        stvt1 = QHBoxLayout()
        stvt1.setContentsMargins(0, 4, 0, 0)
        stvt1.addWidget(self.btn_insia, 1)
        stvt1.addWidget(btn_ins1, 2)
        tvt1.setLayout(stvt1)

        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.textii2)
        page3_box_h.addWidget(tvt1)
        self.ii1_tab.setLayout(page3_box_h)

    def inps2(self):
        self.textii3 = QTextEdit(self)
        self.textii3.setReadOnly(False)
        btn_ins2 = QPushButton('Save edits', self)
        btn_ins2.clicked.connect(self.savelat)
        btn_ins2.setMaximumHeight(20)
        btn_ins2.setShortcut('Ctrl+Shift+Return')
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.textii3)
        page3_box_h.addWidget(btn_ins2)
        self.ii2_tab.setLayout(page3_box_h)

    def sub1(self):
        self.text = QTextEdit(self)
        self.text.setReadOnly(False)
        self.text.setMinimumHeight(140)
        self.text.textChanged.connect(self.on_text_textChanged)
        self.scrollbar = self.text.verticalScrollBar()
        self.scrollbar.valueChanged.connect(self.scr_cha)
        btn_sub1 = QPushButton('Save edits', self)
        btn_sub1.clicked.connect(self.save1)
        btn_sub1.setMaximumHeight(20)
        btn_sub1.setShortcut('Ctrl+Shift+Return')
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text)
        page3_box_h.addWidget(btn_sub1)
        self.sub1_tab.setLayout(page3_box_h)

    def sub2(self):
        self.text_s2 = QTextEdit(self)
        self.text_s2.setReadOnly(False)
        self.text_s2.setMinimumHeight(140)
        btn_sub2 = QPushButton('Save edits', self)
        btn_sub2.clicked.connect(self.save2)
        btn_sub2.setMaximumHeight(20)
        btn_sub2.setShortcut('Ctrl+Shift+Return')
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s2)
        page3_box_h.addWidget(btn_sub2)
        self.sub2_tab.setLayout(page3_box_h)

    def sub3(self):
        self.text_s3 = QTextEdit(self)
        self.text_s3.setReadOnly(False)
        self.text_s3.setMinimumHeight(140)
        btn_sub3 = QPushButton('Save edits', self)
        btn_sub3.clicked.connect(self.save3)
        btn_sub3.setMaximumHeight(20)
        btn_sub3.setShortcut('Ctrl+Shift+Return')
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s3)
        page3_box_h.addWidget(btn_sub3)
        self.sub3_tab.setLayout(page3_box_h)

    def sub4(self):
        self.text_s4 = QTextEdit(self)
        self.text_s4.setReadOnly(False)
        self.text_s4.setMinimumHeight(140)
        btn_sub4 = QPushButton('Save edits', self)
        btn_sub4.clicked.connect(self.save4)
        btn_sub4.setMaximumHeight(20)
        btn_sub4.setShortcut('Ctrl+Shift+Return')
        page3_box_h = QVBoxLayout()
        page3_box_h.addWidget(self.text_s4)
        page3_box_h.addWidget(btn_sub4)
        self.sub4_tab.setLayout(page3_box_h)

    def ext_r(self):
        self.text11 = QPlainTextEdit(self)
        self.text11.setReadOnly(False)
        self.text11.setObjectName("edit")
        self.text11.setPlaceholderText('Problems / questions')
        sl1 = QWidget()
        self.btn_ex11 = QPushButton('Add', self)
        self.btn_ex11.clicked.connect(self.addprob)
        self.btn_ex11.setMaximumHeight(20)
        btn_111 = QPushButton('Clear', self)
        btn_111.clicked.connect(self.clearpro)
        btn_111.setMaximumHeight(20)
        sm1 = QHBoxLayout()
        sm1.setContentsMargins(0, 0, 0, 0)
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
        page3_box_h.addWidget(self.text11)
        page3_box_h.addWidget(sl1)
        page3_box_h.addWidget(self.text12)
        page3_box_h.addWidget(sl2)
        page3_box_h.addWidget(self.text13)
        page3_box_h.addWidget(sl3)
        page3_box_h.addWidget(self.text14)
        page3_box_h.addWidget(sl4)
        self.one_tab.setLayout(page3_box_h)

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
        self.btn_2k1 = QPushButton('Add', self)
        self.btn_2k1.clicked.connect(self.addexc)
        self.btn_2k1.setMaximumHeight(20)
        btn_211 = QPushButton('Clear', self)
        btn_211.clicked.connect(self.clearexc)
        btn_211.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
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

    def concep(self):
        self.lec1 = QLineEdit(self)
        self.lec1.setPlaceholderText('Name of the concept')
        ex1 = QWidget()
        self.btn_ce31 = QPushButton('Add', self)
        self.btn_ce31.clicked.connect(self.addcon)
        self.btn_ce31.setMaximumHeight(20)
        btn_311 = QPushButton('Clear', self)
        btn_311.clicked.connect(self.clearnam)
        btn_311.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
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

    def theors(self):
        self.lec0 = QLineEdit(self)
        self.lec0.setPlaceholderText('Name of the theory')
        ex0 = QWidget()
        self.btn_the30 = QPushButton('Add', self)
        self.btn_the30.clicked.connect(self.addthero)
        self.btn_the30.setMaximumHeight(20)
        btn_300 = QPushButton('Clear', self)
        btn_300.clicked.connect(self.clthen)
        btn_300.setMaximumHeight(20)
        ec0 = QHBoxLayout()
        ec0.setContentsMargins(0, 0, 0, 0)
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

    def meths(self):
        self.lem1 = QLineEdit(self)
        self.lem1.setPlaceholderText('Name of the method')
        ex1 = QWidget()
        self.btn_51 = QPushButton('Add', self)
        self.btn_51.clicked.connect(self.addmetds)
        self.btn_51.setMaximumHeight(20)
        btn_511 = QPushButton('Clear', self)
        btn_511.clicked.connect(self.clearmetnm)
        btn_511.setMaximumHeight(20)
        ec1 = QHBoxLayout()
        ec1.setContentsMargins(0, 0, 0, 0)
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
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text.setPlainText('Please check your path settings!')
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path1, "Markdown Files (*.md)")
            if file_name != '':
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
                        self.widget0.addItems(['Append at the end (default)'])
                        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
                        tarname1 = str(self.le1.text()) + ".md"
                        fulldir1 = os.path.join(path1, tarname1)
                        maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                        pattern = re.compile(r'## (.*?)\n')
                        result = pattern.findall(maintxt)
                        result = '☆'.join(result)
                        result = result.replace('#', '')
                        result = result.replace('# ', '')
                        result = result.replace('Q/P: ', '')
                        result = result.split('☆')
                        for i in range(len(result)):
                            result[i] = 'After ' + result[i]
                            result[i] = ''.join(result[i])
                        self.widget0.addItems(result)

                        with open('path_ttl.txt', 'w', encoding='utf-8') as f0:
                            f0.write(pretc)

                    self.read_t1.setVisible(False)
                    self.read_t2.setVisible(False)
                    self.read_t7.setVisible(False)
                    self.read_t3.setVisible(False)
                    self.read_t8.setVisible(False)
                    self.read_t4.setVisible(False)
                    self.read_t5.setVisible(False)
                    self.lbltool06.setVisible(False)
                    self.tool8.setVisible(False)
                    self.btnx4.setText('🔽')
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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

                part7 = ''
                if self.le5.text() != '':
                    exptag = str(self.le5.text())
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
                            zove = str(self.le2.text()).split('、')
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
                            zove = str(self.le2.text()).split('、')
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
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('、', ', ') + ', “' + str(self.le1.text()) + ',” *' + \
                                str(self.le3.text()) + '*, ' + str(self.le4_1.text()) + ', ' + str(self.le4.text()) + ', pp.' + \
                                str(self.le10.text()) + '.'
                        if self.le3.text() == '' and self.le8.text() != '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('、', ', ') + ', ' + \
                                      str(self.le8.text()) + ', ' + str(self.le3_1.text()) + ', ' + str(self.le4.text()) + ', pp. ' + \
                                      str(self.le10.text()) + '.'
                    if self.web_t3.isVisible():
                        ISOTIMEFORMAT = '%B %d, %Y'
                        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                        if self.leweb3.text() != '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('、', ', ') + ', “' + str(self.le1.text()) + ',” retrieved ' + \
                            theTime + ', from ' + str(self.leweb3.text())
                        if self.leweb3.text() == '':
                            part7_5 = '\n- ' + 'Citation: ' + str(self.le2.text()).replace('、', ', ') + ', “' + str(self.le1.text()) + ',” paper delivered to ' + \
                                str(self.leweb8.text()) + ', sponsored by ' + str(self.leweb9.text()) + ', ' + str(self.leweb10.text()) + ', ' + str(self.le4_1.text()) + ', ' + str(self.le4.text()) + '.'

                part8 = '\n\n---' + '\n\n# Notes'

                with open(fulldir1, 'a', encoding='utf-8') as f1:
                    f1.write(part1+part2+part3+part4+part5+part5_1+part5_5+part6+part6_5+part7+part7_5+part8)
                with open('path_ttl.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.le1.text())

            path2 = codecs.open('path_aut.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                if self.le2.text() != '':
                    expname2 = str(self.le2.text())
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
                if self.le2.text() == '':
                    self.text.setPlainText('Your input is empty!')

            path3 = codecs.open('path_ins.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.le7.text() != '':
                    expname3 = str(self.le7.text())
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
                if self.le7.text() == '':
                    self.text.setPlainText('Your input is empty!')

            path4 = codecs.open('path_pub.txt', 'r', encoding='utf-8').read()
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
                if self.le3.text() == '':
                    self.text.setPlainText('Your input is empty!')

            path5 = codecs.open('path_boo.txt', 'r', encoding='utf-8').read()
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
                if self.le8.text() == '':
                    self.text.setPlainText('Your input is empty!')

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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            self.read_t5.setVisible(False)
            self.lbltool06.setVisible(False)
            self.tool8.setVisible(False)
            self.btnx4.setText('🔽')
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

    def clearabv(self):
        self.le1.clear()
        self.le2.clear()
        self.le7.clear()
        self.le3.clear()
        self.le3_1.clear()
        self.le4.clear()
        self.le4_1.clear()
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
        self.widget0.addItems(['Append at the end (default)'])
        with open('path_rst.txt', 'w', encoding='utf-8') as f0:
            f0.write('')
        self.le1.setEnabled(True)
        with open('path_ttl.txt', 'w', encoding='utf-8') as fz:
            fz.write('')
        self.leweb3.clear()
        self.read_t1.setVisible(True)
        self.read_t2.setVisible(True)
        self.read_t7.setVisible(True)
        self.read_t3.setVisible(True)
        self.read_t8.setVisible(True)
        self.read_t4.setVisible(True)
        self.read_t5.setVisible(True)
        self.lbltool06.setVisible(True)
        self.tool8.setVisible(True)
        self.btnx4.setText('🔼')
        if self.btn_t9.text() == 'Turned on!':
            self.web_t3.setVisible(True)
            self.web_t8.setVisible(True)
            self.read_t3.setVisible(False)
            self.read_t8.setVisible(False)

    def addprob(self):
        if self.btn_ex11.text() != 'Added and renewed list' and self.le1.text() != '':
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text11.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text11.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = '\n\n## ' + 'Q/P: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text11.toPlainText())))) + '\n'
                part_n = '\n' + get_rst
                if self.le1.text() != '' and self.text11.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            path2 = codecs.open('path_pro.txt', 'r', encoding='utf-8').read()
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
                if self.text11.toPlainText() == '':
                    self.text.setPlainText('Your input is empty!')

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            self.widget0.addItems(['Append at the end (default)'])
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
                        itemnub = result.index(itemold) + 1
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text12.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text12.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = '\n- ' + 'Claim: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text12.toPlainText())))) + '\n'
                part_n = '\n' + get_rst
                if self.le1.text() != '' and self.text12.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text13.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text13.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = ''
                part_n = '\n' + get_rst
                if self.text12.toPlainText() != "":
                    part1 = '\n\t- ' + 'Analysis: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text13.toPlainText())))) + '\n'
                if self.text12.toPlainText() == "":
                    part1 = '\n- ' + 'Analysis: ' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text13.toPlainText())))) + '\n'
                if self.le1.text() != '' and self.text13.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text14.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text14.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part1 = ''
                part_n = '\n' + get_rst
                if self.text12.toPlainText() != '' and self.text13.toPlainText() != '':
                    part1 = '\n\t\t- ' + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() != '':
                    part1 = '\n\t- ' + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() != '' and self.text13.toPlainText() == '':
                    part1 = '\n\t- ' + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.text12.toPlainText() == '' and self.text13.toPlainText() == '':
                    part1 = '\n- ' + '【' + str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.text14.toPlainText())))) + '】' + '\n'
                if self.le1.text() != '' and self.text14.toPlainText() != '':
                    with open(fulldir1, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part_n)

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text21.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text21.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.text22.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text22.setStyleSheet('color:red')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
                # self.text.setStyleSheet('color:red')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lec1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lec1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lec1.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec1.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    with open(fulldir2, 'a', encoding='utf-8') as f0:
                        f0.write('')
                if self.lec1.text() == '':
                    self.text_s2.setPlainText('Your input is empty!')

            pathend2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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
        path2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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

        pathend2 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lec0.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lec0.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lec0.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lec0.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    part1 = ''
                    with open(fulldir2, 'a', encoding='utf-8') as f2:
                        f2.write(part1)
                if self.lec0.text() == '':
                    self.text_s3.setPlainText('Your input is empty!')

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.lem1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                with open(fulldir1, 'a', encoding='utf-8') as f0:
                    f0.write('')
                get_ori = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
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

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.text.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.le1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                if self.le1.text() != '':
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    self.text.setPlainText(contend)
                    posnu = codecs.open('path_rst.txt', 'r', encoding='utf-8').read()
                    self.text.ensureCursorVisible()  # 游标可用
                    cursor = self.text.textCursor()  # 设置游标
                    pos = int(len(self.text.toPlainText()) - len(posnu))  # 获取文本尾部的位置
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.text.setTextCursor(cursor)  # 滚动到游标位置
                    if self.text.verticalScrollBar().maximum() != 0:
                        proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                        tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                        self.real1.verticalScrollBar().setValue(tar_pro)

            path2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
            if path2 == '':
                self.lem1.setText('Some directory is empty. Please go to preferences and check!')
            else:
                if self.lem1.text() != '':
                    tarname2 = str(self.default_clean(self.cleanlinebreak(self.cleancitmak(self.lem1.text())))) + ".md"
                    fulldir2 = os.path.join(path2, tarname2)
                    with open(fulldir2, 'a', encoding='utf-8') as f0:
                        f0.write('')
                if self.lem1.text() == '':
                    self.text_s4.setPlainText('Your input is empty!')

            pathend2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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

            pathend2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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
        path2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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

        pathend2 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = contend.replace(self.tool1_5.text(), self.tool1.text())
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)
            self.tool1.clear()
            self.tool1_5.clear()

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            targ = '[[' + self.tool3.text() + '|' + self.tool2.text() + ']]'
            contend = contend.replace(self.tool2.text(), targ)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)
            self.tool2.clear()
            self.tool3.clear()

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = self.addb(contend)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            path2 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname2 = str(self.le1.text()) + ".md"
            fulldir2 = os.path.join(path2, tarname2)
            contend = codecs.open(fulldir2, 'r', encoding='utf-8').read()
            contend = self.remb(contend)
            with open(fulldir2, 'w', encoding='utf-8') as f2:
                f2.write(contend)

            pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
        if path1 != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Start redirection!", path1, "Markdown Files (*.md)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                contend = self.addb(contend)
                with open(file_name, 'w', encoding='utf-8') as f2:
                    f2.write(contend)

    def anobiooff(self):
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
        pathscr = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
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
        pathend = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if pathend == '':
            self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarnameend = str(self.leii1.text()) + ".md"
            fulldirend = os.path.join(pathend, tarnameend)
            if self.leii1.text() != '':
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.textii2.setPlainText(contend)
                self.textii2.verticalScrollBar().setValue(oldv)
                if self.textii2.verticalScrollBar().maximum() != 0:
                    proportion = self.textii2.verticalScrollBar().value() / self.textii2.verticalScrollBar().maximum()
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
                    tarnameb = self.cleaninput(str(title2).replace('TI  - ', '')) + '.md'
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
                    if 'T2  - ' not in ris_list[i] and 'JF  - ' not in ris_list[i] and 'PB  - ' in ris_each[pp]:
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
                        part13 = '\n- ' + 'Citation: ' + str(pretc2).replace('、', ', ') + ', “' + str(pretc) + ',” *' + \
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

            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
                self.widget0.addItems(['Append at the end (default)'])
                path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.le1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                pattern = re.compile(r'## (.*?)\n')
                result = pattern.findall(maintxt)
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

                with open('path_ttl.txt', 'w', encoding='utf-8') as f0:
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
        b = '🔼'
        if not self.read_t1.isVisible():
            a = True
            b = '🔼'
        if self.read_t1.isVisible():
            a = False
            b = '🔽'
        self.read_t1.setVisible(a)
        self.read_t2.setVisible(a)
        self.read_t7.setVisible(a)
        self.read_t3.setVisible(a)
        self.read_t8.setVisible(a)
        self.read_t4.setVisible(a)
        self.read_t5.setVisible(a)
        self.lbltool06.setVisible(a)
        self.tool8.setVisible(a)
        self.btnx4.setText(b)
        if self.btn_t9.text() == 'Turned on!':
            self.web_t3.setVisible(a)
            self.web_t8.setVisible(a)
            self.read_t3.setVisible(a2)
            self.read_t8.setVisible(a2)

    def openascr(self):
        self.widgettem.setCurrentIndex(0)
        pathscr = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if pathscr == '':
            self.textii2.setPlainText('Please check your path settings!')
        if pathscr != '':
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", pathscr, "Markdown Files (*.md);;LaTeX Files (*.tex)")
            if file_name != '':
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                if pathscr in file_name:
                    if '.md' in file_name:
                        patterna = re.compile(r'\[.*<e>\n')
                        resultp = patterna.findall(contend)
                        resultp = ''.join(resultp)
                        resultp = resultp.rstrip('\n')
                        resultp = resultp.replace('<e>', '')
                        resultp = resultp.replace('<e>\n<e>', '')
                        resultp = resultp.replace('<e><e>', '')
                        with open('path_ref.txt', 'w', encoding='utf-8') as fp:
                            fp.write(resultp)

                        pattern = re.compile(r'<!--Title: (.*?)-->')
                        result = pattern.findall(contend)
                        result = ''.join(result)
                        pretc = result.replace('<!--Title: ', '')
                        pretc = pretc.replace('-->', '')
                        pretc = pretc.replace('[', '')
                        pretc = pretc.replace(']', '')
                        self.leii1.setText(pretc)

                        if self.leii1.text() != '':
                            self.textii2.setPlainText(contend)
                            self.btn_a.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #0085FF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #FFFFFF''')
                            self.btn_a.setText('Created')
                            self.leii1.setEnabled(False)
                            with open('path_ste.txt', 'w', encoding='utf-8') as f0:
                                f0.write(self.leii1.text())
                        if self.leii1.text() == '':
                            self.textii2.setPlainText('Not a standard file produced by Strawberry. \nCan not find title within.')
                    if '.tex' in file_name:
                        patterna = re.compile(r'title\{.*}')
                        resultq = patterna.findall(contend)
                        resultq = ''.join(resultq)
                        resultq = resultq.replace('title{', '')
                        resultq = resultq.replace('}', '')
                        resultq = resultq.replace('[', '')
                        resultq = resultq.replace(']', '')
                        self.leii1.setText(resultq)

                        if self.leii1.text() != '':
                            self.textii3.setPlainText(contend)
                            self.btn_a.setStyleSheet('''
                                            border: 1px outset grey;
                                            background-color: #0085FF;
                                            border-radius: 4px;
                                            padding: 1px;
                                            color: #FFFFFF''')
                            self.btn_a.setText('Created')
                            self.leii1.setEnabled(False)
                            with open('path_std.txt', 'w', encoding='utf-8') as f0:
                                f0.write(self.leii1.text())
                        if self.leii1.text() == '':
                            self.textii3.setPlainText('Not a standard file produced by Strawberry. \nCan not find title within.')
                    if self.leii1.text() != '':
                        self.choosepart.clear()
                        self.choosepart.addItems(['Append at the end (default)'])
                        pathscr = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
                        tarname1 = str(self.leii1.text()) + ".md"
                        fulldir1 = os.path.join(pathscr, tarname1)
                        maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                        pattern = re.compile(r'## (.*?)\n')
                        result = pattern.findall(maintxt)
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
            path3 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarname4 = str(self.leii1.text()) + ".md"
                fulldir4 = os.path.join(path3, tarname4)
                parta = '<document-start>'
                partb = '\n<!--Title: ' + str(self.leii1.text()) + '-->'
                partc = '\n\n# ' + str(self.leii1.text())
                with open(fulldir4, 'a', encoding='utf-8') as f3:
                    f3.write(parta + partb + partc)
                self.btn_a.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #0085FF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #FFFFFF''')
                self.btn_a.setText('Created')
                self.leii1.setEnabled(False)
                with open('path_ste.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.leii1.text())

            with open('path_ref.txt', 'w', encoding='utf-8') as citpat:
                citpat.write('')

            pathend = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.leii1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.textii2.setPlainText(contend)
                self.textii2.ensureCursorVisible()  # 游标可用
                cursor = self.textii2.textCursor()  # 设置游标
                pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.textii2.setTextCursor(cursor)  # 滚动到游标位置

    def addinssc(self):
        poslast = 0
        path3 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if path3 == '':
            self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname4 = 'blank'
            if self.leii1.text() != '':
                tarname4 = str(self.leii1.text()) + ".md"
            if self.leii1.text() == '' and self.textii1.toPlainText() != '':
                ISOTIMEFORMAT = '%Y%m%d %H-%M-%S-%f record'
                theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                tarname4 = str(theTime) + ".md"
                self.leii1.setText(str(theTime))
                self.leii1.setEnabled(False)
                self.btn_a.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')
                self.btn_a.setText('Created')
            if self.leii1.text() != '':
                fulldir4 = os.path.join(path3, tarname4)
                with open(fulldir4, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                a = re.sub(r"\n\n\n\n## References[\s\S]*", '', contm)
                for i in range(10):
                    a = a.replace('\r', '☆')
                    a = a.replace('\n', '☆')
                    a = a.replace('☆☆☆☆', '☆☆')
                    a = a.replace('☆☆☆', '☆☆')
                    # a = a.replace('☆☆', '☆☆')
                a = a.replace('☆', '\n')
                partnotes = ''
                if self.leiinote.text() != '':
                    partnotes = ' [' +self.leiinote.text() + ']'
                partat = '<document-start>'
                partbt = '\n<!--Title: ' + str(self.leii1.text()) + '-->'
                partct = '\n\n# ' + str(self.leii1.text())
                parta = ''
                if self.textii1.toPlainText() != '':
                    if contm != '':
                        parta = '\n\n' + str(self.default_clean(self.textii1.toPlainText())) + partnotes
                    if contm == '':
                        parta = partat + partbt + partct + '\n\n' + str(self.default_clean(self.textii1.toPlainText())) + partnotes
                if self.textii1.toPlainText() == '':
                    parta = ''
                partb = '\n\n\n\n' + '## References '
                partc = ''
                tcy = codecs.open('path_ref.txt', 'r', encoding='utf-8').readlines()
                i = 0
                while i >= 0 and i <= len(tcy) - 1:
                    tcy[i] = tcy[i] + '<e>'
                    tcy[i] = ''.join(tcy[i])
                    tcy[i] = tcy[i].replace('\n', '')
                    i = i + 1
                    continue
                tcq = ''.join(tcy)
                tcq = tcq.replace('\n', '')
                tcq = tcq.replace('<e>', '<e>\n')
                tcq = tcq.rstrip('\n')
                qiam = codecs.open('path_ref.txt', 'r', encoding='utf-8').read()
                if qiam != '':
                    partc = '\n\n' + tcq
                if qiam == '':
                    partc = '\n' + tcq
                partd = '\n\n<document-end>'

                get_ori = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                get_rst = codecs.open('path_pat.txt', 'r', encoding='utf-8').read()
                get_ori = get_ori.replace(get_rst, '')
                get_ori = get_ori.rstrip('\n')
                part_z = get_ori
                part_n = '\n\n' + get_rst

                last = int(self.choosepart.count() - 1)
                if self.choosepart.currentIndex() == 0 or self.choosepart.currentIndex() == last:
                    poslast = len(partb + partc + partd)
                    with open(fulldir4, 'w', encoding='utf-8') as f3:
                        f3.write(a + parta + partb + partc + partd)
                if self.choosepart.currentIndex() != 0 and self.choosepart.currentIndex() != last:
                    with open(fulldir4, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + parta + part_n)

                itemold = self.choosepart.currentText()
                self.choosepart.clear()
                self.choosepart.addItems(['Append at the end (default)'])
                pathscr = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
                tarname1 = str(self.leii1.text()) + ".md"
                fulldir1 = os.path.join(pathscr, tarname1)
                maintxt = codecs.open(fulldir1, 'r', encoding='utf-8').read()
                pattern = re.compile(r'## (.*?)\n')
                result = pattern.findall(maintxt)
                result = '☆'.join(result)
                if result != '':
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
                    if itemold in result:
                        itemnub = result.index(itemold) + 1
                        self.choosepart.setCurrentIndex(itemnub)
                    if itemold not in result:
                        self.choosepart.setCurrentIndex(0)

                pathend = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
                if pathend == '':
                    self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
                else:
                    tarnameend = str(self.leii1.text()) + ".md"
                    fulldirend = os.path.join(pathend, tarnameend)
                    contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                    posnu = codecs.open('path_pat.txt', 'r', encoding='utf-8').read()
                    self.textii2.setPlainText(contend)
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

    def addcit(self):
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
                contend = codecs.open(file_name, 'r', encoding='utf-8').read()
                pattern6 = re.compile(r'Citation: (.*?)\n')
                result6 = pattern6.findall(contend)
                result6 = ''.join(result6)
                pretc6 = result6.replace('Citation: ', '')
                pretc6 = pretc6.replace('\n', '')
                pretc6 = pretc6.replace('[[', '')
                pretc6 = pretc6.replace(']]', '')
                oldref = codecs.open('path_ref.txt', 'r', encoding='utf-8').read()
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
                if self.leii2.text() != '':
                    if pretc6 != '':
                        partt1 = '\n[^' + str(self.leii2.text()) + ']: ' + pretc6
                        with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                            citpat.write(partt1)
                    if pretc6 == '':
                        partt1 = '\n[^' + str(self.leii2.text()) + ']: ' + 'Cannot find citation for ' + file_name
                        with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                            citpat.write(partt1)
                if self.leii2.text() == '':
                    # tarnumb = '1'
                    if pretc7 == '0':
                        tarnumb = '1'
                        if pretc6 != '':
                            partt1 = '[^' + str(tarnumb) + ']: ' + pretc6
                            with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                                citpat.write(partt1)
                        if pretc6 == '':
                            partt1 = '[^' + str(tarnumb) + ']: ' + 'Cannot find citation for ' + file_name
                            with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                                citpat.write(partt1)
                    if pretc7 != '0':
                        tarnumb = str(int(pretc7) + 1)
                        if pretc6 != '':
                            partt1 = '\n[^' + str(tarnumb) + ']: ' + pretc6
                            with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                                citpat.write(partt1)
                        if pretc6 == '':
                            partt1 = '\n[^' + str(tarnumb) + ']: ' + 'Cannot find citation for ' + file_name
                            with open('path_ref.txt', 'a', encoding='utf-8') as citpat:
                                citpat.write(partt1)

            path3 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if path3 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            if path3 != '' and file_name != '' and (path1 in file_name or fulldira in file_name):
                tarname4 = str(self.leii1.text()) + ".md"
                fulldir4 = os.path.join(path3, tarname4)
                with open(fulldir4, 'a', encoding='utf-8') as f0:
                    f0.write('')
                contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
                a = re.sub(r"\[.*<e>\n", '', contm)
                a = re.sub(r"\n\n\n\n", '', a)
                a = re.sub(r"## References \n\n", '', a)
                a = re.sub(r"\n<document-end>", '', a)
                for i in range(10):
                    a = a.replace('\r', '☆')
                    a = a.replace('\n', '☆')
                    a = a.replace('☆☆☆☆', '☆☆')
                    a = a.replace('☆☆☆', '☆☆')
                a = a.replace('☆', '\n')
                partb = '\n\n\n\n' + '## References '
                tcy = codecs.open('path_ref.txt', 'r', encoding='utf-8').readlines()
                i = 0
                while i >= 0 and i <= len(tcy) - 1:
                    tcy[i] = tcy[i] + '<e>'
                    tcy[i] = ''.join(tcy[i])
                    tcy[i] = tcy[i].replace('\n', '')
                    i = i + 1
                    continue
                tcq = ''.join(tcy)
                tcq = tcq.replace('\n', '')
                tcq = tcq.replace('<e>', '<e>\n')
                tcq = tcq.rstrip('\n')
                partc = '\n\n' + tcq
                partd = '\n\n<document-end>'
                if self.leii1.text() != '':
                    with open(fulldir4, 'w', encoding='utf-8') as f3:
                        f3.write(a + partb + partc + partd)

            pathend = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if pathend == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                tarnameend = str(self.leii1.text()) + ".md"
                fulldirend = os.path.join(pathend, tarnameend)
                contend = codecs.open(fulldirend, 'r', encoding='utf-8').read()
                self.textii2.setPlainText(contend)
                self.textii2.ensureCursorVisible()  # 游标可用
                cursor = self.textii2.textCursor()  # 设置游标
                pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                cursor.setPosition(pos)  # 游标位置设置为尾部
                self.textii2.setTextCursor(cursor)  # 滚动到游标位置

            self.leii2.clear()

    def clinp(self):
        self.textii1.clear()
        self.textii2.clear()
        self.textii3.clear()
        self.leii1.clear()
        with open('path_ref.txt', 'w', encoding='utf-8') as citpat:
            citpat.write('')
        with open('path_lat.txt', 'w', encoding='utf-8') as reflat:
            reflat.write('')
        self.btn_a.setStyleSheet('''
                border: 1px outset grey;
                background-color: #FFFFFF;
                border-radius: 4px;
                padding: 1px;
                color: #000000''')
        self.btn_a.setText('Create')
        self.leii1.setEnabled(True)
        with open('path_ste.txt', 'w', encoding='utf-8') as r0:
            r0.write('')
        with open('path_std.txt', 'w', encoding='utf-8') as r1:
            r1.write('')
        self.widgettem.setCurrentIndex(0)
        self.choosepart.clear()
        self.choosepart.addItems(['Append at the end (default)'])
        with open('path_pat.txt', 'w', encoding='utf-8') as r1:
            r1.write('')
        self.leiinote.clear()

    def save1(self):
        oldv = self.text.verticalScrollBar().value()
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
            oldnam = codecs.open('path_ttl.txt', 'r', encoding='utf-8').read()
            if oldnam != pretc:
                self.le1.setText(pretc)
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text.toPlainText()
            if self.le1.text() != '' and self.text.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
        self.widget0.addItems(['Append at the end (default)'])
        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
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
                    itemnub = result.index(itemold) + 1
                    self.widget0.setCurrentIndex(itemnub)
                if itemold not in result:
                    self.widget0.setCurrentIndex(0)

    def save2(self):
        path1 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s2.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lec1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s2.toPlainText()
            if self.lec1.text() != '' and self.text_s2.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
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
            path1 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.textii2.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                pattern = re.compile(r'<!--Title: (.*?)-->')
                result = pattern.findall(self.textii2.toPlainText())
                result = ''.join(result)
                okio = result.replace('<!--Title: ', '')
                okio = okio.replace('-->', '')
                okio = okio.replace('[', '')
                okio = okio.replace(']', '')
                oldnam = codecs.open('path_ste.txt', 'r', encoding='utf-8').read()
                if oldnam != okio:
                    self.leii1.setText(okio)
                with open('path_std.txt', 'w', encoding='utf-8') as f0:
                    f0.write(self.leii1.text())
                tarname1 = str(self.leii1.text()) + ".md"
                fulldir1 = os.path.join(path1, tarname1)
                saved = self.textii2.toPlainText()
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

                part_b = '\n\n' + '''\\title{''' + prettle + '}'
                if self.widgettem.currentIndex() == 4:
                    part_b = '\n\n' + '\\title{' + prettle + '*\\thanks{Special thanks to funding agency here. If none, delete this.}}'
                if self.widgettem.currentIndex() == 5:
                    part_b = '\n\n' + '\\SEC{\\songti  ' + prettle + '}'
                if self.widgettem.currentIndex() == 6:
                    part_b = '\n\n' + '\\title{' + prettle + '}'
                if self.widgettem.currentIndex() == 7:
                    part_b = '\n\n' + '\\title{\\textbf{' + prettle + '}}'

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