# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import sys
import maya.mel as mel
import string 
import pymel.core as pm


##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [move]

def rotate_xform(transform):
    'world rotate 추출'
    return cmds.xform(transform, q=1, ws=1, ro=1)



def position_xform(transform):
    'world position 추출'
    return cmds.xform( transform, q=1, ws=1, rp=1)



def move( first_list, second ):
    'first_list 가 second로 이동한다.'
   
    rot = rotate_xform(second)
    pos = position_xform(second)
    
    for first in first_list:        
    
        cmds.xform(first, ws=1, ro= rot)
        cmds.move(pos[0],pos[1], pos[2] ,first,rpr=1)



def AtoB_BtoA( choice ):
    'A를 B로 이동하거나 B를 A로 이동한다.'
    
    sels = cmds.ls(sl=1) 

    if choice == 'AtoB':
        first_list = sels[0:-1]
        second = sels[-1]
    elif choice == 'BtoA':
        first_list = sels[1:]
        second = sels[0]
 

    move(first_list, second)



def xyz_copy_pivot(XYZ):
       
    a= cmds.ls(sl=1)    
    if len(a) < 1:
        pass
    
    else:
        for c in a[0:-1]:
            pos = cmds.xform( a[-1], q=1, ws=1, rp=1)
            c_pos = cmds.xform( c , q=1, ws=1, rp=1)
            
            if 'xyz' == XYZ:
                cmds.xform(  c , ws=1, piv = pos)
            elif 'x' == XYZ:
                cmds.xform(  c , ws=1, piv = (pos[0], c_pos[1], c_pos[2])  )
            elif 'y' == XYZ:
                cmds.xform(  c , ws=1, piv = (c_pos[0], pos[1], c_pos[2])  )
            elif 'z' == XYZ:
                cmds.xform(  c , ws=1, piv = (c_pos[0], c_pos[1], pos[2])  )



def AtoB_BtoA_copy_pivot( choice ):
    'pivot을 A에서 B로 copy 하거나 B에서 A로 copy한다.'

    sels= cmds.ls(sl=1)

    if len(sels) < 1:
        pass    
    else:
        if choice == 'AtoB':
            first_list = sels[0:-1]
            second = sels[-1]
        elif choice == 'BtoA':
            first_list = sels[1:]
            second = sels[0]
    

        pos = position_xform(second)

        for first in first_list :
            cmds.xform(  first , ws=1, piv = pos)



##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [curve]

def curve_cv_amount_get(shape):
    'curve의 cv 개수를 리턴한다.'

    if cmds.getAttr(shape + '.form') == 0:                
        degs = cmds.getAttr( shape + '.degree' )
        spans = cmds.getAttr( shape + '.spans' )
        cv_amount = degs + spans
    else:
        spans = cmds.getAttr( shape + '.spans' )  
        cv_amount = spans 
        
    return cv_amount_list



##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [ctrl]

def offGRP_command():
    '선택한 컨트롤러에 offGRP 생성'
    sels = cmds.ls(sl=1)

    ctrl_list = []
    skin_jnt_list = []

    for i in sels:

        target_grp = cmds.group(em=1, n= '%s%s'%(i, '_GRP'))
        target_ofs = cmds.group(em=1, n= '%s%s'%(i, '_offGRP'))
        
        cmds.parent(target_grp, target_ofs)
        
        i_po = cmds.xform(i, q=1, ws=1, rp=1)
        i_ro = cmds.xform(i, q=1, ws=1, ro=1)
        i_sc = cmds.xform(i, q=1, ws=1, s=1)   # 컨트롤러의 trans,rotate,scale 값 추출
        
        cmds.move(i_po[0], i_po[1], i_po[2], target_ofs, rpr=1 )  #ofs그룹을 원본컨트롤러의 위치로 이동
        cmds.xform(target_ofs, ws=1, ro=i_ro, s=i_sc)
        
        cmds.parent(i, target_grp)
        
        cmds.makeIdentity(i, apply=1, t=1, r=1, s=1, n=0, pn=1) #프리즈
        
        ctrl_list.append(target_ofs)

        
        cmds.select(cl=1) #select 클리어
        name_re = i.replace('_CTL', '_')
        cre_jnt = cmds.joint(n= '%s%s'%(name_re,'skinJNT'), p=(0,0,0))
        cre_jnt_grp = cmds.group(em=1, n= '%s%s'%(cre_jnt, '_GRP'))
        cmds.parent(cre_jnt, cre_jnt_grp)
        
        cmds.move(i_po[0], i_po[1], i_po[2], cre_jnt_grp, rpr=1 )
        cmds.xform(cre_jnt_grp, ws=1, ro=i_ro)
            
        cmds.parentConstraint(i, cre_jnt_grp, mo=1)
        cmds.scaleConstraint(i, cre_jnt_grp, mo=1)

        skin_jnt_list.append(cre_jnt_grp)


    if len(sels) >= 2:

        p = re.compile("[^0-9]")
        num_del = ("".join(p.findall(sels[0]))) # 문자열에서 숫자를 제거 (그룹 네이밍을 위함)

        ctrl_total_grp = num_del.replace('_CTL', 'CTL_GRP')
        skin_jnt_total_grp = num_del.replace('_CTL', 'skinJNT_GRP')


        cmds.group(ctrl_list, n= ctrl_total_grp)
        cmds.group(skin_jnt_list, n = skin_jnt_total_grp)

    else:
        pass



