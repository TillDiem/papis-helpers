#!/opt/homebrew/Caskroom/miniforge/base/bin/python
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QGridLayout, QGroupBox, QComboBox, QTabWidget
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Papis Adder by 🐾'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createGridLayout()

        self.tabs = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "ArXiv/DOI")
        self.tabs.addTab(self.tab2, "Manual")

        self.tab1.setLayout(self.gridLayout)
        self.tab2.setLayout(self.manualGridLayout)

        windowLayout = QGridLayout()
        windowLayout.addWidget(self.tabs, 0, 0)
        self.setLayout(windowLayout)
        self.show()

    def createGridLayout(self):
        # Layout for ArXiv/DOI tab
        self.gridLayout = QGridLayout()
        self.url = QLineEdit()
        self.url.setPlaceholderText("Enter URL")
        self.tags = QLineEdit()
        self.tags.setPlaceholderText("Enter tags")
        self.add = QPushButton('Add', self)
        self.add.clicked.connect(self.on_click)
        self.gridLayout.addWidget(self.url, 0, 0)
        self.gridLayout.addWidget(self.tags, 1, 0)
        self.gridLayout.addWidget(self.add, 2, 0)
        self.warning = QLabel()
        self.gridLayout.addWidget(self.warning, 3, 0)
        self.library = QComboBox()
        self.library.addItem("Papers")
        self.library.addItem("Thesis")
        self.gridLayout.addWidget(self.library, 4, 0)

        # New layout for Manual tab
        self.manualGridLayout = QGridLayout()
        self.title_manual = QLineEdit()
        self.title_manual.setPlaceholderText("Title")
        self.authors_manual = QLineEdit()
        self.authors_manual.setPlaceholderText("Authors")
        self.year_manual = QLineEdit()
        self.year_manual.setPlaceholderText("Year")
        self.url_manual = QLineEdit()
        self.url_manual.setPlaceholderText("URL")
        self.publisher_manual = QLineEdit()
        self.publisher_manual.setPlaceholderText("Publisher")
        self.documenttype_manual = QLineEdit()
        self.documenttype_manual.setPlaceholderText("Document Type (phdthesis, article, etc.)")
        self.ref_manual = QLineEdit()
        self.ref_manual.setPlaceholderText("Reference")
        self.tags_manual = QLineEdit()
        self.tags_manual.setPlaceholderText("Tags")
        self.add_manual = QPushButton('Add', self)
        self.add_manual.clicked.connect(self.on_click_manual)
        self.library_manual = QComboBox()
        self.library_manual.addItem("Papers")
        self.library_manual.addItem("Thesis")
        self.manualGridLayout.addWidget(self.title_manual, 0, 0)
        self.manualGridLayout.addWidget(self.authors_manual, 1, 0)
        self.manualGridLayout.addWidget(self.year_manual, 2, 0)
        self.manualGridLayout.addWidget(self.url_manual, 3, 0)
        self.manualGridLayout.addWidget(self.publisher_manual, 4, 0)
        self.manualGridLayout.addWidget(self.documenttype_manual, 5, 0)
        self.manualGridLayout.addWidget(self.ref_manual, 6, 0)
        self.manualGridLayout.addWidget(self.tags_manual, 7, 0)
        self.manualGridLayout.addWidget(self.add_manual, 8, 0)
        self.manualGridLayout.addWidget(self.library_manual, 9, 0)

    @pyqtSlot()
    def on_click(self):
        url = self.url.text()
        #check if the url is an arxiv url
        papis_add_command = ""
        if "arxiv.org" in url:
            #check if it should be added to the papers or thesis library
            if self.library.currentText() == "Papers":
                papis_add_command = "papis -l papers add --from arxiv " + url
            elif self.library.currentText() == "Thesis":
                papis_add_command = "papis -l thesis add --from arxiv " + url
        elif "doi.org" in url:
            #check if it should be added to the papers or thesis library
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PDF Files (*.pdf)")
            if self.library.currentText() == "Papers":
                papis_add_command = "papis -l papers add --from doi " + url + " " + fileName
            elif self.library.currentText() == "Thesis":
                papis_add_command = "papis -l thesis add --from doi " + url + " " + fileName
        if self.tags.text() != "":
            papis_add_command += " --set tags '" + self.tags.text() + "'"
        else:
            self.warning.setText("URL not supported, please use the terminal version as in:\n https://papis.readthedocs.io/en/stable/commands.html")
        subprocess.call(papis_add_command, shell=True)

    def on_click_manual(self):
        url = self.url_manual.text()
        title = self.title_manual.text()
        authors = self.authors_manual.text()
        year = self.year_manual.text()
        publisher = self.publisher_manual.text()
        documenttype = self.documenttype_manual.text()
        ref = self.ref_manual.text()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PDF Files (*.pdf)")
        papis_add_command = ""
        if self.library_manual.currentText() == "Papers":
            papis_add_command = "papis -l papers add " +fileName
        elif self.library_manual.currentText() == "Thesis":
            papis_add_command = "papis -l thesis add " + fileName
        if self.title_manual.text() != "":
            papis_add_command += " --set title '" + self.title_manual.text() + "'"
        if self.authors_manual.text() != "":
            papis_add_command += " --set author '" + self.authors_manual.text() + "'"
        if self.year_manual.text() != "":
            papis_add_command += " --set year " + self.year_manual.text()
        if self.url_manual.text() != "":
            papis_add_command += " --set url '" + self.url_manual.text() + "'"
        if self.publisher_manual.text() != "":
            papis_add_command += " --set publisher '" + self.publisher_manual.text() + "'"
        if self.documenttype_manual.text() != "":
            papis_add_command += " --set type " + self.documenttype_manual.text()
        if self.ref_manual.text() != "":
            papis_add_command += " --set ref " + self.ref_manual.text()
        if self.tags_manual.text() != "":
            papis_add_command += " --set tags '" + self.tags_manual.text() + "'"
        print(papis_add_command)
        subprocess.call(papis_add_command, shell=True)



    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
