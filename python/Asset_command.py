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
# [asset]

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