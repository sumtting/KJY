# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import json
from collections import OrderedDict


body_CTL_list = [u'test_01_CTL', u'test_02_CTL']
# body의 모든 컨트롤러 리스트

def key_value_dic(list_):
    global CTL_dic_list
    attrs_list = []
    CTL_dic_list = []
    
    for body_CTL in list_:
        attrs = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트를 한세트씩 추출

        keyable_value_dic_list=[]

        for keyable in attrs:

            body_CTL_keyable = '%s' %(body_CTL + '.' + keyable) 
                
            get_values = cmds.keyframe( body_CTL_keyable, time=(0,200), query=True, valueChange=True)
            
            keyable_value_dic = {keyable : get_values}

            keyable_value_dic_list.append(keyable_value_dic)

        CTL_dic = {body_CTL : keyable_value_dic_list}
        CTL_dic_list.append(CTL_dic)

    return CTL_dic_list
    
    
    
           
key_value_dic(body_CTL_list) 

     
         

with open('c:/json/abc.json','w') as f:
    json.dump(CTL_dic_list,f, ensure_ascii=False, indent=4, sort_keys=True)



with open('c:/json/abc.json','r') as json_file:
    json_data = json.load(json_file)




for i in json_data:


    for key_CTL,val_attr in i.items():
        #print(key_CTL,val_attr)


        
        for ats in i.values():
            print key_CTL
            print('-' * 30)

            for at in ats:
            
                for key_at, val_at in at.items():
                
                    print(key_at,val_at)
                
    
        
        







