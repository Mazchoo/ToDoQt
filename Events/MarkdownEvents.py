"""Filtering events to turn markdown display on and off"""

from PyQt5.QtCore import QObject, QEvent, pyqtSignal
from PyQt5.QtWidgets import QTextEdit
import markdown


class MarkdownFocusHandler(QObject):
    """When text edit selected, show raw markdown, when not selected show html of markdown"""

    # Qt signal emitted when focus is lost (editing complete)
    focusOut = pyqtSignal()

    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        self._raw_markdown = None
        self._is_being_edited = False
        self.text_edit.installEventFilter(self)

    @property
    def raw_markdown(self) -> str:
        """Return current markdown"""
        return self._raw_markdown or ""

    @property
    def is_editing(self) -> bool:
        """Return true if current markdown is being edited"""
        return self._is_being_edited

    def stop_editing(self):
        """Turn off editing status"""
        self._is_being_edited = False

    def render_markdown(self):
        """Convert raw edit text to display html of markdown"""
        self._raw_markdown = self.text_edit.toPlainText()
        rendered_html = markdown.markdown(self.raw_markdown)
        self.text_edit.setHtml(rendered_html)

    def eventFilter(self, obj: QObject, event: QEvent):
        """Filter events so the selected focusing on text edit changes display"""
        if obj == self.text_edit and self.raw_markdown is not None:
            if event.type() == QEvent.FocusIn:
                self.text_edit.setPlainText(self.raw_markdown)
                self._is_being_edited = True
            elif event.type() == QEvent.FocusOut:
                self._is_being_edited = False
                self.render_markdown()
                # Emit Qt signal when focus is lost (editing complete)
                self.focusOut.emit()

        return super().eventFilter(obj, event)
