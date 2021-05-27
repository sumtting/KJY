# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import json
from collections import OrderedDict


body_CTL_list = [u'test_01_CTL', u'test_02_CTL']
# body의 모든 컨트롤러 리스트

def key_value_dic(list_):
    # 키값이 들어가있는 컨트롤러 리스트를 컨트롤러:{어트리뷰트:키값} 딕셔너리로 추출
    global CTL_dic_list
    CTL_dic_list = []
    
    for body_CTL in list_:
        attrs = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트들만 한세트씩 추출

        keyable_value_dic_list=[]

        for keyable in attrs:

            body_CTL_keyable = '%s' %(body_CTL + '.' + keyable) # 컨트롤러네임 + .keyable 상태로 추출
                
            get_frame  = cmds.keyframe( body_CTL_keyable, query=True, absolute=True ) # 해당 컨트롤러의 키가 찍혀있는 프레임을 모두 추출    
            get_keyvalue = cmds.keyframe( body_CTL_keyable, query=True, valueChange=True) # 해당 컨트롤러의 키밸류값을 모두 추출 
            
            keyable_value_dic = {keyable : [ {'frame' : get_frame},{'keyvalue' : get_keyvalue} ] } # 어트리뷰트:{프레임:값,키밸류:값} 딕셔너리

            keyable_value_dic_list.append(keyable_value_dic)

        CTL_dic = {body_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:{프레임:값,키밸류:값}} 딕셔너리
        CTL_dic_list.append(CTL_dic)

    return CTL_dic_list
    
    
    
           
key_value_dic(body_CTL_list) 

     



def cre_json(name_, dic_list):  #name_은 문자열로 입력    
    # json 파일 생성

    file_path = 'd:/json_data/'
    file_name = name_ + '.json'

    with open(file_path + file_name,'w') as save_json:
        json.dump(dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)
        
        

cre_json('bbbc',CTL_dic_list)


#--------------------------------------------------------------------------------------------------

def load_json_setkey(name_): #name_은 문자열로 입력, json에있는 딕셔너리로 키프레임을 찍어준다.
    # json 파일 불러오기
 
    file_path = 'd:/json_data/'
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
                        
                            cmds.setKeyframe(CTL_at, t= frame_, v= keyvalue_) 
                                
                            
load_json_setkey('bbbc')
                            
                            

       
        
        
#-------------------------------------------------------------------------------------------------

def key_clear(list_):
    # 현재프레임위치를 0으로 되돌리고 모든키값을 지워준다.
         
    mySel = cmds.ls(list_)

    cmds.currentTime(1)
        
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
        
    cmds.delete(keyframe_list)
    
    
key_clear(body_CTL_list)



