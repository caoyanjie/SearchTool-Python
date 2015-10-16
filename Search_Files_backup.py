__author__ = 'caoyanjie'
# _*_ coding: utf-8 _*_
import re
import platform
from os import (walk, sep, system)
from os.path import (join, splitext, exists)
from PyQt5.QtWidgets import (QApplication, QMessageBox, QFileDialog, QWidget,
                             QLabel, QLineEdit, QRadioButton, QPushButton, QTextBrowser, QButtonGroup, QFrame, QListWidget, QListWidgetItem,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import (Qt, QTimer)
# import threading
from time import sleep


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 700)
        self.__search_mode = {'fuzzy': 'fuzzy_search',
                              'precise': 'precise_search',
                              'reg': 'reg_search'}

        # 创建窗口部件
        self.__lab_title = QLabel('<font color="green" size="6">搜索辅助工具</font>')

        self.__pbn_switch_view = None

        self.__lab_open_tool = QLabel('打开文件方式')
        self.__ln_open_tool = QLineEdit()
        self.__pbn_open_tool = QPushButton('浏览...')
        self.__ln_open_tool.setFixedWidth(150)
        self.__pbn_open_tool.setFixedWidth(50)

        self.__rbn_search_file = QRadioButton('检索文件名')
        self.__rbn_search_content = QRadioButton('检索文件内容')

        self.__rbn_fuzzy = QRadioButton('模糊搜索')
        self.__rbn_precise = QRadioButton('精确搜索')
        self.__rbn_reg = QRadioButton('正则表达式搜索')
        self.__rbn_fuzzy.setChecked(True)

        self.__ln_file_name = QLineEdit()
        self.__ln_file_name.setPlaceholderText('请输入搜索条件或正则表达式......')
        self.__rbn_reg_Iyes = QRadioButton('区分大小写')
        self.__rbn_reg_Ino = QRadioButton('不区分大小写')

        self.__ln_file_path = QLineEdit()
        self.__ln_file_path.setPlaceholderText('请选择或输入路径......')
        self.__pbn_file_path = QPushButton('浏览......')
        self.__pbn_search = QPushButton('检索')
        self.__pbn_file_path.setFixedWidth(70)
        self.__pbn_search.setFixedWidth(120)

        self.__browser = QTextBrowser()
        self.__lab_title.setAlignment(Qt.AlignCenter)

        self.__btn_group_type = QButtonGroup()
        self.__btn_group_type.addButton(self.__rbn_search_file)
        self.__btn_group_type.addButton(self.__rbn_search_content)
        self.__rbn_search_file.setChecked(True)

        self.__btn_group_re_I = QButtonGroup()
        self.__btn_group_re_I.addButton(self.__rbn_reg_Iyes)
        self.__btn_group_re_I.addButton(self.__rbn_reg_Ino)
        self.__rbn_reg_Iyes.setChecked(True)

        self.__line_1 = QFrame()
        self.__line_1.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.__line_2 = QFrame()
        self.__line_2.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.__line_3 = QFrame()
        self.__line_3.setFrameStyle(QFrame.HLine | QFrame.Sunken)

        # 布局
        self.__layout_open_tool = QHBoxLayout()
        self.__layout_open_tool.addWidget(self.__lab_open_tool)
        self.__layout_open_tool.addWidget(self.__ln_open_tool)
        self.__layout_open_tool.addWidget(self.__pbn_open_tool)
        self.__layout_open_tool.setSpacing(2)
        
        self.__layout_title = QHBoxLayout()
        self.__layout_title.addStretch(5)
        self.__layout_title.addWidget(self.__lab_title)
        self.__layout_title.addStretch(1)
        self.__layout_title.addLayout(self.__layout_open_tool)

        self.__layout_search_type = QHBoxLayout()
        self.__layout_search_type.addStretch()
        self.__layout_search_type.addWidget(self.__rbn_search_file)
        self.__layout_search_type.addStretch()
        self.__layout_search_type.addWidget(self.__rbn_search_content)
        self.__layout_search_type.addStretch()

        self.__layout_search_reg_I = QHBoxLayout()
        self.__layout_search_reg_I.addWidget(self.__rbn_reg_Iyes)
        self.__layout_search_reg_I.addWidget(self.__rbn_reg_Ino)

        self.__layout_search_mode = QHBoxLayout()
        self.__layout_search_mode.addWidget(self.__rbn_fuzzy)
        self.__layout_search_mode.addStretch()
        self.__layout_search_mode.addWidget(self.__rbn_precise)
        self.__layout_search_mode.addStretch()
        self.__layout_search_mode.addWidget(self.__rbn_reg)
        self.__layout_search_mode.setContentsMargins(60, 0, 60, 0)

        self.__layout_path = QHBoxLayout()
        self.__layout_path.addWidget(self.__ln_file_path)
        self.__layout_path.addWidget(self.__pbn_file_path)
        self.__layout_path.addWidget(self.__pbn_search)
        self.__layout_path.setSpacing(5)

        self.__layout_pattern = QHBoxLayout()
        self.__layout_pattern.addWidget(self.__ln_file_name)
        self.__layout_pattern.addLayout(self.__layout_search_reg_I)

        self.__layout_top = QVBoxLayout()
        self.__layout_top.addLayout(self.__layout_title)
        self.__layout_top.addWidget(self.__line_1)
        self.__layout_top.addLayout(self.__layout_search_type)
        self.__layout_top.addWidget(self.__line_2)
        self.__layout_top.addLayout(self.__layout_search_mode)
        self.__layout_top.addWidget(self.__line_3)
        self.__layout_top.addLayout(self.__layout_pattern)
        self.__layout_top.addLayout(self.__layout_path)
        self.__layout_top.addWidget(self.__browser)
        self.__layout_top.setSpacing(8)
        self.setLayout(self.__layout_top)

        self.__ln_file_name.setFocus()
        self.__pbn_search.setShortcut(Qt.Key_Return)

        # 关联 信号/槽
        self.__pbn_file_path.clicked.connect(self.choose_path)
        self.__pbn_search.clicked.connect(self.pbn_search_clicked)
        self.__pbn_open_tool.clicked.connect(self.choose_open_tool)

