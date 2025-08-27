import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import QRect, Qt

class RectangleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3-Rectangle Hover App")
        self.setGeometry(100, 100, 400, 300)

        # Rectangle dimensions
        self.rect_width = 100
        self.rect_height = 50
        self.rect3_width = 200
        self.rect3_height = 50
        self.gap = 20

        # Hover states
        self.hover_blue = False
        self.hover_green = False
        self.hover_grey = False

        # Enable mouse tracking for hover detection
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Calculate positions
        center_x = self.width() // 2
        center_y = self.height() // 2

        self.blue_rect = QRect(center_x - self.rect_width, center_y - self.rect_height//2,
                               self.rect_width, self.rect_height)
        self.green_rect = QRect(center_x, center_y - self.rect_height//2,
                                self.rect_width, self.rect_height)
        self.grey_rect = QRect(center_x - self.rect3_width//2,
                               center_y + self.rect_height//2 + self.gap,
                               self.rect3_width, self.rect3_height)

        # Draw grey rectangle if hovering over blue or green
        if self.hover_blue or self.hover_green or self.hover_grey:
            painter.fillRect(self.grey_rect, QColor("lightgrey"))

        # Draw blue rectangle
        painter.fillRect(self.blue_rect, QColor("lightblue"))
        # Draw green rectangle
        painter.fillRect(self.green_rect, QColor("lightgreen"))

        # Draw text if hovering
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        painter.setPen(QColor("black"))
        if self.hover_blue:
            painter.drawText(self.blue_rect, Qt.AlignmentFlag.AlignCenter, "BLUE")
        if self.hover_green:
            painter.drawText(self.green_rect, Qt.AlignmentFlag.AlignCenter, "GREEN")

    def mouseMoveEvent(self, event):
        # Correct handling for PyQt6: position() returns QPointF
        pos = event.position() if callable(event.position) else event.position
        x, y = pos.x(), pos.y()

        self.hover_blue = self.blue_rect.contains(int(x), int(y))
        self.hover_green = self.green_rect.contains(int(x), int(y))
        # Grey rectangle appears if hovering over any
        self.hover_grey = self.hover_blue or self.hover_green
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RectangleWidget()
    window.show()
    sys.exit(app.exec())
