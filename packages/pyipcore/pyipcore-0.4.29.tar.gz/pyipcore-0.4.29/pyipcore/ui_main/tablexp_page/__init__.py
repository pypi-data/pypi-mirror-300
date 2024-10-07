import os.path
from qwork.fileitem import *
from pyipcore.ui_utils import *
from pyipcore.ui_main.tablexp_page._tools import *



class QExcelExampleShower(QWidget):
    def __init__(self, fixed_width, fixed_height, parent=None):
        super(QExcelExampleShower, self).__init__(parent)
        self.setFixedSize(fixed_width, fixed_height)
        self._font = LBL_FONT_MINI
        self.bias:tuple[int, int] = (0, 0)
        self.target:tuple[int, int] = (1, 1)
        self.delta:tuple[int, int] = (0, 0)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        pen0 = QPen(LT_BLACK, 1, Qt.SolidLine)
        pen1 = QPen(Qt.darkGray, 1, Qt.SolidLine)
        painter.setPen(pen0)
        painter.setBrush(QBrush(LT_YELLOW))

        painter.drawRect(0, 0, self.width(), self.height())

        # # top left
        # painter.drawLine(1, 1, self.width(), 0)
        # painter.drawLine(1, 1, 0, self.height())
        #
        # # top 'A' left '1'
        # painter.setPen(pen1)
        # painter.setFont(self._font)
        # painter.drawText(20, 15, 'A')
        # painter.drawText(5, 30, '1')


class QCheckedContainer(QWidget):
    def __init__(self, parent=None):
        super(QCheckedContainer, self).__init__(parent)

class QCheckedListWidget(QWidget):
    def __init__(self, parent=None):
        super(QCheckedListWidget, self).__init__(parent)
        self.sheets = []    # 存储名称
        self._checks = []   # 存储复选框
        self._widgets = []
        self.initUI()
        self.setStyleSheet('background-color: white;' f'border: 1px solid rgba({LT_BLACK.red()}, {LT_BLACK.green()}, {LT_BLACK.blue()}, {LT_BLACK.alpha()});')

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.container = QCheckedContainer()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.addStretch(1)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)
        self._area = QScrollArea()
        self._area.setWidget(self.container)
        self._area.setWidgetResizable(True)
        self._area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.layout.addWidget(self._area)
        # self.layout.addStretch(1)

        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

    def clear(self):
        for widget in self._widgets:
            widget.deleteLater()
        self._area.takeWidget()
        self.container.deleteLater()
        self.container = QCheckedContainer()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)
        self.list_layout.addStretch(1)
        self._area.setWidget(self.container)

        self._widgets.clear()
        self.sheets.clear()
        self._checks.clear()

    def addItem(self, name, checked=False):
        layout = QHBoxLayout()
        lbl = QLabel(name)
        check = QCheckBox()
        check.setChecked(checked)
        layout.addWidget(check)
        layout.addWidget(lbl)
        layout.addStretch(1)
        lbl.setFont(LBL_FONT_MINI)
        lbl.setStyleSheet("border: 0px;")
        check.setStyleSheet("border: 0px;")
        self._checks.append(check)
        self.sheets.append(name)
        self._widgets.append(lbl)
        self._widgets.append(check)
        self.list_layout.insertLayout(len(self._checks) - 1, layout)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.setPen(QPen(LT_BLACK, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))

        painter.drawRect(0, 0, self.width(), self.height())

        super().paintEvent(a0)

    @property
    def selects(self) -> list[bool]:
        return [c.isChecked() for c in self._checks]


class QSheetsListWidget(QCheckedListWidget):
    onCheckedChanged = pyqtSignal(int, int)
    def __init__(self, excel_path=None, parent=None):
        super(QSheetsListWidget, self).__init__(parent)
        self._excel_path = excel_path
        if excel_path: self._load_sheets()

    def _load_sheets(self):
        xls = pd.ExcelFile(self._excel_path)
        for sheet in xls.sheet_names:
            self.addItem(sheet, checked=True)

    @property
    def path(self):
        return self._excel_path

    @path.setter
    def path(self, path):
        self._excel_path = path
        self.clear()
        if os.path.exists(path):
            self._load_sheets()

    def addItem(self, name, checked=False):
        super().addItem(name, checked)
        self._checks[-1].stateChanged.connect(lambda state: self._on_check_changed(len(self._checks) - 1, state))

    def _on_check_changed(self, idx, state):
        self.onCheckedChanged.emit(idx, state)



