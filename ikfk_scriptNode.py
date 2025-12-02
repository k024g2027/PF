import maya.cmds as cmds

def fk_to_ik_snap():
    IK_Ctrl = "HandIK_Ctrl_L"
    FK_Jnt = "HandFK_Jnt_L"
    IK_Pov = "ElbowPV_Ctrl_L"
    FK_Loc = "ElbowPV_Loc_L"
    Loc_Pos = cmds.xform(FK_Loc, ws=True, t=True, q=True)
    Loc_Rot = cmds.xform(FK_Loc, ws=True, ro=True, q=True)
    cmds.matchTransform(IK_Ctrl, FK_Jnt, pos=True, rot=True, scl=True, piv=False)
    cmds.move(Loc_Pos[0], Loc_Pos[1], Loc_Pos[2], IK_Pov, ws=True)
    cmds.rotate(Loc_Rot[0], Loc_Rot[1], Loc_Rot[2], IK_Pov, ws=True)

def ik_to_fk_snap():
    IK_top_jnt = "ArmIK_Jnt_L"
    IK_mid_jnt = "ElbowIK_Jnt_L"
    IK_low_jnt = "HandIK_Jnt_L"
    FK_top_Ctrl = "ArmFK_Ctrl_L"
    FK_mid_Ctrl = "ElbowFK_Ctrl_L"
    FK_low_Ctrl = "HandFK_Ctrl_L"
    upper_rot = cmds.xform(IK_top_jnt, os=True, ro=True, q=True)
    elbow_rot = cmds.xform(IK_mid_jnt, os=True, ro=True, q=True)
    cmds.xform(FK_top_Ctrl, os=True, ro=upper_rot)
    cmds.xform(FK_mid_Ctrl, os=True, ro=elbow_rot)
    cmds.matchTransform(FK_low_Ctrl, IK_low_jnt, pos=False, rot=True, scl=False, piv=False)

def ikfkSwitchCallback():
    auto_switch = cmds.getAttr('HandSwitch_Ctrl_L.Auto_Switch')
    if auto_switch == 0:
        return
    
    ikfk_val = cmds.getAttr('HandSwitch_Ctrl_L.IKFK_Switch')
    if ikfk_val == 1:
        fk_to_ik_snap()
    elif ikfk_val == 0:
        ik_to_fk_snap()

# 古いscriptJobのクリーンアップ
jobs = cmds.scriptJob(listJobs=True)
for job in jobs:
    if 'HandSwitch_Ctrl_L.IKFK_Switch' in job:
        id = int(job.split(":")[0])
        cmds.scriptJob(kill=id, force=True)

# scriptJob登録
cmds.scriptJob(attributeChange=['HandSwitch_Ctrl_L.IKFK_Switch', 'ikfkSwitchCallback()'], protected=True)
