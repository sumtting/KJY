# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import json
from collections import OrderedDict
import sys


body_CTL_list = [u'ankle_FK_L_CTL', u'knee_FK_L_CTL', u'leg_FK_L_CTL', u'toeTip_FK_L_CTL', u'toeBall_FK_L_CTL', u'toes_FK_L_CTL', u'wrist_FK_L_CTL', u'elbow_FK_L_CTL', u'shoulder_FK_L_CTL', u'toes_FK_R_CTL', u'ankle_FK_R_CTL', u'knee_FK_R_CTL', u'leg_FK_R_CTL', u'toeTip_FK_R_CTL', u'toeBall_FK_R_CTL', u'wrist_FK_R_CTL', u'elbow_FK_R_CTL', u'shoulder_FK_R_CTL', u'main_M_CTL', u'world_M_CTL', u'middleFinger_01_R_CTL', u'middleFinger_04_R_CTL', u'middleFinger_03_R_CTL', u'ringFinger_01_R_CTL', u'ringFinger_04_R_CTL', u'ringFinger_03_R_CTL', u'ringFinger_02_R_CTL', u'pelvis_FK_L_CTL', u'leg_IK_pole_L_CTL', u'leg_IKFK_switch_L_CTL', u'wrist_IK_R_CTL', u'hipSwing_M_CTL', u'shoulder_IK_pole_L_CTL', u'shoulder_IKFK_switch_L_CTL', u'scapula_FK_L_CTL', u'ankle_IK_L_CTL', u'toes_IK_R_CTL', u'ankleSub_IK_R_CTL', u'toeTip_R_CTL', u'toeBall_IK_R_CTL', u'pelvis_FK_R_CTL', u'leg_IK_pole_R_CTL', u'leg_IKFK_switch_R_CTL', u'toes_IK_L_CTL', u'thumbFinger_01_R_CTL', u'wristSub_FK_R_CTL', u'ankleSub_IK_L_CTL', u'toeTip_L_CTL', u'toeBall_IK_L_CTL', u'ringFinger_02_L_CTL', u'middleFinger_01_L_CTL', u'middleFinger_04_L_CTL', u'middleFinger_03_L_CTL', u'ringFinger_01_L_CTL', u'ringFinger_04_L_CTL', u'ringFinger_03_L_CTL', u'ankle_IK_R_CTL', u'spine_IK_MU_CTL', u'spine_IK_MM_CTL', u'spine_IK_MD_CTL', u'rootMain_M_CTL', u'neck_M_CTL', u'head_M_CTL', u'neckSub_M_CTL', u'spine_FK_03_M_CTL', u'spine_FK_04_M_CTL', u'middleFinger_02_L_CTL', u'indexFinger_01_L_CTL', u'indexFinger_04_L_CTL', u'shoulder_IK_pole_R_CTL', u'shoulder_IKFK_switch_R_CTL', u'indexFinger_03_L_CTL', u'indexFinger_02_L_CTL', u'thumbFinger_03_L_CTL', u'spine_FK_01_M_CTL', u'spine_FK_02_M_CTL', u'root_FK_M_CTL', u'sky_M_CTL', u'scapula_FK_R_CTL', u'wrist_IK_L_CTL', u'indexFinger_02_R_CTL', u'thumbFinger_03_R_CTL', u'thumbFinger_02_R_CTL', u'middleFinger_02_R_CTL', u'indexFinger_01_R_CTL', u'indexFinger_04_R_CTL', u'indexFinger_03_R_CTL', u'weapon_R_CTL', u'pinkyFinger_01_R_CTL', u'pinkyFinger_04_R_CTL', u'pinkyFinger_03_R_CTL', u'pinkyFinger_02_R_CTL', u'thumbFinger_02_L_CTL', u'thumbFinger_01_L_CTL', u'wristSub_FK_L_CTL', u'fingers_R_CTL', u'weapon_L_CTL', u'pinkyFinger_01_L_CTL', u'pinkyFinger_04_L_CTL', u'pinkyFinger_03_L_CTL', u'pinkyFinger_02_L_CTL', u'fingers_L_CTL']


def RIG_checktool_json_UI():
    ## 윈도우 ID##
    windowID='json_UI'
    ##windows reset
    if cmds.window(windowID, ex=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, t='json_UI', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
    ##master layer
    master = cmds.columnLayout()
    cmds.columnLayout()
    
    cmds.rowColumnLayout( nr=1 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    # cmds.checkBox( 'rev_check', l = u'좌우 동시생성' , v=True )
    cmds.text(l = '    ')
    cmds.text(l = u'JsonFile_name' ,w = 80)
    cmds.text(l = '      ')
    cmds.textField('jsonfile_name' , w = 100 , h = 20 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    #cmds.text(l = u'CTL_list' ,w = 110)
    #cmds.textField('CTL_list' , w = 150 , h = 20)
    #cmds.button( l = u'등록' , w = 50 , c = 'PBS_UI.PBS_spline_ik.tw_sels_tex("st_sel")')
    cmds.setParent (master)
    cmds.button(l=u'생성' , w = 300 , h = 30 , c = 'RIG_checktool_json.key_value_dic(body_CTL_list)')
    cmds.setParent (master)
    cmds.showWindow(windowID)




# body의 모든 컨트롤러 리스트

def key_value_dic(list_):
    # 키값이 들어가있는 컨트롤러 리스트를 컨트롤러:{어트리뷰트:키값} 딕셔너리로 추출
    global CTL_dic_list
    CTL_dic_list = []
    
    for rig_CTL in list_:
        
        key_count = cmds.keyframe( rig_CTL, query=True, keyframeCount=True ) # 선택된 컨트롤러에 키프레임 갯수 카운트

        if key_count > 0: # 키가 찍혀있는 컨트롤러만 추출

            attrs = cmds.listAttr(rig_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트들만 한세트씩 추출

            keyable_value_dic_list=[]

            for keyable in attrs:

                rig_CTL_keyable = '%s' %(rig_CTL + '.' + keyable) # 컨트롤러네임 + .keyable 상태로 추출
                
                get_frame  = cmds.keyframe( rig_CTL_keyable, query=True, absolute=True ) # 해당 컨트롤러의 키가 찍혀있는 프레임을 모두 추출    
                get_keyvalue = cmds.keyframe( rig_CTL_keyable, query=True, valueChange=True) # 해당 컨트롤러의 키밸류값을 모두 추출 
            
                keyable_value_dic = {keyable : [ {'frame' : get_frame},{'keyvalue' : get_keyvalue} ] } # 어트리뷰트:{프레임:값,키밸류:값} 딕셔너리

                keyable_value_dic_list.append(keyable_value_dic)

            CTL_dic = {rig_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:{프레임:값,키밸류:값}} 딕셔너리
            CTL_dic_list.append(CTL_dic)
            
        else:
            pass



    # Json 파일 생성 ---------------------------------------------------------------------
    jsonfile_name = cmds.textField('jsonfile_name' , q = 1 , text = True )

    file_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/'
    file_name = jsonfile_name + '.json'

    with open(file_path + file_name,'w') as save_json:
        json.dump(CTL_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)

   
    
    



        
        