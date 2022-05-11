# -*- coding: utf-8 -*- 
import maya.mel as mel
import maya.OpenMaya as om
import re
from maya import OpenMaya, cmds
import maya.cmds as cmds
import pymel.core as pm
import os
import sys

##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [Sub]

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
        cmds.sets(object_instance_list, n='instance_matches_sets')
    else:
        pass


    print(u'인스턴스 같은 이름 개수: ' + str(len(j)))



def object_matches_sets():
    'object 같은이름'
    print('-----------------------------------------')
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
        cmds.sets(k, n='matchname_set')
        print(j)
    else:
        pass
    
    print(u'같은 이름 개수: ' + str(len(j)))



def matchname_set():
    object_matches_sets()
    getInstances()

# -----------------------------------------------------------------

def cleanup():
    'polygon cleanup을 잡는다.'
    mel.eval('polyCleanupArgList 3 { \"1\",\"2\",\"1\",\"0\",\"1\",\"0\",\"0\",\"0\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1e-005\",\"0\",\"1\",\"1\" }')

   

def attribute_unlock():
    'translate , rotate, scale, visibility 의 옵션을 unlock, unhide한다.'
    a=cmds.ls(sl=1)

    for c in a: 
            cmds.setAttr( c + '.' + 't' + 'x', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 't' + 'y', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 't' + 'z', lock= False ,keyable=True ,channelBox =False)

            cmds.setAttr( c + '.' + 'r' + 'x', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 'r' + 'y', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 'r' + 'z', lock= False ,keyable=True ,channelBox =False)

            cmds.setAttr( c + '.' + 's' + 'x', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 's' + 'y', lock= False ,keyable=True ,channelBox =False)
            cmds.setAttr( c + '.' + 's' + 'z', lock= False ,keyable=True ,channelBox =False)

            cmds.setAttr( c + '.' + 'visibility' , lock= False ,keyable=True ,channelBox =False)



# namespace editor의 네이밍을 모두 지운다. refornce namespace는 제외
def namespace_info():
    refs = cmds.file( q=1 ,r=1)
    refs_na_list = []
    for ref in refs:
    
        refs_na =cmds.referenceQuery(ref, namespace = 1)
        refs_re_na = refs_na.replace(':', '')
        refs_na_list.append(refs_re_na)
    
    
    NS = cmds.namespaceInfo (lon=1)
    NS.remove('UI')
    NS.remove('shared')
    
    set1 = set(NS)
    set2 = set(refs_na_list)
    NS=list(set1-set2)
    
    return NS



def ns_remove():
    'namespace 지움'
    print('-----------------------------------------')

    a = namespace_info()
    g=[]

    while True:
        if len(a) != 0:
            for c in a:

                cmds.namespace(mergeNamespaceWithRoot=1, removeNamespace = c)
                g.append(c)
        else:
            pass
        
        a = namespace_info()
        
        if len(a) == 0:
            break
    print(u'\"namespace\" 지운 이름: ' +  '/'.join(g))
    print(u'\"namespace\" 지운 개수: ' + str(len(g)))


attrExistList = ['visibility', 'lodVisibility', 'translate', 'translateX', 'translateY', 'translateZ',
                'rotate', 'rotateX', 'rotateY', 'rotateZ', 'scale', 'scaleX', 'scaleY', 'scaleZ',
                'rotateOrder', 'rotatePivot', 'rotatePivotX', 'rotatePivotY', 'rotatePivotZ',
                'rotatePivotTranslateX', 'rotatePivotTranslateY', 'rotatePivotTranslateZ',
                'scalePivot', 'scalePivotX', 'scalePivotY', 'scalePivotZ',
                'scalePivotTranslateX', 'scalePivotTranslateY', 'scalePivotTranslateZ', 'outputRotate',
                'outputTranslate', 'outputScale', 'follow', 'stretch', 'elbowPin', 'fkIkSwitch', 'midSub', 'firstTerm',
                'roll', 'tip', 'heel', 'bank', 'twistHeel', 'twistBall', 'twistTip', 'relax', 'input', 'output',
                'saddleVis', 'spread', 'indexCurl', 'middleCurl', 'ringCurl', 'pinkyCurl', 'thumbCurl', 'fist', 'weight',
                'doorAll', 'doorL', 'doorR', 'input1X', 'input1Y', 'input1Z', 'outputX', 'outputY', 'outputZ']

