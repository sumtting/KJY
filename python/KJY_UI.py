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


import Rig_command
import External_command
import Asset_command
import Set_command
import Body_command




reload(Rig_command)
reload(External_command)
reload(Asset_command)
reload(Set_command)
reload(Body_command)





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
    


class KJY_window(QtCore.QObject):
    #def __init__(self, tap):
    def __init__(self):
        self.PATH = "D:/KJY/python"
        self.ui_path = "D:/KJY/python/KJY_UI.ui"
        #maya_main = shiboken.wrapInstance(long(MayaUI.MQtUtil.mainWindow()), QtGui.QWidget)
        super(KJY_window, self).__init__(getMayaWindow()) # maya main window parent
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




       # self.ui.btn_1.clicked.connect(pm.Callback( self.opener_command))
        #self.ui.chbox.clicked.connect(pm.Callback( self.ch_box))





##!--------------------------------------------------------------------------------------------------------------------------
#KJY_UI에 있는 버튼들과 함수를 연결
# [rig]

        self.ui.rename_btn.clicked.connect(pm.Callback( self.rename_load))
        self.ui.jnt_on_btn.clicked.connect(pm.Callback( self.joint_on_off_load, 0))
        self.ui.jnt_off_btn.clicked.connect(pm.Callback( self.joint_on_off_load, 2))
        self.ui.jnt_ps_btn.clicked.connect(pm.Callback( self.jnt_ps_load))
        self.ui.constraint_copy_btn.clicked.connect(pm.Callback( self.constraint_copy_load))
        self.ui.LR_copy_btn.clicked.connect(pm.Callback( self.LR_copy_load))
        self.ui.motionpath_cv_btn.clicked.connect(pm.Callback( self.motionpath_cv_load))

        
        

## --------------------------------------------------------------------------------------------------------------------------
# [move]

        self.ui.AtoB_btn.clicked.connect(pm.Callback( self.AtoB_BtoA_load))
        self.ui.AtoBpv_btn.clicked.connect(pm.Callback( self.AtoB_BtoA_copy_pivot_load))
        


## --------------------------------------------------------------------------------------------------------------------------
# [ctrl]

        self.ui.offGRP_btn.clicked.connect(pm.Callback( self.offGRP_load))
        self.ui.object_grp_btn.clicked.connect(pm.Callback( self.object_grp_load))
        self.ui.position_copy_btn.clicked.connect(pm.Callback( self.position_copy_load))

        self.ui.RX_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'rotate',True,False,False)) # 선택한 curve의 cv를 x축 rotate한다.
        self.ui.RY_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'rotate',False,True,False)) # 선택한 curve의 cv를 y축 rotate한다.
        self.ui.RZ_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'rotate',False,False,True)) # 선택한 curve의 cv를 z축 rotate한다.
        self.ui.SX_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'scale',True,False,False)) # 선택한 curve의 cv를 x축 scale한다.
        self.ui.SY_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'scale',False,True,False)) # 선택한 curve의 cv를 y축 scale한다.
        self.ui.SZ_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'scale',False,False,True)) # 선택한 curve의 cv를 z축 scale한다.
        self.ui.SXYZ_btn.clicked.connect(pm.Callback( self.curve_vtx_ro_sc_load,'scale',True,True,True)) # 선택한 curve의 cv를 xyz축 scale한다.



## --------------------------------------------------------------------------------------------------------------------------
# [skin]

        self.ui.bind_skin_copy_btn.clicked.connect(pm.Callback( self.bind_skin_copy_load))
        self.ui.skin_copy_many_btn.clicked.connect(pm.Callback( self.skin_copy_many_load))
        self.ui.rewei_btn.clicked.connect(pm.Callback( self.rewei_load))
        self.ui.reference_copy_btn.clicked.connect(pm.Callback( self.reference_copy_load))
        self.ui.ngskin_tool_btn.clicked.connect(pm.Callback( self.ngskin_tool_load))



