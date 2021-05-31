# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import json
from collections import OrderedDict

# 컨트롤러 리스트
body_CTL_list = [u'test_01_CTL', u'test_02_CTL']

#--------------------------------------------------------------------------------------------------------------------

def key_value_dic(list_):
    # 키값이 들어가있는 컨트롤러 리스트를 컨트롤러:{어트리뷰트:키값} 딕셔너리로 추출
    global CTL_dic_list
    CTL_dic_list = []
    
    for rig_CTL in list_:
        
        key_count = cmds.keyframe( rig_CTL, query=True, keyframeCount=True ) # 선택된 컨트롤러에 키프레임 갯수 카운트

        if key_count > 0: # 키가 찍혀있는 컨트롤러만 추출(키카운트 갯수가 1개 이상)

            attrs = cmds.listAttr(rig_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트들만 한세트씩 추출

            keyable_value_dic_list=[]

            for keyable in attrs:

                rig_CTL_keyable = '%s' %(rig_CTL + '.' + keyable) # 컨트롤러네임 + .keyable 상태로 추출(단순네이밍, 쿼리를 편하게 하기 위함)
                
                # ------------------------------쿼리 목록------------------------------
                get_frame  = cmds.keyframe( rig_CTL_keyable, query=True, absolute=True ) # 해당 컨트롤러의 키가 찍혀있는 프레임을 모두 추출    
                get_keyvalue = cmds.keyframe( rig_CTL_keyable, query=True, valueChange=True) # 해당 컨트롤러의 키밸류값을 모두 추출
                
                get_intype = cmds.keyTangent( rig_CTL_keyable, query=True, inTangentType=True) # 그래프에디터의 인 탄젠트 타입(해당 키의 안쪽 그래프모양)
                get_inangle = cmds.keyTangent( rig_CTL_keyable,  query=True, inAngle=True) # 그래프에디터의 인 앵글값(그래프 각도)
                
                get_outtype = cmds.keyTangent( rig_CTL_keyable, query=True, outTangentType=True) # 그래프에디터의 아웃 탄젠트 타입(해당 키의 바깥쪽 그래프모양)
                get_outangle = cmds.keyTangent( rig_CTL_keyable,  query=True, outAngle=True) # 그래프에디터의 아웃 앵글값(그래프 각도)
                
                
                # 쿼리 목록 -> 딕셔너리 생성
                keyable_value_dic = {keyable : [ {'frame' : get_frame}, {'keyvalue' : get_keyvalue}, {'intype' : get_intype}, {'inangle' : get_inangle}, {'outtype' : get_outtype}, {'outangle' : get_outangle} ] } 
                # 어트리뷰트 : { 프레임:값, 키밸류:값, 인타입:타입, 인앵글:각도, 아웃타입:타입, 아웃앵글:각도 }
                

                keyable_value_dic_list.append(keyable_value_dic)

            CTL_dic = {rig_CTL : keyable_value_dic_list} # 컨트롤러 : {어트리뷰트 : { 프레임:값, 키밸류:값, 인타입:타입, 인앵글:각도, 아웃타입:타입, 아웃앵글:각도 } }
            CTL_dic_list.append(CTL_dic)
            
        else:
            pass

    return CTL_dic_list
    
    
    
           
key_value_dic(body_CTL_list) 

     



def cre_json(name_, dic_list):  #name_은 문자열로 입력    
    # json 파일 생성

    file_path = 'd:/KJY/python/sub_script/RIG_check_tool/json_data/'
    file_name = name_ + '.json'

    with open(file_path + file_name,'w') as save_json:
        json.dump(dic_list, save_json, ensure_ascii=False, indent=4, sort_keys=True)
        
        

cre_json('bbbc',CTL_dic_list)


#--------------------------------------------------------------------------------------------------

def load_json_setkey(name_): #name_은 문자열로 입력, json에있는 딕셔너리로 키프레임을 찍어준다.
    # json 파일 불러오기
 
    file_path = 'd:/KJY/python/sub_script/RIG_check_tool/json_data/'
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
 
                        
                        for val in val_at: # val_at는 {프레임:값, 키밸류:값, 인타입:타입, 인앵글:각도, 아웃타입:타입, 아웃앵글:각도}
                            key_name = val.keys()[0] 
                        
                        
                            # 각각의 밸류값을 리스트로 만드는 과정
                            if key_name == 'frame': #딕셔너리 키값이 frame이라면 frame의 밸류값 추출 (프레임숫자)
                                frame_list  = val.get('frame')
                            
                            
                            if key_name == 'keyvalue': #딕셔너리 키값이 keyvalue 이라면 keyvalue의 밸류값 추출 (키에찍힌 수치값)
                                keyvalue_list = val.get('keyvalue')
                                
                                
                            if key_name == 'intype': #딕셔너리 키값이 intype 이라면 intype의 밸류값 추출 (인 그래프의 타입)
                                intype_list = val.get('intype')
                                
                                
                            if key_name == 'inangle': #딕셔너리 키값이 inangle 이라면 inangle의 밸류값 추출 (인 그래프의 각도)
                                inangle_list = val.get('inangle')
                                
                                
                            if key_name == 'outtype': #딕셔너리 키값이 outtype 이라면 outtype의 밸류값 추출 (아웃 그래프의 타입)
                                outtype_list = val.get('outtype')
                                
                                
                            if key_name == 'outangle': #딕셔너리 키값이 outangle 이라면 outangle의 밸류값 추출 (아웃 그래프의 각도)
                                outangle_list = val.get('outangle')
                                

                        # 최종적으로 모든 쿼리값을 적용시키는 과정
                        for frame_, keyvalue_, intype_, inangle_, outtype_, outangle_  in zip(frame_list, keyvalue_list, intype_list, inangle_list, outtype_list, outangle_list): 

                            cmds.setKeyframe(CTL_at, t= frame_, v= keyvalue_) # 프레임,키밸류 적용
                            
                            # 그래프에디터는 in값 out값이 개별이므로 따로 해주어야한다
                            if intype_ == 'Fixed': # TangentType이 Fixed일 경우(그래프각도를 프리셋에서 선택한게아니고 수동으로 만진상태)
                                
                                cmds.keyTangent( CTL_at, edit=True, time=(frame_,frame_), absolute=True, inAngle=inangle_) # 적용된 프레임에 그래프에디터 앵글값 적용(그래프를 수동으로 만진상태 이므로 각도값을 똑같이 적용시킨다)
                            
                            else:
                            
                                cmds.keyTangent( CTL_at, edit=True, time=(frame_,frame_), absolute=True, inTangentType=intype_) # 적용된 프레임에 그래프에디터 타입 적용(그래프를 프리셋에서 골라서 사용한경우 이므로 프리셋타입을 똑같이 적용시킨다)
                                
                                
                            if outtype_ == 'Fixed': 
                                
                                cmds.keyTangent( CTL_at, edit=True, time=(frame_,frame_), absolute=True, outAngle=outangle_) 
                            
                            else:
                            
                                cmds.keyTangent( CTL_at, edit=True, time=(frame_,frame_), absolute=True, outTangentType=outtype_) 
                            
                       
load_json_setkey('bbbc')
                            
                            

       
        
        
#-------------------------------------------------------------------------------------------------

def key_clear(list_):
    # 현재프레임위치를 0으로 되돌리고 모든키값을 지워준다.
         
    mySel = cmds.ls(list_)

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
        
    cmds.delete(keyframe_list)
    
    
key_clear(body_CTL_list)



