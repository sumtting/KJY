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

 
        self.ui.RIG_check_btn.clicked.connect(self.UI_listWidget_menu)


        self.ui.key_clear_btn.clicked.connect(self.key_clear_load)
       


    reload (RIG_checktool_command)



    def UI_listWidget_menu(self) :
        RIG_checktool_command.key_clear(body_CTL_list)
        select_ = (self.ui.RIG_check_listWidget.currentItem().text()) #리스트위젯에서 선택했을때
        
        if select_ == 'body_test':
            RIG_checktool_command.load_json_setkey('body_test_json')

        elif select_ == 'hand_test':
            print "Not implemented"

        elif select_ == 'facial_test':
            print "Not implemented"

        elif select_ == 'walk_cycle':
            RIG_checktool_command.load_json_setkey('walk_cycle_json')

        elif select_ == 'run_cycle':
            print "Not implemented" 

  









    def key_clear_load(self):
        RIG_checktool_command.key_clear(body_CTL_list)