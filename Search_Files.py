__author__ = 'caoyanjie'
# _*_ coding: utf-8 _*_
from os import (walk, sep)
import re
from os.path import (join, splitext, exists)
from PyQt5.QtWidgets import (QApplication, QMessageBox, QFileDialog,
                             QWidget, QLabel, QLineEdit, QRadioButton, QPushButton, QTextBrowser, QButtonGroup,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import (Qt)
# import threading


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(800, 700)
        self.__search_mode = {'fuzzy': 'fuzzy_search',
                              'precise': 'precise_search',
                              'reg': 'reg_search'}

        # 创建窗口部件
        self.__lab_title = QLabel('搜索辅助工具')
        self.__ln_file_path = QLineEdit()
        self.__ln_file_name = QLineEdit()
        self.__ln_reg = QLineEdit()
        self.__rbn_search_file = QRadioButton('检索文件名')
        self.__rbn_search_content = QRadioButton('检索文件内容')
        self.__rbn_fuzzy = QRadioButton('模糊搜索')
        self.__rbn_precise = QRadioButton('精确搜索')
        self.__rbn_reg = QRadioButton('正则表达式搜索')
        self.__rbn_reg_Iyes = QRadioButton('区分大小写')
        self.__rbn_reg_Ino = QRadioButton('不区分大小写')
        self.__pbn_file_path = QPushButton('浏览...')
        self.__pbn_search = QPushButton('检索')
        self.__browser = QTextBrowser()
        self.__lab_title.setAlignment(Qt.AlignCenter)
        self.__ln_file_path.setPlaceholderText('请选择或输入路径......')
        self.__ln_file_name.setPlaceholderText('请输入搜索条件......')
        self.__ln_reg.setPlaceholderText('请输入要匹配的正则表达式......')
        self.__btn_group_type = QButtonGroup()
        self.__btn_goup_re_I = QButtonGroup()
        self.__btn_group_type.addButton(self.__rbn_search_file)
        self.__btn_group_type.addButton(self.__rbn_search_content)
        self.__btn_goup_re_I.addButton(self.__rbn_reg_Iyes)
        self.__btn_goup_re_I.addButton(self.__rbn_reg_Ino)
        self.__rbn_search_file.setChecked(True)
        self.__rbn_fuzzy.setChecked(True)
        self.__rbn_reg_Iyes.setChecked(True)
        self.__ln_file_name.setFocus()

        # 布局
        self.__layout_title = QHBoxLayout()
        self.__layout_title.addWidget(self.__lab_title)

        self.__layout_search_type = QHBoxLayout()
        self.__layout_search_type.addStretch()
        self.__layout_search_type.addWidget(self.__rbn_search_file)
        self.__layout_search_type.addStretch()
        self.__layout_search_type.addWidget(self.__rbn_search_content)
        self.__layout_search_type.addStretch()

        self.__layout_search_reg = QHBoxLayout()
        self.__layout_search_reg.addWidget(self.__rbn_reg)
        self.__layout_search_reg.addWidget(self.__ln_reg)
        self.__layout_search_reg.addWidget(self.__rbn_reg_Iyes)
        self.__layout_search_reg.addWidget(self.__rbn_reg_Ino)
        self.__layout_search_reg.setSpacing(5)

        self.__layout_search_mode = QHBoxLayout()
        self.__layout_search_mode.addWidget(self.__rbn_fuzzy)
        self.__layout_search_mode.addWidget(self.__rbn_precise)
        self.__layout_search_mode.addLayout(self.__layout_search_reg)
        self.__layout_search_mode.setSpacing(30)

        self.__layout_path = QHBoxLayout()
        self.__layout_path.addWidget(self.__ln_file_path)
        self.__layout_path.addWidget(self.__pbn_file_path)

        self.__layout_pattern = QHBoxLayout()
        self.__layout_pattern.addWidget(self.__ln_file_name)
        self.__layout_pattern.addWidget(self.__pbn_search)

        self.__layout_top = QVBoxLayout()
        self.__layout_top.addLayout(self.__layout_title)
        self.__layout_top.addLayout(self.__layout_search_type)
        self.__layout_top.addLayout(self.__layout_search_mode)
        self.__layout_top.addLayout(self.__layout_path)
        self.__layout_top.addLayout(self.__layout_pattern)
        self.__layout_top.addWidget(self.__browser)
        self.__layout_top.setSpacing(20)
        self.setLayout(self.__layout_top)

        # 关联 信号/槽
        self.__pbn_file_path.clicked.connect(self.choose_path)
        self.__pbn_search.clicked.connect(self.pbn_search_clicked)

    # 搜索
    def search_from_filename(self, filepath, filename, mode='fuzzy_search', reg=r'', I=True):
        if filepath == '' or not exists(filepath):
            return False
        if mode not in self.__search_mode.values():
            return False
        if mode == self.__search_mode['reg']:
            if reg == '':
                return False
        elif filename == '':
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
            if reg == r'':
                return False
            if I:
                pattern = re.compile(reg)
            else:
                pattern = re.compile(reg, re.I)

            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if re.search(pattern, each_file):
                        yield join(root, each_file)
        self.__browser.append('搜索完毕！')

    # 单击选择路径按钮
    def choose_path(self):
        path = QFileDialog.getExistingDirectory()
        if path != '':
            path = sep.join(path.split('/'))
            self.__ln_file_path.setText(path)

    # 单击检索按钮
    def pbn_search_clicked(self):
        file_path = self.__ln_file_path.text()
        file_name = self.__ln_file_name.text()
        if file_path == '':
            QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入路径', QMessageBox.Ok, self).exec_()
            return
        mode = self.__search_mode['fuzzy']
        reg = r''
        if self.__rbn_reg.isChecked():
            mode = self.__search_mode['reg']
            reg = r'%s' % self.__ln_reg.text()
            if reg == '':
                QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入正则表达式', QMessageBox.Ok, self).exec_()
        else:
            if file_name == '':
                QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入匹配特征', QMessageBox.Ok, self).exec_()
                return
            if self.__rbn_fuzzy.isChecked():
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
        for result in self.search_from_filename(file_path, file_name, mode, reg, I):
            self.__browser.append(result)
            self.repaint()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
