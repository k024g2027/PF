import maya.cmds as cmds # type: ignore

mesh_transforms = cmds.listRelatives(cmds.ls(type="mesh"), parent=True, fullPath=True) or []
curve_transforms = cmds.listRelatives(cmds.ls(type="nurbsCurve"), parent=True, fullPath=True) or []
check_targets = list(set(mesh_transforms + curve_transforms))

ng_objects = []

for obj in check_targets:
    t = cmds.xform(obj, q=True, ws=True, t=True)
    r = cmds.xform(obj, q=True, ws=True, ro=True)
    s = cmds.xform(obj, q=True, r=True, s=True)

    Ct = 1 if all(abs(val) < 1e-6 for val in t) else 0
    Cr = 1 if all(abs(val) < 1e-6 for val in r) else 0
    Cs = 1 if all(abs(val-1.0) < 1e-6 for val in s) else 0

    if not (Ct and Cr and Cs):
        ng_objects.append(obj)

if ng_objects:
    msg = u"フリーズがされていないオブジェクト:\n\n" + "\n".join(ng_objects) + u"\n\nこれらのオブジェクトにフリーズを適用しますか？"
    result = cmds.confirmDialog(
        title='チェック結果',
        message=msg,
        button=['適用', 'キャンセル'],
        defaultButton='適用',
        cancelButton='キャンセル',
        dismissString='キャンセル',
        icon='critical'
    )
    if result == '適用':
        cmds.select(ng_objects, replace=True)
        cmds.makeIdentity(
            apply=True,
            translate=True,
            rotate=True,
            scale=True,
            normal=False,
            preserveNormals=True,
            jointOrient=False
        )
        cmds.confirmDialog(title='フリーズ完了', message=u'フリーズを適用しました。', button=['OK'], icon='information')
else:
    cmds.confirmDialog(title='チェック結果', message=u'フリーズチェックOK！', button=['OK'], icon='information')