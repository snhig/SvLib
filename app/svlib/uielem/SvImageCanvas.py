from PySide6.QtCore import Signal, Qt, QTimer, QEvent, QPointF, Slot
from PySide6.QtGui import QAction, QActionGroup, QMouseEvent
from PySide6.QtWidgets import QApplication, QCheckBox, QFileDialog, QHBoxLayout,QMenu, QWidget, QVBoxLayout, QSlider, QLabel, QToolBar, QSplitter, QTabWidget, QDoubleSpinBox, QPushButton, QGridLayout, QSpinBox, QFormLayout, QProgressBar, QGraphicsSceneContextMenuEvent
import pyqtgraph as pg
import cv2
# from SvJoyStick import JoystickButton
class SvROI(pg.ROI):
    regionChangedSignal = Signal(tuple, tuple) # (origin[tuple], size[tuple])
    def __init__(self, name:str, parent=None, pos=[0,0], size=[0,0], pen=pg.mkPen('r', width=2), **args):
        super().__init__( pos, size, parent=parent, pen=pen, **args)
        self.setVisible(False)
        self.addScaleHandle([1,1], [0,0])
        self.my_name = name
        
        self.sigRegionChangeFinished.connect(self._regionChangedSlot)
     
    @Slot()   
    def _regionChangedSlot(self):
        pos = self.pos() # origin (x,y)
        wh = self.size() # (width, height)
        self.regionChangedSignal.emit(pos, wh)

