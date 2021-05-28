# -*- coding: utf-8 -*- 
import maya.mel as mel
import maya.OpenMaya as om
import re
from maya import OpenMaya, cmds
import maya.cmds as cmds
import pymel.core as pm
import os
import sys
import maya.OpenMayaUI as MayaUI

from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance

import xml.etree.ElementTree as ET





##!--------------------------------------------------------------------------------------------------------------------------
# [UI]

## 버튼 눌렀을 경우 위젯 숨기기
class FrameLayout(object):
 
    def __init__(self, titleBar, frame):
        self.titleBar = titleBar    # 위의 버튼 위젯
        self.frame = frame          # 개폐하는 위젯
        self.collapse = True       # 개폐 상태 플래그
        self.setSignals()           # 신호를 세트
 
    #-------------------------------------------------------------------------
    ## 신호를 설정
    def setSignals(self):
        self.titleBar.clicked.connect(self.setCollapse)
 
    #-------------------------------------------------------------------------
    ## 프레임을 개폐하는 액션
    def setCollapse(self):
        # 현재의 상태를 반전
        self.collapse = not self.collapse
        # 프레임의 비지빌리티를 변경하다
        self.frame.setHidden(self.collapse)
 
        # 개폐 상황에 맞게 애로우 타입을 변경하다
        if self.collapse:
            # 닫혀있을 때
            self.titleBar.setArrowType(QtCore.Qt.RightArrow)
        else:
            # 열려 있을 때
  
            self.titleBar.setArrowType(QtCore.Qt.DownArrow)


def getMayaWindow():
    #MayaUI.MQtUtil.mainWindow()
    ptr = MayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QWidget)
    


class RIG_check_tool_window(QtCore.QObject):
    #def __init__(self, tap):
    def __init__(self):
        self.PATH = "D:/KJY/python/sub_script/RIG_check_tool"
        self.ui_path = "D:/KJY/python/sub_script/RIG_check_tool/RIG_check_tool_UI.ui"
        #maya_main = shiboken.wrapInstance(long(MayaUI.MQtUtil.mainWindow()), QtGui.QWidget)
        super(RIG_check_tool_window, self).__init__(getMayaWindow()) # maya main window parent
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


        self.ui.key_test_btn.clicked.connect(pm.Callback( self.printCurrentItem))
        


    def printCurrentItem(self) :
        print(self.ui.listWidget_Test.currentItem().text()) #리스트위젯에서 선택했을때