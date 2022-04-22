# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import sys
import maya.mel as mel
import pymel.core as pm

#----------------------------------------------------------------------------
# 경로설정

External_route = 'D:/KJY/python/External/' # External 폴더의 경로

#----------------------------------------------------------------------------

def kk_controllers():
    'kk_controllers 실행'
    mel.eval('source\"' + External_route +'kk_controllers/kk_controllers.mel"')



def symmetry_tool():
    'abSymMesh tool 실행'
    mel.eval('source\"' + External_route + 'abSymMesh.mel"')



class ctrlShape_color_UI(): 
    'shape의 컬러를 바꿔준다'
    def __init__(self):
        #from anyzac.rigging import ctrl_make
        windowID='ctrlShapeWindow'
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        
        cmds.window(windowID,t='ctrlShape_color', rtf=0, s=1, mnb=0, mxb=0)
        master=cmds.columnLayout()
        cmds.rowColumnLayout( nc=6, cw=[(1,25),(2,25), (3,25), (4,25), (5,25),(6,25)] )
        cmds.button(l= 're' , c= lambda x: self.ctrlShape_sel_color(0)) # defort
        cmds.button(l= 'L' ,bgc = [0,0,0] ,  c= lambda x: self.ctrlShape_sel_color(1 )) # 검정
        cmds.button(l= 'L' ,bgc = [0.251,0.251,0.251] , c=lambda x: self.ctrlShape_sel_color(2 )) # 진회색
        cmds.button(l= 'L' ,bgc = [0.6,0.6,0.6] , c=lambda x: self.ctrlShape_sel_color(3 )) # 연회색
        cmds.button(l= 'L' ,bgc = [0.608,0,0.157] , c=lambda x: self.ctrlShape_sel_color(4 )) # 진자주색
        cmds.button(l= 'L' ,bgc = [0,0.016,0.376] , c=lambda x: self.ctrlShape_sel_color(5 )) # 진파란색
        cmds.button(l= '' ,bgc = [0,0,1] , c=lambda x: self.ctrlShape_sel_color(6 )) # 파란색
        cmds.button(l= 'L' ,bgc = [0,0.274,0.098] , c=lambda x: self.ctrlShape_sel_color(7 )) # 진초록색
        cmds.button(l= 'L' ,bgc = [0.149,0,0.263] , c=lambda x: self.ctrlShape_sel_color(8 )) # 진보라색
        cmds.button(l= 'L' ,bgc = [0.784,0,0.784] , c= lambda x: self.ctrlShape_sel_color(9 )) # 분홍색
        cmds.button(l= '' ,bgc = [0.541,0.282,0.2] , c=lambda x: self.ctrlShape_sel_color(10 )) # 연갈색
        cmds.button(l= '' ,bgc = [0.247,0.137,0.122] , c=lambda x: self.ctrlShape_sel_color(11 )) # 진갈색
        cmds.button(l= '' ,bgc = [0.6,0.149,0] , c=lambda x: self.ctrlShape_sel_color(12)) # 갈색
        cmds.button(l= '' ,bgc = [1,0,0] , c=lambda x: self.ctrlShape_sel_color(13 )) # 빨간색
        cmds.button(l= '' ,bgc = [0,1,0] , c=lambda x: self.ctrlShape_sel_color(14)) # 초록색
        cmds.button(l= 'L' ,bgc = [0,0.255,0.6] , c=lambda x: self.ctrlShape_sel_color(15)) # 푸른파란색
        cmds.button(l= 'L' ,bgc = [1,1,1] , c=lambda x: self.ctrlShape_sel_color(16)) # 흰색
        cmds.button(l= '' ,bgc = [1,1,0] , c=lambda x: self.ctrlShape_sel_color(17)) #노랑색
        cmds.button(l= '' ,bgc = [0.392,0.863,1] , c=lambda x: self.ctrlShape_sel_color(18 )) # 하늘색
        cmds.button(l= 'L' ,bgc = [0.263,1,0.639] , c=lambda x: self.ctrlShape_sel_color(19 )) # 연한 크리스탈색
        cmds.button(l= '' ,bgc = [1,0.69,0.69] , c=lambda x: self.ctrlShape_sel_color(20 )) # 살색
        cmds.button(l= '' ,bgc = [0.894,0.674,0.475] , c=lambda x: self.ctrlShape_sel_color(21 )) # 진한 살색
        cmds.button(l= 'L' ,bgc = [1,1,0.388] , c=lambda x: self.ctrlShape_sel_color(22 )) # 연한 노랑색
        cmds.button(l= 'L' ,bgc = [0,0.6,0.329] , c=lambda x: self.ctrlShape_sel_color(23 )) # 파스탤 진한 초록색
        cmds.button(l= '' ,bgc = [0.631,0.412,0.188] , c=lambda x: self.ctrlShape_sel_color(24 )) # 파스탤 갈색
        cmds.button(l= '' ,bgc = [0.624,0.631,0.188] , c=lambda x: self.ctrlShape_sel_color(25 )) # 파스탤 노+초
        cmds.button(l= '' ,bgc = [0.408,0.631,0.188] , c=lambda x: self.ctrlShape_sel_color(26 )) # 파스탤 풀색
        cmds.button(l= '' ,bgc = [0.188,0.631,0.365] , c=lambda x: self.ctrlShape_sel_color(27 )) # 파스탤 파+초
        cmds.button(l= '' ,bgc = [0.188,0.631,0.631] , c=lambda x: self.ctrlShape_sel_color(28 )) # 파스탤 연한 파란색
        cmds.button(l= '' ,bgc = [0.188,0.404,0.631] , c=lambda x: self.ctrlShape_sel_color(29 )) # 파스탤 진한 파란색
        cmds.button(l= '' ,bgc = [0.435,0.188,0.631] , c=lambda x: self.ctrlShape_sel_color(30 )) # 보라색
        cmds.button(l= '' ,bgc = [0.631,0.188,0.412] , c=lambda x: self.ctrlShape_sel_color(31 )) # 진한 분홍색


        cmds.showWindow(windowID)


    def ctrlShape_sel_color(self, n ):
        a= cmds.ls(sl=1)
        for c in a:
            sel_curveShape = cmds.listRelatives( c , c = 1, pa=1, typ= 'shape')
            for curveShape in sel_curveShape:
                if cmds.objectType(curveShape) == 'nurbsCurve':
                    if n == False :
                        cmds.setAttr(curveShape + '.overrideEnabled' , 0)
                        cmds.setAttr(curveShape + '.overrideColor' , 1)
                    else:
                        cmds.setAttr(curveShape + '.overrideEnabled' , 1)
                        cmds.setAttr(curveShape + '.overrideColor' , n)
                else :
                    pass



