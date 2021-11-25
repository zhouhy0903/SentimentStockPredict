from PyQt5 import QtCore,QtGui,QtWidgets
import sys

class mainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()
	
	def init_ui(self):
		self.setWindowTitle("SentimentStockPredict")
		self.main_widget = QtWidgets.QWidget() 
		self.main_layout = QtWidgets.QGridLayout()
		self.main_widget.setLayout(self.main_layout)


if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)
	QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
	gui = mainWindow()
	gui.show()
	sys.exit(app.exec_())