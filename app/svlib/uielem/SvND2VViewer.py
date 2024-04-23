from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
import nd2
from typing import Optional
class SvND2Canvas(QWidget):
    def __init__(self, Parent: Optional[QWidget] = None, nd2_filepath:str=None):
        super().__init__()
        pg.setConfigOptions(imageAxisOrder="row-major")
        self.lyout = QHBoxLayout()
        self.imv = pg.ImageView(levelMode="mono")
        self.hist = self.imv.getHistogramWidget()
        self.Parent = Parent
        # histogram properties
        self.imv.ui.histogram.fillHistogram(fill=False)
        self.imv.ui.histogram.autoHistogramRange()
        self.imv.ui.histogram.plot.setBrush((200, 200, 0))
        self.imv.roi.removeHandle(1)
        self.imv.view.invertY()
        self.lyout.addWidget(self.imv)
        self.setLayout(self.lyout)
        
        self.nd2_array = None
        self.nd2_events = None
        
        self.nd2_filepath = nd2_filepath
        if self.nd2_filepath != None:
            self.load_nd2(self.nd2_filepath)
            
    def load_nd2(self, filepath:str):
        with nd2.ND2File(filepath) as f:
            print(f.sizes)
            self.nd2_array = f.asarray()
            self.nd2_events = f.events()
            
        self.imv.setImage(self.nd2_array)
        