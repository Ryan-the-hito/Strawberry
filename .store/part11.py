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