class connect_tool():
    '커넥트, 컨스트레인 툴'
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



class mel_to_python():
    def __init__(self):
        '''

        melToPymelUI v1.0

        Convert MEL code to Python code. The script is based on the function mel2py.mel2pyStr plus some modifications for formatting

        Install/Use:
        1. Copy this script to your Maya script folder : C:\Users\Your_Username\Documents\maya\scripts
        2. To open the UI run the following code in Maya's Python script editor window
        3. Copy the MEL code into the top window and click convert
        4. Find the resulting Python code in the bottom window, copy and paste it into the script editor of your choice

        import melToPymelUI as melToPymelUI
        reload(melToPymelUI)
        melToPymelUI.UI()


        created by Monika Gelbmann
        07/2019
        '''

        import sys

        # Seeing as this can be loaded in either Maya 2016 or 2017,
        # the first thing I need to do is check if PySide2 is loaded.
        # If it's not, there's no need to make any changes
        if 'PySide2' in sys.modules:
            # Repath PySide and shiboken so scripts can still call "import PySide"
            # By doing this in the sys.modules I can ensure this is going to affect all my scripts
            # and not just this single one
            sys.modules['PySide'] = sys.modules['PySide2']

            # Shiboken and pyside2uic also needed repathing
            sys.modules['shiboken'] = sys.modules['shiboken2']

            # I bring in pyside2uic to make sure it's in the sys.modules before I repath it
            import pyside2uic

            sys.modules['pysideuic'] = sys.modules['pyside2uic']

            # I add entries in the modules dict that point to the new locations...
            sys.modules['PySide.QtGui'] = sys.modules['PySide2.QtGui']
            sys.modules['PySide.QtCore'] = sys.modules['PySide2.QtCore']

            # Now because all our old scripts will still be looking in QtGui for all the QWidgets
            # I need to merge the new QtWidgets module into the PySide.QtGui module. I do this by
            # using the dictionary.update() method.
            sys.modules["PySide.QtGui"].__dict__.update(
                sys.modules["PySide2.QtWidgets"].__dict__)

            # I found after running some of my tools that anything that used Custom Widgets that had been
            # generated by pyside-uic, that the old flag PySide.QtGui.QApplication.UnicodeUTF8 had been replaced
            # with a simple '-1'.
            # To get around this I used the setattr method (you cannot edit dict_proxy objects,
            # which sys.modules["PySide.QtGui"].QApplication returns as) to replace the flag with -1
            # ensuring that the custom widget still built in PySide2
            import PySide
            from PySide import QtGui, QtCore, QtWidgets

            setattr(sys.modules["PySide.QtGui"], "QApplication",
                    sys.modules["PySide2.QtWidgets"].QApplication)
            setattr(sys.modules["PySide.QtGui"].QApplication, "UnicodeUTF8", -1)

            # I found a couple more little changes as I went along...
            setattr(sys.modules["PySide.QtGui"], "QSortFilterProxyModel",
                    sys.modules["PySide2.QtCore"].QSortFilterProxyModel)
            setattr(sys.modules["PySide.QtGui"].QHeaderView, "setResizeMode",
                    sys.modules["PySide2.QtWidgets"].QHeaderView.setSectionResizeMode)

        from PySide import QtGui
        import maya.OpenMayaUI as mui
        import shiboken
        import pymel.core as pm
        import pymel.tools.mel2py as mel2py

        textbox_out = ''
        
            
        # 실행문
        import melToPymelUI as melToPymelUI
        reload(melToPymelUI)
        melToPymelUI.UI()


    def getMayaWin():
        pointer = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(pointer), QtGui.QWidget)


    def convert(meltext):
        try:
            pmAnswer = mel2py.mel2pyStr(meltext, pymelNamespace='pm')
            # get rid of old all
            pmCode = pmAnswer.replace("pymel.all", "pymel.core")
            pmCode = pmCode.replace("pm.pm.cmds.", "pm.")
            print(pmCode)
            global textbox_out
            textbox_out.setPlainText(pmCode)
        except:
            pmCode = '## Error converting ##\n## Check Script Editor for details ##'
            textbox_out.setPlainText(pmCode)
            raise
        return pmCode


    def UI():
        ui_name = "ui_window"
        # check existing
        if pm.window(ui_name, exists=True):
            pm.deleteUI(ui_name, wnd=True)
        # window
        ui_parent = getMayaWin()
        ui_window = QtGui.QMainWindow(ui_parent)
        ui_window.setObjectName(ui_name)
        ui_window.setFixedWidth(800)

        # widget
        ui_widget = QtGui.QWidget()
        ui_window.setCentralWidget(ui_widget)

        # layout
        ui_layout = QtGui.QVBoxLayout(ui_widget)

        # create font
        ui_font = QtGui.QFont()
        ui_font.setPointSize(12)
        ui_font.setBold(False)
        code_font = QtGui.QFont()
        code_font.setFamily("Courier")
        code_font.setPointSize(8)

        # textbox
        textbox_in = QtGui.QTextEdit()
        textbox_in.resize(480, 280)
        textbox_in.setFont(code_font)
        ui_layout.addWidget(textbox_in)
        # textbox
        global textbox_out
        textbox_out = QtGui.QTextEdit()
        textbox_out.resize(480, 280)
        textbox_out.setFont(code_font)
        ui_layout.addWidget(textbox_out)

        # button
        ui_button_convert = QtGui.QPushButton(" Convert ")
        ui_layout.addWidget(ui_button_convert)
        ui_button_convert.setFont(ui_font)

        ui_button_convert.setStyleSheet("background-color: rgb(33,55,55);")
        ui_button_convert.clicked.connect(lambda: convert(textbox_in.toPlainText())
                                        )

        ui_window.show()

        # @classmethod
        # def showUI(cls):
        #     ins = cls()
        #     ins.UI()

