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
                
            get_values = cmds.keyframe( body_CTL_keyable, time=(0,1000), query=True, valueChange=True) # 해당 컨트롤러의 0~1000프레임 키값을 모두 추출 
            
            keyable_value_dic = {keyable : get_values} # 어트리뷰트:키값 딕셔너리

            keyable_value_dic_list.append(keyable_value_dic)

        CTL_dic = {body_CTL : keyable_value_dic_list} # 컨트롤러: {어트리뷰트:키값 리스트} 딕셔너리
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
    

    # 불러온 json파일을 이용하여 키프레임을 찍는다.
    for i in json_data:


        for key_CTL,val_attr in i.items(): #json데이터 에서 키:밸류를 추출
            #print(key_CTL,val_attr)


            
            for ats in i.values():
                print key_CTL
                print('-' * 30)

                for at in ats:
                
                    for key_at, val_at in at.items():
                    
                        print(key_at,val_at)
                        
                        CTL_at = ('%s.%s' %(key_CTL,key_at)) #해당 컨트롤러의 어트리뷰트 네임(test_01_CTL.translateX)
                        
                        for count, val in enumerate(val_at): # value값 리스트를 개별로 뽑아내고 순차적으로 키에 넣어준다
                            
                        
                            cmds.setKeyframe(CTL_at, t=(count + 1), v=val) # count는 0부터시작하므로 +1을해준다, 컨트롤러 어트리뷰트에 밸류값을 넣어서 키를찍어줌
                            
                            
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



