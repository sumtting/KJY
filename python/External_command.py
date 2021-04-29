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