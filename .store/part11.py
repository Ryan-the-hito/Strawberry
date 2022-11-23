w1 = window_about()  # about
w2 = window_update()  # update
w3 = window3()  # main1
w3.setAutoFillBackground(True)
p = w3.palette()
p.setColor(w3.backgroundRole(), QColor('#ECECEC'))
w3.setPalette(p)
w4 = window4()  # main2
action1.triggered.connect(w1.activate)
action2.triggered.connect(w2.activate)
action3.triggered.connect(w3.activate)
action4.triggered.connect(w4.activate)
action5.triggered.connect(w3.focuson)
action6.triggered.connect(w3.editoron)
action7.triggered.connect(w3.realon)
action8.triggered.connect(w3.rest_siz)
action9.triggered.connect(w3.hide_dock_choice)
action10.triggered.connect(w3.compact_mode_on)
# tray.activated.connect(w3.activate)
button_action.triggered.connect(w3.activate)
btna2.triggered.connect(w3.focuson2)
btna3.triggered.connect(w3.editoron2)
btna4.triggered.connect(w3.pin_a_tab2)
app.setStyleSheet(style_sheet_ori)
app.exec()