class QExcelFileHeaderCollector(QWidget):
    onExcelChanged = pyqtSignal(str)
    onCstChanged = pyqtSignal(str)
    onSelectedSheetsChanged = pyqtSignal(list)
    def __init__(self, parent=None):
        super(QExcelFileHeaderCollector, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(1, 1, 1, 1)
        self._layout.setSpacing(8)
        self.setLayout(self._layout)
        h0, h1, h2 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        v0 = QVBoxLayout()
        self.setFont(LBL_FONT_MINI)
        self._excelslot = QFileSlot(formats=['xlsx'], size=100)
        self._excelslot.fileChanged.connect(self._on_excel_changed)
        self._excelslot.setFont(ARIAL_FONT)
        self._cstslot = QFileSlot(size=100)
        self._cstslot.fileChanged.connect(self._on_cst_changed)
        self._cstslot.setFont(ARIAL_FONT)
        h0.addStretch(1)
        h0.addWidget(self._excelslot)
        h0.addStretch(1)
        v0.addStretch(1)
        v0.addLayout(h0)
        self._fxlbl = QFixWidthLabel(120)
        self._fxlbl.setText('IO Table\nxlsx')
        self._fxlbl.setAlignment(Qt.AlignCenter)
        v0.addWidget(self._fxlbl)
        h1.addStretch(1)
        h1.addWidget(self._cstslot)
        h1.addStretch(1)
        v0.addLayout(h1)
        self._cslbl = QFixWidthLabel(120)
        self._cslbl.setText('cst fmt\nany')
        self._cslbl.setAlignment(Qt.AlignCenter)
        v0.addWidget(self._cslbl)
        v0.addStretch(1)
        h2.addLayout(v0)
        self._shower = QExcelExampleShower(320, 480)
        h2.addWidget(self._shower)
        self._layout.addLayout(h2)

        l0, l1, l2 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        lbl = QLabel('Bias   : (')
        lbl.setFixedWidth(90)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._bias_x = QSpinBox()  # > 0
        self._bias_x.setMinimum(0)
        self._bias_x.setMaximum(100)
        self._bias_x.setValue(0)
        self._bias_x.setFont(LBL_FONT)
        self._bias_x.valueChanged.connect(self._on_value_changed)
        l0.addWidget(self._bias_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._bias_y = QSpinBox()
        self._bias_y.setMinimum(0)
        self._bias_y.setMaximum(100)
        self._bias_y.setValue(1)
        self._bias_y.setFont(LBL_FONT)
        self._bias_y.valueChanged.connect(self._on_value_changed)
        l0.addWidget(self._bias_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._layout.addLayout(l0)

        lbl = QLabel('Target:(')
        lbl.setFixedWidth(90)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._target_x = QSpinBox()
        self._target_x.setMinimum(1)
        self._target_x.setMaximum(200)
        self._target_x.setValue(6)
        self._target_x.setFont(LBL_FONT)
        self._target_x.valueChanged.connect(self._on_value_changed)
        l1.addWidget(self._target_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._target_y = QSpinBox()
        self._target_y.setMinimum(1)
        self._target_y.setMaximum(200)
        self._target_y.setValue(30)
        self._target_y.setFont(LBL_FONT)
        self._target_y.valueChanged.connect(self._on_value_changed)
        l1.addWidget(self._target_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._layout.addLayout(l1)

        lbl = QLabel('Delta : (')
        lbl.setFixedWidth(90)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._delta_x = QSpinBox()
        self._delta_x.setMinimum(0)
        self._delta_x.setMaximum(100)
        self._delta_x.setValue(0)
        self._delta_x.setFont(LBL_FONT)
        self._delta_x.valueChanged.connect(self._on_value_changed)
        l2.addWidget(self._delta_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._delta_y = QSpinBox()
        self._delta_y.setMinimum(0)
        self._delta_y.setMaximum(100)
        self._delta_y.setValue(2)
        self._delta_y.setFont(LBL_FONT)
        self._delta_y.valueChanged.connect(self._on_value_changed)
        l2.addWidget(self._delta_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._layout.addLayout(l2)

        self._sheets = QSheetsListWidget()
        self._sheets.onCheckedChanged.connect(self._on_selected_sheets_changed)
        # 设置strengthen
        self._layout.addWidget(self._sheets, 2)


    def _on_selected_sheets_changed(self, idx, state):
        selects = self._sheets.selects
        selects[idx] = True if state == Qt.Checked else False
        sheets = [self._sheets.sheets[i] for i, s in enumerate(selects) if s]
        self.onSelectedSheetsChanged.emit(sheets)

    @property
    def selected_sheets(self) -> list[str]:
        return [self._sheets.sheets[i] for i, s in enumerate(self._sheets.selects) if s]

    @property
    def bias(self) -> tuple[int, int]:
        return self._bias_x.value(), self._bias_y.value()

    @property
    def target(self) -> tuple[int, int]:
        return self._target_x.value(), self._target_y.value()

    @property
    def delta(self) -> tuple[int, int]:
        return self._delta_x.value(), self._delta_y.value()

    def _on_value_changed(self, *args):
        self._shower.bias = (self._bias_x.value(), self._bias_y.value())
        self._shower.target = (self._target_x.value(), self._target_y.value())
        self._shower.delta = (self._delta_x.value(), self._delta_y.value())
        self._shower.update()

    def _on_excel_changed(self, path):
        self._sheets.path = path
        self._excelslot.reheight(ARIAL_FONT)
        self.onExcelChanged.emit(path)

    def _on_cst_changed(self, path):
        self._cstslot.reheight(ARIAL_FONT)
        self.onCstChanged.emit(path)

    @property
    def cst_type(self) -> str:  # like 'txt' or 'cst'
        return self._cstslot.filetype

class QPiosTableSelectors(QWidget):
    def __init__(self, parent=None):
        super(QPiosTableSelectors, self).__init__(parent)
        self.initUI()
        self._pios:list[PhysicsIoDef] = []

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(1, 1, 1, 1)
        self._layout.setSpacing(1)
        self.setLayout(self._layout)
        self._checklst = QCheckedListWidget()
        self._layout.addWidget(self._checklst)

    @property
    def pios(self):
        return self._pios

    @pios.setter
    def pios(self, pios):
        self._pios = pios
        self._update_checks()

    @property
    def selects(self):
        return self._checklst.selects

    @property
    def seleted_pios(self):
        return [pio for pio, s in zip(self._pios, self.selects) if s]

    def _update_checks(self):
        self._checklst.clear()
        for pio in self._pios:
            if pio.hiden: continue
            self._checklst.addItem(f"{pio.name}{pio.widthdef}", checked=True if pio.stared else False)

class QExcelTableExportor(QWidget):
    def __init__(self, parent=None):
        super(QExcelTableExportor, self).__init__(parent)
        self.initUI()
        self._excel = None
        if FSV['sv', 'last_excel']:
            self._left._excelslot.setPath(FSV['sv', 'last_excel'])
        if FSV['sv', 'last_cstfmt']:
            self._left._cstslot.setPath(FSV['sv', 'last_cstfmt'])



    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)
        self._left = QExcelFileHeaderCollector()
        self.layout.addWidget(self._left)
        self._right = QPiosTableSelectors()
        self.layout.addWidget(self._right)

        self._left.onExcelChanged.connect(self._on_excel_changed)
        self._left.onSelectedSheetsChanged.connect(self._update_pios)
        self._left.onCstChanged.connect(self._on_cst_changed)

    @property
    def excel(self):
        return self._excel

    def _on_excel_changed(self, path):
        FSV['sv', 'last_excel'] = path
        if not path:
            self._excel = None
        else:
            self._excel = pd.ExcelFile(path)
        self._update_pios(self._left.selected_sheets)

    def _on_cst_changed(self, path):
        FSV['sv', 'last_cstfmt'] = path

    def _update_pios(self, selected_sheets):
        if self._excel is None:
            self._right.pios = []
            return
        # try:
        pios = tbl_export_read(self._excel, self._left.bias, self._left.target, self._left.delta, sheets=selected_sheets)
        # except Exception as e:
        #     PopError("读取失败", f"读取excel文件失败, 请检查bias target delta: {e}")
        #     return
        self._right.pios = pios


    def export(self, path, overwrite=False):
        if not self._left.cst_type:
            raise ValueError("请指定cst文件")
        txt_tpl = auto_open(self._left._cstslot.path)
        dirname, basename = os.path.split(path)
        fname, ftype = os.path.splitext(basename)
        vfpath = os.path.join(dirname, fname + '.v')
        cstpath = os.path.join(dirname, fname + f'{self._left.cst_type}')

        if not overwrite:
            if os.path.exists(vfpath) or os.path.exists(cstpath):
                raise FileExistsError(f"文件已存在: \n\t'{vfpath}' \nor \n\t'{cstpath}'")

        # 如果vfpath存在, 那么提取目标的用户代码
        old_code = None
        if os.path.exists(vfpath):
            with open(vfpath, 'r') as f:
                old_code = f.read()

        # 生成新的代码
        top_str = GenerateVerilogTopModule(self._right.seleted_pios, old_code)
        cst_str = EvalCst(txt_tpl, self._right.seleted_pios)


        with open(vfpath, 'w') as f:
            f.write(top_str)
        with open(cstpath, 'w') as f:
            f.write(cst_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QExcelTableExportor()
    w.show()
    sys.exit(app.exec_())


