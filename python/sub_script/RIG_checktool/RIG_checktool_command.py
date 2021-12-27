# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import json
from collections import OrderedDict
import os
import maya.OpenMaya as om
import maya.mel as mel


import RIG_checktool_json
#reload (RIG_checktool_json)


json_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/'
#json_path = 'Z:/_LIB/02_RIG/_RND/RIG0009_RigPreview/RIG_checktool/json_data/' #미르경로



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




def load_CTL_list(): # ani_CTL_list.json에서 밸류값(CTL_list)만 추출
    global ani_CTL_list

    scene_list = cmds.ls(type='objectSet')

    if ('human_set') or ('crowd_set') in scene_list:
        scene_list = ['human_set']

    elif 'Facial' in scene_list:
        scene_list = ['facial_set']

    else:
        pass

    json_list = folderlist(json_path) # folderlist 함수 쿼리(json_path 경로 폴더에있는 파일 모두 추출)
    same_result = [x for x in scene_list if x in json_list] # 오토리깅을 불러왔을때 잡혀있는 set의 이름과 겹치는 json폴더만 쿼리
    
    for same_ in same_result:
        json_list = folderlist(json_path + same_)
        name_ = same_.split('_set')[0]

        file_name = name_ + '_CTL.json'
        file_path = json_path + same_ + '/'
        
        with open(file_path + file_name,'r') as json_file:
            json_data = json.load(json_file)
        

        for i in json_data:
            
            ani_CTL_list = i.values()[0] #json데이터 에서 밸류를 추출

        return ani_CTL_list
    

ani_CTL_list=load_CTL_list() #ani_CTL_list를 정의해준다(ani_CTL_list.json에서 CTL만 추출)





# body의 모든 컨트롤러 리스트

# def key_value_dic(list_):
#     # 키값이 들어가있는 컨트롤러 리스트를 컨트롤러:{어트리뷰트:키값} 딕셔너리로 추출
#     global CTL_dic_list
#     CTL_dic_list = []
    
#     for rig_CTL in list_:
        
#         key_count = cmds.keyframe( rig_CTL, query=True, keyframeCount=True ) # 선택된 컨트롤러에 키프레임 갯수 카운트

#         if key_count > 0: # 키가 찍혀있는 컨트롤러만 추출

#             attrs = cmds.listAttr(rig_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트들만 한세트씩 추출

#             keyable_value_dic_list=[]

#             for keyable in attrs:

#                 rig_CTL_keyable = '%s' %(rig_CTL + '.' + keyable) # 컨트롤러네임 + .keyable 상태로 추출
                
#                 get_frame  = cmds.keyframe( rig_CTL_keyable, query=True, absolute=True ) # 해당 컨트롤러의 키가 찍혀있는 프레임을 모두 추출    
#                 get_keyvalue = cmds.keyframe( rig_CTL_keyable, query=True, valueChange=True) # 해당 컨트롤러의 키밸류값을 모두 추출 
            
#                 keyable_value_dic = {keyable : [ {'frame' : get_frame},{'keyvalue' : get_keyvalue} ] } # 어트리뷰트:{프레임:값,키밸류:값} 딕셔너리

#                 keyable_value_dic_list.append(keyable_value_dic)

#             CTL_dic = {rig_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:{프레임:값,키밸류:값}} 딕셔너리
#             CTL_dic_list.append(CTL_dic)
            
#         else:
#             pass

#     return CTL_dic_list
    




# def cre_json(name_, dic_list):  #name_은 문자열로 입력    
#     # json 파일 생성

#     file_path = 'd:/KJY/python/sub_script/RIG_checktool/json_data/'
#     file_name = name_ + '.json'

#     with open(file_path + file_name,'w') as save_json:
#         json.dump(dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)
        
        
#--------------------------------------------------------------------------------------------------

def load_json_setkey(name_): #name_은 문자열로 입력, json에있는 딕셔너리로 키프레임을 찍어준다.
    # json 파일 불러오기

    if 'Body' in name_:
        scene_list = cmds.ls(type='objectSet')
        if ('human_set') or ('crowd_set') in scene_list :
            scene_list = ['human_set']
        
        else:
            pass
    
    elif 'Facial' in name_:
        scene_list = ['facial_set']

    else:
        pass

    #scene_list = cmds.ls(type='objectSet')
    json_list = folderlist(json_path) # folderlist 함수 쿼리(json_path 경로 폴더에있는 파일 모두 추출)
    same_result = [x for x in scene_list if x in json_list] # 오토리깅을 불러왔을때 잡혀있는 set의 이름과 겹치는 json폴더만 쿼리
    
    
    for same_ in same_result:
        json_list = folderlist(json_path + same_)

        file_path = json_path + same_ + '/'
        file_name = name_ + '.json'

        with open(file_path + file_name,'r') as json_file:
            json_data = json.load(json_file)
        

        for i in json_data:

            for key_CTL,val_attr in i.items(): #json데이터 에서 딕셔너리 키:밸류를 추출
                #print(key_CTL,val_attr)

                for ats in i.values():

                    for at in ats:
                    
                        for key_at, val_at in at.items():
                        
                            CTL_at = ('%s.%s' %(key_CTL,key_at)) #해당 컨트롤러의 어트리뷰트 네임(test_01_CTL.translateX)
    
                            for val in val_at: # val_at는 {프레임:값,키밸류:값}
                                key_name = val.keys()[0] 
                            
                            
                                if key_name == 'frame': #딕셔너리 키값이 frame이라면 frame의 밸류값 추출
                                    frame_list  = val.get('frame')
                                
                                
                                if key_name == 'keyvalue': #딕셔너리 키값이 keyvalue 이라면 keyvalue의 밸류값 추출
                                    keyvalue_list = val.get('keyvalue')

                                

                            for frame_, keyvalue_  in zip(frame_list,keyvalue_list): 
                                #print 'frame = %s' %(frame_) 
                                #print 'value = %s' %(keyvalue_)

                                try: 
                                    cmds.setKeyframe(CTL_at, t= frame_, v= keyvalue_) # 맨위에서 정의한 컨트롤러 리스트와 겹치는 컨트롤러에 대해서만 키를 찍어준다.
                                except:
                                    pass


