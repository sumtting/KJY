import maya.cmds as cmds


body_CTL_list = [u'root_FK_M_CTL', u'middleFinger_01_R_CTL', u'middleFinger_04_R_CTL', u'middleFinger_03_R_CTL', u'ringFinger_01_R_CTL', u'ringFinger_04_R_CTL', u'ringFinger_03_R_CTL', u'ringFinger_02_R_CTL', u'bend_knee_L_CTL', u'leg_IK_pole_R_CTL', u'leg_IKFK_switch_R_CTL', u'legMid_R_CTL', u'ankle_IK_R_CTL', u'hipSwing_M_CTL', u'rootMain_M_CTL', u'scale_spine_03_M_CTL', u'scale_spine_02_M_CTL', u'scale_spine_04_M_CTL', u'scale_shoulder_R_CTL', u'scale_elbow_R_CTL', u'scale_wrist_R_CTL', u'scale_elbow_L_CTL', u'scale_shoulder_L_CTL', u'scale_wrist_L_CTL', u'scale_leg_R_CTL', u'scale_knee_R_CTL', u'scale_ankle_R_CTL', u'scale_leg_L_CTL', u'wrist_FK_L_CTL', u'elbow_FK_L_CTL', u'shoulder_FK_L_CTL', u'scapula_FK_L_CTL', u'shoulder_IKFK_switch_L_CTL', u'shoulder_IK_pole_L_CTL', u'armMid_L_CTL', u'armMid_R_CTL', u'shoulder_IK_pole_R_CTL', u'wrist_IK_R_CTL', u'middleFinger_01_L_CTL', u'middleFinger_04_L_CTL', u'middleFinger_03_L_CTL', u'ringFinger_02_L_CTL', u'ringFinger_01_L_CTL', u'ringFinger_04_L_CTL', u'ringFinger_03_L_CTL', u'toes_IK_R_CTL', u'ankleSub_IK_R_CTL', u'toeBall_IK_L_CTL', u'toeTip_L_CTL', u'leg_IK_pole_L_CTL', u'leg_IKFK_switch_L_CTL', u'legMid_L_CTL', u'ankle_IK_L_CTL', u'pinkyFinger_04_R_CTL', u'pinkyFinger_03_R_CTL', u'pinkyFinger_02_R_CTL', u'pinkyFinger_01_R_CTL', u'weapon_R_CTL', u'thumbFinger_01_L_CTL', u'wristSub_FK_L_CTL', u'fingers_R_CTL', u'thumbFinger_02_L_CTL', u'pinkyFinger_01_L_CTL', u'pinkyFinger_04_L_CTL', u'pinkyFinger_03_L_CTL', u'pinkyFinger_02_L_CTL', u'weapon_L_CTL', u'fingers_L_CTL', u'toeBall_IK_R_CTL', u'toeTip_R_CTL', u'wrist_IK_L_CTL', u'wrist_FK_R_CTL', u'elbow_FK_R_CTL', u'shoulder_FK_R_CTL', u'scapula_FK_R_CTL', u'shoulder_IKFK_switch_R_CTL', u'bend_shoulder_R_CTL', u'bend_elbow_R_CTL', u'bend_shoulder_L_CTL', u'thumbFinger_01_R_CTL', u'wristSub_FK_R_CTL', u'bend_elbow_L_CTL', u'neck_M_CTL', u'spine_FK_04_M_CTL', u'spine_FK_03_M_CTL', u'neckSub_M_CTL', u'head_M_CTL', u'thumbFinger_03_R_CTL', u'thumbFinger_02_R_CTL', u'indexFinger_02_R_CTL', u'indexFinger_01_R_CTL', u'indexFinger_04_R_CTL', u'indexFinger_03_R_CTL', u'middleFinger_02_R_CTL', u'toes_IK_L_CTL', u'ankleSub_IK_L_CTL', u'indexFinger_02_L_CTL', u'thumbFinger_03_L_CTL', u'indexFinger_03_L_CTL', u'indexFinger_01_L_CTL', u'indexFinger_04_L_CTL', u'middleFinger_02_L_CTL', u'spine_IK_MU_CTL', u'spine_IK_MM_CTL', u'spine_IK_MD_CTL', u'pelvis_FK_R_CTL', u'scale_knee_L_CTL', u'scale_ankle_L_CTL', u'scale_root_M_CTL', u'scale_spine_01_M_CTL', u'pelvis_FK_L_CTL', u'ankle_FK_L_CTL', u'knee_FK_L_CTL', u'leg_FK_L_CTL', u'toes_FK_L_CTL', u'toeBall_FK_L_CTL', u'toeTip_FK_L_CTL', u'knee_FK_R_CTL', u'leg_FK_R_CTL', u'ankle_FK_R_CTL', u'toes_FK_R_CTL', u'toeBall_FK_R_CTL', u'toeTip_FK_R_CTL', u'sky_M_CTL', u'world_M_CTL', u'main_M_CTL', u'spine_FK_01_M_CTL', u'spine_FK_02_M_CTL', u'bend_leg_R_CTL', u'bend_knee_R_CTL', u'bend_leg_L_CTL']
# body의 모든 컨트롤러 리스트



