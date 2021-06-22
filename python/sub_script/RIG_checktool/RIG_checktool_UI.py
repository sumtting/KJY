# -*- coding: utf-8 -*- 



from maya import OpenMaya, cmds
import maya.cmds as cmds


import sys
import maya.OpenMayaUI as MayaUI

from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance

import xml.etree.ElementTree as ET




from RIG_checktool_command import *
import RIG_checktool_command
import RIG_checktool_json







##!--------------------------------------------------------------------------------------------------------------------------
# [UI]

def getMayaWindow():
    #MayaUI.MQtUtil.mainWindow()
    ptr = MayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QWidget)
    


class RIG_checktool_window(QtCore.QObject):
    #def __init__(self, tap):
    def __init__(self):
        self.PATH = "D:/KJY/python/sub_script/RIG_checktool"
        self.ui_path = "D:/KJY/python/sub_script/RIG_checktool/RIG_checktool_UI.ui"
        #maya_main = shiboken.wrapInstance(long(MayaUI.MQtUtil.mainWindow()), QtGui.QWidget)
        super(RIG_checktool_window, self).__init__(getMayaWindow()) # maya main window parent
        # Remove previous window
        # TODO: Delete window without title.
        doc = ET.parse(self.ui_path)
        root = doc.getroot()
        result = {}
        for child in root:
            result[child.tag] = child.attrib
        get_window = result.get('widget').get('name')

        
        if cmds.window(get_window, exists=True):
            cmds.deleteUI(get_window)

        # ui file load
        ui_loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)

        # create widget from ui file
        self.ui = ui_loader.load(ui_file, getMayaWindow()) # self == maya main window parent
        ui_file.close()

        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)          
        self.ui.show()

#----------------------------------------------------------------------------------------------

        self.listwidget_addItem()


        self.ui.key_check_btn.clicked.connect(self.UI_listWidget_menu)


        self.ui.key_clear_btn.clicked.connect(self.key_clear_load)


        self.ui.final_check_btn.clicked.connect(self.final_check_load)


        self.ui.action_json_manager.triggered.connect(self.json_manager_load)

        
    reload (RIG_checktool_command)
    reload (RIG_checktool_json)


    def listwidget_addItem(self): # UI 리스트위젯에 add item
        json_list = RIG_checktool_command.folderlist(json_path) # folderlist 함수 쿼리(json_path 경로 폴더에있는 파일 모두 추출)
        
        for json_ in json_list:
            json_ = json_.split('.')[0]
            if json_ == 'ani_CTL_list': #ani_CTL_list는 컨트롤러 리스트이므로 제외
                pass
            else:
                self.ui.RIG_check_listWidget.addItem(json_)
                # if "body" in json_:
                #     self.ui.RIG_check_listWidget.insertItem(1,json_) # json_path 경로 폴더에 있는 파일들을 add item
                
                # elif "facial" in json_:
                #     self.ui.RIG_check_listWidget.insertItem(4,json_) # json_path 경로 폴더에 있는 파일들을 add item

                # elif "cycle" in json_:
                #     self.ui.RIG_check_listWidget.insertItem(7,json_) # json_path 경로 폴더에 있는 파일들을 add item 

       
    def UI_listWidget_menu(self) : # UI 리스트위젯 item에 연결된 함수
        RIG_checktool_command.key_clear(ani_CTL_list)
        select_ = (self.ui.RIG_check_listWidget.currentItem().text()) #리스트위젯에서 item 선택
        
        RIG_checktool_command.load_json_setkey(select_)

            
    def key_clear_load(self):
        RIG_checktool_command.key_clear(ani_CTL_list)


    def final_check_load(self):
        RIG_checktool_command.matchname_set()
        RIG_checktool_command.unused_node()


    def json_manager_load(self):
        RIG_checktool_json.RIG_checktool_Json_manager()






  








    