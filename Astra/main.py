import sys
import os
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog,QMainWindow,QInputDialog,QVBoxLayout
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.uic import loadUi
import pyttsx3
import speech_recognition as sr
import requests
import random
import io
from PIL import Image


import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
API = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxxxx"}
def R_query(payload):
    response = requests.post(API, headers=headers, json=payload)
    return response.content
def real_gen(text):
    image_bytes = R_query({
        "inputs": text,
    })
    image = Image.open(io.BytesIO(image_bytes))
    image_byt = io.BytesIO(image_bytes)
class TTS(QMainWindow):
    def __init__(self):
        super(TTS,self).__init__()
        loadUi("UIs\TTS.ui",self)
        self.setWindowTitle("Astra")
        self.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
        self.STT_but.clicked.connect(self.gotoSTT)
        self.TTI_but.clicked.connect(self.gotoTTI)
        self.ITT_but.clicked.connect(self.gotoITT)
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 50)
        self.pushButton_5.clicked.connect(lambda: self.speak(self.Input.toPlainText()))
        # self..clicked.connect(self,self.())
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Astra")
        self.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
    def gotoSTT(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoTTI(self):
        widget.setCurrentIndex(widget.currentIndex()+2)
    def gotoITT(self):
        widget.setCurrentIndex(widget.currentIndex()+3)
    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
class STT(QMainWindow):
    def __init__(self):
        super(STT,self).__init__()
        loadUi("UIs\STT.ui",self)
        self.setWindowTitle("Astra")
        self.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
        self.output.hide()
        self.status.hide()
        lay = QVBoxLayout(self)
        lay.addWidget(self.output)
        self.TTS_but.clicked.connect(self.gotoTTS)
        self.TTI_but.clicked.connect(self.gotoTTI)
        self.ITT_but.clicked.connect(self.gotoITT)
        self.Generate_Button_TTS.clicked.connect(self.listen)
    # index=1
    def listen(self):
        try:
            self.status.show()
            self.status.setText("Listening...")
            time.sleep(0.4)
            r = sr.Recognizer()
            # self.status.setText("Recognizer set")
            # device_index=2 fro one plus earbuds
            with sr.Microphone() as source:
                aud = r.listen(source)
                self.output.show()
                try:
                    said = r.recognize_google(aud)
                    self.status.setText("Completed!")
                    self.output.setText(said)
                except Exception as e:
                    self.output.setText('''Sorry , Unable to 
                                                listen carefully, try again''')
        except Exception as em:
            print(em)
    def gotoTTS(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
    def gotoTTI(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoITT(self):
        widget.setCurrentIndex(widget.currentIndex()+2)

class TTI(QMainWindow):
    def __init__(self):
        super(TTI,self).__init__()
        loadUi("UIs\TTI.ui",self)
        self.TTS_but.clicked.connect(self.gotoTTS)
        self.STT_but.clicked.connect(self.gotoSTT)
        self.ITT_but.clicked.connect(self.gotoITT)
        self.download_but.hide()
        self.setWindowTitle("Astra")
        self.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
        self.Download_status.hide()
        self.Generate_Button_TTS.clicked.connect(lambda: self.real_gen(self.prompt.toPlainText()))
        self.download_but.clicked.connect(self.downloadimg)
    def downloadimg(self):
        self.download_but.setText("downloaded !")
        self.image.save(f"Downloads/{self.prompt.toPlainText()+str(random.randint(1,1000))}.jpg")
        self.download_but.setText("Download")
    def R_query(self,payload):
        response = requests.post(API, headers=headers, json=payload)
        return response.content
    def real_gen(self,text):
        os.remove("Assets/cache/brahh.jpg")
        image_bytes = R_query({
            "inputs": text,
        })
        self.image = Image.open(io.BytesIO(image_bytes))
        image_byt = io.BytesIO(image_bytes)
        try:
            self.image.save("Assets/cache/brahh.jpg")
            self.Image_output.setText("Done brahh!!")
            time.sleep(1)
            pixmap = QPixmap("Assets/cache/brahh.jpg")
            self.Image_output.setPixmap(pixmap)
            self.download_but.show()
        except Exception as e:
            print(e)
    def gotoTTS(self):
        widget.setCurrentIndex(widget.currentIndex()-2)
    def gotoSTT(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
    def gotoITT(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class ITT(QMainWindow):
    def __init__(self):
        super(ITT,self).__init__()
        loadUi("UIs\ITT.ui",self)
        self.setWindowTitle("Astra")
        self.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
        self.TTS_but.clicked.connect(self.gotoTTS)
        self.STT_but.clicked.connect(self.gotoSTT)
        self.TTI_but.clicked.connect(self.gotoTTI)
        self.Upload_but.clicked.connect(self.UploadFile)
        self.Generate_Button_TTS.clicked.connect(self.gen_ITT)
    def gen_ITT(self):
        output_text = query(filename=self.filename[0])
        self.TextOutput_ITT.setText(output_text[0]["generated_text"])
    def UploadFile(self):
        self.filename = QFileDialog.getOpenFileName()
        pixmap = QPixmap(self.filename[0])
        self.Image_Box_ITT.setPixmap(pixmap)
    # index=3
    def gotoTTS(self):
        widget.setCurrentIndex(widget.currentIndex()-3)
    def gotoSTT(self):
        widget.setCurrentIndex(widget.currentIndex()-2)
    def gotoTTI(self):
        widget.setCurrentIndex(widget.currentIndex()-1)


app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=TTS()
stt = STT()
tti=TTI()
itt = ITT()
widget.addWidget(mainwindow)
widget.addWidget(stt)
widget.addWidget(tti)
widget.addWidget(itt)
widget.setFixedWidth(201+731)
widget.setFixedHeight(581)
widget.setWindowTitle("Astra")
widget.setWindowIcon(QIcon("Assets/Icon/icon.jpg"))
widget.show()
sys.exit(app.exec_())