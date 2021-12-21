import sys
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QAction, QMenu, QMessageBox
from PyQt5 import QtWidgets, uic

from compress import *
from xmlToJson import *

from XML_GUI import Ui_MainWindow
import os




class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        title = "XML-Editor"
        self.setWindowTitle(title)
        self.menu()

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'XML files (*.xml)')
        path = fname[0]
        with open(path, "r") as f:
            data = f.read()
            self.ui.textEdit.setText(data)

    def exit_app(self):
        self.close()

    def save_file(self):
        file = QtWidgets.QFileDialog.getSaveFileName(None, 'SaveTextFile', '/', "XML Files (*.xml)")
        text = self.ui.textEdit.toPlainText()
        if file[0]:
            with open(file[0], 'w') as f:
                f.write(text)

    def compress_space(self):
        data = minify_file(str(self.ui.textEdit.toPlainText()))
        self.ui.textEdit.setText(data)

    def compress_Huffman(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'XML files (*.xml)')
        path = fname[0]
        generate_compress_code(path)
        QMessageBox.about(self, "Success", "File Compressed Successfully and saved in same directory")

    def decompress_Huffman(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', 'D:', 'Compressed Files (*.Huffman)')
        path = fname[0]
        data = decompress_Huffman(path)
        QMessageBox.about(self, "Success", "File Expanded and will be appear now")
        self.ui.textEdit.setText(data)

    def format(self):
        data = formatting(str(self.ui.textEdit.toPlainText()))
        print(data)
        self.ui.textEdit.setText(data)

    def detect_errors(self):
        data = detectErrors(str(self.ui.textEdit.toPlainText()))
        self.ui.textBrowser.setText(data)

    def modify_errors(self):
        data = errorFixing(str(self.ui.textEdit.toPlainText()))
        self.ui.textEdit.setText(data)

    def xmltojson(self):
        data = main(formatting(str(self.ui.textEdit.toPlainText())))
        self.ui.textEdit.setText(data)


    def menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("edit")

        openAction = QAction(QIcon('open.png'), "Open", self)
        saveAction = QAction(QIcon('save.png'), "Save", self)
        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        compressSpacesAction = QAction(QIcon('cmpressSapces')," Compress Spaces",self)
        compressHuffmanAction = QAction(QIcon('compressHuffman'), " Compress Huffman", self)
        decompressHuffmanAction = QAction(QIcon('decompressHuffman'), " Decompress Huffman", self)
        formatAction = QAction(QIcon('format'), " Format", self)
        detectAction = QAction(QIcon('detect'), " Detect Errors", self)
        modifyErrorsAction = QAction(QIcon('modify error'), " MOdify Errors", self)
        xmlToJsonAction = QAction(QIcon('xml2Json'), " XML to Json", self)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        editMenu.addAction(compressSpacesAction)
        editMenu.addAction(compressHuffmanAction)
        editMenu.addAction(decompressHuffmanAction)

        viewMenu.addAction(formatAction)
        viewMenu.addAction(detectAction)
        viewMenu.addAction(modifyErrorsAction)
        viewMenu.addAction(xmlToJsonAction)


        openAction.triggered.connect(self.browsefiles)
        saveAction.triggered.connect(self.save_file)
        exitAction.triggered.connect(self.exit_app)
        compressSpacesAction.triggered.connect(self.compress_space)
        compressHuffmanAction.triggered.connect(self.compress_Huffman)
        decompressHuffmanAction.triggered.connect(self.decompress_Huffman)
        formatAction.triggered.connect(self.format)
        detectAction.triggered.connect(self.detect_errors)
        modifyErrorsAction.triggered.connect(self.modify_errors)
        xmlToJsonAction.triggered.connect(self.xmltojson)


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1430)
widget.setFixedHeight(650)
widget.show()
sys.exit(app.exec_())
