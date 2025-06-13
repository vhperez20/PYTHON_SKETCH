import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QTabletEvent
from PyQt5.QtCore import Qt, QPoint

class TabletSketch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Tablet Sketch Pad")
        self.resize(800, 600)
        self.lines = []
        self.setAttribute(Qt.WA_StaticContents)

    def tabletEvent(self, event: QTabletEvent):
        print("Tablet event received!")
        print("Type:", event.type())
        print("Pressure:", event.pressure())
        print("Position:", event.pos())
        print("Device:", event.device())
        print("Pointer type:", event.pointerType())
    
    if event.type() == QTabletEvent.TabletMove:
        pressure = event.pressure()
        pen_width = int(pressure * 10)
        line = (self.last_point, event.pos(), pen_width)
        self.lines.append(line)
        self.last_point = event.pos()
        self.update()
    elif event.type() == QTabletEvent.TabletPress:
        self.last_point = event.pos()
    event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        for start, end, width in self.lines:
            pen = QPen(Qt.black, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(start, end)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sketch = TabletSketch()
    sketch.show()
    sys.exit(app.exec_())