def object_grp():
    '선택한 object를 group한다.'
    sels = cmds.ls(sl=1)

    ctrl_list = []
   

    for i in sels:

        target_grp = cmds.group(em=1, n= '%s%s'%(i, '_GRP'))

        
        
        i_po = cmds.xform(i, q=1, ws=1, rp=1)
        i_ro = cmds.xform(i, q=1, ws=1, ro=1)
        i_sc = cmds.xform(i, q=1, ws=1, s=1)   # 컨트롤러의 trans,rotate,scale 값 추출
        
        cmds.move(i_po[0], i_po[1], i_po[2], target_grp, rpr=1 )  #ofs그룹을 원본컨트롤러의 위치로 이동
        cmds.xform(target_grp, ws=1, ro=i_ro, s=i_sc)
        
        cmds.parent(i, target_grp)
        
        cmds.makeIdentity(i, apply=1, t=1, r=1, s=1, n=0, pn=1) #프리즈
        


def position_copy():
    '마지막에 선택한 object를 위치에 맞게 copy한다.'
    sels = cmds.ls(sl=1)
    sel_or = sels[-1]
    sel_copy_list = []
    for sel in sels[:-1]:
        sel_copy = cmds.duplicate(sel_or, rc=1)
        move( sel_copy, sel )
        sel_copy_list.append(sel_copy[0])
    cmds.group(sel_copy_list , n = sel_or + '_copy_grp')

    curve_cv_amount_get(transfrom)