## --------------------------------------------------------------------------------------------------------------------------
# [blend]

        self.ui.blend_copy_btn.clicked.connect(pm.Callback( self.blend_copy_load))



## --------------------------------------------------------------------------------------------------------------------------
# [select]

        self.ui.skin_jnt_select_btn.clicked.connect(pm.Callback( self.skin_jnt_select_load))
        self.ui.jnt_hierarchy_btn.clicked.connect(pm.Callback( self.jnt_hierarchy_load))
        self.ui.same_vtx_set_btn.clicked.connect(pm.Callback( self.same_vtx_set_load))  
        self.ui.geo_of_jnt_btn.clicked.connect(pm.Callback( self.geo_of_jnt_load))        
      


## --------------------------------------------------------------------------------------------------------------------------
# [follicle]

        self.ui.one_follicle_btn.clicked.connect(pm.Callback( self.one_follicle_load))
        self.ui.many_follicle_btn.clicked.connect(pm.Callback( self.many_follicle_load))



## --------------------------------------------------------------------------------------------------------------------------
# [asset]
      
        self.ui.matchname_set_btn.clicked.connect(pm.Callback( self.matchname_set_load))
        self.ui.cleanup_btn.clicked.connect(pm.Callback( self.cleanup_load))
        self.ui.attribute_unlock_btn.clicked.connect(pm.Callback( self.attribute_unlock_load))
        self.ui.ns_remove_btn.clicked.connect(pm.Callback( self.ns_remove_load))
        


## --------------------------------------------------------------------------------------------------------------------------
# [external]
        #UI에서 메뉴를 사용하려면 triggered 명령어를 사용
        self.ui.action_kk_controllers.triggered.connect(pm.Callback( self.kk_controllers_load)) 
        self.ui.action_cv_shape_color.triggered.connect(pm.Callback( self.cv_shape_color_load))
        self.ui.action_symmetry_tool.triggered.connect(pm.Callback( self.symmetry_tool_load))
        self.ui.action_connect_tool.triggered.connect(pm.Callback( self.connect_tool_load))
        self.ui.action_mel_to_python.triggered.connect(pm.Callback( self.mel_to_python_load))





## --------------------------------------------------------------------------------------------------------------------------
# [set]
        self.ui.vehicle_set_btn.clicked.connect(pm.Callback( self.vehicle_set_load))
        self.ui.long_skirt_set_btn.clicked.connect(pm.Callback( self.long_skirt_set_load))
        self.ui.short_skirt_set_btn.clicked.connect(pm.Callback( self.short_skirt_set_load))
        self.ui.body_set_btn.clicked.connect(pm.Callback( self.body_set_load))




        




##!--------------------------------------------------------------------------------------------------------------------------
# KJY_UI의 버튼과 연결된 함수, 이 함수는 command함수와 연결
# [ctrl]

    def offGRP_load(self):
        Rig_command.offGRP_command()


    def object_grp_load(self):
        Rig_command.object_grp()


    def position_copy_load(self):
        Rig_command.position_copy()


    def curve_vtx_ro_sc_load(self,ro_sc,x,y,z):
            ro_weight = self.ui.ro_xyz_box.value() #ro_xyz_box 에 적은 값을 저장
            sc_weight = self.ui.sc_xyz_box.value() #sc_xyz_box 에 적은 값을 저장
            
            Rig_command.curve_vtx_ro_sc(ro_weight, sc_weight , ro_sc, x,y,z )


## --------------------------------------------------------------------------------------------------------------------------
# [move]

    def AtoB_BtoA_load(self):
        Rig_command.AtoB_BtoA('AtoB')


    def AtoB_BtoA_copy_pivot_load(self):
        Rig_command.AtoB_BtoA_copy_pivot('AtoB')


## --------------------------------------------------------------------------------------------------------------------------
# [follicle]

    def one_follicle_load(self):
        Rig_command.follicle_make()


    def many_follicle_load(self):
        Rig_command.follicle_many_UI()


