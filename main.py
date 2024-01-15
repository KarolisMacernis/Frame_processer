import sys
import os
import re
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QFileDialog, QLabel, QSizePolicy, QFormLayout, QComboBox, QMainWindow, QMessageBox
import PyQt6.QtWidgets as qtw
from PIL import Image

class MyApp(QWidget):

    def __init__(self):
        """Setup the widgets in the GUI interface."""
        super().__init__()

        self.setWindowTitle('Frame processer')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setup_directory_button()
        self.setup_directory_label()

        self.setup_dpi_instructions()
        self.setup_dpi_options()
        self.setup_numbering_instructions()
        self.setup_numbering_options()
        self.setup_name_instructions()
        self.setup_name_input()
        self.setup_form_layout()

        self.setup_process_button()

    def setup_directory_button(self):
        """Create a button to choose the project directory."""
        self.directory_button = QPushButton('Choose Image Directory')
        self.layout.addWidget(self.directory_button)
        self.directory_button.clicked.connect(self.choose_directory)
        self.directory_button.setMinimumSize(270, 47)
        self.directory_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_directory_label(self):
        """Create an output label that will show the chosen directory once the user has selected it."""
        self.directory_label = QLabel('Selected path:   None')
        self.layout.addWidget(self.directory_label)
        self.directory_label.setMinimumHeight(50)
        self.directory_label.setWordWrap(True)
        self.directory_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_dpi_instructions(self):
        """Create a label with instructions to choose the resolution of the images (dots per inch)."""
        self.dpi_instructions = QLabel('Select the resolution for the images:')
        self.dpi_instructions.setDisabled(True)
        self.dpi_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_dpi_options(self):
        """Create a dropdown list to choose the resolution of the images."""
        self.dpi_options = qtw.QComboBox(self)
        self.dpi_options.addItem("Use original")
        self.dpi_options.addItem("Set to 600 dpi")
        self.dpi_options.addItem("Set to 300 dpi")
        self.dpi_options.addItem("Set to 150 dpi")
        self.dpi_options.addItem("Set to 75 dpi")
        self.dpi_options.setDisabled(True)
        self.dpi_options.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_numbering_instructions(self):
        """Create a label with instructions to choose the numbering for the images."""
        self.numbering_instructions = QLabel('Choose the numbering for the images:')
        self.numbering_instructions.setDisabled(True)
        self.numbering_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_numbering_options(self):
        """Create a dropdown list to choose the numbering of the images."""
        self.numbering_options = qtw.QComboBox(self)
        self.numbering_options.addItem("_1, _2, ...")
        self.numbering_options.addItem("-1, -2, ...")
        self.numbering_options.addItem("_01, _02, ...")
        self.numbering_options.addItem("-01, -02, ...")
        self.numbering_options.setDisabled(True)
        self.numbering_options.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_name_instructions(self):
        """Create a label with instructions to enter the project name."""
        self.name_instructions = QLabel('Enter name of the project:')
        self.name_instructions.setDisabled(True)
        self.name_instructions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_name_input(self):
        """Create an input box for entering the name of the project."""
        self.project_name = QLineEdit()
        self.project_name.setDisabled(True)
        self.project_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_form_layout(self):
        """Create a form layout to input the project name, frame numbering and the resolution."""
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        self.form_layout.addRow(self.dpi_instructions, self.dpi_options)
        self.form_layout.addRow(self.numbering_instructions, self.numbering_options)
        self.form_layout.addRow(self.name_instructions, self.project_name)

    def setup_process_button(self):
        """
        Create a "Process" button and connect it with the functions used for processing the images and creating the
        output folder.
        """
        self.process_button = QPushButton('Process')
        self.process_button.setMinimumSize(270, 47)
        self.layout.addWidget(self.process_button)
        self.process_button.setDisabled(True)
        self.process_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.process_button.clicked.connect(self.process_images)

    def choose_directory(self):
        """Choose the directory of the project folder and enable the "Process" button once done."""
        self.folder_name = QFileDialog.getExistingDirectory()
        self.directory_label.setText(f"Selected path:   {self.folder_name}")  # Set the label to the chosen folder
        # directory.
        self.enable_options()

    def create_new_folder(self, folder_path):
        """Create a new folder for the processed images."""
        new_folder = os.path.join(folder_path, "Adjusted Images")
        if not os.path.exists(new_folder):  # Create the directory if it doesn't exist.
            os.mkdir(new_folder)
        return new_folder

    def extract_dpi_value(self):
        """Extract the numeric dpi value from the option chosen by the user."""
        chosen_dpi = self.dpi_options.currentText()
        if chosen_dpi != "Use original":
            dpi_numeric = int(''.join(c for c in chosen_dpi if c.isdigit()))  # extract the numeric dpi value.
            return dpi_numeric

    def create_new_filename(self, file_counter, ext, file_count):
        """Create a new filename for the images based on the file counter, extension, and total file count."""
        extracted_name = self.project_name.text()
        num_digits = len(str(file_count))
        chosen_numbering = self.numbering_options.currentText()
        separator = chosen_numbering[0]
        first_digit = int(chosen_numbering[1])
        new_filename = (
            f"{extracted_name}{separator if extracted_name != '' else ''}"
            f"{str(file_counter).zfill(num_digits) if first_digit == 0 else str(file_counter)}"
            f"{ext}"
        )
        return new_filename

    def process_images(self):
        """Adjust and save the images to the created folder."""
        folder_path = self.folder_name
        new_folder = self.create_new_folder(folder_path)

        dpi_numeric = self.extract_dpi_value()

        file_counter = 1  # Index of the image

        img_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")

        # Get the count of the images in the selected folder.
        file_count = len([name for name in os.listdir(folder_path) if name.lower().endswith(img_extensions)])

        for filename in os.listdir(folder_path):  # Loop through all files in the directory.
            if filename.lower().endswith(img_extensions):  # Check if the file is an image.
                img = Image.open(os.path.join(folder_path, filename))  # Open the image file.
                ext = os.path.splitext(filename)[1]  # Get the extension of the current image being processed.

                # Create the new filename using the function create_new_filename and input the extension of the image
                # being processed, its index and the total count of images in the selected folder as the parameters
                # of the function.
                new_filename = self.create_new_filename(file_counter, ext, file_count)

                # Create the complete filepath for the new image to be created.
                new_filepath = os.path.join(new_folder, new_filename)

                # Save the image in the defined filepath. Use the new resolution if the user has selected the option
                # to change the dpi setting.
                if dpi_numeric == None:
                    img.save(new_filepath)
                else:
                    img.save(new_filepath, dpi=(dpi_numeric, dpi_numeric))

                file_counter += 1

        QMessageBox.information(self, 'Info', 'Processing finished')

    def enable_options(self):
        """Enable the image processing options once the image directory has been selected."""
        self.dpi_instructions.setDisabled(False)
        self.dpi_options.setDisabled(False)
        self.numbering_instructions.setDisabled(False)
        self.numbering_options.setDisabled(False)
        self.name_instructions.setDisabled(False)
        self.project_name.setDisabled(False)

        self.process_button.setDisabled(False)

app = QApplication([])
window = MyApp()
window.show()
app.exec()