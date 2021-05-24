import maya.cmds as cmds
import json
from collections import OrderedDict


body_CTL_list = [u'test_01_CTL', u'test_02_CTL']
# body의 모든 컨트롤러 리스트

def key_value_dic(body_CTL_list):

    attrs_list = []
    CTL_dic_list = []

    for body_CTL in body_CTL_list:
        attrs = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트를 한세트씩 추출

        keyable_value_dic_list=[]

        for keyable in attrs:

            body_CTL_keyable = '%s' %(body_CTL + '.' + keyable) 
                
            get_values = cmds.keyframe( body_CTL_keyable, time=(0,200), query=True, valueChange=True)
            
            keyable_value_dic = ('%s : %s' % (keyable, get_values))

            keyable_value_dic_list.append(keyable_value_dic)

        CTL_dic = ('%s : %s' %(body_CTL,keyable_value_dic_list))
        CTL_dic_list.append(CTL_dic)

    return CTL_dic_list
           
           
           

with open('c:/json/abc.json','w') as f:
    json.dump(CTL_dic_list,f, ensure_ascii=False)


