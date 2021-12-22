# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from datacollector.wb import crawler
from model.prepare import inputtext
import jieba
import re
from snownlp import SnowNLP

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ui related
        self.ui.lineEdit_2.setText("1618051664")
        self.ui.lineEdit_3.setText("WEIBOCN_FROM=1110006030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWoawuI8MYqqWDUyLHe9l9.5JpX5K-hUgL.Foq0So5pSKBReh.2dJLoI7f0Us8EMNWyqcHkwJy4; MLOGIN=1; loginScene=102003; _T_WM=65508160464; XSRF-TOKEN=17523d; SCF=Ap2l6JZls0FbnRHRbW5c1o7xhyTXf-07BTrGNlGwL0uRE2bAP1GUSzQugoEGlJGOpUZgdaOkVzw8whB7qRlNsKQ.; SUB=_2A25MxmTSDeRhGeBN7VIQ9SrEyzWIHXVsSQyarDV6PUJbktAKLWT2kW1NREAMJJj-dB53n5BNd5ZLK_DjfG4xvwKA; SSOLoginState=1640109186; ALF=1642701186; M_WEIBOCN_PARAMS=lfid=102803&luicode=20000174&uicode=20000174")
        self.ui.lineEdit_4.setText("1")
        self.ui.lineEdit_5.setText("1")

        self.ui.lineEdit_filelocation.setText(r"C:\Users\zhy99\Desktop\code\final\20211222\SentimentStockPredict\example.csv")
        
        # global variable        
        self.text_df=None



        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "微博信息爬取及股市预测"
        description = "程设大作业"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)

        widgets.pushButton_2.clicked.connect(self.getpage)
        widgets.pushButton_getWordFrequency.clicked.connect(self.getWordFrequency)
        widgets.pushButton_sentiment.clicked.connect(self.getSentiment)

        # widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # if btnName == "btn_widgets":
        #     widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        #     UIFunctions.resetStyle(self, btnName)
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.sentiment_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # if btnName == "btn_save":
        #     print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')
    

    def getpage(self):
        print("get page")
        print(self.ui.lineEdit_2.text())
        print(self.ui.lineEdit_3.text())
        print(self.ui.lineEdit_4.text())
        print(self.ui.lineEdit_5.text())
        mycrawl=crawler(userid=int(self.ui.lineEdit_2.text()),cookie=self.ui.lineEdit_3.text())
        mycrawl.get_pages(startpage=int(self.ui.lineEdit_4.text()),endpage=int(self.ui.lineEdit_5.text()))
        
        print(mycrawl.wb_list)

        self.ui.weibotext.setPlainText("")

        for wb in mycrawl.wb_list:  
            del wb["wbid"],wb["comment"],wb["repost"]  
            self.ui.weibotext.insertPlainText(",".join([str(v) for v in wb.values()])+"\n\n")
        # self.ui.textBrowser.show()
        # self.ui.textBrowser.repaint()

    def getWordFrequency(self):
        myinputtext=inputtext()
        if self.text_df is None:
            self.text_df=myinputtext.handletxt(self.ui.lineEdit_filelocation.text())
        text_list=[jieba.lcut(t) for t in self.text_df["text"].tolist()]
        print(text_list[:2])
        print()

        text_removestopword=myinputtext.remove_stopword(text_list)
        print(text_removestopword[:2])

        # inputSearchText="疫情;经济,科技:历史"
        inputSearchText=self.ui.lineEdit_searchText.text()
        print(inputSearchText)
        keywords=re.split('[,;:]',inputSearchText)
        # keywords_count={"疫情":0,"经济":0}
        keywords_count=dict(zip(keywords,[0]*len(keywords)))
        print(keywords_count)
        for sentence in text_removestopword:
            for text in sentence:
                if text in keywords_count.keys():
                    keywords_count[text]+=1

        print(keywords_count)
        result_text=""
        for key,values in keywords_count.items():
            result_text+="{}出现了{}次\n".format(key,values)
        # print(text_removestopword)        
        
        self.ui.plainTextEdit_result.setPlainText(result_text)

    
    def getSentiment(self):
        myinputtext=inputtext()
        if self.text_df is None:
            self.text_df=myinputtext.handletxt(self.ui.lineEdit_filelocation.text())
        
        self.ui.plainTextEdit_result.setPlainText("分析文本情感指数...")
        for text in self.text_df["text"].to_list():
            s=SnowNLP(text)
            self.ui.plainTextEdit_result.insertPlainText("%s %.2f" % (text,s.sentiments)+"\n")


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
