from svlib.uielem import SvImageCanvasRGB
from PySide6.QtWidgets import QApplication, QFileDialog
import sys
import cv2
# Create QApplication instance
app = QApplication([])


# create a SvImageCamvasRGB widget

image_canvas = SvImageCanvasRGB()

# get file from file dialog
file = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg *.tif *.tiff)")[0]

if file != '':
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_canvas.update_image(img)
    
image_canvas.show()

app.exec()