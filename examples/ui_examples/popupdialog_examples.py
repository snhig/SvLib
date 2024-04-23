from svlib.uielem import SvPopupDialogs
from PySide6.QtWidgets import QApplication
import sys
# Create QApplication instance
app = QApplication([])

# Create an Information Dialog and run it

# This dialog was a default window modality descibed by the block_input=False parameter
# This means that the dialog will not block the main application window from running in the background
info_dialog = SvPopupDialogs.Information(parent=None,
                                         message="This is an information dialog",
                                         title="Information",
                                         block_input=False)

# execute the dialog and get the return value
rett = info_dialog.exec()
print(rett)


# Create Warning Dialog and run it

# This dialog was a default window modality descibed by the block_input=True parameter
# This means that the dialog will block the parent application window from running in the background
warning_dialog = SvPopupDialogs.Warning(parent=None,
                                         message="This is a warning dialog",
                                         title="Warning",
                                         block_input=True)

rett = warning_dialog.exec()
print(rett)

# Create Critical Dialog and run it

# This dialog was a default window modality descibed by the block_input=True parameter
# This means that the dialog will block the parent application window from running in the background
critical_dialog = SvPopupDialogs.Critical(parent=None,
                                         message="This is a critical dialog",
                                         title="Critical",
                                         block_input=True)

rett = critical_dialog.exec()
print(rett)



# close application instance if no dialogs are left to show
app.exec(sys.exit())