class connect_tool():
    '커넥트, 컨스트레인 툴'
    
    def __init__(self):
        if (pm.window('CCC_Tool', q=1, ex=1)): pm.deleteUI('CCC_Tool')
        pm.window('CCC_Tool', ret=1, t='Constraint / Connect Tool', mb=1)
        pm.tabLayout('CCC_tabLayout')
        pm.columnLayout('Connect')
        pm.rowLayout('ConnectFromTo_rowLayout', nc=100)
        pm.columnLayout('ConnectFrom_columnLayout')
        pm.rowLayout('ConnectFromSort_rowLayout', nc=100)
        pm.text('ConnectFromText', w=150, l='                From', h=20)
        pm.button('ConnectFromSort_btn', w=45, h=15, l='sort', c= pm.Callback(self.connectFromListSort))
        pm.textScrollList('ConnectFromList', p='ConnectFrom_columnLayout', w=200, h=200, ams=1)
        pm.rowLayout('ConnectFromList_btn_layout', p='ConnectFrom_columnLayout', nc=100)
        pm.button('ConnectFromListAdd_btn', w=98, l='ADD', c= pm.Callback(self.connectFromListAdd))
        pm.button('ConnectFromListRemove_btn', w=98, l='REMOVE', c= pm.Callback(self.connectFromListRemove))
        pm.text('ConnectFromToText', p='ConnectFromTo_rowLayout', l='>>')
        pm.columnLayout('ConnectTo_columnLayout', p='ConnectFromTo_rowLayout')
        pm.rowLayout('ConnectToSort_rowLayout', nc=100)
        pm.text('ConnectToText', w=150, l='              To', h=20)
        pm.button('ConnectToSort_btn', w=45, h=15, l='sort', c= pm.Callback(self.connectToListSort))
        pm.textScrollList('ConnectToList', p='ConnectTo_columnLayout', w=200, h=200, ams=1)
        pm.rowLayout('ConnectToList_btn_layout', p='ConnectTo_columnLayout', nc=100)
        pm.button('ConnectToListAdd_btn', w=98, l='ADD', c= pm.Callback(self.connectToListAdd))
        pm.button('ConnectToListRemove_btn', w=98, l='REMOVE', c= pm.Callback(self.connectToListRemove))
        pm.rowLayout('ConnectAttr_rowLayout', p='Connect', nc=100)
        pm.columnLayout('ConnectFromAttr_columnLayout')
        pm.text('ConnectFromAttrText', w=200, l='Attributes', h=20)
        pm.textScrollList('ConnectFromAttrList', w=200, h=200, ams=1)
        pm.button('ConnectFromAttr_btn', w=200, l='IMPORT', c= pm.Callback(self.importFromAttr))
        pm.text('ConnectFromToAttrText', p='ConnectAttr_rowLayout', l='>>')
        pm.columnLayout('ConnectToAttr_columnLayout', p='ConnectAttr_rowLayout')
        pm.text('ConnectToAttrText', w=200, l='Attributes', h=20)
        pm.textScrollList('ConnectToAttrList', w=200, h=200, ams=1)
        pm.button('ConnectToAttr_btn', w=200, l='IMPORT', c= pm.Callback(self.importToAttr))
        pm.columnLayout('ConnectBtn_columnLayout', p='Connect')
        pm.separator('ConnectBtn_separator')
        pm.button('Connect_btn', w=424, l='CONNECT', h=35, c= pm.Callback(self.connectAttrFromTo))
        pm.separator('ConnectBtn_separator_01')
        pm.button('Disconnect_btn', w=424, l='DISCONNECT', h=35, c= pm.Callback(self.disconnectAttrTo))
        pm.columnLayout('Constraint', p='CCC_tabLayout')
        pm.separator('Const_sep_01', h=10)
        pm.rowLayout('Const_rowLayout301', nc=100)
        pm.columnLayout('Const_columnLayout120')
        pm.text('Const_text290', w=200, l='From', h=20)
        pm.separator('Const_separator95', h=10)
        pm.textScrollList('Const_FromList', w=200, ams=1, h=340)
        pm.separator('const_FromSort_sep', h=3)
        pm.button('const_FromSort', w=200, h=30, l='SORT', c= pm.Callback(self.constFromListSort))
        pm.separator('const_FromSort_sep2', h=2)
        pm.rowLayout('Const_rowLayout1', nc=100)
        pm.button('Const_fromAdd_btn', w=98, h=35, l='ADD', c= pm.Callback(self.constFromAdd))
        pm.button('Const_fromRemove_btn', w=98, h=35, l='REMOVE', c= pm.Callback(self.constFromRemove))
        pm.text('Const_text292', p='Const_rowLayout301', l='>>')
        pm.columnLayout('Const_columnLayout121', p='Const_rowLayout301')
        pm.text('Const_text291', w=200, l='To', h=20)
        pm.separator('Const_separator96', h=10)
        pm.textScrollList('Const_ToList', w=200, ams=1, h=340)
        pm.separator('const_ToSort_sep', h=3)
        pm.button('const_ToSort', w=200, h=30, l='SORT', c= pm.Callback(self.constToListSort))
        pm.separator('const_ToSort_sep2', h=2)
        pm.rowLayout('Const_rowLayout2', nc=100)
        pm.button('Const_toAdd_btn', w=98, h=35, l='ADD', c= pm.Callback(self.constToAdd))
        pm.button('Const_toRemove_btn', w=98, h=35, l='REMOVE', c= pm.Callback(self.constToRemove))
        pm.separator('Const_separator1', p='Constraint', h=10)
        pm.rowLayout('Const_rowLayout302', p='Constraint', w=395, nc=100)
        pm.separator('Const_separator97', w=65, vis=0)
        pm.checkBox('parentCon_CB', l='Parent', w=80)
        pm.checkBox('pointCon_CB', l='Point', w=80)
        pm.checkBox('orientCon_CB', l='Orient', w=80)
        pm.checkBox('scaleCon_CB', l='Scale', w=80)
        pm.separator('Const_separator21', p='Constraint', w=428, vis=1, h=20)
        pm.rowLayout('Const_rowLayout122', p='Constraint', nc=100)
        pm.separator('Const_separator122', w=155, vis=0)
        pm.separator('Const_separator556', p='Constraint', h=10)
        pm.columnLayout('Const_columnLayout122', p='Constraint')
        pm.button('Const_apply_btn', w=424, l='APPLY', h=45, c= pm.Callback(self.constApply))
        pm.showWindow('CCC_Tool')

    '''
    sel = pm.ls(sl=1, fl=1)
    sel2 = pm.ls(sl=1, fl=1)
    for i in range(len(sel)):
        aa = pm.listAttr(sel[i])

    pm.connectAttr(From, To)


    paC = pm.parentConstraint
    poC = pm.pointConstraint
    orC = pm.orientConstraint
    scC = pm.scaleConstraint
    aiC = pm.aimConstraint

    constraintList = {'Parent': paC, 'Point': poC, 'Orient' : orC, 'Scale' : scC, 'Aim' : aiC}

    selParent = pm.ls(sl=1, fl=1)
    selTarget = pm.ls(sl=1, fl=1)
    '''

    def connectFromListAdd(self):
        currentTargetList = pm.textScrollList('ConnectFromList', q=True, ai=True)
        for item in pm.ls(sl=True, fl=True):
            if type(currentTargetList) == list:
                if currentTargetList.count(item): continue
            pm.textScrollList('ConnectFromList', e=True, a=item)

    def connectFromListSort(self):
        sortList = []
        currentTargetList = pm.textScrollList('ConnectFromList', q=True, ai=True)
        for i in currentTargetList:
            sortList.append(i)
        sortList.sort()
        pm.textScrollList('ConnectFromList', e=True, removeAll=True)
        pm.textScrollList('ConnectFromList', e=True, a=sortList)

    def connectFromListRemove(self):
        selItemList = pm.textScrollList('ConnectFromList', q=True, si=True)
        if selItemList:
            for item in selItemList:
                pm.textScrollList('ConnectFromList', e=True, ri=item)

    def connectToListAdd(self):
        currentTargetList = pm.textScrollList('ConnectToList', q=True, ai=True)
        for item in pm.ls(sl=True, fl=True):
            if type(currentTargetList) == list:
                if currentTargetList.count(item): continue
            pm.textScrollList('ConnectToList', e=True, a=item)

    def connectToListSort(self):
        sortList = []
        currentTargetList = pm.textScrollList('ConnectToList', q=True, ai=True)
        for i in currentTargetList:
            sortList.append(i)
        sortList.sort()
        pm.textScrollList('ConnectToList', e=True, removeAll=True)
        pm.textScrollList('ConnectToList', e=True, a=sortList)

    def connectToListRemove(self):
        selItemList = pm.textScrollList('ConnectToList', q=True, si=True)
        if selItemList:
            for item in selItemList:
                pm.textScrollList('ConnectToList', e=True, ri=item)

    def importFromAttr(self):
        pm.textScrollList('ConnectFromAttrList', e=True, removeAll=True)
        selItemList = pm.textScrollList('ConnectFromList', q=True, si=True)
        interAttrList = []
        for item in selItemList:
            attrList = pm.listAttr(item, c=True)
            for itemAttr in attrList:
                if itemAttr in interAttrList:
                    pass
                else:
                    interAttrList.append(itemAttr)
        for attr in interAttrList:
            if attr in attrExistList:
                pm.textScrollList('ConnectFromAttrList', e=True, append=attr)
            else:
                pass

    def importToAttr(self):
        pm.textScrollList('ConnectToAttrList', e=True, removeAll=True)
        selItemList = pm.textScrollList('ConnectToList', q=True, si=True)
        interAttrList = []
        for item in selItemList:
            attrList = pm.listAttr(item, c=True)
            for itemAttr in attrList:
                if itemAttr in interAttrList:
                    pass
                else:
                    interAttrList.append(itemAttr)
        for attr in interAttrList:
            if attr in attrExistList:
                pm.textScrollList('ConnectToAttrList', e=True, append=attr)
            else:
                pass

    def connectAttrFromTo(self):
        selFromItemList = pm.textScrollList('ConnectFromList', q=True, si=True)
        selFromAttr = pm.textScrollList('ConnectFromAttrList', q=True, si=True)

        selToItemList = pm.textScrollList('ConnectToList', q=True, si=True)
        selToAttr = pm.textScrollList('ConnectToAttrList', q=True, si=True)

        if len(selFromItemList) == len(selToItemList):
            if len(selFromAttr) == len(selToAttr):
                for i in range(len(selFromItemList)):
                    for j in range(len(selFromAttr)):
                        pm.connectAttr(selFromItemList[i]+'.'+selFromAttr[j], selToItemList[i]+'.'+selToAttr[j])
            elif len(selFromAttr) < len(selToAttr):
                if len(selFromAttr) == 1:
                    for i in range(len(selFromItemList)):
                        for j in range(len(selToAttr)):
                            pm.connectAttr(selFromItemList[i]+'.'+selFromAttr[0], selToItemList[i]+'.'+selToAttr[j])
                else:
                    pm.warning('Fuck... this is impossible')
            else:
                pm.warning('Fuck... this is impossible')

        elif len(selFromItemList) < len(selToItemList):
            if len(selFromItemList) == 1:
                if len(selFromAttr) == len(selToAttr):
                    for i in range(len(selToItemList)):
                        for j in range(len(selFromAttr)):
                            pm.connectAttr(selFromItemList[0] + '.' + selFromAttr[j], selToItemList[i] + '.' + selToAttr[j])
                elif len(selFromAttr) == 1:
                    for i in range(len(selToAttr)):
                        for j in range(len(selToAttr)):
                            pm.connectAttr(selFromItemList[0]+'.'+selFromAttr[0], selToItemList[i]+'.'+selToAttr[j])
            else:
                pm.warning('Fuck... this is impossible')
        elif len(selFromItemList) > len(selToItemList):
            pm.warning('Fuck... this is impossible')
        else:
            pass

    def disconnectAttrTo(self):
        selToItemList = pm.textScrollList('ConnectToList', q=True, si=True)
        selToAttr = pm.textScrollList('ConnectToAttrList', q=True, si=True)
        for i in selToItemList:
            for j in selToAttr:
                try:
                    AttrConnectList = pm.listConnections(i+'.'+j, s=1, p=1)[0]
                    pm.disconnectAttr(AttrConnectList, i+'.'+j)
                except:
                    pass

    # ---------------------------------------------------- Constraint --------------------------------------

    def constFromAdd(self):
        currentTargetList = pm.textScrollList('Const_FromList', q=True, ai=True)
        for item in pm.ls(sl=True, fl=True):
            if type(currentTargetList) == list:
                if currentTargetList.count(item): continue
            pm.textScrollList('Const_FromList', e=True, a=item)

    def constFromRemove(self):
        selItemList = pm.textScrollList('Const_FromList', q=True, si=True)
        if selItemList:
            for item in selItemList:
                pm.textScrollList('Const_FromList', e=True, ri=item)

    def constFromListSort(self):
        sortList = []
        currentTargetList = pm.textScrollList('Const_FromList', q=True, ai=True)
        for i in currentTargetList:
            sortList.append(i)
        sortList.sort()
        pm.textScrollList('Const_FromList', e=True, removeAll=True)
        pm.textScrollList('Const_FromList', e=True, a=sortList)

    def constToAdd(self):
        currentTargetList = pm.textScrollList('Const_ToList', q=True, ai=True)
        for item in pm.ls(sl=True, fl=True):
            if type(currentTargetList) == list:
                if currentTargetList.count(item): continue
            pm.textScrollList('Const_ToList', e=True, a=item)

    def constToRemove():
        selItemList = pm.textScrollList('Const_ToList', q=True, si=True)
        if selItemList:
            for item in selItemList:
                pm.textScrollList('Const_ToList', e=True, ri=item)

    def constToListSort(self):
        sortList = []
        currentTargetList = pm.textScrollList('Const_ToList', q=True, ai=True)
        for i in currentTargetList:
            sortList.append(i)
        sortList.sort()
        pm.textScrollList('Const_ToList', e=True, removeAll=True)
        pm.textScrollList('Const_ToList', e=True, a=sortList)

    def constApply(self):
        selFromItemList = pm.textScrollList('Const_FromList', q=True, si=True)
        selToItemList = pm.textScrollList('Const_ToList', q=True, si=True)

        par = pm.checkBox('parentCon_CB', q=1, v=1)
        poi = pm.checkBox('pointCon_CB', q=1, v=1)
        ori = pm.checkBox('orientCon_CB', q=1, v=1)
        sca = pm.checkBox('scaleCon_CB', q=1, v=1)

        if len(selFromItemList) == len(selToItemList):
            for i in range(len(selFromItemList)):
                if par:
                    pm.parentConstraint(selFromItemList[i], selToItemList[i], mo=1)
                if poi:
                    pm.pointConstraint(selFromItemList[i], selToItemList[i], mo=1)
                if ori:
                    pm.orientConstraint(selFromItemList[i], selToItemList[i], mo=1)
                if sca:
                    pm.scaleConstraint(selFromItemList[i], selToItemList[i], mo=1)
                else:
                    pass
        elif len(selFromItemList) < len(selToItemList):
            if len(selFromItemList) == 1:
                for i in range(len(selToItemList)):
                    if par:
                        pm.parentConstraint(selFromItemList[0], selToItemList[i], mo=1)
                    if poi:
                        pm.pointConstraint(selFromItemList[0], selToItemList[i], mo=1)
                    if ori:
                        pm.orientConstraint(selFromItemList[0], selToItemList[i], mo=1)
                    if sca:
                        pm.scaleConstraint(selFromItemList[0], selToItemList[i], mo=1)
                    else:
                        pass
            else:
                pm.warning('Fuck... this is impossible')

        elif len(selFromItemList) > len(selToItemList):
            if len(selToItemList) == 1:
                if par:
                    pm.parentConstraint(selFromItemList[0::], selToItemList[0], mo=1)
                if poi:
                    pm.pointConstraint(selFromItemList[0::], selToItemList[0], mo=1)
                if ori:
                    pm.orientConstraint(selFromItemList[0::], selToItemList[0], mo=1)
                if sca:
                    pm.scaleConstraint(selFromItemList[0::], selToItemList[0], mo=1)
                else:
                    pass
            else:
                pm.warning('Fuck... this is impossible')
        else:
            pass



