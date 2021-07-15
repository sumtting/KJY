# -*- coding: utf-8 -*- 
import maya.cmds as cmds
#import pymel.core as pm
import json
from collections import OrderedDict
import sys
import os

import RIG_checktool_command
reload (RIG_checktool_command)



json_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/' # json 폴더 경로


load_CTL_list_re = RIG_checktool_command.load_CTL_list()



def key_value_dic_create(list_):
    # 키값이 들어가있는 컨트롤러 리스트를 컨트롤러:{어트리뷰트:키값} 딕셔너리로 추출
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
                
                if get_frame == None and get_keyvalue == None :
                    pass

                else:
                    keyable_value_dic = {keyable : [ {'frame' : get_frame},{'keyvalue' : get_keyvalue} ] } # 어트리뷰트:{프레임:값,키밸류:값} 딕셔너리

                    keyable_value_dic_list.append(keyable_value_dic)

            CTL_dic = {rig_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:{프레임:값,키밸류:값}} 딕셔너리
            CTL_dic_list.append(CTL_dic)
            
        else:
            pass








def RIG_checktool_Json_manager(): # json_manager UI
    ## 윈도우 ID##
    windowID='Json_manager'
    ##windows reset
    if cmds.window(windowID, ex=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, t='Json_manager', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
    ##master layer
    master = cmds.columnLayout()
    cmds.columnLayout()
    cmds.text('line_text', w=252, l='CTL List', h=20)
    cmds.rowLayout('json_FromTo_rowLayout', nc=100)
    cmds.columnLayout('json_list_columnLayout', p='json_FromTo_rowLayout')
    cmds.textScrollList('json_list', p='json_list_columnLayout', w=250 , h=100, allowMultiSelection=0, append=textScrollList_addItem()) # textScrollList에 ani_CTL_list를 표시
    cmds.button('json_list_btn', w=250, l=u'View' , c='RIG_checktool_json.RIG_CTL_Json_btn("view")') #CTL_list add 버튼
    cmds.text(l = ' ')
    cmds.columnLayout('json_To_columnLayout', p='json_list_columnLayout')
    cmds.textScrollList('json_ToList', p='json_To_columnLayout', w=250, h=400) # textScrollList에 ani_CTL_list를 표시
    cmds.rowLayout('json_FromList_btn_layout', p='json_To_columnLayout', nc=100)
    cmds.button('json_FromListAdd_btn', w=122, l='Add' , c='RIG_checktool_json.CTL_list_btn("add")') #CTL_list add 버튼
    cmds.button('json_FromListRemove_btn', w=122, l='Remove', c='RIG_checktool_json.CTL_list_btn("remove")') #CTL_list remove 버튼
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = ' ')
    cmds.textField('json_FromListRename' , w = 122 )
    cmds.text(l = ' ')
    cmds.button('json_FromListRename_btn', w = 121, l='Rename', c='RIG_checktool_json.CTL_list_btn("rename")') #CTL_list rename 버튼
    cmds.rowColumnLayout( nr=1 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text('line_text', w=252, l='---------------------- Create Json ----------------------', h=30)
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = u'Jsonfile name' ,w = 80)
    cmds.textField('jsonfile_name' , w = 115 , h = 20 )
    cmds.text(l = ' ')
    cmds.button(l=u'create' , w = 50 , h = 20 , c = 'RIG_checktool_json.key_value_dic(RIG_checktool_json.load_CTL_list_re)') #json파일 생성 command
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = '      ')
    cmds.setParent (master)
    cmds.showWindow(windowID)

    



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
                
                if get_frame == None and get_keyvalue == None :
                    pass

                else:
                    keyable_value_dic = {keyable : [ {'frame' : get_frame},{'keyvalue' : get_keyvalue} ] } # 어트리뷰트:{프레임:값,키밸류:값} 딕셔너리

                    keyable_value_dic_list.append(keyable_value_dic)

            CTL_dic = {rig_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:{프레임:값,키밸류:값}} 딕셔너리
            CTL_dic_list.append(CTL_dic)
            
        else:
            pass

    
    # Json 파일 생성 ---------------------------------------------------------------------
    jsonfile_name = cmds.textField('jsonfile_name' , q = 1 , text = True )

    sels_json = cmds.textScrollList('json_list', si=True,q=True)[0]
    sels_ = sels_json.split('_CTL')[0]

    file_path = json_path + sels_ + '_set/'
    file_name = jsonfile_name + '.json'

    keypreset_json_list = RIG_checktool_command.folderlist(file_path)

    if file_name in keypreset_json_list: #만들 json파일의 이름이 중복이라면 선택메세지 출력
        sub_windowID='message_box'
        ##windows reset
        if cmds.window(sub_windowID, ex=True):
            cmds.deleteUI(sub_windowID)
        cmds.window(sub_windowID, t='message_box', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
        ##master layer
        message_master = cmds.columnLayout()
        cmds.columnLayout()
        cmds.text('message_text', w=252, l=u'폴더에 이미 "%s" 파일이 있습니다.\n덮어씌우시겠습니까?'%(file_name), h=40)
        cmds.rowLayout('message_text_layout', nc=10)
        cmds.button('message_yes_btn', w=125, l=u'예' , c='RIG_checktool_json.message_yes_btn("CTL_dic_list","message_box")')
        cmds.button('message_no_btn', w=125, l=u'아니오', c='RIG_checktool_json.message_no_btn("message_box")')
        cmds.showWindow(sub_windowID)


    else :
        with open(file_path + file_name,'w') as save_json:
            json.dump(CTL_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)

    



# 중복일경우 선택메세지 버튼 함수
def message_yes_btn(CTL_list,ID):
    sels_json = cmds.textScrollList('json_list', si=True,q=True)[0]
    sels_ = sels_json.split('_CTL')[0]
    file_path = json_path + sels_ + '_set/'

    key_value_dic_create(load_CTL_list_re) # CTL_dic_list을 정의하기 위해 호출
    file_name = cmds.textField('jsonfile_name' , q = 1 , text = True )
    file_name = file_name + '.json'
    with open(file_path + file_name,'w') as save_json:
            json.dump(CTL_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)
    cmds.deleteUI(ID)
    

def message_no_btn(ID):
    cmds.deleteUI(ID)    

#-------------------------------------------------------------------------------------------------------






    
def CTL_list_btn(command_): # json_manager UI에서 버튼을 눌렀을때 실행되는 함수 (ani_CTL_list.json에 대한 수정)
    # 누른버튼에 대한 코드를 실행하고 textScrollList 과 json파일을 새로 업데이트 시켜준다.
    sels_json = cmds.textScrollList('json_list', si=True,q=True)[0]
    sels_ = sels_json.split('_CTL')[0]
    file_path = json_path + sels_ + '_set/'
    
    if command_ == 'add' : # 선택한 오브젝트를 ani_CTL_list에 추가

        sels = cmds.ls(sl=1) 
        if len(sels) > 0 : 
            for sel in sels:
                if sel in RIG_CTL_list: # 추가할때 이미 같은 컨트롤러가 있는경우는 pass
                    pass
                else :
                    RIG_CTL_list.append(sel)

            cmds.textScrollList('json_ToList', e=True, removeAll=True,append=RIG_CTL_list) # 기존 textScrollList를 지우고 새로 업데이트

            new_dic_list = [{'RIG_CTL_list':RIG_CTL_list}] # 새로 딕셔너리를 정의해주고 json을 다시 만든다.
            file_name = sels_json + '.json'
            with open(file_path + file_name,'w') as save_json:
                json.dump(new_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)

        else:
            pass

        

    elif command_ == 'remove' : # 선택한 컨트롤러를 삭제
        sels_item = cmds.textScrollList('json_ToList', si=True,q=True)
        
        try:
            for sel_item in sels_item:
                RIG_CTL_list.remove(sel_item)

            cmds.textScrollList('json_ToList', e=True, removeAll=True,append=RIG_CTL_list)

            new_dic_list = [{'RIG_CTL_list':RIG_CTL_list}]

            file_name = sels_json + '.json'
            with open(file_path + file_name,'w') as save_json:
                json.dump(new_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)

        except:
            pass


        
    elif command_ == 'rename' : # 선택한 컨트롤러 리네임

        try:
            sels_item = cmds.textScrollList('json_ToList', si=True,q=True)[0] # textScrollList에서 선택한 item
            rename_text = cmds.textField('json_FromListRename', text=1, q=1) # rename textField에 입력한 text
            
            if rename_text in RIG_CTL_list : # 네이밍이 겹칠경우
                print '%s'%(rename_text) + " match name!"

            else : # sels_item과 rename_text를 치환
                i = RIG_CTL_list.index(sels_item)
                RIG_CTL_list[i] = rename_text
                
                cmds.textScrollList('json_ToList', e=True, removeAll=True,append=RIG_CTL_list)

                new_dic_list = [{'RIG_CTL_list':RIG_CTL_list}]
                
                file_name = sels_json + '.json'
                with open(file_path + file_name,'w') as save_json:
                    json.dump(new_dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)
        
        except:
            pass
       

def textScrollList_addItem(): 
        scene_list = cmds.ls(type='objectSet') # 씬에있는 모든 set을 쿼리
        json_list = RIG_checktool_command.folderlist(json_path) # folderlist 함수 쿼리(json_path 경로 폴더에있는 파일 모두 추출)
        same_result = [x for x in scene_list if x in json_list] # 오토리깅을 불러왔을때 잡혀있는 set의 이름과 겹치는 json폴더만 쿼리
        CTL_list_json = []

        for same_ in same_result:
            json_list = RIG_checktool_command.folderlist(json_path + same_)

            for json_ in json_list:
                json_ = json_.split('.json')[0]

                if '_CTL' in json_: # 오토리깅의 CTL리스트는 addItem항목에서 제외시킨다.(리스트위젯에는 키프리셋만 표기하기위함)
                    CTL_list_json.append(json_)
                
                else:
                    pass

        return CTL_list_json
                
        

def RIG_CTL_Json_btn(command_): # json_manager UI에서 버튼을 눌렀을때 실행되는 함수 (ani_CTL_list.json에 대한 수정)
    # 누른버튼에 대한 코드를 실행하고 textScrollList 과 json파일을 새로 업데이트 시켜준다.
    global sels_json
    global RIG_CTL_list
    
    if command_ == 'view' : 
        sels_json = cmds.textScrollList('json_list', si=True,q=True)[0]
        sels_ = sels_json.split('_CTL')[0]
        
        file_path = json_path + sels_ + '_set/'
        file_name = sels_json + '.json'

        with open(file_path + file_name,'r') as json_file:
            json_data = json.load(json_file)
            

        for i in json_data:
            
            RIG_CTL_list = i.values()[0] #json데이터 에서 밸류를 추출


        cmds.textScrollList('json_ToList', e=True, removeAll=True, allowMultiSelection=1, append=RIG_CTL_list) # 기존 textScrollList를 지우고 새로 업데이트
        
        return RIG_CTL_list
    else:
        pass

        

        
