import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
from matplotlib import pyplot as plt
import sqlite3


class Storage_Ui():
    path = None

    def __init__(self, relative_path=None):
        Storage_Ui.path = relative_path
        self.ui = uic.loadUi(self.path + "storage.ui")
        self.ui.setLayout(self.ui.layout1)
        self.list1 = [0 for i in range(60)]
        self.t = int(time.time() * 10) % 90

    def old_storage_change_text(self):
        for i in range(1, 19):
            # self.win6.data1.setText("11111")

            str1 = str(i) + "." + "%02d" % (int(time.time() * 10) % 100)  # 时间

            eval("self.ui.data%d.setText(\"%s\")" % (i, str1))

            # print(i)

    def storage_change_text(self):
        self.t = int(time.time() * 10) % 90
        self.pic1()
        image = QImage(self.path + "pictures/storage_pic1.jpg")
        image.scaled(self.ui.PHOTO.size())
        spic1 = QPixmap(image)
        self.ui.PHOTO.setPixmap(spic1)
        self.ui.PHOTO.setScaledContents(True)
        self.read_data_to_text()

    def pic1(self):
        fig, ax = plt.subplots(figsize=(4.80, 3.87))
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        a = min(max(self.t, 15), 45) - 15
        # print(df)
        ax.set_xlabel("t(s)")
        ax.set_ylabel("Power(kW)")
        ax.set_title("Storage_system")
        plt.ylim(-15, 15)
        for i in range(60):
            self.list1[i] = 0
            self.list1[i] -= df["loadkW"][i + a] / 20
            self.list1[i] += df["windkW"][i + a] / 20
            self.list1[i] += df["photokW"][i + a] / 20
        ax.plot([i for i in range(a, a + 60)], self.list1)
        ax.plot([self.t], [self.list1[self.t - a]], color="red", marker="o")
        plt.savefig(self.path + "pictures/storage_pic1.jpg")
        plt.close()

    def read_data_to_text(self):
        b = min(max(self.t, 15), 45) - 15
        a = self.t - b
        conn = sqlite3.connect("data/data_db.db")
        query = "SELECT * FROM dataTable"
        df = pd.read_sql_query(query, conn)
        data_column = [0, 500.90, 2.30, 00.00, 100.00, 100.00, 30, 530.65, 229.65, 0.65, 3.00, 1.00, 30, 2.34, 2.26,
                       26.5, 24.00, 99, 97]

        self.ui.data3.setText("%.2f" % self.list1[a])
        self.ui.data2.setText("%.2f" % (self.list1[a] / 2))
        for i in range(1, 19):
            if i == 3 or i == 2: continue
            eval("self.ui.data%d.setText(\"%.2f\")" % (i, data_column[i]))