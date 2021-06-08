# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import pymel.core as pm
import json
from collections import OrderedDict
import sys
import os

json_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/'
body_CTL_list = [u'ankle_FK_L_CTL', u'knee_FK_L_CTL', u'leg_FK_L_CTL', u'toeTip_FK_L_CTL', u'toeBall_FK_L_CTL', u'toes_FK_L_CTL', u'wrist_FK_L_CTL', u'elbow_FK_L_CTL', u'shoulder_FK_L_CTL', u'toes_FK_R_CTL', u'ankle_FK_R_CTL', u'knee_FK_R_CTL', u'leg_FK_R_CTL', u'toeTip_FK_R_CTL', u'toeBall_FK_R_CTL', u'wrist_FK_R_CTL', u'elbow_FK_R_CTL', u'shoulder_FK_R_CTL', u'main_M_CTL', u'world_M_CTL', u'middleFinger_01_R_CTL', u'middleFinger_04_R_CTL', u'middleFinger_03_R_CTL', u'ringFinger_01_R_CTL', u'ringFinger_04_R_CTL', u'ringFinger_03_R_CTL', u'ringFinger_02_R_CTL', u'pelvis_FK_L_CTL', u'leg_IK_pole_L_CTL', u'leg_IKFK_switch_L_CTL', u'wrist_IK_R_CTL', u'hipSwing_M_CTL', u'shoulder_IK_pole_L_CTL', u'shoulder_IKFK_switch_L_CTL', u'scapula_FK_L_CTL', u'ankle_IK_L_CTL', u'toes_IK_R_CTL', u'ankleSub_IK_R_CTL', u'toeTip_R_CTL', u'toeBall_IK_R_CTL', u'pelvis_FK_R_CTL', u'leg_IK_pole_R_CTL', u'leg_IKFK_switch_R_CTL', u'toes_IK_L_CTL', u'thumbFinger_01_R_CTL', u'wristSub_FK_R_CTL', u'ankleSub_IK_L_CTL', u'toeTip_L_CTL', u'toeBall_IK_L_CTL', u'ringFinger_02_L_CTL', u'middleFinger_01_L_CTL', u'middleFinger_04_L_CTL', u'middleFinger_03_L_CTL', u'ringFinger_01_L_CTL', u'ringFinger_04_L_CTL', u'ringFinger_03_L_CTL', u'ankle_IK_R_CTL', u'spine_IK_MU_CTL', u'spine_IK_MM_CTL', u'spine_IK_MD_CTL', u'rootMain_M_CTL', u'neck_M_CTL', u'head_M_CTL', u'neckSub_M_CTL', u'spine_FK_03_M_CTL', u'spine_FK_04_M_CTL', u'middleFinger_02_L_CTL', u'indexFinger_01_L_CTL', u'indexFinger_04_L_CTL', u'shoulder_IK_pole_R_CTL', u'shoulder_IKFK_switch_R_CTL', u'indexFinger_03_L_CTL', u'indexFinger_02_L_CTL', u'thumbFinger_03_L_CTL', u'spine_FK_01_M_CTL', u'spine_FK_02_M_CTL', u'root_FK_M_CTL', u'sky_M_CTL', u'scapula_FK_R_CTL', u'wrist_IK_L_CTL', u'indexFinger_02_R_CTL', u'thumbFinger_03_R_CTL', u'thumbFinger_02_R_CTL', u'middleFinger_02_R_CTL', u'indexFinger_01_R_CTL', u'indexFinger_04_R_CTL', u'indexFinger_03_R_CTL', u'weapon_R_CTL', u'pinkyFinger_01_R_CTL', u'pinkyFinger_04_R_CTL', u'pinkyFinger_03_R_CTL', u'pinkyFinger_02_R_CTL', u'thumbFinger_02_L_CTL', u'thumbFinger_01_L_CTL', u'wristSub_FK_L_CTL', u'fingers_R_CTL', u'weapon_L_CTL', u'pinkyFinger_01_L_CTL', u'pinkyFinger_04_L_CTL', u'pinkyFinger_03_L_CTL', u'pinkyFinger_02_L_CTL', u'fingers_L_CTL']



