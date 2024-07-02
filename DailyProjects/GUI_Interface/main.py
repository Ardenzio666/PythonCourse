import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel


class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Enter text: ", self)
        self.layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        self.layout.addWidget(self.textbox)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Simple CSV Appender")
        self.show()

    def on_submit(self):
        text = self.textbox.text()
        if text:
            with open('csv_file/output.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow([text])
            self.textbox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    sys.exit(app.exec())








