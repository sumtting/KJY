# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import sys
import maya.mel as mel
import string 
import pymel.core as pm

Set_route = 'D:/KJY/python/Set/' # Set 폴더의 경로

# [vehicle_set]


class vehicle_set():

    def __init__(self):
        if pm.window('mirRigVehicle', q=1, ex=1):
            pm.deleteUI('mirRigVehicle')
        pm.window('mirRigVehicle', ret=1, w=264, t='Vehicle Build V01 TK01', h=124, s=1, mb=1)
        pm.columnLayout('mRV_columnLayout', w=262, h=120)
        pm.separator('mRV_separator1')
        pm.text('mRV_text1', l='                                      Import')
        pm.separator('mRV_separator2')
        pm.button('mRV_button1', w=260, h=30, l='Import', c=pm.Callback(self.import_vehicle))
        pm.separator('mRV_separator3')
        pm.text('mRV_text2', l='                                      Build')
        pm.separator('mRV_separator4')
        pm.button('mRV_button2', w=260, h=30, l='Build', c=pm.Callback(self.applySet))
        pm.separator('mRV_separator5')
        pm.text('mRV_text3', l='                             Go To Build Pose')
        pm.separator('mRV_separator6')
        pm.button('mRV_button3', w=260, h=30, l='Go To Build Pose', c=pm.Callback(self.buildPose))
        pm.separator('mRV_separator7')
        pm.text('mRV_text4', l='     Do you want to roll back? Nothing like that.')
        pm.showWindow('mirRigVehicle')


    def import_vehicle(self):
        vehicle_bindpose = Set_route + 'vehicle_pos.mb'
        cmds.file( vehicle_bindpose, i = 1 , f = 1  )




    def buildSet(self):
        selDelete = pm.ls('*_vehicleDelete')
        deleteETC = pm.delete(selDelete)
        dmtList = ['frontWheel_R_distance_MULT',
        'frontWheel_L_distance_MULT',
        'backWheel_R_distance_MULT',
        'backWheel_L_distance_MULT']
        dmtCtlList = ['frontWheel_R_CTL',
        'frontWheel_L_CTL',
        'backWheel_R_CTL',
        'backWheel_L_CTL']
        for i in range(len(dmtList)):
            diameter = pm.getAttr(dmtList[i] + '.outputX')
            pm.setAttr(dmtCtlList[i] + '.diameter', diameter)

        pm.parentConstraint('body_M_pivTarget_GRP', 'body_M_control_conGRP', mo=1)
        parList = ['sky_M_CTL',
        'body_M_CTL',
        'frontDoor_L_CTL',
        'backDoor_L_CTL',
        'frontDoor_R_CTL',
        'backDoor_R_CTL',
        'frontWheel_R_tgetJNT',
        'backWheel_R_tgetJNT',
        'frontWheel_L_tgetJNT',
        'backWheel_L_tgetJNT']
        chiList = ['root_M_skinJNT',
        'body_M_skinJNT',
        'frontDoor_L_skinJNT',
        'backDoor_L_skinJNT',
        'frontDoor_R_skinJNT',
        'backDoor_R_skinJNT',
        'frontWheel_R_skinJNT',
        'backWheel_R_skinJNT',
        'frontWheel_L_skinJNT',
        'backWheel_L_skinJNT']
        for i in range(len(parList)):
            if pm.objExists(chiList[i]):
                pm.parentConstraint(parList[i], chiList[i], mo=1)
                pm.scaleConstraint(parList[i], chiList[i], mo=1)
            else:
                delName = chiList[i].split('_skinJNT')[0]
                pm.delete(delName + '*')

        pm.setAttr('main_M_CTL_GRP.visibility', 1)
        pm.setAttr('poser_GRP.visibility', 0)
        selDeleteEnd = pm.ls('*_endVehicleDelete')
        deleteETCEnd = pm.delete(selDeleteEnd)


    def applySet(self):
        pm.Callback(self.buildSet())
        


    def buildPose(self):
        ctlList = ['frontWheel_L_CTL',
        'backWheel_L_CTL',
        'front_set_CTL',
        'back_set_CTL',
        'right_set_CTL',
        'backDoor_R_CTL',
        'frontWheel_R_CTL',
        'frontDoor_R_CTL',
        'backWheel_R_CTL',
        'world_M_CTL',
        'body_M_CTL',
        'main_M_CTL',
        'sky_M_CTL',
        'backWheel_rot_CTL',
        'left_set_CTL',
        'frontWheel_rot_CTL',
        'frontDoor_L_CTL',
        'backDoor_L_CTL']
        attrName = ['translateX',
        'translateY',
        'translateZ',
        'rotateX',
        'rotateY',
        'rotateZ',
        'scaleX',
        'scaleY',
        'scaleZ']
        for i in range(len(ctlList)):
            if pm.objExists(ctlList[i]):
                for s in attrName:
                    if pm.getAttr(ctlList[i] + '.' + s, k=1):
                        if 'scale' in str(s):
                            pm.setAttr(ctlList[i] + '.' + s, 1)
                        else:
                            pm.setAttr(ctlList[i] + '.' + s, 0)



# [skirt_def]

def move_point( first, second ):
    'first_list 가 second로 이동한다.'

    pos = position_xform(second)
    
    cmds.move(pos[0],pos[1], pos[2] ,first,rpr=1)

def position_xform(transform):
    'world position 추출'
    return cmds.xform( transform, q=1, ws=1, rp=1)


def change_number(part):
    #base_num = cmds.textField('%s_'%(position) + 'number_tex_box'  , text =1, q=1)
    base_num=cmds.intSliderGrp(part, q=1, value=1)
    base_num = int(base_num)
    return base_num


def normalize_float(num):
    '0.0000000123 => 0.0, -0.0 => 0.0'
    result = float('%.5f' % num)
    if result == -0.0:
        result = 0.0
    return result


def rotate_xform(transform):
    'world rotate 추출'
    return cmds.xform(transform, q=1, ws=1, ro=1)


def move(first_list, second ):
    'first_list 가 second로 이동한다.'

    rot = rotate_xform(second)
    pos = position_xform(second)
    
    for first in first_list:        
    
        cmds.xform(first, ws=1, ro= rot)
        cmds.move(pos[0],pos[1], pos[2] ,first,rpr=1)