#        timer = QTimer(self)
#        timer.timeout.connect(self.set_open_tool)
#        timer.start(10000)

    def set_open_tool(self):
        if platform.architecture() == ('32bit', 'WindowsPE'):
            possible_dir = ['C:/Program Files/Sublime Text 2', 'C:/Sublime Text 2',
                            'D:/Program Files/Sublime Text 2', 'D:/Sublime Text 2',
                            'E:/Program Files/Sublime Text 2', 'E:/Sublime Text 2',
                            'F:/Program Files/Sublime Text 2', 'F:/Sublime Text 2',
                            'C:/Program Files/Notepad++', 'C:/notepad++',
                            'D:/Program Files/Notepad++', 'D:/notepad++',
                            'E:/Program Files/Notepad++', 'E:/notepad++',
                            'F:/Program Files/Notepad++', 'F:/notepad++',
                            'C:\Windows\System32']
        elif platform.architecture() == ('32bit', 'ELF'):
            possible_dir = ['/usr/bin']
        for rootdir in possible_dir:
            for root, dirs, files in walk(rootdir):
                for file in files:
                    if file == 'sublime_text.exe' or file == 'notepad++.exe' or file == 'notepad.exe':
                        self.__ln_open_tool.setText(join(root, file))
                        return
        
    # 搜索文件名
    def search_from_filename(self, filepath, filename, mode='fuzzy_search', I=True):
        if filepath == '' or not exists(filepath):
            return False
        if mode not in self.__search_mode.values():
            return False
        if filename == '':
            return False

        if mode == self.__search_mode['fuzzy']:
            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if filename in each_file:
                        yield join(root, each_file)
        elif mode == self.__search_mode['precise']:
            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if filename == splitext(each_file)[0] or filename == each_file:
                        yield join(root, each_file)
        elif mode == self.__search_mode['reg']:
            if I:
                pattern = re.compile(r'%s' % filename)
            else:
                pattern = re.compile(r'%s' % filename, re.I)

            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if re.search(pattern, each_file):
                        yield join(root, each_file)
        self.__browser.append('搜索完毕！')

    # 搜索文件内容
    def search_from_content(self, path, content, mode='fuzzy_search', I=True):
        if path == '' or not exists(path):
            return False
        if mode not in self.__search_mode.values():
            return False
        if content == '':
            return False
        pass_file_count = 0
        error_number = 0
        current_file = ''
        processing_file = ''
        if mode == self.__search_mode['reg']:
            if I:
                pattern = re.compile(r'%s' % content)
            else:
                pattern = re.compile(r'%s' % content, re.I)
            for root, dirs, files in walk(path):
                for each_file in [file for file in files if file.endswith('.h') or file.endswith('.cpp') or file.endswith('.cs')]:
                    current_file = join(root, each_file)
                    pass_file_count += 1
                    try:
                        for line_number, line in enumerate(open(current_file)):
                            if re.search(pattern, line):
                                if processing_file != current_file:
                                    yield '\n%s' % (current_file)
                                    processing_file = current_file
                                yield 'line %s: %s' % (line_number, line.strip())
                    except Exception as error:
                        print("%s\n(%s)\n" % (error, current_file))
                        pass_file_count -= 1
                        error_number += 1
                        continue
        else:
            for root, dirs, files in walk(path):
                for each_file in [file for file in files if file.endswith('.h') or file.endswith('.cpp') or file.endswith('.cs')]:
                    current_file = join(root, each_file)
                    pass_file_count += 1
                    try:
                        for line_number, line in enumerate(open(current_file)):
                            if content in line:
                                if processing_file != current_file:
                                    yield '\n%s' % (current_file)
                                    processing_file = current_file
                                yield 'line %s: %s' % (line_number, line.strip())
                    except Exception as error:
                        print("%s\n(%s)\n" % (error, current_file))
                        pass_file_count -= 1
                        error_number += 1
                        continue
        self.__browser.append('\n搜索完毕！\n处理 %s 个文件\n失败 %s 文件' % (pass_file_count, error_number))

    # 单击选择路径按钮
    def choose_path(self):
        path = QFileDialog.getExistingDirectory()
        if path != '':
            path = sep.join(path.split('/'))
            self.__ln_file_path.setText(path)

    #
    def choose_open_tool(self):
        path = QFileDialog.getOpenFileName()
        if path != '':
            self.__ln_open_tool.setText(path[0])

    # 单击检索按钮
    def pbn_search_clicked(self):
        file_path = self.__ln_file_path.text()
        file_name = self.__ln_file_name.text()
        if file_path == '':
            QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入路径', QMessageBox.Ok, self).exec_()
            return
        if file_name == '':
                QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入匹配特征', QMessageBox.Ok, self).exec_()
                return
        mode = self.__search_mode['fuzzy']
        if self.__rbn_reg.isChecked():
            mode = self.__search_mode['reg']
        elif self.__rbn_fuzzy.isChecked():
            mode = self.__search_mode['fuzzy']
        elif self.__rbn_precise.isChecked():
            mode = self.__search_mode['precise']
        I = True
        if self.__rbn_reg_Ino.isChecked():
            I = False
#        new_threading = threading.Thread(target=self.search_from_filename, args=(file_path, file_name, mode, reg))
#        new_threading.start()
#        new_threading.join()
        self.__browser.clear()
        if self.__rbn_search_file.isChecked():
            for result in self.search_from_filename(file_path, file_name, mode, I):
                self.__browser.append(result)
                #self.repaint()
        else:
            for result in self.search_from_content(file_path, file_name, mode, I):
                self.__browser.append(result)
                #self.repaint()
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.set_open_tool()
    sys.exit(app.exec_())
