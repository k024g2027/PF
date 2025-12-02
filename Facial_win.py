from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)

class FloatSliderWidget(QtWidgets.QWidget):
    def __init__(self, label, min_value=0.0, max_value=1.0, step=0.01, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        self.label = QtWidgets.QLabel(label)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtWidgets.QDoubleSpinBox()

        # スライダーは整数値で管理
        self.slider.setMinimum(0)
        self.slider.setMaximum(int((max_value - min_value) / step))
        self.slider.setSingleStep(1)

        # スピンボックスは小数で管理
        self.spinbox.setDecimals(2)
        self.spinbox.setRange(min_value, max_value)
        self.spinbox.setSingleStep(step)

        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.spinbox)

        self.min_value = min_value
        self.max_value = max_value
        self.step = step

        # 双方向連動
        self.slider.valueChanged.connect(self.slider_to_spinbox)
        self.spinbox.valueChanged.connect(self.spinbox_to_slider)

    def slider_to_spinbox(self, v):
        value = self.min_value + v * self.step
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value)
        self.spinbox.blockSignals(False)

    def spinbox_to_slider(self, v):
        idx = int(round((v - self.min_value) / self.step))
        self.slider.blockSignals(True)
        self.slider.setValue(idx)
        self.slider.blockSignals(False)

    def set_value(self, v):
        self.spinbox.setValue(v)

    def value(self):
        return self.spinbox.value()

class AttrSliderUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AttrSliderUI, self).__init__(parent)
        self.setWindowTitle("Facial_Control")
        self.resize(440, 160)
        main_layout = QtWidgets.QHBoxLayout(self)

        # 左側：ボタン
        left_col = QtWidgets.QVBoxLayout()

        A = QtWidgets.QPushButton("A")
        I = QtWidgets.QPushButton("I")
        U = QtWidgets.QPushButton("U")
        E = QtWidgets.QPushButton("E")
        O = QtWidgets.QPushButton("O")
        EYE = QtWidgets.QPushButton("EYE")
        FACE = QtWidgets.QPushButton("FACE")
        EYEBROW = QtWidgets.QPushButton("EYEBROW")
        EYELASH = QtWidgets.QPushButton("EYELASH")
        MOUTH = QtWidgets.QPushButton("MOUTH")
        btn_reload = QtWidgets.QPushButton("再読み込み")
        
        left_col.addWidget(A)
        left_col.addWidget(I)
        left_col.addWidget(U)
        left_col.addWidget(E)
        left_col.addWidget(O)
        left_col.addWidget(EYE)
        left_col.addWidget(FACE)
        left_col.addWidget(EYEBROW)
        left_col.addWidget(EYELASH)
        left_col.addWidget(MOUTH)
        left_col.addWidget(btn_reload)

        left_col.addStretch()
        main_layout.addLayout(left_col)

        # 右側：表示エリア
        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout(self.right_widget)
        main_layout.addWidget(self.right_widget)

        A.clicked.connect(self.show_A_x)
        I.clicked.connect(self.show_I_x)
        U.clicked.connect(self.show_U_x)
        E.clicked.connect(self.show_E_x)
        O.clicked.connect(self.show_O_x)
        EYE.clicked.connect(self.show_EYE)
        FACE.clicked.connect(self.show_FACE)
        EYEBROW.clicked.connect(self.show_EYEBROW)
        EYELASH.clicked.connect(self.show_EYELASH)
        MOUTH.clicked.connect(self.show_MOUTH)
        btn_reload.clicked.connect(self.reload_volumes)

        # スライダー参照用
        self.A_slider = None
        self.I_slider = None
        self.U_slider = None
        self.E_slider = None
        self.O_slider = None
        
        self.eyeClose_slider = None
        self.eyeSmall_slider = None
        
        self.ONE_MOUTH_slider = None
        self.TWO_FACE_slider = None
        self.THREE_MOUTH_slider = None
        self.FOUR_FACE_slider = None
        self.FIVE_MOUTH_slider = None
        self.SIX_MOUTH_slider = None
        self.SEVEN_MOUTH_slider = None
        self.SEVEN_FACE_slider = None
        self.EIGHT_MOUTH_slider = None
        self.EIGHT_FACE_slider = None
        self.NINE_slider = None
        self.TEN_FACE_slider = None
        self.TEN_MOUTH_slider = None
        self.THREE_FACE_slider = None
        
        self.eyebrow_SMILE_slider = None
        self.eyebrow_NINE_slider = None
        self.eyebrow_EIGHT_slider = None
        self.eyebrow_FIVE_slider = None
        
        self.eyelash_TEN_EYEFOLD_slider = None
        self.eyelash_EIGHT_EYEFOLD_slider = None
        self.eyelash_FIVE_EYEFOLD_slider = None
        self.eyelash_TEN_EYELASH_slider = None
        self.eyelash_NINE_EYELASH_slider = None
        self.eyelash_EIGHT_EYELASH_slider = None
        
        self.MOUTH_slider = None

    def clear_right(self):
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.A_slider = None
        self.I_slider = None
        self.U_slider = None
        self.E_slider = None
        self.O_slider = None
        
        self.eyeClose_slider = None
        self.eyeSmall_slider = None
        
        self.ONE_MOUTH_slider = None
        self.TWO_FACE_slider = None
        self.THREE_MOUTH_slider = None
        self.FOUR_FACE_slider = None
        self.FIVE_MOUTH_slider = None
        self.SIX_MOUTH_slider = None
        self.SEVEN_MOUTH_slider = None
        self.SEVEN_FACE_slider = None
        self.EIGHT_MOUTH_slider = None
        self.EIGHT_FACE_slider = None
        self.NINE_slider = None
        self.TEN_FACE_slider = None
        self.TEN_MOUTH_slider = None
        self.THREE_FACE_slider = None
        
        self.eyebrow_SMILE_slider = None
        self.eyebrow_NINE_slider = None
        self.eyebrow_EIGHT_slider = None
        self.eyebrow_FIVE_slider = None
        
        self.eyelash_TEN_EYEFOLD_slider = None
        self.eyelash_EIGHT_EYEFOLD_slider = None
        self.eyelash_FIVE_EYEFOLD_slider = None
        self.eyelash_TEN_EYELASH_slider = None
        self.eyelash_NINE_EYELASH_slider = None
        self.eyelash_EIGHT_EYELASH_slider = None
        
        self.MOUTH_slider = None

    def show_A_x(self):
        self.clear_right()
        if cmds.objExists("A_switch_ctl"):
            cmds.select("A_switch_ctl")
        slider = FloatSliderWidget("translateX", 0.0, 2.0, 0.01)
        value = 0.0
        if cmds.objExists("A_switch_ctl"):
            value = cmds.getAttr("A_switch_ctl.translateX")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_A_x)
        slider.slider.valueChanged.connect(lambda v: self.set_A_x(slider.value()))
        self.A_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_A_x(self, v):
        if cmds.objExists("A_switch_ctl"):
            cmds.setAttr("A_switch_ctl.translateX", v)

    def show_I_x(self):
        self.clear_right()
        if cmds.objExists("I_switch_ctl"):
            cmds.select("I_switch_ctl")
        slider = FloatSliderWidget("translateX", 0.0, 2.0, 0.01)
        value = 0.0
        if cmds.objExists("I_switch_ctl"):
            value = cmds.getAttr("I_switch_ctl.translateX")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_I_x)
        slider.slider.valueChanged.connect(lambda v: self.set_I_x(slider.value()))
        self.I_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_I_x(self, v):
        if cmds.objExists("I_switch_ctl"):
            cmds.setAttr("I_switch_ctl.translateX", v)
            
    def show_U_x(self):
        self.clear_right()
        if cmds.objExists("U_switch_ctl"):
            cmds.select("U_switch_ctl")
        slider = FloatSliderWidget("translateX", 0.0, 2.0, 0.01)
        value = 0.0
        if cmds.objExists("U_switch_ctl"):
            value = cmds.getAttr("U_switch_ctl.translateX")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_U_x)
        slider.slider.valueChanged.connect(lambda v: self.set_U_x(slider.value()))
        self.U_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_U_x(self, v):
        if cmds.objExists("U_switch_ctl"):
            cmds.setAttr("U_switch_ctl.translateX", v)
            
    def show_E_x(self):
        self.clear_right()
        if cmds.objExists("E_switch_ctl"):
            cmds.select("E_switch_ctl")
        slider = FloatSliderWidget("translateX", 0.0, 2.0, 0.01)
        value = 0.0
        if cmds.objExists("E_switch_ctl"):
            value = cmds.getAttr("E_switch_ctl.translateX")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_E_x)
        slider.slider.valueChanged.connect(lambda v: self.set_E_x(slider.value()))
        self.E_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_E_x(self, v):
        if cmds.objExists("E_switch_ctl"):
            cmds.setAttr("E_switch_ctl.translateX", v)
            
    def show_O_x(self):
        self.clear_right()
        if cmds.objExists("O_switch_ctl"):
            cmds.select("O_switch_ctl")
        slider = FloatSliderWidget("translateX", 0.0, 2.0, 0.01)
        value = 0.0
        if cmds.objExists("O_switch_ctl"):
            value = cmds.getAttr("O_switch_ctl.translateX")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_O_x)
        slider.slider.valueChanged.connect(lambda v: self.set_O_x(slider.value()))
        self.O_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_O_x(self, v):
        if cmds.objExists("O_switch_ctl"):
            cmds.setAttr("O_switch_ctl.translateX", v)

    def show_EYE(self):
        self.clear_right()
        if cmds.objExists("eyeClose_ctl"):
            cmds.select("eyeClose_ctl")
            
        # Close Eyes
        slider_eyeClose = FloatSliderWidget("Close Eyes", 0.0, 1.0, 0.01)
        value_eyeClose = 0.0
        if cmds.objExists("eyeClose_ctl"):
            value_eyeClose = cmds.getAttr("eyeClose_ctl.Close Eyes")
        slider_eyeClose.set_value(value_eyeClose)
        slider_eyeClose.spinbox.valueChanged.connect(self.set_eyeClose)
        slider_eyeClose.slider.valueChanged.connect(lambda v: self.set_eyeClose(slider_eyeClose.value()))
        self.eyeClose_slider = slider_eyeClose
        self.right_layout.addWidget(slider_eyeClose)
        
        # Small
        slider_eyeSmall = FloatSliderWidget("Small", 0.0, 1.0, 0.01)
        value_eyeSmall = 1.0
        if cmds.objExists("eyeClose_ctl"):
            value_eyeSmall = cmds.getAttr("eyeClose_ctl.Small")
        slider_eyeSmall.set_value(value_eyeSmall)
        slider_eyeSmall.spinbox.valueChanged.connect(self.set_eyeSmall)
        slider_eyeSmall.slider.valueChanged.connect(lambda v: self.set_eyeSmall(slider_eyeSmall.value()))
        self.eyeSmall_slider = slider_eyeSmall
        self.right_layout.addWidget(slider_eyeSmall)
        self.right_layout.addStretch()

    def set_eyeClose(self, v):
        if cmds.objExists("eyeClose_ctl"):
            cmds.setAttr("eyeClose_ctl.Close Eyes", v)

    def set_eyeSmall(self, v):
        if cmds.objExists("eyeClose_ctl"):
            cmds.setAttr("eyeClose_ctl.Small", v)
            
    def show_FACE(self):
        self.clear_right()
        if cmds.objExists("face_ctl"):
            cmds.select("face_ctl")
            
        # ONE MOUTH
        slider_ONE_MOUTH = FloatSliderWidget("ONE_MOUTH", 0.0, 1.0, 0.01)
        value_ONE_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_ONE_MOUTH = cmds.getAttr("face_ctl.ONE_MOUTH")
        slider_ONE_MOUTH.set_value(value_ONE_MOUTH)
        slider_ONE_MOUTH.spinbox.valueChanged.connect(self.set_ONE_MOUTH)
        slider_ONE_MOUTH.slider.valueChanged.connect(lambda v: self.set_ONE_MOUTH(slider_ONE_MOUTH.value()))
        self.ONE_MOUTH_slider = slider_ONE_MOUTH
        self.right_layout.addWidget(slider_ONE_MOUTH)
        
        # TWO FACE
        slider_TWO_FACE = FloatSliderWidget("TWO_FACE", 0.0, 1.0, 0.01)
        value_TWO_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_TWO_FACE = cmds.getAttr("face_ctl.TWO_FACE")
        slider_TWO_FACE.set_value(value_TWO_FACE)
        slider_TWO_FACE.spinbox.valueChanged.connect(self.set_TWO_FACE)
        slider_TWO_FACE.slider.valueChanged.connect(lambda v: self.set_TWO_FACE(slider_TWO_FACE.value()))
        self.TWO_FACE_slider = slider_TWO_FACE
        self.right_layout.addWidget(slider_TWO_FACE)
        
        # THREE MOUTH
        slider_THREE_MOUTH = FloatSliderWidget("THREE_MOUTH", 0.0, 1.0, 0.01)
        value_THREE_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_THREE_MOUTH = cmds.getAttr("face_ctl.THREE_MOUTH")
        slider_THREE_MOUTH.set_value(value_THREE_MOUTH)
        slider_THREE_MOUTH.spinbox.valueChanged.connect(self.set_THREE_MOUTH)
        slider_THREE_MOUTH.slider.valueChanged.connect(lambda v: self.set_THREE_MOUTH(slider_THREE_MOUTH.value()))
        self.THREE_MOUTH_slider = slider_THREE_MOUTH
        self.right_layout.addWidget(slider_THREE_MOUTH)
        
        # FOUR FACE
        slider_FOUR_FACE = FloatSliderWidget("FOUR_FACE", 0.0, 1.0, 0.01)
        value_FOUR_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_FOUR_FACE = cmds.getAttr("face_ctl.FOUR_FACE")
        slider_FOUR_FACE.set_value(value_FOUR_FACE)
        slider_FOUR_FACE.spinbox.valueChanged.connect(self.set_FOUR_FACE)
        slider_FOUR_FACE.slider.valueChanged.connect(lambda v: self.set_FOUR_FACE(slider_FOUR_FACE.value()))
        self.FOUR_FACE_slider = slider_FOUR_FACE
        self.right_layout.addWidget(slider_FOUR_FACE)
        
        # FIVE MOUTH
        slider_FIVE_MOUTH = FloatSliderWidget("FIVE_MOUTH", 0.0, 1.0, 0.01)
        value_FIVE_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_FIVE_MOUTH = cmds.getAttr("face_ctl.FIVE_MOUTH")
        slider_FIVE_MOUTH.set_value(value_FIVE_MOUTH)
        slider_FIVE_MOUTH.spinbox.valueChanged.connect(self.set_FIVE_MOUTH)
        slider_FIVE_MOUTH.slider.valueChanged.connect(lambda v: self.set_FIVE_MOUTH(slider_FIVE_MOUTH.value()))
        self.FIVE_MOUTH_slider = slider_FIVE_MOUTH
        self.right_layout.addWidget(slider_FIVE_MOUTH)
        
        # SIX MOUTH
        slider_SIX_MOUTH = FloatSliderWidget("SIX_MOUTH", 0.0, 1.0, 0.01)
        value_SIX_MOUTH = 1.0
        if cmds.objExists("face_ctl"):
            value_SIX_MOUTH = cmds.getAttr("face_ctl.SIX_MOUTH")
        slider_SIX_MOUTH.set_value(value_SIX_MOUTH)
        slider_SIX_MOUTH.spinbox.valueChanged.connect(self.set_SIX_MOUTH)
        slider_SIX_MOUTH.slider.valueChanged.connect(lambda v: self.set_SIX_MOUTH(slider_SIX_MOUTH.value()))
        self.SIX_MOUTH_slider = slider_SIX_MOUTH
        self.right_layout.addWidget(slider_SIX_MOUTH)
        
        # SEVEN MOUTH
        slider_SEVEN_MOUTH = FloatSliderWidget("SEVEN_MOUTH", 0.0, 1.0, 0.01)
        value_SEVEN_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_SEVEN_MOUTH = cmds.getAttr("face_ctl.SEVEN_MOUTH")
        slider_SEVEN_MOUTH.set_value(value_SEVEN_MOUTH)
        slider_SEVEN_MOUTH.spinbox.valueChanged.connect(self.set_SEVEN_MOUTH)
        slider_SEVEN_MOUTH.slider.valueChanged.connect(lambda v: self.set_SEVEN_MOUTH(slider_SEVEN_MOUTH.value()))
        self.SEVEN_MOUTH_slider = slider_SEVEN_MOUTH
        self.right_layout.addWidget(slider_SEVEN_MOUTH)
        
        # SEVEN FACE
        slider_SEVEN_FACE = FloatSliderWidget("SEVEN_FACE", 0.0, 1.0, 0.01)
        value_SEVEN_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_SEVEN_FACE = cmds.getAttr("face_ctl.SEVEN_FACE")
        slider_SEVEN_FACE.set_value(value_SEVEN_FACE)
        slider_SEVEN_FACE.spinbox.valueChanged.connect(self.set_SEVEN_FACE)
        slider_SEVEN_FACE.slider.valueChanged.connect(lambda v: self.set_SEVEN_FACE(slider_SEVEN_FACE.value()))
        self.SEVEN_FACE_slider = slider_SEVEN_FACE
        self.right_layout.addWidget(slider_SEVEN_FACE)
        
        # EIGHT MOUTH
        slider_EIGHT_MOUTH = FloatSliderWidget("EIGHT_MOUTH", 0.0, 1.0, 0.01)
        value_EIGHT_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_EIGHT_MOUTH = cmds.getAttr("face_ctl.EIGHT_MOUTH")
        slider_EIGHT_MOUTH.set_value(value_EIGHT_MOUTH)
        slider_EIGHT_MOUTH.spinbox.valueChanged.connect(self.set_EIGHT_MOUTH)
        slider_EIGHT_MOUTH.slider.valueChanged.connect(lambda v: self.set_EIGHT_MOUTH(slider_EIGHT_MOUTH.value()))
        self.EIGHT_MOUTH_slider = slider_EIGHT_MOUTH
        self.right_layout.addWidget(slider_EIGHT_MOUTH)
        
        # EIGHT FACE
        slider_EIGHT_FACE = FloatSliderWidget("EIGHT_FACE", 0.0, 1.0, 0.01)
        value_EIGHT_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_EIGHT_FACE = cmds.getAttr("face_ctl.EIGHT_FACE")
        slider_EIGHT_FACE.set_value(value_EIGHT_FACE)
        slider_EIGHT_FACE.spinbox.valueChanged.connect(self.set_EIGHT_FACE)
        slider_EIGHT_FACE.slider.valueChanged.connect(lambda v: self.set_EIGHT_FACE(slider_EIGHT_FACE.value()))
        self.EIGHT_FACE_slider = slider_EIGHT_FACE
        self.right_layout.addWidget(slider_EIGHT_FACE)
        
        # NINE
        slider_NINE = FloatSliderWidget("NINE", 0.0, 1.0, 0.01)
        value_NINE = 0.0
        if cmds.objExists("face_ctl"):
            value_NINE = cmds.getAttr("face_ctl.NINE")
        slider_NINE.set_value(value_NINE)
        slider_NINE.spinbox.valueChanged.connect(self.set_NINE)
        slider_NINE.slider.valueChanged.connect(lambda v: self.set_NINE(slider_NINE.value()))
        self.NINE_slider = slider_NINE
        self.right_layout.addWidget(slider_NINE)
        
        # TEN FACE
        slider_TEN_FACE = FloatSliderWidget("TEN_FACE", 0.0, 1.0, 0.01)
        value_TEN_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_TEN_FACE = cmds.getAttr("face_ctl.TEN_FACE")
        slider_TEN_FACE.set_value(value_TEN_FACE)
        slider_TEN_FACE.spinbox.valueChanged.connect(self.set_TEN_FACE)
        slider_TEN_FACE.slider.valueChanged.connect(lambda v: self.set_TEN_FACE(slider_TEN_FACE.value()))
        self.TEN_FACE_slider = slider_TEN_FACE
        self.right_layout.addWidget(slider_TEN_FACE)
        
        # TEN MOUTH
        slider_TEN_MOUTH = FloatSliderWidget("TEN_MOUTH", 0.0, 1.0, 0.01)
        value_TEN_MOUTH = 0.0
        if cmds.objExists("face_ctl"):
            value_TEN_MOUTH = cmds.getAttr("face_ctl.TEN_MOUTH")
        slider_TEN_MOUTH.set_value(value_TEN_MOUTH)
        slider_TEN_MOUTH.spinbox.valueChanged.connect(self.set_TEN_MOUTH)
        slider_TEN_MOUTH.slider.valueChanged.connect(lambda v: self.set_TEN_MOUTH(slider_TEN_MOUTH.value()))
        self.TEN_MOUTH_slider = slider_TEN_MOUTH
        self.right_layout.addWidget(slider_TEN_MOUTH)
        
        # THREE FACE
        slider_THREE_FACE = FloatSliderWidget("THREE_FACE", 0.0, 1.0, 0.01)
        value_THREE_FACE = 1.0
        if cmds.objExists("face_ctl"):
            value_THREE_FACE = cmds.getAttr("face_ctl.THREE_FACE")
        slider_THREE_FACE.set_value(value_THREE_FACE)
        slider_THREE_FACE.spinbox.valueChanged.connect(self.set_THREE_FACE)
        slider_THREE_FACE.slider.valueChanged.connect(lambda v: self.set_THREE_FACE(slider_THREE_FACE.value()))
        self.THREE_FACE_slider = slider_THREE_FACE
        self.right_layout.addWidget(slider_THREE_FACE)
        self.right_layout.addStretch()

    def set_ONE_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.ONE_MOUTH", v)

    def set_TWO_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.TWO_FACE", v)

    def set_THREE_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.THREE_MOUTH", v)

    def set_FOUR_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.FOUR_FACE", v)
            
    def set_FIVE_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.FIVE_MOUTH", v)

    def set_SIX_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.SIX_MOUTH", v)

    def set_SEVEN_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.SEVEN_MOUTH", v)

    def set_SEVEN_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.SEVEN_FACE", v)

    def set_EIGHT_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.EIGHT_MOUTH", v)
            
    def set_EIGHT_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.EIGHT_FACE", v)

    def set_NINE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.NINE", v)

    def set_TEN_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.TEN_FACE", v)

    def set_TEN_MOUTH(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.TEN_MOUTH", v)

    def set_THREE_FACE(self, v):
        if cmds.objExists("face_ctl"):
            cmds.setAttr("face_ctl.THREE_FACE", v)
            
    def show_EYEBROW(self):
        self.clear_right()
        if cmds.objExists("eyebrow_ctl"):
            cmds.select("eyebrow_ctl")
            
        # Smile
        slider_eyebrow_SMILE = FloatSliderWidget("smile", 0.0, 1.0, 0.01)
        value_eyebrow_SMILE = 0.0
        if cmds.objExists("eyebrow_ctl"):
            value_eyebrow_SMILE = cmds.getAttr("eyebrow_ctl.smile")
        slider_eyebrow_SMILE.set_value(value_eyebrow_SMILE)
        slider_eyebrow_SMILE.spinbox.valueChanged.connect(self.set_eyebrow_SMILE)
        slider_eyebrow_SMILE.slider.valueChanged.connect(lambda v: self.set_eyebrow_SMILE(slider_eyebrow_SMILE.value()))
        self.SMILE_slider = slider_eyebrow_SMILE
        self.right_layout.addWidget(slider_eyebrow_SMILE)
        
        # NINE
        slider_eyebrow_NINE = FloatSliderWidget("NINE", 0.0, 1.0, 0.01)
        value_eyebrow_NINE = 1.0
        if cmds.objExists("eyebrow_ctl"):
            value_eyebrow_NINE = cmds.getAttr("eyebrow_ctl.NINE")
        slider_eyebrow_NINE.set_value(value_eyebrow_NINE)
        slider_eyebrow_NINE.spinbox.valueChanged.connect(self.set_eyebrow_NINE)
        slider_eyebrow_NINE.slider.valueChanged.connect(lambda v: self.set_eyebrow_NINE(slider_eyebrow_NINE.value()))
        self.eyebrow_NINE_slider = slider_eyebrow_NINE
        self.right_layout.addWidget(slider_eyebrow_NINE)
        
        # EIGHT
        slider_eyebrow_EIGHT = FloatSliderWidget("EIGHT", 0.0, 1.0, 0.01)
        value_eyebrow_EIGHT = 0.0
        if cmds.objExists("eyebrow_ctl"):
            value_eyebrow_EIGHT = cmds.getAttr("eyebrow_ctl.EIGHT")
        slider_eyebrow_EIGHT.set_value(value_eyebrow_EIGHT)
        slider_eyebrow_EIGHT.spinbox.valueChanged.connect(self.set_eyebrow_EIGHT)
        slider_eyebrow_EIGHT.slider.valueChanged.connect(lambda v: self.set_eyebrow_EIGHT(slider_eyebrow_EIGHT.value()))
        self.eyebrow_EIGHT_slider = slider_eyebrow_EIGHT
        self.right_layout.addWidget(slider_eyebrow_EIGHT)
        
        # FIVE
        slider_eyebrow_FIVE = FloatSliderWidget("FIVE", 0.0, 1.0, 0.01)
        value_eyebrow_FIVE = 1.0
        if cmds.objExists("eyebrow_ctl"):
            value_eyebrow_FIVE = cmds.getAttr("eyebrow_ctl.FIVE")
        slider_eyebrow_FIVE.set_value(value_eyebrow_FIVE)
        slider_eyebrow_FIVE.spinbox.valueChanged.connect(self.set_eyebrow_FIVE)
        slider_eyebrow_FIVE.slider.valueChanged.connect(lambda v: self.set_eyebrow_FIVE(slider_eyebrow_FIVE.value()))
        self.eyebrow_FIVE_slider = slider_eyebrow_FIVE
        self.right_layout.addWidget(slider_eyebrow_FIVE)
        self.right_layout.addStretch()

    def set_eyebrow_SMILE(self, v):
        if cmds.objExists("eyebrow_ctl"):
            cmds.setAttr("eyebrow_ctl.smile", v)

    def set_eyebrow_NINE(self, v):
        if cmds.objExists("eyebrow_ctl"):
            cmds.setAttr("eyebrow_ctl.NINE", v)

    def set_eyebrow_EIGHT(self, v):
        if cmds.objExists("eyebrow_ctl"):
            cmds.setAttr("eyebrow_ctl.EIGHT", v)

    def set_eyebrow_FIVE(self, v):
        if cmds.objExists("eyebrow_ctl"):
            cmds.setAttr("eyebrow_ctl.FIVE", v)
            
    def show_EYELASH(self):
        self.clear_right()
        if cmds.objExists("eyelash_ctl"):
            cmds.select("eyelash_ctl")
            
        # TEN Eyefold
        slider_eyefold_TEN_EYEFOLD = FloatSliderWidget("TEN_Eyefold", 0.0, 1.0, 0.01)
        value_eyefold_TEN_EYEFOLD = 0.0
        if cmds.objExists("eyelash_ctl"):
            value_eyefold_TEN_EYEFOLD = cmds.getAttr("eyelash_ctl.TEN_eyefold")
        slider_eyefold_TEN_EYEFOLD.set_value(value_eyefold_TEN_EYEFOLD)
        slider_eyefold_TEN_EYEFOLD.spinbox.valueChanged.connect(self.set_eyefold_TEN_EYEFOLD)
        slider_eyefold_TEN_EYEFOLD.slider.valueChanged.connect(lambda v: self.set_eyefold_TEN_EYEFOLD(slider_eyefold_TEN_EYEFOLD.value()))
        self.TEN_Eyefold_slider = slider_eyefold_TEN_EYEFOLD
        self.right_layout.addWidget(slider_eyefold_TEN_EYEFOLD)
        
        # EIGHT Eyefold
        slider_eyefold_EIGHT_EYEFOLD = FloatSliderWidget("EIGHT_Eyefold", 0.0, 1.0, 0.01)
        value_eyefold_EIGHT_EYEFOLD = 1.0
        if cmds.objExists("eyelash_ctl"):
            value_eyefold_EIGHT_EYEFOLD = cmds.getAttr("eyelash_ctl.EIGHT_eyefold")
        slider_eyefold_EIGHT_EYEFOLD.set_value(value_eyefold_EIGHT_EYEFOLD)
        slider_eyefold_EIGHT_EYEFOLD.spinbox.valueChanged.connect(self.set_eyefold_EIGHT_EYEFOLD)
        slider_eyefold_EIGHT_EYEFOLD.slider.valueChanged.connect(lambda v: self.set_eyefold_EIGHT_EYEFOLD(slider_eyefold_EIGHT_EYEFOLD.value()))
        self.EIGHT_Eyefold_slider = slider_eyefold_EIGHT_EYEFOLD
        self.right_layout.addWidget(slider_eyefold_EIGHT_EYEFOLD)
        
        # FIVE Eyefold
        slider_eyefold_FIVE_EYEFOLD = FloatSliderWidget("FIVE_Eyefold", 0.0, 1.0, 0.01)
        value_eyefold_FIVE_EYEFOLD = 0.0
        if cmds.objExists("eyelash_ctl"):
            value_eyefold_FIVE_EYEFOLD = cmds.getAttr("eyelash_ctl.FIVE_eyefold")
        slider_eyefold_FIVE_EYEFOLD.set_value(value_eyefold_FIVE_EYEFOLD)
        slider_eyefold_FIVE_EYEFOLD.spinbox.valueChanged.connect(self.set_eyefold_FIVE_EYEFOLD)
        slider_eyefold_FIVE_EYEFOLD.slider.valueChanged.connect(lambda v: self.set_eyefold_FIVE_EYEFOLD(slider_eyefold_FIVE_EYEFOLD.value()))
        self.FIVE_Eyefold_slider = slider_eyefold_FIVE_EYEFOLD
        self.right_layout.addWidget(slider_eyefold_FIVE_EYEFOLD)
        
        # TEN Eyelash
        slider_eyelash_TEN_EYELASH = FloatSliderWidget("TEN_Eyelash", 0.0, 1.0, 0.01)
        value_eyelash_TEN_EYELASH = 1.0
        if cmds.objExists("eyelash_ctl"):
            value_eyelash_TEN_EYELASH = cmds.getAttr("eyelash_ctl.TEN_eyelash")
        slider_eyelash_TEN_EYELASH.set_value(value_eyelash_TEN_EYELASH)
        slider_eyelash_TEN_EYELASH.spinbox.valueChanged.connect(self.set_eyelash_TEN_EYELASH)
        slider_eyelash_TEN_EYELASH.slider.valueChanged.connect(lambda v: self.set_eyelash_TEN_EYELASH(slider_eyelash_TEN_EYELASH.value()))
        self.TEN_Eyelash_slider = slider_eyelash_TEN_EYELASH
        self.right_layout.addWidget(slider_eyelash_TEN_EYELASH)
        
        # NINE Eyelash
        slider_eyelash_NINE_EYELASH = FloatSliderWidget("NINE_Eyelash", 0.0, 1.0, 0.01)
        value_eyelash_NINE_EYELASH = 0.0
        if cmds.objExists("eyelash_ctl"):
            value_eyelash_NINE_EYELASH = cmds.getAttr("eyelash_ctl.NINE_eyelash")
        slider_eyelash_NINE_EYELASH.set_value(value_eyelash_NINE_EYELASH)
        slider_eyelash_NINE_EYELASH.spinbox.valueChanged.connect(self.set_eyelash_NINE_EYELASH)
        slider_eyelash_NINE_EYELASH.slider.valueChanged.connect(lambda v: self.set_eyelash_NINE_EYELASH(slider_eyelash_NINE_EYELASH.value()))
        self.NINE_Eyelash_slider = slider_eyelash_NINE_EYELASH
        self.right_layout.addWidget(slider_eyelash_NINE_EYELASH)
        
        # EIGHT Eyelash
        slider_eyelash_EIGHT_EYELASH = FloatSliderWidget("EIGHT_Eyelash", 0.0, 1.0, 0.01)
        value_eyelash_EIGHT_EYELASH = 1.0
        if cmds.objExists("eyelash_ctl"):
            value_eyelash_EIGHT_EYELASH = cmds.getAttr("eyelash_ctl.EIGHT_eyelash")
        slider_eyelash_EIGHT_EYELASH.set_value(value_eyelash_EIGHT_EYELASH)
        slider_eyelash_EIGHT_EYELASH.spinbox.valueChanged.connect(self.set_eyelash_EIGHT_EYELASH)
        slider_eyelash_EIGHT_EYELASH.slider.valueChanged.connect(lambda v: self.set_eyelash_EIGHT_EYELASH(slider_eyelash_EIGHT_EYELASH.value()))
        self.EIGHT_Eyelash_slider = slider_eyelash_EIGHT_EYELASH
        self.right_layout.addWidget(slider_eyelash_EIGHT_EYELASH)
        self.right_layout.addStretch()

    def set_eyefold_TEN_EYEFOLD(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.TEN_eyefold", v)
            
    def set_eyefold_EIGHT_EYEFOLD(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.EIGHT_eyefold", v)

    def set_eyefold_FIVE_EYEFOLD(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.FIVE_eyefold", v)

    def set_eyelash_TEN_EYELASH(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.TEN_eyelash", v)

    def set_eyelash_NINE_EYELASH(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.NINE_eyelash", v)

    def set_eyelash_EIGHT_EYELASH(self, v):
        if cmds.objExists("eyelash_ctl"):
            cmds.setAttr("eyelash_ctl.EIGHT_eyelash", v)
            
    def show_MOUTH(self):
        self.clear_right()
        if cmds.objExists("mouth_ctl"):
            cmds.select("mouth_ctl")
        slider = FloatSliderWidget("Teeth", 0.0, 1.0, 0.01)
        value = 0.0
        if cmds.objExists("mouth_ctl"):
            value = cmds.getAttr("mouth_ctl.Teeth")
        slider.set_value(value)
        slider.spinbox.valueChanged.connect(self.set_MOUTH)
        slider.slider.valueChanged.connect(lambda v: self.set_MOUTH(slider.value()))
        self.MOUTH_slider = slider
        self.right_layout.addWidget(slider)
        self.right_layout.addStretch()

    def set_MOUTH(self, v):
        if cmds.objExists("mouth_ctl"):
            cmds.setAttr("mouth_ctl.Teeth", v)
    
    def reload_volumes(self):
        # A_switch_ctl用スライダーの更新
        if self.A_slider and cmds.objExists("A_switch_ctl"):
            value = cmds.getAttr("A_switch_ctl.translateX")
            self.A_slider.set_value(value)
            
        # I_switch_ctl用スライダーの更新
        if self.I_slider and cmds.objExists("I_switch_ctl"):
            value = cmds.getAttr("I_switch_ctl.translateX")
            self.I_slider.set_value(value)
            
        # U_switch_ctl用スライダーの更新
        if self.U_slider and cmds.objExists("U_switch_ctl"):
            value = cmds.getAttr("U_switch_ctl.translateX")
            self.U_slider.set_value(value)
            
        # E_switch_ctl用スライダーの更新
        if self.E_slider and cmds.objExists("E_switch_ctl"):
            value = cmds.getAttr("E_switch_ctl.translateX")
            self.E_slider.set_value(value)
            
        # O_switch_ctl用スライダーの更新
        if self.O_slider and cmds.objExists("O_switch_ctl"):
            value = cmds.getAttr("O_switch_ctl.translateX")
            self.O_slider.set_value(value)
        
        # eyeClose_ctl用スライダーの更新
        if self.eyeClose_slider and cmds.objExists("eyeClose_ctl"):
            value_eyeClose = cmds.getAttr("eyeClose_ctl.Close Eyes")
            self.eyeClose_slider.set_value(value_eyeClose)
        if self.eyeSmall_slider and cmds.objExists("eyeClose_ctl"):
            value_eyeSmall = cmds.getAttr("eyeClose_ctl.Small")
            self.eyeSmall_slider.set_value(value_eyeSmall)
            
        # face_ctl用スライダーの更新
        if self.ONE_MOUTH_slider and cmds.objExists("face_ctl"):
            value_ONE_MOUTH = cmds.getAttr("face_ctl.ONE_MOUTH")
            self.ONE_MOUTH_slider.set_value(value_ONE_MOUTH)
            
        if self.TWO_FACE_slider and cmds.objExists("face_ctl"):
            value_TWO_FACE = cmds.getAttr("face_ctl.TWO_FACE")
            self.TWO_FACE_slider.set_value(value_TWO_FACE)
            
        if self.THREE_MOUTH_slider and cmds.objExists("face_ctl"):
            value_THREE_MOUTH = cmds.getAttr("face_ctl.THREE_MOUTH")
            self.THREE_MOUTH_slider.set_value(value_THREE_MOUTH)
            
        if self.FOUR_FACE_slider and cmds.objExists("face_ctl"):
            value_FOUR_FACE = cmds.getAttr("face_ctl.FOUR_FACE")
            self.FOUR_FACE_slider.set_value(value_FOUR_FACE)
            
        if self.FIVE_MOUTH_slider and cmds.objExists("face_ctl"):
            value_FIVE_MOUTH = cmds.getAttr("face_ctl.FIVE_MOUTH")
            self.FIVE_MOUTH_slider.set_value(value_FIVE_MOUTH)
            
        if self.SIX_MOUTH_slider and cmds.objExists("face_ctl"):
            value_SIX_MOUTH = cmds.getAttr("face_ctl.SIX_MOUTH")
            self.SIX_MOUTH_slider.set_value(value_SIX_MOUTH)
            
        if self.SEVEN_MOUTH_slider and cmds.objExists("face_ctl"):
            value_SEVEN_MOUTH = cmds.getAttr("face_ctl.SEVEN_MOUTH")
            self.SEVEN_MOUTH_slider.set_value(value_SEVEN_MOUTH)
            
        if self.SEVEN_FACE_slider and cmds.objExists("face_ctl"):
            value_SEVEN_FACE = cmds.getAttr("face_ctl.SEVEN_FACE")
            self.SEVEN_FACE_slider.set_value(value_SEVEN_FACE)
            
        if self.EIGHT_MOUTH_slider and cmds.objExists("face_ctl"):
            value_EIGHT_MOUTH = cmds.getAttr("face_ctl.EIGHT_MOUTH")
            self.EIGHT_MOUTH_slider.set_value(value_EIGHT_MOUTH)
            
        if self.EIGHT_FACE_slider and cmds.objExists("face_ctl"):
            value_EIGHT_FACE = cmds.getAttr("face_ctl.EIGHT_FACE")
            self.EIGHT_FACE_slider.set_value(value_EIGHT_FACE)
            
        if self.NINE_slider and cmds.objExists("face_ctl"):
            value_NINE = cmds.getAttr("face_ctl.NINE")
            self.NINE_slider.set_value(value_NINE)
            
        if self.TEN_FACE_slider and cmds.objExists("face_ctl"):
            value_TEN_FACE = cmds.getAttr("face_ctl.TEN_FACE")
            self.TEN_FACE_slider.set_value(value_TEN_FACE)
            
        if self.TEN_MOUTH_slider and cmds.objExists("face_ctl"):
            value_TEN_MOUTH = cmds.getAttr("face_ctl.TEN_MOUTH")
            self.TEN_MOUTH_slider.set_value(value_TEN_MOUTH)
            
        if self.THREE_FACE_slider and cmds.objExists("face_ctl"):
            value_THREE_FACE = cmds.getAttr("face_ctl.THREE_FACE")
            self.THREE_FACE_slider.set_value(value_THREE_FACE)
        
        # eyebrow    
        if self.eyebrow_SMILE_slider and cmds.objExists("eyebrow_ctl"):
            value_eyebrow_SMILE = cmds.getAttr("eyebrow_ctl.smile")
            self.eyebrow_SMILE_slider.set_value(value_eyebrow_SMILE)
            
        if self.eyebrow_NINE_slider and cmds.objExists("eyebrow_ctl"):
            value_eyebrow_NINE = cmds.getAttr("eyebrow_ctl.smile")
            self.eyebrow_NINE_slider.set_value(value_eyebrow_NINE)
            
        if self.eyebrow_EIGHT_slider and cmds.objExists("eyebrow_ctl"):
            value_eyebrow_EIGHT = cmds.getAttr("eyebrow_ctl.smile")
            self.eyebrow_EIGHT_slider.set_value(value_eyebrow_EIGHT)
            
        if self.eyebrow_FIVE_slider and cmds.objExists("eyebrow_ctl"):
            value_eyebrow_FIVE = cmds.getAttr("eyebrow_ctl.smile")
            self.eyebrow_FIVE_slider.set_value(value_eyebrow_FIVE)
            
        # eyelash
        if self.eyelash_TEN_EYEFOLD_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_TEN_EYEFOLD = cmds.getAttr("eyelash_ctl.TEN_eyefold")
            self.eyelash_TEN_EYEFOLD_slider.set_value(value_eyelash_TEN_EYEFOLD)
            
        if self.eyelash_EIGHT_EYEFOLD_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_EIGHT_EYEFOLD = cmds.getAttr("eyelash_ctl.EIGHT_eyefold")
            self.eyelash_EIGHT_EYEFOLD_slider.set_value(value_eyelash_EIGHT_EYEFOLD)
            
        if self.eyelash_FIVE_EYEFOLD_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_FIVE_EYEFOLD = cmds.getAttr("eyelash_ctl.FIVE_eyefold")
            self.eyelash_FIVE_EYEFOLD_slider.set_value(value_eyelash_FIVE_EYEFOLD)
            
        if self.eyelash_TEN_EYELASH_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_TEN_EYELASH = cmds.getAttr("eyelash_ctl.TEN_eyelash")
            self.eyelash_TEN_EYELASH_slider.set_value(value_eyelash_TEN_EYELASH)
            
        if self.eyelash_NINE_EYELASH_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_NINE_EYELASH = cmds.getAttr("eyelash_ctl.NINE_eyelash")
            self.eyelash_NINE_EYELASH_slider.set_value(value_eyelash_NINE_EYELASH)
            
        if self.eyelash_EIGHT_EYELASH_slider and cmds.objExists("eyelash_ctl"):
            value_eyelash_EIGHT_EYELASH = cmds.getAttr("eyelash_ctl.EIGHT_eyelash")
            self.eyelash_EIGHT_EYELASH_slider.set_value(value_eyelash_EIGHT_EYELASH)
            
        # mouth
        if self.MOUTH_slider and cmds.objExists("mouth_ctl"):
            value_MOUTH = cmds.getAttr("mouth_ctl.Teeth")
            self.MOUTH_slider.set_value(value_MOUTH)

def show_ui():
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win = AttrSliderUI(parent=get_maya_main_window())
    win.show()

show_ui()