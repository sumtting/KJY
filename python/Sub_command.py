# -*- coding: utf-8 -*- 
import maya.mel as mel
import maya.OpenMaya as om
import re
from maya import OpenMaya, cmds
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
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


##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [copy]


def constraint_copy() :
    # 원본 MOD(리깅안된상태) + RIG 그룹이 갖춰진상태에서 
    # 리깅이 완성돼있는 씬을 레퍼런스로 불러온뒤 레퍼런스의 MOD그룹을 선택하고 스크립트 실행을 하면 
    # 레퍼런스 MOD -> 원본MOD로 컨스트레인 리깅을 옮길수있다.
    # 컨스트레인리깅을 옮길때 사용 *
    
    sel_mod_grp = cmds.ls(sl=1) # 레퍼런스(컨스트레인 리깅이 되어있는)로 불러온 MOD최상위 그룹을 선택
    reference_mod = cmds.listRelatives( sel_mod_grp, allDescendents=True ) # 선택한 MOD그룹의 하위항목을 모두쿼리(컨스트레인 포함)

    for reference_mod_ in reference_mod:
        if 'Constraint' in reference_mod_: # 위에서 쿼리한 항목중 Constraint이 포함된 항목만 다시 쿼리
            
            
            if cmds.objectType(reference_mod_) == 'parentConstraint' : # 오브젝트 타입이 parentConstraint 이면
                find_constraint = reference_mod_.split(':')[-1] # 스플릿으로 레퍼런스의 네임스페이스 삭제
                
                find_mod = find_constraint.split('_parentConstraint')[0] # 스플릿으로 컨스트레인이 걸려있는 모델링의 네임만 쿼리
                
                target_controller = cmds.parentConstraint(reference_mod_ , targetList=1, q=1)[0] # 컨스트레인을 걸고있는 컨트롤러 쿼리
                find_target_controller = target_controller.split(':')[-1] # 마찬가지로 스플릿을 이용해 레퍼런스 네임스페이스 삭제
                
                try:
                    cmds.parentConstraint( find_target_controller, find_mod, mo=1, w=1 ) # 다시 원본씬에서 컨스트레인을 똑같이 걸어준다
                except:
                    pass
            
            elif cmds.objectType(reference_mod_) == 'scaleConstraint' :
                find_constraint = reference_mod_.split(':')[-1]
                
                find_mod = find_constraint.split('_scaleConstraint')[0]
                
                
                target_controller = cmds.scaleConstraint(reference_mod_ , targetList=1, q=1)[0]
                find_target_controller = target_controller.split(':')[-1]
                
                try:
                    cmds.scaleConstraint( find_target_controller, find_mod, mo=1, w=1 )
                except:
                    pass
                
            elif cmds.objectType(reference_mod_) == 'pointConstraint' :
                find_constraint = reference_mod_.split(':')[-1]
                
                find_mod = find_constraint.split('_pointConstraint')[0]
                
                
                target_controller = cmds.pointConstraint(reference_mod_ , targetList=1, q=1)[0]
                find_target_controller = target_controller.split(':')[-1]
                
                try:
                    cmds.pointConstraint( find_target_controller, find_mod, mo=1, w=1 )
                except:
                    pass
                
            elif cmds.objectType(reference_mod_) == 'orientConstraint' : 
                find_constraint = reference_mod_.split(':')[-1]
                
                find_mod = find_constraint.split('_orientConstraint')[0]
                
            
                target_controller = cmds.orientConstraint(reference_mod_ , targetList=1, q=1)[0]   
                find_target_controller = target_controller.split(':')[-1]   
                
                try:
                    cmds.orientConstraint( find_target_controller, find_mod, mo=1, w=1 )
                except:
                    pass
                
            elif cmds.objectType(reference_mod_) == 'aimConstraint' :  
                find_constraint = reference_mod_.split(':')[-1]
                
                find_mod = find_constraint.split('_aimConstraint')[0]
                
            
                target_controller = cmds.aimConstraint(reference_mod_ , targetList=1, q=1)[0]    
                find_target_controller = target_controller.split(':')[-1]
                
                try:
                    cmds.aimConstraint( find_target_controller, find_mod, mo=1, w=1 )
                except:
                    pass  
                
            else:
                pass



