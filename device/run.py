import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import  QUrl,QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
from Model import *
from APIFetch import APIFetcher
from Repository import *
from SensorHelper import SensorHelper
from BluetoohHelper import BluetoothHelper
import sys
import asyncio

from datetime import datetime


form_class = uic.loadUiType("untitled.ui")[0]
formRounteInfoClass = uic.loadUiType("untitled2.ui")[0]

modelHelper = ModelHelper()
terminalRepository =TerminalRepository(modelHelper=modelHelper)
positionRepository = PositionRepository(modelHelper=modelHelper)
terminalNumber = terminalRepository.findById(1).getTerminalNumber()
apiFetcher = APIFetcher(terminalNumber)


class ObserverInterface():
    def notify(self,*args,**kwargs):
        pass


class Provider:

    def __init__(self):
        self.__observers = []

    def register(self,observer:ObserverInterface):
        self.__observers.append(observer)

    def notifyAll(self,*args,**kwargs):
        for observer in self.__observers:
            observer.notify(*args,**kwargs)



class PositionThread(QThread,Provider):
    positionUploadEvent = pyqtSignal(RMCPosition)
    def run(self):
        sensorReceiver = SensorHelper().getSensorReceiver()
        while True:
            try:
                position = sensorReceiver.getPosition()
                self.notifyAll(position=position)
            except Exception as e:
                pass

    def stop(self):
        self.terminate()


class BluetoothThread(QThread,Provider):
    def __init__(self):
        super().__init__()
        self.bluetoothHelper = BluetoothHelper()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_run())

    async def async_run(self):
        while True:
            beaconUUIDList = await self.bluetoothHelper.getBeaconUUIDList()
            self.notifyAll(beaconUUIDList=beaconUUIDList)
 


class PositionSaver(ObserverInterface):
    def __init__(self):
        modelHelper = ModelHelper()
        self.positionRepository = PositionRepository(modelHelper=modelHelper)

    def notify(self,*args,**kwargs):
        position = kwargs.get("position",None)
        if(not position):
            return
        latitude = position.getLatitude()
        longitude = position.getLongitude()
        speed = position.getSpeed()
        apiFetcher.uploadPosition(position)
        entity = Position(latitude=latitude,longitude=longitude,speed=speed,time=datetime.now())
        self.positionRepository.save(entity)


class MainWindow(QMainWindow, form_class,ObserverInterface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.close)
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://device.littleriders.co.kr"))
        self.mapLayout.addWidget(self.webview)
        self.webview.loadFinished.connect(self.on_load_finished)
        self.mapLoad = False


    def on_load_finished(self, success):
        if success:
            self.mapLoad = True
            self.webview.page().runJavaScript('console.log("helloworld")')

    def terminalInfoButtonEvent(self):
        pass
    def courseInfoButtonEvent(self):
        print(apiFetcher.getRouteList())
        self.hide()
        self.second = RouteInfoWindow()
        self.second.exec()
        self.show()


        #routeList = apiFetcher.getRouteList()
        #self.uuidText.setText(json.dumps(routeList,ensure_ascii=False,indent=4))

    def notify(self,*args,**kwargs):
        position = kwargs.get("position",None)
        if(not position):
            return
        position = kwargs["position"]
        latitude = position.getLatitude()
        longitude = position.getLongitude()
        speed = position.getSpeed()
        if(self.mapLoad):
            self.webview.page().runJavaScript(f'change({latitude},{longitude})')
        self.latitudeText.setText(f"{latitude}")
        self.longitudeText.setText(f"{longitude}")
        self.speedText.setText(f"{speed}")


class RouteInfoListWidget(QListWidgetItem):
    def __init__(self,data=None,parent=None):
        super().__init__("",parent)
    
        self.id = data["id"]
        self.name = data["name"]
        self.setText(self.name)
        self.setFont(QFont("Arial",23))
        # su.__init__(parent)

    def getId(self):
        return self.id

class RouteInfoWindow(QDialog,QWidget,formRounteInfoClass):

    def __init__(self):
        super(RouteInfoWindow,self).__init__()
        self.setupUi(self)

        self.routeList = apiFetcher.getRouteList()
        for i in self.routeList:
            print(i)
            self.addItem(i)
        self.show()

    def addItem(self,data):
        item = RouteInfoListWidget(data=data)
        self.courseListWidget.addItem(item)

    def clickItem(self,items):
        print(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    
    positionSaver = PositionSaver()
    postionThread = PositionThread()
    postionThread.start()
    postionThread.register(win)
    postionThread.register(positionSaver)

    bluetoothThread = BluetoothThread()
    bluetoothThread.start()

    
    win.show()
    app.exec()