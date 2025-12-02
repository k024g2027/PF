import maya.cmds as cmds
import os
import json
import maya.api.OpenMaya as om

#実行時IKとFKを切り替え ON/True OFF/False 
change = True

#Locatorないとき
Loc = True

#ロック
rock = False

# JSON読み込み
project_root = cmds.workspace(query=True, rootDirectory=True)
scripts_dir = os.path.join(project_root, "scripts")
save_path = os.path.join(scripts_dir, "joint_map.json")
with open(save_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# controller_mapからコントローラ情報を取得
def get_controller_info(ctrl_name):
    return data.get("controller_map", {}).get(ctrl_name)

# PVの位置合わせ
def PV_Loc(d):
    saved_transforms = {}
    controllers = ["IK_Ctrl", "PV_Ctrl", "FK_top_Ctrl", "FK_mid_Ctrl", "FK_low_Ctrl", "Scapula", "Chest", "Spine", "Root"]

    #現在の値の保存,初期値へのリセット
    for ctrl in controllers:
        if ctrl in d:
            pos = cmds.xform(d[ctrl], q=True, os=True, t=True)
            rot = cmds.xform(d[ctrl], q=True, os=True, ro=True)
            saved_transforms[ctrl] = {"pos": pos, "rot": rot}
                
            if ctrl == "IK_Ctrl" or ctrl == "Scapula" or ctrl == "Chest" or ctrl == "Spine" or ctrl == "Root":
                cmds.setAttr(d[ctrl] + ".translate", 0, 0, 0)
                cmds.setAttr(d[ctrl] + ".rotate", 0, 0, 0)
                
            elif ctrl == "PV_Ctrl":
                cmds.setAttr(d[ctrl] + ".translate", 0, 0, 0)
                
            else:
                if ctrl == "FK_mid_Ctrl":
                    if abs(rot[0]) > 0.001 or abs(rot[1]) > 0.001:  # 0.001誤差許容範囲
                        error_msg = f"Error: {d['FK_mid_Ctrl']} の回転X,Yが0ではないため、正常にPVの移動が行われていない可能性があります"
                        cmds.warning(error_msg)
                    
                    if rock:
                        cmds.setAttr(d["FK_mid_Ctrl"] + ".rx", lock=False)
                        cmds.setAttr(d["FK_mid_Ctrl"] + ".ry", lock=False)
                    
                cmds.setAttr(d[ctrl] + ".rotate", 0, 0, 0)

    #PVにロケーター配置,FK_elbowへコンストレイント
    tmpLo = cmds.spaceLocator(n="tmpLo")[0]
    tmpLoGrp = cmds.group(tmpLo, n="tmpLoGrp")
    cmds.matchTransform(tmpLoGrp, d["FK_mid_Ctrl"], pos=True, rot=True, scl=False, piv=False)
    tmpLo1 = cmds.spaceLocator(n="tmpLo1")[0]
    tmpLoGrp1 = cmds.group(tmpLo1, n="tmpLoGrp1")
    cmds.matchTransform(tmpLoGrp1, d["PV_Space"], pos=True, rot=True, scl=False, piv=False)
    cmds.parent("tmpLoGrp1", tmpLo)
    cmds.parentConstraint(d["FK_mid_Ctrl"], tmpLo, mo=True, name="temp_PV_constraint")

    #位置の復元
    for ctrl, trans in saved_transforms.items():
        if ctrl == "IK_Ctrl" or ctrl == "Scapula" or ctrl == "Chest" or ctrl == "Spine" or ctrl == "Root":
            cmds.setAttr(d[ctrl] + ".rotate", *trans["rot"])
            cmds.setAttr(d[ctrl] + ".translate", *trans["pos"])
            
        elif ctrl == "PV_Ctrl":
            cmds.setAttr(d[ctrl] + ".translate", *trans["pos"])
            
        else:
            cmds.setAttr(d[ctrl] + ".rotate", *trans["rot"])
            if ctrl == "FK_mid_Ctrl" and rock:
               cmds.setAttr(d["FK_mid_Ctrl"] + ".rx", lock=True)
               cmds.setAttr(d["FK_mid_Ctrl"] + ".ry", lock=True)

    #PVの位置合わせ
    cmds.matchTransform(d["PV_Ctrl"], tmpLo1, pos=True, rot=True, scl=False, piv=False)
    cmds.delete("temp_PV_constraint")
    cmds.delete("tmpLoGrp")

# IK→FK変換
def IKtoFK_for_limb(d):
    try:
        upper_rot = cmds.xform(d["IK_top_jnt"], os=True, ro=True, q=True)
        cmds.xform(d["FK_top_Ctrl"], os=True, ro=upper_rot)
        elbow_rot = cmds.xform(d["IK_mid_jnt"], os=True, ro=True, q=True)
        cmds.xform(d["FK_mid_Ctrl"], os=True, ro=elbow_rot)

        if d["limb"] == "hand" and d.get("FK_low_Ctrl") and d.get("IK_low_jnt"):
            cmds.matchTransform(d["FK_low_Ctrl"], d["IK_low_jnt"], pos=False, rot=True, scl=False, piv=False)
        if d["limb"] == "foot" and d.get("FK_low_Ctrl") and d.get("IK_low_jnt"):
            tmpLo = cmds.spaceLocator(n="tmpLo")[0]
            cmds.matchTransform(tmpLo, d["IK_low_jnt"], pos=True, rot=True, scl=False, piv=False)
            cmds.matchTransform(d["FK_low_Ctrl"], tmpLo, pos=False, rot=True, scl=False, piv=False)
            cmds.delete("tmpLo")
            ball_rot = cmds.xform(d["IK_low_Ctrl"], os=True, ro=True, q=True)
            cmds.rotate(ball_rot[0], ball_rot[1], ball_rot[2], d["FK_toe_Ctrl"], os=True)
        if change:
            cmds.setAttr(d["Switch"] + "." + d["Blend"], int(d["value"]))
        return True

    except Exception as e:
        print(f"IKtoFK_for_limbエラー: {e}")
        return False

# FK→IK変換
def FKtoIK_for_hand(d):
    try:
        if Loc:
            PV_Loc(d)
            
        cmds.matchTransform(d["IK_Ctrl"], d["FK_jnt"], pos=True, rot=True, scl=True, piv=False)
        
        if Loc == False:
            tmp_pos = cmds.xform(d["PV_Loc"], ws=True, t=True, q=True)
            tmp_rot = cmds.xform(d["PV_Loc"], ws=True, ro=True, q=True)
            cmds.move(tmp_pos[0], tmp_pos[1], tmp_pos[2], d["PV_Ctrl"], rotatePivotRelative=True, ws=True)
            cmds.rotate(tmp_rot[0], tmp_rot[1], tmp_rot[2], d["PV_Ctrl"], ws=True)
        if change:
            cmds.setAttr(d["Switch"] + "." + d["Blend"], int(d["value"]))
        return True

    except Exception as e:
        print(f"FKtoIK_for_handエラー: {e}")
        return False
        
def FKtoIK_for_foot(d):
    try:
        cmds.matchTransform(d["IK_Ctrl"], d["FK_jnt_Space"], pos=True, rot=True, scl=True, piv=False)
        ball_rot = cmds.xform(d["FK_toe_Ctrl"], os=True, ro=True, q=True)
        cmds.rotate(ball_rot[0], ball_rot[1], ball_rot[2], d["IK_low_Ctrl"], os=True)
            
        if Loc == False:
            tmp_pos = cmds.xform(d["PV_Loc"], ws=True, t=True, q=True)
            tmp_rot = cmds.xform(d["PV_Loc"], ws=True, ro=True, q=True)
            cmds.move(tmp_pos[0], tmp_pos[1], tmp_pos[2], d["PV_Ctrl"], rotatePivotRelative=True, ws=True)
            cmds.rotate(tmp_rot[0], tmp_rot[1], tmp_rot[2], d["PV_Ctrl"], ws=True)
        if change:
            cmds.setAttr(d["Switch"] + "." + d["Blend"], int(d["value"]))
        return True

    except Exception as e:
        print(f"FKtoIK_for_footエラー: {e}")
        return False

# 実行
selection = cmds.ls(sl=True)
if not selection:
    print("コントローラを選択してください")
else:
    for sel in selection:
        d = get_controller_info(sel)
        if not d:
            print(f"{sel}はcontroller_mapに登録されていません")
            continue
        mode = d.get("mode")
        if mode == "IK":
            IKtoFK_for_limb(d)
        elif mode == "FK":
            if d["limb"] == "hand":
                FKtoIK_for_hand(d)
            elif d["limb"] == "foot":
                FKtoIK_for_foot(d)
            else :

                print("判別不可")
