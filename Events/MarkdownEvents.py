from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QTextEdit
import markdown


class MarkdownFocusHandler(QObject):
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        self._raw_markdown = None
        self._is_being_edited = False
        self.text_edit.installEventFilter(self)

    @property
    def raw_markdown(self) -> str:
        return self._raw_markdown or ""

    @property
    def is_editing(self) -> bool:
        return self._is_being_edited

    def stop_editing(self):
        self._is_being_edited = False

    def render_markdown(self):
        self._raw_markdown = self.text_edit.toPlainText()
        rendered_html = markdown.markdown(self.raw_markdown)
        self.text_edit.setHtml(rendered_html)

    def eventFilter(self, obj: QObject, event: QEvent):
        if obj == self.text_edit and self.raw_markdown is not None:
            if event.type() == QEvent.FocusIn:
                self.text_edit.setPlainText(self.raw_markdown)
                self._is_being_edited = True
            elif event.type() == QEvent.FocusOut:
                self._is_being_edited = False
                self.render_markdown()

        return super().eventFilter(obj, event)