def LR_copy(): # 선택한 컨트롤러의 어트리뷰트 값을 반대편 컨트롤러로 copy

    sel_list = cmds.ls(sl=1) # 선택한 컨트롤러 리스트
    sel_list_revers = [] 

    for sel in sel_list: # 선택한 컨트롤러의 반대편 리스트를 만들어준다 (ex. L -> R)
        if '_L_' in sel:
            sel_revers = sel.replace('_L_', '_R_')
            sel_list_revers.append(sel_revers)


        elif '_R_' in sel:
            sel_revers = sel.replace('_R_', '_L_')
            sel_list_revers.append(sel_revers)

    
    for sel, sel_reverse in zip(sel_list, sel_list_revers): # 선택한 컨트롤러에서 반대편 컨트롤러로 값을 옮겨준다.
        sel_keyable = cmds.listAttr(sel, k=1) # keyable 상태인 어트리뷰트만 쿼리
        sel_reverse_keyable = cmds.listAttr(sel_reverse, k=1)
        
        for attr in sel_keyable:
            sel_attr = cmds.getAttr(sel + '.' + attr) # 위에서 쿼리한 어트리뷰트의 값을 추출
            sel_reverse_attr = cmds.setAttr(sel_reverse + '.' + attr , sel_attr) # 반대편 컨트롤러 어트리뷰트에 추출한 값을 똑같이 넣어준다



def reference_copy():
    '레퍼런스 -> 원본오브젝트로 바인드 및 스킨카피(name동일해야함)'

    reference_objs = cmds.ls(sl=1) # 레퍼런스 오브젝트만 선택(스킨이 되어있는)
    
    for reference_obj in reference_objs:
        
        ori_obj = reference_obj.split(':')[-1] # 레퍼런스 오브젝트를 스플릿 ':'으로 나눠주어 오리지날 오브젝트를 추출
            
        reference_skincluster=mel.eval('findRelatedSkinCluster(\"' + reference_obj + '\")')
        reference_joint = cmds.skinCluster( reference_skincluster, q=1,inf=1) # 선택한 레퍼런스 오브젝트에 스킨된 조인트 추출
        reference_skin_method = cmds.skinCluster(reference_skincluster , q=1, sm=1) # 스킨매소드 추출(클래식,듀얼,웨이트블렌드)

        ori_joint_list = []

        try: 
            for i in reference_joint:
                ori_joint = i.split(':')[-1] # 위에서 뽑은 레퍼런스조인트를 이용하여 원본 조인트 추출
                
                ori_joint_list.append(ori_joint)
                
                
            cmds.skinCluster( ori_joint_list , ori_obj ,tsb = 1, sm = reference_skin_method ) # 원본조인트->원본오브젝트 바인드
            
            cmds.copySkinWeights(reference_obj,ori_obj, noMirror =1,surfaceAssociation ='closestPoint',influenceAssociation ='closestJoint') # 레퍼런스->원본 스킨카피
        
        except:
            pass



