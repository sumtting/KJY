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
# [blend]

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

            blend_combi_list.append(blend_combi_name)
            new_combination_node_list.append(new_combination_node)
            combination_connect_info_list.append(combination_connect_info)
            
            
            cmds.delete(combination_node)

            #cmds.disconnectAttr (combination_node + '.outputWeight', blend_combi_name) # 기존에 블렌드노드에 콤비네이션쉐입이 연결된걸 끊어준다
            #cmds.disconnectAttr (combination_target, blend_combi_name) # 기존에 블렌드노드에 콤비네이션쉐입이 연결된걸 끊어준다

   

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

            
    # 이대로 진행하면 블렌드쉐입의 네이밍에 '_1_0'이 들어가므로 리네임을 해준다.
    main_target_list_re = []
    for i in main_target_list:
        re = i.split('_1_0')[0]

        sel_re = cmds.ls(re)
        if len(sel_re) > 0 :
            cmds.delete(i)
        
        else:
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

    for main_num, inbet_wei in enumerate(inbet_list):
    
        if len(inbet_wei) >= 1:
            print main_num 
            inbet_main_target = cmds.ls(main_target_list_re[main_num])[0]
            print inbet_main_target
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




    


