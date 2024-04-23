import numpy as np
import nd2, cv2
from scipy.signal import find_peaks, peak_prominences 

# This file opens an ND2 file and gets the tenengrad score of each image in the file
# It then finds the two most prominent peaks in the scores and returns the indexes of those peaks
# This is useful for finding the two most in-focus images in a stack of images


def openND2fromPath(file_path)->nd2.ND2File:
    f = nd2.ND2File(file_path)
    return f

def get_tenengrad_score(im):
    # sobel 
    # covert to correct RGB format if needed
    #gray_img = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.GaussianBlur(im, (3, 3), 0)
    """Get the Tenengrad focus measure, which is a score that can be used relative to other images"""
    # Compute the x and y derivatives using the Sobel operator
    sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
    # Compute the gradient magnitude using the x and y derivatives
    grad_mag = np.sqrt(sobelx**2 + sobely**2)
    # Compute the Tenengrad focus measure as the sum of the gradient magnitudes squared
    tenengrad = np.sum(grad_mag**2)
    return tenengrad

def get_stack_scores_and_peak_idexes(nd2_file:nd2.ND2File):
    scores = []
    arr = nd2_file.asarray()
    event_data = nd2_file.events()
    for i in range(len(arr)):
        im = arr[i]
        im = im[1000:2000, 1000:2000]
        scores.append(get_tenengrad_score(im))
    peaks = find_peaks(scores) 
# get peak prominences
    prominences = peak_prominences(scores, peaks[0]) 
    # sorts peaks by prominences
    sort_peaks_by_promnence = sorted(zip(peaks[0], prominences[0]), key=lambda x: x[1], reverse=True) 

    # get the 2 most prominent peaks
    top_2_peaks = sort_peaks_by_promnence[:2]
    top_2_indexes = [i[0] for i in top_2_peaks]
    # get the two most prominent peaks in order
    top_2_indexes.sort()  
        
    return scores, top_2_indexes


from svlib.uielem import SvSimplePlot, SvImageCanvasMono
from PySide6.QtWidgets import QApplication, QTabWidget
from PySide6.QtCore import Qt
FP = 'example.nd2'
f = openND2fromPath('example.nd2')

scores, peaks = get_stack_scores_and_peak_idexes(f)

print(scores)
print(peaks)

app = QApplication([])
plot = SvSimplePlot()
view = QTabWidget()




for wid in [plot, view]:
    wid.setWindowFlags(Qt.WindowStaysOnTopHint)

plot.update_xs_ys(range(len(scores)), scores)

for p in peaks:
    plot.add_marker(p, str(p))


# get only the images bounded "inclusively" by the two most prominent peaks
uncropped_arr = f.asarray()
uncropped_arr  = [cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX) for im in uncropped_arr]
# cropped_arr = f.asarray()[peaks[0]: peaks[1]+1]
# normalize images to 8 bit
# cropped_arr = [cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX) for im in cropped_arr]

for im in range(len(uncropped_arr)):
    canvas = SvImageCanvasMono(parent=view)
    view.addTab(canvas, str(im))
    canvas.update_image(uncropped_arr[im])
    
# bind the signals from the current SvImageCanvasMono and the vertical lines on the SvSimplePlot
    
plot.vertical_line_moved.connect(lambda x: view.setCurrentIndex(x))
view.currentChanged.connect(lambda x: plot.vertical_line.setPos(x))

plot.show()
view.show()
app.exec()
f.close()