def curve_vtx_ro_sc(ro_weight, sc_weight , ro_sc, x,y,z ):
    'curve의 vtx를 자기 피봇 위치에 rotate, scale을 변경한다.'
    sels = cmds.ls(sl=1,fl=1)

    for sel in sels:    
        shape_list = cmds.listRelatives(sel , c=1,pa=1, type = 'shape')
        for shape in shape_list:        
            if cmds.getAttr(shape + '.form') == 0:                
                degs = cmds.getAttr( shape + '.degree' )
                spans = cmds.getAttr( shape + '.spans' )
                cv_amount = degs + spans
            else:
                spans = cmds.getAttr( shape + '.spans' )  
                cv_amount = spans 
            pos = cmds.xform(sel, ws =1, rp=True, q=1)
            if ro_sc == 'rotate':
                if x == True:
                    cmds.rotate(ro_weight,0,0, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                elif y == True:
                    cmds.rotate(0,ro_weight,0, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                elif z == True:
                    cmds.rotate(0,0,ro_weight, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                else:
                    pass
            elif ro_sc == 'scale':
                if x == True and y != True and z != True:
                    cmds.scale(sc_weight,1,1, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                elif y == True and x != True and z != True:
                    cmds.scale(1,sc_weight,1, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                elif z == True and y != True and x != True:
                    cmds.scale(1,1,sc_weight, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                elif x == True and y == True and z == True:
                    cmds.scale(sc_weight,sc_weight,sc_weight, shape + '.cv[0:' + str(cv_amount-1) + ']', r=1, p = pos ,os=1 )
                else:
                    pass
            else:
                pass



##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [skin]

def skincluster_get(transform):
    'paint skin weights tool 에 선택된 joint 추출'
    return mel.eval('findRelatedSkinCluster(\"' + transform + '\")')



def bind_skin_copy():
    '선택된 object에 bindskin 및 skincopy'

    sels=cmds.ls(sl=1)

    sel_skin = sels[-1]
    copyskinCluster = skincluster_get(sel_skin) # skinCluster 추출
    skin_joint=cmds.skinCluster( copyskinCluster, q=1,inf=1) # skinCluster에 귀속된 joint 추출
    skin_method = cmds.skinCluster(copyskinCluster , q=1, sm=1)

    for sel in sels[0:-1]:

        grp_sels=cmds.listRelatives(sel, ad=1 ,pa=True,typ='transform')

        if grp_sels == None:
            get_sels = [sel]
        else:
            get_sels = [sel] + grp_sels
        
        for get_sel in get_sels:
            try:
                skinCluster = cmds.skinCluster( skin_joint , get_sel ,tsb = 1, sm = skin_method )            
            except: 
                pass
            try:                    
                cmds.copySkinWeights(sels[-1],get_sel, noMirror =1,surfaceAssociation ='closestPoint',influenceAssociation ='closestJoint')
            except: 
                pass



def remove_skin_weight(weight_amount):
    '선택한 object의 지정한 값의 skinWeight를 지운다. '

    sel_list = cmds.ls(sl=1,fl=1)

    for sel in sel_list:
        type = cmds.objectType(sel)
        if type == 'transform' :
            sel_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + sel + '\")')
            skin_jnt_list = cmds.skinCluster( sel_skin_cluster , q=1,inf=1)
            for skin_jnts in skin_jnt_list:
                cmds.setAttr( skin_jnts + '.liw', 0)                
            cmds.skinPercent ( sel_skin_cluster, sel , pruneWeights = weight_amount)
        elif '.vtx' in sel:
            transform = '.vtx'.join(sel.split('.vtx')[:-1])
            sel_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + transform + '\")')
            skin_jnt_list = cmds.skinCluster( sel_skin_cluster , q=1,inf=1)
            for skin_jnts in skin_jnt_list:
                cmds.setAttr( skin_jnts + '.liw', 0) 
            cmds.skinPercent ( sel_skin_cluster, sel , pruneWeights = weight_amount)    
        else:
            pass



def skin_copy_many():
    '마지막에 선택한 skinWeight 값을 모두 copy한다.'
    #선택 명령
    sels=cmds.ls(sl=1, fl =1)
    #기존 skin cluster 저장
    sel_skin=sels[-1]
    sel_skin_cluster = mel.eval('findRelatedSkinCluster(\"' + sel_skin + '\")')


    if '.vtx' in sels[0]:
        vtx_sets = cmds.sets(sels[0:-1], n= 'skinCopy_vtx_sets')
        cmds.copySkinWeights(sel_skin,vtx_sets, nm=True, sa= 'closestPoint', ia='closestJoint')
        cmds.delete(vtx_sets)

    else:  
        for sel in sels[0:-1]: 
            grp_sels=cmds.listRelatives(sel, ad=1 ,pa=True,typ='shape')
    
            for grp_sel in grp_sels:
                skin_cluster=mel.eval('findRelatedSkinCluster(\"' + grp_sel + '\")')
        
                if skin_cluster :
                    cmds.copySkinWeights(ss=sel_skin_cluster,ds=skin_cluster, nm=True, sa= 'closestPoint', ia='closestJoint')
                else:
                    pass



def ngskin_tool():
    'ngSkinTool 실행'
    from ngSkinTools.ui.mainwindow import MainWindow
    MainWindow.open()



##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [select]

def skin_jnt_select():
    '선택한 object의 skin된 joint를 잡는다.'
    sels=cmds.ls(sl=1)
    jnt_list = []
    for sel in sels:
        skinCluster=mel.eval('findRelatedSkinCluster(\"' + sel + '\")')

        joint=cmds.skinCluster( skinCluster, q=1,inf=1)
        cmds.select(joint)



def jnt_hierarchy():
    '하위 객체 joint select하기'

    sel=cmds.ls(sl=1)

    sel_joint = cmds.ls(sl=1, type = 'joint')

    sel_lower_joint = cmds.listRelatives(sel, ad=1, pa=1, typ='joint')
    cmds.select(sel_joint + sel_lower_joint)



def normalize_float(num):
    '0.0000000000123 => 0.0, -0.0 => 0.0'
    result = float('%.5f' % num)
    if result == -0.0:
        result = 0.0
    return result



def get_vertex_list(node):
    'vtx의 위치 postion값을 return한다.'
    vtx_num = cmds.polyEvaluate(node, v=1) # vtx 개수 얻기
    # 모든 버텍스 위치 얻기
    result = []
    for i in range(vtx_num):
        vtx_pos = cmds.xform(node + '.vtx[' + str(i) + ']', ws=1, t=1, q=1)
        vtx_pos = [ normalize_float(num) for num in vtx_pos ] # 소수점 자리 정리, -0.0 => 0.0
        result.append(vtx_pos)
    return result



def same_vtx_set():
    '같은 위치의 vtx를 sets로 묶는다.'
    a = cmds.ls(sl=1)
    transforms = a[0:-1]
    last_transform = a[-1]

    result = {} # 여러 transform 들의 vertex_list 를 담는 딕셔너리
    for transform in transforms:
        result[transform] = get_vertex_list(transform)

    last_vertex_list = get_vertex_list(last_transform) # 마지막으로 선택된 트랜스폼의 좌표값 리스트를 얻는다.
    for transform, vertex_list in result.items():
        vtx_str_list=[]
        for i, xyz in enumerate(last_vertex_list):
            if xyz in vertex_list:
                vtx_str = last_transform + '.vtx[' + str(i) + ']'
                vtx_str_list.append(vtx_str)

        if len(vtx_str_list) == 0:
            pass
        else:
            cmds.sets( vtx_str_list , n = transform + '_vtx_sets' )
            cmds.select( vtx_str_list )



def skinCluster_of_jnt_get( joint ):
    'joint 로 skinCluster를 리스트로 얻는다. '
    return cmds.listConnections( joint, s=0, d=1, type = 'skinCluster')



def geo_of_jnt():
    'joint에 스킨된 geometry를 얻는다.'
    sels=cmds.ls(sl=1, type= 'joint')

    geo_list = []
    for sel in sels:
        skincluster_list = skinCluster_of_jnt_get( sel )
        skincluster_list = list(set(skincluster_list)) # 중복 리스트 제거
        for skincluster in skincluster_list:
            geos = cmds.skinCluster(skincluster, q=1, g=1 )
            for geo in geos:
                
                if cmds.objectType(geo) != 'transform':
                    geo = cmds.listRelatives(geo, p=1)[0]
                else :
                    pass
                geo_list.append(geo)
    
    cmds.select(geo_list)



##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [rig]

def rename(rename_text):
    'rename UI 실행'
    sels = cmds.ls(sl=1)

    rename_tex_re = rename_text.replace(' ', '_') # 공백을 _로 변환
    rename_count = rename_tex_re.count('#') # 텍스트필드에 적힌 샾의 갯수를 카운트(정수)
    

    if rename_count > 0 : # 카운트된 샾의갯수가 0보다 많을경우
        sharp_amount = '#' * rename_count # 텍스트필드에 샾을 적은만큼 문자로 다시 샾을 만들어준다. 
        rename_splt = rename_tex_re.split(sharp_amount) # 내가적은 샾과 문자로빼준 샾이 갯수가같으므로 그걸 기준으로 스플릿
        number_digit = '%s%s%s%s'%('%','0',rename_count,'d') # 샾의갯수로 숫자의 자릿수를 결정
        
        for num,sel in enumerate(sels): 
            cmds.rename(sel, rename_splt[0] + number_digit%int(num+1) + rename_splt[1]) 
            #리네임, 샾을기준으로 앞뒤를 나누고 숫자는 1부터 시작해야하므로 +1을 해준다  


    elif '@' in rename_tex_re: # 적은 텍스트필드에 @가 있을경우
       
        abc = string.ascii_uppercase # 알파벳 리스트

        for num, sel in enumerate(sels):   
            replace_at = rename_tex_re.replace('@', abc[num]) # @를 알파벳으로 변환
            rename_at = cmds.rename(sel, replace_at)

      
    else : # 샾과 @가 없을경우
        for sel in sels:
            cmds.rename(sel, rename_tex_re)



def joint_on_off(i):
    'joint on off'
    print('-----------------------------------------')
    sels = cmds.ls(typ='joint')
    if i == 0:
        choice = ' ON '
    else:
        choice = ' OFF '


    for sel in sels :
        cmds.setAttr( sel + '.drawStyle', i )
        
    print(u'joint' + choice + u'개수: ' + str(len(sels)))



def axis_on_off(i):
    'joint axis on off'
    print('-----------------------------------------')
    sels = cmds.ls(typ='joint')
    if i == 0:
        choice = ' ON '
    else:
        choice = ' OFF '


    for sel in sels :
        cmds.setAttr( sel + '.displayLocalAxis', i )
        
    #print(u'joint' + choice + u'개수: ' + str(len(sels)))



def jnt_ps(parent, scale):
    '선택한 object에 joint, joint group 을 만들고 parent 한다.'
    a=cmds.ls(sl=1)
    if len(a) == 0:
        grp = cmds.group(em=1, w=1, n=  'base_skinJNT_GRP')
        cmds.joint(n='base_skinJNT')        
    else:
        grp_list=[]
        for c in a:          
            rot = cmds.xform(c, q=1, ws=1, ro=1)
            pos = cmds.xform(c, q=1, ws=1, rp=1)
            if '_CTL' == c[-5:]:
                pixed_name = c.replace('_CTL', '')
            else :
                pixed_name = c
            grp = cmds.group(em=1, w=1, n= pixed_name + '_skinJNT_GRP')
            cmds.joint(n= pixed_name + '_skinJNT')        
            cmds.xform(grp, ws=1, ro= rot)
            cmds.move(pos[0],pos[1], pos[2] ,grp,rpr=1)          
            if parent :
                cmds.parentConstraint( c,grp , mo=1, w=1)
            else :
                pass
            if scale :
                cmds.scaleConstraint( c,grp , mo=1, w=1)
            else :
                pass
            grp_list.append(grp)
        cmds.group(grp_list, n = grp_list[0] + '_GRP')



class motionpath_cv():

    def __init__(self):   
        ## 윈도우 ID##
        windowID='motionpath_cv'
        ##windows reset
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        cmds.window(windowID, t='motionpath_cv', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
        ##master layer
        master = cmds.columnLayout()
        cmds.columnLayout()
        cmds.rowColumnLayout( nr=1 )
        #cmds.text(l = u'corve - 커브등록 /copy_target  - 카피할 타겟등록/')
        cmds.setParent (master)
        cmds.columnLayout()
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'    rotate - 커브의 방향에 맞게 타겟을 생성')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'    attach - 타겟을 커브에 붙임')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = '    ')
        cmds.text(l = u'copy_count' ,w = 70)
        cmds.text(l = '      ')
        cmds.intField('tw_int_field' , w = 30 , h = 20 ,v=10)
        cmds.checkBox( 'rotate_check', l = u'rotate' , v=True )
        cmds.checkBox( 'attach_check', l = u'attach' , v=False )
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'curve' ,w = 100)
        cmds.textField('start_tex_box' , w = 150 , h = 20 )
        cmds.button( l = u'등록' , w = 50,c = pm.Callback(self.sels_tex, 'st_sel'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'copy_target' , w = 100)
        cmds.textField('end_tex_box' , w = 150 , h = 20)
        cmds.button( l = u'등록' , w = 50,c = pm.Callback(self.sels_tex, 'end_sel'))
        cmds.setParent (master)

        cmds.button(l=u'연결' , w = 301 , h = 30 ,c = pm.Callback(self.motionPath_command))
        cmds.setParent (master)
        cmds.showWindow(windowID)

    def sels_tex(self,part):
        sels = cmds.ls(sl=1)
        if part=="st_sel":cmds.textField('start_tex_box' , edit =1, tx= sels[0] )
        if part=="end_sel":cmds.textField('end_tex_box' , edit =1, tx= sels[0] )

    def motionPath_command(self):
        ui_rotate_q = cmds.checkBox( 'rotate_check', v=True, q=1)
        ui_nod_q = cmds.checkBox( 'attach_check',v=True,q=1)
        ui_copy_count_q = cmds.intField('tw_int_field',v=True, q = 1)
        ui_cv_q = cmds.textField('start_tex_box' , tx=1,q=1 )
        ui_target_q = cmds.textField('end_tex_box' , tx=1,q=1)

        if ui_rotate_q ==True:
            ui_ro_ch = True
        else:
            ui_ro_ch = False
        if ui_nod_q ==True:
            attach = False
        else:
            attach = True
        go = self.motion_count_cr(ui_cv_q,ui_target_q,ui_copy_count_q,ro =ui_ro_ch,nod_del = attach , dis_conn_r = attach , dis_conn_t = attach )
        chil = go['target']
        target_grp = cmds.group(n='%s%s'%(ui_target_q,'_motionPath_copy_grp'),em = 1)
        cmds.parent(chil,target_grp)

    def motionPath_point(self,cv, number , **bool):
        '커브의 길이를 1값으로 모션패스 pos rotate 를 추출'
        ## cv 이름혹은 트랜스폼 / 커브의 위치점 0~1 / 'nod_del' = False 를 사용하여 노드를 지우지않을수잇다
        sh = cmds.listRelatives(cv, shapes =1, children=1)[0]
        cre_motionPath = cmds.createNode('motionPath', n = cv + '_motionPath')

        cmds.setAttr(cre_motionPath + '.follow', 1)
        cmds.setAttr(cre_motionPath + '.frontAxis', 0)
        cmds.setAttr(cre_motionPath + '.upAxis', 1)
        
        cmds.setAttr(cre_motionPath + '.worldUpVectorX', 1)
        cmds.setAttr(cre_motionPath + '.worldUpVectorY', 0)
        cmds.setAttr(cre_motionPath + '.worldUpVectorZ', 0)  # 모션패스노드의 업벡터

        cmds.setAttr(cre_motionPath + '.fractionMode', 1) 
        cmds.connectAttr(sh + '.worldSpace' , cre_motionPath + '.geometryPath')
        cmds.setAttr(cre_motionPath + '.uValue', number)
        motionPath_tr = cmds.getAttr(cre_motionPath + '.allCoordinates')
        motionPath_ro = cmds.getAttr(cre_motionPath + '.rotate')
        if bool.get('nod_del') == None or bool.get('nod_del') == True:
            cmds.delete(cre_motionPath)
        else:pass
        ## 리턴값은 해당포지션의 tr / ro 값   / 모션패스노드
        return {'t':motionPath_tr[0] , 'r':motionPath_ro[0] , 'nod':cre_motionPath}

    def motion_count_cr(self,cv ,target_transform , count,**bool):
        ## 커브(해당메인커브) / 타겟(복사해서 붙을 타겟 트랜스폼) /카운트(횟수) /
        ###**bool명령** ///// 'ro' = False 로테이션 제거 / 'nod_del' = False  노드를 삭제하지 않는다 
        # ## bool커넥션 명령 해당명령은 'nod_del'= False 일떄만 사용할수있다// 'dis_conn_r' = False   모션패스 노드 로테이트 커넥션 // 'dis_conn_t' = False  모션패스노드 트랜스 커넥션
        ## 모션패스 커브 포지션에 타겟을 복사해서 붙인다
        if bool.get('nod_del') == None or bool.get('nod_del') == True:
            get = True
        else:
            get = False
        target = target_transform
        tr_xform_lst = []
        ro_xform_lst = []
        nod_lst = []
        st_target = cmds.duplicate(target)[0]
        target_copy_lst = [st_target]
        st_pos = self.motionPath_point(cv, 0,nod_del=get)
        nod_lst.append(st_pos['nod'])
        st_xform_t = cmds.xform(st_target , t = st_pos['t'])
        tr_xform_lst.append(st_pos['t'])
        ro_xform_lst.append(st_pos['r'])
        f_cn = float(count)
        div = 1.0/(f_cn-1)
        cn = 0.0
        return_lst = [0]
        for i in range(count-2):
            cn = cn+div
            target_copy = cmds.duplicate(target)[0]
            path = self.motionPath_point(cv, cn,nod_del=get)
            pos = cmds.xform(target_copy , t = path['t'])
            if bool.get('ro') == None or bool.get('ro') == True:
                ro = cmds.xform(target_copy , ro = path['r'])
            else:pass      
            return_lst.append(cn)
            target_copy_lst.append(target_copy)
            tr_xform_lst.append(path['t'])
            ro_xform_lst.append(path['r'])  
            nod_lst.append(path['nod'])
        end_target = cmds.duplicate(target)[0]
        end_pos = self.motionPath_point(cv, 1 ,nod_del=get)
        cmds.xform(end_target , t = end_pos['t'] )
        if bool.get('ro') == None or bool.get('ro') == True:
            st_xform_r = cmds.xform(st_target , ro = st_pos['r'])
            cmds.xform(end_target , ro = end_pos['r'])
        else:
            pass
        nod_lst.append(end_pos['nod'])
        target_copy_lst.append(end_target)
        return_lst.append(1)
        tr_xform_lst.append(end_pos['t'])
        ro_xform_lst.append(end_pos['r'])
        if bool.get('dis_conn_t') == None or bool.get('dis_conn_t') == True:
            pass
        else:
            for i in range(len(nod_lst)):
                cn = 0+i
                cmds.connectAttr('%s%s%s'%(nod_lst[cn],'.','allCoordinates'),'%s%s%s'%(target_copy_lst[cn],'.','translate'))
        if bool.get('dis_conn_r') == None or bool.get('dis_conn_r') == True:
            pass
        else:
            for i in range(len(nod_lst)):
                cn = 0+i
                cmds.connectAttr('%s%s%s'%(nod_lst[cn],'.','rotate'),'%s%s%s'%(target_copy_lst[cn],'.','rotate'))
        rev_return_lst=[]
        for i in return_lst:
            a = (i-1)*-1
            rev_return_lst.append(a) 
        # 리턴값은: 'div' :등분 소수 리스트 / 'div_rev' : 등분소수 뒤집은 반대값/ 'target'카피타겟 리스트/'nod' : 노드 리스트 / 't' 타겟 포지션/ 'r'  타겟 로테이션
        return {'div':return_lst ,'div_rev':rev_return_lst, 'target':target_copy_lst ,'nod':nod_lst, 't':tr_xform_lst , 'r':ro_xform_lst}



def shape_copy():

    sel = cmds.ls(sl=True)

    new_ctrl = sel[-1]
    old_ctrls = sel[:-1]
            
    for old_ctrl in old_ctrls:
        dup = cmds.duplicate(new_ctrl, rc=True)
        cmds.delete(cmds.parentConstraint(old_ctrl, dup))
        cmds.parent(dup, old_ctrl)
        cmds.makeIdentity(dup, apply=True)
        old_shapes = cmds.listRelatives(old_ctrl, type="shape", f=True)
        ctrl_shapes = cmds.listRelatives(dup, type="shape", f=True) 
        color = cmds.getAttr(old_shapes[0] + ".overrideColor")                
        
        for ctrl_shape in ctrl_shapes:            
            cmds.setAttr(ctrl_shape + ".overrideEnabled", 1)
            cmds.setAttr(ctrl_shape + ".overrideColor", color)
            ren = cmds.rename(ctrl_shape, old_ctrl + "Shape#")
            cmds.parent(ren, old_ctrl, relative=True, shape=True)
        
        cmds.delete(dup)
        cmds.delete(old_shapes)
        
    cmds.select(clear=True)



class insert_jnt():

    def __init__(self):

        # Builds the interface for the splitSelJointUI

        win="js_splitSelJointWin"
        if cmds.window(win, exists=1):
            cmds.deleteUI(win)
            
        cmds.window(win, t="Split Selected Joints")
        f=cmds.formLayout(nd=100)
        segments=cmds.intSliderGrp(field=True, max=20, l="Segments", min=2)
        b1=cmds.button(l="Okay")
        b2=cmds.button(l="Cancel")
        cmds.formLayout(f, ap=[(b1, 'right', 0, 47), (b2, 'left', 0, 52)], e=1, af=[(segments, 'top', 5), (segments, 'left', 5), (segments, 'right', 5), (b1, 'left', 5), (b1, 'bottom', 5), (b2, 'right', 5), (b2, 'bottom', 5)])


        # set up callbacks
        cmds.button(b2, c=lambda *args: cmds.deleteUI(str(win)), e=1)
        cmds.button(b1, c=lambda *args: self.js_buildSplitJointCmd(str(segments)), e=1)

        # set up defaults
        segmentOpt=2
        segmentOpt=int(self.js_getOptionVar(segmentOpt, "js_splitSelSegments"))


        # now set the item
        cmds.intSliderGrp(segments, e=1, value=segmentOpt)
        cmds.showWindow(win)

    def js_getOptionVar(self, default, optionVar):
	
        return_=default
        # check and see if the optionVar exists
        if not pm.optionVar(exists=optionVar):
            pm.optionVar(iv=(optionVar, default))
            
        return_=int(pm.optionVar(q=optionVar))
        return return_
	

    def js_buildSplitJointCmd(self, segments):

        # get the values
        segmentVal=cmds.intSliderGrp(segments, q=1, value=1)
        segmentVal = segmentVal + 1 # 기존 스크립트에서는 (segments-1)이 생성되는 조인트 갯수였기 때문에 segments에 입력한대로 조인트가 생성되게 하기위해 +1을 해준다.

        # set the optionVars
        cmds.optionVar(iv=("js_splitSelSegments", segmentVal))


        # build the command
        cmd=("js_splitSelJoint " + str(segmentVal))
        cmds.evalEcho(cmd)



    def js_splitSelJoint(self, numSegments):

        # This proc will split the selected joint into the specified number of segments    #
        #

        if numSegments<2:
            cmds.error("The number of segments has to be greater than 1.. ")
        
        # VARIABLES
        #

        joints = [""] * (0)
        joint = ""
        newChildJoints = [""] * (0)
        count=0
        joints=cmds.ls(type='joint', sl=1)
        for joint in joints:
            # first check the rotation order vs. the axis the joint should be rotating around.  In order for this to work
            # correctly, the child joint of the joint specified must have translation values ONLY IN ONE AXIS.  Let's
            # and, that axis MUST be the first one in the rotation order.  For example, if the joint structure is:
            #      upArm->loArm
            # and the loArm has a translate value of 6 0 0, then upArm should have a rotation order of XYZ or XZY.
            #
            child = ""
            child=str(self.js_getChildJoint(joint))


            if len(child) == "":
                cmds.error("Joint: " + str(joint) + " has no children joints.\n")
                

            else:
                axis = ""
                rotationOrder = ""
                firstChar = ""
                radius=float(cmds.getAttr(str(joint) + ".radius"))
                axis=str(self.js_getJointAxis(child))

                
                # now that we have the axis, we want to check and make sure the rotation order on $joint is correct.
                rotOrderIndex=int(cmds.getAttr(str(joint) + ".rotateOrder"))
                rotationOrder=self.js_getRotOrderString(joint)

                # ** REMOVING CHECK FOR ROTATION ORDER MATCHING
                # check that the rotaiton order will work.
                # 
                #$firstChar = `substring $rotationOrder 1 1`;
                #if ($axis == $firstChar)
                if axis == firstChar:
                
                    childT=0.0
                    tVal=0.0
                    attr = ""


                    # the rotation order is correct!  we're set!

                    # get the axis attr
                    attr=("t" + str(axis))

                    # get the value of the child
                    childT=cmds.getAttr(str(child) + "." + str(attr))
                    space=float(childT / numSegments)

                    # create a series of locators along the joint based on the number of segments.
                    locators = [""] * (0)
                    for x in range(0,(numSegments - 1)):
                        tmp=cmds.spaceLocator()
                        locators[x]=str(tmp[0])
                        cmds.parent(locators[x], joint)
                        cmds.setAttr((locators[x] + ".t"), 
                            0, 0, 0)
                        cmds.setAttr((locators[x] + "." + str(attr)), (space * (x + 1)))
        
                    # We just want to segment the joint, nothing more.
                
                    # for each segment, we're going to insert a joint, and then move it to the position of the locator
                    prevJoint=str(joint)
                    for x in range(0,len(locators)):
                        # insert a joint
                        newJoint=cmds.insertJoint(prevJoint)

                        # get the position of the locator
                        pos=cmds.xform(locators[x], q=1, rp=1, ws=1)

                        # move the joint there
                        cmds.move(pos[0], pos[1], pos[2], (str(newJoint) + ".scalePivot"), (str(newJoint) + ".rotatePivot"), a=1, ws=1)

                        
                        # rename the new joint
                        newJoint=cmds.rename((newJoint), (str(joint) + "_seg_" + str((x + 1)) + "_joint"))
                        cmds.setAttr((str(newJoint) + ".radius"), radius)

                        # set the rotation order
                        cmds.setAttr((str(newJoint) + ".rotateOrder"), rotOrderIndex)

                        # set the prevJoint
                        prevJoint=newJoint

                    

                    cmds.delete(locators)
                # ** END ROTATION ORDER CHECK
                #
                #else
                #{
                    # The rotation order is incorrect.  The user needs to re-orient the joint
                    #js_orientJointWarning $joint $rotationOrder $axis $firstChar;

                #}

    def js_orientJointWarning(self, joint, rotationOrder, axis, firstChar):

        message = ""
        message=("Warning!!!!\n\n")
        message+=("The rotation order and joint orient for " + str(joint) + " do not match up.\n")
        message+=("The rotation order is: " + str(rotationOrder) + "\n")
        message+=("The axis aiming down the joint is: " + str(axis) + "\n\n")
        message+=("In order for this script to work, you need to either change the axis that\n")
        message+=("aims down the joint to " + str(firstChar) + ", or switch the rotation order to ")
        if axis == "x":
            message+=("xyz or xzy.\n")
            
            
        elif axis == "y":
            message+=("yxz or yzx.\n")
            
            
        elif axis == "z":
            message+=("zxy or zyx.\n")
            
            
        message+=("\nSkipping Joint: " + str(joint) + "...\n")
        cmds.confirmDialog(ma="left", m=message)
        cmds.warning(message)



    def js_getRotOrderString(self, joint):

        return_ = ""
        ro = 0
        ro=int(cmds.getAttr(str(joint) + ".ro"))
        if ro == 0:
            return_="xyz"
            
            
        elif ro == 1:
            return_="yzx"
            
            
        elif ro == 2:
            return_="zxy"
            
            
        elif ro == 3:
            return_="xzy"
            
            
        elif ro == 4:
            return_="yxz"
            
            
        elif ro == 5:
            return_="zyx"
            
            
        return return_


    def js_getJointAxis(self, child):

        axis = ""
        t = [0.0] * (0)
        t=cmds.getAttr(str(child) + ".t")


        # get the translation values of the $child joint
        # now check and see which one is greater than 0.  We should have a tolerance value just in case
        tol=0.0001
        for x in range(0,2+1):
            if (t[x]>tol) or (t[x]<(-1 * tol)):
                if x == 0:
                    axis="x"
                    
                    
                elif x == 1:
                    axis="y"
                    
                    
                elif x == 2:
                    axis="z"
                    
        if axis == "":
            cmds.error("The child joint is too close to the parent joint. Cannot determine the proper axis to segment.")
            
        return axis


    def js_getChildJoint(self, joint):
        
        tmp = [""] * (0)
        tmp=cmds.listRelatives(joint, c=1, type='joint', f=1)
        return (tmp[0])
        


        


##-------------------------------------------------------------------------------------------------------------------------------------------------------
# [follicle]

def follicle_make():
    'follice 생성후 넙스에 붙이기'
    nubs = cmds.ls(sl=1)
    for nub in nubs:  
        nurbs_shape = cmds.listRelatives(nub, children=True , pa=1)[0]
        #follicle 생성후 위치에 맞게 nurbs에 붙이기   
        #follicleShape 생성후 Transform에 연결
        f_shape = cmds.createNode('follicle', n = nub + '_follicleShape')
        f_transform = cmds.listRelatives(f_shape, parent=True, pa=1)[0]   
        f_transform = cmds.rename(f_transform , f_shape.replace('Shape',''))
        cmds.connectAttr(f_shape + '.outTranslate', f_transform + '.translate')
        cmds.connectAttr(f_shape + '.outRotate', f_transform + '.rotate') 
        # follicle을 nurbs에 붙이기
        if cmds.objectType(nurbs_shape) == 'nurbsSurface':
            cmds.connectAttr(nurbs_shape + '.local' , f_shape + '.inputSurface',f= True)
            cmds.connectAttr(nurbs_shape + '.worldMatrix[0]', f_shape + '.inputWorldMatrix', f= True)    
        elif cmds.objectType(nurbs_shape) == 'mesh':
            cmds.connectAttr(nurbs_shape + '.outMesh' , f_shape + '.inputMesh',f= True)
            cmds.connectAttr(nurbs_shape + '.worldMatrix[0]', f_shape + '.inputWorldMatrix', f= True)     
        cmds.setAttr(f_shape + '.parameterU', 0.5)
        cmds.setAttr(f_shape + '.parameterV', 0.5)



class follicle_many_UI():
    'follicle 여러개를 생성해서 붙인다.'
    def __init__(self):      
        # global U_amount
        # global V_amount
        # global U_revers
        # global V_revers
       
        windowID='follicleUI'
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        
        window= cmds.window(windowID,t='follicle many',  rtf=0, s=1, mnb=0, mxb=0)
        master=cmds.columnLayout()

        hi_layout = cmds.rowColumnLayout()

        cmds.rowColumnLayout( nc=8, cw=[(1,25),(2,15), (3,10), (4,30),(5,25),(6,15),(7,10),(8,30)] )

        cmds.text(l='U re:')
        self.U_revers = cmds.checkBox(l='revers', v=0)
        #self.U_check_revers = cmds.checkBox(self.U_revers,q=True, v=True)
        cmds.text(l='U')
        self.U_amount = cmds.intField( min=1, max=999, v=1)
        #self.U_joint_amount = cmds.intField( self.U_amount, q= True , v= True )
        cmds.text(l='V re:')
        self.V_revers = cmds.checkBox(l='revers', v=0)
        #self.V_check_revers = cmds.checkBox(self.V_revers,q=True, v=True)
        cmds.text(l='V')
        self.V_amount = cmds.intField( min=1, max=999, v=1)
        #self.V_joint_amount = cmds.intField( V_amount, q= True , v= True )

        cmds.setParent(hi_layout)

        cmds.rowColumnLayout( nc=2, cw=[(1,80),(2,80)] )
        # cmds.button(l= 'create' , c= 'anyzac_Asset_tool.follicle_many()')
        # cmds.button(l= 'close' , c =('cmds.deleteUI(\"' + window + '\", window=True)'))
        cmds.button(l= 'create' , c= pm.Callback(self.follicle_many))
        cmds.button(l= 'close' , c =('cmds.deleteUI(\"' + window + '\", window=True)'))

        cmds.showWindow(windowID)


    def follicle_many(self):
        '개수에 맞게 follice 생성후 넙스에 붙이기' 
        self.U_joint_amount = cmds.intField( self.U_amount, q= True , v= True )
        self.V_joint_amount = cmds.intField( self.V_amount, q= True , v= True )
        self.U_check_revers = cmds.checkBox(self.U_revers,q=True, v=True)
        self.V_check_revers = cmds.checkBox(self.V_revers,q=True, v=True)  
        nubs = cmds.ls(sl=1)
        for nub in nubs:
            nurbs_shape = cmds.listRelatives(nub, children=True, type='shape', pa=1 )[0]
            f_transform_list = []
            f_shape_list = []
            skin_grp_list = []
            skin_ctrl_ofs_list = []
            iu=0
            iv=0
            U=1
            V=1     
            follicle_transform_list = []
            for a in range(self.U_joint_amount): 
                for a in range(self.V_joint_amount):     
                    if iv == self.V_joint_amount:
                        iv=0
                        V=1
                    f_shape = cmds.createNode('follicle', n = nub + '_%02dU_%02dV_follicleShape'%(U,V))            
                    f_transform = cmds.listRelatives(f_shape, parent=True, pa=1)[0]  
                    f_transform = cmds.rename(f_transform , f_shape.replace('Shape',''))
                    cmds.connectAttr(f_shape + '.outTranslate', f_transform + '.translate')
                    cmds.connectAttr(f_shape + '.outRotate', f_transform + '.rotate')            
                    if cmds.objectType(nurbs_shape) == 'nurbsSurface':
                        cmds.connectAttr(nurbs_shape + '.local' , f_shape + '.inputSurface',f= True)
                        cmds.connectAttr(nurbs_shape + '.worldMatrix[0]', f_shape + '.inputWorldMatrix', f= True)    
                    elif cmds.objectType(nurbs_shape) == 'mesh':
                        cmds.connectAttr(nurbs_shape + '.outMesh' , f_shape + '.inputMesh',f= True)
                        cmds.connectAttr(nurbs_shape + '.worldMatrix[0]', f_shape + '.inputWorldMatrix', f= True)             
                    if self.U_joint_amount == 1:
                        cmds.setAttr(f_shape + '.parameterU' , 0.5  )
                    else:
                        if self.U_check_revers == True:
                            cmds.setAttr(f_shape + '.parameterU' , (1.0 / (self.U_joint_amount-1)*1.0) * iu   )
                        else:
                            cmds.setAttr(f_shape + '.parameterU' , (1.0 / (self.U_joint_amount-1)*1.0) * (self.U_joint_amount - U))
                            
                    
                                        
                    
                    if self.V_joint_amount == 1:
                        cmds.setAttr(f_shape + '.parameterV' , 0.5  )
                    else:    
                        if self.V_check_revers == True:
                            cmds.setAttr(f_shape + '.parameterV' , (1.0 / (self.V_joint_amount-1)*1.0) * iv   )
                        else:
                            cmds.setAttr(f_shape + '.parameterV' , (1.0 / (self.V_joint_amount-1)*1.0) * (self.V_joint_amount - V)) 
                    follicle_transform_list.append(f_transform)
                    iv=iv+1    
                    V=V+1 
    
                iu=iu+1    
                U=U+1
            cmds.group(follicle_transform_list, n = nub + '_follicle_grp', w=1)         




    


