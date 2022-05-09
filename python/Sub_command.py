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