def folderlist(path, include=False): # include - False = 모든 파일, folder = 폴더만, ['.ma', '.mb'] = 리스트 내용만 
    '경로 위치의 file 이름 list 반환'
    try:
        file_list = os.listdir(path)
    except:
        file_list = []
    folder_list = []
    for file_ in file_list: # 파일 위치의 리스트 반환
        if include.__class__ == list: # include가 리스트 일경우 리스트의 파일 형식만 리스트 반환
            for incl in include:
                if incl in file_[-1*len(incl):]:
                    folder_list.append(file_)
        else: # include가 리스트가 아닐 경우
            if include == False: # include가 False 일경우 모든 파일 리스트 반환
                folder_list.append(file_)
            elif include == 'folder': # include가 'folder'일경우 폴더 이름만 리스트 반환
                if not '.' in file_:
                    folder_list.append(file_)
            else:
                pass
    return folder_list


json_file_list = folderlist(json_path)



def RIG_checktool_Json_manager():
    ## 윈도우 ID##
    windowID='Json_manager'
    ##windows reset
    if cmds.window(windowID, ex=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, t='Json_manager', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
    ##master layer
    master = cmds.columnLayout()
    cmds.columnLayout()


    cmds.rowLayout('json_FromTo_rowLayout', nc=100)
    cmds.columnLayout('json_From_columnLayout')
    cmds.text('json_FromText', w=95, l='Json', h=20)
    cmds.textScrollList('json_FromList',p='json_From_columnLayout', w=100, h=200, append=json_file_list)
    cmds.rowLayout('json_FromList_btn_layout', p='json_From_columnLayout', nc=100)
    cmds.button('json_FromListAdd_btn', w=98, l='Show CTL',c='RIG_checktool_json.json_info_query("json_FromList")')
    
    
    cmds.text('json_FromToText', p='json_FromTo_rowLayout', l='=>')
    cmds.columnLayout('json_To_columnLayout', p='json_FromTo_rowLayout')
    cmds.text('json_ToText', w=150, l='              CTL_list', h=20)
    cmds.textScrollList('json_ToList', p='json_To_columnLayout', w=200, h=200, allowMultiSelection=1)
    cmds.rowLayout('json_FromList_btn_layout', p='json_To_columnLayout', nc=100)
    cmds.button('json_FromListAdd_btn', w=98, l='Add' )
    cmds.button('json_FromListRemove_btn', w=98, l='Remove')




    
    cmds.rowColumnLayout( nr=1 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text('json_create', w=320, l='-' * 90, h=30)
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    
  
    cmds.text(l = '    ')
    cmds.text(l = u'JsonFile_name' ,w = 80)
    cmds.text(l = '    ')
    cmds.textField('jsonfile_name' , w = 150 , h = 20 )
    
    cmds.text(l = ' ')
    cmds.button(l=u'create' , w = 60 , h = 20 , c = 'RIG_checktool_json.key_value_dic(body_CTL_list)')
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = '      ')
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

   
    
    



def json_info_query(title):
    'textScrollList의 선택한 value를 qury 한다. '
    text = cmds.textScrollList( title, q=1, si=1)[0]

        
    file_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/'
    file_name = '%s'%(text)

    with open(file_path + file_name,'r') as json_file:
        json_data = json.load(json_file)
    
    global json_CTL_list
    json_CTL_list = []


    cmds.textScrollList('json_ToList', e=True, removeAll=True)
    for i in json_data:
        
        for CTL in i.keys(): #json데이터 에서 딕셔너리 키:밸류를 추출
            
            cmds.textScrollList('json_ToList', e=True, append=CTL)
    

 
    











        
# 실행명령
# import sys

# Json_manager_path = 'D:/KJY/python/sub_script/RIG_checktool'

# sys.path.append(Json_manager_path)

# import RIG_checktool_json
# reload(RIG_checktool_json)


# RIG_checktool_json.RIG_checktool_Json_manager()


