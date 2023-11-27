import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel
from pathlib import Path

# class RenameImages:
#
#     def __init__(self, path):
#         """Rename the images according to the name of the project and the chosen numbering"""
#
#         # Change the working directory to the folder chosen by the user and convert it to a Path object.
#         folder_path = (window.output_label.text())
#
#         print(folder_path)
#
#         # os.chdir(Path(folder_path))
#
#         # Assign a path variable to the current working directory.
#         # path = os.getcwd()
#
#         # Get the tail of the path (which will give us only the name of the chosen folder) and assign a image_folder
#         # variable to it.
#         # image_folder = os.path.basename(path)
#
#         # print(path)
#
#         # os.chdir('./Visuals')
#         #
#         # render_file_number = 0
#         #
#         # global render_file_path
#         #
#         # for render_file in os.listdir():
#         #     render_name, ext = os.path.splitext(render_file)
#         #     render_file_number += 1
#         #     new_render_name = f"{project_name}_{render_file_number}{ext}"
#         #     render_file_path = ('./' + new_render_name)
#         #     if os.path.isfile(render_file_path):
#         #         continue
#         #     else:
#         #         os.rename(render_file, new_render_name)
#         #
#         # render_name_no_number = f"{project_name}{ext}"
#         #
#         # # Remove the numbering if there is only one file.
#         # if render_file_number == 1:
#         #     os.rename(new_render_name, render_name_no_number)
# 
# Karolis = RenameImages('users/john/folder')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Frame processer')
        self.resize(500, 350) # width, height

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputField = QLineEdit()
        button = QPushButton()
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)

        # Create an output label that will show the chosen directory once the user has selected it.
        output_label = QLabel('')
        layout.addWidget(output_label)
        output_label.setMinimumHeight(40)

# app = QApplication([])
app = QApplication(sys.argv)
app.setStyleSheet('''
    QWidget {
        font-size: 25px;
    }

    QPushButton {
        font-size: 20px;
    }
''')

window = MyApp()
window.show()

app.exec()