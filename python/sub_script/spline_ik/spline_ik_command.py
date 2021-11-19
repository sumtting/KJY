# -*- coding: utf-8 -*- 
import maya.cmds as cmds



def spline_ik_UI():
    ## 윈도우 ID##
    windowID='spline_ik'
    ##windows reset
    if cmds.window(windowID, ex=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, t='spline_ik', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
    ##master layer
    master = cmds.columnLayout()
    cmds.columnLayout()
    
    cmds.rowColumnLayout( nr=1 )

    # cmds.checkBox( 'rev_check', l = u'좌우 동시생성' , v=True )
    cmds.text(l = '    ')
    cmds.text(l = u'컨트롤러 갯수' ,w = 70)
    cmds.text(l = '      ')
    cmds.intField('CTL_textbox' , w = 30 , h = 20 ,v=5)
    cmds.text(l = '                     ')
    #stretch_checkbox = cmds.checkBox ( l = 'stretch' , w = 55 , v = 0 )
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = u'start_joint' ,w = 100)
    cmds.textField('start_joint_textbox' , w = 100 , h = 20 , tx = 'joint1')
    cmds.button( l = u'등록' , w = 50 , c = 'spline_ik_command.sels_object_tex("st_sel")')
    cmds.setParent (master)
    cmds.rowColumnLayout( nr=1 )
    cmds.text(l = u'stretch_CTL' ,w = 100)
    cmds.textField('stretch_CTL_textbox' , w = 100 , h = 20 )
    cmds.button( l = u'등록' , w = 50 , c = 'spline_ik_command.sels_object_tex("stretch_CTL")')
    cmds.setParent (master)
    cmds.button(l=u'연결' , w = 251 , h = 30 , c = 'spline_ik_command.spline_ik_execute()')
    cmds.setParent (master)
    cmds.showWindow(windowID)



def sels_object_tex(part):
    sels = cmds.ls(sl=1)
    if part=="st_sel":cmds.textField('start_joint_textbox' , edit =1, tx= sels[0] )
    if part=="stretch_CTL":cmds.textField('stretch_CTL_textbox' , edit =1, tx= sels[0] )
    # if part=="target_sel":cmds.textField('target_tex_box' , edit =1, tx= sels[0] )




def cv_vtx_count(cv_transform):
    #커브의 버택스 len 을 리턴한다
    vtx_count= len(cmds.ls(cv_transform + '.cv[:]', fl=1))
    return vtx_count

def cv_rebild(cv_transform,vtx_cn):
    #커브를 리빌드한다
    cmds.rebuildCurve (cv_transform , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 , s = vtx_cn-1 , d = 3 , tol = 0.01)
    
    
    cn = cv_vtx_count(cv_transform)
    vtx_list = []
    for i in range(cn):
        cv_vtx='%s%s%s%s'%(cv_transform,'.cv[',0+i,']')
        vtx_list.append(cv_vtx)
    # 커브의 1,-2번째의 버텍스를 지워준다.
    cmds.delete(vtx_list[-2])
    cmds.delete(vtx_list[1])
    return cv_transform

def hir_return(transform):
    '네이밍 정렬하여 트랜스폼의 자식 손자 모든 하위구조를 리턴'
    hir_lst = [transform]
    hir_cn = cmds.listRelatives(transform, ad = 1, pa=1, type='joint')
    hir_cn.sort()
    for i in hir_cn:
        hir_lst.append(i)
    return hir_lst


def spn_ik_handle_cr(st_jnt,cv_vtx_cn):
    global cv_rename
    
    jnt_hir = hir_return(st_jnt)
    ed_jnt = jnt_hir[-1]
    
    
    '스플라인 핸들을 생성 핸들 커브 이팩트를 리턴'
    ###스타트조인트/엔드조인트 / 커브버택스 카운트시작 끝점을 뺀다 예시 > 5포인트를만들고 싶을시 시작 끝점을뺀 3을넣으면된다
    spn_cr = cmds.ikHandle(sj = st_jnt , ee = ed_jnt , sol = 'ikSplineSolver' , ns = cv_vtx_cn , n = st_jnt+'_splineIK_handle')
    effect_rename = cmds.rename(spn_cr[1] , spn_cr[0]+'_effector')
    cv_rename = cmds.rename(spn_cr[2] , spn_cr[0]+'_curve')
    ###리턴값은 : 스플라인 ik 핸들 / 스플라인커브 / 스플라인 이팩트
    #return {'handle': spn_cr[0], 'cv': cv_rename , 'effe': effect_rename}
    cv_rebild(cv_rename,cv_vtx_cn)
    re_vtx_count = cv_vtx_count(cv_rename)
    for re_count in range(re_vtx_count):
        vtx_po = cmds.xform( (cv_rename+'.cv[%s]' %(re_count)), q=1,ws=1,t=1)
        loc_cre = cmds.spaceLocator(n = '%s_%02d_%s'%(cv_rename ,re_count+1 ,'pin_loc'))
        cmds.xform(loc_cre,ws=1,t=vtx_po)
        
    return cv_rename
        
    
    
def stretch_set(stretch_CTL, start_jnt):
    cmds.addAttr(stretch_CTL, ln = 'stretch', at='double', attributeType='float', keyable=1, min=0, max=1, dv=0) #CTL에 stretch 어트리뷰트 추가
    
    cv_rename_sh = cmds.listRelatives(cv_rename,shapes=1)[0]
    
    cureve_info = cmds.createNode('curveInfo', n=cv_rename+'_curveInfo')
    cmds.connectAttr(cv_rename_sh + '.worldSpace[0]', cureve_info + '.inputCurve')
    set_range = cmds.createNode('setRange', n=cv_rename+'_setRange')
    arc_length = cmds.getAttr(cureve_info + '.arcLength')
    cmds.setAttr(set_range + '.maxX' , arc_length)
    cmds.connectAttr(stretch_CTL + '.stretch', set_range + '.valueX')
    cmds.connectAttr(cureve_info + '.arcLength', set_range + '.minX')
    cmds.setAttr(set_range + '.oldMaxX' , 1)
    multi = cmds.createNode('multiplyDivide', n=cv_rename + '_multiplyDivide')
    cmds.setAttr(multi + '.operation',2)
    cmds.connectAttr(cureve_info + '.arcLength', multi + '.input1X')
    cmds.connectAttr(set_range + '.outValueX', multi + '.input2X')
    
    st_jnt_list = hir_return(start_jnt)
    del st_jnt_list[-1]

    for st_jnt in st_jnt_list:
       cmds.connectAttr(multi + '.outputX', st_jnt + '.scaleX')    
    



def spline_ik_execute():

    ## ui 쿼리값
    CTL_amount =  cmds.intField('CTL_textbox' ,q = 1 , v=True)
    start_JNT = cmds.textField('start_joint_textbox' , q = 1 , text = True )

    spn_ik_handle_cr(start_JNT,CTL_amount)

    #ui_stretch_checkbox = cmds.checkBox( stretch_checkbox , q=True , v=1 )

    #if ui_stretch_checkbox == True:spline_ik_command.stretch_set(start_JNT)
  


    
#stretch_set('nurbsCircle1','joint1')

  
    







