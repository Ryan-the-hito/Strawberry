class window4(QWidget):  # Customization settings
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):  # 设置窗口内布局
        self.setUpMainWindow()
        self.resize(839, 475)
        self.center()
        self.setWindowTitle('Customization settings')
        self.setFocus()
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def setUpMainWindow(self):
        wid0 = QWidget()
        lbl0 = QLabel("Set your path", self)
        font = PyQt6.QtGui.QFont()
        font.setBold(True)
        lbl0.setFont(font)
        b40 = QHBoxLayout()
        b40.setContentsMargins(10, 10, 10, 10)
        b40.addStretch()
        b40.addWidget(lbl0)
        b40.addStretch()
        wid0.setLayout(b40)

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
        main_h_box.addWidget(wid0)
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
        self.setLayout(main_h_box)

    def center(self):  # 设置窗口居中
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
        if e.key() == Qt.Key.Key_Escape.value:
            self.close()

    def cancel(self):  # 设置取消键的功能
        self.close()

    def activate(self):  # 设置窗口显示
        self.show()
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

        path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.lbl4_11.setText('The directory is empty. Please check!')
            self.lbl4_11.setStyleSheet('color:red')
        else:
            self.lbl4_11.setText(path1)
            self.lbl4_11.setStyleSheet('color:black')

        path2 = codecs.open('path_aut.txt', 'r', encoding='utf-8').read()
        if path2 == '':
            self.lbl4_21.setText('The directory is empty. Please check!')
            self.lbl4_21.setStyleSheet('color:red')
        else:
            self.lbl4_21.setText(path2)
            self.lbl4_21.setStyleSheet('color:black')

        path3 = codecs.open('path_ins.txt', 'r', encoding='utf-8').read()
        if path3 == '':
            self.lbl4_31.setText('The directory is empty. Please check!')
            self.lbl4_31.setStyleSheet('color:red')
        else:
            self.lbl4_31.setText(path3)
            self.lbl4_31.setStyleSheet('color:black')

        path4 = codecs.open('path_pub.txt', 'r', encoding='utf-8').read()
        if path4 == '':
            self.lbl4_41.setText('The directory is empty. Please check!')
            self.lbl4_41.setStyleSheet('color:red')
        else:
            self.lbl4_41.setText(path4)
            self.lbl4_41.setStyleSheet('color:black')

        path5 = codecs.open('path_pro.txt', 'r', encoding='utf-8').read()
        if path5 == '':
            self.lbl4_51.setText('The directory is empty. Please check!')
            self.lbl4_51.setStyleSheet('color:red')
        else:
            self.lbl4_51.setText(path5)
            self.lbl4_51.setStyleSheet('color:black')

        path6 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
        if path6 == '':
            self.lbl4_61.setText('The directory is empty. Please check!')
            self.lbl4_61.setStyleSheet('color:red')
        else:
            self.lbl4_61.setText(path6)
            self.lbl4_61.setStyleSheet('color:black')

        path7 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
        if path7 == '':
            self.lbl4_71.setText('The directory is empty. Please check!')
            self.lbl4_71.setStyleSheet('color:red')
        else:
            self.lbl4_71.setText(path7)
            self.lbl4_71.setStyleSheet('color:black')

        path8 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
        if path8 == '':
            self.lbl4_81.setText('The directory is empty. Please check!')
            self.lbl4_81.setStyleSheet('color:red')
        else:
            self.lbl4_81.setText(path8)
            self.lbl4_81.setStyleSheet('color:black')

        path9 = codecs.open('path_boo.txt', 'r', encoding='utf-8').read()
        if path9 == '':
            self.lbl4_91.setText('The directory is empty. Please check!')
            self.lbl4_91.setStyleSheet('color:red')
        else:
            self.lbl4_91.setText(path9)
            self.lbl4_91.setStyleSheet('color:black')

        path10 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if path10 == '':
            self.lbl4_101.setText('The directory is empty. Please check!')
            self.lbl4_101.setStyleSheet('color:red')
        else:
            self.lbl4_101.setText(path10)
            self.lbl4_101.setStyleSheet('color:black')

    def fullsave(self):
        home_dir = str(Path.home())
        tarname1 = "StrawberryAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname2 = "DoNotDelete.txt"
        fulldir2 = os.path.join(fulldir1, tarname2)
        part1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read() + '\n'
        part2 = codecs.open('path_aut.txt', 'r', encoding='utf-8').read() + '\n'
        part3 = codecs.open('path_ins.txt', 'r', encoding='utf-8').read() + '\n'
        part4 = codecs.open('path_pub.txt', 'r', encoding='utf-8').read() + '\n'
        part5 = codecs.open('path_pro.txt', 'r', encoding='utf-8').read() + '\n'
        part6 = codecs.open('path_con.txt', 'r', encoding='utf-8').read() + '\n'
        part7 = codecs.open('path_the.txt', 'r', encoding='utf-8').read() + '\n'
        part8 = codecs.open('path_met.txt', 'r', encoding='utf-8').read() + '\n'
        part9 = codecs.open('path_boo.txt', 'r', encoding='utf-8').read() + '\n'
        part10 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read() + '\n'
        with open(fulldir2, 'w', encoding='utf-8') as f0:
            f0.write(part1 + part2 + part3 + part4 + part5 + part6 + part7 +
                     part8 + part9 + part10)
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
        with open('path_pro.txt', 'w', encoding='utf-8') as f5:
            f5.write(fulldira)
        tarnameb = 'Concepts'
        fulldirb = os.path.join(fulldir3, tarnameb)
        if not os.path.exists(fulldirb):
            os.makedirs(fulldirb)
        self.lbl4_61.setText(fulldirb)
        self.lbl4_61.setStyleSheet('color:black')
        with open('path_con.txt', 'w', encoding='utf-8') as f6:
            f6.write(fulldirb)
        tarnamec = 'Theories'
        fulldirc = os.path.join(fulldir3, tarnamec)
        if not os.path.exists(fulldirc):
            os.makedirs(fulldirc)
        self.lbl4_71.setText(fulldirc)
        self.lbl4_71.setStyleSheet('color:black')
        with open('path_the.txt', 'w', encoding='utf-8') as f7:
            f7.write(fulldirc)
        tarnamed = 'Methods'
        fulldird = os.path.join(fulldir3, tarnamed)
        if not os.path.exists(fulldird):
            os.makedirs(fulldird)
        self.lbl4_81.setText(fulldird)
        self.lbl4_81.setStyleSheet('color:black')
        with open('path_met.txt', 'w', encoding='utf-8') as f8:
            f8.write(fulldird)
        tarnamee = 'Authors'
        fulldire = os.path.join(fulldir3, tarnamee)
        if not os.path.exists(fulldire):
            os.makedirs(fulldire)
        self.lbl4_21.setText(fulldire)
        self.lbl4_21.setStyleSheet('color:black')
        with open('path_aut.txt', 'w', encoding='utf-8') as f2:
            f2.write(fulldire)
        tarnamef = 'Institutes'
        fulldirf = os.path.join(fulldir3, tarnamef)
        if not os.path.exists(fulldirf):
            os.makedirs(fulldirf)
        self.lbl4_31.setText(fulldirf)
        self.lbl4_31.setStyleSheet('color:black')
        with open('path_ins.txt', 'w', encoding='utf-8') as f3:
            f3.write(fulldirf)
        tarnameg = 'Publications'
        fulldirg = os.path.join(fulldir3, tarnameg)
        if not os.path.exists(fulldirg):
            os.makedirs(fulldirg)
        self.lbl4_41.setText(fulldirg)
        self.lbl4_41.setStyleSheet('color:black')
        with open('path_pub.txt', 'w', encoding='utf-8') as f4:
            f4.write(fulldirg)
        tarnameh = 'Articles'
        fulldirh = os.path.join(fulldir3, tarnameh)
        if not os.path.exists(fulldirh):
            os.makedirs(fulldirh)
        self.lbl4_11.setText(fulldirh)
        self.lbl4_11.setStyleSheet('color:black')
        with open('path_art.txt', 'w', encoding='utf-8') as f1:
            f1.write(fulldirh)
        tarnamei = 'Books'
        fulldiri = os.path.join(fulldir3, tarnamei)
        if not os.path.exists(fulldiri):
            os.makedirs(fulldiri)
        self.lbl4_91.setText(fulldiri)
        self.lbl4_91.setStyleSheet('color:black')
        with open('path_boo.txt', 'w', encoding='utf-8') as f9:
            f9.write(fulldiri)
        tarnamej = 'My Scripts'
        fulldirj = os.path.join(fulldir3, tarnamej)
        if not os.path.exists(fulldirj):
            os.makedirs(fulldirj)
        self.lbl4_101.setText(fulldirj)
        self.lbl4_101.setStyleSheet('color:black')
        with open('path_scr.txt', 'w', encoding='utf-8') as f10:
            f10.write(fulldirj)

    def locatefile1(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_art.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_11.setText('The directory is empty. Please check!')
            self.lbl4_11.setStyleSheet('color:red')
        else:
            self.lbl4_11.setText(path)
            self.lbl4_11.setStyleSheet('color:black')

    def locatefile2(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_aut.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_aut.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_21.setText('The directory is empty. Please check!')
            self.lbl4_21.setStyleSheet('color:red')
        else:
            self.lbl4_21.setText(path)
            self.lbl4_21.setStyleSheet('color:black')

    def locatefile3(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_ins.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_ins.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_31.setText('The directory is empty. Please check!')
            self.lbl4_31.setStyleSheet('color:red')
        else:
            self.lbl4_31.setText(path)
            self.lbl4_31.setStyleSheet('color:black')

    def locatefile4(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_pub.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_pub.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_41.setText('The directory is empty. Please check!')
            self.lbl4_41.setStyleSheet('color:red')
        else:
            self.lbl4_41.setText(path)
            self.lbl4_41.setStyleSheet('color:black')

    def locatefile5(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_pro.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_pro.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_51.setText('The directory is empty. Please check!')
            self.lbl4_51.setStyleSheet('color:red')
        else:
            self.lbl4_51.setText(path)
            self.lbl4_51.setStyleSheet('color:black')

    def locatefile6(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_con.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_61.setText('The directory is empty. Please check!')
            self.lbl4_61.setStyleSheet('color:red')
        else:
            self.lbl4_61.setText(path)
            self.lbl4_61.setStyleSheet('color:black')

    def locatefile7(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_the.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_71.setText('The directory is empty. Please check!')
            self.lbl4_71.setStyleSheet('color:red')
        else:
            self.lbl4_71.setText(path)
            self.lbl4_71.setStyleSheet('color:black')

    def locatefile8(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_met.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_81.setText('The directory is empty. Please check!')
            self.lbl4_81.setStyleSheet('color:red')
        else:
            self.lbl4_81.setText(path)
            self.lbl4_81.setStyleSheet('color:black')

    def locatefile9(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_boo.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_boo.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_91.setText('The directory is empty. Please check!')
            self.lbl4_91.setStyleSheet('color:red')
        else:
            self.lbl4_91.setText(path)
            self.lbl4_91.setStyleSheet('color:black')

    def locatefile10(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getExistingDirectory(self, 'Open', home_dir)
        pathfile = codecs.open('path_scr.txt', 'w', encoding='utf-8')
        pathfile.write(fj)
        pathfile.close()
        path = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if path == '':
            self.lbl4_101.setText('The directory is empty. Please check!')
            self.lbl4_101.setStyleSheet('color:red')
        else:
            self.lbl4_101.setText(path)
            self.lbl4_101.setStyleSheet('color:black')

style_sheet_ori = '''
    QTabWidget::pane {
        border: 1px solid #ECECEC;
        background: #ECECEC;
        border-radius: 9px;
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
'''