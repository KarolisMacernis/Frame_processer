import sys
import os
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QFileDialog, QLabel, QSizePolicy, QFormLayout, QComboBox, QMainWindow
import PyQt6.QtWidgets as qtw
from PIL import Image
import re

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Frame processer')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create a button to choose the project directory.
        self.btn_dir = QPushButton('Choose Image Directory')
        self.layout.addWidget(self.btn_dir)
        self.btn_dir.clicked.connect(self.search_dir)
        self.btn_dir.clicked.connect(self.enable_options)
        self.btn_dir.setMinimumSize(270, 47)
        self.btn_dir.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create an output label that will show the chosen directory once the user has selected it.
        self.output_label = QLabel('Selected path:   None')
        self.layout.addWidget(self.output_label)
        self.output_label.setMinimumHeight(50)
        self.output_label.setWordWrap(True)
        self.output_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a form layout to input the project name, frame numbering and the resolution.
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Create a vertical layout for the options to choose the new resolution.
        self.layout1 = QHBoxLayout()
        self.layout.addLayout(self.layout1)

        # Create a label with instructions to the resolution of the images.
        self.dpi_instructions = QLabel('Select the resolution for the images:')
        self.layout1.addWidget(self.dpi_instructions)
        self.dpi_instructions.setDisabled(True)
        self.dpi_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a dropdown list to choose the resolution of the images.
        self.dpi_combo = qtw.QComboBox(self)
        self.dpi_combo.addItem("Use original")
        self.dpi_combo.addItem("Set to 600 dpi")
        self.dpi_combo.addItem("Set to 300 dpi")
        self.dpi_combo.addItem("Set to 150 dpi")
        self.dpi_combo.addItem("Set to 75 dpi")
        self.layout1.addWidget(self.dpi_combo)
        self.dpi_combo.setDisabled(True)
        self.dpi_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a horizontal layout for entering the name of the project.
        self.layout2 = QHBoxLayout()
        self.layout.addLayout(self.layout2)

        # Create a horizontal layout for choosing the numbering of the project.
        self.layout3 = QHBoxLayout()
        self.layout.addLayout(self.layout3)

        # Create the input line for entering the project name and the instructions to do so.
        self.name_instructions = QLabel('Enter name of the project:')
        self.layout3.addWidget(self.name_instructions)
        self.name_instructions.setDisabled(True)
        self.name_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create an instruction label to choose the numbering for the images.
        self.numbering_instructions = QLabel('Choose the numbering for the images:')
        self.layout2.addWidget(self.numbering_instructions)
        self.numbering_instructions.setDisabled(True)
        self.numbering_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a dropdown list to choose the numbering of the images.
        self.numbering_combo = qtw.QComboBox(self)
        self.numbering_combo.addItem("_1, _2, ...")
        self.numbering_combo.addItem("-1, -2, ...")
        self.numbering_combo.addItem("_01, _02, ...")
        self.numbering_combo.addItem("-01, -02, ...")
        self.layout2.addWidget(self.numbering_combo)
        self.numbering_combo.setDisabled(True)
        self.numbering_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create an input box for entering the name of the project.
        self.project_name = QLineEdit()
        self.layout3.addWidget(self.project_name)
        self.project_name.setDisabled(True)
        self.project_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a "Process" button and connect it with the functions used for renaming the files and creating the
        # project zip file.
        self.btn_process = QPushButton('Process')
        self.btn_process.setMinimumSize(270, 47)
        self.layout.addWidget(self.btn_process)
        self.btn_process.setDisabled(True)
        self.btn_process.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_process.clicked.connect(self.change_dpi)

        # self.btn_process.clicked.connect(self.img.adjust_dpi)

        self.form_layout.addRow(self.dpi_instructions, self.dpi_combo)
        self.form_layout.addRow(self.numbering_instructions, self.numbering_combo)
        self.form_layout.addRow(self.name_instructions, self.project_name)



    def search_dir(self):
        """Choose the directory of the project folder and enable the "Process" button once done."""
        self.folder_name = QFileDialog.getExistingDirectory()
        self.output_label.setText(f"Selected path:   {self.folder_name}")  # Set the label to the chosen folder
        # directory.



    def change_dpi(self):


        """Change the dpi value of the images."""
        folder_path = self.folder_name

        new_folder = os.path.join(folder_path, "Adjusted Images")

        img_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")

        if not os.path.exists(new_folder):  # Create the directory if it doesn't exist
            os.mkdir(new_folder)

        dpi_chosen = self.dpi_combo.currentText()
        dpi_numeric = int(''.join(c for c in dpi_chosen if c.isdigit()))  # extract the numeric dpi value.

        name_extracted = self.project_name.text()

        self.numbering_chosen = self.numbering_combo.currentText()
        self.number_seperation = self.numbering_chosen[0]
        self.first_digit = int(self.numbering_chosen[1])
        file_counter = 1  # index of the image

        if dpi_chosen == "Use original":  # Change the dpi of the images if the user chooses so.
            for filename in os.listdir(folder_path):  # Loop through all files in the directory
                if filename.lower().endswith(img_extensions):  # Check if the file is an image
                    img = Image.open(os.path.join(folder_path, filename))  # Open the image file
                    ext = os.path.splitext(filename)[1]
                    if self.first_digit == 0:
                        # Count the number of images
                        file_count = len(
                            [name for name in os.listdir(folder_path) if name.lower().endswith(img_extensions)])
                        num_digits = len(str(file_count))  # Get the total digits required

                        new_filepath = os.path.join(
                            new_folder,
                            f"{name_extracted}{self.number_seperation}{str(file_counter).zfill(num_digits)}{ext}"
                        )
                        img.save(new_filepath)
                        file_counter += 1

                    else:
                        file_count = len(
                            [name for name in os.listdir(folder_path) if name.lower().endswith(img_extensions)])
                        num_digits = len(str(file_count))  # Get the total digits required

                        new_filepath = os.path.join(
                            new_folder,
                            f"{name_extracted}{self.number_seperation}{str(file_counter)}{ext}"
                        )
                        img.save(new_filepath)
                        file_counter += 1

        else:
            for filename in os.listdir(folder_path):  # Loop through all files in the directory
                if filename.lower().endswith(img_extensions):  # Check if the file is an image
                    img = Image.open(os.path.join(folder_path, filename))  # Open the image file
                    ext = os.path.splitext(filename)[1]
                    if self.first_digit == 0:
                        # Count the number of images
                        file_count = len(
                            [name for name in os.listdir(folder_path) if name.lower().endswith(img_extensions)])
                        num_digits = len(str(file_count))  # Get the total digits required

                        new_filepath = os.path.join(
                            new_folder,
                            f"{name_extracted}{self.number_seperation}{str(file_counter).zfill(num_digits)}{ext}"
                        )
                        img.save(new_filepath, dpi=(dpi_numeric, dpi_numeric))
                        file_counter += 1

                    else:
                        file_count = len(
                            [name for name in os.listdir(folder_path) if name.lower().endswith(img_extensions)])
                        num_digits = len(str(file_count))  # Get the total digits required

                        new_filepath = os.path.join(
                            new_folder,
                            f"{name_extracted}{self.number_seperation}{str(file_counter)}{ext}"
                        )
                        img.save(new_filepath, dpi=(dpi_numeric, dpi_numeric))
                        file_counter += 1

    def enable_options(self):
        """Enable the image processing options once the image directory has been selected."""
        self.dpi_instructions.setDisabled(False)
        self.dpi_combo.setDisabled(False)
        self.name_instructions.setDisabled(False)
        self.numbering_instructions.setDisabled(False)
        self.numbering_combo.setDisabled(False)
        self.project_name.setDisabled(False)
        self.btn_process.setDisabled(False)

    def enable_process(self):
        """Enable the Process button."""
        self.btn_process.setDisabled(False)

app = QApplication([])
window = MyApp()
window.show()
app.exec()