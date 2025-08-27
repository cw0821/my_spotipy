import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPainterPath
from PyQt6.QtCore import QRect, Qt, QPointF
from my_spotipy import get_current_track, get_playback_state, play_playback, pause_playback, fast_forward, rewind_playback

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

        # Hover states
        self.hover_blue = False
        self.hover_green = False
        self.hover_grey = False
        
        # Button rectangles
        self.rewind_rect = QRect()
        self.play_pause_rect = QRect()
        self.fast_forward_rect = QRect()

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.is_playing = False


    def paintEvent(self, event):
        painter = QPainter(self)

        # Calculate positions
        center_x = self.width() // 2
        center_y = self.height() // 2

        self.blue_rect = QRect(center_x - self.rect_width, center_y - self.rect_height//2,
                               self.rect_width, self.rect_height)
        self.green_rect = QRect(center_x, center_y - self.rect_height//2,
                                self.rect_width, self.rect_height)
        
        grey_top = center_y + self.rect_height // 2
        self.grey_rect = QRect(center_x - self.rect3_width//2,
                               grey_top,
                               self.rect3_width, self.rect3_height)

        # Update button positions
        button_height = self.grey_rect.height()
        button_width = button_height * 0.8
        padding = (self.grey_rect.width() - (button_width * 3)) // 4
        
        # Fixed the TypeError by casting to int
        self.rewind_rect = QRect(int(self.grey_rect.x() + padding), int(self.grey_rect.y()), int(button_width), int(button_height))
        self.play_pause_rect = QRect(int(self.grey_rect.x() + (padding * 2) + button_width), int(self.grey_rect.y()), int(button_width), int(button_height))
        self.fast_forward_rect = QRect(int(self.grey_rect.x() + (padding * 3) + (button_width * 2)), int(self.grey_rect.y()), int(button_width), int(button_height))

        # Draw grey rectangle if hovering over blue or green or grey
        if self.hover_blue or self.hover_green or self.hover_grey:
            painter.fillRect(self.grey_rect, QColor("lightgrey"))
            
            # Draw rewind button
            painter.setPen(QColor(Qt.GlobalColor.black))
            painter.setBrush(QColor(Qt.GlobalColor.black))
            rewind_path = QPainterPath()
            rewind_path.moveTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.7, self.rewind_rect.center().y())
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.3, self.rewind_rect.top() + self.rewind_rect.height() * 0.2)
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.3, self.rewind_rect.bottom() - self.rewind_rect.height() * 0.2)
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.7, self.rewind_rect.center().y())
            rewind_path.moveTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.3, self.rewind_rect.center().y())
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.1, self.rewind_rect.top() + self.rewind_rect.height() * 0.2)
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.1, self.rewind_rect.bottom() - self.rewind_rect.height() * 0.2)
            rewind_path.lineTo(self.rewind_rect.x() + self.rewind_rect.width() * 0.3, self.rewind_rect.center().y())
            painter.drawPath(rewind_path)
            
            # Draw fast forward button
            fast_forward_path = QPainterPath()
            fast_forward_path.moveTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.3, self.fast_forward_rect.center().y())
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.7, self.fast_forward_rect.top() + self.fast_forward_rect.height() * 0.2)
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.7, self.fast_forward_rect.bottom() - self.fast_forward_rect.height() * 0.2)
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.3, self.fast_forward_rect.center().y())
            fast_forward_path.moveTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.7, self.fast_forward_rect.center().y())
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.9, self.fast_forward_rect.top() + self.fast_forward_rect.height() * 0.2)
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.9, self.fast_forward_rect.bottom() - self.fast_forward_rect.height() * 0.2)
            fast_forward_path.lineTo(self.fast_forward_rect.x() + self.fast_forward_rect.width() * 0.7, self.fast_forward_rect.center().y())
            painter.drawPath(fast_forward_path)

            # Draw play/pause button based on state
            self.is_playing = (get_playback_state() == "playing")
            if self.is_playing:
                # Draw pause button
                pause_width = self.play_pause_rect.width() * 0.2
                pause_gap = self.play_pause_rect.width() * 0.15
                pause_height = self.play_pause_rect.height() * 0.6
                pause_x = self.play_pause_rect.center().x() - pause_width - (pause_gap / 2)
                
                # Fixed the TypeError by casting to int
                painter.drawRect(int(pause_x), int(self.play_pause_rect.center().y() - pause_height / 2), int(pause_width), int(pause_height))
                painter.drawRect(int(pause_x + pause_width + pause_gap), int(self.play_pause_rect.center().y() - pause_height / 2), int(pause_width), int(pause_height))
            else:
                # Draw play button
                play_path = QPainterPath()
                play_path.moveTo(self.play_pause_rect.x() + self.play_pause_rect.width() * 0.2, self.play_pause_rect.top() + self.play_pause_rect.height() * 0.2)
                play_path.lineTo(self.play_pause_rect.x() + self.play_pause_rect.width() * 0.8, self.play_pause_rect.center().y())
                play_path.lineTo(self.play_pause_rect.x() + self.play_pause_rect.width() * 0.2, self.play_pause_rect.bottom() - self.play_pause_rect.height() * 0.2)
                play_path.lineTo(self.play_pause_rect.x() + self.play_pause_rect.width() * 0.2, self.play_pause_rect.top() + self.play_pause_rect.height() * 0.2)
                painter.drawPath(play_path)


        # Draw blue rectangle
        painter.fillRect(self.blue_rect, QColor("lightblue"))
        
        # Draw green rectangle
        painter.fillRect(self.green_rect, QColor("lightgreen"))

        # Draw text
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        painter.setPen(QColor("black"))
        if self.hover_blue:
            painter.drawText(self.blue_rect, Qt.AlignmentFlag.AlignCenter, "BLUE")
        
        # Set font for the green rectangle text
        painter.setFont(QFont("Helvetica", 9))

        # This text will always be drawn
        track_info = get_current_track()
        if "Spotify is not running" in track_info:
            text_to_display = "Spotify is not running."
        else:
            lines = track_info.split('\n')
            track = lines[0].split(': ')[1]
            artist = lines[1].split(': ')[1]
            album = lines[2].split(': ')[1]
            # Updated the format string to place each part on a new line
            text_to_display = f"{track}\n{artist}\n{album}"
        
        # Use QRect to help with text layout over the rectangle.
        painter.drawText(self.green_rect, Qt.AlignmentFlag.AlignCenter, text_to_display)


    def mousePressEvent(self, event):
        pos = event.position() if callable(event.position) else event.pos()
        if self.rewind_rect.contains(pos.toPoint()):
            rewind_playback()
            self.update()
        elif self.play_pause_rect.contains(pos.toPoint()):
            if self.is_playing:
                pause_playback()
            else:
                play_playback()
            self.update()
        elif self.fast_forward_rect.contains(pos.toPoint()):
            fast_forward()
            self.update()
            
    def mouseMoveEvent(self, event):
        pos = event.position() if callable(event.position) else event.pos()
        x, y = pos.x(), pos.y()

        # Update hover states for all three rectangles
        self.hover_blue = self.blue_rect.contains(int(x), int(y))
        self.hover_green = self.green_rect.contains(int(x), int(y))
        self.hover_grey = self.grey_rect.contains(int(x), int(y))

        # Grey rectangle appears if hovering over any of the three
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RectangleWidget()
    widget.show()
    sys.exit(app.exec())