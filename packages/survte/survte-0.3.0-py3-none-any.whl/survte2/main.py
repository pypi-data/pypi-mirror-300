import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from landxml_viewer import LandXMLViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set the application style
    app.setStyle("Fusion")
    
    # Set a lighter color palette
    palette = app.palette()
    palette.setColor(palette.Window, QColor(240, 240, 240))
    palette.setColor(palette.WindowText, Qt.black)
    palette.setColor(palette.Base, QColor(255, 255, 255))
    palette.setColor(palette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.black)
    palette.setColor(palette.Text, Qt.black)
    palette.setColor(palette.Button, QColor(240, 240, 240))
    palette.setColor(palette.ButtonText, Qt.black)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Link, QColor(0, 0, 255))
    palette.setColor(palette.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    viewer = LandXMLViewer()
    viewer.show()
    sys.exit(app.exec_())