#-------------------------------------------------------------------------------------------------

def key_clear():
    # 현재프레임위치를 0으로 되돌리고 모든키값을 지워준다.
    scene_list = cmds.ls(type='objectSet')

    if 'crowd_set' in scene_list : # crowd_set은 human_set과 동일하게 취급
        scene_list.append('human_set')
    else:
        pass

    json_list = folderlist(json_path) # folderlist 함수 쿼리(json_path 경로 폴더에있는 파일 모두 추출)
    same_result = [x for x in scene_list if x in json_list] # 오토리깅을 불러왔을때 잡혀있는 set의 이름과 겹치는 json폴더만 쿼리
    
    
    for same_ in same_result:
        json_list = folderlist(json_path + same_)
        name_ = same_.split('_set')[0]

        file_name = name_ + '_CTL.json'
        file_path = json_path + same_ + '/'
        
        with open(file_path + file_name,'r') as json_file:
            json_data = json.load(json_file)
        

        for i in json_data:
            
            ani_CTL_list = i.values()[0] #json데이터 에서 밸류를 추출

         
            mySel = cmds.ls(ani_CTL_list)
            
            cmds.currentTime(0)
                
            keyframe_list = []
            try:
                keyframe_list += cmds.listConnections(mySel,s=True, type="animCurveTU")
            except:
                pass
            try:
                keyframe_list += cmds.listConnections(mySel,s=True, type="animCurveTL")
            except:
                pass
            try:
                keyframe_list += cmds.listConnections(mySel,s=True, type="animCurveTA")
            except:
                pass
                
            if len(keyframe_list) > 0 : # key노드가 있을경우에만 지워줌
                cmds.delete(keyframe_list)
            else:
                pass

            cmds.playbackOptions (min=1, max=200, animationStartTime=1, animationEndTime=200)
            cmds.currentTime(1)


def key_framebar(list_): #키가 찍혀있는 가장 마지막 프레임에 맞게 프레임바를 셋팅해준다.
    
    max_get_frame_list = []
    for CTL_ in list_:
        try:
            get_frame  = cmds.keyframe( CTL_, query=True, absolute=True )
            if get_frame is not None: # 키가 찍혀있지않은 CTL은 프레임이 None으로 쿼리되기때문에 if문을 넣어준다.
                max_get_frame = max(get_frame)
                max_get_frame_list.append(max_get_frame)
        except:
            pass
        
    
    final_max_frame = max(max_get_frame_list) # 쿼리한 프레임 리스트중 가장 큰값을 맥스프레임으로 지정
    cmds.playbackOptions (min = 1, max = final_max_frame, animationStartTime = 1, animationEndTime = final_max_frame)

    




# 같은 이름을 set으로 잡는다.
def getInstances():
    '인스턴스 같은이름'
    
    # 인스턴스 추출
    instances = []
    iterDag = om.MItDag(om.MItDag.kBreadthFirst)
    while not iterDag.isDone():
        instanced = om.MItDag.isInstanced(iterDag)
        if instanced:
            instances.append(iterDag.fullPathName())
        iterDag.next()


    new_instance_list = []
    object_instance_list = []
    for instance in instances:
        obTy = cmds.objectType( instance )
        if obTy == 'mesh':
            pass
        elif obTy == 'VRayMeshPreview':
            pass
        else: # object instance 만 추출
            if '|' in instance:
                split_instance = instance.split('|') # 경로와 이름 분리
                new_instance = split_instance[-1] # 경로 없는 이름만 추출
                
                new_instance_list.append(new_instance) # 경로 없는 이름을 리스트 묶음
                object_instance_list.append(instance)

    
    t=set([x for x in new_instance_list if new_instance_list.count(x) > 1])


    j=list(t)
    k=cmds.ls(j)
    if len(k) != 0:
        #cmds.sets(object_instance_list, n='instance_matches_sets')
        print j
    else:
        pass


    print(u'인스턴스 같은 이름 개수: ' + str(len(j)))



def object_matches_sets():
    'object 같은이름'
    print('-----------------------------------------\n[match name]')
    sels = cmds.ls()
    d=[]
    for sel in sels:
        if '|' in sel:
            g = sel.split('|')
            k=g[-1]

            d.append(k)

    t=set([x for x in d if d.count(x) > 1])

    j=list(t)
    k=cmds.ls(j)
    if len(k) != 0:
        #cmds.sets(k, n='matchname_set')
        print(j)
    else:
        pass
    
    print(u'같은 이름 개수: ' + str(len(j)))



def matchname_set():
    object_matches_sets()
    getInstances()



def unused_node(): # unused node 삭제
    print '-----------------------------------------\n[unused node]'
    un_node = mel.eval ( 'MLdeleteUnused;')

    if un_node == 0:
        print (u'삭제된 노드 없음')

    else:
        print (u'삭제된 노드 개수: %d'%(un_node))



def MOD_GRP_vis(): # MOD 그룹 vix on
    scene_list = cmds.ls(type='transform')
    for i in scene_list:
        if 'MOD_' in i:  
            cmds.setAttr(i + '.visibility' , 1)
            
        else :
            pass


    


