from maya import cmds

# 作成ウィンドウ
def textfieldtest(*arg):
    name = cmds.textField('namelog', q=True, text=True)
    width = cmds.textField('widthlog', q=True, text=True)
    height = cmds.textField('heightlog', q=True, text=True)
    depth = cmds.textField('depthlog', q=True, text=True)
    subdivisionsX = cmds.textField('sxlog', q=True, text=True)
    subdivisionsY = cmds.textField('sylog', q=True, text=True)
    subdivisionsZ = cmds.textField('szlog', q=True, text=True)
    cmds.polyCube(n=name,d=depth,w=width,h=height,sx=int(subdivisionsX),sy=int(subdivisionsY),sz=int(subdivisionsZ))
    if cmds.checkBox('MeshHeight',q=True,value=True):
        cmds.move(0,int(height)/2,0)

# ウィンドウ作成
def cube():
    cmds.window(title='Cube', mnb=False, mxb=False)
    cmds.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,150),(2,150),(3,150),(4,150),(5,150),(6,150),(7,150)])
    cmds.text(label="名前")
    cmds.textField('namelog',text="pCube")
    cmds.text(label="幅")
    cmds.textField('widthlog',text="1")
    cmds.text(label="高さ")
    cmds.textField('heightlog',text="1")
    cmds.text(label="深度")
    cmds.textField('depthlog',text="1")
    cmds.text(label="幅の分割数")
    cmds.textField('sxlog',text="1")
    cmds.text(label="高さの分割数")
    cmds.textField('sylog',text="1")
    cmds.text(label="深度の分割数")
    cmds.textField('szlog',text="1")
    cmds.text(label="0に合わせる")
    cmds.checkBox('MeshHeight')
    cmds.button('button',label='button',command=textfieldtest)
    cmds.showWindow()
    
cube()
