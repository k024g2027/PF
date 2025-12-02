import maya.cmds as cmds # type: ignore

mesh_transforms = cmds.listRelatives(cmds.ls(type="mesh"), parent=True, fullPath=True) or []

freeze_errors = []
pivot_errors = []

for obj in mesh_transforms:
    t = cmds.xform(obj, q=True, ws=True, t=True)
    r = cmds.xform(obj, q=True, ws=True, ro=True)
    s = cmds.xform(obj, q=True, r=True, s=True)

    Ft = 1 if all(abs(val) < 1e-6 for val in t) else 0
    Fr = 1 if all(abs(val) < 1e-6 for val in r) else 0
    Fs = 1 if all(abs(val-1.0) < 1e-6 for val in s) else 0

    pivot = cmds.xform(obj, q=True, piv=True, ws=False)
    rotate_pivot = pivot[:3]
    scale_pivot = pivot[3:]
    Pc = 1 if all(abs(val) < 1e-6 for val in rotate_pivot) and all(abs(val) < 1e-6 for val in scale_pivot) else 0

    if not (Ft and Fr and Fs):
        freeze_errors.append(obj)
    if not Pc:
        pivot_errors.append(obj)

msg = ""
if freeze_errors:
    msg += u"フリーズがされていないオブジェクト:\n" + "\n".join(freeze_errors) + "\n\n"
if pivot_errors:
    msg += u"ピボットが原点にないオブジェクト:\n" + "\n".join(pivot_errors) + "\n\n"

if pivot_errors:
    msg_fix = u"ピボットが原点にないオブジェクトがあります。\n\n" + "\n".join(pivot_errors) + u"\n\nこれらのピボットを原点に移動しますか？"
    result = cmds.confirmDialog(
        title='ピボット修正',
        message=msg_fix,
        button=['適用', 'キャンセル'],
        defaultButton='適用',
        cancelButton='キャンセル',
        dismissString='キャンセル',
        icon='critical'
    )
    if result == '適用':
        for obj in pivot_errors:
            cmds.setAttr(obj + '.scalePivot', 0, 0, 0)
            cmds.setAttr(obj + '.rotatePivot', 0, 0, 0)
        cmds.confirmDialog(title='ピボット修正完了', message=u'ピボットを原点に移動しました。', button=['OK'], icon='information')

elif msg:
    cmds.confirmDialog(title='チェック結果', message=msg, button=['OK'], icon='critical')
else:

    cmds.confirmDialog(title='チェック結果', message=u'ピボットチェックOK！', button=['OK'], icon='information')
