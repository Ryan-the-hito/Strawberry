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