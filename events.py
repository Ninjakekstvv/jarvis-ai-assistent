from PySide6.QtCore import QObject, Signal


class JarvisEvents(QObject):

    show_programs = Signal()


events = JarvisEvents()