keyable_dic_list =[]

for body_CTL in body_CTL_list:
  
    
    attr = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트를 한세트씩 추출

    for i in attr:
        body_CTL_keyable = '%s' %(body_CTL + '.' + i) 
        # 해당컨트롤러에 keyable상태인 어트리뷰트들을
        # 'root_FK_M_CTL.rotateZ' 와 같은식의 형태로 바꿔준다(문자열) 
    
        keyable_value = cmds.getAttr(body_CTL_keyable) #위에서 만든 body_CTL_keyable을 넣어서 해당 밸류값을 추출
        keyable_dic = {body_CTL_keyable:keyable_value} # 컨트롤러의 keyable어트리뷰트 : 어트리뷰트 밸류값
        keyable_dic_list.append(keyable_dic)
print keyable_dic_list






















import maya.cmds as cmds

body_CTL_list = [u'root_FK_M_CTL', u'middleFinger_01_R_CTL', u'middleFinger_04_R_CTL', u'middleFinger_03_R_CTL', u'ringFinger_01_R_CTL', u'ringFinger_04_R_CTL', u'ringFinger_03_R_CTL', u'ringFinger_02_R_CTL', u'bend_knee_L_CTL', u'leg_IK_pole_R_CTL', u'leg_IKFK_switch_R_CTL', u'legMid_R_CTL', u'ankle_IK_R_CTL', u'hipSwing_M_CTL', u'rootMain_M_CTL', u'scale_spine_03_M_CTL', u'scale_spine_02_M_CTL', u'scale_spine_04_M_CTL', u'scale_shoulder_R_CTL', u'scale_elbow_R_CTL', u'scale_wrist_R_CTL', u'scale_elbow_L_CTL', u'scale_shoulder_L_CTL', u'scale_wrist_L_CTL', u'scale_leg_R_CTL', u'scale_knee_R_CTL', u'scale_ankle_R_CTL', u'scale_leg_L_CTL', u'wrist_FK_L_CTL', u'elbow_FK_L_CTL', u'shoulder_FK_L_CTL', u'scapula_FK_L_CTL', u'shoulder_IKFK_switch_L_CTL', u'shoulder_IK_pole_L_CTL', u'armMid_L_CTL', u'armMid_R_CTL', u'shoulder_IK_pole_R_CTL', u'wrist_IK_R_CTL', u'middleFinger_01_L_CTL', u'middleFinger_04_L_CTL', u'middleFinger_03_L_CTL', u'ringFinger_02_L_CTL', u'ringFinger_01_L_CTL', u'ringFinger_04_L_CTL', u'ringFinger_03_L_CTL', u'toes_IK_R_CTL', u'ankleSub_IK_R_CTL', u'toeBall_IK_L_CTL', u'toeTip_L_CTL', u'leg_IK_pole_L_CTL', u'leg_IKFK_switch_L_CTL', u'legMid_L_CTL', u'ankle_IK_L_CTL', u'pinkyFinger_04_R_CTL', u'pinkyFinger_03_R_CTL', u'pinkyFinger_02_R_CTL', u'pinkyFinger_01_R_CTL', u'weapon_R_CTL', u'thumbFinger_01_L_CTL', u'wristSub_FK_L_CTL', u'fingers_R_CTL', u'thumbFinger_02_L_CTL', u'pinkyFinger_01_L_CTL', u'pinkyFinger_04_L_CTL', u'pinkyFinger_03_L_CTL', u'pinkyFinger_02_L_CTL', u'weapon_L_CTL', u'fingers_L_CTL', u'toeBall_IK_R_CTL', u'toeTip_R_CTL', u'wrist_IK_L_CTL', u'wrist_FK_R_CTL', u'elbow_FK_R_CTL', u'shoulder_FK_R_CTL', u'scapula_FK_R_CTL', u'shoulder_IKFK_switch_R_CTL', u'bend_shoulder_R_CTL', u'bend_elbow_R_CTL', u'bend_shoulder_L_CTL', u'thumbFinger_01_R_CTL', u'wristSub_FK_R_CTL', u'bend_elbow_L_CTL', u'neck_M_CTL', u'spine_FK_04_M_CTL', u'spine_FK_03_M_CTL', u'neckSub_M_CTL', u'head_M_CTL', u'thumbFinger_03_R_CTL', u'thumbFinger_02_R_CTL', u'indexFinger_02_R_CTL', u'indexFinger_01_R_CTL', u'indexFinger_04_R_CTL', u'indexFinger_03_R_CTL', u'middleFinger_02_R_CTL', u'toes_IK_L_CTL', u'ankleSub_IK_L_CTL', u'indexFinger_02_L_CTL', u'thumbFinger_03_L_CTL', u'indexFinger_03_L_CTL', u'indexFinger_01_L_CTL', u'indexFinger_04_L_CTL', u'middleFinger_02_L_CTL', u'spine_IK_MU_CTL', u'spine_IK_MM_CTL', u'spine_IK_MD_CTL', u'pelvis_FK_R_CTL', u'scale_knee_L_CTL', u'scale_ankle_L_CTL', u'scale_root_M_CTL', u'scale_spine_01_M_CTL', u'pelvis_FK_L_CTL', u'ankle_FK_L_CTL', u'knee_FK_L_CTL', u'leg_FK_L_CTL', u'toes_FK_L_CTL', u'toeBall_FK_L_CTL', u'toeTip_FK_L_CTL', u'knee_FK_R_CTL', u'leg_FK_R_CTL', u'ankle_FK_R_CTL', u'toes_FK_R_CTL', u'toeBall_FK_R_CTL', u'toeTip_FK_R_CTL', u'sky_M_CTL', u'world_M_CTL', u'main_M_CTL', u'spine_FK_01_M_CTL', u'spine_FK_02_M_CTL', u'bend_leg_R_CTL', u'bend_knee_R_CTL', u'bend_leg_L_CTL']
# body의 모든 컨트롤러 리스트