class SvImageCanvas(QWidget):
    """A widget for displaying images with additional functionality such as point-click events and ROI selection."""
    point_clicked = Signal(list) # [xyPoint[list], img_shape[list]] -> [ [int(pos.x()), int(pos.y())], img.shape ]
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.click_move_enabled = False
        self.normalize = False
        self.histogram_visible = False
        self.image_shape = (0,0)
        self._init_gui()
        self.last_unprocessed_frame = None
        self.roi_enabled = False
        self.roi_counter = 0
    def _init_gui(self):
        pg.setConfigOption('imageAxisOrder', 'row-major')
        self.lyout = QHBoxLayout()
        # self.imv.view.setBackgroundColor('black')
        self.graphics_view = pg.GraphicsLayoutWidget()
        self.vb = pg.ViewBox(lockAspect=True, enableMenu=False, invertY=True)
        self.graphics_view.addItem(self.vb)
        self.imv = pg.ImageItem()
        self.vb.addItem(self.imv)
        # self.lyout.addWidget(JoystickButton())
        
        
        
        self.roi = SvROI('tester', parent=self.imv)
        # pg.ROI( [0,0], [0,0], pen=pg.mkPen('r', width=2),parent=self.vb)
        self.roi.setVisible(False)
        
        self.roi_widget = QWidget()
        
        self.roi_widget.setWindowTitle("ROI Settings")
        self.roi_widget.setMinimumWidth(200)
        self.roi_form_layout = QFormLayout()
        self.roi_widget.setLayout(self.roi_form_layout)
        self.roi_widget.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.roi_widget.setVisible(False)
        self.roi_width_spin = QSpinBox()
        self.roi_width_spin.setRange(0, 9999999)
        self.roi_width_spin.setValue(0)
        self.roi_width_spin.valueChanged.connect(lambda val: self.roi.setSize([val, self.roi.size()[1]]))
        self.roi_height_spin = QSpinBox()
        self.roi_height_spin.setRange(0, 9999999)
        self.roi_height_spin.setValue(0)
        self.roi_height_spin.valueChanged.connect(lambda val: self.roi.setSize([self.roi.size()[0], val]))
        self.roi_form_layout.addRow("Width", self.roi_width_spin)
        self.roi_form_layout.addRow("Height", self.roi_height_spin)
        
        self.roi_pos_x_spin = QSpinBox()
        self.roi_pos_x_spin.setRange(0, 9999999)
        self.roi_pos_x_spin.setValue(0)
        self.roi_pos_x_spin.valueChanged.connect(lambda val: self.roi.setPos([val, self.roi.pos()[1]]))
        self.roi_pos_y_spin = QSpinBox()
        self.roi_pos_y_spin.setRange(0, 9999999)
        self.roi_pos_y_spin.setValue(0)
        
        self.roi_pos_y_spin.valueChanged.connect(lambda val: self.roi.setPos([self.roi.pos()[0], val]))
        self.roi_form_layout.addRow("X", self.roi_pos_x_spin)
        self.roi_form_layout.addRow("Y", self.roi_pos_y_spin)
        
        #self.roi.addFreeHandle([0,0])
        #self.vb.addItem(self.roi)
        
        
        
        self.roi.regionChangedSignal.connect(self.roi_pos_changed_slot)
        #histogram properties
        # self.imv.ui.histogram.fillHistogram(fill=False)
        # self.imv.ui.histogram.autoHistogramRange()
        # self.imv.ui.histogram.plot.setBrush((200,200,0))
        # self.imv.roi.removeHandle(1)
        # self.imv.ui.menuBtn.deleteLater()
        # self.imv.ui.roiBtn.deleteLater()
        # self.imv.view.invertY()
       # self.hist.autoHistogramRange()
        self.lyout.addWidget(self.graphics_view)
        self.setLayout(self.lyout)
        
        # allow for mouse click event
        self.imv.scene().sigMouseClicked.connect(self.mouseClickEvent)
        # Context Menu Events
        
        self.view_all_action = QAction("View All", self)
        self.roi_settings_action = QAction("ROI Settings", self)
        self.center_roi_action = QAction("Center ROI", self)
        self.toggle_roi_action = QAction("ROI", self)
        self.toggle_roi_action.setCheckable(True)
        self.toggle_roi_action.setChecked(False)
        
        self.menu_actions = {
            self.view_all_action: self.vb.autoRange,
            self.roi_settings_action: self.bring_roi_settings,
            self.center_roi_action: self.center_roi,
            self.toggle_roi_action: self.toggle_roi
        }

    #     self.imv.view.setBackgroundColor('w')
    
    
    def bring_roi_settings(self):
        self.roi_widget.setVisible(True)
        self.roi_widget.setFocus()
        
    def toggle_roi(self):
        if self.roi_counter <= 0 and self.last_unprocessed_frame is not None:
            self.roi.setSize([self.last_unprocessed_frame.shape[1], self.last_unprocessed_frame.shape[0]])
            self.roi_counter += 1
        self.roi.setVisible(self.toggle_roi_action.isChecked())
        print(f'{self.getArrayRegion(self.last_unprocessed_frame)} ROI')
    
    def update_image(self, img):
        pass

    def getArrayRegion(self, external_img):
        tup = self.roi.getArraySlice(external_img, self.imv, returnSlice=False)
        return tup[0]
    
    def histogram_toggle(self, force=None):
        pass

    def center_roi(self):
        image_shape = self.image_shape
        roi_pos = self.roi.size()
        self.roi.setPos([image_shape[1]/2 - roi_pos[0]//2, image_shape[0]/2-roi_pos[1]//2])

    @Slot()
    def normalize_pressed(self):
        """Slot for the normalize checkbox."""
        if self.normalize:
            im = self.imv.getProcessedImage()
            self.imv.setImage(im, autoRange=False, autoLevels=True)
        else:
            self.update_image(self.last_unprocessed_frame)      

    ## POINT CLICK FUNCTION HERE
    @Slot()
    def mouseClickEvent(self, event: QMouseEvent):
        if event.button() != Qt.LeftButton:
            return
        pos = QPointF(event.pos())
        # Convert the mouse position to pixel coordinates
        pos = self.imv.mapFromScene(pos)
        # Get the pixel value at the clicked position
        ptt = [int(pos.x()), int(pos.y())]
        print(f'Clicked pixel: {ptt}, image shape: {self.image_shape}')
        self.point_clicked.emit([ptt, self.image_shape])
    @Slot()
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        for action in self.menu_actions.keys():
            menu.addAction(action)
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action in self.menu_actions:
            self.menu_actions[action]()
            
    @Slot()
    def click_move_slot(self, enable):
        self.click_move_enabled = enable
           
    @Slot()    
    def roi_pos_changed_slot(self, pos, wh):
        pos = pos
        wh = wh
        self.roi_pos_x_spin.setValue(pos[0])
        self.roi_pos_y_spin.setValue(pos[1])
        self.roi_width_spin.setValue(wh[0])
        self.roi_height_spin.setValue(wh[1])
        
class SvImageCanvasMono(SvImageCanvas):
    """A widget for displaying monochrome images with additional functionality such as point-click events and ROI selection."""
    point_clicked = Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hist = pg.HistogramLUTWidget(image=self.imv, levelMode='mono', orientation='vertical')
        self.hist.autoHistogramRange()
        self.hist.setVisible(False)
        self.lyout.addWidget(self.hist)
    
        self.histogram_action = QAction("Histogram", self)
        self.histogram_action.setCheckable(True)
        self.histogram_action.setChecked(False)
        self.menu_actions[self.histogram_action] = self.histogram_toggle

    
    def update_image(self, img):
        self.imv.clear()
        # if image is monochrome
        self.last_unprocessed_frame = img
        self.image_shape = img.shape
        self.imv.setImage(img, autoRange=False, autoLevels=False, levels=(0,255), levelMode='mono') if not self.normalize else self.imv.setImage(img, autoRange=False, autoLevels=True, levelMode='mono')

    def histogram_toggle(self, force=None):
        if self.hist.isVisible():
            self.hist.hide()
        else:
            self.hist.show()
            
            
    

class SvImageCanvasRGB(SvImageCanvas):
    """A widget for displaying RGB images with additional functionality such as point-click events and ROI selection."""
    point_clicked = Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hist = pg.HistogramLUTWidget(image=self.imv, levelMode='rgba', orientation='horizontal')
        self.hist.autoHistogramRange()
        self.hist.setVisible(False)
        self.lyout.addWidget(self.hist)
    
        self.histogram_action = QAction("Histogram", self)
        self.histogram_action.setCheckable(True)
        self.histogram_action.setChecked(False)
        self.menu_actions[self.histogram_action] = self.histogram_toggle
    
    def update_image(self, img):
        self.imv.clear()
        self.last_unprocessed_frame = img
        self.image_shape = img.shape
        self.imv.setImage(img, autoRange=False, autoLevels=False, levels=(0,255),) if not self.normalize else self.imv.setImage(img, autoRange=False,autoLevels=True)
        lvl=self.imv.getLevels()
        self.hist.item.setLevels(min=0, max=255)
        
    def histogram_toggle(self, force=None):
        if self.hist.isVisible():
            self.hist.hide()
        else:
            self.hist.show()    
        
        
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    wid = QWidget()
    lay = QHBoxLayout()
    wid.setLayout(lay)
    w = SvImageCanvasMono(parent=wid)
    lay.addWidget(w)
    
    wr = SvImageCanvasRGB(parent=wid)
    lay.addWidget(wr)
    
    load_button = QPushButton("Load Image")
    lay.addWidget(load_button)
    load_button.clicked.connect(lambda: w.update_image(cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)))
    load_button.clicked.connect(lambda: wr.update_image(cv2.cvtColor(cv2.imread("test_image.jpg", cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)))
    
    wid.show()
    sys.exit(app.exec())