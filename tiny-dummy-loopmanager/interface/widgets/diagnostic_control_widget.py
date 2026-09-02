# libraries
import pathlib

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QCheckBox, QLabel, QDoubleSpinBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ...utils.check_IP_address import validate_address
from laplace_log import log


class DiagnosticControlWidget(QWidget):
    '''
    Define the diagnostic control line. 
    '''

    def __init__(self, address: str, name: str):
        '''
            Args:
                definition: address 
        '''
        super().__init__() # Inheritance from QWidget
        self.address = None
        self.name = None 

        try : 
            self.define(address, name)
        except Exception as e:
            log.error(f'Could not define diagnostic, invalid definition')
            log.error(f'Exception: {e}')

        self.set_up()  # builds the input widget
        self.actions() # defines the actions of InputWidget

    def define(self, address: str, name: str):
        if not validate_address(address):
            raise ValueError(f'{address} is not a valid address')
        else: 
            self.address = address
            self.name = name


    def set_up(self) -> None:

        # input line layout
        line_layout = QHBoxLayout(self)
        line_layout.setContentsMargins(4, 2, 4, 2) # widget margin
        line_layout.setSpacing(8)                  # spacing
        self.setLayout(line_layout)                # set layout

        p = pathlib.Path(__file__)              # get the file path
        icon_path = p.parent.parent / 'icons'   # get the icon folder path

        # build the check and uncheck icons
        self.connected_icon = QIcon(str(icon_path / 'connected.png'))
        self.disconnected_icon = QIcon(str(icon_path / 'disconnected.png'))

        # state icon
        self.state_icon = QLabel()                                     
        self.state_icon.setFixedWidth(20)
        self.state_icon.setPixmap(self.disconnected_icon.pixmap(16, 16)) 
        self.state_icon.setToolTip("Current state")
        line_layout.addWidget(self.state_icon)

        # scan
        self.scan_checkbox = QCheckBox()
        self.scan_checkbox.setToolTip(f"Check this box to scan")
        self.scan_checkbox.setFixedWidth(20)
        line_layout.addWidget(self.scan_checkbox)

        # scanning rank
        self.rank_input =  QDoubleSpinBox()
        self.rank_input.setMinimum(0)
        self.rank_input.setMaximum(10)
        self.rank_input.setFixedWidth(70)
        self.rank_input.setToolTip(f"Rank 0 outer, rank 1 inner - defined as in a for loop")
        line_layout.addWidget(self.rank_input)

        # ip_port
        self.address_label = QLabel()
        self.address_label.setText(self.address or "Unknown")
        self.address_label.setEnabled(False)
        self.address_label.setToolTip("Actuator IP:port")
        line_layout.addWidget(self.address_label)

        # name
        self.name_label = QLabel()
        self.name_label.setText(self.name or "Unknown")
        self.name_label.setEnabled(False)
        self.name_label.setToolTip("Actuator name")
        line_layout.addWidget(self.name_label)

        # position 

        self.current_pos_spin = QDoubleSpinBox()
        self.current_pos_spin.setDecimals(6)
        self.current_pos_spin.setEnabled(False)
        self.current_pos_spin.setFixedWidth(70)
        self.current_pos_spin.setToolTip("Lower bound")
        line_layout.addWidget(self.current_pos_spin)

        # Min spinBox
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setDecimals(6)
        self.min_spin.setEnabled(False)
        self.min_spin.setFixedWidth(70)
        self.min_spin.setToolTip("Lower bound")
        line_layout.addWidget(self.min_spin)

        # Max spinBox
        self.max_spin = QDoubleSpinBox()
        self.max_spin.setDecimals(6)
        self.max_spin.setEnabled(False)
        self.max_spin.setFixedWidth(70)
        self.max_spin.setToolTip("Higher bound")
        line_layout.addWidget(self.max_spin)

        # Stepsize spinBox
        self.stepsize_spin = QDoubleSpinBox()
        self.stepsize_spin.setDecimals(6)
        self.stepsize_spin.setEnabled(False)
        self.stepsize_spin.setFixedWidth(70)
        self.stepsize_spin.setToolTip("Step size")
        line_layout.addWidget(self.stepsize_spin)

        # Unit
        self.unit_label = QLabel()
        self.unit_label.setText("Unknown")
        self.unit_label.setFixedWidth(60)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unit_label.setToolTip("Input unit")
        line_layout.addWidget(self.unit_label)


    def actions(self) -> None:
        '''
        Defines the actions of the InputWidget class.
        '''
        # when the input state is changed, change the icon and enable / disable the spin boxes
        self.scan_checkbox.stateChanged.connect(self.on_state_changed)
        
        # when the spin boxes are updated, change the input instance boundaries
        self.min_spin.valueChanged.connect(self.update_instance_bounds)
        self.max_spin.valueChanged.connect(self.update_instance_bounds)

        # when the spin boxes are updated, change the spin boxes range
        self.min_spin.valueChanged.connect(self.update_min_max)
        self.max_spin.valueChanged.connect(self.update_min_max)


    def on_state_changed(self, enabled: bool) -> None:
        '''
        '''
        pass


    def update_instance_bounds(self) -> None:
        '''
        Update the boundaries in the class instance.
        '''
        pass

    def update_min_max(self) -> None:
        '''
        Update the min and max values of the spin boxes.
        '''
        pass



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ActuatorControlWidget('147.250.140.85:7531', 'name')
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())