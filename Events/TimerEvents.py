from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtCore import QTimer, QTime

class TimerEvents(QTimer):
    def __init__(self, time_display: QTimeEdit):
        super().__init__()
        self.setInterval(60_000) # Trigger once per minute
        self.timeout.connect(self.update_time)
        self.time_display = time_display
        self._recording = False

    def update_time(self):
        current_time = self.time_display.time()
        new_time = current_time.addSecs(60)
        self.time_display.setTime(new_time)

    def stop_recording(self):
        self._recording = False
        self.stop()

    def toggle_recording(self) -> bool:
        self._recording = not self._recording
        if self._recording:
            self.start()
        else:
            self.stop()
        return self._recording
