from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import pafy
import threading
import time
from Designer import Ui_Form


class Pencere(QMainWindow,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        # Video ve ses seçenekli radio butonları olıuşturuyoruz.
        self.radio1.toggled.connect(self.comboyutemizle)
        self.radio1.toggled.connect(self.videocozunurluk)
        # --------------------------------------------------
        self.radio2.toggled.connect(self.comboyutemizle)
        self.radio2.toggled.connect(self.sescozunurluk)
        # Dosyanın kaydetme konumu için gereklilerin oluşturulması
        self.kaydet.setReadOnly(True)
        # =======Kaydet Butonu İçin========#
        self.kaydetB.clicked.connect(self.konumisi)
        self.kaydetB.clicked.connect(self.kaydett)
        self.kaydetB.setEnabled(False)
        # Video İndirme Butonu Oluşturma
        self.indirme.clicked.connect(self.startDownloadThread)
        self.indirme.setEnabled(False)
        # Ses İndirme butonu
        self.indirme2.clicked.connect(self.start2)
        self.indirme2.setEnabled(False)

        self.show()

    def comboyutemizle(self):
        self.cozunurluk.clear()

    def startDownloadThread(self):
        th = threading.Thread(target=self.videoyuindirme, daemon=True)
        th.start()

    def start2(self):
        th = threading.Thread(target=self.sesindir, daemon=True)
        th.start()
    def tamamlandi(self):
        if self.cubuk.value() == 100:
            self.error = QMessageBox(self)
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("Uyarı")
            self.error.setText("İndirme Tamamlandı")
            x = self.error.exec_()

    def progress(self, total, recvd, ratio, rate, eta):
        self.cubuk.setValue(ratio * 100)
    def sescozunurluk(self):
        a = self.url.text()
        b = a.startswith('https://www.youtube.com/watch?v=') == False
        if self.radio2.isChecked():
            if b:
                self.error = QMessageBox(self)
                self.error.setIcon(QMessageBox.Critical)
                self.error.setWindowTitle("Hata")
                self.error.setText(
                    " Url alanı boş veya hatalı url.!!\n Lütfen url'i 'https://www.youtube.com/watch?v=' formatında girin.!!")
                x = self.error.exec_()
            else:
                if self.radio2.isChecked():
                    self.indirme.setEnabled(False)
                    self.indirme2.setEnabled(False)
                    self.kaydetB.setEnabled(True)

                    liste = []
                    url = self.url.text()
                    ses = pafy.new(url)
                    streams = ses.getbestaudio()
                    f = 1024 * 1024
                    t = (streams.get_filesize() / f)
                    a = 'Ses dosyası ' + str(round(t, 2)) + " MB  --> " + str(streams.title)
                    self.cozunurluk.addItem(a)

    def videocozunurluk(self):
        a = self.url.text()
        b = a.startswith('https://www.youtube.com/watch?v=') == False
        if self.radio1.isChecked():
            if b:
                self.error = QMessageBox(self)
                self.error.setIcon(QMessageBox.Critical)
                self.error.setWindowTitle("Hata")
                self.error.setText("Url alanı boş veya hatalı url.!!")
                x = self.error.exec_()
            else:
                if self.radio1.isChecked():
                    self.indirme2.setEnabled(False)
                    self.indirme.setEnabled(False)
                    self.kaydetB.setEnabled(True)

                    liste = []
                    url = self.url.text()
                    video = pafy.new(url)
                    streams = video.streams
                    f = 1024 * 1024
                    for i in streams:
                        t = (i.get_filesize() / f)
                        a = i.resolution + 'p -- ' + str(round(t, 2)) + " MB"
                        liste.append(a)
                        for i in liste:
                            self.cozunurluk.addItem(str(i))
                    self.cozunurluk.removeItem(0)

    def kaydett(self):
        if self.radio1.isChecked():
            self.indirme.setEnabled(True)
            self.indirme2.setEnabled(False)

        elif self.radio2.isChecked():
            self.indirme2.setEnabled(True)

            self.indirme.setEnabled(False)

    def sesindir(self):
        if self.radio2.isChecked():
            url = self.url.text()
            ses = pafy.new(url)
            a = ses.getbestaudio()
            y = self.kaydet.text()
            out_file = a.download(y, callback=self.progress)
            for filename in os.listdir(y):
                infilename = os.path.join(y, filename)
                if not os.path.isfile(infilename): continue
                oldbase = os.path.splitext(filename)
                newname = infilename.replace('.webm', '.mp3')
                output = os.rename(infilename, newname)

    def videoyuindirme(self):
        a = self.url.text()
        if self.url.text() == '':
            self.error = QMessageBox(self)
            self.error.setIcon(QMessageBox.Critical)
            self.error.setWindowTitle("Hata")
            self.error.setText("Url alanı boş olamaz.!")
            x = self.error.exec_()
        else:
            url = self.url.text()
            video = pafy.new(url)
            streams = video.streams
            index = self.cozunurluk.currentIndex()
            if str(index) == "0":
                streams[0].download(filepath=self.kaydet.text(), callback=self.progress)
            elif str(index) == "1":
                streams[1].download(filepath=self.kaydet.text(), callback=self.progress)
            elif str(index) == "2":
                streams[2].download(filepath=self.kaydet.text(), callback=self.progress)
    

    def konumisi(self):
        fpath = QFileDialog.getExistingDirectory(self)
        self.kaydet.setText(fpath)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    pencere = Pencere()
    pencere.show()
    sys.exit(app.exec_())
