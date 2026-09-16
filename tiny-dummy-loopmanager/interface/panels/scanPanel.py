# libraries
import sys
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel,
    QApplication, QTableWidget, 
    QTableWidgetItem
)
from PyQt6.QtCore import pyqtSignal
from laplace_log import log


class ScanPanel(QGroupBox):
    load_scan_config_signal = pyqtSignal()

    def __init__(self):        
        super().__init__("Scan config")

        self.set_up()  # build the elements
        self.actions() # defines the panel actions

    def set_up(self) -> None:

        self.scan_table = QTableWidget()
        self.scan_table.setColumnCount(5)
        self.scan_table.setHorizontalHeaderLabels(
            ["Rank", "Control", "Range", "Step", "Points"]
        )

        self.total_points_label = QLabel("0 points")

        self.load_button = QPushButton("Load")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scan_table)
        main_layout.addWidget(self.total_points_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

    def actions(self):
        # click load button to emit signal caught by ScanWindow
        self.load_button.clicked.connect(self.load_scan_config_signal)

    def load_scan_config(self, settings: dict) -> None:
        """Load scan settings into the scan table."""

        self.scan_table.setRowCount(0)

        total_points = 1

        # Sort by scan rank
        sorted_settings = sorted(
            settings.items(),
            key=lambda item: item[1]["rank"]
        )

        for name, scan in sorted_settings:
            current = scan["current"]
            start = scan["min"]
            stop = scan["max"]
            spacing = scan["step"]
            rank = scan["rank"]

            # Number of positions, including both endpoints.
            if spacing != 0:
                points = int(round((stop - start) / spacing)) + 1
            else:
                points = 1

            total_points *= points

            row = self.scan_table.rowCount()
            self.scan_table.insertRow(row)

            # Rank
            self.scan_table.setItem(
                row, 0,
                QTableWidgetItem(str(rank))
            )

            # Control name
            self.scan_table.setItem(
                row, 1,
                QTableWidgetItem(name)
            )

            # Range
            range_text = f"{start:g} → {stop:g}"
            self.scan_table.setItem(
                row, 2,
                QTableWidgetItem(range_text)
            )

            # Spacing
            spacing_text = f"{spacing:g}"
            self.scan_table.setItem(
                row, 3,
                QTableWidgetItem(spacing_text)
            )

            # Number of points
            self.scan_table.setItem(
                row, 4,
                QTableWidgetItem(str(points))
            )

        self.total_points_label.setText(
            f"{total_points:,} scan points"
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ScanPanel()
    scan_settings = {
        1: {
            "name": "X position",
            "start": -2,
            "stop": 2,
            "spacing": 0.2,
            "unit": "mm",
        },
        2: {
            "name": "Y position",
            "start": 10,
            "stop": 50,
            "spacing": 5,
            "unit": "mm",
        },
    }
    window.load_scan_settings(scan_settings)
    window.resize(600, 300)
    window.show()

    sys.exit(app.exec())