for body_CTL in body_CTL_list:
    attrs = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트를 한세트씩 추출

        
    for attr in attrs:
        body_CTL_keyable = '%s' %(body_CTL + '.' + attr) 
        get_frames = cmds.keyframe( body_CTL_keyable, query=True, absolute=True )
        get_values = cmds.keyframe( body_CTL_keyable, time=(0,200), query=True, valueChange=True)
       # print body_CTL_keyable
      #  print get_frames
      #  print get_values
        dic = {body_CTL:
            
            {
            "Attribute":body_CTL_keyable,
            "frame":get_frames,
            "Value":get_values
            }
            }
  
        print dic            
        dic_list.append(dic)
           















import maya.cmds as cmds

body_CTL_list = [u'root_FK_M_CTL', u'middleFinger_01_R_CTL', u'middleFinger_04_R_CTL', u'middleFinger_03_R_CTL', u'ringFinger_01_R_CTL', u'ringFinger_04_R_CTL', u'ringFinger_03_R_CTL', u'ringFinger_02_R_CTL', u'bend_knee_L_CTL', u'leg_IK_pole_R_CTL', u'leg_IKFK_switch_R_CTL', u'legMid_R_CTL', u'ankle_IK_R_CTL', u'hipSwing_M_CTL', u'rootMain_M_CTL', u'scale_spine_03_M_CTL', u'scale_spine_02_M_CTL', u'scale_spine_04_M_CTL', u'scale_shoulder_R_CTL', u'scale_elbow_R_CTL', u'scale_wrist_R_CTL', u'scale_elbow_L_CTL', u'scale_shoulder_L_CTL', u'scale_wrist_L_CTL', u'scale_leg_R_CTL', u'scale_knee_R_CTL', u'scale_ankle_R_CTL', u'scale_leg_L_CTL', u'wrist_FK_L_CTL', u'elbow_FK_L_CTL', u'shoulder_FK_L_CTL', u'scapula_FK_L_CTL', u'shoulder_IKFK_switch_L_CTL', u'shoulder_IK_pole_L_CTL', u'armMid_L_CTL', u'armMid_R_CTL', u'shoulder_IK_pole_R_CTL', u'wrist_IK_R_CTL', u'middleFinger_01_L_CTL', u'middleFinger_04_L_CTL', u'middleFinger_03_L_CTL', u'ringFinger_02_L_CTL', u'ringFinger_01_L_CTL', u'ringFinger_04_L_CTL', u'ringFinger_03_L_CTL', u'toes_IK_R_CTL', u'ankleSub_IK_R_CTL', u'toeBall_IK_L_CTL', u'toeTip_L_CTL', u'leg_IK_pole_L_CTL', u'leg_IKFK_switch_L_CTL', u'legMid_L_CTL', u'ankle_IK_L_CTL', u'pinkyFinger_04_R_CTL', u'pinkyFinger_03_R_CTL', u'pinkyFinger_02_R_CTL', u'pinkyFinger_01_R_CTL', u'weapon_R_CTL', u'thumbFinger_01_L_CTL', u'wristSub_FK_L_CTL', u'fingers_R_CTL', u'thumbFinger_02_L_CTL', u'pinkyFinger_01_L_CTL', u'pinkyFinger_04_L_CTL', u'pinkyFinger_03_L_CTL', u'pinkyFinger_02_L_CTL', u'weapon_L_CTL', u'fingers_L_CTL', u'toeBall_IK_R_CTL', u'toeTip_R_CTL', u'wrist_IK_L_CTL', u'wrist_FK_R_CTL', u'elbow_FK_R_CTL', u'shoulder_FK_R_CTL', u'scapula_FK_R_CTL', u'shoulder_IKFK_switch_R_CTL', u'bend_shoulder_R_CTL', u'bend_elbow_R_CTL', u'bend_shoulder_L_CTL', u'thumbFinger_01_R_CTL', u'wristSub_FK_R_CTL', u'bend_elbow_L_CTL', u'neck_M_CTL', u'spine_FK_04_M_CTL', u'spine_FK_03_M_CTL', u'neckSub_M_CTL', u'head_M_CTL', u'thumbFinger_03_R_CTL', u'thumbFinger_02_R_CTL', u'indexFinger_02_R_CTL', u'indexFinger_01_R_CTL', u'indexFinger_04_R_CTL', u'indexFinger_03_R_CTL', u'middleFinger_02_R_CTL', u'toes_IK_L_CTL', u'ankleSub_IK_L_CTL', u'indexFinger_02_L_CTL', u'thumbFinger_03_L_CTL', u'indexFinger_03_L_CTL', u'indexFinger_01_L_CTL', u'indexFinger_04_L_CTL', u'middleFinger_02_L_CTL', u'spine_IK_MU_CTL', u'spine_IK_MM_CTL', u'spine_IK_MD_CTL', u'pelvis_FK_R_CTL', u'scale_knee_L_CTL', u'scale_ankle_L_CTL', u'scale_root_M_CTL', u'scale_spine_01_M_CTL', u'pelvis_FK_L_CTL', u'ankle_FK_L_CTL', u'knee_FK_L_CTL', u'leg_FK_L_CTL', u'toes_FK_L_CTL', u'toeBall_FK_L_CTL', u'toeTip_FK_L_CTL', u'knee_FK_R_CTL', u'leg_FK_R_CTL', u'ankle_FK_R_CTL', u'toes_FK_R_CTL', u'toeBall_FK_R_CTL', u'toeTip_FK_R_CTL', u'sky_M_CTL', u'world_M_CTL', u'main_M_CTL', u'spine_FK_01_M_CTL', u'spine_FK_02_M_CTL', u'bend_leg_R_CTL', u'bend_knee_R_CTL', u'bend_leg_L_CTL']
# body의 모든 컨트롤러 리스트

key_dic_list=[]
attrs_list=[]

for body_CTL in body_CTL_list:
    attrs = cmds.listAttr(body_CTL, k=1) # 컨트롤러마다 keyable상태인 어트리뷰트를 한세트씩 추출
    attrs_list.append(attrs)
        
    for keyable in attrs_list:
        for k in keyable:
            
            body_CTL_keyable = '%s' %(body_CTL + '.' + k) 
            get_frames = cmds.keyframe( body_CTL_keyable, query=True, absolute=True )
            get_values = cmds.keyframe( body_CTL_keyable, time=(0,200), query=True, valueChange=True)
       # print body_CTL_keyable
       #  print get_frames
       #  print get_values

 
            key_dic = {
            "Attribute":body_CTL_keyable,
            "frame":get_frames,
            "Value":get_values
            }
            
            print key_dic
            key_dic_list.append(key_dic)
        
        
    dic = {body_CTL:key_dic}
    print dic


           










