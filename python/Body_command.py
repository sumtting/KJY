# -*- coding: utf-8 -*- 
import maya.cmds as cmds
import sys
import maya.mel as mel
import string 
import pymel.core as pm

Set_route = 'D:/KJY/python/Set/' # Set 폴더의 경로


class body_set():

    def __init__(self):
        if cmds.window('body_set_UI', q=1, ex=1):
            cmds.deleteUI('body_set_UI')
        cmds.window('body_set_UI', ret=1, w=264, t='body_set', h=124, s=1, mb=1)
        cmds.columnLayout('body_set_columnLayout', w=262, h=120)
        cmds.separator('body_set_separator1')
        cmds.button('body_set_button1', w=260, h=30, l='Pose Import', c=pm.Callback(self.import_body_pose))
        cmds.separator('body_set_separator3')
        cmds.button('body_set_button2', w=260, h=30, l='Build', c=pm.Callback(self.body_build))
        cmds.showWindow('body_set_UI')


    def import_body_pose(self):
        body_bindpose = Set_route + 'body_pos.ma'
        cmds.file( body_bindpose, i = 1 , f = 1  )



    def body_build(self):
        self.setSpineNeck()
        self.setArm()
        self.setLeg()
        self.setHand()
        self.setFoot()
        self.delPreAtt()
        #self.delEmpty()
        self.patchUp_20140331()
        self.keySet()
        self.setEye()

        #######################
        #ext_ctrl 보이게 한다
        cmds.setAttr("total_ctrl.exCtrls_vis", 0)



    ##############################/
    #필요한 기능펑션선언

    ##############################
    #$obj01의 위치로 $obj02의 위치를 맞추는 함수


    def changeLoc(self, obj01, obj02):
        
        pos01=cmds.xform(obj01, q=1, rotatePivot=1, ws=1, absolute=1)
        pos02=cmds.xform(obj02, q=1, rotatePivot=1, ws=1, absolute=1)
        tmpX01=pos01[0]
        tmpY01=pos01[1]
        tmpZ01=pos01[2]
        tmpX02=pos02[0]
        tmpY02=pos02[1]
        tmpZ02=pos02[2]
        tmpX=(tmpX01 - tmpX02)
        tmpY=(tmpY01 - tmpY02)
        tmpZ=(tmpZ01 - tmpZ02)
        cmds.move(tmpX, tmpY, tmpZ, obj02, r=1, ws=1, wd=1)
        

    ########################################
    #조인트에 넙스 컨트롤을 만드는 함수

    def ctrlCreat(self, sel, x, y, z, r):
        
        joint = ""
        for joint in sel:
            loc=cmds.xform(joint, q=1, ws=1, t=1)
            cmds.circle(fp=(loc[0], loc[1], loc[2]), nr=(x, y, z), r=r, sw=360, n=(joint + "_control"))
            cmds.parent((joint + "_controlShape"), 
                joint, shape=1, r=1)
            cmds.setAttr((joint + "_controlShape.overrideEnabled"), 
                1)
            cmds.setAttr((joint + "_controlShape.overrideColor"), 
                18)
            cmds.delete(joint + "_control")
            cmds.DeleteHistory()
            

    ##################################/
    #피벗의 위치를 이동시키는 함수

    def changeLoc_PV(self, obj01, obj02):
        
        pos01=cmds.xform(obj01, q=1, rotatePivot=1, ws=1, absolute=1)
        pos02=cmds.xform(obj02, q=1, rotatePivot=1, ws=1, absolute=1)
        tmpX01=pos01[0]
        tmpY01=pos01[1]
        tmpZ01=pos01[2]
        tmpX02=pos02[0]
        tmpY02=pos02[1]
        tmpZ02=pos02[2]
        tmpX=(tmpX01 - tmpX02)
        tmpY=(tmpY01 - tmpY02)
        tmpZ=(tmpZ01 - tmpZ02)
        obj02_RP=obj02 + ".rotatePivot"
        obj02_SP=obj02 + ".scalePivot"
        cmds.move(tmpX, tmpY, tmpZ, obj02_RP, r=1, ws=1, wd=1)
        cmds.move(tmpX, tmpY, tmpZ, obj02_SP, r=1, ws=1, wd=1)
        


    ###########################################
    #두조인트 사이에 ikSC를 만드는 함수

    def ikSC(self, startJnt, endJnt, name, efftr):
        
        cmds.ikHandle(ee=endJnt, sj=startJnt, sol='ikSCsolver', n=name)
        autoEfftr=cmds.ikHandle(name, q=1, ee=1)
        cmds.select(autoEfftr, r=1)
        cmds.rename(autoEfftr, efftr)
        cmds.select(cl=1)
        

    ##############################/
    #각 부위별 세팅 펑션

    ################################/
    #목과, 허리를 세팅하는 함수
    #목과 척추를 세팅하고 머리와 허리에 pin_rot와 pin_pos, 그리고 pin_rot를 만든다.
    #만들어진 머리, 목, 가슴, 허리에 shldr와 hip을 연결한다.




    def setSpineNeck(self):


        ###########################################/

        #eye_UI_빼기
        cmds.select('eye_R_UI_grp_pre', r=1)
        cmds.select('eye_L_UI_grp_pre', add=1)
        cmds.parent(w=1)


        #UI 컨트롤러 제거
        cmds.delete('scale_UI_grp_pre')



        #################################
        #머리크기 조절하는 keyData와 cls를 지운다.

        cmds.disconnectAttr('head_jntEnd_tmp_translateX.output', 'head_jntEnd.translateX')
        cmds.delete('head_jntEnd_tmp_translateX')
        cmds.select('head_ctrl', r=1)
        cmds.DeleteHistory()


        #################################/
        #목과 허리 커브의 히스토리를 지운다.

        cmds.select('neck_crv', r=1)
        cmds.DeleteHistory()
        cmds.select('spine_crv', r=1)
        cmds.DeleteHistory()


        #히스토리 지우면서 상위 그룹도 지워지네..
        #select -r neck_crv_cls02_prntCnst_grp ;
        #select -add neck_crv_cls03_prntCnst_grp ;
        #select -add spine_crv_cls02_prntCnst_grp ;
        #select -add spine_crv_cls03_prntCnst_grp ;
        #doDelete;

        cmds.select(cl=1)

        ################################ # mel체크
        # 커브 스킨 조인트의 위치를 맞춘다.

        self.changeLoc("neck_ik_jnt01", "neck_crvCtrl_jnt01")
        self.changeLoc("neck_ik_jnt03", "neck_crvCtrl_jnt01_1")
        self.changeLoc("neck_ik_jntEnd", "neck_crvCtrl_jnt02")
        cmds.select('neck_crvCtrl_jnt01', r=1)
        cmds.joint(zso=1, ch=1, e=1, oj='yxz', secondaryAxisOrient='xup')
        cmds.setAttr("neck_crvCtrl_jnt01_1.jointOrientX", 0)
        self.changeLoc("spine_ik_jnt01", "spine_crvCtrl_jnt01")
        self.changeLoc("spine_ik_jntEnd", "spine_crvCtrl_jnt02")


        ############################################/
        #fk 조인트들을 ik조인트 위치에 맞춘다.

        self.changeLoc("hip_ctrl", "pelvis_ctrl_preSet_grp")
        self.changeLoc("spine_ik_jnt01", "spine_fk_jnt01_grp")
        self.changeLoc("spine_ik_jnt03", "spine_fk_jnt02_grp")
        self.changeLoc("spine_ik_jnt05", "spine_fk_jnt03_grp")
        self.changeLoc("spine_ik_jntEnd", "spine_fk_jntEnd_grp")
        cmds.select('spine_fk_jnt01', r=1)
        cmds.joint(zso=1, ch=1, e=1, oj='yxz', secondaryAxisOrient='xup')
        tmpVal=-1 * cmds.getAttr('spine_fk_jntEnd_grp.rotateAxisX')
        cmds.setAttr("spine_fk_jntEnd.jointOrientX", tmpVal)


        #아래의 단락은 척추가 곡선인 fk컨트롤을 만들지 못한다. 위의 두줄이 답이 될 듯
        #$tmpVal=`getAttr spine_fk_jnt01.jointOrientX`;
        #setAttr "spine_fk_jnt01_grp.rotateAxisX" $tmpVal;
        #setAttr "spine_fk_jnt01.jointOrientX" 0;
        #setAttr "spine_fk_jnt02_grp.rotateAxisX" 0;
        #setAttr "spine_fk_ctrl01.jointOrientX" 0;
        #setAttr "spine_fk_jnt03_grp.rotateAxisX" 0;
        #setAttr "spine_fk_ctrl02.jointOrientX" 0;
        #setAttr "spine_fk_jntEnd_grp.rotateAxisX" 0;
        #setAttr "spine_fk_jntEnd.jointOrientX" 0;


        self.changeLoc("neck_ik_jnt01", "neck_jnt_grp")
        self.changeLoc("neck_ik_jnt04", "neck_fk_jnt02_grp")
        self.changeLoc("neck_ik_jntEnd", "neck_fk_jntEnd_grp")
        cmds.select('neck_ctrl', r=1)
        cmds.joint(zso=1, ch=1, e=1, oj='yxz', secondaryAxisOrient='xup')
        tmpVal=-1 * cmds.getAttr('neck_fk_jntEnd_grp.rotateAxisX')
        cmds.setAttr("neck_fk_jntEnd.jointOrientX", tmpVal)
        cmds.parentConstraint('neck_ctrl', 'neck_crvCtrl_jnt_grp', mo=1, weight=1, n='neck_crvCtrl_jnt_grp_parentConstraint')


        #아래의 단락은 목이 곡선인 fk컨트롤을 만들지 못한다. 위의 두줄이 답이 될 듯
        #$tmpVal=`getAttr neck_fk_ctrl01.jointOrientX`;
        #setAttr "neck_fk_jnt01_grp.rotateAxisX" $tmpVal;
        #setAttr "neck_fk_ctrl01.jointOrientX" 0;
        #setAttr "neck_fk_jnt02_grp.rotateAxisX" 0;
        #setAttr "neck_fk_ctrl02.jointOrientX" 0;
        #setAttr "neck_fk_jntEnd_grp.rotateAxisX" 0;
        #setAttr "neck_fk_jntEnd.jointOrientX" 0;

        cmds.select(cl=1)


        #################################
        #ik 컨트롤러의 조인트들과 커브를 스킨한다.

        cmds.select('spine_crvCtrl_jnt01', r=1)
        cmds.select('spine_crvCtrl_jnt02', add=1)
        cmds.select('spine_crv', add=1)
        cmds.select('spine_ik_ctrl02', add=1)
        cmds.select('spine_ik_ctrl01', add=1)
        cmds.skinCluster(mi=5, dr=4, n='spine_crv_skin')
        cmds.select('neck_crvCtrl_jnt01', r=1)
        cmds.select('neck_crvCtrl_jnt01_1', add=1)
        cmds.select('neck_crvCtrl_jnt02', add=1)
        cmds.select('neck_crv', add=1)
        cmds.skinCluster(mi=5, dr=4, n='neck_crv_skin')
        cmds.select(cl=1)

        #############################/
        #fk에 컨트롤을 만든다.
        cmds.select('spine_fk_ctrl01', 'spine_fk_ctrl02', r=1)
        self.ctrlCreat(cmds.ls(sl=1), 0, 1, 0, 2)
        cmds.select('neck_fk_ctrl01', 'neck_fk_ctrl02', r=1)
        self.ctrlCreat(cmds.ls(sl=1), 0, 1, 0, 0.7)
        cmds.setAttr("neck_ctrl.visibility", 1)
        cmds.setAttr("spine_fk_jnt01.visibility", 1)
        cmds.select(cl=1)


        ###############################/
        #부피변화를 없애기 위해 현재 커브길이를 ik조인트의 scaleYZ기준값으로 한다.

        cmds.setAttr("spine_crv_intScaleYZ.input2X", 
            cmds.getAttr('spine_crv_intScaleYZ.input1X'))
        cmds.setAttr("neck_crv_intScaleYZ.input2X", 
            cmds.getAttr('neck_crv_intScaleYZ.input1X'))


        #################################/
        #머리 컨트롤에 회전핀, 위치핀 만들기

        self.changeLoc_PV("neck_ik_jntEnd", "head_ctrl")
        self.changeLoc_PV("neck_ik_jntEnd", "head_ctrl_cnst_grp")
        self.changeLoc_PV("neck_ik_jntEnd", "head_ctrl_preSet_grp")
        cmds.group(em=1, n='head_worldRot_grp')
        cmds.select('head_worldRot_grp', r=1)
        cmds.select('total_ctrl', add=1)
        cmds.parent()
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.group(em=1, n='head_worldPos_grp')
        cmds.select('head_worldPos_grp', r=1)
        cmds.select('total_ctrl', add=1)
        cmds.parent()
        self.changeLoc("head_ctrl", "head_worldPos_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        #neck 끝에 loc을 만들어 붙인다. neckEnd_loc
        cmds.spaceLocator(p=(0, 0, 0), n="neckEnd_loc")
        cmds.setAttr("neckEnd_loc.localScaleX", .5)
        cmds.setAttr("neckEnd_loc.localScaleY", .5)
        cmds.setAttr("neckEnd_loc.localScaleZ", .5)
        self.changeLoc("neck_fk_jntEnd", "neckEnd_loc")
        cmds.parent('neckEnd_loc', 'chest_ctrl')
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.select('neck_fk_jntEnd', r=1)
        cmds.select('neckEnd_loc', tgl=1)
        cmds.parentConstraint(mo=1, weight=1, n='neckEnd_loc_prntCnst')


        #head_ctrl_cnst_grp의 cnst대상을 neck_world와 neckEnd_loc으로 한다.
        cmds.select('head_worldPos_grp', r=1)
        cmds.select('neckEnd_loc', tgl=1)
        cmds.select('head_ctrl_cnst_grp', add=1)
        cmds.pointConstraint(mo=1, weight=1, n='head_ctrl_cnst_grp_pntCnst')
        cmds.select('head_worldRot_grp', r=1)
        cmds.select('neckEnd_loc', tgl=1)
        cmds.select('head_ctrl_cnst_grp', add=1)
        cmds.orientConstraint(mo=1, weight=1, n='head_ctrl_cnst_grp_orntCnst')
        cmds.setAttr("head_ctrl_cnst_grp_orntCnst.offsetX", 0)


        #head_ctrl의 pin속성들과 연결한다.
        cmds.createNode('reverse', n='head_rvrs')
        cmds.connectAttr('head_ctrl.rotationPin', 'head_ctrl_cnst_grp_orntCnst.head_worldRot_grpW0', f=1)
        cmds.connectAttr('head_ctrl.rotationPin', 'head_rvrs.inputX', f=1)
        cmds.connectAttr('head_rvrs.outputX', 'head_ctrl_cnst_grp_orntCnst.neckEnd_locW1', f=1)
        cmds.connectAttr('head_ctrl.positionPin', 'head_ctrl_cnst_grp_pntCnst.head_worldPos_grpW0', f=1)
        cmds.connectAttr('head_ctrl.positionPin', 'head_rvrs.inputY', f=1)
        cmds.connectAttr('head_rvrs.outputY', 'head_ctrl_cnst_grp_pntCnst.neckEnd_locW1', f=1)
        cmds.setAttr("neckEnd_loc.visibility", 0)
        cmds.setAttr("neckEnd_loc.v", lock=True)
        cmds.setAttr('head_ctrl.rotationPin', 0)
        cmds.select(cl=1)


        ####################################/
        #가슴 컨트롤과 히프 컨트롤러의 parentConst

        cmds.select('spine_fk_jntEnd', r=1)
        cmds.select('chest_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='chest_ctrl_cnst_grp_prntCnst')
        cmds.select('pelvis_ctrl', r=1)
        cmds.select('hip_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='hip_ctrl_cnst_grp_prntCnst')


        ############################/
        #척추 컨트롤01의 회전핀 설치

        cmds.group(em=1, n='spine_worldRot_grp')
        cmds.select('spine_worldRot_grp', r=1)
        cmds.select('total_ctrl', add=1)
        cmds.parent()
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.select('spine_worldRot_grp', r=1)
        cmds.select('pelvis_ctrl', tgl=1)
        cmds.select('spine_fk_jnt02_grp', add=1)
        cmds.orientConstraint(mo=1, weight=1, n='spine_fk_jnt02_grp_orntCnst')
        cmds.connectAttr('spine_fk_ctrl01.rotationPin', 'spine_fk_jnt02_grp_orntCnst.spine_worldRot_grpW0', f=1)
        cmds.createNode('reverse', n='spine_rvrs')
        cmds.connectAttr('spine_fk_ctrl01.rotationPin', 'spine_rvrs.inputX', f=1)
        cmds.connectAttr('spine_rvrs.outputX', 'spine_fk_jnt02_grp_orntCnst.pelvis_ctrlW1', f=1)
        cmds.setAttr("spine_fk_ctrl01.rotationPin", 0)


        ###############################/
        #어깨와 히프를 바디와 연결

        cmds.select('chest_ctrl', r=1)
        cmds.select('shldr_L_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='shldr_L_cnst_grp_prntCnst')
        cmds.select('chest_ctrl', r=1)
        cmds.select('shldr_R_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='shldr_R_cnst_grp_prntCnst')
        cmds.select('hip_ctrl', r=1)
        cmds.select('hip_L_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='hip_L_cnst_grp_prntCnst')
        cmds.select('hip_ctrl', r=1)
        cmds.select('hip_R_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='hip_R_cnst_grp_prntCnst')
        cmds.select(cl=1)


        ###################################/
        #굳히기
        #어깨 위치에 관한 preSet연결끊고, 해당 속성 잠그기, 필요없는 노드 지우기

        cmds.disconnectAttr('total_preSet_grp.shldr_width', 'shldr_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.shldr_height', 'shldr_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.shldr_frontBack', 'shldr_L_preSet_grp.tz')
        cmds.disconnectAttr('shldr_R_tmp_negativMult.outputX', 'shldr_R_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.shldr_height', 'shldr_R_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.shldr_frontBack', 'shldr_R_preSet_grp.tz')
        cmds.setAttr("shldr_L_preSet_grp.tx", lock=True)
        cmds.setAttr("shldr_L_preSet_grp.ty", lock=True)
        cmds.setAttr("shldr_L_preSet_grp.tz", lock=True)
        cmds.setAttr("shldr_R_preSet_grp.tx", lock=True)
        cmds.setAttr("shldr_R_preSet_grp.ty", lock=True)
        cmds.setAttr("shldr_R_preSet_grp.tz", lock=True)
        cmds.delete('shldr_R_tmp_negativMult')


        #어깨의 각도에 관한 preSet연결 끊고, 해당속성 잠그기
        cmds.disconnectAttr('total_preSet_grp.shldr_length', 'shldr_L_ctrl_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.shldr_angle01', 'shldr_L_ctrl_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.shldr_angle02', 'shldr_L_ctrl_preSet_grp.tz')
        cmds.disconnectAttr('shldr_R_preSet_mult.output', 'shldr_R_ctrl_preSet_grp.translate')
        cmds.delete('arm_L_jnt_preSet_multiply')
        cmds.delete('arm_R_jnt_preSet_multiply')
        cmds.delete('shldr_R_preSet_mult')
        cmds.setAttr("shldr_L_ctrl_preSet_grp.tx", lock=True)
        cmds.setAttr("shldr_L_ctrl_preSet_grp.ty", lock=True)
        cmds.setAttr("shldr_L_ctrl_preSet_grp.tz", lock=True)
        cmds.setAttr("shldr_R_ctrl_preSet_grp.tx", lock=True)
        cmds.setAttr("shldr_R_ctrl_preSet_grp.ty", lock=True)
        cmds.setAttr("shldr_R_ctrl_preSet_grp.tz", lock=True)
        cmds.setAttr("arm_L_jnt_preSet_grp.rx", lock=True)
        cmds.setAttr("arm_L_jnt_preSet_grp.ry", lock=True)
        cmds.setAttr("arm_L_jnt_preSet_grp.rz", lock=True)
        cmds.setAttr("hand_L_ik_ctrl_preSet_grp.rx", lock=True)
        cmds.setAttr("hand_L_ik_ctrl_preSet_grp.ry", lock=True)
        cmds.setAttr("hand_L_ik_ctrl_preSet_grp.rz", lock=True)
        cmds.setAttr("arm_R_jnt_preSet_grp.rx", lock=True)
        cmds.setAttr("arm_R_jnt_preSet_grp.ry", lock=True)
        cmds.setAttr("arm_R_jnt_preSet_grp.rz", lock=True)
        cmds.setAttr("hand_R_ik_ctrl_preSet_grp.rx", lock=True)
        cmds.setAttr("hand_R_ik_ctrl_preSet_grp.ry", lock=True)
        cmds.setAttr("hand_R_ik_ctrl_preSet_grp.rz", lock=True)

        #힙의 위치에 관한 preSet연결 끊고, 필요없는 노드 지우기.
        cmds.disconnectAttr('total_preSet_grp.hip_width', 'hip_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.hip_height', 'hip_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.hip_frontBack', 'hip_L_preSet_grp.tz')
        cmds.disconnectAttr('hip_R_tmp_negativMult.outputX', 'hip_R_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.hip_height', 'hip_R_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.hip_frontBack', 'hip_R_preSet_grp.tz')
        cmds.setAttr("hip_L_preSet_grp.tx", lock=True)
        cmds.setAttr("hip_L_preSet_grp.ty", lock=True)
        cmds.setAttr("hip_L_preSet_grp.tz", lock=True)
        cmds.setAttr("hip_R_preSet_grp.tx", lock=True)
        cmds.setAttr("hip_R_preSet_grp.ty", lock=True)
        cmds.setAttr("hip_R_preSet_grp.tz", lock=True)
        cmds.delete('hip_R_tmp_negativMult')


        #힙의 각도에 관한 preSet연결 끊고, 해당속성 잠그기.
        cmds.disconnectAttr('total_preSet_grp.hip_upDown', 'hip_L_ctrl_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.hip_angle01', 'hip_L_ctrl_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.hip_angle02', 'hip_L_ctrl_preSet_grp.tz')
        cmds.disconnectAttr('total_preSet_grp.hip_upDown', 'hip_R_ctrl_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.hip_angle01', 'hip_R_ctrl_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.hip_angle02', 'hip_R_ctrl_preSet_grp.tz')
        cmds.setAttr("hip_L_ctrl_preSet_grp.tx", lock=True)
        cmds.setAttr("hip_L_ctrl_preSet_grp.ty", lock=True)
        cmds.setAttr("hip_L_ctrl_preSet_grp.tz", lock=True)
        cmds.setAttr("hip_R_ctrl_preSet_grp.tx", lock=True)
        cmds.setAttr("hip_R_ctrl_preSet_grp.ty", lock=True)
        cmds.setAttr("hip_R_ctrl_preSet_grp.tz", lock=True)





    ##########################################
    #fk,ik 팔 맞추기

    def setArm(self):


        #늘어날 만큼 직접 키 데이터를 고치고,뷰에서 팔이 얼마나 늘어날지 보려고 만든 tmp_plus노드를 지운다. 

        #변수선언
        val_lowArm=cmds.getAttr('total_preSet_grp.upArm')
        val_hand=cmds.getAttr('total_preSet_grp.lowArm')


        #원래 길이에 위의 값으로 2배, 100배값을 구한다.
        val_L_lowArm_01=2.6 + val_lowArm

        #$val_L_lowArm_02  = $val_L_lowArm_01*2;
        val_L_lowArm_03=val_L_lowArm_01 * 100


        val_L_hand_01=2.6 + val_hand

        #$val_L_hand_02    = $val_L_hand_01*2;
        val_L_hand_03=val_L_hand_01 * 100


        val_R_lowArm_01=-2.6 - val_lowArm
        #$val_R_lowArm_02  = $val_R_lowArm_01*2;
        val_R_lowArm_03=val_R_lowArm_01 * 100

        val_R_hand_01=-2.6 - val_hand
        #$val_R_hand_02    = $val_R_hand_01*2;
        val_R_hand_03=val_R_hand_01 * 100

        #fk_arm_jnt에 연결된 key값을 바꾼다.
        cmds.keyframe('lowArm_L_fk_ctrl_translateX', valueChange=val_L_lowArm_01, index=(1,1), absolute=1)
        cmds.keyframe('lowArm_L_fk_ctrl_translateX', valueChange=val_L_lowArm_03, index=(2,2), absolute=1)
        cmds.keyframe('hand_L_fk_ctrl_translateX', valueChange=val_L_hand_01, index=(1,1), absolute=1)
        cmds.keyframe('hand_L_fk_ctrl_translateX', valueChange=val_L_hand_03, index=(2,2), absolute=1)
        cmds.keyframe('lowArm_R_fk_ctrl_translateX', valueChange=val_R_lowArm_01, index=(1,1), absolute=1)
        cmds.keyframe('lowArm_R_fk_ctrl_translateX', valueChange=val_R_lowArm_03, index=(2,2), absolute=1)
        cmds.keyframe('hand_R_fk_ctrl_translateX', valueChange=val_R_hand_01, index=(1,1), absolute=1)
        cmds.keyframe('hand_R_fk_ctrl_translateX', valueChange=val_R_hand_03, index=(2,2), absolute=1)


        #수정된 키 데이터를 조인트에 연결한다.
        cmds.connectAttr('lowArm_L_fk_ctrl_translateX.output', 'lowArm_L_fk_ctrl.translateX', f=1)
        cmds.connectAttr('hand_L_fk_ctrl_translateX.output', 'hand_L_fk_ctrl.translateX', f=1)
        cmds.connectAttr('lowArm_R_fk_ctrl_translateX.output', 'lowArm_R_fk_ctrl.translateX', f=1)
        cmds.connectAttr('hand_R_fk_ctrl_translateX.output', 'hand_R_fk_ctrl.translateX', f=1)
        cmds.setAttr("lowArm_L_fk_ctrl.t", 
            l=True)
        cmds.setAttr("hand_L_fk_ctrl.t", 
            l=True)
        cmds.setAttr("lowArm_R_fk_ctrl.t", 
            l=True)
        cmds.setAttr("hand_R_fk_ctrl.t", 
            l=True)

        #필요없어진 tmp_plus노드를 지운다.
        cmds.delete('lowArm_L_fk_preSet_tmp_plus', 'lowArm_R_fk_preSet_tmp_plus', 'hand_L_fk_preSet_tmp_plus', 'hand_R_fk_preSet_tmp_plus')


        #ik_arm_jnt에 연결된 key 값을 바꾼다.
        cmds.keyframe('lowArm_L_ik_jnt_translateX', valueChange=val_L_lowArm_01, index=(0,0), absolute=1)
        cmds.keyframe('lowArm_L_ik_jnt_translateX', valueChange=val_L_lowArm_01, index=(1,1), absolute=1)
        #keyframe -index 2 -absolute -valueChange $val_L_lowArm_02 lowArm_L_ik_jnt_translateX ;
        cmds.keyframe('lowArm_L_ik_jnt_translateX', valueChange=val_L_lowArm_03, index=(2,2), absolute=1)
        cmds.keyframe('hand_L_ik_jnt_translateX', valueChange=val_L_hand_01, index=(0,0), absolute=1)
        cmds.keyframe('hand_L_ik_jnt_translateX', valueChange=val_L_hand_01, index=(1,1), absolute=1)

        #keyframe -index 2 -absolute -valueChange $val_L_hand_02 hand_L_ik_jnt_translateX ;
        cmds.keyframe('hand_L_ik_jnt_translateX', valueChange=val_L_hand_03, index=(2,2), absolute=1)
        cmds.keyframe('lowArm_R_ik_jnt_translateX', valueChange=val_R_lowArm_01, index=(2,2), absolute=1)
        cmds.keyframe('lowArm_R_ik_jnt_translateX', valueChange=val_R_lowArm_01, index=(1,1), absolute=1)
        #keyframe -index 1 -absolute -valueChange $val_R_lowArm_02 lowArm_R_ik_jnt_translateX ;
        cmds.keyframe('lowArm_R_ik_jnt_translateX', valueChange=val_R_lowArm_03, index=(0,0), absolute=1)
        cmds.keyframe('hand_R_ik_jnt_translateX', valueChange=val_R_hand_01, index=(2,2), absolute=1)
        cmds.keyframe('hand_R_ik_jnt_translateX', valueChange=val_R_hand_01, index=(1,1), absolute=1)

        #keyframe -index 1 -absolute -valueChange $val_R_hand_02 hand_R_ik_jnt_translateX ;
        cmds.keyframe('hand_R_ik_jnt_translateX', valueChange=val_R_hand_03, index=(0,0), absolute=1)


        #ik_ctrl들의 위치를 해당 fk 조인트로 옮긴다.
        self.changeLoc("hand_L_fk_ctrl", "hand_L_ik_ctrl_preSet_grp")
        self.changeLoc("hand_R_fk_ctrl", "hand_R_ik_ctrl_preSet_grp")
        self.changeLoc("lowArm_L_fk_ctrl", "elbow_L_ctrl_preSet_grp")
        self.changeLoc("lowArm_R_fk_ctrl", "elbow_R_ctrl_preSet_grp")



        #팔의 총 길이를 알아내서,
        arm_L_dist01=cmds.getAttr('arm_L_distShape.distance')
        arm_R_dist01=cmds.getAttr('arm_L_distShape.distance')


        #길이값의 2배,100배값을 구한다.
        #$arm_L_dist02 = $arm_L_dist01 * 2;
        arm_L_dist03=arm_L_dist01 * 100


        #$arm_R_dist02 = $arm_R_dist01 * 2;
        arm_R_dist03=arm_R_dist01 * 100


        #ik늘어남에 관계된 key 데이터를 구한값으로 수정한다.
        cmds.keyframe('lowArm_L_ik_jnt_translateX', floatChange=arm_L_dist01, index=(1,1), option='over', absolute=1)

        #keyframe -option over -index 2 -absolute -floatChange $arm_L_dist02 lowArm_L_ik_jnt_translateX ;
        cmds.keyframe('lowArm_L_ik_jnt_translateX', floatChange=arm_L_dist03, index=(2,2), option='over', absolute=1)

        cmds.keyframe('hand_L_ik_jnt_translateX', floatChange=arm_L_dist01, index=(1,1), option='over', absolute=1)
        # ERR:
        #keyframe -option over -index 2 -absolute -floatChange $arm_L_dist02  hand_L_ik_jnt_translateX ;
        cmds.keyframe('hand_L_ik_jnt_translateX', floatChange=arm_L_dist03, index=(2,2), option='over', absolute=1)
        cmds.keyframe('lowArm_R_ik_jnt_translateX', floatChange=arm_R_dist01, index=(1,1), option='over', absolute=1)

        #keyframe -option over -index 1 -absolute -floatChange $arm_R_dist02 lowArm_R_ik_jnt_translateX ;
        cmds.keyframe('lowArm_R_ik_jnt_translateX', floatChange=arm_R_dist03, index=(0,0), option='over', absolute=1)
        cmds.keyframe('hand_R_ik_jnt_translateX', floatChange=arm_R_dist01, index=(1,1), option='over', absolute=1)

        #keyframe -option over -index 1 -absolute -floatChange $arm_R_dist02 hand_R_ik_jnt_translateX ;
        cmds.keyframe('hand_R_ik_jnt_translateX', floatChange=arm_R_dist03, index=(0,0), option='over', absolute=1)


        #fk_jnt의 늘어남을 수정한 변수로, elbowHand_fk_jnt의 늘어남 키 데이터를 수정한다.
        cmds.keyframe('elbowHand_L_fk_ctrl_translateX', valueChange=val_L_hand_01, index=(1,1), absolute=1)
        cmds.keyframe('elbowHand_R_fk_ctrl_translateX', valueChange=val_R_hand_01, index=(1,1), absolute=1)



    ###################################
    #fk,ik 발 맞추기

    def setLeg(self):

        ####################################/
        #다리의fk가 늘어난 만큼, 다리의 ik 키값을 고친다.

        #변수선언
        val_lowLeg=cmds.getAttr('total_preSet_grp.upLeg')
        val_foot=cmds.getAttr('total_preSet_grp.lowLeg')


        #원래 길이에 위의 값으로 2배, 10배값을 구한다.
        val_L_lowLeg_01=2.6 + val_lowLeg

        #$val_L_lowLeg_02  = $val_L_lowLeg_01*2;
        val_L_lowLeg_03=val_L_lowLeg_01 * 100


        val_L_foot_01=2.6 + val_foot

        #$val_L_foot_02    = $val_L_foot_01*2;
        val_L_foot_03=val_L_foot_01 * 100


        val_R_lowLeg_01=-2.6 - val_lowLeg
        #$val_R_lowLeg_02  = $val_R_lowLeg_01*2;
        val_R_lowLeg_03=val_R_lowLeg_01 * 100
        val_R_foot_01=-2.6 - val_foot

        #$val_R_foot_02    = $val_R_foot_01*2;
        val_R_foot_03=val_R_foot_01 * 100

        #fk_leg_jnt에 연결된 key값을 바꾼다.
        cmds.keyframe('lowLeg_L_fk_ctrl_translateX', valueChange=val_L_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_L_fk_ctrl_translateX', valueChange=val_L_lowLeg_03, index=(2,2), absolute=1)
        cmds.keyframe('foot_L_fk_ctrl_translateX', valueChange=val_L_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_L_fk_ctrl_translateX', valueChange=val_L_foot_03, index=(2,2), absolute=1)
        cmds.keyframe('lowLeg_R_fk_ctrl_translateX', valueChange=val_R_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_R_fk_ctrl_translateX', valueChange=val_R_lowLeg_03, index=(2,2), absolute=1)
        cmds.keyframe('foot_R_fk_ctrl_translateX', valueChange=val_R_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_R_fk_ctrl_translateX', valueChange=val_R_foot_03, index=(2,2), absolute=1)


        ##수정된 키 데이터를 조인트에 연결한다.
        cmds.connectAttr('lowLeg_L_fk_ctrl_translateX.output', 'lowLeg_L_fk_ctrl.translateX', f=1)
        cmds.connectAttr('foot_L_fk_ctrl_translateX.output', 'foot_L_fk_ctrl.translateX', f=1)
        cmds.connectAttr('lowLeg_R_fk_ctrl_translateX.output', 'lowLeg_R_fk_ctrl.translateX', f=1)
        cmds.connectAttr('foot_R_fk_ctrl_translateX.output', 'foot_R_fk_ctrl.translateX', f=1)
        cmds.setAttr("lowLeg_L_fk_ctrl.t", 
            l=True)
        cmds.setAttr("foot_L_fk_ctrl.t", 
            l=True)
        cmds.setAttr("lowLeg_R_fk_ctrl.t", 
            l=True)
        cmds.setAttr("foot_R_fk_ctrl.t", 
            l=True)


        #필요없어진 tmp_plus노드를 지운다.
        cmds.delete('lowLeg_L_fk_preSet_tmp_plus', 'lowLeg_R_fk_preSet_tmp_plus', 'foot_L_fk_preSet_tmp_plus', 'foot_R_fk_preSet_tmp_plus')


        #ik_leg_jnt에 연결된 key 값을 바꾼다.(noFlip,pv)
        cmds.keyframe('lowLeg_L_noFlip_pv_jnt_translateX', valueChange=val_L_lowLeg_01, index=(0,0), absolute=1)
        cmds.keyframe('lowLeg_L_noFlip_pv_jnt_translateX', valueChange=val_L_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_L_noFlip_pv_jnt_translateX', valueChange=val_L_lowLeg_03, index=(2,2), absolute=1)
        cmds.keyframe('lowLeg_L_ik_pv_jnt_translateX', valueChange=val_L_lowLeg_01, index=(0,0), absolute=1)
        cmds.keyframe('lowLeg_L_ik_pv_jnt_translateX', valueChange=val_L_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_L_ik_pv_jnt_translateX', valueChange=val_L_lowLeg_03, index=(2,2), absolute=1)
        cmds.keyframe('foot_L_ik_noFlip_jnt_translateX', valueChange=val_L_foot_01, index=(0,0), absolute=1)
        cmds.keyframe('foot_L_ik_noFlip_jnt_translateX', valueChange=val_L_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_L_ik_noFlip_jnt_translateX', valueChange=val_L_foot_03, index=(2,2), absolute=1)
        cmds.keyframe('foot_L_ik_pv_jnt_translateX', valueChange=val_L_foot_01, index=(0,0), absolute=1)
        cmds.keyframe('foot_L_ik_pv_jnt_translateX', valueChange=val_L_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_L_ik_pv_jnt_translateX', valueChange=val_L_foot_03, index=(2,2), absolute=1)
        cmds.keyframe('lowLeg_R_noFlip_pv_jnt_translateX', valueChange=val_R_lowLeg_01, index=(2,2), absolute=1)
        cmds.keyframe('lowLeg_R_noFlip_pv_jnt_translateX', valueChange=val_R_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_R_noFlip_pv_jnt_translateX', valueChange=val_R_lowLeg_03, index=(0,0), absolute=1)
        cmds.keyframe('lowLeg_R_ik_pv_jnt_translateX', valueChange=val_R_lowLeg_01, index=(2,2), absolute=1)
        cmds.keyframe('lowLeg_R_ik_pv_jnt_translateX', valueChange=val_R_lowLeg_01, index=(1,1), absolute=1)
        cmds.keyframe('lowLeg_R_ik_pv_jnt_translateX', valueChange=val_R_lowLeg_03, index=(0,0), absolute=1)
        cmds.keyframe('foot_R_ik_noFlip_jnt_translateX', valueChange=val_R_foot_01, index=(2,2), absolute=1)
        cmds.keyframe('foot_R_ik_noFlip_jnt_translateX', valueChange=val_R_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_R_ik_noFlip_jnt_translateX', valueChange=val_R_foot_03, index=(0,0), absolute=1)
        cmds.keyframe('foot_R_ik_pv_jnt_translateX', valueChange=val_R_foot_01, index=(2,2), absolute=1)
        cmds.keyframe('foot_R_ik_pv_jnt_translateX', valueChange=val_R_foot_01, index=(1,1), absolute=1)
        cmds.keyframe('foot_R_ik_pv_jnt_translateX', valueChange=val_R_foot_03, index=(0,0), absolute=1)

        #ik_ctrl들의 위치를 해당 fk 조인트로 옮긴다.
        self.changeLoc("foot_L_fk_ctrl", "leg_L_distEnd_preSet_grp")
        self.changeLoc("foot_R_fk_ctrl", "leg_R_distEnd_preSet_grp")
        self.changeLoc("lowLeg_L_fk_ctrl", "knee_L_ctrl_preSet_grp")
        self.changeLoc("lowLeg_R_fk_ctrl", "knee_R_ctrl_preSet_grp")



        #다리의 총 길이를 알아내서,
        leg_L_dist01=cmds.getAttr('leg_L_pv_dist_totalCtrl_scale.input1X')
        leg_R_dist01=cmds.getAttr('leg_R_pv_dist_totalCtrl_scale.input1X')

        #길이값의 2배,100배값을 구한다.
        #$leg_L_dist02 = $leg_L_dist01 * 2;
        leg_L_dist03=leg_L_dist01 * 100

        #$leg_R_dist02 = $leg_R_dist01 * 2;
        leg_R_dist03=leg_R_dist01 * 100

        #ik늘어남에 관계된 key 데이터를 구한값으로 수정한다.
        #PV ik
        cmds.keyframe('lowLeg_L_ik_pv_jnt_translateX', floatChange=leg_L_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('lowLeg_L_ik_pv_jnt_translateX', floatChange=leg_L_dist03, index=(2,2), option='over', absolute=1)
        cmds.keyframe('foot_L_ik_pv_jnt_translateX', floatChange=leg_L_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('foot_L_ik_pv_jnt_translateX', floatChange=leg_L_dist03, index=(2,2), option='over', absolute=1)
        cmds.keyframe('lowLeg_R_ik_pv_jnt_translateX', floatChange=leg_R_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('lowLeg_R_ik_pv_jnt_translateX', floatChange=leg_R_dist03, index=(0,0), option='over', absolute=1)
        cmds.keyframe('foot_R_ik_pv_jnt_translateX', floatChange=leg_R_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('foot_R_ik_pv_jnt_translateX', floatChange=leg_R_dist03, index=(0,0), option='over', absolute=1)


        #noFlip ik
        cmds.keyframe('lowLeg_L_noFlip_pv_jnt_translateX', floatChange=leg_L_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('lowLeg_L_noFlip_pv_jnt_translateX', floatChange=leg_L_dist03, index=(2,2), option='over', absolute=1)
        cmds.keyframe('foot_L_ik_noFlip_jnt_translateX', floatChange=leg_L_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('foot_L_ik_noFlip_jnt_translateX', floatChange=leg_L_dist03, index=(2,2), option='over', absolute=1)
        cmds.keyframe('lowLeg_R_noFlip_pv_jnt_translateX', floatChange=leg_R_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('lowLeg_R_noFlip_pv_jnt_translateX', floatChange=leg_R_dist03, index=(0,0), option='over', absolute=1)
        cmds.keyframe('foot_R_ik_noFlip_jnt_translateX', floatChange=leg_R_dist01, index=(1,1), option='over', absolute=1)
        cmds.keyframe('foot_R_ik_noFlip_jnt_translateX', floatChange=leg_R_dist03, index=(0,0), option='over', absolute=1)




    ############################/
    #손의 세팅

    def setHand(self):

        #ik_jnt길이를 fk_jnt에 맞춘다.

        self.changeLoc("thumb_L_fk_jntEnd", "thumb_L_ik_jntEnd")
        self.changeLoc("index_L_fk_jntEnd", "index_L_ik_jntEnd")
        self.changeLoc("middle_L_fk_jntEnd", "middle_L_ik_jntEnd")
        self.changeLoc("ring_L_fk_jntEnd", "ring_L_ik_jntEnd")
        self.changeLoc("pinky_L_fk_jntEnd", "pinky_L_ik_jntEnd")
        self.changeLoc("thumb_R_fk_jntEnd", "thumb_R_ik_jntEnd")
        self.changeLoc("index_R_fk_jntEnd", "index_R_ik_jntEnd")
        self.changeLoc("middle_R_fk_jntEnd", "middle_R_ik_jntEnd")
        self.changeLoc("ring_R_fk_jntEnd", "ring_R_ik_jntEnd")
        self.changeLoc("pinky_R_fk_jntEnd", "pinky_R_ik_jntEnd")


        #in,bend,out_loc의 위치 수정

        self.changeLoc("index_L_ik_jnt01", "fing_L_inSide_loc")
        self.changeLoc("middle_L_ik_jnt01", "fing_L_bend_loc")
        self.changeLoc("pinky_L_ik_jnt01", "fing_L_outSide_loc")
        self.changeLoc("index_R_ik_jnt01", "fing_R_inSide_loc")
        self.changeLoc("middle_R_ik_jnt01", "fing_R_bend_loc")
        self.changeLoc("pinky_R_ik_jnt01", "fing_R_outSide_loc")



        #loc의 parent

        cmds.parent('fing_L_bend_loc', 'fing_L_inSide_loc')
        cmds.parent('fing_L_inSide_loc', 'fing_L_outSide_loc')
        cmds.parent('fing_R_bend_loc', 'fing_R_inSide_loc')
        cmds.parent('fing_R_inSide_loc', 'fing_R_outSide_loc')


        #ik손가락에 ikSC를 건다.
        self.ikSC("thumb_L_ik_jnt01", "thumb_L_ik_jntEnd", "thumb_L_ikHdl", "thumb_L_ik_efftr")
        self.ikSC("index_L_ik_jnt01", "index_L_ik_jntEnd", "index_L_ikHdl", "index_L_ik_efftr")
        self.ikSC("middle_L_ik_jnt01", "middle_L_ik_jntEnd", "middle_L_ikHdl", "middle_L_ik_efftr")
        self.ikSC("ring_L_ik_jnt01", "ring_L_ik_jntEnd", "ring_L_ikHdl", "ring_L_ik_efftr")
        self.ikSC("pinky_L_ik_jnt01", "pinky_L_ik_jntEnd", "pinky_L_ikHdl", "pinky_L_ik_efftr")
        self.ikSC("thumb_R_ik_jnt01", "thumb_R_ik_jntEnd", "thumb_R_ikHdl", "thumb_R_ik_efftr")
        self.ikSC("index_R_ik_jnt01", "index_R_ik_jntEnd", "index_R_ikHdl", "index_R_ik_efftr")
        self.ikSC("middle_R_ik_jnt01", "middle_R_ik_jntEnd", "middle_R_ikHdl", "middle_R_ik_efftr")
        self.ikSC("ring_R_ik_jnt01", "ring_R_ik_jntEnd", "ring_R_ikHdl", "ring_R_ik_efftr")
        self.ikSC("pinky_R_ik_jnt01", "pinky_R_ik_jntEnd", "pinky_R_ikHdl", "pinky_R_ik_efftr")

        #ikHdl을 ikHdl_grp에 넣는다.

        cmds.select('thumb_L_ikHdl', 'index_L_ikHdl', 'middle_L_ikHdl', 'ring_L_ikHdl', 'pinky_L_ikHdl', r=1)
        cmds.select('fing_L_ikHdl_grp', add=1)
        cmds.parent()
        cmds.select('thumb_R_ikHdl', 'index_R_ikHdl', 'middle_R_ikHdl', 'ring_R_ikHdl', 'pinky_R_ikHdl', r=1)
        cmds.select('fing_R_ikHdl_grp', add=1)
        cmds.parent()


        #bend_loc과 parentCnst

        cmds.select('fing_L_bend_loc', r=1)
        cmds.select('handBase_L_jnt', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='handBase_L_jnt_prntCnst')
        cmds.select('fing_R_bend_loc', r=1)
        cmds.select('handBase_R_jnt', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='handBase_R_jnt_prntCnst')


        ##############################
        #굳히기
        #손가락의 위치에 관한 preSet연결 끊고, 속성 잠근 후, tmpNode들을 지우기

        cmds.disconnectAttr('total_preSet_grp.thumb_tx', 'thumb_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.thumb_ty', 'thumb_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.thumb_tz', 'thumb_L_preSet_grp.tz')
        cmds.disconnectAttr('total_preSet_grp.index_tx', 'index_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.index_ty', 'index_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.index_tz', 'index_L_preSet_grp.tz')
        cmds.disconnectAttr('total_preSet_grp.middle_tx', 'middle_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.middle_ty', 'middle_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.middle_tz', 'middle_L_preSet_grp.tz')
        cmds.disconnectAttr('total_preSet_grp.ring_tx', 'ring_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.ring_ty', 'ring_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.ring_tz', 'ring_L_preSet_grp.tz')
        cmds.disconnectAttr('total_preSet_grp.pinky_tx', 'pinky_L_preSet_grp.tx')
        cmds.disconnectAttr('total_preSet_grp.pinky_ty', 'pinky_L_preSet_grp.ty')
        cmds.disconnectAttr('total_preSet_grp.pinky_tz', 'pinky_L_preSet_grp.tz')
        cmds.disconnectAttr('thumb_tmp_negativMult.output', 'thumb_R_preSet_grp.translate')
        cmds.disconnectAttr('index_tmp_negativMult.output', 'index_R_preSet_grp.translate')
        cmds.disconnectAttr('middle_tmp_negativMult.output', 'middle_R_preSet_grp.translate')
        cmds.disconnectAttr('ring_tmp_negativMult.output', 'ring_R_preSet_grp.translate')
        cmds.disconnectAttr('pinky_tmp_negativMult.output', 'pinky_R_preSet_grp.translate')
        cmds.setAttr("thumb_L_preSet_grp.tx", lock=True)
        cmds.setAttr("thumb_L_preSet_grp.ty", lock=True)
        cmds.setAttr("thumb_L_preSet_grp.tz", lock=True)
        cmds.setAttr("index_L_preSet_grp.tx", lock=True)
        cmds.setAttr("index_L_preSet_grp.ty", lock=True)
        cmds.setAttr("index_L_preSet_grp.tz", lock=True)
        cmds.setAttr("middle_L_preSet_grp.tx", lock=True)
        cmds.setAttr("middle_L_preSet_grp.ty", lock=True)
        cmds.setAttr("middle_L_preSet_grp.tz", lock=True)
        cmds.setAttr("ring_L_preSet_grp.tx", lock=True)
        cmds.setAttr("ring_L_preSet_grp.ty", lock=True)
        cmds.setAttr("ring_L_preSet_grp.tz", lock=True)
        cmds.setAttr("pinky_L_preSet_grp.tx", lock=True)
        cmds.setAttr("pinky_L_preSet_grp.ty", lock=True)
        cmds.setAttr("pinky_L_preSet_grp.tz", lock=True)
        cmds.setAttr("thumb_R_preSet_grp.tx", lock=True)
        cmds.setAttr("thumb_R_preSet_grp.ty", lock=True)
        cmds.setAttr("thumb_R_preSet_grp.tz", lock=True)
        cmds.setAttr("index_R_preSet_grp.tx", lock=True)
        cmds.setAttr("index_R_preSet_grp.ty", lock=True)
        cmds.setAttr("index_R_preSet_grp.tz", lock=True)
        cmds.setAttr("middle_R_preSet_grp.tx", lock=True)
        cmds.setAttr("middle_R_preSet_grp.ty", lock=True)
        cmds.setAttr("middle_R_preSet_grp.tz", lock=True)
        cmds.setAttr("ring_R_preSet_grp.tx", lock=True)
        cmds.setAttr("ring_R_preSet_grp.ty", lock=True)
        cmds.setAttr("ring_R_preSet_grp.tz", lock=True)
        cmds.setAttr("pinky_R_preSet_grp.tx", lock=True)
        cmds.setAttr("pinky_R_preSet_grp.ty", lock=True)
        cmds.setAttr("pinky_R_preSet_grp.tz", lock=True)
        cmds.delete('thumb_tmp_negativMult', 'index_tmp_negativMult', 'middle_tmp_negativMult', 'ring_tmp_negativMult', 'pinky_tmp_negativMult')
            

        #손가락의 회전에 관한 preSet연결 끊고, 속성 잠그기

        cmds.disconnectAttr('total_preSet_grp.thumb_rx', 'thumbBase_L_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.thumb_ry', 'thumbBase_L_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.thumb_rz', 'thumbBase_L_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.thumb_rx', 'thumbBase_R_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.thumb_ry', 'thumbBase_R_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.thumb_rz', 'thumbBase_R_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.index_rx', 'indexBase_L_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.index_ry', 'indexBase_L_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.index_rz', 'indexBase_L_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.index_rx', 'indexBase_R_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.index_ry', 'indexBase_R_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.index_rz', 'indexBase_R_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.middle_rx', 'middleBase_L_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.middle_ry', 'middleBase_L_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.middle_rz', 'middleBase_L_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.middle_rx', 'middleBase_R_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.middle_ry', 'middleBase_R_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.middle_rz', 'middleBase_R_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.ring_rx', 'ringBase_L_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.ring_ry', 'ringBase_L_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.ring_rz', 'ringBase_L_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.ring_rx', 'ringBase_R_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.ring_ry', 'ringBase_R_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.ring_rz', 'ringBase_R_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.pinky_rx', 'pinkyBase_L_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.pinky_ry', 'pinkyBase_L_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.pinky_rz', 'pinkyBase_L_ofs_jnt.rotateZ')
        cmds.disconnectAttr('total_preSet_grp.pinky_rx', 'pinkyBase_R_ofs_jnt.rotateX')
        cmds.disconnectAttr('total_preSet_grp.pinky_ry', 'pinkyBase_R_ofs_jnt.rotateY')
        cmds.disconnectAttr('total_preSet_grp.pinky_rz', 'pinkyBase_R_ofs_jnt.rotateZ')
        cmds.setAttr("thumbBase_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("thumbBase_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("thumbBase_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("indexBase_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("indexBase_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("indexBase_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("middleBase_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("middleBase_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("middleBase_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("ringBase_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("ringBase_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("ringBase_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("pinkyBase_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("pinkyBase_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("pinkyBase_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("thumbBase_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("thumbBase_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("thumbBase_R_ofs_jnt.rz", lock=True)
        cmds.setAttr("indexBase_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("indexBase_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("indexBase_R_ofs_jnt.rz", lock=True)
        cmds.setAttr("middleBase_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("middleBase_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("middleBase_R_ofs_jnt.rz", lock=True)
        cmds.setAttr("ringBase_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("ringBase_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("ringBase_R_ofs_jnt.rz", lock=True)
        cmds.setAttr("pinkyBase_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("pinkyBase_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("pinkyBase_R_ofs_jnt.rz", lock=True)


        #손가락 길이에 관한 preSet연결 끊고, 필요없는 key data지우기
        cmds.disconnectAttr('thumb_L_ik_jnt01_tmp_translateX.output', 'thumb_L_ik_jnt01.tx')
        cmds.disconnectAttr('thumb_L_fk_jnt02_tmp_translateX.output', 'thumb_L_ctrl03.tx')
        cmds.disconnectAttr('thumb_L_fk_jntEnd_tmp_translateX.output', 'thumb_L_fk_jntEnd.tx')
        cmds.disconnectAttr('index_L_ik_jnt01_tmp_translateX.output', 'index_L_ik_jnt01.tx')
        cmds.disconnectAttr('index_L_fk_jnt02_tmp_translateX.output', 'index_L_ctrl03.tx')
        cmds.disconnectAttr('index_L_fk_jnt03_tmp_translateX.output', 'index_L_ctrl04.tx')
        cmds.disconnectAttr('index_L_fk_jntEnd_tmp_translateX.output', 'index_L_fk_jntEnd.tx')
        cmds.disconnectAttr('middle_L_ik_jnt01_tmp_translateX.output', 'middle_L_ik_jnt01.tx')
        cmds.disconnectAttr('middle_L_fk_jnt02_tmp_translateX.output', 'middle_L_ctrl03.tx')
        cmds.disconnectAttr('middle_L_fk_jnt03_tmp_translateX.output', 'middle_L_ctrl04.tx')
        cmds.disconnectAttr('middle_L_fk_jntEnd_tmp_translateX.output', 'middle_L_fk_jntEnd.tx')
        cmds.disconnectAttr('ring_L_ik_jnt01_tmp_translateX.output', 'ring_L_ik_jnt01.tx')
        cmds.disconnectAttr('ring_L_fk_jnt02_tmp_translateX.output', 'ring_L_ctrl03.tx')
        cmds.disconnectAttr('ring_L_fk_jnt03_tmp_translateX.output', 'ring_L_ctrl04.tx')
        cmds.disconnectAttr('ring_L_fk_jntEnd_tmp_translateX.output', 'ring_L_fk_jntEnd.tx')
        cmds.disconnectAttr('pinky_L_ik_jnt01_tmp_translateX.output', 'pinky_L_ik_jnt01.tx')
        cmds.disconnectAttr('pinky_L_fk_jnt02_tmp_translateX.output', 'pinky_L_ctrl03.tx')
        cmds.disconnectAttr('pinky_L_fk_jnt03_tmp_translateX.output', 'pinky_L_ctrl04.tx')
        cmds.disconnectAttr('pinky_L_fk_jntEnd_tmp_translateX.output', 'pinky_L_fk_jntEnd.tx')
        cmds.disconnectAttr('thumb_R_ik_jnt01_tmp_translateX.output', 'thumb_R_ik_jnt01.tx')
        cmds.disconnectAttr('thumb_R_fk_jnt02_tmp_translateX.output', 'thumb_R_ctrl03.tx')
        cmds.disconnectAttr('thumb_R_fk_jntEnd_tmp_translateX.output', 'thumb_R_fk_jntEnd.tx')
        cmds.disconnectAttr('index_R_ik_jnt01_tmp_translateX.output', 'index_R_ik_jnt01.tx')
        cmds.disconnectAttr('index_R_fk_jnt02_tmp_translateX.output', 'index_R_ctrl03.tx')
        cmds.disconnectAttr('index_R_fk_jnt03_tmp_translateX.output', 'index_R_ctrl04.tx')
        cmds.disconnectAttr('index_R_fk_jntEnd_tmp_translateX.output', 'index_R_fk_jntEnd.tx')
        cmds.disconnectAttr('middle_R_ik_jnt01_tmp_translateX.output', 'middle_R_ik_jnt01.tx')
        cmds.disconnectAttr('middle_R_fk_jnt02_tmp_translateX.output', 'middle_R_ctrl03.tx')
        cmds.disconnectAttr('middle_R_fk_jnt03_tmp_translateX.output', 'middle_R_ctrl04.tx')
        cmds.disconnectAttr('middle_R_fk_jntEnd_tmp_translateX.output', 'middle_R_fk_jntEnd.tx')
        cmds.disconnectAttr('ring_R_ik_jnt01_tmp_translateX.output', 'ring_R_ik_jnt01.tx')
        cmds.disconnectAttr('ring_R_fk_jnt02_tmp_translateX.output', 'ring_R_ctrl03.tx')
        cmds.disconnectAttr('ring_R_fk_jnt03_tmp_translateX.output', 'ring_R_ctrl04.tx')
        cmds.disconnectAttr('ring_R_fk_jntEnd_tmp_translateX.output', 'ring_R_fk_jntEnd.tx')
        cmds.disconnectAttr('pinky_R_ik_jnt01_tmp_translateX.output', 'pinky_R_ik_jnt01.tx')
        cmds.disconnectAttr('pinky_R_fk_jnt02_tmp_translateX.output', 'pinky_R_ctrl03.tx')
        cmds.disconnectAttr('pinky_R_fk_jnt03_tmp_translateX.output', 'pinky_R_ctrl04.tx')
        cmds.disconnectAttr('pinky_R_fk_jntEnd_tmp_translateX.output', 'pinky_R_fk_jntEnd.tx')
        cmds.setAttr("thumb_L_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("index_L_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("index_L_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("middle_L_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("middle_L_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("ring_L_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("ring_L_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("pinky_L_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("pinky_L_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("thumb_R_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("index_R_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("index_R_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("middle_R_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("middle_R_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("ring_R_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("ring_R_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("pinky_R_ctrl03.tx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("pinky_R_ctrl04.tx", lock=True, channelBox=False, keyable=False)
        cmds.delete('thumb_L_ik_jnt01_tmp_translateX', 'thumb_L_fk_jnt02_tmp_translateX', 'thumb_L_fk_jntEnd_tmp_translateX', 'index_L_ik_jnt01_tmp_translateX', 'index_L_fk_jnt02_tmp_translateX', 'index_L_fk_jnt03_tmp_translateX', 'index_L_fk_jntEnd_tmp_translateX', 'middle_L_ik_jnt01_tmp_translateX', 'middle_L_fk_jnt02_tmp_translateX', 'middle_L_fk_jnt03_tmp_translateX', 'middle_L_fk_jntEnd_tmp_translateX', 'ring_L_ik_jnt01_tmp_translateX', 'ring_L_fk_jnt02_tmp_translateX', 'ring_L_fk_jnt03_tmp_translateX', 'ring_L_fk_jntEnd_tmp_translateX', 'pinky_L_ik_jnt01_tmp_translateX', 'pinky_L_fk_jnt02_tmp_translateX', 'pinky_L_fk_jnt03_tmp_translateX', 'pinky_L_fk_jntEnd_tmp_translateX', 'thumb_R_ik_jnt01_tmp_translateX', 'thumb_R_fk_jnt02_tmp_translateX', 'thumb_R_fk_jntEnd_tmp_translateX', 'index_R_ik_jnt01_tmp_translateX', 'index_R_fk_jnt02_tmp_translateX', 'index_R_fk_jnt03_tmp_translateX', 'index_R_fk_jntEnd_tmp_translateX', 'middle_R_ik_jnt01_tmp_translateX', 'middle_R_fk_jnt02_tmp_translateX', 'middle_R_fk_jnt03_tmp_translateX', 'middle_R_fk_jntEnd_tmp_translateX', 'ring_R_ik_jnt01_tmp_translateX', 'ring_R_fk_jnt02_tmp_translateX', 'ring_R_fk_jnt03_tmp_translateX', 'ring_R_fk_jntEnd_tmp_translateX', 'pinky_R_ik_jnt01_tmp_translateX', 'pinky_R_fk_jnt02_tmp_translateX', 'pinky_R_fk_jnt03_tmp_translateX', 'pinky_R_fk_jntEnd_tmp_translateX')


        #손의 크기에 관한 preSet연결 끊고, 속성 잠그기
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_L_scale_jnt.sx')
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_L_scale_jnt.sy')
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_L_scale_jnt.sz')
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_R_scale_jnt.sx')
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_R_scale_jnt.sy')
        cmds.disconnectAttr('total_preSet_grp.hand_scale', 'hand_R_scale_jnt.sz')
        cmds.setAttr("hand_L_scale_jnt.sx", lock=True)
        cmds.setAttr("hand_R_scale_jnt.sx", lock=True)
        cmds.setAttr("hand_L_scale_jnt.sy", lock=True)
        cmds.setAttr("hand_R_scale_jnt.sy", lock=True)
        cmds.setAttr("hand_L_scale_jnt.sz", lock=True)
        cmds.setAttr("hand_R_scale_jnt.sz", lock=True)



    #####################/
    #발 세팅하기.

    def setFoot(self):

        #fk의 진짜 길이를 구한다.
        foot_height=cmds.getAttr('total_preSet_grp.toe_height')
        ball_position=cmds.getAttr('total_preSet_grp.toe_frontBack')
        toe_length=cmds.getAttr('total_preSet_grp.toe_length')
        foot_L_height=1.2 + foot_height
        ball_L_position=1 + ball_position
        toe_L_length=1.2 + toe_length
        foot_R_height=-1.2 - foot_height
        ball_R_position=-1 - ball_position
        toe_R_length=-1.2 - toe_length


        #tmp_node들로부터 연결끊고, 구한 진짜길이를 넣는다.
        cmds.disconnectAttr("toe_L_height_tmp_plus.output1D", "toe_L_fk_ctrl.tx")
        cmds.disconnectAttr("toe_L_front_tmp_plus.output1D", "toe_L_fk_ctrl.tz")
        cmds.disconnectAttr("toe_L_length_tmp_plus.output1D", "toe_L_fk_jntEnd.tx")
        cmds.setAttr("toe_L_fk_ctrl.tx", foot_L_height)
        cmds.setAttr("toe_L_fk_ctrl.tz", ball_L_position)
        cmds.setAttr("toe_L_fk_jntEnd.tx", toe_L_length)
        cmds.disconnectAttr("toe_R_height_tmp_plus.output1D", "toe_R_fk_ctrl.tx")
        cmds.disconnectAttr("toe_R_front_tmp_plus.output1D", "toe_R_fk_ctrl.tz")
        cmds.disconnectAttr("toe_R_length_tmp_plus.output1D", "toe_R_fk_jntEnd.tx")
        cmds.setAttr("toe_R_fk_ctrl.tx", foot_R_height)
        cmds.setAttr("toe_R_fk_ctrl.tz", ball_R_position)
        cmds.setAttr("toe_R_fk_jntEnd.tx", toe_R_length)

        #fk조인트를 무조건 바닥면에 붙게 한다.
        cmds.select('toe_L_fk_ctrl', r=1)
        cmds.move(0, y=1, rpr=1, ws=1)
        cmds.select('toe_R_fk_ctrl', r=1)
        cmds.move(0, y=1, rpr=1, ws=1)


        #발 위치 loc들을 tmp_grp에서 꺼낸다.
        cmds.select('foot_L_heel_loc', r=1)
        cmds.select('foot_L_outside_loc', tgl=1)
        cmds.select('foot_L_inside_loc', tgl=1)
        cmds.select('foot_R_heel_loc', tgl=1)
        cmds.select('foot_R_outside_loc', tgl=1)
        cmds.select('foot_R_inside_loc', tgl=1)
        cmds.select('total_ctrl', add=1)
        cmds.parent()

        #다른 loc들과 ik_ctrl을 해당 조인트의 위치에 맞춘다.
        self.changeLoc("toe_L_fk_ctrl", "foot_L_ball_loc")
        self.changeLoc("toe_L_fk_ctrl", "toeWiggle_L_loc")
        self.changeLoc("toe_L_fk_jntEnd", "toe_L_loc")
        self.changeLoc("foot_L_heel_loc", "foot_L_ik_ctrl_preSet_grp")
        self.changeLoc("toe_R_fk_ctrl", "foot_R_ball_loc")
        self.changeLoc("toe_R_fk_ctrl", "toeWiggle_R_loc")
        self.changeLoc("toe_R_fk_jntEnd", "toe_R_loc")
        self.changeLoc("foot_R_heel_loc", "foot_R_ik_ctrl_preSet_grp")


        #발의 매치 오브젝트도 heel_loc의 위치에 맞춘다.
        self.changeLoc("foot_L_heel_loc", "foot_L_ik_ctrl_match")
        self.changeLoc("foot_R_heel_loc", "foot_R_ik_ctrl_match")


        #ik 조인트들을 fk조인트의 위치에 맞춘다.
        self.changeLoc("toe_L_fk_ctrl", "toe_L_ik_jnt")
        self.changeLoc("toe_L_fk_jntEnd", "toe_L_ik_jntEnd")
        self.changeLoc("toe_R_fk_ctrl", "toe_R_ik_jnt")
        self.changeLoc("toe_R_fk_jntEnd", "toe_R_ik_jntEnd")

        #메인 조인트들을 fk조인트의 위치에 맞춘다.
        self.changeLoc("toe_L_fk_ctrl", "toe_L_jnt")
        self.changeLoc("toe_L_fk_jntEnd", "toe_L_jntEnd")
        self.changeLoc("toe_R_fk_ctrl", "toe_R_jnt")
        self.changeLoc("toe_R_fk_jntEnd", "toe_R_jntEnd")

        #ikSC를 건다.
        self.ikSC("foot_L_ik_jnt", "toe_L_ik_jnt", "foot_L_ikHdl", "foot_L_ik_efftr")
        self.ikSC("toe_L_ik_jnt", "toe_L_ik_jntEnd", "toe_L_ikHdl", "toe_L_ik_efftr")
        self.ikSC("foot_R_ik_jnt", "toe_R_ik_jnt", "foot_R_ikHdl", "foot_R_ik_efftr")
        self.ikSC("toe_R_ik_jnt", "toe_R_ik_jntEnd", "toe_R_ikHdl", "toe_R_ik_efftr")

        #parent구조를 만든다.
        cmds.parent('foot_L_ikHdl', 'foot_L_inside_loc')
        cmds.parent('toe_L_ikHdl', 'toeWiggle_L_loc')
        cmds.parent('leg_L_distEnd_preSet_grp', 'foot_L_ball_loc')
        cmds.parent('foot_L_ball_loc', 'toeWiggle_L_loc', 'foot_L_inside_loc')
        cmds.parent('foot_L_inside_loc', 'foot_L_outside_loc')
        cmds.parent('foot_L_outside_loc', 'toe_L_loc')
        cmds.parent('toe_L_loc', 'foot_L_heel_loc')
        cmds.parent('foot_L_heel_loc', 'foot_L_ik_ctrl')
        cmds.parent('foot_R_ikHdl', 'foot_R_inside_loc')
        cmds.parent('toe_R_ikHdl', 'toeWiggle_R_loc')
        cmds.parent('leg_R_distEnd_preSet_grp', 'foot_R_ball_loc')
        cmds.parent('foot_R_ball_loc', 'toeWiggle_R_loc', 'foot_R_inside_loc')
        cmds.parent('foot_R_inside_loc', 'foot_R_outside_loc')
        cmds.parent('foot_R_outside_loc', 'toe_R_loc')
        cmds.parent('toe_R_loc', 'foot_R_heel_loc')
        cmds.parent('foot_R_heel_loc', 'foot_R_ik_ctrl')

        #발 위치잡는 loc중 가장 상위loc을 감추고, lock시킨다.
        cmds.setAttr("foot_L_heel_loc.visibility", 0)
        cmds.setAttr("foot_L_heel_loc.v", lock=True)
        cmds.setAttr("foot_R_heel_loc.visibility", 0)
        cmds.setAttr("foot_R_heel_loc.v", lock=True)

        ##########################/
        #굳히기
        #쓸모없는 tmp_node들을 지운다.
        cmds.delete('toe_negativ_tmp_mult01', 'toe_negativ_tmp_mult02', 'toe_L_front_tmp_plus', 'toe_L_height_tmp_plus', 'toe_L_length_tmp_plus', 'toe_R_front_tmp_plus', 'toe_R_height_tmp_plus', 'toe_R_length_tmp_plus', 'foot_L_heel_loc_tmp_grp', 'foot_L_outside_loc_tmp_grp', 'foot_L_inside_loc_tmp_grp', 'foot_R_heel_loc_tmp_grp', 'foot_R_outside_loc_tmp_grp', 'foot_R_inside_loc_tmp_grp')


    #더이상 필요없는 preSet 속성들을 지운다. totla_ctrl에 초기값을 세팅한다. 키 데이터를 잠근다.

    def delPreAtt(self):


        cmds.deleteAttr("total_preSet_grp", attribute="shldr_width")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_height")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_frontBack")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_length")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_angle01")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_angle02")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="shldr_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_width")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_height")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_frontBack")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_upDown")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_angle01")
        cmds.deleteAttr("total_preSet_grp", attribute="hip_angle02")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_tx")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_ty")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_tz")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_length01")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_length02")
        cmds.deleteAttr("total_preSet_grp", attribute="thumb_length03")
        cmds.deleteAttr("total_preSet_grp", attribute="index_tx")
        cmds.deleteAttr("total_preSet_grp", attribute="index_ty")
        cmds.deleteAttr("total_preSet_grp", attribute="index_tz")
        cmds.deleteAttr("total_preSet_grp", attribute="index_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="index_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="index_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="index_length01")
        cmds.deleteAttr("total_preSet_grp", attribute="index_length02")
        cmds.deleteAttr("total_preSet_grp", attribute="index_length03")
        cmds.deleteAttr("total_preSet_grp", attribute="index_length04")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_tx")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_ty")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_tz")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_length01")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_length02")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_length03")
        cmds.deleteAttr("total_preSet_grp", attribute="middle_length04")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_tx")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_ty")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_tz")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_length01")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_length02")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_length03")
        cmds.deleteAttr("total_preSet_grp", attribute="ring_length04")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_tx")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_ty")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_tz")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_rx")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_ry")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_rz")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_length01")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_length02")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_length03")
        cmds.deleteAttr("total_preSet_grp", attribute="pinky_length04")
        cmds.deleteAttr("total_preSet_grp", attribute="hand_scale")
        cmds.deleteAttr("total_preSet_grp", attribute="upArm")
        cmds.deleteAttr("total_preSet_grp", attribute="lowArm")
        cmds.deleteAttr("total_preSet_grp", attribute="upLeg")
        cmds.deleteAttr("total_preSet_grp", attribute="lowLeg")
        cmds.deleteAttr("total_preSet_grp", attribute="toe_height")
        cmds.deleteAttr("total_preSet_grp", attribute="toe_frontBack")
        cmds.deleteAttr("total_preSet_grp", attribute="toe_length")
        cmds.deleteAttr("total_preSet_grp", attribute="heel_pos")
        cmds.deleteAttr("total_preSet_grp", attribute="outside_pos")
        cmds.deleteAttr("total_preSet_grp", attribute="inside_pos")

        #total_preSet_grp의 크기 속성을 잠근다.
        cmds.setAttr("total_preSet_grp.preScale", lock=True)

        #붉은 포인트 오브젝트들 지우자.
        cmds.delete('toeTip_L_point', 'toeTip_L_point', 'toe_L_point', 'foot_L_point', 'knee_L_point', 'leg_L_point', 'hip_L_point', 'spineStart_point', 'spineEnd_point', 'shoulder_L_point', 'arm_L_point', 'elbow_L_point', 'hand_L_point', 'thumb_L_point01', 'thumb_L_point02', 'thumb_L_point03', 'index_L_point01', 'index_L_point02', 'index_L_point03', 'index_L_point04', 'middle_L_point01', 'middle_L_point02', 'middle_L_point03', 'middle_L_point04', 'ring_L_point01', 'ring_L_point02', 'ring_L_point03', 'ring_L_point04', 'pinky_L_point01', 'pinky_L_point02', 'pinky_L_point03', 'pinky_L_point04', 'neckStart_point', 'neckEnd_point', 'footOut_L_point', 'footIn_L_point', 'heel_L_point', 'heel_R_point', 'footIn_R_point', 'footOut_R_point', 'pinky_R_point04', 'pinky_R_point03', 'pinky_R_point02', 'pinky_R_point01', 'ring_R_point04', 'ring_R_point03', 'ring_R_point02', 'ring_R_point01', 'middle_R_point04', 'middle_R_point03', 'middle_R_point02', 'middle_R_point01', 'index_R_point04', 'index_R_point03', 'index_R_point02', 'index_R_point01', 'thumb_R_point03', 'thumb_R_point02', 'thumb_R_point01', 'hand_R_point', 'elbow_R_point', 'arm_R_point', 'shoulder_R_point', 'hip_R_point', 'leg_R_point', 'knee_R_point', 'foot_R_point', 'toe_R_point', 'toeTip_R_point')


        #숨겨놨던 컨트롤러들을 보이게 한다.
        cmds.setAttr("head_ctrlShape.visibility", 1)
        cmds.setAttr("chest_ctrlShape.visibility", 1)
        cmds.setAttr("shldr_L_ctrlShape.visibility", 1)
        cmds.setAttr("shldr_R_ctrlShape.visibility", 1)
        cmds.setAttr("arm_R_orient_ctrlShape.visibility", 1)
        cmds.setAttr("arm_L_orient_ctrlShape.visibility", 1)
        cmds.setAttr("hip_ctrlShape.visibility", 1)
        cmds.setAttr("pelvis_ctrlShape.visibility", 1)
        cmds.setAttr("hip_L_ctrlShape.visibility", 1)
        cmds.setAttr("hip_R_ctrlShape.visibility", 1)
        cmds.setAttr("leg_R_orient_ctrlShape.visibility", 1)
        cmds.setAttr("leg_L_orient_ctrlShape.visibility", 1)
        cmds.setAttr("total_ctrlShape.visibility", 1)
        cmds.setAttr("total_out_ctrlShape.visibility", 1)
        cmds.setAttr("upArm_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("lowArm_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("hand_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("upArm_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("lowArm_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("hand_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("upLeg_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("lowLeg_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("foot_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("toe_L_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("upLeg_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("lowLeg_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("foot_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("toe_R_fk_ctrl_controlShape.visibility", 1)
        cmds.setAttr("finger_L_ctrlShape.visibility", 1)
        cmds.setAttr("thumb_L_ctrlShape.visibility", 1)
        cmds.setAttr("index_L_ctrlShape.visibility", 1)
        cmds.setAttr("middle_L_ctrlShape.visibility", 1)
        cmds.setAttr("ring_L_ctrlShape.visibility", 1)
        cmds.setAttr("pinky_L_ctrlShape.visibility", 1)
        cmds.setAttr("finger_R_ctrlShape.visibility", 1)
        cmds.setAttr("thumb_R_ctrlShape.visibility", 1)
        cmds.setAttr("index_R_ctrlShape.visibility", 1)
        cmds.setAttr("middle_R_ctrlShape.visibility", 1)
        cmds.setAttr("ring_R_ctrlShape.visibility", 1)
        cmds.setAttr("pinky_R_ctrlShape.visibility", 1)
        cmds.setAttr("foot_L_heel_locShape.visibility", 1)
        cmds.setAttr("foot_L_outside_locShape.visibility", 1)
        cmds.setAttr("foot_L_inside_locShape.visibility", 1)
        cmds.setAttr("foot_R_heel_locShape.visibility", 1)
        cmds.setAttr("foot_R_outside_locShape.visibility", 1)
        cmds.setAttr("foot_R_inside_locShape.visibility", 1)
        cmds.setAttr("thumb_L_ctrl01Shape.visibility", 1)
        cmds.setAttr("thumb_L_ctrl02Shape.visibility", 1)
        cmds.setAttr("thumb_L_ctrl03Shape.visibility", 1)
        cmds.setAttr("index_L_ctrl01Shape.visibility", 1)
        cmds.setAttr("index_L_ctrl02Shape.visibility", 1)
        cmds.setAttr("index_L_ctrl03Shape.visibility", 1)
        cmds.setAttr("index_L_ctrl04Shape.visibility", 1)
        cmds.setAttr("middle_L_ctrl01Shape.visibility", 1)
        cmds.setAttr("middle_L_ctrl02Shape.visibility", 1)
        cmds.setAttr("middle_L_ctrl03Shape.visibility", 1)
        cmds.setAttr("middle_L_ctrl04Shape.visibility", 1)
        cmds.setAttr("ring_L_ctrl01Shape.visibility", 1)
        cmds.setAttr("ring_L_ctrl02Shape.visibility", 1)
        cmds.setAttr("ring_L_ctrl03Shape.visibility", 1)
        cmds.setAttr("ring_L_ctrl04Shape.visibility", 1)
        cmds.setAttr("pinky_L_ctrl01Shape.visibility", 1)
        cmds.setAttr("pinky_L_ctrl02Shape.visibility", 1)
        cmds.setAttr("pinky_L_ctrl03Shape.visibility", 1)
        cmds.setAttr("pinky_L_ctrl04Shape.visibility", 1)
        cmds.setAttr("thumb_R_ctrl01Shape.visibility", 1)
        cmds.setAttr("thumb_R_ctrl02Shape.visibility", 1)
        cmds.setAttr("thumb_R_ctrl03Shape.visibility", 1)
        cmds.setAttr("index_R_ctrl01Shape.visibility", 1)
        cmds.setAttr("index_R_ctrl02Shape.visibility", 1)
        cmds.setAttr("index_R_ctrl03Shape.visibility", 1)
        cmds.setAttr("index_R_ctrl04Shape.visibility", 1)
        cmds.setAttr("middle_R_ctrl01Shape.visibility", 1)
        cmds.setAttr("middle_R_ctrl02Shape.visibility", 1)
        cmds.setAttr("middle_R_ctrl03Shape.visibility", 1)
        cmds.setAttr("middle_R_ctrl04Shape.visibility", 1)
        cmds.setAttr("ring_R_ctrl01Shape.visibility", 1)
        cmds.setAttr("ring_R_ctrl02Shape.visibility", 1)
        cmds.setAttr("ring_R_ctrl03Shape.visibility", 1)
        cmds.setAttr("ring_R_ctrl04Shape.visibility", 1)
        cmds.setAttr("pinky_R_ctrl01Shape.visibility", 1)
        cmds.setAttr("pinky_R_ctrl02Shape.visibility", 1)
        cmds.setAttr("pinky_R_ctrl03Shape.visibility", 1)
        cmds.setAttr("pinky_R_ctrl04Shape.visibility", 1)

        #손 조인트를 감춘다.
        #setAttr "handBase_L_jnt.visibility" 0;
        #setAttr "handBase_R_jnt.visibility" 0;

        #주요 컨트롤러의 기본 값을 정한다.

        cmds.setAttr("total_ctrl.arm_L_fkik", 0)
        cmds.setAttr("total_ctrl.arm_R_fkik", 0)
        cmds.setAttr("total_ctrl.leg_L_fkik", 1)
        cmds.setAttr("total_ctrl.leg_R_fkik", 1)
        cmds.setAttr("total_ctrl.fk_arm_L_orient", 0)
        cmds.setAttr("total_ctrl.fk_arm_R_orient", 0)
        cmds.setAttr("total_ctrl.fk_leg_L_orient", 0)
        cmds.setAttr("total_ctrl.fk_leg_R_orient", 0)
        cmds.setAttr("total_ctrl.ik_elbow_L_hand_fkik", 1)
        cmds.setAttr("total_ctrl.ik_elbow_R_hand_fkik", 1)
        cmds.setAttr("total_ctrl.ik_leg_L_kneeVis", 0)
        cmds.setAttr("total_ctrl.ik_leg_R_kneeVis", 0)
        cmds.setAttr("total_ctrl.exCtrls_vis", 0)
        cmds.setAttr("total_ctrl.facialCtrls_vis", 1)
        cmds.setAttr("total_ctrl.accCtrls_vis", 1)
        cmds.setAttr("total_ctrl.model_vis", 1)
        #cmds.setAttr("total_ctrl.disco_boots_vis", 1)
        cmds.setAttr("total_ctrl.hair_vis", 1)

        #모든 키 데이터를 잠근다.
        cmds.select(cmds.ls(type='animCurve'))
        cmds.setAttr(".keyTimeValue", l=1)


        # #더미 오브젝트들을 보인다.
        # setAttr "head_dummy.visibility" 1;
        # setAttr "neck_dummy01.visibility" 1;
        # setAttr "neck_dummy02.visibility" 1;
        # setAttr "neck_dummy03.visibility" 1;
        # setAttr "neck_dummy04.visibility" 1;
        # setAttr "neck_dummy05.visibility" 1;
        # setAttr "neck_dummy06.visibility" 1;
        # setAttr "neck_dummy07.visibility" 1;
        # setAttr "spine_dummy01.visibility" 1;
        # setAttr "spine_dummy02.visibility" 1;
        # setAttr "spine_dummy03.visibility" 1;
        # setAttr "spine_dummy04.visibility" 1;
        # setAttr "spine_dummy05.visibility" 1;
        # setAttr "spine_dummy06.visibility" 1;
        # setAttr "spine_dummy07.visibility" 1;
        # setAttr "shldr_L_dummy01.visibility" 1;
        # setAttr "shldr_L_dummy02.visibility" 1;
        # setAttr "arm_L_dummy01.visibility" 1;
        # setAttr "arm_L_dummy02.visibility" 1;
        # setAttr "arm_L_dummy03.visibility" 1;
        # setAttr "arm_L_dummy04.visibility" 1;
        # setAttr "arm_L_dummy05.visibility" 1;
        # setAttr "arm_L_dummy06.visibility" 1;
        # setAttr "arm_L_dummy07.visibility" 1;
        # setAttr "arm_L_dummy08.visibility" 1;
        # setAttr "arm_L_dummy09.visibility" 1;
        # setAttr "hand_L_dummy.visibility" 1;
        # setAttr "thumb_L_dummy01.visibility" 1;
        # setAttr "thumb_L_dummy02.visibility" 1;
        # setAttr "thumb_L_dummy03.visibility" 1;
        # setAttr "thumb_L_dummy04.visibility" 1;
        # setAttr "index_L_dummy01.visibility" 1;
        # setAttr "index_L_dummy02.visibility" 1;
        # setAttr "index_L_dummy03.visibility" 1;
        # setAttr "index_L_dummy04.visibility" 1;
        # setAttr "middle_L_dummy01.visibility" 1;
        # setAttr "middle_L_dummy02.visibility" 1;
        # setAttr "middle_L_dummy03.visibility" 1;
        # setAttr "middle_L_dummy04.visibility" 1;
        # setAttr "ring_L_dummy01.visibility" 1;
        # setAttr "ring_L_dummy02.visibility" 1;
        # setAttr "ring_L_dummy03.visibility" 1;
        # setAttr "ring_L_dummy04.visibility" 1;
        # setAttr "pinky_L_dummy01.visibility" 1;
        # setAttr "pinky_L_dummy02.visibility" 1;
        # setAttr "pinky_L_dummy03.visibility" 1;
        # setAttr "pinky_L_dummy04.visibility" 1;
        # setAttr "hip_L_dummy01.visibility" 1;
        # setAttr "hip_L_dummy02.visibility" 1;
        # setAttr "leg_L_dummy01.visibility" 1;
        # setAttr "leg_L_dummy02.visibility" 1;
        # setAttr "leg_L_dummy03.visibility" 1;
        # setAttr "leg_L_dummy04.visibility" 1;
        # setAttr "leg_L_dummy05.visibility" 1;
        # setAttr "leg_L_dummy06.visibility" 1;
        # setAttr "leg_L_dummy07.visibility" 1;
        # setAttr "leg_L_dummy08.visibility" 1;
        # setAttr "leg_L_dummy09.visibility" 1;
        # setAttr "foot_L_dummy01.visibility" 1;
        # setAttr "foot_L_dummy02.visibility" 1;
        # setAttr "foot_L_dummy03.visibility" 1;
        # setAttr "shldr_R_dummy01.visibility" 1;
        # setAttr "shldr_R_dummy02.visibility" 1;
        # setAttr "arm_R_dummy01.visibility" 1;
        # setAttr "arm_R_dummy02.visibility" 1;
        # setAttr "arm_R_dummy03.visibility" 1;
        # setAttr "arm_R_dummy04.visibility" 1;
        # setAttr "arm_R_dummy05.visibility" 1;
        # setAttr "arm_R_dummy06.visibility" 1;
        # setAttr "arm_R_dummy07.visibility" 1;
        # setAttr "arm_R_dummy08.visibility" 1;
        # setAttr "arm_R_dummy09.visibility" 1;
        # setAttr "hand_R_dummy.visibility" 1;
        # setAttr "thumb_R_dummy01.visibility" 1;
        # setAttr "thumb_R_dummy02.visibility" 1;
        # setAttr "thumb_R_dummy03.visibility" 1;
        # setAttr "thumb_R_dummy04.visibility" 1;
        # setAttr "index_R_dummy01.visibility" 1;
        # setAttr "index_R_dummy02.visibility" 1;
        # setAttr "index_R_dummy03.visibility" 1;
        # setAttr "index_R_dummy04.visibility" 1;
        # setAttr "middle_R_dummy01.visibility" 1;
        # setAttr "middle_R_dummy02.visibility" 1;
        # setAttr "middle_R_dummy03.visibility" 1;
        # setAttr "middle_R_dummy04.visibility" 1;
        # setAttr "ring_R_dummy01.visibility" 1;
        # setAttr "ring_R_dummy02.visibility" 1;
        # setAttr "ring_R_dummy03.visibility" 1;
        # setAttr "ring_R_dummy04.visibility" 1;
        # setAttr "pinky_R_dummy01.visibility" 1;
        # setAttr "pinky_R_dummy02.visibility" 1;
        # setAttr "pinky_R_dummy03.visibility" 1;
        # setAttr "pinky_R_dummy04.visibility" 1;
        # setAttr "hip_R_dummy01.visibility" 1;
        # setAttr "hip_R_dummy02.visibility" 1;
        # setAttr "leg_R_dummy01.visibility" 1;
        # setAttr "leg_R_dummy02.visibility" 1;
        # setAttr "leg_R_dummy03.visibility" 1;
        # setAttr "leg_R_dummy04.visibility" 1;
        # setAttr "leg_R_dummy05.visibility" 1;
        # setAttr "leg_R_dummy06.visibility" 1;
        # setAttr "leg_R_dummy07.visibility" 1;
        # setAttr "leg_R_dummy08.visibility" 1;
        # setAttr "leg_R_dummy09.visibility" 1;
        # setAttr "foot_R_dummy01.visibility" 1;
        # setAttr "foot_R_dummy02.visibility" 1;
        # setAttr "foot_R_dummy03.visibility" 1;
        # select -cl  ;



    #빈 transform노드들을 지운다.
    def delEmpty(self):
        cmds.select(ado=1, r=1)
        dups=cmds.ls(sl=1)
        cmds.select(cl=1)
        dup = ""
        m = 0
        tmp = 0
        for dup in dups:
            tmp=int(gmatch(dup, "transform*"))
            if tmp == 1:
                tmpPrnt = [""] * (0)
                tmpChld = [""] * (0)
                tmpShp = [""] * (0)
                tmpPrnt=cmds.listRelatives(dups[m], p=1, f=1)
                tmpChld=cmds.listRelatives(dups[m], c=1, f=1)
                tmpShp=cmds.listRelatives(dups[m], s=1, f=1)
                if (tmpPrnt[0] == "") and (tmpChld[0] == "") and (tmpShp[0] == ""):
                    cmds.delete(dups[m])
                    
                
            m+=1
        


    # #############################/
    # #캐릭터 셋 만들기

    def keySet(self):


        # #$head_ctrl[];

        # #$head_ctrl[0]="head_ctrl";
                        
        # character -name "keySet";
        # setCurrentCharacters( { "keySet" } );
        # doCreateSubcharacterArgList 2 { "A_body","0","0","0","0","0","0" };
        # doCreateSubcharacterArgList 2 { "B_face","0","0","0","0","0","0" };
        # doCreateSubcharacterArgList 2 { "C_exCtrls","0","0","0","0","0","0" };
        # doCreateSubcharacterArgList 2 { "D_etc","0","0","0","0","0","0" };

        # 	setCurrentCharacters( { "A_body" } );
        # 	doCreateSubcharacterArgList 2 { "Aa_bodyUpper","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Ab_bodyLower","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Ac_bodyTotal","0","0","0","0","0","0" };

        # 	setCurrentCharacters( { "B_face" } );
        # 	doCreateSubcharacterArgList 2 { "Ba_faceUpper","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Bb_faceLower","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Bc_faceSquash","0","0","0","0","0","0" };

        # 	setCurrentCharacters( { "C_exCtrls" } );
        # 	doCreateSubcharacterArgList 2 { "Ca_exArm_L","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Cb_exArm_R","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Cc_exLeg_L","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Cd_exLeg_R","0","0","0","0","0","0" };

        #     setCurrentCharacters( { "D_etc" } );
        # 	doCreateSubcharacterArgList 2 { "Da_acc","0","0","0","0","0","0" };
        # 	doCreateSubcharacterArgList 2 { "Db_hear","0","0","0","0","0","0" };

        # 		setCurrentCharacters( { "Aa_bodyUpper" } );
        # 		doCreateSubcharacterArgList 2 { "Aa1_eye","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa2_head","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa3_torso","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa4_arm_L","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa5_arm_R","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa6_hand_L","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Aa7_hand_R","0","0","0","0","0","0" };

        # 		setCurrentCharacters( { "Ab_bodyLower" } );
        # 		doCreateSubcharacterArgList 2 { "Ab1_pelvis","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Ab2_leg_L","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Ab3_leg_R","0","0","0","0","0","0" };
        #         doCreateSubcharacterArgList 2 { "Ab4_foot_L","0","0","0","0","0","0" };
        # 		doCreateSubcharacterArgList 2 { "Ab5_foot_R","0","0","0","0","0","0" };

        # ClearCurrentCharacterList;

        # character	-forceElement Aa2_head 
        # 		head_ctrl
        # 		neck_ctrl
        # 		neck_fk_ctrl01
        # 		neck_fk_ctrl02
        #         ;
        # character	-forceElement Aa3_torso 
        # 		spine_fk_ctrl01
        # 		spine_ik_ctrl01
        # 		spine_fk_ctrl02
        # 		spine_ik_ctrl02
        # 		chest_ctrl
        #         ;

        # character	-forceElement Aa4_arm_L 
        # 		hand_L_fk_ctrl
        # 		lowArm_L_fk_ctrl
        # 		upArm_L_fk_ctrl
        # 		arm_L_orient_ctrl
        # 		hand_L_ik_ctrl
        # 		elbow_L_ik_ctrl
        # 		elbowHand_L_fk_ctrl
        # 		shldr_L_ctrl
        #         ;

        # character	-forceElement Aa5_arm_R 
        # 		hand_R_fk_ctrl
        # 		lowArm_R_fk_ctrl
        # 		upArm_R_fk_ctrl
        # 		arm_R_orient_ctrl
        # 		hand_R_ik_ctrl
        # 		elbow_R_ik_ctrl
        # 		elbowHand_R_fk_ctrl
        # 		shldr_R_ctrl
        #         ;

        # character	-forceElement Aa6_hand_L 
        # 		finger_L_ctrl
        # 		thumb_L_ctrl
        # 		thumb_L_ctrl01
        # 		thumb_L_ctrl02
        # 		thumb_L_ctrl03
        # 		index_L_ctrl
        # 		index_L_ctrl01
        # 		index_L_ctrl02
        # 		index_L_ctrl03
        # 		index_L_ctrl04
        # 		middle_L_ctrl
        # 		middle_L_ctrl01
        # 		middle_L_ctrl02
        # 		middle_L_ctrl03
        # 		middle_L_ctrl04
        # 		ring_L_ctrl
        # 		ring_L_ctrl01
        # 		ring_L_ctrl02
        # 		ring_L_ctrl03
        # 		ring_L_ctrl04
        # 		pinky_L_ctrl
        # 		pinky_L_ctrl01
        # 		pinky_L_ctrl02
        # 		pinky_L_ctrl03
        # 		pinky_L_ctrl04
        #         ;

        # character	-forceElement Aa7_hand_R 
        # 		finger_R_ctrl
        # 		thumb_R_ctrl
        # 		thumb_R_ctrl01
        # 		thumb_R_ctrl02
        # 		thumb_R_ctrl03
        # 		index_R_ctrl
        # 		index_R_ctrl01
        # 		index_R_ctrl02
        # 		index_R_ctrl03
        # 		index_R_ctrl04
        # 		middle_R_ctrl
        # 		middle_R_ctrl01
        # 		middle_R_ctrl02
        # 		middle_R_ctrl03
        # 		middle_R_ctrl04
        # 		ring_R_ctrl
        # 		ring_R_ctrl01
        # 		ring_R_ctrl02
        # 		ring_R_ctrl03
        # 		ring_R_ctrl04
        # 		pinky_R_ctrl
        # 		pinky_R_ctrl01
        # 		pinky_R_ctrl02
        # 		pinky_R_ctrl03
        # 		pinky_R_ctrl04
        #         ;

        # character	-forceElement Ab1_pelvis 
        # 		pelvis_ctrl
        # 		hip_ctrl
        #         ;

        # character	-forceElement Ab2_leg_L 
        # 		lowLeg_L_fk_ctrl
        # 		upLeg_L_fk_ctrl
        # 		leg_L_orient_ctrl
        # 		knee_L_ctrl
        # 		hip_L_ctrl
        #         ;

        # character	-forceElement Ab3_leg_R 
        # 		lowLeg_R_fk_ctrl
        # 		upLeg_R_fk_ctrl
        # 		leg_R_orient_ctrl
        # 		knee_R_ctrl
        # 		hip_R_ctrl
        #         ;

        # character	-forceElement Ab4_foot_L 
        # 		toe_L_fk_ctrl
        # 		foot_L_fk_ctrl		
        # 		foot_L_ik_ctrl		
        #         ;

        #  character	-forceElement Ab5_foot_R 
        # 		toe_R_fk_ctrl
        # 		foot_R_fk_ctrl		
        # 		foot_R_ik_ctrl		
        #         ;
            

        # character	-forceElement Ac_bodyTotal 
        # 		total_ctrl
        # 		#total_pivot_ctrl
        # 		total_out_ctrl
        #         ;


        # character	-forceElement Ca_exArm_L
        # 		arm_L_ex_ctrl1
        # 		arm_L_ex_ctrl2
        # 		arm_L_ex_ctrl3
        # 		arm_L_ex_ctrl4
        # 		arm_L_ex_ctrl5
        #         ;

        # character	-forceElement Cb_exArm_R
        # 		arm_R_ex_ctrl1
        # 		arm_R_ex_ctrl2
        # 		arm_R_ex_ctrl3
        # 		arm_R_ex_ctrl4
        # 		arm_R_ex_ctrl5
        #         ;

        # character	-forceElement Cc_exLeg_L
        # 		leg_L_ex_ctrl1
        # 		leg_L_ex_ctrl2
        # 		leg_L_ex_ctrl3
        # 		leg_L_ex_ctrl4
        # 		leg_L_ex_ctrl5
        #         ;

        # character	-forceElement Cd_exLeg_R
        # 		leg_R_ex_ctrl1
        # 		leg_R_ex_ctrl2
        # 		leg_R_ex_ctrl3
        # 		leg_R_ex_ctrl4
        # 		leg_R_ex_ctrl5
        #         ;



        # #############################################
        # #caharacter default pose 만들기
        # #pose -name "eye_pose" "Aa1_eye";

        # pose -name "defalut_pose" "keySet";



        ############################################/
        #ctrl_set 만들기

        eye_set=cmds.sets(n="eye_ctrl_set")
        head_set=cmds.sets('head_ctrl', 'neck_ctrl', 'neck_fk_ctrl01', 'neck_fk_ctrl02', n="head_ctrl_set")
        L_arm_set=cmds.sets('hand_L_fk_ctrl', 'lowArm_L_fk_ctrl', 'upArm_L_fk_ctrl', 'arm_L_orient_ctrl', 'hand_L_ik_ctrl', 'elbow_L_ik_ctrl', 'elbowHand_L_fk_ctrl', 'shldr_L_ctrl', 'arm_L_ex_ctrl1', 'arm_L_ex_ctrl2', 'arm_L_ex_ctrl3', 'arm_L_ex_ctrl4', 'arm_L_ex_ctrl5', n="L_arm_ctrl_set")
        R_arm_set=cmds.sets('hand_R_fk_ctrl', 'lowArm_R_fk_ctrl', 'upArm_R_fk_ctrl', 'arm_R_orient_ctrl', 'hand_R_ik_ctrl', 'elbow_R_ik_ctrl', 'elbowHand_R_fk_ctrl', 'shldr_R_ctrl', 'arm_R_ex_ctrl1', 'arm_R_ex_ctrl2', 'arm_R_ex_ctrl3', 'arm_R_ex_ctrl4', 'arm_R_ex_ctrl5', n="R_arm_ctrl_set")
        L_hand_set=cmds.sets('finger_L_ctrl', 'thumb_L_ctrl', 'thumb_L_ctrl01', 'thumb_L_ctrl02', 'thumb_L_ctrl03', 'index_L_ctrl', 'index_L_ctrl01', 'index_L_ctrl02', 'index_L_ctrl03', 'index_L_ctrl04', 'middle_L_ctrl', 'middle_L_ctrl01', 'middle_L_ctrl02', 'middle_L_ctrl03', 'middle_L_ctrl04', 'ring_L_ctrl', 'ring_L_ctrl01', 'ring_L_ctrl02', 'ring_L_ctrl03', 'ring_L_ctrl04', 'pinky_L_ctrl', 'pinky_L_ctrl01', 'pinky_L_ctrl02', 'pinky_L_ctrl03', 'pinky_L_ctrl04', n="L_hand_ctrl_set")
        R_hand_set=cmds.sets('finger_R_ctrl', 'thumb_R_ctrl', 'thumb_R_ctrl01', 'thumb_R_ctrl02', 'thumb_R_ctrl03', 'index_R_ctrl', 'index_R_ctrl01', 'index_R_ctrl02', 'index_R_ctrl03', 'index_R_ctrl04', 'middle_R_ctrl', 'middle_R_ctrl01', 'middle_R_ctrl02', 'middle_R_ctrl03', 'middle_R_ctrl04', 'ring_R_ctrl', 'ring_R_ctrl01', 'ring_R_ctrl02', 'ring_R_ctrl03', 'ring_R_ctrl04', 'pinky_R_ctrl', 'pinky_R_ctrl01', 'pinky_R_ctrl02', 'pinky_R_ctrl03', 'pinky_R_ctrl04', n="R_hand_ctrl_set")
        L_leg_set=cmds.sets('lowLeg_L_fk_ctrl', 'upLeg_L_fk_ctrl', 'leg_L_orient_ctrl', 'knee_L_ctrl', 'hip_L_ctrl', 'leg_L_ex_ctrl1', 'leg_L_ex_ctrl2', 'leg_L_ex_ctrl3', 'leg_L_ex_ctrl4', 'leg_L_ex_ctrl5', n="L_leg_ctrl_set")
        R_leg_set=cmds.sets('lowLeg_R_fk_ctrl', 'upLeg_R_fk_ctrl', 'leg_R_orient_ctrl', 'knee_R_ctrl', 'hip_R_ctrl', 'leg_R_ex_ctrl1', 'leg_R_ex_ctrl2', 'leg_R_ex_ctrl3', 'leg_R_ex_ctrl4', 'leg_R_ex_ctrl5', n="R_leg_ctrl_set")
        L_foot_set=cmds.sets('toe_L_fk_ctrl', 'foot_L_fk_ctrl', 'foot_L_ik_ctrl', n="L_foot_ctrl_set")
        R_foot_set=cmds.sets('toe_R_fk_ctrl', 'foot_R_fk_ctrl', 'foot_R_ik_ctrl', n="R_foot_ctrl_set")
        spline_set=cmds.sets('spine_fk_ctrl01', 'spine_fk_ctrl02', 'spine_ik_ctrl01', 'spine_ik_ctrl02', 'chest_ctrl', 'pelvis_ctrl', 'hip_ctrl', n="spline_ctrl_set")
        total_set=cmds.sets('total_ctrl', 'total_out_ctrl', n="total_ctrl_set")
        acc_set=cmds.sets(n="acc_ctrl_set")
        hair_set=cmds.sets(n="hair_ctrl_set")
        body_set=cmds.sets(eye_set, head_set, L_arm_set, R_arm_set, L_hand_set, R_hand_set, L_leg_set, R_leg_set, spline_set, total_set, L_foot_set, R_foot_set, n="body_ctrl_set")
        cmds.sets(body_set, acc_set, hair_set, n="all_ctrl_set")


        ############################################
        #cltrl layer 만들기
        cmds.createDisplayLayer('head_ctrl', 'neck_ctrl', 'neck_fk_ctrl01', 'neck_fk_ctrl02', 'hand_L_fk_ctrl', 'lowArm_L_fk_ctrl', 'upArm_L_fk_ctrl', 'arm_L_orient_ctrl', 'hand_L_ik_ctrl', 'elbow_L_ik_ctrl', 'elbowHand_L_fk_ctrl', 'shldr_L_ctrl', 'arm_L_ex_ctrl1', 'arm_L_ex_ctrl2', 'arm_L_ex_ctrl3', 'arm_L_ex_ctrl4', 'arm_L_ex_ctrl5', 'hand_R_fk_ctrl', 'lowArm_R_fk_ctrl', 'upArm_R_fk_ctrl', 'arm_R_orient_ctrl', 'hand_R_ik_ctrl', 'elbow_R_ik_ctrl', 'elbowHand_R_fk_ctrl', 'shldr_R_ctrl', 'arm_R_ex_ctrl1', 'arm_R_ex_ctrl2', 'arm_R_ex_ctrl3', 'arm_R_ex_ctrl4', 'arm_R_ex_ctrl5', 'finger_L_ctrl', 'thumb_L_ctrl', 'thumb_L_ctrl01', 'thumb_L_ctrl02', 'thumb_L_ctrl03', 'index_L_ctrl', 'index_L_ctrl01', 'index_L_ctrl02', 'index_L_ctrl03', 'index_L_ctrl04', 'middle_L_ctrl', 'middle_L_ctrl01', 'middle_L_ctrl02', 'middle_L_ctrl03', 'middle_L_ctrl04', 'ring_L_ctrl', 'ring_L_ctrl01', 'ring_L_ctrl02', 'ring_L_ctrl03', 'ring_L_ctrl04', 'pinky_L_ctrl', 'pinky_L_ctrl01', 'pinky_L_ctrl02', 'pinky_L_ctrl03', 'pinky_L_ctrl04', 'finger_R_ctrl', 'thumb_R_ctrl', 'thumb_R_ctrl01', 'thumb_R_ctrl02', 'thumb_R_ctrl03', 'index_R_ctrl', 'index_R_ctrl01', 'index_R_ctrl02', 'index_R_ctrl03', 'index_R_ctrl04', 'middle_R_ctrl', 'middle_R_ctrl01', 'middle_R_ctrl02', 'middle_R_ctrl03', 'middle_R_ctrl04', 'ring_R_ctrl', 'ring_R_ctrl01', 'ring_R_ctrl02', 'ring_R_ctrl03', 'ring_R_ctrl04', 'pinky_R_ctrl', 'pinky_R_ctrl01', 'pinky_R_ctrl02', 'pinky_R_ctrl03', 'pinky_R_ctrl04', 'lowLeg_L_fk_ctrl', 'upLeg_L_fk_ctrl', 'leg_L_orient_ctrl', 'knee_L_ctrl', 'hip_L_ctrl', 'leg_L_ex_ctrl1', 'leg_L_ex_ctrl2', 'leg_L_ex_ctrl3', 'leg_L_ex_ctrl4', 'leg_L_ex_ctrl5', 'lowLeg_R_fk_ctrl', 'upLeg_R_fk_ctrl', 'leg_R_orient_ctrl', 'knee_R_ctrl', 'hip_R_ctrl', 'leg_R_ex_ctrl1', 'leg_R_ex_ctrl2', 'leg_R_ex_ctrl3', 'leg_R_ex_ctrl4', 'leg_R_ex_ctrl5', 'spine_fk_ctrl01', 'spine_fk_ctrl02', 'spine_ik_ctrl01', 'spine_ik_ctrl02', 'chest_ctrl', 'pelvis_ctrl', 'hip_ctrl', 'total_ctrl', 'total_out_ctrl', nr=1, 
            name="body_ctrl_layer", number=1)





    ##############################/
    #Patch up 2014.03.31
    #내용 - ik 손과 발이 몸통을 따라 움직였으면 좋겠다는 애니메이터들의 의견 수렴.
    ##############################################


    def patchUp_20140331(self):

        #hand_L_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="hand_L_ik_ctrl_cnst_grp")
        self.changeLoc("hand_L_ik_ctrl", "hand_L_ik_ctrl_cnst_grp")
        cmds.parent("hand_L_ik_ctrl_cnst_grp", "hand_L_ik_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("hand_L_ik_ctrl_prnt_grp", "hand_L_ik_ctrl_cnst_grp")


        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('hand_L_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="spine_shldrPin", max=1, k=1, at='double', dv=0)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="hand_L_ik_ctrl_world_grp")
        cmds.parent("hand_L_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)

        # parent cnst를 건다.

        cmds.select('hand_L_ik_ctrl_world_grp', r=1)
        cmds.select('spine_fk_jntEnd', tgl=1)
        cmds.select('shldr_L_ctrl', add=1)
        cmds.select('hand_L_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='hand_L_ik_ctrl_cnst_grp_prntCnst')

        #ctrl에 연결한다.

        cmds.connectAttr('hand_L_ik_ctrl.worldPin', 'hand_L_ik_ctrl_cnst_grp_prntCnst.hand_L_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='hand_L_ik_ctrl_rvrs')
        cmds.createNode('multiplyDivide', n='hand_L_ik_ctrl_mult')
        cmds.connectAttr('hand_L_ik_ctrl.worldPin', 'hand_L_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('hand_L_ik_ctrl.spine_shldrPin', 'hand_L_ik_ctrl_rvrs.inputY', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_rvrs.outputX', 'hand_L_ik_ctrl_mult.input2X', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_rvrs.outputX', 'hand_L_ik_ctrl_mult.input2Y', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_rvrs.outputY', 'hand_L_ik_ctrl_mult.input1Y', f=1)
        cmds.connectAttr('hand_L_ik_ctrl.spine_shldrPin', 'hand_L_ik_ctrl_mult.input1X', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_mult.outputY', 'hand_L_ik_ctrl_cnst_grp_prntCnst.spine_fk_jntEndW1', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_mult.outputX', 'hand_L_ik_ctrl_cnst_grp_prntCnst.shldr_L_ctrlW2', f=1)
        cmds.setAttr("hand_L_ik_ctrl.spine_shldrPin", 0)
        cmds.setAttr("hand_L_ik_ctrl.worldPin", 0)
        cmds.select(cl=1)


        #elbow_L_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="elbow_L_ik_ctrl_cnst_grp")
        self.changeLoc("elbow_L_ik_ctrl", "elbow_L_ik_ctrl_cnst_grp")
        cmds.parent("elbow_L_ik_ctrl_cnst_grp", "elbow_L_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("elbow_L_ik_ctrl", "elbow_L_ik_ctrl_cnst_grp")



        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('elbow_L_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="elbow_L_ik_ctrl_world_grp")
        cmds.parent("elbow_L_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)

        # parent cnst를 건다.
        cmds.select('elbow_L_ik_ctrl_world_grp', r=1)
        cmds.select('spine_fk_jntEnd', tgl=1)
        cmds.select('shldr_L_ctrl', add=1)
        cmds.select('elbow_L_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='elbow_L_ik_ctrl_cnst_grp_prntCnst')


        #ctrl에 연결한다.

        cmds.connectAttr('elbow_L_ik_ctrl.worldPin', 'elbow_L_ik_ctrl_cnst_grp_prntCnst.elbow_L_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='elbow_L_ik_ctrl_rvrs')
        cmds.createNode('multiplyDivide', n='elbow_L_ik_ctrl_mult')
        cmds.connectAttr('hand_L_ik_ctrl.spine_shldrPin', 'elbow_L_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('elbow_L_ik_ctrl_rvrs.outputX', 'elbow_L_ik_ctrl_mult.input2X', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_rvrs.outputZ', 'elbow_L_ik_ctrl_mult.input1X', f=1)
        cmds.connectAttr('elbow_L_ik_ctrl.worldPin', 'hand_L_ik_ctrl_rvrs.inputZ', f=1)
        cmds.connectAttr('elbow_L_ik_ctrl_mult.outputX', 'elbow_L_ik_ctrl_cnst_grp_prntCnst.spine_fk_jntEndW1', f=1)
        cmds.connectAttr('hand_L_ik_ctrl.spine_shldrPin', 'elbow_L_ik_ctrl_mult.input2Y', f=1)
        cmds.connectAttr('hand_L_ik_ctrl_rvrs.outputZ', 'elbow_L_ik_ctrl_mult.input1Y', f=1)
        cmds.connectAttr('elbow_L_ik_ctrl_mult.outputY', 'elbow_L_ik_ctrl_cnst_grp_prntCnst.shldr_L_ctrlW2', f=1)
        cmds.setAttr("elbow_L_ik_ctrl.worldPin", 0)
        cmds.select(cl=1)

        ##################################/
        #hand_R_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="hand_R_ik_ctrl_cnst_grp")
        self.changeLoc("hand_R_ik_ctrl", "hand_R_ik_ctrl_cnst_grp")
        cmds.parent("hand_R_ik_ctrl_cnst_grp", "hand_R_ik_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("hand_R_ik_ctrl_prnt_grp", "hand_R_ik_ctrl_cnst_grp")

        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('hand_R_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="spine_shldrPin", max=1, k=1, at='double', dv=0)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="hand_R_ik_ctrl_world_grp")
        cmds.parent("hand_R_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        # parent cnst를 건다.

        cmds.select('hand_R_ik_ctrl_world_grp', r=1)
        cmds.select('spine_fk_jntEnd', tgl=1)
        cmds.select('shldr_R_ctrl', add=1)
        cmds.select('hand_R_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='hand_R_ik_ctrl_cnst_grp_prntCnst')


        #ctrl에 연결한다.

        cmds.connectAttr('hand_R_ik_ctrl.worldPin', 'hand_R_ik_ctrl_cnst_grp_prntCnst.hand_R_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='hand_R_ik_ctrl_rvrs')
        cmds.createNode('multiplyDivide', n='hand_R_ik_ctrl_mult')
        cmds.connectAttr('hand_R_ik_ctrl.worldPin', 'hand_R_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('hand_R_ik_ctrl.spine_shldrPin', 'hand_R_ik_ctrl_rvrs.inputY', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_rvrs.outputX', 'hand_R_ik_ctrl_mult.input2X', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_rvrs.outputX', 'hand_R_ik_ctrl_mult.input2Y', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_rvrs.outputY', 'hand_R_ik_ctrl_mult.input1Y', f=1)
        cmds.connectAttr('hand_R_ik_ctrl.spine_shldrPin', 'hand_R_ik_ctrl_mult.input1X', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_mult.outputY', 'hand_R_ik_ctrl_cnst_grp_prntCnst.spine_fk_jntEndW1', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_mult.outputX', 'hand_R_ik_ctrl_cnst_grp_prntCnst.shldr_R_ctrlW2', f=1)
        cmds.setAttr("hand_R_ik_ctrl.spine_shldrPin", 0)
        cmds.setAttr("hand_R_ik_ctrl.worldPin", 0)
        cmds.select(cl=1)

        #elbow_R_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="elbow_R_ik_ctrl_cnst_grp")
        self.changeLoc("elbow_R_ik_ctrl", "elbow_R_ik_ctrl_cnst_grp")
        cmds.parent("elbow_R_ik_ctrl_cnst_grp", "elbow_R_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("elbow_R_ik_ctrl", "elbow_R_ik_ctrl_cnst_grp")

        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('elbow_R_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="elbow_R_ik_ctrl_world_grp")
        cmds.parent("elbow_R_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        # parent cnst를 건다.
        cmds.select('elbow_R_ik_ctrl_world_grp', r=1)
        cmds.select('spine_fk_jntEnd', tgl=1)
        cmds.select('shldr_R_ctrl', add=1)
        cmds.select('elbow_R_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='elbow_R_ik_ctrl_cnst_grp_prntCnst')

        #ctrl에 연결한다.

        cmds.connectAttr('elbow_R_ik_ctrl.worldPin', 'elbow_R_ik_ctrl_cnst_grp_prntCnst.elbow_R_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='elbow_R_ik_ctrl_rvrs')
        cmds.createNode('multiplyDivide', n='elbow_R_ik_ctrl_mult')
        cmds.connectAttr('hand_R_ik_ctrl.spine_shldrPin', 'elbow_R_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('elbow_R_ik_ctrl_rvrs.outputX', 'elbow_R_ik_ctrl_mult.input2X', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_rvrs.outputZ', 'elbow_R_ik_ctrl_mult.input1X', f=1)
        cmds.connectAttr('elbow_R_ik_ctrl.worldPin', 'hand_R_ik_ctrl_rvrs.inputZ', f=1)
        cmds.connectAttr('elbow_R_ik_ctrl_mult.outputX', 'elbow_R_ik_ctrl_cnst_grp_prntCnst.spine_fk_jntEndW1', f=1)
        cmds.connectAttr('hand_R_ik_ctrl.spine_shldrPin', 'elbow_R_ik_ctrl_mult.input2Y', f=1)
        cmds.connectAttr('hand_R_ik_ctrl_rvrs.outputZ', 'elbow_R_ik_ctrl_mult.input1Y', f=1)
        cmds.connectAttr('elbow_R_ik_ctrl_mult.outputY', 'elbow_R_ik_ctrl_cnst_grp_prntCnst.shldr_R_ctrlW2', f=1)
        cmds.setAttr("elbow_R_ik_ctrl.worldPin", 0)
        cmds.select(cl=1)

        ###############################################
        #foot_L_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="foot_L_ik_ctrl_cnst_grp")
        self.changeLoc("foot_L_ik_ctrl", "foot_L_ik_ctrl_cnst_grp")
        cmds.parent("foot_L_ik_ctrl_cnst_grp", "foot_L_ik_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("foot_L_ik_ctrl_prnt_grp", "foot_L_ik_ctrl_cnst_grp")


        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('foot_L_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="foot_L_ik_ctrl_world_grp")
        cmds.parent("foot_L_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)

        # parent cnst를 건다.

        cmds.select('foot_L_ik_ctrl_world_grp', r=1)
        cmds.select('pelvis_ctrl', tgl=1)
        cmds.select('foot_L_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='foot_L_ik_ctrl_cnst_grp_prntCnst')


        #ctrl에 연결한다.

        cmds.connectAttr('foot_L_ik_ctrl.worldPin', 'foot_L_ik_ctrl_cnst_grp_prntCnst.foot_L_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='foot_L_ik_ctrl_rvrs')
        cmds.connectAttr('foot_L_ik_ctrl.worldPin', 'foot_L_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('foot_L_ik_ctrl_rvrs.outputX', 'foot_L_ik_ctrl_cnst_grp_prntCnst.pelvis_ctrlW1', f=1)
        cmds.setAttr("foot_L_ik_ctrl.worldPin", 1)
        cmds.select(cl=1)


        #knee_L_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="knee_L_ctrl_cnst_grp")
        self.changeLoc("knee_L_ctrl", "knee_L_ctrl_cnst_grp")
        cmds.parent("knee_L_ctrl_cnst_grp", "knee_L_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("knee_L_ctrl", "knee_L_ctrl_cnst_grp")


        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('knee_L_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="knee_L_ctrl_world_grp")
        cmds.parent("knee_L_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        # parent cnst를 건다.
        cmds.select('knee_L_ctrl_world_grp', r=1)
        cmds.select('pelvis_ctrl', tgl=1)
        cmds.select('knee_L_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='knee_L_ctrl_cnst_grp_prntCnst')

        #ctrl에 연결한다.

        cmds.connectAttr('knee_L_ctrl.worldPin', 'knee_L_ctrl_cnst_grp_prntCnst.knee_L_ctrl_world_grpW0', f=1)
        cmds.connectAttr('knee_L_ctrl.worldPin', 'foot_L_ik_ctrl_rvrs.inputY', f=1)
        cmds.connectAttr('foot_L_ik_ctrl_rvrs.outputY', 'knee_L_ctrl_cnst_grp_prntCnst.pelvis_ctrlW1', f=1)
        cmds.setAttr("knee_L_ctrl.worldPin", 1)
        cmds.select(cl=1)

        ####################################
        #foot_R_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="foot_R_ik_ctrl_cnst_grp")
        self.changeLoc("foot_R_ik_ctrl", "foot_R_ik_ctrl_cnst_grp")
        cmds.parent("foot_R_ik_ctrl_cnst_grp", "foot_R_ik_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("foot_R_ik_ctrl_prnt_grp", "foot_R_ik_ctrl_cnst_grp")

        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('foot_R_ik_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="foot_R_ik_ctrl_world_grp")
        cmds.parent("foot_R_ik_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        # parent cnst를 건다.

        cmds.select('foot_R_ik_ctrl_world_grp', r=1)
        cmds.select('pelvis_ctrl', tgl=1)
        cmds.select('foot_R_ik_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='foot_R_ik_ctrl_cnst_grp_prntCnst')


        #ctrl에 연결한다.

        cmds.connectAttr('foot_R_ik_ctrl.worldPin', 'foot_R_ik_ctrl_cnst_grp_prntCnst.foot_R_ik_ctrl_world_grpW0', f=1)
        cmds.createNode('reverse', n='foot_R_ik_ctrl_rvrs')
        cmds.connectAttr('foot_R_ik_ctrl.worldPin', 'foot_R_ik_ctrl_rvrs.inputX', f=1)
        cmds.connectAttr('foot_R_ik_ctrl_rvrs.outputX', 'foot_R_ik_ctrl_cnst_grp_prntCnst.pelvis_ctrlW1', f=1)
        cmds.setAttr("foot_R_ik_ctrl.worldPin", 1)
        cmds.select(cl=1)

        #knee_R_ik_ctrl
        #cnst_grp를 하나 만들어서 ik_ctrl_prnt_grp 상위에 놓는다.

        cmds.group(em=1, n="knee_R_ctrl_cnst_grp")
        self.changeLoc("knee_R_ctrl", "knee_R_ctrl_cnst_grp")
        cmds.parent("knee_R_ctrl_cnst_grp", "knee_R_ctrl_preSet_grp")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.parent("knee_R_ctrl", "knee_R_ctrl_cnst_grp")


        #ik_ctrl에 속성을 하나 추가한다.
        cmds.select('knee_R_ctrl', r=1)
        cmds.addAttr(min=0, ln="worldPin", max=1, k=1, at='double', dv=0)

        #ik_ctrl의 월드 핀 그룹을 만든다.
        cmds.group(em=1, n="knee_R_ctrl_world_grp")
        cmds.parent("knee_R_ctrl_world_grp", "total_ctrl")
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        # parent cnst를 건다.
        cmds.select('knee_R_ctrl_world_grp', r=1)
        cmds.select('pelvis_ctrl', tgl=1)
        cmds.select('knee_R_ctrl_cnst_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='knee_R_ctrl_cnst_grp_prntCnst')


        #ctrl에 연결한다.

        cmds.connectAttr('knee_R_ctrl.worldPin', 'knee_R_ctrl_cnst_grp_prntCnst.knee_R_ctrl_world_grpW0', f=1)
        cmds.connectAttr('knee_R_ctrl.worldPin', 'foot_R_ik_ctrl_rvrs.inputY', f=1)
        cmds.connectAttr('foot_R_ik_ctrl_rvrs.outputY', 'knee_R_ctrl_cnst_grp_prntCnst.pelvis_ctrlW1', f=1)
        cmds.setAttr("knee_R_ctrl.worldPin", 1)
        cmds.select(cl=1)

        #####################################/
        #캐릭터 셋에 추가

        # character	-forceElement Aa4_arm_L 
        # 		hand_L_ik_ctrl.spine_shldrPin
        # 		hand_L_ik_ctrl.worldPin
        # 		elbow_L_ik_ctrl.worldPin; 
                
        # character	-forceElement Aa5_arm_R
        # 		hand_R_ik_ctrl.spine_shldrPin
        # 		hand_R_ik_ctrl.worldPin
        # 		elbow_R_ik_ctrl.worldPin; 

        # character	-forceElement Ab2_leg_L
        # 		foot_L_ik_ctrl.worldPin
        # 		knee_L_ctrl.worldPin; 

        # character	-forceElement Ab3_leg_R
        # 		foot_R_ik_ctrl.worldPin
        # 		knee_R_ctrl.worldPin; 






    #########################
    #Patch up 2014.03.31 끝

    ##############################/
    #전체 proc을 실행한다.


    ##############################/
    #필요한 기능펑션선언

    ##############################
    #$obj01의 위치로 $obj02의 위치를 맞추는 함수

    def changeLoc(self, obj01, obj02):

        pos01=cmds.xform(obj01, q=1, rotatePivot=1, ws=1, absolute=1)
        pos02=cmds.xform(obj02, q=1, rotatePivot=1, ws=1, absolute=1)
        tmpX01=pos01[0]
        tmpY01=pos01[1]
        tmpZ01=pos01[2]
        tmpX02=pos02[0]
        tmpY02=pos02[1]
        tmpZ02=pos02[2]
        tmpX=(tmpX01 - tmpX02)
        tmpY=(tmpY01 - tmpY02)
        tmpZ=(tmpZ01 - tmpZ02)
        cmds.move(tmpX, tmpY, tmpZ, obj02, r=1, ws=1, wd=1)


    def setEye(self):

        ################################
        #안구세팅시작

        #조인트를 보이게 하자.
        cmds.setAttr("eyeBall_L_ofs_jnt.visibility", 1)
        cmds.setAttr("eyeBall_R_ofs_jnt.visibility", 1)


        #각 ofs_jnt를 안구의 위치로 옮긴다.
        self.changeLoc("eye_L_loc", "eyeBall_L_ofs_jnt")
        self.changeLoc("eye_R_loc", "eyeBall_R_ofs_jnt")


        #안구의 스케일값과 회전값을 받아놓는다.
        eyeBall_L_sx=float(cmds.getAttr('eye_L_loc.sx'))
        eyeBall_L_sy=float(cmds.getAttr('eye_L_loc.sy'))
        eyeBall_L_sz=float(cmds.getAttr('eye_L_loc.sz'))
        eyeBall_L_rx=float(cmds.getAttr('eye_L_loc.rx'))
        eyeBall_L_ry=float(cmds.getAttr('eye_L_loc.ry'))
        eyeBall_L_rz=float(cmds.getAttr('eye_L_loc.rz'))
        eyeBall_R_sx=float(cmds.getAttr('eye_R_loc.sx'))
        eyeBall_R_sy=float(cmds.getAttr('eye_R_loc.sy'))
        eyeBall_R_sz=float(cmds.getAttr('eye_R_loc.sz'))
        eyeBall_R_rx=float(cmds.getAttr('eye_R_loc.rx'))
        eyeBall_R_ry=float(cmds.getAttr('eye_R_loc.ry'))
        eyeBall_R_rz=float(cmds.getAttr('eye_R_loc.rz'))

        #안구의 스케일과 회전값을 원래크기로 되돌린다.
        cmds.setAttr("eye_L_loc.scaleX", 1)
        cmds.setAttr("eye_L_loc.scaleY", 1)
        cmds.setAttr("eye_L_loc.scaleZ", 1)
        cmds.setAttr("eye_L_loc.rotateX", 0)
        cmds.setAttr("eye_L_loc.rotateY", 0)
        cmds.setAttr("eye_L_loc.rotateZ", 0)

        # 안구,동공1,동공2의 연결을 끊는다.
        cmds.disconnectAttr('eye_L_loc.translate', 'eyeBall_L.translate')
        cmds.disconnectAttr('eye_L_loc.rotate', 'eyeBall_L.rotate')
        cmds.disconnectAttr('eye_L_loc.scale', 'eyeBall_L.scale')
        cmds.disconnectAttr('eye_R_loc.translate', 'eyeBall_R.translate')
        cmds.disconnectAttr('eye_R_loc.rotate', 'eyeBall_R.rotate')
        cmds.disconnectAttr('eye_R_loc.scale', 'eyeBall_R.scale')
        cmds.disconnectAttr('eye_L_loc.translate', 'eyePupil01_L.translate')
        cmds.disconnectAttr('eye_L_loc.rotate', 'eyePupil01_L.rotate')
        cmds.disconnectAttr('eye_L_loc.scale', 'eyePupil01_L.scale')
        cmds.disconnectAttr('eye_R_loc.translate', 'eyePupil01_R.translate')
        cmds.disconnectAttr('eye_R_loc.rotate', 'eyePupil01_R.rotate')
        cmds.disconnectAttr('eye_R_loc.scale', 'eyePupil01_R.scale')
        cmds.disconnectAttr('eye_L_loc.translate', 'eyePupil02_L.translate')
        cmds.disconnectAttr('eye_L_loc.rotate', 'eyePupil02_L.rotate')
        cmds.disconnectAttr('eye_L_loc.scale', 'eyePupil02_L.scale')
        cmds.disconnectAttr('eye_R_loc.translate', 'eyePupil02_R.translate')
        cmds.disconnectAttr('eye_R_loc.rotate', 'eyePupil02_R.rotate')
        cmds.disconnectAttr('eye_R_loc.scale', 'eyePupil02_R.scale')


        #눈 컨트롤의 연결을 끊는다.
        cmds.disconnectAttr('eye_L_loc.translateY', 'eye_ctrl.translateY')
        cmds.disconnectAttr('eye_L_loc.translateZ', 'eye_ctrl.translateZ')

        #loc과 대칭노드를 지운다.
        cmds.delete('mirror_mult', 'eye_L_loc', 'eye_R_loc')

        #안구를 freeze한다.
        #select -r eyeBall_L ;
        #select -tgl eyeBall_R ;
        #select -tgl eyePupil01_L ;
        #select -tgl eyePupil01_R ;
        #select -tgl eyePupil02_L ;
        #select -tgl eyePupil02_R ;
        #makeIdentity -apply true -t 1 -r 0 -s 0 -n 0;

        #select -r eyeBall_L ;
        #select -tgl eyePupil02_L ;
        #select -tgl eyePupil01_L ;
        #select -tgl eyeReflect_L ;
        #select -tgl eyeBall_R ;
        #select -tgl eyePupil02_R ;
        #select -tgl eyePupil01_R ;
        #select -tgl eyeReflect_R ;
        #doBakeNonDefHistory( 1, {"prePost" });

        #select -cl;


        #안구조인트와 안구를 스킨한다.


        cmds.select('eyeBall_L_jnt', r=1)
        cmds.select('eyeBall_L', add=1)
        cmds.skinCluster(mi=5, n='eyeBall_L_skin', dr=4, tsb=1)
        cmds.select('eyeBall_L_jnt', r=1)
        cmds.select('eyePupil01_L', add=1)
        cmds.skinCluster(mi=5, n='eyePupil01_L_skin', dr=4, tsb=1)
        cmds.select('eyeBall_L_jnt', r=1)
        cmds.select('eyePupil02_L', add=1)
        cmds.skinCluster(mi=5, n='eyePupil02_L_skin', dr=4, tsb=1)
        cmds.select('eyeBall_R_jnt', r=1)
        cmds.select('eyeBall_R', add=1)
        cmds.skinCluster(mi=5, n='eyeBall_R_skin', dr=4, tsb=1)
        cmds.select('eyeBall_R_jnt', r=1)
        cmds.select('eyePupil01_R', add=1)
        cmds.skinCluster(mi=5, n='eyePupil01_R_skin', dr=4, tsb=1)
        cmds.select('eyeBall_R_jnt', r=1)
        cmds.select('eyePupil02_R', add=1)
        cmds.skinCluster(mi=5, n='eyePupil02_R_skin', dr=4, tsb=1)
        cmds.select(cl=1)


        #ofs_jnt의 스케일과 회전값을 처음 안구의 스케일 값으로 고친다.
        cmds.setAttr("eyeBall_L_scale_grp.sx", eyeBall_L_sx)
        cmds.setAttr("eyeBall_L_scale_grp.sy", eyeBall_L_sy)
        cmds.setAttr("eyeBall_L_scale_grp.sz", eyeBall_L_sz)
        cmds.setAttr("eyeBall_L_scale_grp.rx", eyeBall_L_rx)
        cmds.setAttr("eyeBall_L_scale_grp.ry", eyeBall_L_ry)
        cmds.setAttr("eyeBall_L_scale_grp.rz", eyeBall_L_rz)
        cmds.setAttr("eyeBall_R_scale_grp.sx", eyeBall_R_sx)
        cmds.setAttr("eyeBall_R_scale_grp.sy", eyeBall_R_sy)
        cmds.setAttr("eyeBall_R_scale_grp.sz", eyeBall_R_sz)
        cmds.setAttr("eyeBall_R_scale_grp.rx", eyeBall_R_rx)
        cmds.setAttr("eyeBall_R_scale_grp.ry", eyeBall_R_ry)
        cmds.setAttr("eyeBall_R_scale_grp.rz", eyeBall_R_rz)


        #각 눈알 컨트롤을 눈알 조인트 위치로 이동.
        self.changeLoc("eyeBall_L_ofs_jnt", "eye_L_ctrl")
        self.changeLoc("eyeBall_R_ofs_jnt", "eye_R_ctrl")

        #눈알 컨트롤러를 높이비례 반절의 값으로 앞으로 이동.
        eye_ty=float(cmds.getAttr('eye_ctrl.ty'))
        eye_tz=float(cmds.getAttr('eye_ctrl.tz'))
        eyeFront=eye_ty * 0.5 + eye_tz
        cmds.setAttr("eye_ctrl.tz", eyeFront)
        cmds.select('eye_ctrl', r=1)
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)


        #각 눈알 컨트롤러와 눈알조인트를 aim컨스트시킨다.
        cmds.select('eye_L_ctrl', r=1)
        cmds.select('eyeBall_L_jnt', add=1)
        cmds.aimConstraint(weight=1, upVector=(0, 1, 0), mo=1, 
            worldUpObject='head_jnt01', 
            worldUpType="objectrotation", 
            n='eyeBall_L_jnt_aimCnst', 
            aimVector=(0, 0, 1), 
            worldUpVector=(0, 1, 0))
        cmds.select('eye_R_ctrl', r=1)
        cmds.select('eyeBall_R_jnt', add=1)
        cmds.aimConstraint(weight=1, upVector=(0, 1, 0), mo=1, 
            worldUpObject='head_jnt01', 
            worldUpType="objectrotation", 
            n='eyeBall_R_jnt_aimCnst', 
            aimVector=(0, 0, 1), 
            worldUpVector=(0, 1, 0))


        #눈알 컨트롤러의 상위그룹을 2개 만든다. 하나는 ofs용, 다른 하나는 eye_grp
        cmds.group(em=1, n='eye_ctrl_const_grp')
        cmds.xform(os=1, piv=(0, 0, 0))
        cmds.group(em=1, n='eye_grp')
        cmds.xform(os=1, piv=(0, 0, 0))
        cmds.parent('eye_ctrl', 'eye_ctrl_const_grp')
        cmds.parent('eye_ctrl_const_grp', 'eye_grp')
        cmds.select(cl=1)


        #눈알 조인트, cls_grp를 eye_grp에 넣는다.
        cmds.parent('eyeBall_L_ofs_jnt', 'eye_grp')
        cmds.parent('eyeBall_R_ofs_jnt', 'eye_grp')

        #parent pupil_cls_grp eye_grp ;

        #빈그룹 1개를 만든다. 눈의 positionPin용
        cmds.group(em=1, n='eye_worldRot_grp')
        cmds.xform(os=1, piv=(0, 0, 0))


        #위에서 만들어진 4개의 그룹과, 동공cls그룹을 해당하는 곳에 parent 시킨다.
        cmds.parent('eye_grp', 'head_ctrl')
        cmds.parent('eye_worldRot_grp', 'total_ctrl')


        #굳히기
        cmds.setAttr("eye_grp.tx", lock=True)
        cmds.setAttr("eye_grp.ty", lock=True)
        cmds.setAttr("eye_grp.tz", lock=True)
        cmds.setAttr("eye_grp.rx", lock=True)
        cmds.setAttr("eye_grp.ry", lock=True)
        cmds.setAttr("eye_grp.rz", lock=True)
        cmds.setAttr("eye_grp.sx", lock=True)
        cmds.setAttr("eye_grp.sy", lock=True)
        cmds.setAttr("eye_grp.sz", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.tx", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.tx", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.ty", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.ty", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.tz", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.tz", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.rx", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.rx", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.ry", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.ry", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.rz", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.rz", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.sx", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.sx", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.sy", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.sy", lock=True)
        cmds.setAttr("eyeBall_R_ofs_jnt.sz", lock=True)
        cmds.setAttr("eyeBall_L_ofs_jnt.sz", lock=True)
        cmds.select('eye_worldRot_grp', r=1)
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)

        #positionPin을 위한 연결
        cmds.select('eye_worldRot_grp', r=1)
        cmds.select('head_ctrl', tgl=1)
        cmds.select('eye_ctrl_const_grp', add=1)
        cmds.parentConstraint(mo=1, weight=1, n='eye_ctrl_const_grp_prntCnst')
        cmds.createNode('reverse', n='eye_rvrs')
        cmds.connectAttr('eye_ctrl.positionPin', 'eye_rvrs.inputX', f=1)
        cmds.connectAttr('eye_ctrl.positionPin', 'eye_ctrl_const_grp_prntCnst.eye_worldRot_grpW0', f=1)
        cmds.connectAttr('eye_rvrs.outputX', 'eye_ctrl_const_grp_prntCnst.head_ctrlW1', f=1)

        #정리
        #오브젝트 정리해서 그룹안에 정리

        cmds.group(em=1, n='eyeBall_obj_grp')
        cmds.xform(os=1, piv=(0, 0, 0))
        cmds.parent('eyeBall_L', 'eyePupil01_L', 'eyePupil02_L', 'eyeBall_R', 'eyePupil01_R', 'eyePupil02_R', 'eyeBall_obj_grp')



        #eye_UI 제거
        cmds.delete('eye_L_UI_grp_pre')
        cmds.delete('eye_R_UI_grp_pre')
        cmds.delete('eye_grp_pre')


        #컨트롤러 채널 정리
        cmds.setAttr("eye_ctrl.visibility", 1)
        cmds.setAttr("eye_ctrl.sx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_ctrl.sy", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_ctrl.sz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_ctrl.v", lock=True, channelBox=False, keyable=False)
        #setAttr -lock true -keyable false -channelBox false "eye_ctrl.pupilAdd01";
        #setAttr -lock true -keyable false -channelBox false "eye_ctrl.pupilAdd02";

        cmds.setAttr("eye_R_ctrl.rx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.rx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.ry", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.ry", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.rz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.rz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.sx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.sx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.sy", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.sy", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.sz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.sz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_R_ctrl.v", lock=True, channelBox=False, keyable=False)
        cmds.setAttr("eye_L_ctrl.v", lock=True, channelBox=False, keyable=False)
        cmds.setAttr('eye_ctrl.rotateOrder', 2)

        # #캐릭셋에 추가.
        # select -cl;
        # character	-forceElement Aa1_eye 
        # 		eye_ctrl
        # 		eye_L_ctrl
        # 		eye_R_ctrl
        # 		;


        ############################################/
        #caharacter default pose 만들기

        # delete "defalut_pose"; #기존 포즈 제거

        # pose -name "defalut_pose" "keySet";

        #eye_set에 추가
        cmds.sets('eye_ctrl', 'eye_L_ctrl', 'eye_R_ctrl', edit=1, forceElement='eye_ctrl_set')

        #ctrl_layer 에 추가
        cmds.editDisplayLayerMembers('body_ctrl_layer', 'eye_ctrl', 'eye_L_ctrl', 'eye_R_ctrl', noRecurse=1)