def blend_copy():
    '새로운 오브젝트에 기존블렌드타겟을 카피 및 블렌드적용'
    sels = cmds.ls(sl=1)

    new_obj = sels[0]
    ori_obj = sels[1]

    new_shape = cmds.listRelatives(new_obj, shapes =1, children=1)[0]
    ori_shape = cmds.listRelatives(ori_obj, shapes =1, children=1)[0]

    cmds.CreateWrap(new_obj)

    #블렌드쉐입의 노드 추출
    object_= ori_obj
    deform_list = cmds.findDeformers(object_ )
    blend_deform_list = []
    for deform in deform_list:
        if cmds.objectType(deform) == 'blendShape':
            blend_deform_list.append(deform)
            
        else:
            pass
    

    blend_node = blend_deform_list[0]
    blend_weight = cmds.getAttr(blend_node + '.weight')[0]

    blend_target_list = cmds.listAttr (blend_node + ".w", m=1) # 블랜드타겟 리스트

    blend_combi_list = []
    ori_combination_node_list = []
    new_combination_node_list = []
    combination_connect_info_list = []
    for i in blend_target_list: 
        attr_settable = cmds.getAttr(blend_node + '.' + i, settable=1) # 어트리뷰트가 아무것도 연결되어있지 않은것들만 반환(setAttr에 의해 설정 가능한 attr)
        if attr_settable == False: # 위의 경우가 아니라면 (어트리뷰트에 어떠한 연결(connect)이 되어있는상태), 블렌드 콤비네이션을 쿼리하기 위함
            blend_combi_name =  (blend_node + '.' + i) # 블렌드노드이름 + 콤비네이션 네임 쿼리
            combination_node = cmds.listConnections( blend_node,  t='combinationShape', d=False, s=True )[0] # 블렌드노드와 연결된 콤비네이션쉐입 노드만 쿼리
            combination_target = cmds.listConnections( combination_node,  t='blendShape', p=True, d=False, s=True )[0] # 콤비네이션된 블렌드타겟 쿼리

            combination_connect_info = cmds.listConnections( combination_node, p=True, d=False, s=True ) #콤비네이션에 연결된 베이스타겟들을 쿼리
            
            new_combination_node = cmds.duplicate( combination_node )[0]

            ori_combination_node_list.append(combination_node) # 기존의 콤비네이션노드 리스트

            blend_combi_list.append(blend_combi_name)
            new_combination_node_list.append(new_combination_node)
            combination_connect_info_list.append(combination_connect_info)
            
            cmds.disconnectAttr(combination_node + '.outputWeight' , blend_combi_name) # 콤비네이션 노드의 커넥션을 끊어준다(블렌드카피 할때 커넥션된게 없어야하기 때문)
            # 마지막에 다시 재연결시켜준다
   

    new_target_list = []
    new_target_sh_list = []
    main_target_list = []
    inbetween_target_list = []


    blend_node = pm.PyNode(blend_deform_list[0])
    blend_number = blend_node.weightIndexList()

    blend_number_list = range(len(blend_number))

    for list_num,num,a in zip(blend_number_list,blend_number,blend_weight):  #블렌드타겟의 갯수, 블렌드타겟의 웨이트값
    
        target_weight_list = blend_node.targetItemIndexList(num, ori_shape) # 타겟의 웨이트값을 구함 (0은 5000, 1은 6000으로 표기됨)
        target_amount = len(target_weight_list)
        
        for i in target_weight_list:
            
            if i == 6000:
                appendValue = float(1)
                # 이프문이 충족될시 0.i 값을 플룻처리
            else:
                if str(i)[-1] == '0':
                    i_final = str(i)[:-1] # 인비트윈 밸류값의 맨 뒷자리수가 0이라면 제거해준다(ex: 750 -> 75)
                    if str(i_final)[-1] == '0':
                        i_final_final = str(i_final)[:-1]
                        new_i = int(i_final_final[1:]) #첫째자리의 5를 삭제해준다                
                        appendValue = float('%d.%d'%( 0 , new_i)) #0.을 앞에 추가해준다.
                        ## 이프문이 충족하지않을시 어펜드 벨류값은 플룻(1)
                    
                    else:
                    
                        new_i = int(i_final[1:]) #첫째자리의 5를 삭제해준다                
                        appendValue = float('%d.%d'%( 0 , new_i)) #0.을 앞에 추가해준다.
                            ## 이프문이 충족하지않을시 어펜드 벨류값은 플룻(1)
                    
                else:
                    new_i = int(str(i)[1:]) #첫째자리의 5를 삭제해준다
                    
                    appendValue = float('%d.%d'%( 0 , new_i)) #0.을 앞에 추가해준다.
                    ## 이프문이 충족하지않을시 어펜드 벨류값은 플룻(1)


            cmds.setAttr(blend_node + '.weight' + '[%d]'%(num) , appendValue) # 블랜드타겟의 웨이트를 1로 설정
            new_target = cmds.duplicate(new_obj, n=blend_target_list[list_num] + '_' + str(appendValue))[0] # 기존 블랜드타겟의 네이밍을 따서 새로운 타겟복사
            cmds.setAttr(blend_node + '.weight' + '[%d]'%(num) , 0) # 블랜드타겟의 웨이트를 다시 0으로 설정
            
            
            if '_1_0' in new_target:
                main_target = cmds.ls(blend_target_list[list_num] + '_1_0' )[0] #메인 블렌드타겟 추출
                main_target_list.append(main_target)
                
                
            elif '_0_' in new_target:
                inbetween_target = cmds.ls(blend_target_list[list_num] + '_0_' + '%s'%(new_i))[0] #인비트윈 블렌드타겟 추출
                inbetween_target_list.append(inbetween_target)
                
                
            else:
                pass

            
    custom_target = []
    for i in main_target_list:
        re = i.split('_1_0')[0]
    
        sel_re = cmds.ls(re)
        if len(sel_re) > 0 :
            custom_target.append(re)
        
        else:
            pass
    

    # 이대로 진행하면 블렌드쉐입의 네이밍에 '_1_0'이 들어가므로 리네임을 해준다.
    main_target_list_re = []
    for i in main_target_list:
        re = i.split('_1_0')[0]
    
        sel_re = cmds.ls(re)
        # if len(sel_re) > 0 :
        #     cmds.delete(i)
        
        # else:
        cmds.rename(i,re)
        main_target_list_re.append(re)

    sel_main_target = cmds.ls(main_target_list_re)

    sels = cmds.ls(sel_main_target)
    d=[]
    for sel in sels: 
        if '|' in sel: #매치네임이 있다면
            g = sel.split('|')
            k=g[-1]
            d.append(k) #중복된 오브젝트 리스트
               
        else:
            pass
            
    t=set([x for x in d if d.count(x) > 1])
    j=list(t)
    k=cmds.ls(j)
             
    overlap_target = d[0::2] # 중복된 오브젝트가 두개씩 짝지어 모두 출력되므로 홀수번째 자리만 출력

    for list_tar_remove in k: #타겟리스트에서 중복된타겟들은 리스트에서 제외시킨다.
        sel_main_target.remove(list_tar_remove)

    for count_ in overlap_target: #기존에 타겟이 남아있는 블렌드쉐입은 새로운 타겟이 필요없기때문에 새로생성된 타겟을 지워준다.
        
        sel_target = '|' + count_
        
        try:
            cmds.delete(sel_target)
        
        except:
            pass


    cmds.select( sel_main_target,new_obj)
    cmds.blendShape(n='new_' + blend_node)
    cmds.select(cl=1)

    # 새로운 블렌드쉐입의 노드 추출
    new_deform_list = cmds.findDeformers(new_obj)
    new_blend_deform_list = []
    for new_deform in new_deform_list:
        if cmds.objectType(new_deform) == 'blendShape':
            new_blend_deform_list.append(new_deform)
    new_blend_node = new_blend_deform_list[0]


    main_num = len(main_target_list_re)
    main_num_list = range(0,main_num)

    inbet_list = []

    for list_num,num,a in zip(blend_number_list,blend_number,blend_weight):  #블렌드타겟의 갯수, 블렌드타겟의 웨이트값

        target_weight_list = blend_node.targetItemIndexList(num, ori_shape) # 타겟의 웨이트값을 구함 (0은 5000, 1은 6000으로 표기됨)
        target_amount = len(target_weight_list)
        target_weight_list.pop()
        
        inbetween_value_list = []

        if target_weight_list >1 :
        
            for inbetween in target_weight_list :
                
                new_inbetween = int(str(inbetween)[1:]) #첫째자리의 5를 삭제해준다
                inbetween_value = float('%d.%d'%( 0 , new_inbetween)) #0.을 앞에 추가해준다.
                inbetween_value_list.append(inbetween_value)
                
        else:
            pass
                
        inbet_list.append(inbetween_value_list)
    count_target = len(main_target_list_re)
    
    for main_num, inbet_wei in enumerate(inbet_list):
        #print main_num,inbet_wei

        if len(inbet_wei) >= 1:
            #print main_num
            #print main_target_list_re
            inbet_main_target = cmds.ls(main_target_list_re[main_num])[0]
            for inbet_weight in inbet_wei:
                
                re_ = '%s'%(inbet_weight)
                inbet_weight_num = re_.split(".")[1]
                
                inbetween_ = cmds.ls('%s_0_%s'%(inbet_main_target,inbet_weight_num))
                inbetween_shape = cmds.listRelatives(inbetween_, shapes =1, children=1)[0]
                
                cmds.blendShape(new_blend_node, e=1, ib=1, tc=1, ibt= 'absolute', t=(new_shape, main_num ,inbetween_shape, inbet_weight))
                
        else:
            pass
    
    for combi_name, combi_node, combination_connect_info in zip(blend_combi_list, new_combination_node_list, combination_connect_info_list) :
        # 콤비네이션 블렌드 타겟네임과 거기에 연결된 베이스 타겟네임, 콤비네이션쉐입노드 쿼리 
        cmds.connectAttr('%s.outputWeight'%(combi_node), 'new_%s'%(combi_name))
        for num, combi_target in enumerate(combination_connect_info): 
            cmds.connectAttr('new_%s'%(combi_target), '%s'%(combi_node) + '.inputWeight[%s]'%(num))
            # 새로운 블렌드쉐입과 콤비네이션 노드를 연결을 해준다 (new_는 새로만든 블렌드쉐입 네임과 맞추기위함)

    for combi_sh,combi_target in zip(ori_combination_node_list, blend_combi_list): # 기존에 콤비네이션타겟을 재연결(블렌드 카피때문에 연결을 끊어두었기 때문)
        cmds.connectAttr(combi_sh + '.outputWeight', combi_target)

    
    main_target_list_re = list(set(main_target_list_re) - set(custom_target))

    #new_GRP = cmds.group( main_target_list_re, inbetween_target_list, n='new_target_GRP' )
    
    new_GRP = cmds.group(em=1, n='new_target_GRP' )
    
    for i in main_target_list_re:
        cmds.parent(i, new_GRP)

    try:
        for i in inbetween_target_list:
            cmds.parent(i, new_GRP)
    except:
        pass

    new_GRP_pa = cmds.listRelatives(new_GRP,p=1)
    if not new_GRP_pa == None:
        cmds.parent(new_GRP, w=1) # new_target 그룹을 아웃라이너 가장 바깥으로 빼줌
    else:
        pass

    find_deform_list = cmds.findDeformers(new_obj)
    wrap_deform_list = []
    for wrap_deform in find_deform_list:
        if cmds.objectType(wrap_deform) == 'wrap':
            wrap_deform_list.append(wrap_deform)
            
        else:
            pass
            
    new_obj_wrap = wrap_deform_list[0]
    cmds.delete (new_obj_wrap)
    cmds.delete (new_GRP) # 타켓그룹을 지워준다


##-------------------------------------------------------------------------------------------------------------------------------------------------------

mel_route = 'D:/KJY/python/mel/' # mel 폴더의 경로

def tex_manager():
    # file tex manager 실행
    mel.eval('source\"' + mel_route +'FileTextureManager_2018.mel"')