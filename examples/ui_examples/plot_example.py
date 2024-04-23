from svlib.uielem import SvSimplePlot
from PySide6.QtWidgets import QApplication
import sys

# Create QApplication instance
app = QApplication([])

# create a SvSimplePlot widget
plot = SvSimplePlot()

# Add data to the plot
plot.update_xs_ys(
    xs = [i for i in range(10)],
    ys = [i**2 for i in range(10)],
)

plot.show()


app.exec()