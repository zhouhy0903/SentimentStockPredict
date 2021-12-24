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
# from model.predicting import analyze
import jieba
import re
from snownlp import SnowNLP
from time import sleep
import pandas as pd
import threading
import matplotlib.pyplot as plt
from matplotlib import cm

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
        self.ui.lineEdit_uid.setText("1618051664")
        # self.ui.lineEdit_3.setText("WEIBOCN_FROM=1110006030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWoawuI8MYqqWDUyLHe9l9.5JpX5K-hUgL.Foq0So5pSKBReh.2dJLoI7f0Us8EMNWyqcHkwJy4; MLOGIN=1; loginScene=102003; _T_WM=65508160464; XSRF-TOKEN=17523d; SCF=Ap2l6JZls0FbnRHRbW5c1o7xhyTXf-07BTrGNlGwL0uRE2bAP1GUSzQugoEGlJGOpUZgdaOkVzw8whB7qRlNsKQ.; SUB=_2A25MxmTSDeRhGeBN7VIQ9SrEyzWIHXVsSQyarDV6PUJbktAKLWT2kW1NREAMJJj-dB53n5BNd5ZLK_DjfG4xvwKA; SSOLoginState=1640109186; ALF=1642701186; M_WEIBOCN_PARAMS=lfid=102803&luicode=20000174&uicode=20000174")
        self.ui.lineEdit_startpage.setText("1")
        self.ui.lineEdit_endpage.setText("3")

        self.ui.lineEdit_filelocation.setText(r"C:\Users\zhy99\Desktop\code\final\20211222\SentimentStockPredict\example.csv")
        
        # global variable        
        self.text_df=None
        self.is_crawling=False



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

        #crawl page
        widgets.pushButton_save2file.clicked.connect(self.save2file)
        widgets.pushButton_2.clicked.connect(self.getpage)
        
        # sentiment page
        widgets.pushButton_getWordFrequency.clicked.connect(self.getWordFrequency)
        widgets.pushButton_sentiment.clicked.connect(self.getSentiment)
        widgets.pushButton_readfile.clicked.connect(self.readtextfile)
        widgets.pushButton_keywords.clicked.connect(self.showkeywords)
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
        self.is_crawling=True
        print("get page")
        print(self.ui.lineEdit_uid.text())
        print(self.ui.lineEdit_cookies.text())
        print(self.ui.lineEdit_startpage.text())
        print(self.ui.lineEdit_endpage.text())
        mycrawler=crawler(userid=int(self.ui.lineEdit_uid.text()),cookie=self.ui.lineEdit_cookies.text())
        # mycrawl.get_pages(startpage=int(self.ui.lineEdit_startpage.text()),endpage=int(self.ui.lineEdit_endpage.text()))
        startpage,endpage=int(self.ui.lineEdit_startpage.text()),int(self.ui.lineEdit_endpage.text())
        self.ui.weibotext.setPlainText("")
        # progresstext=threading.Thread(target=changetext,args=(self.ui.crawlprogress,))
        # progresstext.start()
        self.wb_all=[]
        for p in range(startpage,endpage):
            self.ui.crawlprogress.setPlainText("正在抓取第{}页".format(p)+"."*(p-startpage))
            self.ui.crawlprogress.repaint()
            sleep(1)
            mycrawler.get_page(p)
            self.wb_all.extend(mycrawler.wb_list)
            for wb in mycrawler.wb_list:  
                self.ui.weibotext.insertPlainText(",".join([str(v) for v in dict((key, value) for key, value in wb.items() if key in ["time","text"]).values()])+"转发 {}-评论 {}-点赞 {}".format(wb["repost"],wb["comment"],wb["like"])+"\n\n")

            mycrawler.wb_list=[]
            sleep(2)
        
        self.ui.crawlprogress.setPlainText("全部完成！")
        self.is_crawling=False

    def save2file(self):
        savepath=self.ui.lineEdit_savepath.text()
        if savepath:
            with open(savepath,"w") as f:
                for wb in self.wb_all:
                    try:
                        f.write(",".join([str(v) for v in wb.values()])+"\n")
                    except Exception:
                        pass

        if os.path.exists(savepath):
            self.ui.crawlprogress.setPlainText("已保存至文件 %s" % savepath)
            self.ui.crawlprogress.repaint()

        
        
        # self.ui.textBrowser.show()
        # self.ui.textBrowser.repaint()

    def getWordFrequency(self):
        myinputtext=inputtext()
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
        self.text_df=myinputtext.handletxt(self.ui.lineEdit_filelocation.text())
        
        self.ui.plainTextEdit_result.setPlainText("")
        # print(self.text_df[:5])
        # pos,neg,score=analyze(self.text_df)
        # print(pos,neg,score)
        for idx,text in enumerate(self.text_df["text"].to_list()):
            s=SnowNLP(text)
            self.ui.plainTextEdit_result.insertPlainText("%s %.2f" % (text[:10],s.sentiments-0.5)+"\n")

            # ai.baidu.com
            # self.ui.plainTextEdit_result.insertPlainText("积极:%.2f 消极:%.2f 成绩:%.2f——%s\n" % (pos[idx],neg[idx],score[idx],text))

    def readtextfile(self):
        self.ui.weibotext_file.setPlainText("")
        myinputtext=inputtext()
        self.text_df=myinputtext.handletxt(self.ui.lineEdit_filelocation.text())
        self.ui.weibotext_file.setPlainText("\n\n".join(["\n".join([a[0],a[1]]) for a in zip(self.text_df["time"].tolist(),self.text_df["text"].tolist())]))

    def showkeywords(self):
        self.ui.plainTextEdit_result.setPlainText("")
        myinputtext=inputtext()
        self.text_df=myinputtext.handletxt(self.ui.lineEdit_filelocation.text())
        text_list=[jieba.lcut(t) for t in self.text_df["text"].tolist()]
        text_removestopword=myinputtext.remove_stopword(text_list)
        print(text_removestopword[:5])
        df=pd.DataFrame([b for a in text_removestopword for b in a],columns=["word"])

        df_count=df["word"].value_counts()
        for idx in range(1,len(df_count)):
            self.ui.plainTextEdit_result.insertPlainText("%s %d" % (df_count.index[idx],df_count.iloc[idx])+"\n")
        df_count_freq=pd.DataFrame(df_count[1:])
        df_count_freq.columns=["freq"]
        df_count_freq_select=df_count_freq[df_count_freq["freq"]>len(df)/300]
        print(len(df))

        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
        norm = plt.Normalize(-1,1)
        map_vir = cm.get_cmap(name='viridis')
        colors = map_vir(norm((df_count_freq_select["freq"]-df_count_freq_select["freq"].min())/(df_count_freq_select["freq"].max()-df_count_freq_select["freq"].min()).tolist()))
        # print(norm(df_count_freq_select["freq"].tolist()))
        plt.bar(df_count_freq_select.index.tolist(),df_count_freq_select["freq"].tolist(),color=colors)
        plt.xticks(fontproperties = 'Simhei', size = 18)
        plt.xticks(fontproperties = 'Simhei', size = 18)
        plt.show()

        # df.sort_values("word",inplace=True)
        # print(df)





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
