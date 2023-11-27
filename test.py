import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path

class EditImages:

    def __init__(self, path):

        folder_path = (window.output_label.text())

        print(folder_path)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Frame processer')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a button to choose the project directory.
        btn1 = QPushButton('Choose Project Directory')
        layout.addWidget(btn1)
        btn1.clicked.connect(self.search_dir)
        btn1.setMinimumSize(250, 40)

        # Create an output label that will show the chosen directory once the user has selected it.
        output_label = QLabel('')
        layout.addWidget(output_label)
        output_label.setMinimumHeight(40)

        # Create a "Process" button and connect it with the functions used for renaming the files and creating the project
        # zip file.
        btn2 = QPushButton('Process')
        btn2.setMinimumSize(250, 40)
        btn2.setStyleSheet('QPushButton {background-color: rgb(120, 120, 120); font: bold 14px; color: white;}')
        layout.addWidget(btn2)
        
    def search_dir(self):
        """Choose the directory of the project folder and enable the "Process" button once done."""
        folder_name = QFileDialog.getExistingDirectory()
        self.output_label.setText(folder_name)  # Set the label to the chosen folder directory.
        # self.btn2.setDisabled(False)

app = QApplication([])

window = MyApp()
window.show()

app.exec()