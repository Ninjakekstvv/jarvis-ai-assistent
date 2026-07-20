"""Animiertes deutsches JARVIS-3D-Dashboard.

Starten mit:  python ui.py
"""

import math
import random
import sys
import os
import tempfile
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QRectF
from events import events
from PySide6.QtNetwork import QLocalServer
from ipc import SERVER_NAME
from programs_window import ProgramsWindow
from programs_window import ProgramsWindow
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QApplication, QWidget
from voice_state import get_voice_state, launcher_is_alive


class JarvisUI(QWidget):
    """Ein responsives HUD, das vollständig mit Qt gezeichnet wird."""

    ORANGE = QColor("#ff6a21")
    BRIGHT_ORANGE = QColor("#ff9b52")
    GREEN = QColor("#79e8a2")
    BG = QColor("#101218")
    PANEL = QColor("#171a22")
    LINE = QColor("#3c3030")
    MUTED = QColor("#8f827d")
    LISTEN = QColor("#4de1c1")
    THINK = QColor("#c18cff")

    def handle_connection(self):

        socket = self.server.nextPendingConnection()

        socket.readyRead.connect(
            lambda s=socket: self.read_command(s)
        )


    def read_command(self, socket):

        command = bytes(socket.readAll()).decode().strip()

        print("IPC:", command)

        if command == "SHOW_PROGRAMS":
            self.show_programs_window()

        elif command == "CLOSE_PROGRAMS":
            self.close_programs_window()

        socket.disconnectFromServer()

    VOICE_STATES = {
        "idle": ("STANDBY", "BEREIT FÜR JARVIS", ORANGE),
        "listening": ("HÖRT ZU", "ICH HÖRE ZU", LISTEN),
        "thinking": ("DENKT NACH", "ANFRAGE WIRD ANALYSIERT", THINK),
        "speaking": ("ANTWORTET", "JARVIS SPRICHT", BRIGHT_ORANGE),
    }

    def __init__(self):
        super().__init__()
        self.program_window = None

        # IPC-Server starten
        QLocalServer.removeServer(SERVER_NAME)

        self.server = QLocalServer(self)
        self.server.listen(SERVER_NAME)
        self.server.newConnection.connect(self.handle_connection)

        events.show_programs.connect(self.show_programs_window)

        self.setWindowTitle("JARVIS // KOMMANDOZENTRALE")
        self.resize(1280, 760)
        self.setMinimumSize(960, 620)
        self.setAttribute(Qt.WA_OpaquePaintEvent)

        self.frame = 0
        self.scanning = True
        self.voice_state = "idle"
        self.voice_message = ""
        self.random = random.Random(41)
        self.history = [self.random.uniform(0.18, 0.77) for _ in range(56)]
        self.particles = []
        for _ in range(96):
            point = [self.random.uniform(-1, 1) for _ in range(3)]
            length = math.sqrt(sum(value * value for value in point)) or 1
            distance = self.random.uniform(.48, 1.42) / length
            self.particles.append(tuple(value * distance for value in point))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(33)

    def animate(self):
        if not launcher_is_alive():
            self.timer.stop()
            app = QApplication.instance()
            if app is not None:
                app.quit()
            return
        self.frame += 1
        self.voice_state, self.voice_message = get_voice_state()
        if self.voice_state not in self.VOICE_STATES:
            self.voice_state = "idle"
        if self.frame % 4 == 0:
            next_value = self.history[-1] + self.random.uniform(-0.14, 0.14)
            self.history = self.history[1:] + [max(0.10, min(0.88, next_value))]
        self.update()


    def show_programs_window(self):

        if self.program_window is None:
            self.program_window = ProgramsWindow()

        self.program_window.show()
        self.program_window.raise_()
        self.program_window.activateWindow()

    def close_programs_window(self):
        if self.program_window is not None:
            self.program_window.close()
            self.program_window = None

    def closeEvent(self, event):
        stop_path = os.path.join(
            tempfile.gettempdir(),
            "jarvis_vbs_stop.txt"
        )

        with open(stop_path, "w") as f:
            f.write("STOP")

        event.accept()

    def voice_visual(self):
        """Returns the visible label and accent for the current speech state."""
        label, message, color = self.VOICE_STATES[self.voice_state]
        return label, self.voice_message or message, color

    @staticmethod
    def with_alpha(color, alpha):
        tinted = QColor(color)
        tinted.setAlpha(alpha)
        return tinted

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scanning = not self.scanning
            self.update()

    def font(self, size, weight=QFont.Normal):
        value = QFont("Consolas")
        value.setStyleHint(QFont.Monospace)
        value.setPixelSize(size)
        value.setWeight(weight)
        return value

    def text(self, painter, rect, value, size=11, color=None, align=Qt.AlignLeft | Qt.AlignVCenter):
        painter.setFont(self.font(size))
        painter.setPen(color or self.MUTED)
        painter.drawText(rect, align, value)

    def panel(self, painter, rect, title, status="AKTIV"):
        # Glassy, beveled card base: dark in the center, slightly lighter at the top.
        painter.save()
        painter.setPen(Qt.NoPen)
        glass = QLinearGradient(0, rect.y(), 0, rect.bottom())
        glass.setColorAt(0, QColor("#20242f"))
        glass.setColorAt(.18, QColor("#191c25"))
        glass.setColorAt(1, QColor("#11131a"))
        painter.setBrush(glass)
        painter.drawRect(rect)
        painter.restore()
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(255, 255, 255, 24), 1))
        painter.drawRect(rect)
        painter.fillRect(QRectF(rect.x(), rect.y(), 3, rect.height()), self.ORANGE)
        painter.setPen(QPen(QColor(255, 145, 77, 75), 1))
        painter.drawLine(int(rect.x() + 7), int(rect.y() + 1), int(rect.right() - 7), int(rect.y() + 1))
        # Small corner brackets sell the instrument-panel / hologram look.
        painter.setPen(QPen(QColor(255, 145, 77, 150), 1))
        corner = 9
        for x1, y1, x2, y2 in (
            (rect.x() + 5, rect.y() + 5, rect.x() + 5 + corner, rect.y() + 5),
            (rect.x() + 5, rect.y() + 5, rect.x() + 5, rect.y() + 5 + corner),
            (rect.right() - 5, rect.bottom() - 5, rect.right() - 5 - corner, rect.bottom() - 5),
            (rect.right() - 5, rect.bottom() - 5, rect.right() - 5, rect.bottom() - 5 - corner),
        ):
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        self.text(painter, QRectF(rect.x() + 10, rect.y() + 6, rect.width() - 70, 16), title.upper(), 10, self.BRIGHT_ORANGE)
        painter.setPen(QPen(QColor("#31272a"), 1))
        painter.drawLine(int(rect.x() + 8), int(rect.y() + 26), int(rect.right() - 8), int(rect.y() + 26))
        self.text(painter, QRectF(rect.right() - 52, rect.y() + 6, 42, 16), status, 8, self.GREEN, Qt.AlignRight | Qt.AlignVCenter)

    def draw_metric_card(self, painter, rect, name, value, delta, positive=True):
        painter.fillRect(rect, QColor("#14171f"))
        painter.setPen(QPen(self.LINE, 1))
        painter.drawRect(rect)
        self.text(painter, QRectF(rect.x() + 10, rect.y() + 5, rect.width() - 20, 14), name, 8, self.MUTED)
        self.text(painter, QRectF(rect.x() + 10, rect.y() + 20, rect.width() - 20, 24), value, 17, QColor("#f1d8ca"))
        color = self.GREEN if positive else self.ORANGE
        prefix = "▲ " if positive else "▼ "
        self.text(painter, QRectF(rect.x() + 10, rect.bottom() - 18, rect.width() - 20, 12), prefix + delta, 8, color)

    def draw_grid(self, painter):
        painter.fillRect(self.rect(), self.BG)
        painter.setPen(QPen(QColor(255, 106, 33, 14), 1))
        step = 28
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

        # very subtle moving scan lines
        scan_y = (self.frame * 2) % max(1, self.height())
        gradient = QLinearGradient(0, scan_y - 32, 0, scan_y + 32)
        gradient.setColorAt(0, QColor(255, 106, 33, 0))
        gradient.setColorAt(0.5, QColor(255, 106, 33, 25 if self.scanning else 0))
        gradient.setColorAt(1, QColor(255, 106, 33, 0))
        painter.fillRect(QRectF(0, scan_y - 32, self.width(), 64), gradient)

        # Vignette: the center remains readable while the edges recede into the HUD.
        vignette = QRadialGradient(self.width() / 2, self.height() / 2, max(self.width(), self.height()) * .72)
        vignette.setColorAt(0, QColor(0, 0, 0, 0))
        vignette.setColorAt(.72, QColor(0, 0, 0, 10))
        vignette.setColorAt(1, QColor(0, 0, 0, 105))
        painter.setPen(Qt.NoPen)
        painter.setBrush(vignette)
        painter.drawRect(self.rect())

    def project_globe(self, longitude, latitude, center_x, center_y, radius, rotation):
        """Orthografische 3D-Projektion von Längen-/Breitengrad auf den Globus."""
        lon = math.radians(longitude) + rotation
        lat = math.radians(latitude)
        x3 = math.cos(lat) * math.sin(lon)
        y3 = math.sin(lat)
        z3 = math.cos(lat) * math.cos(lon)
        depth = .78 + z3 * .22
        return center_x + x3 * radius, center_y - y3 * radius, z3, depth

    def draw_satellite_marker(self, painter, x, y, depth, color):
        size = max(2.0, 4.8 * depth)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.with_alpha(color, 35))
        painter.drawEllipse(QRectF(x - size * 2.4, y - size * 2.4, size * 4.8, size * 4.8))
        painter.setBrush(color)
        painter.drawEllipse(QRectF(x - size / 2, y - size / 2, size, size))
        painter.setPen(QPen(self.with_alpha(color, 210), 1))
        painter.drawLine(int(x - size * 3), int(y), int(x - size), int(y))
        painter.drawLine(int(x + size), int(y), int(x + size * 3), int(y))
        painter.drawLine(int(x), int(y - size * 2), int(x), int(y + size * 2))

    def draw_globe(self, painter, rect):
        """3D-Weltkugel mit Kontinenten, Partikeln und sichtbaren Satellitenbahnen."""
        center_x, center_y = rect.center().x(), rect.center().y() - 2
        radius = min(rect.width(), rect.height()) * .34
        rotation = self.frame * .008 if self.scanning else 0
        tilt = .48 + math.sin(self.frame * .009) * .025

        glow = QRadialGradient(center_x, center_y, radius * 1.65)
        glow.setColorAt(0, QColor(255, 106, 33, 42))
        glow.setColorAt(.60, QColor(255, 106, 33, 14))
        glow.setColorAt(1, QColor(255, 106, 33, 0))
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(center_x - radius * 1.65, center_y - radius * 1.65, radius * 3.3, radius * 3.3))

        sphere_gradient = QRadialGradient(center_x - radius * .26, center_y - radius * .3, radius * 1.25)
        sphere_gradient.setColorAt(0, QColor("#3e3030"))
        sphere_gradient.setColorAt(.48, QColor("#1d242b"))
        sphere_gradient.setColorAt(1, QColor("#090d13"))
        painter.setBrush(sphere_gradient)
        painter.setPen(QPen(QColor(255, 142, 75, 205), 2))
        painter.drawEllipse(QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2))

        painter.save()
        painter.setClipPath(self.ellipse_path(center_x, center_y, radius))

        # Breiten-/Längengrade give the sphere its physical depth.
        painter.setPen(QPen(QColor(111, 198, 212, 75), 1))
        for latitude in (-60, -30, 0, 30, 60):
            previous = None
            for step in range(73):
                point = self.project_globe(step * 5 - 180, latitude, center_x, center_y, radius, rotation)
                if previous and point[2] > -.12 and previous[2] > -.12:
                    painter.drawLine(int(previous[0]), int(previous[1]), int(point[0]), int(point[1]))
                previous = point
        for longitude in range(-150, 180, 30):
            previous = None
            for step in range(37):
                point = self.project_globe(longitude, step * 5 - 90, center_x, center_y, radius, rotation)
                if previous and point[2] > -.12 and previous[2] > -.12:
                    painter.drawLine(int(previous[0]), int(previous[1]), int(point[0]), int(point[1]))
                previous = point

        # Simplified, recognizable world-map coastlines in the same holographic style.
        landmasses = (
            ((-168, 72), (-145, 71), (-132, 55), (-123, 48), (-112, 30), (-98, 20), (-82, 25), (-76, 43), (-61, 51), (-67, 61), (-92, 72), (-125, 76)),
            ((-81, 12), (-70, 8), (-62, -5), (-67, -23), (-57, -52), (-72, -55), (-81, -28), (-88, -4)),
            ((-17, 36), (5, 37), (30, 31), (43, 12), (34, -12), (25, -35), (8, -35), (-5, -8), (-15, 15)),
            ((-10, 36), (5, 48), (25, 62), (45, 67), (56, 56), (35, 43), (18, 36)),
            ((35, 70), (75, 73), (110, 62), (145, 54), (165, 42), (140, 28), (112, 22), (78, 8), (48, 14), (34, 32)),
            ((112, -10), (143, -12), (153, -24), (145, -39), (120, -35), (110, -20)),
        )
        painter.setPen(QPen(QColor(255, 177, 93, 205), 1.25))
        for landmass in landmasses:
            for first, second in zip(landmass, landmass[1:] + landmass[:1]):
                a = self.project_globe(first[0], first[1], center_x, center_y, radius, rotation)
                b = self.project_globe(second[0], second[1], center_x, center_y, radius, rotation)
                if a[2] > -.08 and b[2] > -.08:
                    painter.drawLine(int(a[0]), int(a[1]), int(b[0]), int(b[1]))

        # Floating data particles on the surface.
        for index in range(44):
            longitude = (index * 47 + self.frame * .65) % 360 - 180
            latitude = -62 + ((index * 31) % 124)
            x, y, z, depth = self.project_globe(longitude, latitude, center_x, center_y, radius, rotation)
            if z > .02:
                particle = self.LISTEN if index % 7 == 0 else self.BRIGHT_ORANGE
                size = max(1.0, depth * (1.8 + (index % 3)))
                painter.setPen(Qt.NoPen)
                painter.setBrush(self.with_alpha(particle, int(65 + depth * 140)))
                painter.drawEllipse(QRectF(x - size / 2, y - size / 2, size, size))
        painter.restore()

        # Three independently tilted orbital planes, each carrying a satellite.
        orbit_specs = ((0, .0, self.BRIGHT_ORANGE), (1, 1.9, self.LISTEN), (2, 3.8, self.ORANGE))
        for axis, phase, color in orbit_specs:
            previous = None
            satellite = None
            for index in range(121):
                angle = math.tau * index / 120 + phase + rotation * (1.5 if axis == 1 else 1)
                if axis == 0:
                    point = (math.cos(angle) * 1.36, math.sin(angle) * .52, 0)
                elif axis == 1:
                    point = (math.cos(angle) * 1.22, 0, math.sin(angle) * .82)
                else:
                    point = (0, math.cos(angle) * 1.17, math.sin(angle) * .90)
                x, y, z, depth = self.project_3d(point, center_x, center_y, radius * .92, rotation, tilt)
                if previous:
                    painter.setPen(QPen(self.with_alpha(color, int(75 + max(0, z) * 120)), 1.2))
                    painter.drawLine(int(previous[0]), int(previous[1]), int(x), int(y))
                if index == (18 + int(self.frame / 2)) % 121:
                    satellite = (x, y, depth)
                previous = (x, y, z, depth)
            if satellite:
                self.draw_satellite_marker(painter, satellite[0], satellite[1], satellite[2], color)

        painter.setPen(QPen(QColor(255, 119, 49, 150), 1))
        for multiplier, start, span in ((1.16, 35, 78), (1.28, 190, 44), (1.42, 270, 36)):
            ring = QRectF(center_x - radius * multiplier, center_y - radius * multiplier, radius * multiplier * 2, radius * multiplier * 2)
            painter.drawArc(ring, start * 16, span * 16)
        self.text(painter, QRectF(rect.x() + 12, rect.bottom() - 39, rect.width() - 24, 15), "WELTNETZ // 94,7 % SYNCHRONISIERT", 8, self.GREEN)
        self.text(painter, QRectF(rect.x() + 12, rect.bottom() - 23, rect.width() - 24, 15), "SATELLITEN: 12 VERBUNDEN // UMLÄUFE AKTIV", 7, self.BRIGHT_ORANGE)

    def ellipse_path(self, x, y, r):
        from PySide6.QtGui import QPainterPath
        path = QPainterPath()
        path.addEllipse(QRectF(x - r, y - r, r * 2, r * 2))
        return path

    def project_3d(self, point, center_x, center_y, scale, yaw, tilt):
        """Project a 3D point into the 2D panel with a gentle perspective lens."""
        x, y, z = point
        cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)
        x, z = x * cos_yaw - z * sin_yaw, x * sin_yaw + z * cos_yaw
        cos_tilt, sin_tilt = math.cos(tilt), math.sin(tilt)
        y, z = y * cos_tilt - z * sin_tilt, y * sin_tilt + z * cos_tilt
        depth = 1 / (2.65 - z)
        return center_x + x * scale * depth, center_y + y * scale * depth, z, depth

    def draw_orbit(self, painter, center_x, center_y, scale, yaw, tilt, axis, phase, front):
        """Draw one projected, inclined energy orbit in front of or behind the core."""
        previous = None
        for index in range(145):
            angle = math.tau * index / 144 + phase
            if axis == 0:
                point = (math.cos(angle) * 1.5, math.sin(angle) * .55, 0)
            elif axis == 1:
                point = (math.cos(angle) * 1.32, 0, math.sin(angle) * .78)
            else:
                point = (0, math.cos(angle) * 1.2, math.sin(angle) * .92)
            x, y, z, depth = self.project_3d(point, center_x, center_y, scale, yaw, tilt)
            if previous:
                px, py, pz, _ = previous
                segment_is_front = (z + pz) / 2 > .10
                if segment_is_front == front:
                    intensity = int(75 + min(150, (z + 1) * 70))
                    painter.setPen(QPen(QColor(255, 112, 39, intensity), 2 if front else 1))
                    painter.drawLine(int(px), int(py), int(x), int(y))
            previous = (x, y, z, depth)

    def draw_core_particles(self, painter, center_x, center_y, scale, yaw, tilt):
        """A depth-sorted particle cloud makes the reactor feel volumetric."""
        rendered = []
        for index, point in enumerate(self.particles):
            wobble = math.sin(self.frame * .028 + index * 1.7) * .055
            x, y, z, depth = self.project_3d(
                (point[0] * (1 + wobble), point[1] * (1 + wobble), point[2]),
                center_x, center_y, scale, yaw * .54, tilt,
            )
            rendered.append((z, x, y, depth))
        for z, x, y, depth in sorted(rendered):
            alpha = int(45 + (z + 1.4) * 66)
            size = max(1.2, min(4.1, depth * 7.2))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 151, 76, alpha))
            painter.drawEllipse(QRectF(x - size / 2, y - size / 2, size, size))

    def draw_core(self, painter, rect):
        """A pseudo-3D arc reactor rendered with perspective and depth layers."""
        painter.save()
        painter.setClipRect(rect)
        state_label, state_message, state_color = self.voice_visual()
        cx, cy = rect.center().x(), rect.center().y() + 5
        base = min(rect.width(), rect.height()) * .31
        motion = self.frame if self.scanning else 0
        pulse = math.sin(motion * (.18 if self.voice_state == "listening" else .11)) * (11 if self.voice_state != "idle" else 5)
        yaw = motion * (.030 if self.voice_state == "listening" else .018)
        tilt = .53 + math.sin(motion * .01) * .09

        # Atmospheric bloom beneath the 3D elements.
        bloom = QRadialGradient(cx, cy, base * 1.9)
        bloom.setColorAt(0, self.with_alpha(state_color, 62 if self.voice_state != "idle" else 42))
        bloom.setColorAt(.35, self.with_alpha(state_color, 22))
        bloom.setColorAt(1, self.with_alpha(state_color, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(bloom)
        painter.drawEllipse(QRectF(cx - base * 1.9, cy - base * 1.9, base * 3.8, base * 3.8))

        # Deep layer: particles and the hidden halves of three orbital rings.
        self.draw_core_particles(painter, cx, cy, base, yaw, tilt)
        for axis, phase in ((0, yaw), (1, -yaw * 1.34), (2, yaw * .78)):
            self.draw_orbit(painter, cx, cy, base, yaw, tilt, axis, phase, False)

        # The central sphere has a directional highlight, dark rim and energy texture.
        sphere = base * (.72 + pulse / 120)
        sphere_gradient = QRadialGradient(cx - sphere * .25, cy - sphere * .30, sphere * 1.30)
        sphere_gradient.setColorAt(0, QColor("#fff7eb"))
        sphere_gradient.setColorAt(.11, QColor("#ffc18f"))
        sphere_gradient.setColorAt(.38, QColor("#ff7830"))
        sphere_gradient.setColorAt(.73, QColor("#9e2d0d"))
        sphere_gradient.setColorAt(1, QColor("#21100d"))
        painter.setPen(QPen(QColor(255, 178, 112, 210), 2))
        painter.setBrush(sphere_gradient)
        painter.drawEllipse(QRectF(cx - sphere, cy - sphere, sphere * 2, sphere * 2))
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(255, 235, 204, 115), 1))
        painter.drawArc(QRectF(cx - sphere * .82, cy - sphere * .82, sphere * 1.64, sphere * 1.64), 42 * 16, 100 * 16)

        # Three tilted shell rings make the reactor read as a 3D object, not a flat icon.
        painter.save()
        painter.translate(cx, cy)
        for ring_scale, squash, rotation, alpha in ((1.34, .34, -20, 105), (1.52, .22, 32, 82), (1.70, .13, 73, 58)):
            painter.save()
            painter.rotate(rotation + math.sin(motion * .012 + ring_scale) * 3)
            shell_w = sphere * ring_scale * 2
            shell_h = sphere * ring_scale * squash * 2
            painter.setPen(QPen(self.with_alpha(state_color, alpha), 1))
            painter.drawEllipse(QRectF(-shell_w / 2, -shell_h / 2, shell_w, shell_h))
            painter.restore()
        painter.restore()

        # Bright, projected orbital segments pass in front of the core.
        for axis, phase in ((0, yaw), (1, -yaw * 1.34), (2, yaw * .78)):
            self.draw_orbit(painter, cx, cy, base, yaw, tilt, axis, phase, True)

        # The colored, rotating state arc is the instant visual feedback for voice activity.
        state_radius = sphere * 1.22
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(self.with_alpha(state_color, 235), 3 if self.voice_state != "idle" else 1))
        painter.drawArc(
            QRectF(cx - state_radius, cy - state_radius, state_radius * 2, state_radius * 2),
            int(-motion * 7) * 16,
            (105 if self.voice_state == "listening" else 72) * 16,
        )

        # Mechanical depth markers orbit in three planes.
        for index in range(12):
            angle = math.tau * index / 12 + yaw * (1.7 if index % 2 else -.8)
            point = (math.cos(angle) * 1.5, math.sin(angle) * .55, 0)
            x, y, z, depth = self.project_3d(point, cx, cy, base, yaw, tilt)
            dot_size = 3.2 if z > 0 else 1.8
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 181, 114, 230 if z > 0 else 85))
            painter.drawEllipse(QRectF(x - dot_size / 2, y - dot_size / 2, dot_size, dot_size))

        self.text(painter, QRectF(cx - sphere * .72, cy - 17, sphere * 1.44, 17), "J A R V I S", 12, QColor("#35160c"), Qt.AlignCenter)
        self.text(painter, QRectF(cx - sphere * .72, cy + 2, sphere * 1.44, 14), state_label, 7, QColor("#5d260e"), Qt.AlignCenter)
        self.text(painter, QRectF(rect.x() + 10, rect.bottom() - 42, rect.width() - 20, 14), state_message, 8, state_color, Qt.AlignCenter)
        state = "3D-SCAN PAUSIEREN" if self.scanning else "3D-SCAN FORTSETZEN"
        self.text(painter, QRectF(rect.x() + 10, rect.bottom() - 24, rect.width() - 20, 14), "KLICK: " + state, 7, self.MUTED, Qt.AlignCenter)
        painter.restore()

    def draw_chart(self, painter, rect):
        inner = QRectF(rect.x() + 13, rect.y() + 38, rect.width() - 26, rect.height() - 54)
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        for y in range(1, 4):
            yy = inner.y() + inner.height() * y / 4
            painter.drawLine(int(inner.x()), int(yy), int(inner.right()), int(yy))
        points = []
        for index, value in enumerate(self.history):
            x = inner.x() + inner.width() * index / (len(self.history) - 1)
            y = inner.bottom() - value * inner.height()
            points.append((x, y))
        painter.setPen(QPen(self.ORANGE, 2))
        for first, second in zip(points, points[1:]):
            painter.drawLine(int(first[0]), int(first[1]), int(second[0]), int(second[1]))
        painter.setPen(QPen(QColor(121, 232, 162, 200), 1))
        for first, second in zip(points[-20:], points[-19:]):
            painter.drawLine(int(first[0]), int(first[1] + 10), int(second[0]), int(second[1] + 10))
        self.text(painter, QRectF(inner.x(), inner.y(), inner.width(), 14), "SIGNAL  84,31 THz", 8, self.BRIGHT_ORANGE)

    def draw_status_stack(self, painter, rect):
        """Compact data strips echo the dense, technical center column of the reference."""
        voice_label, _, voice_color = self.voice_visual()
        labels = (
            ("REAKTORTEMPERATUR", "1.402 K", .76, self.ORANGE),
            ("NEURONALE BANDBREITE", "94,7%", .94, self.GREEN),
            ("SATELLITENNETZ", "12 / 12", .88, self.GREEN),
            ("GEFAHRENANALYSE", "KLAR", .24, self.BRIGHT_ORANGE),
            ("SPRACHSTATUS", voice_label, .68 if self.voice_state == "idle" else .96, voice_color),
        )
        row_h = min(37, (rect.height() - 42) / len(labels))
        y = rect.y() + 36
        for index, (label, value, amount, color) in enumerate(labels):
            row = QRectF(rect.x() + 10, y, rect.width() - 20, row_h - 5)
            painter.fillRect(row, QColor("#13161d"))
            painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
            painter.drawRect(row)
            self.text(painter, QRectF(row.x() + 8, row.y() + 3, row.width() * .60, 12), label, 7, self.MUTED)
            self.text(painter, QRectF(row.right() - 72, row.y() + 3, 64, 12), value, 7, color, Qt.AlignRight | Qt.AlignVCenter)
            meter = QRectF(row.x() + 8, row.bottom() - 8, row.width() - 16, 3)
            painter.fillRect(meter, QColor("#302b2c"))
            painter.fillRect(QRectF(meter.x(), meter.y(), meter.width() * amount, meter.height()), color)
            y += row_h

        # A small animated optical read-out below the stack.
        scan_x = rect.x() + 11 + ((self.frame * 3) % max(1, int(rect.width() - 22)))
        painter.setPen(QPen(QColor(255, 138, 71, 130), 1))
        painter.drawLine(int(scan_x), int(rect.bottom() - 13), int(scan_x), int(rect.bottom() - 5))

    def draw_telemetry_table(self, painter, rect):
        rows = (
            ("01", "HILFSENERGIE", "98,6%", self.GREEN),
            ("02", "HAPTISCHES NETZ", "STABIL", self.GREEN),
            ("03", "EXTERNE SENSOREN", "VERBUNDEN", self.BRIGHT_ORANGE),
            ("04", "SICHERHEITSPROTOKOLL", "AKTIV", self.ORANGE),
        )
        row_h = max(19, (rect.height() - 37) / len(rows))
        y = rect.y() + 34
        for number, label, value, color in rows:
            self.text(painter, QRectF(rect.x() + 12, y, 26, row_h), number, 8, self.ORANGE)
            self.text(painter, QRectF(rect.x() + 42, y, rect.width() * .58, row_h), label, 8, self.MUTED)
            self.text(painter, QRectF(rect.right() - 76, y, 64, row_h), value, 8, color, Qt.AlignRight | Qt.AlignVCenter)
            painter.setPen(QPen(QColor(255, 255, 255, 18), 1))
            painter.drawLine(int(rect.x() + 12), int(y + row_h - 2), int(rect.right() - 12), int(y + row_h - 2))
            y += row_h

    def draw_log(self, painter, rect):
        entries = [
            ("10:42:18", "SYSTEMINTEGRITÄT GEPRÜFT", self.GREEN),
            ("10:42:15", "NEURONALE VERBINDUNG // 4,2 ms", self.BRIGHT_ORANGE),
            ("10:42:10", "SATELLITENRELAIS 03 VERBUNDEN", self.GREEN),
            ("10:42:04", "LOKALE UMGEBUNG WIRD GESCANNT", self.MUTED),
            ("10:41:58", "SICHERHEITSPROTOKOLLE AKTIV", self.GREEN),
        ]
        y = rect.y() + 37
        for timestamp, message, color in entries:
            self.text(painter, QRectF(rect.x() + 12, y, 64, 16), timestamp, 8, self.MUTED)
            self.text(painter, QRectF(rect.x() + 78, y, rect.width() - 90, 16), message, 8, color)
            y += 20

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_grid(painter)

        width, height = self.width(), self.height()
        margin = max(14, width * .015)
        gap = max(9, width * .009)

        # Header
        header = QRectF(margin, margin, width - margin * 2, 43)
        painter.fillRect(header, QColor("#161820"))
        painter.setPen(QPen(self.LINE, 1))
        painter.drawRect(header)
        self.text(painter, QRectF(header.x() + 14, header.y() + 7, 310, 28), "JARVIS / KOMMANDOZENTRALE", 16, QColor("#f0d2bf"))
        self.text(painter, QRectF(header.center().x() - 120, header.y() + 8, 240, 26), "SYS-07  //  SICHERER DATENLINK", 9, self.GREEN, Qt.AlignCenter)
        now = datetime.now().strftime("%H:%M:%S")
        self.text(painter, QRectF(header.right() - 164, header.y() + 8, 150, 26), now + "  CET", 12, self.BRIGHT_ORANGE, Qt.AlignRight | Qt.AlignVCenter)

        available = height - margin - header.height() - gap
        top_height = available * .46
        middle_height = available * .20
        bottom_height = available - top_height - middle_height - gap * 2
        top_y = header.bottom() + gap
        board_width = width - margin * 2 - gap * 2
        left_width = board_width * .35
        center_width = board_width * .31
        right_width = board_width - left_width - center_width
        left = QRectF(margin, top_y, left_width, top_height)
        center = QRectF(left.right() + gap, top_y, center_width, top_height)
        right = QRectF(center.right() + gap, top_y, right_width, top_height)
        voice_label, voice_message, voice_color = self.voice_visual()
        self.panel(painter, left, "3D-Weltkarte", "BAHNEN")
        self.draw_globe(painter, QRectF(left.x(), left.y() + 22, left.width(), left.height() - 22))
        self.panel(painter, center, "Systemvektoren", "ABGLEICH")
        self.draw_status_stack(painter, center)
        self.panel(painter, right, "Arc-Reaktor Status", voice_label[:8])
        self.draw_core(painter, QRectF(right.x(), right.y() + 22, right.width(), right.height() - 22))

        middle_y = top_y + top_height + gap
        waveform_width = (width - margin * 2 - gap) * .61
        waveform = QRectF(margin, middle_y, waveform_width, middle_height)
        telemetry = QRectF(waveform.right() + gap, middle_y, width - margin - waveform.right() - gap, middle_height)
        self.panel(painter, waveform, "Energie-Wellenform", "AKTIV")
        self.draw_chart(painter, waveform)
        self.panel(painter, telemetry, "Subsystem-Telemetrie", "NORMAL")
        self.draw_telemetry_table(painter, telemetry)

        bottom_y = middle_y + middle_height + gap
        metrics_width = (width - margin * 2 - gap) * .47
        log_width = width - margin * 2 - gap - metrics_width
        metrics = QRectF(margin, bottom_y, metrics_width, bottom_height)
        log = QRectF(metrics.right() + gap, bottom_y, log_width, bottom_height)

        metric_gap = 8
        metric_w = (metrics.width() - metric_gap) / 2
        metric_h = (metrics.height() - 35 - metric_gap) / 2
        self.panel(painter, metrics, "Kern-Diagnose", "VERBUNDEN")
        metric_y = metrics.y() + 30
        self.draw_metric_card(painter, QRectF(metrics.x() + 7, metric_y, metric_w - 7, metric_h), "PROZESSORLAST", "37,4%", "2,1%", True)
        self.draw_metric_card(painter, QRectF(metrics.x() + metric_w + metric_gap, metric_y, metric_w - 7, metric_h), "ARBEITSSPEICHER", "12,8 GB", "STABIL", True)
        self.draw_metric_card(painter, QRectF(metrics.x() + 7, metric_y + metric_h + metric_gap, metric_w - 7, metric_h), "ENERGIE", "98,6%", "0,4%", True)
        self.draw_metric_card(painter, QRectF(metrics.x() + metric_w + metric_gap, metric_y + metric_h + metric_gap, metric_w - 7, metric_h), "BEDROHUNGEN", "00", "KLAR", True)
        self.panel(painter, log, "Aktivitätsprotokoll", "VERSCHL")
        self.draw_log(painter, log)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = JarvisUI()
    window.show()
    sys.exit(app.exec())
