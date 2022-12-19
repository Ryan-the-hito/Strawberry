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

                savelatex = re.sub(r"<document-start>", '', oldtext)
                savelatex = re.sub(r"\n<document-end>", '', savelatex)
                savelatex = re.sub(r"<!--Title: .*-->\n\n", '', savelatex)
                savelatex = re.sub(r"# " + prettle + '\n\n', '', savelatex)
                savelatex = re.sub(r"\[.*<e>\n", '', savelatex)
                savelatex = re.sub(r"\n\n\n\n", '', savelatex)
                savelatex = re.sub(r"## References \n\n", '', savelatex)
                pattern2 = re.compile(r'\[.[0-9]+]')
                result = pattern2.findall(savelatex)
                result.sort()
                cajref = codecs.open('path_ref.txt', 'r', encoding='utf-8').read()
                cajref = cajref.replace('[[', '')
                cajref = cajref.replace(']]', '')
                cajref = cajref.split('\n')
                i = 0
                n = 0
                while i >= 0 and i <= len(result) - 1 and n >= 0 and n <= len(cajref) - 1:
                    #while n >= 0 and n <= len(cajref) - 1:
                    if result[i] in cajref[n]:
                        stripednum = result[i].replace('[^', '')
                        stripednum = stripednum.replace(']', '')
                        stripedref = re.sub(r"\[.*]: ", '', cajref[n])
                        stripedref = re.sub(r"<e>", '', stripedref)
                        savelatex = re.sub(r"\[." + stripednum + "]", "\\footnote{" + stripedref + '}', savelatex)
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
                    savelatex = re.sub("\n\d\..", r'\\item ', savelatex)

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

                preref = codecs.open('path_ref.txt', 'r', encoding='utf-8').read()
                preref = preref.replace('[[', '')
                preref = preref.replace(']]', '')
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
                    with open('path_lat.txt', 'w', encoding='utf-8') as flat:
                        flat.write(reflat)
                if preref == '':
                    with open('path_lat.txt', 'w', encoding='utf-8') as flat:
                        flat.write('')
                biblat = codecs.open('path_lat.txt', 'r', encoding='utf-8').read()
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

                tarname10 = str(self.leii1.text()) + ".tex"
                fulldir10 = os.path.join(path1, tarname10)
                lattex = part_a + part_b + part_c + part_d + part_e + part_f + part_g
                with open(fulldir10, 'a', encoding='utf-8') as f0:
                    f0.write('')
                with open(fulldir10, 'w', encoding='utf-8') as f1:
                    f1.write(lattex)

            contendc = self.textii2.toPlainText()
            patterna = re.compile(r'\[.*<e>\n')
            resultp = patterna.findall(contendc)
            resultp = ''.join(resultp)
            resultp = resultp.rstrip('\n')
            resultp = resultp.replace('<e>', '')
            resultp = resultp.replace('<e>\n<e>', '')
            resultp = resultp.replace('<e><e>', '')
            with open('path_ref.txt', 'w', encoding='utf-8') as fp:
                fp.write(resultp)

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

            pathend2 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
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

    def savelat(self):
        if self.leii1.text() != '' and self.textii3.toPlainText() != '':
            path1 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if path1 == '':
                self.textii3.setPlainText('Some directory is empty. Please go to preferences and check!')
            else:
                patterna = re.compile(r'title\{.*}')
                resultq = patterna.findall(self.textii3.toPlainText())
                resultq = ''.join(resultq)
                resultq = resultq.replace('title{', '')
                resultq = resultq.replace('}', '')
                oldnam = codecs.open('path_std.txt', 'r', encoding='utf-8').read()
                if oldnam != resultq:
                    self.leii1.setText(resultq)
                tarname1 = str(self.leii1.text()) + ".tex"
                fulldir1 = os.path.join(path1, tarname1)
                saved = self.textii3.toPlainText()
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

            pathend2 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s3.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lec0.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s3.toPlainText()
            if self.lec0.text() != '' and self.text_s3.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
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
        path1 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
        if path1 == '':
            self.text_s4.setPlainText('Some directory is empty. Please go to preferences and check!')
        else:
            tarname1 = str(self.lem1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s4.toPlainText()
            if self.lem1.text() != '' and self.text_s4.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

        pathend = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
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
            self.mainii2.setVisible(False)
            self.main2.setVisible(False)
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
            action5.setChecked(False)
            btna2.setChecked(False)

    def focuson2(self):
        if btna2.isChecked():
            action10.setChecked(False)
            action10.setVisible(False)
            self.mainii2.setVisible(False)
            self.main2.setVisible(False)
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
            self.btn_insia.setVisible(True)
        else:
            action10.setVisible(True)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            self.btn_insia.setVisible(False)

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
            self.btn_insia.setVisible(True)
        else:
            action10.setVisible(True)
            self.description_box.setVisible(True)
            self.t2.setVisible(True)
            action6.setChecked(False)
            btna3.setChecked(False)
            self.btn_insia.setVisible(False)

    def realon(self):
        MOST_WEIGHT = int(self.screen().availableGeometry().width() * 0.75)
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())

        if action7.isChecked():
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            md2 = self.textii2.toPlainText()
            newhtml2 = self.md2html(md2)
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
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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
            md2 = self.textii2.toPlainText()
            newhtml2 = self.md2html(md2)
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
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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
        with open('win_width.txt', 'w', encoding='utf-8') as f0:
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

    def rest_siz(self):
        HALF_WEIGHT = int(self.screen().availableGeometry().width() / 2)
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())

        self.resize(HALF_WEIGHT, DE_HEIGHT)
        with open('win_width.txt', 'w', encoding='utf-8') as f0:
            f0.write(str(self.width()))
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

    def stop_dock_icon(self, app_name: str, status: bool = True):
        PLIST_PATH_TEM = "/Applications/{0}.app/Contents/Info.plist"
        info_plist = PLIST_PATH_TEM.format(app_name)
        if os.path.exists(info_plist):
            with open(info_plist, "rb") as fp:
                pl = plistlib.load(fp)
                if status:
                    pl["LSUIElement"] = "1"
                else:
                    pl.pop("LSUIElement", '')
            with open(info_plist, "wb") as fp:
                plistlib.dump(pl, fp)
                #print(f"{app_name} icon is {'hidden' if status else 'shows'} successfully, Please restart it.")
        else:
            output = f"Please make sure the app_name is correct, {app_name} is not in /Applications."
            print("\033[1;31;40m" + output + "\033[0m")

    def hide_dock_choice(self):
        if action9.isChecked():
            fire.Fire(self.stop_dock_icon('Strawberry', True))
            with open('dock_state.txt', 'w', encoding='utf-8') as f1:
                f1.write('1')
        else:
            fire.Fire(self.stop_dock_icon('Strawberry', False))
            with open('dock_state.txt', 'w', encoding='utf-8') as f1:
                f1.write('0')

    def compact_mode_on(self):
        QUARTER_WEIGHT = int(self.screen().availableGeometry().width() * 0.3)
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

            self.main2.addTab(self.upper1, 'Info')
            QObjectCleanupHandler().add(self.page2_box_h)
            QObjectCleanupHandler().add(self.wings_h_box)
            self.newbox = QVBoxLayout()
            self.newbox.addWidget(self.main2)
            self.newbox.addWidget(self.widget0)
            self.newbox.addWidget(self.tabs)
            self.art_tab.setLayout(self.newbox)

            QObjectCleanupHandler().add(self.page1_v_box)
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

            QObjectCleanupHandler().add(self.page3_v_box)
            self.page3_new = QVBoxLayout()
            self.page3_new.addWidget(self.mainii2)
            self.page3_new.addWidget(self.t2)
            self.insp_tab.setLayout(self.page3_new)

            self.resize(QUARTER_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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

            self.upper1.deleteLater()
            QObjectCleanupHandler().add(self.newbox)
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
            self.wings_h_box.addWidget(self.tabs)
            self.description_box.setLayout(self.wings_h_box)
            self.page2_box_h = QHBoxLayout()
            self.page2_box_h.addWidget(self.description_box, 1)
            self.page2_box_h.addWidget(self.main2, 1)
            self.page2_box_h.addWidget(self.main3, 1)
            self.art_tab.setLayout(self.page2_box_h)

            QObjectCleanupHandler().add(self.page1_new)
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

            QObjectCleanupHandler().add(self.page3_new)
            self.page3_v_box = QHBoxLayout()
            self.page3_v_box.addWidget(self.t2, 1)
            self.page3_v_box.addWidget(self.mainii2, 1)
            self.page3_v_box.addWidget(self.mainii3, 1)
            self.insp_tab.setLayout(self.page3_v_box)

            self.resize(HALF_WEIGHT, DE_HEIGHT)
            self.tab_bar.setVisible(True)
            with open('win_width.txt', 'w', encoding='utf-8') as f0:
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
            self.read_t5.setVisible(True)
            self.lbltool06.setVisible(True)
            self.tool8.setVisible(True)
            self.btnx4.setVisible(True)
            self.btnx4.setText('🔼')
            self.btn_00.setStyleSheet('''
                                                        border: 1px outset grey;
                                                        background-color: #0085FF;
                                                        border-radius: 4px;
                                                        padding: 1px;
                                                        color: #FFFFFF''')

    def addtable(self):
        poslast = 0
        if self.leii3.text() != '' and self.leii4.text() != '':
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
            path3 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            if path3 != '' and self.leii1.text() != '':
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
                parta = a.replace('☆', '\n')

                part0 = '\n'
                part1 = c_part1*colomn_num
                part1 = part1.replace('||', '|')
                part1 = '\n' + part1
                part2 = c_part2*colomn_num
                part2 = part2.replace('||', '|')
                part2 = '\n' + part2

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
                    with open(fulldir4, 'w', encoding='utf-8') as f0:
                        f0.write(parta + part0 + part1 + part2 + part1*row_num + partb + partc +partd)
                if self.choosepart.currentIndex() != 0 and self.choosepart.currentIndex() != last:
                    with open(fulldir4, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part0 + part1 + part2 + part1*row_num + part_n)

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
                    pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                    if posnu != '':
                        pos = len(self.textii2.toPlainText()) - len(posnu)  # 获取文本尾部的位置
                    if posnu == '':
                        pos = len(self.textii2.toPlainText()) - poslast
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.textii2.setTextCursor(cursor)  # 滚动到游标位置

                self.leii3.clear()
                self.leii4.clear()

    def addimage(self):
        poslast = 0
        path3 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
        if path3 != '' and self.leii1.text() != '':
            tarname4 = str(self.leii1.text()) + ".md"
            fulldir4 = os.path.join(path3, tarname4)
            with open(fulldir4, 'a', encoding='utf-8') as f0:
                f0.write('')
            contm = codecs.open(fulldir4, 'r', encoding='utf-8').read()
            file_name, ok = QFileDialog.getOpenFileName(self, "Open File", path3)
            if file_name != '':
                part1 = '\n\n!['
                part2 = 'Image caption]'
                if self.leii5.text() != '':
                    part2 = str(self.leii5.text()) + ']'
                part3 = '(' + str(file_name) + ')'

                a = re.sub(r"\[.*<e>\n", '', contm)
                a = re.sub(r"\n\n\n\n", '', a)
                a = re.sub(r"## References \n\n", '', a)
                a = re.sub(r"\n<document-end>", '', a)
                for i in range(10):
                    a = a.replace('\r', '☆')
                    a = a.replace('\n', '☆')
                    a = a.replace('☆☆☆☆', '☆☆')
                    a = a.replace('☆☆☆', '☆☆')
                parta = a.replace('☆', '\n')
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
                    with open(fulldir4, 'w', encoding='utf-8') as f0:
                        f0.write(parta + part1 + part2 + part3 + partb + partc + partd)
                if self.choosepart.currentIndex() != 0 and self.choosepart.currentIndex() != last:
                    with open(fulldir4, 'w', encoding='utf-8') as f1:
                        f1.write(part_z + part1 + part2 + part3 + part_n)

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
                    pos = len(self.textii2.toPlainText())  # 获取文本尾部的位置
                    if posnu != '':
                        pos = len(self.textii2.toPlainText()) - len(posnu)  # 获取文本尾部的位置
                    if posnu == '':
                        pos = len(self.textii2.toPlainText()) - poslast
                    cursor.setPosition(pos)  # 游标位置设置为尾部
                    self.textii2.setTextCursor(cursor)  # 滚动到游标位置

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
        ret = markdown2.markdown(mdstr, extras=extras)
        return html % ret

    def on_text_textChanged(self):
        if self.text.toPlainText() != '':
            path1 = codecs.open('path_art.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.le1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text.toPlainText()
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)
        if action7.isChecked():
            md = self.text.toPlainText()
            newhtml = self.md2html(md)
            self.real1.setHtml(newhtml)
            if self.text.verticalScrollBar().maximum() != 0:
                proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
                tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
                self.real1.verticalScrollBar().setValue(tar_pro)

    def scr_cha(self):
        if self.text.verticalScrollBar().maximum() != 0 and action7.isChecked():
            proportion = self.text.verticalScrollBar().value() / self.text.verticalScrollBar().maximum()
            tar_pro = int(self.real1.verticalScrollBar().maximum() * proportion)
            self.real1.verticalScrollBar().setValue(tar_pro)

    def on_text2_textChanged(self):
        if self.textii2.toPlainText() != '':
            path1 = codecs.open('path_scr.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.leii1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.textii2.toPlainText()
            with open(fulldir1, 'w', encoding='utf-8') as f1:
                f1.write(saved)
        if action7.isChecked():
            md = self.textii2.toPlainText()
            newhtml = self.md2html(md)
            self.real2.setHtml(newhtml)
            if self.textii2.verticalScrollBar().maximum() != 0:
                proportion = self.textii2.verticalScrollBar().value() / self.textii2.verticalScrollBar().maximum()
                tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
                self.real2.verticalScrollBar().setValue(tar_pro)

    def scr_cha2(self):
        if self.textii2.verticalScrollBar().maximum() != 0 and action7.isChecked():
            proportion = self.textii2.verticalScrollBar().value() / self.textii2.verticalScrollBar().maximum()
            tar_pro = int(self.real2.verticalScrollBar().maximum() * proportion)
            self.real2.verticalScrollBar().setValue(tar_pro)

    def on_text_textChanged_concept(self):
        if self.text_s2.toPlainText() != '':
            path1 = codecs.open('path_con.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lec1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s2.toPlainText()
            if self.lec1.text() != '' and self.text_s2.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

    def on_text_textChanged_theory(self):
        if self.text_s3.toPlainText() != '':
            path1 = codecs.open('path_the.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lec0.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s3.toPlainText()
            if self.lec0.text() != '' and self.text_s3.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

    def on_text_textChanged_method(self):
        if self.text_s4.toPlainText() != '':
            path1 = codecs.open('path_met.txt', 'r', encoding='utf-8').read()
            tarname1 = str(self.lem1.text()) + ".md"
            fulldir1 = os.path.join(path1, tarname1)
            saved = self.text_s4.toPlainText()
            if self.lem1.text() != '' and self.text_s4.toPlainText() != '':
                with open(fulldir1, 'w', encoding='utf-8') as f1:
                    f1.write(saved)

    def card1changed(self):
        if self.carda.toPlainText() != '' and self.cardb.toPlainText() != '':
            deck_path = codecs.open('path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            if '' in ori_lst:
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
            deck_path = codecs.open('path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            if '' in ori_lst:
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
            if self.lew1.text() != '':
                corepart = self.lew1.text() + '\n'
                with open(fulldir2, 'a', encoding='utf-8') as f0:
                    f0.write(corepart)
                contend2 = codecs.open(fulldir2, 'r', encoding='utf-8').read()
                alllist2 = contend2.split('\n')
                alllist2.sort()
                if '' in alllist2:
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
            if '' in alllist2:
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
            with open('path_dec.txt', 'w', encoding='utf-8') as f0:
                f0.write(fulldir3)
            self.lew2.setText(endname.replace('.txt', ''))
            self.lew2.setEnabled(False)

    def opendeck(self):
        home_dir = str(Path.home())
        fj = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Text Files (*.txt)")
        if fj != '':
            str_fj = ''.join(fj)
            str_fj = str_fj.replace('Text Files (*.txt)', '')
            lst_fj = str_fj.split('/')
            if '.txt' in lst_fj[-1]:
                endname = lst_fj[-1].replace('.txt', '')
                self.lew2.setText(endname)
                self.lew2.setEnabled(False)
                with open('path_dec.txt', 'w', encoding='utf-8') as f0:
                    f0.write(str_fj)

    def closedeck(self):
        with open('path_dec.txt', 'w', encoding='utf-8') as f0:
            f0.write('')
        self.lew2.clear()
        self.lew2.setEnabled(True)
        self.carda.clear()
        self.cardb.clear()

    def search_on_web(self):
        searchcon = self.wid_word.currentText()
        fullurl = 'https://www.collinsdictionary.com/dictionary/english/' + str(searchcon.lower())
        webbrowser.open(fullurl)

    def makecard(self):
        if self.textw1.toPlainText() != '' and self.lew2.text() != '' and self.wid_word.currentText() != 'None' and self.wid_word.currentText() != '':
            deck_path = codecs.open('path_dec.txt', 'r', encoding='utf-8').read()
            part1 = str(self.wid_word.currentText().lower())
            part1_5 = '\t'
            tags = str(self.lew3.text()).replace('、', ' #')
            part2 = str(self.textw1.toPlainText().replace('\n', '<br>')) + '<br>#' + tags + '\t'
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
            if '' in alllist2:
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
                if '' in new_lst[i]:
                    new_lst[i].remove('')
                new_lst2.append(new_lst[i])
            new_dict = dict(new_lst2)
            waittopri = str(new_dict.keys())
            waittopri = waittopri.replace('dict_keys([', '')
            waittopri = waittopri.replace('])', '')
            waittopri = waittopri.replace("'", '')
            waittopri = waittopri.replace(', ', '\n')
            self.text_res.setPlainText(waittopri)
            #print(waittopri)

    def newsearch(self):
        self.lew4.clear()
        self.text_res.clear()

    def editcardsave(self):
        if self.carda.toPlainText() != '' and self.cardb.toPlainText() != '':
            deck_path = codecs.open('path_dec.txt', 'r', encoding='utf-8').read()
            ori_cont = codecs.open(deck_path, 'r', encoding='utf-8').read()
            ori_lst = ori_cont.split('\n')
            if '' in ori_lst:
                ori_lst.remove('')
            ori_lst.remove(ori_lst[-1])
            new_cont = '\n'.join(ori_lst) + '\n'
            with open(deck_path, 'w', encoding='utf-8') as f0:
                f0.write(new_cont)
            title = self.carda.toPlainText() + '\t'
            content = self.cardb.toPlainText()
            with open(deck_path, 'a', encoding='utf-8') as f0:
                f0.write(title + content + '\n')

    def pin_a_tab(self):
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        WINDOW_WEIGHT = int(self.width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        if self.pos().x() + WINDOW_WEIGHT + 4 < SCREEN_WEIGHT and self.pos().x() > 4:
            self.btn_00.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        else:
            target_x = 0
            if self.i % 2 == 1:
                win_old_width = codecs.open('win_width.txt', 'r', encoding='utf-8').read()
                if self.pos().x() + WINDOW_WEIGHT >= SCREEN_WEIGHT: # 右侧显示
                    target_x = SCREEN_WEIGHT - int(win_old_width) - 3
                btna4.setChecked(True)
                self.btn_00.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.tab_bar.setVisible(True)
                self.resize(int(win_old_width), DE_HEIGHT)
            if self.i % 2 == 0:
                if self.pos().x() + WINDOW_WEIGHT + 4 >= SCREEN_WEIGHT:  # 右侧隐藏
                    target_x = SCREEN_WEIGHT - 10
                btna4.setChecked(False)
                self.btn_00.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
                self.tab_bar.setVisible(False)
                with open('win_width.txt', 'w', encoding='utf-8') as f0:
                    f0.write(str(self.width()))
                self.resize(self.new_width, DE_HEIGHT)
            self.move_window(target_x, self.pos().y())

    def pin_a_tab2(self):
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        WINDOW_WEIGHT = int(self.width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        if self.pos().x() + WINDOW_WEIGHT + 4 < SCREEN_WEIGHT and self.pos().x() > 4:
            self.btn_00.setStyleSheet('''
                                    border: 1px outset grey;
                                    background-color: #FFFFFF;
                                    border-radius: 4px;
                                    padding: 1px;
                                    color: #000000''')
        else:
            target_x = 0
            if self.i % 2 == 1:
                win_old_width = codecs.open('win_width.txt', 'r', encoding='utf-8').read()
                if self.pos().x() + WINDOW_WEIGHT >= SCREEN_WEIGHT: # 右侧显示
                    target_x = SCREEN_WEIGHT - int(win_old_width) - 3
                btna4.setChecked(True)
                self.btn_00.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #0085FF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #FFFFFF''')
                self.tab_bar.setVisible(True)
                self.resize(int(win_old_width), DE_HEIGHT)
            if self.i % 2 == 0:
                if self.pos().x() + WINDOW_WEIGHT + 4 >= SCREEN_WEIGHT:  # 右侧隐藏
                    target_x = SCREEN_WEIGHT - 10
                btna4.setChecked(False)
                self.btn_00.setStyleSheet('''
                            border: 1px outset grey;
                            background-color: #FFFFFF;
                            border-radius: 4px;
                            padding: 1px;
                            color: #000000''')
                self.tab_bar.setVisible(False)
                with open('win_width.txt', 'w', encoding='utf-8') as f0:
                    f0.write(str(self.width()))
                self.resize(self.new_width, DE_HEIGHT)
            self.move_window(target_x, self.pos().y())

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

    def activate(self):  # 设置窗口显示
        SCREEN_WEIGHT = int(self.screen().availableGeometry().width())
        WINDOW_WEIGHT = int(self.width())
        DE_HEIGHT = int(self.screen().availableGeometry().height())
        win_old_width = codecs.open('win_width.txt', 'r', encoding='utf-8').read()
        self.tab_bar.setVisible(True)
        self.resize(int(win_old_width), DE_HEIGHT)
        self.show()
        if self.pos().x() + WINDOW_WEIGHT >= SCREEN_WEIGHT:
            self.move_window(SCREEN_WEIGHT - int(win_old_width) - 3, self.pos().y())
        btna4.setChecked(True)
        self.btn_00.setStyleSheet('''
                    border: 1px outset grey;
                    background-color: #0085FF;
                    border-radius: 4px;
                    padding: 1px;
                    color: #FFFFFF''')

    def cancel(self):  # 设置取消键的功能
        self.close()