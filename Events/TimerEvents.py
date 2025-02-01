''' Class links a timer that updates a time display every minute '''
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtCore import QTimer


class TimerEvents(QTimer):
    ''' Timer connected to qt time edit '''
    def __init__(self, time_display: QTimeEdit):
        super().__init__()
        self.setInterval(60_000)  # Trigger once per minute
        self.timeout.connect(self.update_time)
        self.time_display = time_display
        self._recording = False

    def update_time(self):
        ''' Increment time display '''
        current_time = self.time_display.time()
        new_time = current_time.addSecs(60)
        self.time_display.setTime(new_time)

    def stop_recording(self):
        ''' Stop recording time '''
        self._recording = False
        self.stop()

    def toggle_recording(self) -> bool:
        ''' Turn timing on and off '''
        self._recording = not self._recording
        if self._recording:
            self.start()
        else:
            self.stop()
        return self._recording
