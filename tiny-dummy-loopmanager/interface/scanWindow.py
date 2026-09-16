# libraries
import pathlib

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtGui import QIcon
import qdarkstyle
from laplace_log import log

# project
from .panels import (
    ExecutionPanel, ActuatorsPanel, DiagnosticsPanel
)
from ..core.scanManager import ScanManager

from ..utils.diagnostic_utils import format_plottable_data_dict


class ScanWindow(QMainWindow):
    
    def __init__(self):

        super().__init__() # heritage from QMainWindow

        self.scan_manager = ScanManager()  # class managing the scan
        self.set_up()  # build the window panels and buttons
        self.actions() # defines the actions of the window
        self.actuators = dict({})
        self.diagnostics = dict({})



    def set_up(self) -> None:
        '''
        Build the panels and buttons of the main loop window.
        '''        
        p = pathlib.Path(__file__) # path to the current file
        
        # set title, geometry and style
        self.setWindowTitle("Scan Window")
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        self.setGeometry(100, 30, 900, 300)

        # icon
        icon_path = p.parent / 'icons' # path to the icon folder
        self.setWindowIcon( QIcon( str(icon_path / 'LOA.png') ) )

        # central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Block 1: Server and Reader modes
        self.execution_panel = ExecutionPanel()
        main_layout.addWidget(self.execution_panel)

        # Block 2: Actuators panel (empty at startup)
        self.actuators_panel = ActuatorsPanel()
        main_layout.addWidget(self.actuators_panel)

        # Block 3: Diagnostics panel (empty at startup)
        self.diagnostics_panel = DiagnosticsPanel()
        main_layout.addWidget(self.diagnostics_panel)


        # Block 5: Start and Stop buttons
        bottom_layout = QHBoxLayout()

        bottom_layout.addStretch()
        self.step_label = QLabel("Step: -/-")
        self.step_label.setStyleSheet("font-weight: bold;")
        bottom_layout.addWidget(self.step_label)
        # state label
        self.status_label = QLabel("🟢 Ready")
        self.status_label.setStyleSheet("font-weight: bold;")
        bottom_layout.addWidget(self.status_label)
        # Stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedWidth(120)
        bottom_layout.addWidget(self.stop_button)
            # Start
        self.start_button = QPushButton("Start")
        self.start_button.setFixedWidth(120)
        bottom_layout.addWidget(self.start_button)

        main_layout.addLayout(bottom_layout)

    
    def actions(self) -> None:
        '''
        Defines the actions between the several panels and
        make the bridget with the loop manager.
        '''
        # Start and Stop buttons
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.execution_panel.server_state_changed.connect(
            self.scan_manager.server_launch
        )

        # transmit the server address from the server to the ExecutionPanel
        self.scan_manager.on_server_address.connect(
            self.execution_panel.set_server_address
        )

        # Signal coming from scan manager, passed on from ServerController, 
        # emitted in callback function called by ServerLHC instance 
        self.scan_manager.on_actuators_dict_received.connect(
            self.update_actuators
        )

        self.scan_manager.on_diagnostics_dict_received.connect(
            self.update_diagnostics
        )



    def update_actuators(self, actuators_dict: dict) -> None:

        # 1. Find motor servers that used to exist but are no longer available
        removed_addresses = set(self.actuators) - set(actuators_dict)

        for address in removed_addresses:

            self.actuators_panel.update_actuators_unavailable(address)


        # 2. Add new servers and update existing ones
        try  :
            for address, status in actuators_dict.items():

                if address in self.actuators:
                    self.actuators_panel.update_actuator_widget(address, status)

                else:
                    self.actuators[address] = status
                    log.info(f'Motor status at {address} in scan window: {status}')
                    self.actuators_panel.add_actuator_widgets_from_status(
                        address, status
                    )
        except Exception as e :
            log.error(f'Could not update actuator GUI, error {e} occurred')

    def update_diagnostics(self, diagnostics_dict: dict) -> None:

        removed_addresses = set(self.diagnostics) - set(diagnostics_dict)

        for address in removed_addresses:

            self.diagnostics_panel.update_diagnostic_unavailable(address)


        # 2. Add new servers and update existing ones
        try  :
            for address, status in diagnostics_dict.items():

                if address in self.diagnostics:
                    self.diagnostics_panel.update_diagnostic_widget(address, status)

                else:
                    self.diagnostics[address] = status
                    self.diagnostics_panel.add_diagnostic_widgets_from_status(
                        address, status
                    )
        except Exception as e :
            log.error(f'Could not update diag GUI, error {e} occurred')

        # removed_addresses = set(self.diagnostics) - set(diagnostics_dict)

        # for address in removed_addresses:
        #     log.debug(f'Diagnostic at {address} is no longer available')
        #     self.diagnostics_panel.update_diagnostic_unavailable(address)

        # if diagnostics_dict: 
        #     address, name, plottables = format_plottable_data_dict(diagnostics_dict)
        #     # plottables is a dictionary of format {'plottable_1':float, ..., 'plottable_n':float}
        #     if plottables:
        #         log.debug(f'Plottables {plottables}')
           
        #     # 2. Add new servers and update existing ones
        #     try  :

        #         if address in self.diagnostics:
        #             self.diagnostics_panel.update_diagnostic_widget(address, True)

        #         else:
        #             self.diagnostics[address] = {'name': name, 'plottables': plottables}
        #             log.info(f'Actuator plottables at {address} in scan window: {plottables}')
        #             self.diagnostics_panel.add_diagnostic_widget(address, name, plottables)
        #     except Exception as e :
        #         log.error(f'Could not update actuator GUI, error {e} occurred')
        # else:
        #     pass



    def on_start(self) -> None:
        '''
        Function used when 'start_button' is pressed. Create a 
        config dictionary gathering the panel informations and 
        transmit it to the loop manager.

        Check if the panel informations are sufficient to continue,
        raise error and warning message box if needed.
        '''
        log.debug("Start button pressed.")

        # gather the panel informations
        execution = self.execution_panel.get_execution()



        log.info("Starting scan")
        self.set_loop_state(True)



    def on_stop(self) -> None:
        '''
        Function used when 'stop_button' is pressed.
        '''
        log.debug("Stop button pressed.")

        self.set_loop_state(False)
    

    def on_max_iteration_reached(self) -> None:
        '''
        Maximum iteration set a initialization is reached.
        '''
        log.debug("The maximum number of iterations has been reached. Stopping the process...")

        self.scan_manager.stop_scan()
        self.set_opt_state(False)

        QMessageBox.warning(
            self,
            "End criterium",
            "Maximum iteration reached."
        )
    



    
    def set_loop_state(self, scanning: bool):
        if scanning:
            self.status_label.setText("🟡 Scannng...")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.start_button.setEnabled(False)      # lock the start button
            self.execution_panel.set_locked(True)    # lock the ExecutionPanel
            
        else:
            self.status_label.setText("🟢 Ready")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.start_button.setEnabled(True)      # unlock the start button
            self.execution_panel.set_locked(False)  # unlock the ExecutionPanel



    def closeEvent(self, event) -> None:
        '''
        Function called when the window is closing.
        
        Close the server stored in 'OptManager'.
        '''
        if self.execution_panel.is_online_enabled():
            self.scan_manager.server_launch(server_state=False)
        
        event.accept()