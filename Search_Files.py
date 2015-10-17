# _*_ coding: utf-8 _*_import re
import re
import platform
from os import (walk, sep, system)
from os.path import (join, splitext, exists)
from PyQt5.QtWidgets import (QApplication, QMessageBox, QFileDialog, QWidget,
                             QLabel, QLineEdit, QRadioButton, QToolButton, QPushButton, QTextBrowser,
			     QButtonGroup, QFrame, QListWidget, QListWidgetItem, QListWidget, QListWidgetItem, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout)

from PyQt5.QtCore import (Qt, QTimer)
from threading import Thread
from queue import Queue
from time import sleep


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
#        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
#        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(900, 700)
        self.__search_mode = {'fuzzy':   'fuzzy_search',
                              'precise': 'precise_search',
                              'reg':     'reg_search'}
        # self.__pbn_switch_view = None

        # 创建窗口部件
        self.__widget_frame = QLabel()

        # window title
        self.__lab_title_fram = QLabel()
        self.__lab_title = QLabel('搜索辅助工具')
        self.__lab_title.setAlignment(Qt.AlignCenter)

        self.__lab_open_tool = QLabel('打开文件方式')
        self.__ln_open_tool = QLineEdit()
        self.__pbn_open_tool = QToolButton()
        self.__pbn_open_tool.setText('选择...')
        self.__ln_open_tool.setFixedHeight(20)
        self.__ln_open_tool.setFixedWidth(150)
        self.__pbn_open_tool.setFixedSize(48, 20)
        self.__lab_title_fram.setFixedHeight(50)

        # search mode
        self.__lab_mode_fram = QLabel()
        self.__rbn_fuzzy = QRadioButton('模糊搜索')
        self.__rbn_precise = QRadioButton('精确搜索')
        self.__rbn_reg = QRadioButton('正则表达式搜索')
        self.__rbn_fuzzy.setChecked(True)
        self.__lab_mode_fram.setFixedHeight(22)

        # search pattern
        self.__lab_pattern_fram = QLabel()
        self.__ln_file_name = QLineEdit()
        self.__ln_file_name.setPlaceholderText('请输入搜索条件或正则表达式......')
        self.__rbn_reg_Iyes = QRadioButton('区分大小写')
        self.__rbn_reg_Ino = QRadioButton('不区分大小写')
        self.__lab_pattern_fram.setFixedHeight(20)

        # search path
        self.__lab_path_fram = QLabel()
        self.__ln_file_path = QLineEdit()
        self.__ln_file_path.setPlaceholderText('请选择或输入路径......')
        self.__pbn_file_path = QToolButton()
        self.__pbn_file_path.setText('浏览...')
        self.__rbn_search_file = QRadioButton('检索文件名')
        self.__rbn_search_content = QRadioButton('检索文件内容')
        self.__pbn_file_path.setFixedSize(48, 20)
        self.__lab_path_fram.setFixedHeight(20)

        # search state
        self.__lab_state_fram = QLabel()
        self.__lab_state = QLabel('状态：暂无搜索结果！')
        self.__pbn_search = QPushButton('开始')
        self.__pbn_stop = QPushButton('停止')
        self.__pbn_search.setFixedWidth(89)
        self.__pbn_stop.setFixedWidth(89)
        self.__lab_state_fram.setFixedHeight(35)

        # search result
        self.__tabView = QTabWidget()
        self.__browser_result = QListWidget()
        self.__browser_error = QTextBrowser()
        self.__tabView.addTab(self.__browser_result, '匹配结果')
        self.__tabView.addTab(self.__browser_error, '错误结果')

        self.__btn_group_type = QButtonGroup()
        self.__btn_group_type.addButton(self.__rbn_search_file)
        self.__btn_group_type.addButton(self.__rbn_search_content)
        self.__rbn_search_file.setChecked(True)

        # radiobutton group
        self.__btn_group_re_I = QButtonGroup()
        self.__btn_group_re_I.addButton(self.__rbn_reg_Iyes)
        self.__btn_group_re_I.addButton(self.__rbn_reg_Ino)
        self.__rbn_reg_Iyes.setChecked(True)

        # lines
        '''
        self.__line_1 = QFrame()
        self.__line_1.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        '''

        # 布局
        # open tool
        self.__layout_tool_choose = QHBoxLayout()
        self.__layout_tool_choose.addWidget(self.__ln_open_tool)
        self.__layout_tool_choose.addWidget(self.__pbn_open_tool)
        self.__layout_tool_choose.setSpacing(0)
        self.__layout_tool_choose.setContentsMargins(0, 0, 0, 0)
        
        self.__layout_open_tool = QHBoxLayout()
        self.__layout_open_tool.addWidget(self.__lab_open_tool)
        self.__layout_open_tool.addLayout(self.__layout_tool_choose)
        self.__layout_open_tool.setSpacing(2)

        # window title
        self.__layout_title = QHBoxLayout()
        self.__layout_title.addStretch(5)
        self.__layout_title.addWidget(self.__lab_title)
        self.__layout_title.addStretch(1)
        self.__layout_title.addLayout(self.__layout_open_tool)
        self.__layout_title.setContentsMargins(0, 0, 0, 20)
        self.__lab_title_fram.setLayout(self.__layout_title)

        # search mode
        self.__layout_search_mode = QHBoxLayout()
        self.__layout_search_mode.addWidget(self.__rbn_fuzzy)
        self.__layout_search_mode.addStretch()
        self.__layout_search_mode.addWidget(self.__rbn_precise)
        self.__layout_search_mode.addStretch()
        self.__layout_search_mode.addWidget(self.__rbn_reg)
        self.__layout_search_mode.setContentsMargins(60, 0, 60, 0)
        self.__lab_mode_fram.setLayout(self.__layout_search_mode)

        # search pattern
        self.__layout_search_reg_I = QHBoxLayout()
        self.__layout_search_reg_I.addWidget(self.__rbn_reg_Iyes)
        self.__layout_search_reg_I.addWidget(self.__rbn_reg_Ino)

        self.__layout_pattern = QHBoxLayout()
        self.__layout_pattern.addWidget(self.__ln_file_name)
        self.__layout_pattern.addLayout(self.__layout_search_reg_I)
        self.__layout_pattern.setContentsMargins(0, 0, 0, 0)
        self.__lab_pattern_fram.setLayout(self.__layout_pattern)

        # search path
        self.__layout_choose_path = QHBoxLayout()
        self.__layout_choose_path.addWidget(self.__ln_file_path)
        self.__layout_choose_path.addWidget(self.__pbn_file_path)
        self.__layout_choose_path.setSpacing(0)

        self.__layout_path = QHBoxLayout()
        self.__layout_path.addLayout(self.__layout_choose_path)
        self.__layout_path.addWidget(self.__rbn_search_file)
        self.__layout_path.addWidget(self.__rbn_search_content)
        self.__layout_path.setContentsMargins(0, 0, 0, 0)
        self.__lab_path_fram.setLayout(self.__layout_path)

        # search state
        self.__layout_state = QHBoxLayout()
        self.__layout_state.addWidget(self.__lab_state)
        self.__layout_state.addWidget(self.__pbn_search)
        self.__layout_state.addWidget(self.__pbn_stop)
        self.__layout_state.setContentsMargins(0, 0, 0, 10)
        self.__lab_state_fram.setLayout(self.__layout_state)

        # top layout
        self.__layout_top = QVBoxLayout()
        self.__layout_top.addWidget(self.__lab_title_fram)
        self.__layout_top.addWidget(self.__lab_mode_fram)
        self.__layout_top.addWidget(self.__lab_pattern_fram)
        self.__layout_top.addWidget(self.__lab_path_fram)
        self.__layout_top.addWidget(self.__lab_state_fram)
        self.__layout_top.addWidget(self.__tabView)
        self.__layout_top.setSpacing(10)
        self.__widget_frame.setLayout(self.__layout_top)

        self.__layout_fram = QGridLayout()
        self.__layout_fram.addWidget(self.__widget_frame, 0, 0, 1, 1)
        self.__layout_fram.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout_fram)

        # set object name
        self.__widget_frame.setObjectName('fram')
        self.__lab_title.setObjectName('lab_title')
        self.__ln_open_tool.setObjectName('ln_open_tool')
        self.__lab_mode_fram.setObjectName('mode_fram')
        self.__ln_file_name.setObjectName('ln_pattern')
        self.__ln_file_path.setObjectName('ln_path')
        self.__lab_state.setObjectName('state')
        self.__tabView.setObjectName('tabView')
        self.__browser_result.setObjectName('browser_result')
        self.__browser_error.setObjectName('browser_error')

        self.setStyleSheet(
            '#fram{'
                'border-image: url(Images/bg);'
            '}'
            '#lab_title{'
                'color: white;'
                'font-size: 18pt;'
            '}'
            '#open_tool{'
                'color: black;'
            '}'
            '#mode_fram{'
                # 'border-top: 1px solid rgba(20, 20, 20, 100);'
                # 'border-bottom: 1px solid rgba(20, 20, 20, 100);'
                'background: rgba(0, 0, 0, 40);'
            '}'
            '#ln_open_tool, #ln_path{'
                'border-top-left-radius:    2px;'
                'border-bottom-left-radius: 2px;'
            '}'
            '#ln_pattern{'
                'border-radius: 2px;'
            '}'
            '#state{'
                'background: rgba(0, 0, 0, 40);'
                'border-radius: 2px;'
                'padding: 1px;'
                'color: rgb(240, 240, 240);'
            '}'
            'QTabBar::tab {'
                'border: 0;'
                'width:  90px;'
                'height: 20px;'
                'margin: 0 2px 0 0;'        # top right bottom left
                # 'border-top-left-radius: 5px;'
                # 'border-top-right-radius: 5px;'
                'color: rgb(200, 255, 255;);'
            '}'
            'QTabBar::tab:selected{'
                'background: rgba(25, 0, 0, 40);'
                'border-left: 1px solid rgba(255, 255, 255, 200);'
                'border-top: 1px solid rgba(255, 255, 255, 200);'
                'border-right: 1px solid rgba(255, 255, 255, 200);'
            '}'
            'QTabWidget:pane {'
                'border: 1px solid rgba(255, 255, 255, 200);'
                'background: rgba(0, 0, 0, 80);'
            '}'
            '#browser_result, #browser_error{'
                'background: rgba(0, 0, 0, 0);'
                'border: 0;'
            '}'
            'QLineEdit{'
                'background: rgba(0, 0, 0, 40);'
                'border: 1px solid rgba(220, 220, 220, 200);'
                'color: white;'
                'height: 20px;'
            '}'
            'QPushButton{'
                'background: rgba(0, 0, 0, 100);'
                'border-radius: 5px;'
                'height: 20px;'
                'color: white;'
            '}'
            'QPushButton::hover{'
                'background: rgba(0, 0, 0, 150);'
            '}'
            'QToolButton{'
                'background: rgba(0, 0, 0, 100);'
                'color: white;'
                'border-top-right-radius:    2px;'
                'border-bottom-right-radius: 2px;'
            '}'
            'QToolButton::hover{'
                'background: rgba(0, 0, 0, 150);'
            '}'
            )

        self.__ln_file_name.setFocus()
        self.__pbn_search.setShortcut(Qt.Key_Return)

        # 关联 信号/槽
        self.__pbn_file_path.clicked.connect(self.choose_path)
        self.__pbn_search.clicked.connect(self.pbn_search_clicked)
        self.__pbn_stop.clicked.connect(self.pbn_stop)
        self.__pbn_open_tool.clicked.connect(self.choose_open_tool)
        self.__browser_result.doubleClicked.connect(self.listitem_clicked)

        # 线程间共享数据队列
        queue_size = 10000
        self.__queue_result = Queue(queue_size)
        self.__queue_error = Queue(queue_size)

        # 标记搜索状态
        self.__searching = False

    # 重写鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.pos()

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.offset)

    # 检测记事本程序
    def set_open_tool(self):
        if platform.architecture() == ('32bit', 'WindowsPE'):
            possible_dir = ['C:\\Program Files\\Sublime Text 2', 'C:\\Sublime Text 2',
                            'D:\\Program Files\\Sublime Text 2', 'D:\\Sublime Text 2',
                            'E:\\Program Files\\Sublime Text 2', 'E:\\Sublime Text 2',
                            'F:\\Program Files\\Sublime Text 2', 'F:\\Sublime Text 2',
                            'C:\\Program Files\\Notepad++', 'C:\\notepad++',
                            'D:\\Program Files\\Notepad++', 'D:\\notepad++',
                            'E:\\Program Files\\Notepad++', 'E:\\notepad++',
                            'F:\\Program Files\\Notepad++', 'F:\\notepad++',
                            'C:\\Windows\\System32']
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
        # check arguments of searching
        if filepath == '' or not exists(filepath):
            return False
        if mode not in self.__search_mode.values():
            return False
        if filename == '':
            return False

        # count
        count = 0

        # fuzzy mode
        if mode == self.__search_mode['fuzzy']:
            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if filename in each_file:
                        count += 1
                        self.__lab_state.setText('正在搜索......已搜到 %d 个文件' % count)
                        self.__queue_result.put(join(root, each_file))
                        self.__tabView.setTabText(0, '匹配结果(%d)' % count)
        # precise mode
        elif mode == self.__search_mode['precise']:
            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if filename == splitext(each_file)[0] or filename == each_file:
                        count += 1
                        self.__lab_state.setText('正在搜索......已搜到 %d 个文件' % count)
                        self.__queue_result.put(join(root, each_file))
                        self.__tabView.setTabText(0, '匹配结果(%d)' % count)
        # regular expression mode
        elif mode == self.__search_mode['reg']:
            if I:
                pattern = re.compile(r'%s' % filename)
            else:
                pattern = re.compile(r'%s' % filename, re.I)

            for root, dirs, files in walk(filepath):
                for each_file in files:
                    if re.search(pattern, each_file):
                        count += 1
                        self.__lab_state.setText('正在搜索......已搜到 %d 个文件' % count)
                        self.__queue_result.put(join(root, each_file))
                        self.__tabView.setTabText(0, '匹配结果(%d)' % count)
        self.__lab_state.setText('搜索完毕！ 共搜到 %d 个文件' % count)     # finished
        self.__searching = False                # set serching flag

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
        match_files_count = 0
        if mode == self.__search_mode['reg']:
            if I:
                pattern = re.compile(r'%s' % content)
            else:
                pattern = re.compile(r'%s' % content, re.I)
            for root, dirs, files in walk(path):
                for each_file in [file for file in files if file.endswith('.h') or file.endswith('.cpp') or file.endswith('.cs')]:
                    current_file = join(root, each_file)
                    pass_file_count += 1
                    self.__lab_state.setText('正在搜索......%s' % current_file)
                    try:
                        for line_number, line in enumerate(open(current_file)):
                            if re.search(pattern, line):
                                if processing_file != current_file:
                                    self.__queue_result.put('\n%s' % current_file)
                                    processing_file = current_file
                                    match_files_count += 1
                                self.__queue_result.put('line %s: %s' % (line_number, line.strip()))
                    except Exception as error:
                        self.__queue_error.put("%s\n(%s)\n" % (error, current_file))
                        pass_file_count -= 1
                        error_number += 1
                        continue
                    self.__tabView.setTabText(0, '匹配结果(%d)' % match_files_count)
        else:
            for root, dirs, files in walk(path):
                for each_file in [file for file in files if file.endswith('.h') or file.endswith('.cpp') or file.endswith('.cs') or file.endswith('.txt') or file.endswith('.py')]:
                    current_file = join(root, each_file)
                    pass_file_count += 1
                    self.__lab_state.setText('正在搜索......%s' % current_file)
                    try:
                        for line_number, line in enumerate(open(current_file)):
                            if content in line:                                         # 匹配成功
                                if processing_file != current_file:                     # 如果是新文件
                                    self.__queue_result.put('\n%s' % current_file)      # 文件名入队
                                    processing_file = current_file                      # 更新文件标记
                                    match_files_count += 1
                                self.__queue_result.put('line %s: %s' % (line_number, line.strip()))    # 匹配行入队
                    except Exception as error:
                        self.__queue_error.put("%s\n(%s)\n" % (error, current_file))
                        pass_file_count -= 1
                        error_number += 1
                        continue
                    self.__tabView.setTabText(0, '匹配结果(%d)' % match_files_count)
        # self.__queue_result.put()
        self.__lab_state.setText('搜索完毕！成功匹配 %d 个文件，处理 %s 个文件，失败 %s 文件。' % (match_files_count, pass_file_count, error_number))
        self.__searching = False

    # 单击选择路径按钮
    def choose_path(self):
        path = QFileDialog.getExistingDirectory()
        if path != '':
            path = sep.join(path.split('/'))
            self.__ln_file_path.setText(path)

    # 选择打开文件工具
    def choose_open_tool(self):
        path = QFileDialog.getOpenFileName()
        if path[0] != '':
            self.__ln_open_tool.setText(path[0])

    # 显示搜索结果
    def show_search_result(self):
        """将搜索结果加载到界面，供用户查看和操作"""
        line_block = []         # 定义临时列表，成批加载，避免刷新频率过高造成界面闪烁
        block_size = 10         # 一次性加载的个数
        while self.__searching or self.__queue_result.qsize():
            # if self.__searching or self.__queue_result.qsize() >= block_size:     // 永远记住这个 bug （生产者-消费者 问题）
            if self.__queue_result.qsize() >= block_size:                           # 如果队列中不小于 block_size 个项
                for i in range(block_size):                                             # 取出 block_size 个项
                    line_block.append(self.__queue_result.get())                        # 出队操作
                self.__browser_result.addItems(line_block)                                     # 一次性添加 block_size 个条目
                line_block.clear()                                                      # 清空临时列表
            elif self.__queue_result.qsize() >= 0:                                                                   # 如果队列中小于 block_size 各项
                item = self.__queue_result.get()                                        # 出队一项
                self.__browser_result.addItem(QListWidgetItem(item))                           # 加载到界面
            #self.__browser.setCurrentRow(self.__browser.count()-1)                  # 设置列表中最后一项为当前项，使列表不停滚动
            sleep(0.05)                                                              # 给界面事件循环腾出时间，避免界面冻结
        #self.__pbn_search.setEnabled(True)

    # 显示出错结果
    def show_error_result(self):
        """打印略过的文件和出错原因，多为 I/O Error"""
        count = 0
        while self.__queue_error.qsize() or self.__searching:
            if self.__queue_error.qsize() <= 0:
               continue
            self.__browser_error.append(self.__queue_error.get())
            count += 1
            self.__tabView.setTabText(1, '错误结果(%d)' % count)

    # 单击检索按钮
    def pbn_search_clicked(self):
        """To search allow the arguments from UI"""
        # 获取 UI 数据
        file_path = self.__ln_file_path.text()
        file_name = self.__ln_file_name.text()

        # 检查参数
        if file_path == '':
            QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入搜索路径！', QMessageBox.Ok, self).exec_()
            return
        if file_name == '':
            QMessageBox(QMessageBox.Warning, '缺少参数！', '请输入匹配条件！', QMessageBox.Ok, self).exec_()
            return

        # 判断搜索模式
        mode = self.__search_mode['fuzzy']
        if self.__rbn_reg.isChecked():
            mode = self.__search_mode['reg']
        elif self.__rbn_fuzzy.isChecked():
            mode = self.__search_mode['fuzzy']
        elif self.__rbn_precise.isChecked():
            mode = self.__search_mode['precise']

        # 大小写敏感标记
        I = True
        if self.__rbn_reg_Ino.isChecked():
            I = False

        self.__browser_result.clear()
        self.__browser_error.clear()
        self.__tabView.setTabText(0, '匹配结果(0)')
        self.__tabView.setTabText(1, '错误结果(0)')
        self.__searching = True

        # 开启子线程，后台深度遍历
        if self.__rbn_search_file.isChecked():
            self.__lab_state.setText('正在搜索......已搜索到 0 个文件')
            self.__sub_thread_search = Thread(target=self.search_from_filename, args=(file_path, file_name, mode, I))
            self.__sub_thread_search.start()
        else:
            self.__lab_state.setText('正在搜索......')
            self.__sub_thread_search = Thread(target=self.search_from_content, args=(file_path, file_name, mode, I))
            self.__sub_thread_search.start()

        # 开启子线程，显示搜索结果
        self.__sub_thread_show_result = Thread(target=self.show_search_result)
        self.__sub_thread_show_result.start()

        # 开启子线程，显示错误结果
        self.__sub_thread_show_error = Thread(target=self.show_error_result)
        self.__sub_thread_show_error.start()

        # self.__pbn_search_file.setEnable(False)
        # self.__pbn_search_content.setEnable(False)

    # 单击停止按钮
    def pbn_stop(self):
        if not self.__searching:
            return
        if self.__sub_thread_search.isAlive():
            self.__sub_thread_search._stop()
        self.__queue_result.Clear()
        self.__queue_error.Clear()
        if self.__sub_thread_show_result.isAlive:
            self.__sub_thread_show_result._stop()
        if self.__sub_thread_show_error.isAlive:
            self.__sub_thread_show_error._stop()
        self.__lab_state.setText('搜索已停止！')
        self.__searching = False

    # 双击搜索结果
    def listitem_clicked(self):
        """Double click to open the file from search result"""
        file_path = self.__browser_result.currentItem().text().strip()
        read_tool = self.__ln_open_tool.text()
        if not exists(file_path):
            QMessageBox.warning(self, '错误！', '请双击文件名\n%s 不是文件或打不开！' % file_path, QMessageBox.Ok)
            return
        if splitext(file_path)[1] in ['.jpg', '.png', '.jpeg', '.gif']:
            file_path = r'%s'.replace(' ', r'\ ') % file_path
            system('%s' % file_path)
        else:
            system('"%s" %s' % (read_tool, file_path))

# 程序入口
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.set_open_tool()
    sys.exit(app.exec_())
