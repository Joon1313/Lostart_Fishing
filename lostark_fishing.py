import sys
import os
import time
import datetime as dt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyautogui as pa
import mouse as mo
import keyboard as key
import random

class Thread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.main = parent

    def run(self):
        img_path = self.main.resource_path(name="mark.png")
        img_path2 = self.main.resource_path(name="hand.png")
        tup = pa.size()
        tup = (int(tup[0] / 2), int(tup[1] / 2))
        region = self.main.makeRegion(center=tup, width=100, height=100)
        count = 0
        hand = 0
        time.sleep(3)
        while True:
            if self.main.status == 0:
                break
            else:
                if self.main.count == 10:
                    text.append('10회 이상 실패로 인한 매크로 중지')
                    status.showMessage('대기중')
                    break
                else:
                    pa.moveTo(random.randrange(250, 600), random.randrange(300, 500), 1)
                    if hand == 5:
                        pa.press('r')
                        sbtn.setText('시작')
                        text.append('투망 낚시 시작으로인한 매크로 중지')
                        status.showMessage('대기중')
                        break
                        # for i in range(20000):
                    else:
                        hand = 0
                        pa.press('e')
                        time.sleep(2)
                        for i in range(150):
                            if self.main.status == 0:
                                break

                            imgpos = pa.locateOnScreen(img_path, confidence=0.7, region=region)
                            if imgpos != None:
                                time.sleep(round(random.uniform(0.3, 0.7), 2))
                                pa.press('e')
                                count += 1
                                text.append(f"{count} 회 작동중!")
                                for i in range(55):
                                    hand_img = pa.locateOnScreen(img_path2, confidence=0.7, region=(912, 570, 120, 120))
                                    if hand_img != None:
                                        hand = 1
                                        # self.main.status = 0
                                        time.sleep(3)
                                        break
                                    else:
                                        time.sleep(0.1)
                                break
                            else:
                                time.sleep(0.1)
                                if i==149:
                                    if imgpos == None:
                                        text.append('작동 실패...')
                                        self.main.count += 1
                                        break


class MyApp(QWidget):
    status = 0
    sbtn = 0
    count = 0
    text = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.statusBar().showMessage('Ready')
        grid = QGridLayout()
        grid.addWidget(self.ment(), 0, 0)
        grid.addWidget(self.createFirstExclusiveGroup(), 1, 0)
        grid.addWidget(self.btnGroup(), 2, 0)
        grid.addWidget(self.record(), 3, 0)
        grid.addWidget(self.status(), 4, 0)

        # self.statusbar = QtWidgets.QStatusBar()
        # self.statusBar().showMessage('Ready')
        # self.statusBar = QStatusBar(self)
        # self.statusBar.showMessage('상태바')
        self.setWindowTitle('camon')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setLayout(grid)
        self.setWindowIcon(QIcon(self.resource_path(name='icon.ico')))
        self.move(300, 300)
        self.resize(300, 300)
        self.show()
        # # 클래스 시그널 연결
        # self.cal = Thread(self)
        # self.cal.success.connect(self.success_print)
    #
    #
    # @pyqtSlot(str)
    # def success_print(self , data):
    #     print(data)

    def status_control(self):
        x = dt.datetime.now()
        time = x.strftime("%H시 %M분 %S초")
        if sbtn.text() == '시작':
             sbtn.setText('중지')
             text.append(time+' 시작 되었습니다.')
             status.showMessage('작동중입니다.')
             self.status = 1
             self.count = 0
             self.start()
        else:
            sbtn.setText('시작')
            text.append(time+' 중지 되었습니다.')
            status.showMessage('대기중.')
            self.status = 0
            self.count = 0

    def start(self):
        x = Thread(self)
        x.start()

    def makeRegion(self ,center, width, height):
        x = center[0]
        y = center[1]
        startPos = (x - width, y - height)
        region = (startPos[0], startPos[1], 2 * width, 2 * height)
        return region

    def createFirstExclusiveGroup(self):
        groupbox = QGroupBox('낚시 지역 선택')

        radio1 = QRadioButton('레이크바')
        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        groupbox.setLayout(vbox)

        return groupbox
    def btnGroup(self):
        global sbtn

        groupbox = QGroupBox('동작')

        sbtn = QPushButton('시작', self)
        sbtn.resize(sbtn.sizeHint())
        sbtn.clicked.connect(self.status_control)

        qbtn = QPushButton('종료', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.clicked.connect(QCoreApplication.instance().quit)

        vbox = QVBoxLayout()
        vbox.addWidget(sbtn)
        vbox.addWidget(qbtn)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def ment(self):

        groupbox = QGroupBox('제작자')

        label = QLabel('깜언', self)
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(20)
        font.setBold(True)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        groupbox.setLayout(vbox)

        return groupbox
    def record(self):
        global text
        groupbox = QGroupBox('기록')
        text = QTextBrowser()
        vbox = QVBoxLayout()
        vbox.addWidget(text)
        groupbox.setLayout(vbox)

        return groupbox

    def status(self):
        global status
        groupbox = QGroupBox('상태')
        status = QStatusBar()
        status.showMessage('대기중.')
        vbox = QVBoxLayout()
        vbox.addWidget(status)
        groupbox.setLayout(vbox)

        return groupbox

    def resource_path(self, name):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, name)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