def offGRP_command(curve):
    '선택한 컨트롤러에 offGRP 생성'
    sels = cmds.ls(curve)

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
        #cre_jnt_grp = cmds.group(em=1, n= '%s%s'%(cre_jnt, '_GRP'))
        #cmds.parent(cre_jnt, cre_jnt_grp)
        
        cmds.move(i_po[0], i_po[1], i_po[2], cre_jnt, rpr=1 )
        cmds.xform(cre_jnt, ws=1, ro=i_ro)
            
        cmds.parentConstraint(i, cre_jnt, mo=1)
        cmds.scaleConstraint(i, cre_jnt, mo=1)

        skin_jnt_list.append(cre_jnt)


def offGRP_command_CTL(curve):
    '선택한 컨트롤러에 CTL_offGRP만생성'
    sels = cmds.ls(curve)

    ctrl_list = []

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



# [long_skirt_set]


class long_skirt_set():

    def __init__(self):
        self.create_UI()


    def create_UI(self):
        ## 윈도우 ID##
        windowID='long_UI'
        ##windows reset
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        cmds.window(windowID, t='long_UI', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
        ##master layer
        master = cmds.columnLayout()
        cmds.columnLayout()
        ##싱글 텍스트필드
        #cmds.rowColumnLayout( nc=1 )
        cmds.button(l=u'pose import' , w = 300 , h = 30 , c = pm.Callback(self.import_long_skirt))
        #cmds.rowColumnLayout( nc=1 )
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'    *  leg, knee, ankle에 위치한 컨트롤러는 고정')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        #cmds.text(l = u'up controller' ,w = 100)
        #cmds.textField('number_tex_box' , w = 30 , h = 20 , tx = '9', textChangedCommand='skirt_command.change_number()') # textChangedCommand는 ui에서 text를 바꿀때 커멘드입력이 안돼도 실시간으로 쿼리가능
        #cmds.textField('up number_tex_box' , w = 30 , h = 20 , tx = '2') # 기존 텍스트필드에 숫자입력방식
        cmds.intSliderGrp('up_segments', w=300, columnAttach = (1, 'left', 0), columnWidth =(1,97), field=True, l="    Up Segments", max=10, min=1, value=2)
        # 슬라이드바 방식, columnAttach와 columnWidth는 정렬 옵션
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        # cmds.text(l = u'down controller' ,w = 100)
        # cmds.textField('down number_tex_box' , w = 30 , h = 20 , tx = '2') # 기존 텍스트필드에 숫자입력방식
        cmds.intSliderGrp('down_segments', w=300, columnAttach = (1, 'left', 0), columnWidth =(1,97), field=True, l="    Down Segments", max=10, min=1, value=2) # 슬라이드바 방식
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'   -----------------------------------------------------------------------')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'total' ,w = 100)
        cmds.textField('total_tex_box' , w = 150 , h = 20 , tx = 'world_M_CTL')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'total'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'hip' , w = 100)
        cmds.textField('hip_tex_box' , w = 150 , h = 20 , tx = 'root_M_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'hip'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'spline01' , w = 100)
        cmds.textField('spn_01_tex_box' , w = 150 , h = 20 , tx = 'spine_01_M_skinJNT') 
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'spn'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'L_Leg' , w = 100)
        cmds.textField( 'L_leg_tex_box' , w = 150 , h = 20 , tx = 'leg_L_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'L_leg'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'L_Knee' , w = 100)
        cmds.textField( 'L_knee_tex_box' , w = 150 , h = 20 , tx = 'knee_L_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'L_knee'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'L_Ankle' , w = 100)
        cmds.textField( 'L_ankle_tex_box' , w = 150 , h = 20 , tx = 'ankle_L_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'L_ankle'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'R_Leg' , w = 100)
        cmds.textField( 'R_leg_tex_box' , w = 150 , h = 20 , tx = 'leg_R_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'R_leg'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'R_Knee' , w = 100)
        cmds.textField( 'R_knee_tex_box' , w = 150 , h = 20 , tx = 'knee_R_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'R_knee'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'R_Ankle' , w = 100)
        cmds.textField( 'R_ankle_tex_box' , w = 150 , h = 20 , tx = 'ankle_R_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'R_ankle'))
        cmds.setParent (master)
        cmds.button(l=u'배치' , w = 301 , h = 30 , c = pm.Callback(self.pose_position))
        cmds.setParent (master)
        cmds.button(l=u'연결' , w = 301 , h = 30 , c = pm.Callback(self.skirt_connect))
        cmds.setParent (master)
        cmds.showWindow(windowID)
        
        
    def import_long_skirt(self):
        long_skirt_bindpose = Set_route + 'long_skirt_pos.ma'
        cmds.file( long_skirt_bindpose, i = 1 , f = 1  )


    def sels_tex(self,part):
        sels = cmds.ls(sl=1)
        if part == "total":cmds.textField('total_tex_box'  , edit =1, tx= sels[0] )
        if part == "hip":cmds.textField('hip_tex_box'  , edit =1, tx= sels[0] )
        if part == "spn":cmds.textField('spn_01_tex_box'  , edit =1, tx= sels[0] )
        if part == "L_leg":cmds.textField('L_leg_tex_box'  , edit =1, tx= sels[0] )
        if part == "L_knee":cmds.textField('L_knee_tex_box'  , edit =1, tx= sels[0] )
        if part == "L_ankle":cmds.textField('L_ankle_tex_box'  , edit =1, tx= sels[0] )
        if part == "R_leg":cmds.textField('R_leg_tex_box'  , edit =1, tx= sels[0] )
        if part == "R_knee":cmds.textField('R_knee_tex_box'  , edit =1, tx= sels[0] )
        if part == "R_ankle":cmds.textField('R_ankle_tex_box'  , edit =1, tx= sels[0] )
        
       
    def pose_position(self):
    
        hip_JNT = cmds.textField( 'hip_tex_box' , q = 1 , text = 1)
        move_point('skirt_total_CTL_offGRP', hip_JNT)

        L_up_leg_JNT = cmds.textField( 'L_leg_tex_box' , q = 1 , text = 1)
        move_point('L_skirt_total_CTL', L_up_leg_JNT)

        L_low_leg_JNT = cmds.textField( 'L_knee_tex_box' , q = 1 , text = 1)
        move_point('L_leg_CTL', L_low_leg_JNT)

        # L_low_leg_JNT = cmds.textField( 'L_knee_tex_box' , q = 1 , text = 1)
        # move_point('down_L_skirt_total_CTL', L_low_leg_JNT)

        L_ankle_JNT = cmds.textField( 'L_ankle_tex_box' , q = 1 , text = 1)
        move_point('down_L_leg_CTL', L_ankle_JNT)

        spn_JNT = cmds.textField( 'spn_01_tex_box' , q = 1 , text = 1)
        move_point('waist_total_CTL', spn_JNT)


    def skirt_connect(self):
        cmds.disconnectAttr ('L_skirt_total_CTL.translateX', 'L_leg_CTL.translateX')
        cmds.disconnectAttr ('L_skirt_total_CTL.translateZ', 'L_leg_CTL.translateZ')
            
        top_loc_list = cmds.listRelatives('top_loc_GRP', c=1)
        mid_loc_list = cmds.listRelatives('mid_loc_GRP', c=1)

        top_loc_y = cmds.xform('top_01_loc',q=1,rp=1, ws=1)[1] # top loc의 Y축값만 쿼리
        top_loc_y = normalize_float(top_loc_y) # 소수점정리

        mid_loc_y = cmds.xform('mid_01_loc',q=1,rp=1, ws=1)[1] # mid loc의 Y축값만 쿼리
        mid_loc_y = normalize_float(mid_loc_y)

        low_loc_y = cmds.xform('low_01_loc',q=1,rp=1, ws=1)[1] # low loc의 Y축값만 쿼리
        low_loc_y = normalize_float(low_loc_y)

        # use_num = change_number() #사용자 지정 컨트롤러 갯수
        # num = (use_num-3) / 2 #허벅지 ~ 무릎, 무릎 ~ 발목 파트를 2개로 나눈다 (지정한 컨트롤러갯수 - 고정된컨트롤러(top,mid,low) / 2(윗다리,아랫다리)
        # top_con_num = (top_loc_y - mid_loc_y) / (num + 1)# 허벅지에서 무릎
        # # top Y축과 mid Y축 사이 (허벅지~무릎)에 컨트롤러갯수(num)+1 을 해주어야 등분갯수가 나온다(컨트롤러를 일정한간격으로 배치하기위함)
        # low_con_num = (mid_loc_y - low_loc_y) / (num + 1)# 무릎에서 발목

        up_use_num = change_number('up_segments')
        top_con_num = (top_loc_y - mid_loc_y) / (up_use_num + 1)# 허벅지에서 무릎

        down_use_num = change_number('down_segments')
        low_con_num = (mid_loc_y - low_loc_y) / (down_use_num + 1)# 무릎에서 발목

        top_leg_y_list = []
        for count in range(up_use_num):
            con_count = count+1
            top_leg_y = con_count * top_con_num
            top_con_po = top_loc_y - top_leg_y
            
            top_leg_y_list.append(top_con_po)
        #print top_leg_y_list
            
        low_leg_y_list = []
        for count in range(down_use_num+1): # 무릎 ~ 발목 은 맨아래컨트롤러가 하나 더 생성되어야 하기때문에 +1 해준다
            con_count = count+1
            low_leg_y = con_count * low_con_num
            low_con_po = mid_loc_y - low_leg_y
            
            low_leg_y_list.append(low_con_po)
        #print low_leg_y_list
            

    # ------------------------------- top_loc_GRP 에서 트랜스 X,Z를 쿼리 (허벅지 - 무릎)
        top_loc_x_list = []
        top_loc_z_list = []

        for top_loc_po in top_loc_list:
            
            po = cmds.xform(top_loc_po,q=1,rp=1, ws=1)
        
            
            top_loc_x_list.append(po[0]) #x축의 값
            top_loc_z_list.append(po[2]) #z축의 값

        top_loc_x_list = [ normalize_float(num) for num in top_loc_x_list ] #소수점 자리 정리
        top_loc_z_list = [ normalize_float(num) for num in top_loc_z_list ] 

    # ------------------------------- mid_loc_GRP 에서 트랜스 X,Z를 쿼리 (무릎 - 발목)
        mid_loc_x_list = []
        mid_loc_z_list = []

        for mid_loc_po in mid_loc_list:
            
            po = cmds.xform(mid_loc_po,q=1,rp=1, ws=1)
        
            
            mid_loc_x_list.append(po[0]) #x축의 값
            mid_loc_z_list.append(po[2]) #z축의 값

        mid_loc_x_list = [ normalize_float(num) for num in mid_loc_x_list ] #소수점 자리 정리
        mid_loc_z_list = [ normalize_float(num) for num in mid_loc_z_list ] 





        con_name_list = [u'skirt_F_M', u'skirt_L_A', u'skirt_L_B', u'skirt_L_D', u'skirt_L_F', u'skirt_L_G', u'skirt_B_M', u'skirt_R_G', u'skirt_R_F', u'skirt_R_D', u'skirt_R_B', u'skirt_R_A' ]
        # 컨트롤러 프리픽스네임 리스트
        top_FK_last_list = []
        top_IK_last_JNT_list = []

        # 허벅지 - 무릎 / FK컨트롤러 생성
        for loc_x, loc_z, con_name in zip(top_loc_x_list, top_loc_z_list, con_name_list): # x축과 z축은 한줄씩 고정값임
            
            for i, top_loc_y  in enumerate(top_leg_y_list): # y축은 치마 길이에따라 변화됨
                top_FK_con = cmds.duplicate('FK_con', n= con_name + '_FK_%02d_CTL'%(i+2))
                cmds.move(loc_x, top_loc_y, loc_z,  top_FK_con)

                fix_rotate = rotate_xform(con_name + '_FK_01_CTL') # 만들어질 컨트롤러의 기준 로테이션은 FK_01 컨트롤러에서 추출
                cmds.xform(top_FK_con, ws=1, ro= fix_rotate)
                
                offGRP_command_CTL(top_FK_con)
                cmds.parent( con_name + '_FK_%02d_CTL_offGRP'%(i+2), con_name + '_FK_%02d_CTL'%(i+1) ) # FK컨트롤러 하이라키 정리
            top_FK_last_list.append(top_FK_con[0])
            # top fk컨트롤러의 마지막 컨트롤러를 리스트화시킨다(쿼리해서 point_loc가 그 밑에 하이라키로 들어갈수있게하기 위함)

        # 허벅지 - 무릎 / IK컨트롤러 생성
        for loc_x, loc_z, con_name in zip(top_loc_x_list, top_loc_z_list, con_name_list): # x축과 z축은 한줄씩 고정값임
            
            for i, top_loc_y  in enumerate(top_leg_y_list): # y축은 치마 길이에따라 변화됨
                top_IK_con = cmds.duplicate('IK_con', n= con_name + '_IK_%02d_CTL'%(i+2))
                cmds.move(loc_x, top_loc_y, loc_z,  top_IK_con)

                fix_rotate = rotate_xform(con_name + '_FK_01_CTL') # 만들어질 컨트롤러의 기준 로테이션은 FK_01 컨트롤러에서 추출
                cmds.xform(top_IK_con, ws=1, ro= fix_rotate)

                offGRP_command(top_IK_con)
                cmds.parent( con_name + '_IK_%02d_CTL_offGRP'%(i+2), con_name + '_FK_%02d_CTL'%(i+2) ) # IK컨트롤러 하이라키 정리
                cmds.parent( con_name + '_IK_%02d_skinJNT'%(i+2), con_name + '_IK_%02d_skinJNT'%(i+1) ) # IK스킨조인트 하이라키 정리

                cmds.connectAttr('down_skirt_RIG_setup_CTL.ikVis', con_name + '_IK_%02d_CTL_offGRP'%(i+2) + '.visibility')
                # IK_vis 연결

            top_IK_last_JNT = con_name + '_IK_%02d_skinJNT'%(i+2) # 허벅지 - 무릎의 마지막조인트, down_IK조인트와 하이라키로 이어주기위해 쿼리
            top_IK_last_JNT_list.append(top_IK_last_JNT)
        
        
        
        point_loc_list = []      
        for loc_x, loc_z, con_name in zip(mid_loc_x_list, mid_loc_z_list, con_name_list):
        
            # 무릎 - 발목 / FK컨트롤러 생성    
            for i, low_loc_y in enumerate(low_leg_y_list):
                low_FK_con = cmds.duplicate('FK_con', n= 'down_' + con_name + '_FK_%02d_CTL'%(i+2))
                cmds.move(loc_x, low_loc_y, loc_z,  low_FK_con)

                fix_rotate = rotate_xform('down_' + con_name + '_FK_01_CTL') # 만들어질 컨트롤러의 기준 로테이션은 FK_01 컨트롤러에서 추출
                cmds.xform(low_FK_con, ws=1, ro= fix_rotate)
                
                offGRP_command_CTL(low_FK_con)
                cmds.parent( 'down_' + con_name + '_FK_%02d_CTL_offGRP'%(i+2), 'down_' + con_name + '_FK_%02d_CTL'%(i+1) ) # down FK컨트롤러 하이라키 정리

            # 무릎 - 발목 / IK컨트롤러 생성
            for i, low_loc_y in enumerate(low_leg_y_list):
                low_IK_con = cmds.duplicate('IK_con', n= 'down_' + con_name + '_IK_%02d_CTL'%(i+2))
                cmds.move(loc_x, low_loc_y, loc_z,  low_IK_con)

                fix_rotate = rotate_xform('down_' + con_name + '_FK_01_CTL') # 만들어질 컨트롤러의 기준 로테이션은 FK_01 컨트롤러에서 추출
                cmds.xform(low_IK_con, ws=1, ro= fix_rotate)
                
                offGRP_command(low_IK_con)
                cmds.parent( 'down_' + con_name + '_IK_%02d_CTL_offGRP'%(i+2), 'down_' + con_name + '_FK_%02d_CTL'%(i+2) ) # down IK컨트롤러 하이라키 정리
                cmds.parent( 'down_' + con_name + '_IK_%02d_skinJNT'%(i+2), 'down_' + con_name + '_IK_%02d_skinJNT'%(i+1) ) # down IK스킨조인트 하이라키 정리

                cmds.connectAttr('down_skirt_RIG_setup_CTL.ikVis', 'down_' + con_name + '_IK_%02d_CTL_offGRP'%(i+2) + '.visibility')
                # IK_vis 연결


        # 허벅지 - 무릎의 마지막 조인트와, 무릎 - 발목의 첫 조인트를 하이라키로 연결
        for top_IK_last_JNT, con_name in zip(top_IK_last_JNT_list, con_name_list):

            cmds.parent( 'down_' + con_name + '_IK_01_skinJNT', top_IK_last_JNT )
            point_loc = cmds.spaceLocator(n = (con_name + '_point_loc')) 
            cmds.setAttr (point_loc[0] + '.visibility', 0) # point_loc 하이드
            # point로케이터를 생성(loc -> down fk의 첫번째 컨트롤러에 포인트 컨스트레인을 하기위함)

            down_FK_firt = ('down_' + con_name + '_FK_01_CTL_offGRP') # down FK 의 첫번째 컨트롤러
            move( point_loc, down_FK_firt ) # down FK 의 첫번째 컨트롤러와 위치를 똑같이 맞춰준다
            point_loc_list.append(point_loc)# point_loc 리스트화(하이라키 구조로 전부 넣기 위함)

        down_FK_firt_list = []
        for top_FK_last,point_loc,con_name in zip(top_FK_last_list,point_loc_list,con_name_list):
            
            cmds.parent(point_loc, top_FK_last) #point_loc는 up_FK컨트롤러의 하이라키 최하위에 있어야됨(FK마지막)
            down_FK_firt = ('down_' + con_name + '_FK_01_CTL_offGRP')
            down_FK_firt_sub = ('down_' + con_name + '_FK_01_CTL_key_GRP') # 무릎 FK1번 key그룹
            cmds.pointConstraint(point_loc, down_FK_firt, mo=1, w=1) # point_loc가 무릎FK 1번을 point로 물고있는다
            cmds.orientConstraint(point_loc, down_FK_firt_sub, mo=1, w=1) # point_loc가 무릎 FK 1번 key그룹에 오리엔트(knee_FK_rotate 스위치를 위함)
            cmds.connectAttr ('down_skirt_RIG_setup_CTL.kneeFkRotate', down_FK_firt_sub + '_orientConstraint1.' + con_name + '_point_locW0')
            # knee_FK_rotate on/off 스위치 연결

            down_FK_firt_list.append(down_FK_firt)

        
        lower_joint = cmds.listRelatives('skirt_IK_skinJNT_GRP', ad=1, pa=1, typ='joint') 
        sel_lower_joint = cmds.select(lower_joint)
        cmds.sets(n='skirt_skinJNT_set') # skirt_skinJNT_set 생성
        hip_JNT = cmds.textField( 'hip_tex_box' , q = 1 , text = 1) # root조인트
        for con_name in con_name_list:
            cmds.parent(con_name + '_IK_01_skinJNT', hip_JNT) # root조인트 밑으로 치마조인트가 들어가게 하이라키 정리
        cmds.delete('skirt_RIG_skinJNT_GRP') # 비어있는 스킨조인트 그룹은 삭제


        cmds.delete('con_shape') # 컨트롤러 복사가 끝난뒤 con_shape 그룹은 삭제

        # legFollow 옵션에 따라 point컨스트레인 on/off
        cmds.createNode( 'reverse', n = 'down_point_reverse')
        cmds.connectAttr ('down_skirt_RIG_setup_CTL.legFollow', 'down_point_reverse.inputX')
        for down_FK_firt,con_name in zip(down_FK_firt_list,con_name_list):
            cmds.connectAttr ('down_point_reverse.outputX', down_FK_firt + '_pointConstraint1.' + con_name + '_point_locW0' )
            
        # 빌드후 리깅 셋팅 관련 어트리뷰트는 하이드            
        cmds.setAttr("down_skirt_RIG_setup_CTL.skirtLength", lock=True, keyable=False, channelBox=False) # 빌드후 skirtLength lock
        cmds.setAttr("down_skirt_RIG_setup_CTL.____Rig____", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("down_skirt_RIG_setup_CTL.legSkirtStrength", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("down_skirt_RIG_setup_CTL.middleSkirtStrength", lock=True, keyable=False, channelBox=False)




        # cmds.setAttr('skirt_sub_RIG_FK_CTL_GRP.visibility',1)
        # cmds.setAttr('skirt_RIG_skinJNT_GRP.visibility',1)
        # cmds.setAttr('skirt_sub_total_CTL.visibility',1)
        # cmds.setAttr('skirt_RIG_setup_CTL_offGRP.visibility',1)


        total_ui = cmds.textField( 'total_tex_box' , q = 1 , text = 1)
        hip_ui = cmds.textField( 'hip_tex_box' , q = 1 , text = 1)
        spn_ui = cmds.textField( 'spn_01_tex_box' , q = 1 , text = 1) 
        L_up_leg_ui = cmds.textField( 'L_leg_tex_box' , q = 1 , text = 1)
        L_low_leg_ui = cmds.textField( 'L_knee_tex_box' , q = 1 , text = 1)
        L_ankle_ui = cmds.textField( 'L_ankle_tex_box' , q = 1 , text = 1)

        R_up_leg_ui = cmds.textField( 'R_leg_tex_box' , q = 1 , text = 1)
        R_low_leg_ui = cmds.textField( 'R_knee_tex_box' , q = 1 , text = 1)
        R_ankle_ui = cmds.textField( 'R_ankle_tex_box' , q = 1 , text = 1)

        sels=cmds.sets( 'delete_set',int='delete_set')
        cmds.delete(sels)
        cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_front_M_FK_01_rot_pin' , mo=1, w=1)
        cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_back_M_FK_01_rot_pin' , mo=1, w=1)
        cmds.parentConstraint( total_ui , 'skirt_total_CTL_offGRP' , mo=1, w=1)
        cmds.scaleConstraint( total_ui , 'skirt_total_CTL_offGRP' , mo=1, w=1)
        cmds.pointConstraint( hip_ui , 'skirt_total_CTL_GRP' , mo=1, w=1)


        cmds.parentConstraint( spn_ui , 'waist_total_CTL' , mo=1, w=1)
        cmds.pointConstraint( L_up_leg_ui , 'L_skirt_total_CTL' , mo=1, w=1)
        cmds.pointConstraint( R_up_leg_ui , 'R_skirt_total_CTL' , mo=1, w=1)

        cmds.parentConstraint( L_low_leg_ui , 'L_leg_CTL' , mo=1, w=1) # skirt_auto on/off 시 전환
        cmds.parentConstraint( 'L_skirt_total_CTL' , 'L_leg_CTL' , mo=1, w=1) # skirt_auto on/off 시 전환
        cmds.parentConstraint( R_low_leg_ui , 'R_leg_CTL' , mo=1, w=1)
        cmds.parentConstraint( 'R_skirt_total_CTL' , 'R_leg_CTL' , mo=1, w=1)

        cmds.parentConstraint( L_ankle_ui , 'down_L_leg_CTL' , mo=1, w=1) # skirt_auto on/off 시 전환
        cmds.parentConstraint( 'down_L_skirt_total_CTL' , 'down_L_leg_CTL' , mo=1, w=1) # skirt_auto on/off 시 전환
        cmds.parentConstraint( R_ankle_ui , 'down_R_leg_CTL' , mo=1, w=1)
        cmds.parentConstraint( 'down_R_skirt_total_CTL' , 'down_R_leg_CTL' , mo=1, w=1)



        move_point('L_ankle_loc', L_ankle_ui)
        move_point('R_ankle_loc', R_ankle_ui)
        cmds.parentConstraint( L_ankle_ui , 'L_ankle_loc' , mo=1, w=1)
        cmds.parentConstraint( R_ankle_ui , 'R_ankle_loc' , mo=1, w=1)

        # leg_follow
        cmds.parentConstraint('L_skirt_total_CTL', 'down_L_skirt_total_CTL_offGRP', mo=1, w=1)
        cmds.parentConstraint('R_skirt_total_CTL', 'down_R_skirt_total_CTL_offGRP', mo=1, w=1)
        cmds.connectAttr ('down_skirt_RIG_setup_CTL.legFollow', 'down_L_skirt_total_CTL_offGRP_parentConstraint1.L_leg_CTLW0')
        cmds.connectAttr ('down_skirt_RIG_setup_CTL.legFollow', 'down_R_skirt_total_CTL_offGRP_parentConstraint1.R_leg_CTLW0')
        cmds.connectAttr ('leg_follow_reverse.outputX', 'down_L_skirt_total_CTL_offGRP_parentConstraint1.L_skirt_total_CTLW1')
        cmds.connectAttr ('leg_follow_reverse.outputX', 'down_R_skirt_total_CTL_offGRP_parentConstraint1.R_skirt_total_CTLW1')

        cmds.pointConstraint('down_L_front_skirt_trans_sub_CTL', 'down_skirt_sub_side_L_01_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_L_side_L_01_skirt_trans_sub_CTL', 'down_skirt_sub_side_L_02_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_L_side_L_03_skirt_trans_sub_CTL', 'down_skirt_sub_side_L_04_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_L_side_L_05_skirt_trans_sub_CTL', 'down_skirt_sub_side_L_06_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_L_side_back_skirt_trans_sub_CTL', 'down_skirt_sub_side_L_07_FK_01_CTL_offGRP', mo=1, w=1)

        cmds.pointConstraint('down_M_front_skirt_trans_sub_CTL', 'down_skirt_sub_front_M_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_M_side_back_skirt_trans_sub_CTL', 'down_skirt_sub_back_M_FK_01_CTL_offGRP', mo=1, w=1)

        cmds.pointConstraint('down_R_front_skirt_trans_sub_CTL', 'down_skirt_sub_side_R_01_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_R_side_R_01_skirt_trans_sub_CTL', 'down_skirt_sub_side_R_02_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_R_side_R_03_skirt_trans_sub_CTL', 'down_skirt_sub_side_R_04_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_R_side_R_05_skirt_trans_sub_CTL', 'down_skirt_sub_side_R_06_FK_01_CTL_offGRP', mo=1, w=1)
        cmds.pointConstraint('down_R_side_back_skirt_trans_sub_CTL', 'down_skirt_sub_side_R_07_FK_01_CTL_offGRP', mo=1, w=1)





        i=1
        for b in range(7):
            cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_side_L_%02d_FK_01_rot_pin'%i , mo=1, w=1)
            cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_side_R_%02d_FK_01_rot_pin'%i , mo=1, w=1)
            
            i=i+1


        pin_GRP_list = cmds.listRelatives('skirt_sub_FK_01_rot_pin_GRP',children=1)
        pin_loc_list = cmds.listRelatives(pin_GRP_list,children=1)
        #for pin_loc in pin_loc_list:
            #cmds.connectAttr('skirt_RIG_setup_CTL.waist_pin', pin_loc + '_parentConstraint1.skirt_sub_total_CTLW0')

        cmds.setAttr ("down_skirt_RIG_setup_CTL.legFollow", 0)
        cmds.setAttr("down_skirt_RIG_setup_CTL.legFollow", lock=True, keyable=False, channelBox=False) # 빌드후 leg follow lock


        #skirt_auto 스위치
        cmds.createNode('reverse', n='skirt_auto_reverse')
        
        #skirt_auto on
        cmds.connectAttr('down_skirt_RIG_setup_CTL.skirtAuto', 'L_leg_CTL_parentConstraint1.knee_L_skinJNTW0')
        cmds.connectAttr('down_skirt_RIG_setup_CTL.skirtAuto', 'R_leg_CTL_parentConstraint1.knee_R_skinJNTW0')
        cmds.connectAttr('down_skirt_RIG_setup_CTL.skirtAuto', 'down_L_leg_CTL_parentConstraint1.ankle_L_skinJNTW0')
        cmds.connectAttr('down_skirt_RIG_setup_CTL.skirtAuto', 'down_R_leg_CTL_parentConstraint1.ankle_R_skinJNTW0')

        #skirt_auto off
        cmds.connectAttr('down_skirt_RIG_setup_CTL.skirtAuto', 'skirt_auto_reverse.inputX')
        cmds.connectAttr('skirt_auto_reverse.outputX', 'L_leg_CTL_parentConstraint1.L_skirt_total_CTLW1')
        cmds.connectAttr('skirt_auto_reverse.outputX', 'R_leg_CTL_parentConstraint1.R_skirt_total_CTLW1')
        cmds.connectAttr('skirt_auto_reverse.outputX', 'down_L_leg_CTL_parentConstraint1.down_L_skirt_total_CTLW1')
        cmds.connectAttr('skirt_auto_reverse.outputX', 'down_R_leg_CTL_parentConstraint1.down_R_skirt_total_CTLW1')

        # 빌드 후 옵션
        cmds.disconnectAttr ('L_leg_CTL_parentConstraint1.constraintRotateX', 'L_leg_CTL.rotateX') # 로테이트 브레이크커넥션
        cmds.disconnectAttr ('L_leg_CTL_parentConstraint1.constraintRotateY', 'L_leg_CTL.rotateY')
        cmds.disconnectAttr ('L_leg_CTL_parentConstraint1.constraintRotateZ', 'L_leg_CTL.rotateZ')
        cmds.disconnectAttr ('R_leg_CTL_parentConstraint1.constraintRotateX', 'R_leg_CTL.rotateX')
        cmds.disconnectAttr ('R_leg_CTL_parentConstraint1.constraintRotateY', 'R_leg_CTL.rotateY')
        cmds.disconnectAttr ('R_leg_CTL_parentConstraint1.constraintRotateZ', 'R_leg_CTL.rotateZ')

        cmds.disconnectAttr ('down_L_leg_CTL_parentConstraint1.constraintRotateX', 'down_L_leg_CTL.rotateX') # 로테이트 브레이크커넥션
        cmds.disconnectAttr ('down_L_leg_CTL_parentConstraint1.constraintRotateY', 'down_L_leg_CTL.rotateY')
        cmds.disconnectAttr ('down_L_leg_CTL_parentConstraint1.constraintRotateZ', 'down_L_leg_CTL.rotateZ')
        cmds.disconnectAttr ('down_R_leg_CTL_parentConstraint1.constraintRotateX', 'down_R_leg_CTL.rotateX')
        cmds.disconnectAttr ('down_R_leg_CTL_parentConstraint1.constraintRotateY', 'down_R_leg_CTL.rotateY')
        cmds.disconnectAttr ('down_R_leg_CTL_parentConstraint1.constraintRotateZ', 'down_R_leg_CTL.rotateZ')

        cmds.connectAttr ('root_M_skinJNT.rotateY', 'skirt_total_CTL_GRP.rotateY')
        cmds.createNode('plusMinusAverage', n='main_world_plus')
        cmds.createNode('multiplyDivide', n='main_world_plus_reverse')
        cmds.setAttr ("main_world_plus_reverse.input2X", -1)

        cmds.connectAttr ('main_M_CTL.rotateY', 'main_world_plus.input1D[0]')
        cmds.connectAttr ('world_M_CTL.rotateY', 'main_world_plus.input1D[1]')
        cmds.connectAttr ('main_world_plus.output1D', 'main_world_plus_reverse.input1X')
        cmds.connectAttr ('main_world_plus_reverse.outputX', 'skirt_total_CTL_GRP_reverse.rotateY')








        cmds.setAttr ('down_skirt_RIG_setup_CTL.skirtAuto', 1)

        cmds.setAttr ('skirt_total_CTLShape.visibility', 0)
        cmds.setAttr ('waist_total_CTL.visibility', 0)
        cmds.setAttr ('L_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('R_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('M_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('L_leg_CTL.visibility', 0)
        cmds.setAttr ('R_leg_CTL.visibility', 0)
        cmds.setAttr ('down_L_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('down_R_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('down_M_skirt_total_CTL.visibility', 0)
        cmds.setAttr ('down_L_leg_CTL.visibility', 0)
        cmds.setAttr ('down_R_leg_CTL.visibility', 0)
        cmds.setAttr ('ankle_M_skirt_total_CTL_offGRP.visibility', 0)



# [short_skirt_set]


class short_skirt_set():

    def __init__(self):
        self.create_UI()


    def create_UI(self):
        ## 윈도우 ID##
        windowID='short_UI'
        ##windows reset
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        cmds.window(windowID, t='short_UI', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
        ##master layer
        master = cmds.columnLayout()
        cmds.columnLayout()
        ##싱글 텍스트필드
        #cmds.rowColumnLayout( nc=1 )
        cmds.button(l=u'pose import' , w = 300 , h = 30 , c = pm.Callback(self.import_short_skirt))
        #cmds.rowColumnLayout( nc=1 )
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'controller count' ,w = 100)
        #cmds.textField('number_tex_box' , w = 30 , h = 20 , tx = '9', textChangedCommand='skirt_command.change_number()') # textChangedCommand는 ui에서 text를 바꿀때 커멘드입력이 안돼도 실시간으로 쿼리가능
        cmds.textField('number_tex_box' , w = 30 , h = 20 , tx = '7')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'total' ,w = 100)
        cmds.textField('total_tex_box' , w = 150 , h = 20 , tx = 'world_M_CTL')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'total'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'hip' , w = 100)
        cmds.textField('hip_tex_box' , w = 150 , h = 20 , tx = 'root_M_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'hip'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'spline01' , w = 100)
        cmds.textField('spn_01_tex_box' , w = 150 , h = 20 , tx = 'spine_01_M_skinJNT') 
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'spn'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'L_Leg' , w = 100)
        cmds.textField( 'L_leg_tex_box' , w = 150 , h = 20 , tx = 'leg_L_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'L_leg'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'L_Knee' , w = 100)
        cmds.textField( 'L_knee_tex_box' , w = 150 , h = 20 , tx = 'knee_L_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'L_knee'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'R_Leg' , w = 100)
        cmds.textField( 'R_leg_tex_box' , w = 150 , h = 20 , tx = 'leg_R_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'R_leg'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'R_Knee' , w = 100)
        cmds.textField( 'R_knee_tex_box' , w = 150 , h = 20 , tx = 'knee_R_skinJNT')
        cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'R_knee'))
        cmds.setParent (master)
        cmds.button(l=u'배치' , w = 301 , h = 30 , c = pm.Callback(self.pose_position))
        cmds.setParent (master)
        cmds.button(l=u'연결' , w = 301 , h = 30 , c = pm.Callback(self.skirt_connect))
        cmds.setParent (master)
        cmds.showWindow(windowID)


    def import_short_skirt(self):
            short_skirt_bindpose = Set_route + 'short_skirt_pos.ma'
            cmds.file( short_skirt_bindpose, i = 1 , f = 1  )


    def sels_tex(self, part):
        print 'sel_import'
        sels = cmds.ls(sl=1)
        if part == "total":cmds.textField('total_tex_box'  , edit =1, tx= sels[0] )
        if part == "hip":cmds.textField('hip_tex_box'  , edit =1, tx= sels[0] )
        if part == "spn":cmds.textField('spn_01_tex_box'  , edit =1, tx= sels[0] )
        if part == "L_leg":cmds.textField('L_leg_tex_box'  , edit =1, tx= sels[0] )
        if part == "L_knee":cmds.textField('L_knee_tex_box'  , edit =1, tx= sels[0] )
        if part == "R_leg":cmds.textField('R_leg_tex_box'  , edit =1, tx= sels[0] )
        if part == "R_knee":cmds.textField('R_knee_tex_box'  , edit =1, tx= sels[0] )

        
    def pose_position(self):
    
        hip_JNT = cmds.textField( 'hip_tex_box' , q = 1 , text = 1)
        move_point('skirt_total_CTL_offGRP', hip_JNT)

        L_up_leg_JNT = cmds.textField( 'L_leg_tex_box' , q = 1 , text = 1)
        move_point('L_skirt_total_CTL', L_up_leg_JNT)

        L_low_leg_JNT = cmds.textField( 'L_knee_tex_box' , q = 1 , text = 1)
        move_point('L_leg_CTL', L_low_leg_JNT)

        spn_JNT = cmds.textField( 'spn_01_tex_box' , q = 1 , text = 1)
        move_point('waist_total_CTL', spn_JNT)


    def skirt_connect(self):
        total_ui = cmds.textField( 'total_tex_box' , q = 1 , text = 1)
        hip_ui = cmds.textField( 'hip_tex_box' , q = 1 , text = 1)
        spn_ui = cmds.textField( 'spn_01_tex_box' , q = 1 , text = 1) 
        L_up_leg_ui = cmds.textField( 'L_leg_tex_box' , q = 1 , text = 1)
        L_low_leg_ui = cmds.textField( 'L_knee_tex_box' , q = 1 , text = 1)
        R_up_leg_ui = cmds.textField( 'R_leg_tex_box' , q = 1 , text = 1)
        R_low_leg_ui = cmds.textField( 'R_knee_tex_box' , q = 1 , text = 1)
        sels=cmds.sets( 'delete_set',int='delete_set')
        cmds.delete(sels)
        cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_front_M_fk_01_rot_pin' , mo=1, w=1)
        cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_back_M_fk_01_rot_pin' , mo=1, w=1)
        cmds.parentConstraint( hip_ui , 'skirt_total_CTL_offGRP' , mo=1, w=1)
        cmds.scaleConstraint( hip_ui , 'skirt_total_CTL_offGRP' , mo=1, w=1)
        cmds.parentConstraint( spn_ui , 'waist_total_CTL' , mo=1, w=1)
        cmds.pointConstraint( L_up_leg_ui , 'L_skirt_total_CTL' , mo=1, w=1)
        cmds.pointConstraint( R_up_leg_ui , 'R_skirt_total_CTL' , mo=1, w=1)
        cmds.pointConstraint( L_low_leg_ui , 'L_leg_CTL' , mo=1, w=1)
        cmds.pointConstraint( R_low_leg_ui , 'R_leg_CTL' , mo=1, w=1)
        i=1
        for b in range(7):
            cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_side_L_%02d_fk_01_rot_pin'%i , mo=1, w=1)
            cmds.parentConstraint( 'skirt_sub_total_CTL' , 'skirt_sub_side_R_%02d_fk_01_rot_pin'%i , mo=1, w=1)
            
            i=i+1



# [hair_set]
class hair_set():

    def __init__(self):
        self.create_UI()
        global prefix_name
        prefix_name = cmds.textField('prefix_tex_box' , tx=1,q=1 )

    def create_UI(self):
        ## 윈도우 ID##
        windowID='hair_UI'
        ##windows reset
        if cmds.window(windowID, ex=True):
            cmds.deleteUI(windowID)
        cmds.window(windowID, t='hair_UI', rtf=True, s=True, mnb=True, mxb=True,wh=(30,30))
        ##master layer
        master = cmds.columnLayout()
        cmds.columnLayout()
        ##싱글 텍스트필드
        #cmds.text(l = u'    *  leg, knee, ankle에 위치한 컨트롤러는 고정')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        #cmds.text(l = u'   -----------------------------------------------------------------------')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.text(l = u'prefix name' ,w = 100)
        cmds.textField('prefix_tex_box' , w = 150 , h = 20 , tx = 'hair_')
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.intSliderGrp('CTL', w=300, columnAttach = (1, 'left', 0), columnWidth =(1,97), field=True, l="       CTL", max=20, min=3, value=3)
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.button(l=u'create controller' , w = 300 , h = 30 , c = pm.Callback(self.set_bindpose))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.intSliderGrp('skinJNT', w=300, columnAttach = (1, 'left', 0), columnWidth =(1,97), field=True, l="       skinJNT", max=20, min=3, value=3)
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.button(l=u'Build' , w = 300 , h = 30 , c = pm.Callback(self.set_build))
        #cmds.button( l = u'등록' , w = 50 , c = pm.Callback(self.sels_tex, 'total'))
        cmds.setParent (master)
        cmds.rowColumnLayout( nr=1 )
        cmds.setParent (master)
        #cmds.button(l=u'연결' , w = 301 , h = 30 , c = pm.Callback(self.skirt_connect))
        cmds.setParent (master)
        cmds.showWindow(windowID)


    def change_number(part):
        base_num=cmds.intSliderGrp(part, q=1, value=1)
        base_num = int(base_num)
        return base_num

    def set_bindpose(self):
        global cre_loc_grp
        cre_loc_grp = []
        segments = change_number('CTL')
        prefix_name = cmds.textField('prefix_tex_box' , tx=1,q=1 )
        for i in range(segments):
          
            #cre_loc = cmds.spaceLocator(n = prefix_name + '%02d'%(i+1) + '_bindpose')[0]
            cre_loc = self.con_shape('locator', prefix_name + '%02d'%(i+1) + '_bindpose')
            
            cmds.setAttr(cre_loc + '.translateY', -i)
            cmds.setAttr(cre_loc + '.scaleX', 0.1)
            cmds.setAttr(cre_loc + '.scaleY', 0.1)
            cmds.setAttr(cre_loc + '.scaleZ', 0.1)
            cmds.makeIdentity(apply=True, s=1, pn=1, n=0)

            cmds.setAttr(cre_loc + '.overrideEnabled' , 1)
            cmds.setAttr(cre_loc + '.overrideColor' , 17)
            cre_loc_grp.append(cre_loc)

        cre_loc_grp = list(reversed(cre_loc_grp))
        cre_loc_num = len(cre_loc_grp)
        

        for i in range(cre_loc_num):
            try:
                cmds.parent(cre_loc_grp[i], cre_loc_grp[i+1])
            except:
                pass
        
        cmds.select(cre_loc_grp[-1])

        
            

    def con_shape(self,shape,name):
        if shape == 'locator':
            cre_curve = cmds.curve(d=1, n=name, p=[(0.0, 2.001501540839854, 0.0),
            (0.0, -2.001501540839854, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, -2.001501540839854),
            (0.0, 0.0, 2.001501540839854),
            (0.0, 0.0, 0.0),
            (2.001501540839854, 0.0, 0.0),
            (-2.001501540839854, 0.0, 0.0)])

            

        if shape == 'box':
            cre_curve = cmds.curve(d=1, n=name, p=[ (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, 2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, 2.001501540839854),
        (-2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, 2.001501540839854, -2.001501540839854),
        (2.001501540839854, -2.001501540839854, -2.001501540839854),
        (-2.001501540839854, -2.001501540839854, -2.001501540839854)])
        
        else:
            pass

        return cre_curve


    def nubs_match(self, name):
        global cluster_grp
        global cre_nub
        global segments

        cluster_grp = []
        segments = change_number('CTL')
        cre_nub = cmds.nurbsPlane(ch=1, d=1, v=segments-1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1, n=name)[0]

        for i in range(segments):
            cre_cluster = cmds.cluster(cre_nub + '.cv[0:1][%s]'%(i))[0]
            cluster_grp.append(cre_cluster)
        
        
    def A2B(self, fir,sec):
        'A를 B로 이동한다.'

        a= cmds.ls(fir, sec)
        
        rot = cmds.xform(a[-1], q=1, ws=1, ro=1)
        pos = cmds.xform(a[-1], q=1, ws=1, rp=1)
        
        for c in a[0:-1]:        
        
            cmds.xform(c, ws=1, ro= rot)
            cmds.move(pos[0],pos[1], pos[2] ,c,rpr=1)


    def set_build(self):
        self.nubs_match('hair_linear_nub')
        cre_loc_grp_ = list(reversed(cre_loc_grp))

        for cluster_, loc_ in zip(cluster_grp, cre_loc_grp_):
            self.A2B(cluster_ + 'Handle', loc_)

        cmds.rebuildSurface(cre_nub, rt=0, kc=0, fr=0, ch=1, end=1, sv=segments-1, su=1, kr=0, dir=2, kcp=0, tol=0.01, dv=3, du=3, rpo=1)    
        cmds.delete(cre_nub, constructionHistory = True)

        first_po = cre_loc_grp_[0]
        second_po = cre_loc_grp_[-1]
        
      
        first_con = self.con_shape('box', prefix_name)
            
      
