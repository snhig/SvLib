import csv
import os
import sys
from typing import Optional

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal,QPointF
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QApplication, QFileDialog, QPushButton, QToolBar, QVBoxLayout, QWidget, QMenu, QInputDialog

class SvSimplePlot(QWidget):
    """
    Inputs:
        parent: Parent widget
        y_label: Y-axis label
        x_label: X-axis label
        bg_color: Background color
        line_color: Color of the line
    """
    vertical_line_moved = Signal(float) # position
    def __init__(
        self,
        y_label: str = "Value (unit)",
        x_label: str = "Time (s)",
        bg_color: tuple = (0, 0, 0),
        line_color: tuple = (255, 255, 255),
        sim: bool = False,
    ):
        super().__init__()
        self.start_time = 0
        self.time = self.start_time
        self.x_label = x_label
        self.y_label = y_label
        self.bg_color = bg_color
        self.line_color = line_color

        # self.data = np.zeros(1000)
        self.line_color = line_color
        self.data = []
        self.custom_markers = []
        self.create_ui()

    def create_ui(self):
        self.curve = pg.ScatterPlotItem()
        self.plot = pg.PlotWidget()
        self.plot.getPlotItem().setMenuEnabled(False)
        self.plot.setLabel("left", self.y_label)
        self.plot.setLabel("bottom", self.x_label)
        self.plot.setBackground(QColor(self.bg_color[0], self.bg_color[1], self.bg_color[2]))
        self.plot.addItem(self.curve)
        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        self.setLayout(layout)
        self.toolbar = QToolBar()
        self.toolbar.setOrientation(Qt.Horizontal)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        
        
        self.save_action = QAction("Save CSV", self)
        self.save_action.triggered.connect(self.save_csv)

        # self.load_Action = QAction("Load CSV", self)
        # self.load_Action.triggered.connect(self.load_data)

        self.max_button = QPushButton("Mark Max")
        self.max_button.clicked.connect(self.mark_max)

        self.toolbar.addAction(self.save_action)
        # self.toolbar.addAction(self.load_Action)
        self.toolbar.addWidget(self.max_button)

        layout.setMenuBar(self.toolbar)
        self.peak_lines = []
        self.vertical_line = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen((188, 56, 251, 100), width=5))
        self.vertical_line.addMarker('<|>', position=1, size=15)
        self.vertical_line.addMarker('<|>', position=0, size=15)
        self.plot.addItem(self.vertical_line)
        self.vertical_line.setMovable(True)
        self.vertical_line.sigPositionChanged.connect(lambda: self.vertical_line_moved.emit(self.vertical_line.value()))
        self.horizontal_line = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen("g", width=1))
        self.plot.addItem(self.horizontal_line)

    def update_xs_ys(self, xs, ys, labels=None):

        self.data = [xs, ys]
        # print(self.data)
        # add plot data
        self.curve.clear()
        self.curve = pg.ScatterPlotItem(brush=pg.mkBrush(255, 255, 255, 150))

        if labels is not None:
            self.plot.setLabel("left", labels[1])
            self.plot.setLabel("bottom", labels[0])
        self.curve.setData(
            x=np.array(xs),
            y=np.array(ys),
            hoverable=True,
            hoverSize=15,
            hoverBrush=pg.mkBrush(158, 219, 251, 150),
            size=8,
        )
        self.plot.addItem(self.curve)

    def mark_max(self):
        x, y = self.get_x_of_max_y(), np.max(self.data[1])
        self.vertical_line.setPos(x)
        self.horizontal_line.setPos(y)


        self.max_button.setText(f"Mark Max: ( {x}, {y} )")
        self.vertical_line_moved.emit(self.vertical_line.value())

        # add marker lines

    def mark_peaks(self, peak_indexes):
        for i in self.peak_lines:
            self.plot.removeItem(i)
        for i in peak_indexes:
            line = pg.InfiniteLine(pos=self.data[0][i], angle=90, pen=pg.mkPen("b", width=1))
            self.plot.addItem(line)
            self.peak_lines.append(line)
            pg.InfLineLabel(
                    line,
                    text=f"{i}",
                    position=0.10,
                    rotateAxis=(1, 0),
                    anchor=(1, 1),
                )

    def save_csv(self):
        fname = QFileDialog.getSaveFileName(self, "Save file", os.getcwd())
        if fname[0] != "":
            with open(fname[0], "w") as f:
                writer = csv.writer(f)
                writer.writerow([self.x_label, self.y_label])
                for i in range(len(self.data[0])):
                    writer.writerow([self.data[0][i], self.data[1][i]])

    def load_data(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", os.getcwd())
        if fname[0] != "":
            with open(fname[0], "r") as f:
                self.csv_reader = csv.reader(f)
                self.csv_reader = list(self.csv_reader)
                titles = self.csv_reader[0]
                self.csv_reader = self.csv_reader[1:]
                self.csv_reader = [[float(i) for i in j] for j in self.csv_reader]
                self.csv_reader = list(zip(*self.csv_reader))

                # print(self.csv_reader[0])
                self.update_xs_ys(list(self.csv_reader[0]), list(self.csv_reader[1]), labels=titles)

    def get_x_of_max_y(self):
        return self.data[0][np.argmax(self.data[1])]

    def add_marker(self, x, label, moveable=False):
        marker = pg.InfiniteLine(pos=x, angle=90, pen=pg.mkPen((255,255,255.150), width=1), label=label)
        marker.setMovable(moveable)
        self.custom_markers.append(marker)
        self.plot.addItem(marker)

    def contextMenuEvent(self, event):
        menu = QMenu()
        view_all = menu.addAction("View All")
        add_vertical_maker = menu.addAction("Add Vertical Marker")
        remove_markers = menu.addAction("Remove Marker")
        
        
        action = menu.exec(self.mapToGlobal(event.pos()))

        if action == view_all:
            self.plot.autoRange()
        if action == remove_markers:
            gpt = event.pos()
            position = self.plot.plotItem.vb.mapSceneToView(gpt)
            spos_x = position.x()
            #remove marker with closest X coord
            closest = None
            closest_diff = float('inf')
            for marker in self.custom_markers:
                diff = abs(marker.value() - spos_x)
                if diff < closest_diff:
                    closest = marker
                    closest_diff = diff

            self.plot.removeItem(closest)

        if action == add_vertical_maker:
            gpt = event.pos()
            position = self.plot.plotItem.vb.mapSceneToView(gpt)
            spos_x = position.x()
            #position, etc = QInputDialog.getDouble(self, "Add Marker", "Enter Marker Position (can be dragged to new position later)")
            
            text,tf = QInputDialog.getText(self, "Add Marker", "Enter Marker Name")
            if text == "":
                return
            
            self.add_marker(spos_x, text, moveable=True)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimplePlot()
    window.show()
    sys.exit(app.exec())