class posereader():
    def __init__(self):
        if pm.window('createPR', q=1, ex=1):
            pm.deleteUI('createPR')
        pm.window('createPR', ret=1, s=0, t='Create PSD v01', w=302, mb=1)
        pm.tabLayout('tabLay', w=300)
        pm.columnLayout('Default', w=294)
        pm.separator('sep01', h=5)
        pm.text('txtSelJNT', w=293, l='* Select Joints * ')
        pm.separator('sep02', h=5)
        pm.rowLayout('rowLay01', nc=100, h=110)
        pm.rowLayout('rowLay02', nc=100)
        pm.textScrollList('defaultJNTList', ams=1, h=100, w=210)
        pm.columnLayout('buttonsLay', p='rowLay01')
        pm.button('addButton', h=30, w=75, l='<<ADD', command=pm.Callback(self.defaultLoadJNTListAdd))
        pm.separator('sep03', h=30)
        pm.button('removeButton', h=30, w=75, l='>>REMOVE', command=pm.Callback(self.defaultLoadJNTListRemove))
        pm.columnLayout('columnLay03', p='Default')
        pm.rowLayout('rowLay07', nc=100, h=20)
        pm.separator('sep12', vis=0, w=55)
        pm.radioCollection('bendButtons')
        pm.radioButton('bendRadioButton', l='Bend Joint', sl=1)
        pm.radioButton('notBendRadioButton', l='Not Bend Joint')
        pm.rowLayout('rowLay082', p='columnLay03', nc=100, h=20)
        pm.separator('sep122', vis=0, w=70)
        pm.radioCollection('hierConstButtons')
        pm.radioButton('hierRadioButton', l='Hierarchy')
        pm.radioButton('constRadioButton', l='Constraint', sl=1)
        pm.rowLayout('rowLay08', p='columnLay03', nc=100, h=25)
        pm.radioCollection('reverseButtonsD')
        pm.radioButton('defaultRadioButtonD', w=70, l='Default', sl=1)
        pm.radioButton('xReverseRadioButtonD', w=70, l='X reverse')
        pm.radioButton('yReverseRadioButtonD', w=70, l='Y reverse')
        pm.radioButton('zReverseRadioButtonD', w=70, l='Z reverse')
        pm.button('defaultApplyButton', p='Default', h=40, w=292, l='Apply', command=pm.Callback(self.defaultPoseReader))
        pm.columnLayout('Custom', p='tabLay', w=294)
        pm.separator('sep04', h=5)
        pm.text('txtSelJNTs', w=293, l='* Select Joint * ')
        pm.separator('sep05', h=5)
        pm.rowLayout('rowLay03', nc=100, h=30)
        pm.text('txtBaseJNT', w=70, l='Base Joint')
        pm.textScrollList('baseJNTList', w=150, h=25)
        pm.button('baseJNTbutton', w=65, l='<<', h=23, command=pm.Callback(self.customLoadJNTListBase))
        pm.separator('sep06', p='Custom', h=5)
        pm.rowLayout('rowLay10', p='Custom', nc=100)
        pm.text('txtFollowJNT', w=70, l='Follow Joint')
        pm.textScrollList('followJNTList', w=150, h=25)
        pm.button('followJNTbutton', w=65, h=23, l='<<', command=pm.Callback(self.customLoadJNTListFollow))
        pm.separator('sep07', p='Custom', h=5)
        pm.rowLayout('rowLay04', p='Custom', nc=100, h=30)
        pm.text('txtUpJNT', w=70, l='Up Joint')
        pm.textScrollList('upJNTList', w=150, h=25)
        pm.button('upJNTbutton', w=65, l='<<', h=23, command=pm.Callback(self.customLoadJNTListUp))
        pm.separator('sep08', p='Custom', h=5)
        pm.rowLayout('rowLay05', p='Custom', nc=100, h=30)
        pm.text('txtDownJNT', w=70, l='Down Joint')
        pm.textScrollList('downJNTList', w=150, h=25)
        pm.button('downJNTbutton', w=65, l='<<', h=23, command=pm.Callback(self.customLoadJNTListDown))
        pm.rowLayout('rowLay09', p='Custom', nc=100, h=25)
        pm.radioCollection('reverseButtonsC')
        pm.radioButton('defaultRadioButtonC', l='Default', w=70, sl=1)
        pm.radioButton('xReverseRadioButtonC', l='X reverse', w=70)
        pm.radioButton('yReverseRadioButtonC', l='Y reverse', w=70)
        pm.radioButton('zReverseRadioButtonC', l='Z reverse', w=70)
        pm.separator('sep13', p='Custom', h=5)
        pm.button('customApplyButton', p='Custom', w=292, h=40, l='Apply', command=pm.Callback(self.customPoseReader))
        pm.columnLayout('MirrorPSD', rs=5, w=300, p='tabLay')
        pm.text('selMesh', w=294, h=20, l='* Select mesh to mirror *')
        pm.rowLayout('fN', w=294, nc=100)
        pm.text('findName', w=80, l='Search Name')
        pm.textField('searchName', w=208, h=25)
        pm.rowLayout('nN', p='MirrorPSD', nc=100)
        pm.text('newName', w=80, l='Replace Name')
        pm.textField('replaceName', w=208, h=25)
        pm.rowLayout('mB', p='MirrorPSD', nc=100)
        pm.button('MirrorBS', w=290, h=40, l='Mirror BlendShape', c=pm.Callback(self.MirrorBlendUsingWrap))
        pm.rowLayout('cB', p='MirrorPSD', nc=100)
        pm.button('connectBS', w=290, h=40, l='Connect PoseReader', c=pm.Callback(self.connectPSD))
        pm.rowLayout('dcB', p='MirrorPSD', nc=100)
        pm.button('disconnectBS', w=290, h=40, l='Disconnect PoseReader', c=pm.Callback(self.disconnectPSD))
        pm.columnLayout('columnLay01', p='createPR', h=70, w=300)
        pm.text('txtPoseReaderVis', h=15, w=300, l='PoseReader Vis')
        pm.separator('sep09')
        pm.rowLayout('rowLay06', nc=100, h=50)
        pm.separator('sep10', vis=0, w=70)
        pm.button('onButton', h=40, w=80, l='ON', command=pm.Callback(self.poseReaderVisOn))
        pm.separator('sep11', vis=0, w=10)
        pm.button('offButton', h=40, w=80, l='OFF', command=pm.Callback(self.poseReaderVisOff))
        pm.showWindow('createPR')


    def defaultLoadJNTListAdd(self,*args):
        currentTargetList = pm.textScrollList('defaultJNTList', q=True, ai=True)
        for jnt in pm.ls(sl=True, type='joint'):
            if type(currentTargetList) == list:
                if currentTargetList.count(jnt):
                    continue
            pm.textScrollList('defaultJNTList', e=True, a=jnt)


    def defaultLoadJNTListRemove(self,*args):
        selJntList = pm.textScrollList('defaultJNTList', q=True, si=True)
        if selJntList:
            for jnt in selJntList:
                pm.textScrollList('defaultJNTList', e=True, ri=jnt)


    def customLoadJNTListBase(self,*args):
        currentTargetList = pm.textScrollList('baseJNTList', q=True, ai=True)
        for jnt in pm.ls(sl=True, type='joint'):
            if len(pm.ls(sl=True, type='joint')) > 1:
                pm.warning('select one Joint!!!')
                continue
            if type(currentTargetList) == list:
                if currentTargetList.count(jnt):
                    continue
            if currentTargetList:
                pm.textScrollList('baseJNTList', e=True, ra=True)
            pm.textScrollList('baseJNTList', e=True, a=jnt, si=jnt)


    def customLoadJNTListFollow(self,*args):
        currentTargetList = pm.textScrollList('followJNTList', q=True, ai=True)
        for jnt in pm.ls(sl=True, type='joint'):
            if len(pm.ls(sl=True, type='joint')) > 1:
                pm.warning('select one Joint!!!')
                continue
            if type(currentTargetList) == list:
                if currentTargetList.count(jnt):
                    continue
            if currentTargetList:
                pm.textScrollList('followJNTList', e=True, ra=True)
            pm.textScrollList('followJNTList', e=True, a=jnt, si=jnt)


    def customLoadJNTListUp(self,*args):
        currentTargetList = pm.textScrollList('upJNTList', q=True, ai=True)
        for jnt in pm.ls(sl=True, type='joint'):
            if len(pm.ls(sl=True, type='joint')) > 1:
                pm.warning('select one Joint!!!')
                continue
            if type(currentTargetList) == list:
                if currentTargetList.count(jnt):
                    continue
            if currentTargetList:
                pm.textScrollList('upJNTList', e=True, ra=True)
            pm.textScrollList('upJNTList', e=True, a=jnt, si=jnt)


    def customLoadJNTListDown(self,*args):
        currentTargetList = pm.textScrollList('downJNTList', q=True, ai=True)
        for jnt in pm.ls(sl=True, type='joint'):
            if len(pm.ls(sl=True, type='joint')) > 1:
                pm.warning('select one Joint!!!')
                continue
            if type(currentTargetList) == list:
                if currentTargetList.count(jnt):
                    continue
            if currentTargetList:
                pm.textScrollList('downJNTList', e=True, ra=True)
            pm.textScrollList('downJNTList', e=True, a=jnt, si=jnt)


    def defaultPoseReader(self,*args):
        selJntList = pm.textScrollList('defaultJNTList', q=True, si=True)
        selreAxis = pm.radioCollection('reverseButtonsD', q=1, sl=1)
        for selJnt in selJntList:
            if selreAxis == 'defaultRadioButtonD':
                self.crePosereader(selJnt)
            elif selreAxis == 'xReverseRadioButtonD':
                self.crePosereader(selJnt, 'rotateX')
            elif selreAxis == 'yReverseRadioButtonD':
                self.crePosereader(selJnt, 'rotateY')
            elif selreAxis == 'zReverseRadioButtonD':
                self.crePosereader(selJnt, 'rotateZ')


    def customPoseReader(self,*args):
        selJntList = pm.textScrollList('baseJNTList', q=True, si=True)
        selreAxis = pm.radioCollection('reverseButtonsC', q=1, sl=1)
        for selJnt in selJntList:
            if selreAxis == 'defaultRadioButtonC':
                customPosereader(selJnt)
            elif selreAxis == 'xReverseRadioButtonC':
                customPosereader(selJnt, 'rotateX')
            elif selreAxis == 'yReverseRadioButtonC':
                customPosereader(selJnt, 'rotateY')
            elif selreAxis == 'zReverseRadioButtonC':
                customPosereader(selJnt, 'rotateZ')


    def crePosereader(self,name, *args):
        setList = []
        pm.select(name)
        selJnt = pm.ls(sl=True)
        parentJnt = selJnt[0].listRelatives(p=True, type='joint')
        childJnt = selJnt[0].listRelatives(c=True, type='joint')
        print childJnt
        if len(selJnt) != 1:
            pm.warnimg('Select Object or Please select one')
        else:
            locPkg = {'base': [],
            'target': [],
            'pose': []}
            for i in locPkg:
                creLoc = pm.spaceLocator(p=(0, 0, 0), n='%s_%s_hiddenLoc' % (selJnt[0], i))
                setList.append(creLoc)
                creDecomp = pm.shadingNode('decomposeMatrix', asUtility=True, n='%s_%s_DMpR' % (selJnt[0], i))
                setList.append(creDecomp)
                locPkg[i] = (creLoc, creDecomp)
                locPkg[i][0].worldMatrix >> locPkg[i][1].inputMatrix

            avergPkg = {'avergA': [],
            'avergB': []}
            for i in avergPkg:
                avergPkg[i] = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_%s_PMApR' % (selJnt[0], i))
                avergPkg[i].operation.set(2)
                setList.append(avergPkg[i])

            locPkg['base'][1].outputTranslate >> avergPkg['avergA'].input3D[0]
            locPkg['base'][1].outputTranslate >> avergPkg['avergB'].input3D[0]
            locPkg['target'][1].outputTranslate >> avergPkg['avergA'].input3D[1]
            locPkg['pose'][1].outputTranslate >> avergPkg['avergB'].input3D[1]
            creAng = pm.shadingNode('angleBetween', asUtility=True, n='%s_ABpR' % selJnt[0])
            creMulD = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_MDpR' % selJnt[0])
            creConD = pm.shadingNode('condition', asUtility=True, n='%s_CDpR' % selJnt[0])
            creSetR = pm.shadingNode('setRange', asUtility=True, n='%s_SRpR' % selJnt[0])
            creAverg = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_PMApR' % selJnt[0])
            setList.append(creAng)
            setList.append(creMulD)
            setList.append(creConD)
            setList.append(creSetR)
            setList.append(creAverg)
            avergPkg['avergA'].output3D >> creAng.vector1
            avergPkg['avergB'].output3D >> creAng.vector2
            creAng.angle >> creMulD.input1X
            creMulD.outputX >> creConD.firstTerm
            creMulD.outputX >> creConD.colorIfFalseR
            creMulD.operation.set(2)
            creConD.secondTerm.set(1)
            creConD.colorIfTrueR.set(1)
            creConD.operation.set(2)
            creSetR.oldMaxX.set(1)
            creSetR.maxX.set(1)
            creAverg.operation.set(2)
            creConD.outColorR >> creSetR.valueX
            creSetR.outValueX >> creAverg.input1D[1]
            creAverg.input1D[0].set(1)
            locPkg_t = {'base': [],
            'target': [],
            'pose': []}
            for i in locPkg_t:
                creLoc = pm.spaceLocator(p=(0, 0, 0), n='%s_%s_twist_hiddenLoc' % (selJnt[0], i))
                setList.append(creLoc)
                creDecomp = pm.shadingNode('decomposeMatrix', asUtility=True, n='%s_%s_twist_DMpR' % (selJnt[0], i))
                setList.append(creDecomp)
                locPkg_t[i] = (creLoc, creDecomp)
                locPkg_t[i][0].worldMatrix >> locPkg_t[i][1].inputMatrix

            avergPkg_t = {'avergA': [],
            'avergB': []}
            for i in avergPkg_t:
                avergPkg_t[i] = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_twist_%s_PMApR' % (selJnt[0], i))
                setList.append(avergPkg_t[i])
                avergPkg_t[i].operation.set(2)

            locPkg_t['base'][1].outputTranslate >> avergPkg_t['avergA'].input3D[0]
            locPkg_t['base'][1].outputTranslate >> avergPkg_t['avergB'].input3D[0]
            locPkg_t['target'][1].outputTranslate >> avergPkg_t['avergA'].input3D[1]
            locPkg_t['pose'][1].outputTranslate >> avergPkg_t['avergB'].input3D[1]
            creAng_t = pm.shadingNode('angleBetween', asUtility=True, n='%s_ABpR' % selJnt[0])
            creFollowCond_t = pm.shadingNode('condition', asUtility=True, n='%s_follow_CDpR' % selJnt[0])
            creMulD_t = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_MDpR' % selJnt[0])
            creConD_t = pm.shadingNode('condition', asUtility=True, n='%s_CDpR' % selJnt[0])
            creSetR_t = pm.shadingNode('setRange', asUtility=True, n='%s_SRpR' % selJnt[0])
            creAverg_t = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_PMApR' % selJnt[0])
            setList.append(creAng_t)
            setList.append(creFollowCond_t)
            setList.append(creMulD_t)
            setList.append(creConD_t)
            setList.append(creSetR_t)
            setList.append(creAverg_t)
            avergPkg_t['avergA'].output3D >> creAng_t.vector1
            avergPkg_t['avergB'].output3D >> creAng_t.vector2
            creAng_t.angle >> creFollowCond_t.colorIfTrueR
            creFollowCond_t.outColorR >> creMulD_t.input1X
            creMulD_t.outputX >> creConD_t.firstTerm
            creMulD_t.outputX >> creConD_t.colorIfFalseR
            creFollowCond_t.secondTerm.set(0)
            creFollowCond_t.colorIfFalseR.set(0)
            creMulD_t.operation.set(2)
            creConD_t.secondTerm.set(1)
            creConD_t.colorIfTrueR.set(1)
            creConD_t.operation.set(2)
            creSetR_t.oldMaxX.set(1)
            creSetR_t.maxX.set(1)
            creAverg_t.operation.set(2)
            creConD_t.outColorR >> creSetR_t.valueX
            creSetR_t.outValueX >> creAverg_t.input1D[1]
            creAverg_t.input1D[0].set(1)
            creAddAverg = pm.shadingNode('multDoubleLinear', asUtility=True, n='%s_MDLpR' % selJnt[0])
            creAddReValue = pm.shadingNode('remapValue', asUtility=True, n='%s_RMVpR' % selJnt[0])
            creAddDbL = pm.shadingNode('addDoubleLinear', asUtility=True, n='%s_ADLpR' % selJnt[0])
            setList.append(creAddAverg)
            setList.append(creAddReValue)
            setList.append(creAddDbL)
            creAddDbL.input2.set(1)
            creAverg.output1D >> creAddAverg.input1
            creAverg_t.output1D >> creAddAverg.input2
            creAddAverg.output >> creAddReValue.inputValue
            creAddDbL.output >> creAddReValue.value[0].value_Interp
            minPkg = {'posAngle': [],
            'twsitAngle': []}
            for i in minPkg:
                creMinCond = pm.shadingNode('condition', asUtility=True, n='%s_%s_CDpR' % (selJnt[0], i))
                creMinMulD = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_%s_MDpR' % (selJnt[0], i))
                creMinCondMax = pm.shadingNode('condition', asUtility=True, n='%s_%s_maxSet_CDpR' % (selJnt[0], i))
                setList.append(creMinCond)
                setList.append(creMinMulD)
                setList.append(creMinCondMax)
                minPkg[i] = (creMinCond, creMinMulD, creMinCondMax)
                minPkg[i][0].operation.set(3)
                minPkg[i][1].operation.set(2)
                minPkg[i][2].colorIfTrueR.set(0.999)
                minPkg[i][2].secondTerm.set(1)

            minPkg['posAngle'][1].outputX >> minPkg['posAngle'][2].colorIfFalseR
            minPkg['posAngle'][1].outputX >> minPkg['posAngle'][2].firstTerm
            minPkg['twsitAngle'][1].outputX >> minPkg['twsitAngle'][2].colorIfFalseR
            minPkg['twsitAngle'][1].outputX >> minPkg['twsitAngle'][2].firstTerm
            minPkg['posAngle'][2].outColorR >> creSetR.oldMinX
            minPkg['twsitAngle'][2].outColorR >> creSetR_t.oldMinX
            locPkg['target'][0].tx.set(1)
            locPkg_t['target'][0].ty.set(1)
            locPkg['target'][0].visibility.set(0)
            locPkg['pose'][0].visibility.set(0)
            locPkg_t['base'][0].visibility.set(0)
            locPkg_t['pose'][0].visibility.set(0)
            locPkg['pose'][0].tx.set(1)
            locPkg_t['pose'][0].ty.set(1)
            locPkg['base'][0].rename('%s_poseReaderLoc' % selJnt[0])
            creAnno = pm.annotate(locPkg['target'][0], tx='', p=(0, 0, 0))
            setList.append(creAnno)
            shapeLoc = locPkg['base'][0].listRelatives(type='shape')
            shapeLoc[0].visibility.set(0)
            transAnno = creAnno.listRelatives(type='transform', parent=True)
            pm.parent(creAnno, locPkg['base'][0], r=True, s=True)
            pm.delete(transAnno[0])
            pm.parent(locPkg['target'][0], locPkg['base'][0], r=True)
            pm.parent(locPkg_t['target'][0], locPkg_t['base'][0], r=True)
            pm.color(creAnno, locPkg['base'][0], rgb=(255, 0, 0))
            locPkg['base'][0].addAttr('_____', at='enum', en='POSE', k=True)
            locPkg['base'][0].addAttr('readAxis', at='enum', en='X-Axis:Y-Axis:Z-Axis', k=True)
            locPkg['base'][0].addAttr('interpMode', at='enum', en='Linear:Smooth:Curve', k=True)
            locPkg['base'][0].addAttr('minAngle', at='double', min=0, max=180, dv=0, k=True)
            locPkg['base'][0].addAttr('maxAngle', at='double', min=0, max=180, dv=90, k=True)
            locPkg['base'][0].addAttr('allowTwist', at='double', min=0, max=1, dv=1, k=True)
            locPkg['base'][0].addAttr('minTwist', at='double', min=0, max=180, dv=0, k=True)
            locPkg['base'][0].addAttr('maxTwist', at='double', min=0, max=180, dv=90, k=True)
            locPkg['base'][0].addAttr('weight', at='double', dv=0, k=True)
            locPkg['base'][0].maxAngle >> creMulD.input2X
            locPkg['base'][0].maxTwist >> creMulD_t.input2X
            locPkg['base'][0].allowTwist >> creFollowCond_t.firstTerm
            locPkg['base'][0].interpMode >> creAddDbL.input1
            locPkg['base'][0].minAngle >> minPkg['posAngle'][0].firstTerm
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][0].secondTerm
            locPkg['base'][0].minAngle >> minPkg['posAngle'][0].colorIfFalseR
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][0].colorIfTrueR
            locPkg['base'][0].minTwist >> minPkg['twsitAngle'][0].firstTerm
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][0].secondTerm
            locPkg['base'][0].minTwist >> minPkg['twsitAngle'][0].colorIfFalseR
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][0].colorIfTrueR
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][1].input2X
            minPkg['posAngle'][0].outColorR >> minPkg['posAngle'][1].input1X
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][1].input2X
            minPkg['twsitAngle'][0].outColorR >> minPkg['twsitAngle'][1].input1X
            condPkg = {'condX': [],
            'condY': [],
            'condZ': []}
            for i in condPkg:
                creAxisCond = pm.shadingNode('condition', asUtility=True, n='%s_%s_CDpR' % (selJnt[0], i))
                setList.append(creAxisCond)
                condPkg[i] = creAxisCond
                condPkg[i].colorIfTrueR.set(1)
                condPkg[i].colorIfFalseR.set(0)
                locPkg['base'][0].readAxis >> condPkg[i].firstTerm

            condPkg['condX'].secondTerm.set(0)
            condPkg['condY'].secondTerm.set(1)
            condPkg['condZ'].secondTerm.set(2)
            condPkg['condX'].outColorR >> locPkg['target'][0].translateX
            condPkg['condY'].outColorR >> locPkg['target'][0].translateY
            condPkg['condZ'].outColorR >> locPkg['target'][0].translateZ
            condPkg['condX'].outColorR >> locPkg['pose'][0].translateX
            condPkg['condY'].outColorR >> locPkg['pose'][0].translateY
            condPkg['condZ'].outColorR >> locPkg['pose'][0].translateZ
            condPkg_t = {'condX': [],
            'condY': [],
            'condZ': []}
            for i in condPkg_t:
                creAxisCond_t = pm.shadingNode('condition', asUtility=True, n='%s_twist_%s_CDpR' % (selJnt[0], i))
                setList.append(creAxisCond_t)
                condPkg_t[i] = creAxisCond_t
                condPkg_t[i].colorIfTrueR.set(1)
                condPkg_t[i].colorIfFalseR.set(0)
                locPkg['base'][0].readAxis >> condPkg_t[i].firstTerm

            condPkg_t['condX'].secondTerm.set(0)
            condPkg_t['condY'].secondTerm.set(1)
            condPkg_t['condZ'].secondTerm.set(2)
            creDb = pm.shadingNode('addDoubleLinear', asUtility=True, n='ADLpR')
            setList.append(creDb)
            condPkg_t['condX'].outColorR >> locPkg_t['target'][0].translateY
            condPkg_t['condY'].outColorR >> creDb.input1
            condPkg_t['condZ'].outColorR >> creDb.input2
            creDb.output >> locPkg_t['target'][0].translateX
            condPkg_t['condX'].outColorR >> locPkg_t['pose'][0].translateY
            creDb.output >> locPkg_t['pose'][0].translateX
            consPointBase = pm.parentConstraint(selJnt[0], locPkg['base'][0], mo=False, w=1)
            consPointBase_t = pm.parentConstraint(selJnt[0], locPkg_t['base'][0], mo=False, w=1)
            consOrientPose = pm.orientConstraint(selJnt[0], locPkg['pose'][0], mo=False, w=1)
            consOrientPose_t = pm.orientConstraint(selJnt[0], locPkg_t['pose'][0], mo=False, w=1)
            selHierConst = pm.radioCollection('hierConstButtons', q=1, sl=1)
            if selHierConst == 'hierRadioButton':
                pm.parent(locPkg['base'][0], selJnt[0], r=True)
                grpBase = pm.group(locPkg['base'][0], a=True)
                setList.append(grpBase)
                pm.rename(grpBase, locPkg['base'][0] + '_offset')
                selreAxis = pm.radioCollection('reverseButtonsD', q=1, sl=1)
                if selreAxis == 'defaultRadioButtonD':
                    pass
                else:
                    pm.setAttr(grpBase + '.' + args[0], 180)
                if parentJnt != []:
                    pm.parent(grpBase, parentJnt[0])
                pm.parent(locPkg_t['base'][0], locPkg['base'][0], r=True)
                pm.parent(locPkg['pose'][0], selJnt[0], r=True)
                pm.parent(locPkg_t['pose'][0], selJnt[0], r=True)
                grpHidden = pm.group((locPkg['pose'][0], locPkg_t['pose'][0]), a=True)
                setList.append(grpHidden)
                pm.rename(grpHidden, locPkg['pose'][0] + '_offset')
                if selreAxis == 'defaultRadioButtonD':
                    pass
                else:
                    pm.setAttr(grpHidden + '.' + args[0], 180)
                pm.parent(grpHidden, childJnt[0], a=True)
                pm.pointConstraint(selJnt[0], grpBase, mo=1, n=locPkg['base'][0] + '_pointConstraint')
                pm.pointConstraint(selJnt[0], grpHidden, mo=1, n=locPkg['pose'][0] + '_pointConstraint')
            elif selHierConst == 'constRadioButton':
                pm.parent(locPkg['base'][0], selJnt[0], r=True)
                grpBase = pm.group(locPkg['base'][0], a=True)
                setList.append(grpBase)
                pm.rename(grpBase, locPkg['base'][0] + '_offset')
                selreAxis = pm.radioCollection('reverseButtonsD', q=1, sl=1)
                if selreAxis == 'defaultRadioButtonD':
                    pass
                else:
                    pm.setAttr(grpBase + '.' + args[0], 180)
                pm.parent(grpBase, world=1)
                pm.pointConstraint(selJnt[0], grpBase, mo=1, n=locPkg['base'][0] + '_pointConstraint')
                pm.orientConstraint(parentJnt[0], grpBase, mo=1, n=locPkg['base'][0] + '_orientConstraint')
                pm.scaleConstraint(parentJnt[0], grpBase, mo=1, n=locPkg['base'][0] + '_scaleConstraint')
                pm.parent(locPkg_t['base'][0], locPkg['base'][0], r=True)
                pm.parent(locPkg['pose'][0], selJnt[0], r=True)
                pm.parent(locPkg_t['pose'][0], selJnt[0], r=True)
                grpHidden = pm.group((locPkg['pose'][0], locPkg_t['pose'][0]), a=True)
                setList.append(grpHidden)
                if selreAxis == 'defaultRadioButtonD':
                    pass
                else:
                    pm.setAttr(grpHidden + '.' + args[0], 180)
                pm.parent(grpHidden, world=1)
                pm.pointConstraint(selJnt[0], grpHidden, mo=1, n=locPkg['pose'][0] + '_pointConstraint')
                bendExist = pm.radioCollection('bendButtons', q=1, sl=1)
                if bendExist == 'bendRadioButton':
                    pm.orientConstraint(childJnt[0], grpHidden, mo=1, n=locPkg['pose'][0] + '_orientConstraint')
                elif bendExist == 'notBendRadioButton':
                    pm.orientConstraint(selJnt[0], grpHidden, mo=1, n=locPkg['pose'][0] + '_orientConstraint')
                pm.scaleConstraint(selJnt[0], grpHidden, mo=1, n=locPkg['pose'][0] + '_scaleConstraint')
                pm.rename(grpHidden, locPkg['pose'][0] + '_offset')
                grpAll = pm.group((grpBase, grpHidden), a=True)
                setList.append(grpAll)
                pm.rename(grpAll, locPkg['base'][0] + '_GRP')
            selreAxis = pm.radioCollection('reverseButtonsD', q=1, sl=1)
            if selreAxis == 'defaultRadioButtonD':
                pass
            else:
                pm.setAttr(locPkg['base'][0] + '.' + args[0], 0)
                pm.setAttr(locPkg_t['pose'][0] + '.' + args[0], 0)
                pm.setAttr(locPkg['pose'][0] + '.' + args[0], 0)
            pm.delete(consPointBase)
            pm.delete(consOrientPose)
            pm.delete(consPointBase_t)
            pm.delete(consOrientPose_t)
            creAddReValue.outValue >> locPkg['base'][0].weight
            print setList
            if pm.objExists('pR_SW_set'):
                pRset = pm.sets(setList, n=selJnt[0] + '_pR_set')
                pRallSet = pm.ls('pR_SW_set')[0]
                pm.sets(pRallSet, add=pRset)
            else:
                crePRallset = pm.sets(em=1, n='pR_SW_set')
                pRset = pm.sets(setList, n=selJnt[0] + '_pR_set')
                pm.sets(crePRallset, add=pRset)


    def customPosereader(self,name, *args):
        setList = []
        pm.select(name)
        selJnt = pm.ls(sl=True)
        followJnt = pm.ls(pm.textScrollList('followJNTList', q=True, si=True), type='joint')[0]
        parentJnt = pm.ls(pm.textScrollList('upJNTList', q=True, si=True), type='joint')[0]
        childJnt = pm.ls(pm.textScrollList('downJNTList', q=True, si=True), type='joint')[0]
        print childJnt
        if len(selJnt) != 1:
            pm.warnimg('Select Object or Please select one')
        else:
            locPkg = {'base': [],
            'target': [],
            'pose': []}
            for i in locPkg:
                creLoc = pm.spaceLocator(p=(0, 0, 0), n='%s_%s_hiddenLoc' % (selJnt[0], i))
                setList.append(creLoc)
                creDecomp = pm.shadingNode('decomposeMatrix', asUtility=True, n='%s_%s_DMpR' % (selJnt[0], i))
                setList.append(creDecomp)
                locPkg[i] = (creLoc, creDecomp)
                locPkg[i][0].worldMatrix >> locPkg[i][1].inputMatrix

            avergPkg = {'avergA': [],
            'avergB': []}
            for i in avergPkg:
                avergPkg[i] = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_%s_PMApR' % (selJnt[0], i))
                setList.append(avergPkg[i])
                avergPkg[i].operation.set(2)

            locPkg['base'][1].outputTranslate >> avergPkg['avergA'].input3D[0]
            locPkg['base'][1].outputTranslate >> avergPkg['avergB'].input3D[0]
            locPkg['target'][1].outputTranslate >> avergPkg['avergA'].input3D[1]
            locPkg['pose'][1].outputTranslate >> avergPkg['avergB'].input3D[1]
            creAng = pm.shadingNode('angleBetween', asUtility=True, n='%s_ABpR' % selJnt[0])
            creMulD = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_MDpR' % selJnt[0])
            creConD = pm.shadingNode('condition', asUtility=True, n='%s_CDpR' % selJnt[0])
            creSetR = pm.shadingNode('setRange', asUtility=True, n='%s_SRpR' % selJnt[0])
            creAverg = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_PMApR' % selJnt[0])
            setList.append(creAng)
            setList.append(creMulD)
            setList.append(creConD)
            setList.append(creSetR)
            setList.append(creAverg)
            avergPkg['avergA'].output3D >> creAng.vector1
            avergPkg['avergB'].output3D >> creAng.vector2
            creAng.angle >> creMulD.input1X
            creMulD.outputX >> creConD.firstTerm
            creMulD.outputX >> creConD.colorIfFalseR
            creMulD.operation.set(2)
            creConD.secondTerm.set(1)
            creConD.colorIfTrueR.set(1)
            creConD.operation.set(2)
            creSetR.oldMaxX.set(1)
            creSetR.maxX.set(1)
            creAverg.operation.set(2)
            creConD.outColorR >> creSetR.valueX
            creSetR.outValueX >> creAverg.input1D[1]
            creAverg.input1D[0].set(1)
            locPkg_t = {'base': [],
            'target': [],
            'pose': []}
            for i in locPkg_t:
                creLoc = pm.spaceLocator(p=(0, 0, 0), n='%s_%s_twist_hiddenLoc' % (selJnt[0], i))
                setList.append(creLoc)
                creDecomp = pm.shadingNode('decomposeMatrix', asUtility=True, n='%s_%s_twist_DMpR' % (selJnt[0], i))
                setList.append(creDecomp)
                locPkg_t[i] = (creLoc, creDecomp)
                locPkg_t[i][0].worldMatrix >> locPkg_t[i][1].inputMatrix

            avergPkg_t = {'avergA': [],
            'avergB': []}
            for i in avergPkg_t:
                avergPkg_t[i] = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_twist_%s_PMApR' % (selJnt[0], i))
                setList.append(avergPkg_t[i])
                avergPkg_t[i].operation.set(2)

            locPkg_t['base'][1].outputTranslate >> avergPkg_t['avergA'].input3D[0]
            locPkg_t['base'][1].outputTranslate >> avergPkg_t['avergB'].input3D[0]
            locPkg_t['target'][1].outputTranslate >> avergPkg_t['avergA'].input3D[1]
            locPkg_t['pose'][1].outputTranslate >> avergPkg_t['avergB'].input3D[1]
            creAng_t = pm.shadingNode('angleBetween', asUtility=True, n='%s_ABpR' % selJnt[0])
            creFollowCond_t = pm.shadingNode('condition', asUtility=True, n='%s_follow_CDpR' % selJnt[0])
            creMulD_t = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_MDpR' % selJnt[0])
            creConD_t = pm.shadingNode('condition', asUtility=True, n='%s_CDpR' % selJnt[0])
            creSetR_t = pm.shadingNode('setRange', asUtility=True, n='%s_SRpR' % selJnt[0])
            creAverg_t = pm.shadingNode('plusMinusAverage', asUtility=True, n='%s_PMApR' % selJnt[0])
            setList.append(creAng_t)
            setList.append(creFollowCond_t)
            setList.append(creMulD_t)
            setList.append(creConD_t)
            setList.append(creSetR_t)
            setList.append(creAverg_t)
            avergPkg_t['avergA'].output3D >> creAng_t.vector1
            avergPkg_t['avergB'].output3D >> creAng_t.vector2
            creAng_t.angle >> creFollowCond_t.colorIfTrueR
            creFollowCond_t.outColorR >> creMulD_t.input1X
            creMulD_t.outputX >> creConD_t.firstTerm
            creMulD_t.outputX >> creConD_t.colorIfFalseR
            creFollowCond_t.secondTerm.set(0)
            creFollowCond_t.colorIfFalseR.set(0)
            creMulD_t.operation.set(2)
            creConD_t.secondTerm.set(1)
            creConD_t.colorIfTrueR.set(1)
            creConD_t.operation.set(2)
            creSetR_t.oldMaxX.set(1)
            creSetR_t.maxX.set(1)
            creAverg_t.operation.set(2)
            creConD_t.outColorR >> creSetR_t.valueX
            creSetR_t.outValueX >> creAverg_t.input1D[1]
            creAverg_t.input1D[0].set(1)
            creAddAverg = pm.shadingNode('multDoubleLinear', asUtility=True, n='%s_MDLpR' % selJnt[0])
            creAddReValue = pm.shadingNode('remapValue', asUtility=True, n='%s_RMVpR' % selJnt[0])
            creAddDbL = pm.shadingNode('addDoubleLinear', asUtility=True, n='%s_ADLpR' % selJnt[0])
            setList.append(creAddAverg)
            setList.append(creAddReValue)
            setList.append(creAddDbL)
            creAddDbL.input2.set(1)
            creAverg.output1D >> creAddAverg.input1
            creAverg_t.output1D >> creAddAverg.input2
            creAddAverg.output >> creAddReValue.inputValue
            creAddDbL.output >> creAddReValue.value[0].value_Interp
            minPkg = {'posAngle': [],
            'twsitAngle': []}
            for i in minPkg:
                creMinCond = pm.shadingNode('condition', asUtility=True, n='%s_%s_CDpR' % (selJnt[0], i))
                creMinMulD = pm.shadingNode('multiplyDivide', asUtility=True, n='%s_%s_MDpR' % (selJnt[0], i))
                creMinCondMax = pm.shadingNode('condition', asUtility=True, n='%s_%s_maxSet_CDpR' % (selJnt[0], i))
                setList.append(creMinCond)
                setList.append(creMinMulD)
                setList.append(creMinCondMax)
                minPkg[i] = (creMinCond, creMinMulD, creMinCondMax)
                minPkg[i][0].operation.set(3)
                minPkg[i][1].operation.set(2)
                minPkg[i][2].colorIfTrueR.set(0.999)
                minPkg[i][2].secondTerm.set(1)

            minPkg['posAngle'][1].outputX >> minPkg['posAngle'][2].colorIfFalseR
            minPkg['posAngle'][1].outputX >> minPkg['posAngle'][2].firstTerm
            minPkg['twsitAngle'][1].outputX >> minPkg['twsitAngle'][2].colorIfFalseR
            minPkg['twsitAngle'][1].outputX >> minPkg['twsitAngle'][2].firstTerm
            minPkg['posAngle'][2].outColorR >> creSetR.oldMinX
            minPkg['twsitAngle'][2].outColorR >> creSetR_t.oldMinX
            locPkg['target'][0].tx.set(1)
            locPkg_t['target'][0].ty.set(1)
            locPkg['target'][0].visibility.set(0)
            locPkg['pose'][0].visibility.set(0)
            locPkg_t['base'][0].visibility.set(0)
            locPkg_t['pose'][0].visibility.set(0)
            locPkg['pose'][0].tx.set(1)
            locPkg_t['pose'][0].ty.set(1)
            locPkg['base'][0].rename('%s_poseReaderLoc' % selJnt[0])
            creAnno = pm.annotate(locPkg['target'][0], tx='', p=(0, 0, 0))
            setList.append(creAnno)
            shapeLoc = locPkg['base'][0].listRelatives(type='shape')
            shapeLoc[0].visibility.set(0)
            transAnno = creAnno.listRelatives(type='transform', parent=True)
            pm.parent(creAnno, locPkg['base'][0], r=True, s=True)
            pm.delete(transAnno[0])
            pm.parent(locPkg['target'][0], locPkg['base'][0], r=True)
            pm.parent(locPkg_t['target'][0], locPkg_t['base'][0], r=True)
            pm.color(creAnno, locPkg['base'][0], rgb=(255, 0, 0))
            locPkg['base'][0].addAttr('_____', at='enum', en='POSE', k=True)
            locPkg['base'][0].addAttr('readAxis', at='enum', en='X-Axis:Y-Axis:Z-Axis', k=True)
            locPkg['base'][0].addAttr('interpMode', at='enum', en='Linear:Smooth:Curve', k=True)
            locPkg['base'][0].addAttr('minAngle', at='double', min=0, max=180, dv=0, k=True)
            locPkg['base'][0].addAttr('maxAngle', at='double', min=0, max=180, dv=90, k=True)
            locPkg['base'][0].addAttr('allowTwist', at='double', min=0, max=1, dv=1, k=True)
            locPkg['base'][0].addAttr('minTwist', at='double', min=0, max=180, dv=0, k=True)
            locPkg['base'][0].addAttr('maxTwist', at='double', min=0, max=180, dv=90, k=True)
            locPkg['base'][0].addAttr('weight', at='double', dv=0, k=True)
            locPkg['base'][0].maxAngle >> creMulD.input2X
            locPkg['base'][0].maxTwist >> creMulD_t.input2X
            locPkg['base'][0].allowTwist >> creFollowCond_t.firstTerm
            locPkg['base'][0].interpMode >> creAddDbL.input1
            locPkg['base'][0].minAngle >> minPkg['posAngle'][0].firstTerm
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][0].secondTerm
            locPkg['base'][0].minAngle >> minPkg['posAngle'][0].colorIfFalseR
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][0].colorIfTrueR
            locPkg['base'][0].minTwist >> minPkg['twsitAngle'][0].firstTerm
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][0].secondTerm
            locPkg['base'][0].minTwist >> minPkg['twsitAngle'][0].colorIfFalseR
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][0].colorIfTrueR
            locPkg['base'][0].maxAngle >> minPkg['posAngle'][1].input2X
            minPkg['posAngle'][0].outColorR >> minPkg['posAngle'][1].input1X
            locPkg['base'][0].maxTwist >> minPkg['twsitAngle'][1].input2X
            minPkg['twsitAngle'][0].outColorR >> minPkg['twsitAngle'][1].input1X
            condPkg = {'condX': [],
            'condY': [],
            'condZ': []}
            for i in condPkg:
                creAxisCond = pm.shadingNode('condition', asUtility=True, n='%s_%s_CDpR' % (selJnt[0], i))
                setList.append(creAxisCond)
                condPkg[i] = creAxisCond
                condPkg[i].colorIfTrueR.set(1)
                condPkg[i].colorIfFalseR.set(0)
                locPkg['base'][0].readAxis >> condPkg[i].firstTerm

            condPkg['condX'].secondTerm.set(0)
            condPkg['condY'].secondTerm.set(1)
            condPkg['condZ'].secondTerm.set(2)
            condPkg['condX'].outColorR >> locPkg['target'][0].translateX
            condPkg['condY'].outColorR >> locPkg['target'][0].translateY
            condPkg['condZ'].outColorR >> locPkg['target'][0].translateZ
            condPkg['condX'].outColorR >> locPkg['pose'][0].translateX
            condPkg['condY'].outColorR >> locPkg['pose'][0].translateY
            condPkg['condZ'].outColorR >> locPkg['pose'][0].translateZ
            condPkg_t = {'condX': [],
            'condY': [],
            'condZ': []}
            for i in condPkg_t:
                creAxisCond_t = pm.shadingNode('condition', asUtility=True, n='%s_twist_%s_CDpR' % (selJnt[0], i))
                setList.append(creAxisCond_t)
                condPkg_t[i] = creAxisCond_t
                condPkg_t[i].colorIfTrueR.set(1)
                condPkg_t[i].colorIfFalseR.set(0)
                locPkg['base'][0].readAxis >> condPkg_t[i].firstTerm

            condPkg_t['condX'].secondTerm.set(0)
            condPkg_t['condY'].secondTerm.set(1)
            condPkg_t['condZ'].secondTerm.set(2)
            creDb = pm.shadingNode('addDoubleLinear', asUtility=True, n='ADLpR')
            setList.append(creDb)
            condPkg_t['condX'].outColorR >> locPkg_t['target'][0].translateY
            condPkg_t['condY'].outColorR >> creDb.input1
            condPkg_t['condZ'].outColorR >> creDb.input2
            creDb.output >> locPkg_t['target'][0].translateX
            condPkg_t['condX'].outColorR >> locPkg_t['pose'][0].translateY
            creDb.output >> locPkg_t['pose'][0].translateX
            consPointBase = pm.parentConstraint(selJnt[0], locPkg['base'][0], mo=False, w=1)
            consPointBase_t = pm.parentConstraint(selJnt[0], locPkg_t['base'][0], mo=False, w=1)
            consOrientPose = pm.orientConstraint(selJnt[0], locPkg['pose'][0], mo=False, w=1)
            consOrientPose_t = pm.orientConstraint(selJnt[0], locPkg_t['pose'][0], mo=False, w=1)
            pm.parent(locPkg['base'][0], selJnt[0], r=True)
            grpBase = pm.group(locPkg['base'][0], a=True)
            setList.append(grpBase)
            pm.rename(grpBase, locPkg['base'][0] + '_offset')
            selreAxis = pm.radioCollection('reverseButtonsC', q=1, sl=1)
            if selreAxis == 'defaultRadioButtonC':
                pass
            else:
                pm.setAttr(grpBase + '.' + args[0], 180)
            pm.parent(grpBase, world=1)
            pm.pointConstraint(followJnt, grpBase, mo=1, n=locPkg['base'][0] + '_pointConstraint')
            pm.orientConstraint(parentJnt, grpBase, mo=1, n=locPkg['base'][0] + '_orientConstraint')
            pm.scaleConstraint(parentJnt, grpBase, mo=1, n=locPkg['base'][0] + '_scaleConstraint')
            pm.parent(locPkg_t['base'][0], locPkg['base'][0], r=True)
            pm.parent(locPkg['pose'][0], selJnt[0], r=True)
            pm.parent(locPkg_t['pose'][0], selJnt[0], r=True)
            grpHidden = pm.group((locPkg['pose'][0], locPkg_t['pose'][0]), a=True)
            setList.append(grpHidden)
            if selreAxis == 'defaultRadioButtonC':
                pass
            else:
                pm.setAttr(grpHidden + '.' + args[0], 180)
            pm.parent(grpHidden, world=1)
            pm.pointConstraint(followJnt, grpHidden, mo=1, n=locPkg['pose'][0] + '_pointConstraint')
            pm.orientConstraint(childJnt, grpHidden, mo=1, n=locPkg['pose'][0] + '_orientConstraint')
            pm.scaleConstraint(followJnt, grpHidden, mo=1, n=locPkg['pose'][0] + '_scaleConstraint')
            pm.rename(grpHidden, locPkg['pose'][0] + '_offset')
            grpAll = pm.group((grpBase, grpHidden), a=True)
            setList.append(grpAll)
            pm.rename(grpAll, locPkg['base'][0] + '_GRP')
            selreAxis = pm.radioCollection('reverseButtonsC', q=1, sl=1)
            if selreAxis == 'defaultRadioButtonC':
                pass
            else:
                pm.setAttr(locPkg['base'][0] + '.' + args[0], 0)
                pm.setAttr(locPkg_t['pose'][0] + '.' + args[0], 0)
                pm.setAttr(locPkg['pose'][0] + '.' + args[0], 0)
            pm.delete(consPointBase)
            pm.delete(consOrientPose)
            pm.delete(consPointBase_t)
            pm.delete(consOrientPose_t)
            creAddReValue.outValue >> locPkg['base'][0].weight
            print setList
            if pm.objExists('pR_SW_set'):
                pRset = pm.sets(setList, n=selJnt[0] + '_pR_set')
                pRallSet = pm.ls('pR_SW_set')[0]
                pm.sets(pRallSet, add=pRset)
            else:
                crePRallset = pm.sets(em=1, n='pR_SW_set')
                pRset = pm.sets(setList, n=selJnt[0] + '_pR_set')
                pm.sets(crePRallset, add=pRset)


    def poseReaderVisOn(self,*args):
        selPoseLOC = pm.ls('*_poseReaderLoc', '*:*_poseReaderLoc')
        for i in selPoseLOC:
            i.visibility.set(1)


    def poseReaderVisOff(self,*args):
        selPoseLOC = pm.ls('*_poseReaderLoc', '*:*_poseReaderLoc')
        for i in selPoseLOC:
            i.visibility.set(0)


    def MirrorBlendUsingWrap(self,*args):
        fN = pm.textField('searchName', query=True, text=True)
        nN = pm.textField('replaceName', query=True, text=True)
        sA = pm.setAttr
        lS = pm.ls
        axis = ['X', 'Y', 'Z']
        attrs = ['translate', 'rotate', 'scale']
        selMesh = lS(sl=1, fl=1)
        mirrorMesh = pm.duplicate(selMesh, name='mirrorMesh_' + selMesh[0])[0]
        for ax in axis:
            for attr in attrs:
                sA(mirrorMesh + '.' + attr + ax, lock=0)

        sA(mirrorMesh + '.scaleX', -1)
        pm.select(clear=True)
        pm.select(mirrorMesh, selMesh)
        mel.eval('CreateWrap;')
        for i in selMesh:
            blendList = lS(pm.listHistory(i), type='blendShape')[0]
            blendWeightList = pm.listAttr(blendList + '.w', m=True)
            bs = pm.PyNode(blendList)
            lastCnt = max(bs.weightIndexList()) + 1
            for j in blendWeightList:
                if pm.listConnections(blendList + '.' + j, c=1):
                    pm.disconnectAttr(pm.listConnections(blendList + '.' + j)[0] + '.weight', blendList + '.' + j)
                newName = j.replace(fN, nN)
                sA(blendList + '.' + j, 1)
                mirrorTarget = pm.duplicate(mirrorMesh, n=newName)[0]
                sA(mirrorTarget + '.scaleX', 1)
                pm.blendShape(blendList, edit=1, t=[selMesh[0],
                lastCnt,
                mirrorTarget,
                1.0])
                pm.delete(mirrorTarget, ch=True)
                pm.delete(mirrorTarget)
                sA(blendList + '.' + j, 0)
                lastCnt += 1

            pm.delete(mirrorMesh, ch=True)
            pm.delete(mirrorMesh)
            BaseName = i + 'Base'
            if pm.objExists(BaseName):
                pm.delete(BaseName)

        pm.select(selMesh)


    def connectPSD(self,*args):
        lS = pm.ls
        selMesh = lS(sl=1, fl=1)
        blendList = lS(pm.listHistory(selMesh), type='blendShape')[0]
        blendWeightList = pm.listAttr(blendList + '.w', m=True)
        selPRL = pm.ls('*_poseReaderLoc', type='transform')
        for i in selPRL:
            reName = i.split('_poseReaderLoc')[0]
            for j in blendWeightList:
                if reName == j:
                    if '_C_' in j:
                        pass
                    elif pm.isConnected(reName + '_poseReaderLoc.weight', blendList + '.' + j):
                        pass
                    else:
                        pm.connectAttr(reName + '_poseReaderLoc.weight', blendList + '.' + j)

        for k in blendWeightList:
            if pm.listConnections(blendList + '.' + k, c=1):
                pass
            else:
                pm.warning('poseReader name and target name are different')


    def disconnectPSD(self,*args):
        lS = pm.ls
        selMesh = lS(sl=1, fl=1)
        blendList = lS(pm.listHistory(selMesh), type='blendShape')[0]
        blendWeightList = pm.listAttr(blendList + '.w', m=True)
        selPRL = pm.ls('*_poseReaderLoc', type='transform')
        for i in selPRL:
            reName = i.split('_poseReaderLoc')[0]
            for j in blendWeightList:
                if reName in j:
                    if pm.isConnected(reName + '_poseReaderLoc.weight', blendList + '.' + j):
                        pm.disconnectAttr(reName + '_poseReaderLoc.weight', blendList + '.' + j)

