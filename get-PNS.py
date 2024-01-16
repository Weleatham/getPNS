#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 2024

Program created to download the latest PNS data from the NWS and surrounding 
offices specified.

@author: Bill Leatham
"""
import requests, sys
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QDialog
from PyQt5.QtCore import QTimer

versions = map(str, range(1, 21, 1))

class SelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize variables to store selected options
        self.selected_option1 = None
        self.selected_option2 = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label1 = QLabel("Select option 1:")
        combo_box1 = QComboBox()
        combo_box1.addItems(["ALL", "ALY", "BOX", "GYX", "OKX"])

        label2 = QLabel("Select option 2:")
        combo_box2 = QComboBox()
        combo_box2.addItems(versions)

        enter_button = QPushButton("Enter")
        enter_button.clicked.connect(self.on_enter_button_clicked)

        layout.addWidget(label1)
        layout.addWidget(combo_box1)
        layout.addWidget(label2)
        layout.addWidget(combo_box2)
        layout.addWidget(enter_button)

        self.setLayout(layout)

        self.setWindowTitle("Selection Widget")
        self.show()

    def on_enter_button_clicked(self):
        # Get the selected options and store them in instance variables
        self.selected_option1 = self.layout().itemAt(1).widget().currentText()
        self.selected_option2 = self.layout().itemAt(3).widget().currentText()
        # Show "Program Completed" message in another window
        completion_dialog = CompletionDialog()
        completion_dialog.exec_()

        # After clicking "Enter", call the main function with the selected options
        main(self.selected_option1, self.selected_option2)

        # Close the application after clicking "Enter"
        self.close()
        #QApplication.instance().close()

    def get_selected_options(self):
        # Method to retrieve the selected options
        return self.selected_option1, self.selected_option2

class CompletionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        message_label = QLabel("Program Completed")
        layout.addWidget(message_label)

        self.setLayout(layout)
        self.setWindowTitle("Completion Dialog")

        # Use QTimer to close the dialog after 10 seconds
        timer = QTimer(self)
        timer.timeout.connect(self.close_dialog)
        timer.start(1000)  # 2000 milliseconds = 2 seconds

    def close_dialog(self):
        self.close()

def url_request(url):
    # Making the request for the data.
    req = requests.get(url)
    # Only give us the data if the status code is successful.
    if req.status_code != 200:
        print("There was an issue")
    else:
        # Giving the data if the data request
        return req.content

def main(loc, num):
    sites = ["BOX", "ALY", "GYX", "OKX"]
    if loc == "ALL":
        for site in sites:
            base_url = f'https://forecast.weather.gov/product.php?site=NWS&issuedby={site}' \
                       f'&product=PNS&format=CI&version={num}&glossary=1&highlight=off'
            data = url_request(base_url)
            soup = BeautifulSoup(data, 'html.parser')
            ds = soup.find(attrs={"class": "glossaryProduct"}).get_text()[1:]
            with open(f'PNS{site}.txt', 'w') as file:
                file.write(ds[:-2])
    else:
        base_url = f'https://forecast.weather.gov/product.php?site=NWS&issuedby={loc}' \
                   f'&product=PNS&format=CI&version={num}&glossary=1&highlight=off'
        data = url_request(base_url)
        soup = BeautifulSoup(data, 'html.parser')
        ds = soup.find(attrs={"class": "glossaryProduct"}).get_text()[1:]
        with open(f'PNS{loc}.txt', 'w') as file:
            file.write(ds[:-2])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectionWidget()
    sys.exit(app.exec_())