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