## --------------------------------------------------------------------------------------------------------------------------
# [select]

    def skin_jnt_select_load(self):
        Rig_command.skin_jnt_select()


    def jnt_hierarchy_load(self):
        Rig_command.jnt_hierarchy()


    def same_vtx_set_load(self):
        Rig_command.same_vtx_set()


    def geo_of_jnt_load(self):
        Rig_command.geo_of_jnt()


## --------------------------------------------------------------------------------------------------------------------------
# [skin]

    def bind_skin_copy_load(self):
        Rig_command.bind_skin_copy()


    def skin_copy_many_load(self):
        Rig_command.skin_copy_many()


    def rewei_load(self):
        weight = self.ui.rewei_box.value() # rewei_box 에 적은 값을 저장
        Rig_command.remove_skin_weight( weight )


    def reference_copy_load(self):
        Rig_command.reference_copy()
        

    def ngskin_tool_load(self):
        Rig_command.ngskin_tool()


## --------------------------------------------------------------------------------------------------------------------------
# [rig]

    def rename_load(self):
        
        global rename_texfld
        # 윈도우_ID
        windowID='KJY_tool'

        #windows_reset
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        cmds.window(windowID, t='KJY_rename', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))

        #master_layer
        master = cmds.columnLayout()
        cmds.columnLayout()

        #rename
        cmds.rowColumnLayout( nr=1 )
        rename_texfld = cmds.textField(h=20,w=200, aie=1, ec='KJY_UI.rename_command("rename")')
        
        
        #ec는 엔터로 명령어를 실행하게해줌, aie는 큰엔터로도 실행가능하게 해줌 

       # cmds.button(l = 'Rename' , w = 100 , c = 'Rig_command.re_test("test")')
        cmds.setParent(master)

        cmds.showWindow(windowID)


    def joint_on_off_load(self,vis):
        Rig_command.joint_on_off(vis)

    
    def jnt_ps_load(self):
        parent_check = self.ui.jnt_ps_p_cb.isChecked() # joint constraintParent 체크박스 선택
        scale_check = self.ui.jnt_ps_s_cb.isChecked() # joint constraintSacale 체크박스 선택

        Rig_command.jnt_ps(parent_check, scale_check)



    def constraint_copy_load(self):
        Rig_command.constraint_copy()


    def LR_copy_load(self):
        Rig_command.LR_copy()


    def motionpath_cv_load(self):
        Rig_command.motionpath_cv()

## --------------------------------------------------------------------------------------------------------------------------
# [blend]

    def blend_copy_load(self):
        Rig_command.blend_copy()


## --------------------------------------------------------------------------------------------------------------------------
# [asset]

    def matchname_set_load(self):
        Asset_command.matchname_set()


    def cleanup_load(self):
        Asset_command.cleanup()


    def attribute_unlock_load(self):
        Asset_command.attribute_unlock()


    def ns_remove_load(self):
        Asset_command.ns_remove()


## --------------------------------------------------------------------------------------------------------------------------
# [external]
    
    def kk_controllers_load(self):
        External_command.kk_controllers()


    def cv_shape_color_load(self):
        External_command.ctrlShape_color_UI()


    def symmetry_tool_load(self):
        External_command.symmetry_tool()

    
    def connect_tool_load(self):
        External_command.connect_tool()


    def mel_to_python_load(self):
        External_command.mel_to_python()



## --------------------------------------------------------------------------------------------------------------------------
# [set]

    def vehicle_set_load(self):
        Set_command.vehicle_set()

    def long_skirt_set_load(self):
        Set_command.long_skirt_set()

    def short_skirt_set_load(self):
        Set_command.short_skirt_set()

    def body_set_load(self):
        Body_command.body_set()









##!--------------------------------------------------------------------------------------------------------------------------
# KJY_UI class밖의 함수

# rename_load 의 연결 함수
def rename_command(part):
    rename_tex = cmds.textField(rename_texfld, q=1, text=1) #rename.UI_textField에 적는 값을 추출

    if part == "rename":Rig_command.rename(rename_tex) #Rig_command에 있는 rename함수 연결
        




















