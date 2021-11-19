# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import sys
import maya.mel as mel
import string 
import pymel.core as pm

Set_route = 'D:/KJY/python/Set/' # Set 폴더의 경로

# [vehicle_set]


class vehicle_set():

    def __init__(self):
        if pm.window('mirRigVehicle', q=1, ex=1):
            pm.deleteUI('mirRigVehicle')
        pm.window('mirRigVehicle', ret=1, w=264, t='Vehicle Build V01 TK01', h=124, s=1, mb=1)
        pm.columnLayout('mRV_columnLayout', w=262, h=120)
        pm.separator('mRV_separator1')
        pm.text('mRV_text1', l='                                      Import')
        pm.separator('mRV_separator2')
        pm.button('mRV_button1', w=260, h=30, l='Import', c=pm.Callback(self.import_vehicle))
        pm.separator('mRV_separator3')
        pm.text('mRV_text2', l='                                      Build')
        pm.separator('mRV_separator4')
        pm.button('mRV_button2', w=260, h=30, l='Build', c=pm.Callback(self.applySet))
        pm.separator('mRV_separator5')
        pm.text('mRV_text3', l='                             Go To Build Pose')
        pm.separator('mRV_separator6')
        pm.button('mRV_button3', w=260, h=30, l='Go To Build Pose', c=pm.Callback(self.buildPose))
        pm.separator('mRV_separator7')
        pm.text('mRV_text4', l='     Do you want to roll back? Nothing like that.')
        pm.showWindow('mirRigVehicle')


    def import_vehicle(self):
        vehicle_bindpose = Set_route + 'car_fit.mb'
        cmds.file( vehicle_bindpose, i = 1 , f = 1  )




    def buildSet(self):
        selDelete = pm.ls('*_vehicleDelete')
        deleteETC = pm.delete(selDelete)
        dmtList = ['frontWheel_R_distance_MULT',
        'frontWheel_L_distance_MULT',
        'backWheel_R_distance_MULT',
        'backWheel_L_distance_MULT']
        dmtCtlList = ['frontWheel_R_CTL',
        'frontWheel_L_CTL',
        'backWheel_R_CTL',
        'backWheel_L_CTL']
        for i in range(len(dmtList)):
            diameter = pm.getAttr(dmtList[i] + '.outputX')
            pm.setAttr(dmtCtlList[i] + '.diameter', diameter)

        pm.parentConstraint('body_M_pivTarget_GRP', 'body_M_control_conGRP', mo=1)
        parList = ['sky_M_CTL',
        'body_M_CTL',
        'frontDoor_L_CTL',
        'backDoor_L_CTL',
        'frontDoor_R_CTL',
        'backDoor_R_CTL',
        'frontWheel_R_tgetJNT',
        'backWheel_R_tgetJNT',
        'frontWheel_L_tgetJNT',
        'backWheel_L_tgetJNT']
        chiList = ['root_M_skinJNT',
        'body_M_skinJNT',
        'frontDoor_L_skinJNT',
        'backDoor_L_skinJNT',
        'frontDoor_R_skinJNT',
        'backDoor_R_skinJNT',
        'frontWheel_R_skinJNT',
        'backWheel_R_skinJNT',
        'frontWheel_L_skinJNT',
        'backWheel_L_skinJNT']
        for i in range(len(parList)):
            if pm.objExists(chiList[i]):
                pm.parentConstraint(parList[i], chiList[i], mo=1)
                pm.scaleConstraint(parList[i], chiList[i], mo=1)
            else:
                delName = chiList[i].split('_skinJNT')[0]
                pm.delete(delName + '*')

        pm.setAttr('main_M_CTL_GRP.visibility', 1)
        pm.setAttr('poser_GRP.visibility', 0)
        selDeleteEnd = pm.ls('*_endVehicleDelete')
        deleteETCEnd = pm.delete(selDeleteEnd)


    def applySet(self):
        pm.Callback(self.buildSet())
        


    def buildPose(self):
        ctlList = ['frontWheel_L_CTL',
        'backWheel_L_CTL',
        'front_set_CTL',
        'back_set_CTL',
        'right_set_CTL',
        'backDoor_R_CTL',
        'frontWheel_R_CTL',
        'frontDoor_R_CTL',
        'backWheel_R_CTL',
        'world_M_CTL',
        'body_M_CTL',
        'main_M_CTL',
        'sky_M_CTL',
        'backWheel_rot_CTL',
        'left_set_CTL',
        'frontWheel_rot_CTL',
        'frontDoor_L_CTL',
        'backDoor_L_CTL']
        attrName = ['translateX',
        'translateY',
        'translateZ',
        'rotateX',
        'rotateY',
        'rotateZ',
        'scaleX',
        'scaleY',
        'scaleZ']
        for i in range(len(ctlList)):
            if pm.objExists(ctlList[i]):
                for s in attrName:
                    if pm.getAttr(ctlList[i] + '.' + s, k=1):
                        if 'scale' in str(s):
                            pm.setAttr(ctlList[i] + '.' + s, 1)
                        else:
                            pm.setAttr(ctlList[i] + '.' + s, 0)


    