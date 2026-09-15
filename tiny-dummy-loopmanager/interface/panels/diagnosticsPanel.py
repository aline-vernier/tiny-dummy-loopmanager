# libraries
import sys
from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QVBoxLayout, QRadioButton,
    QCheckBox, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QLabel, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from laplace_log import log

# project
from ...utils.config_helper import get_from_config, set_in_config
from ..widgets.diagnostic_control_widget import DiagnosticControlWidget


class DiagnosticsPanel(QGroupBox):

    def __init__(self):        
        super().__init__("Actuators (motors, gas, etc.)")

        self.diagnostic_widgets = dict({})
        self.set_up()  # build the elements
        self.actions() # defines the panel actions

    def set_up(self) -> None:
        '''
        Build the panel widgets.
        '''
        panel_layout = QVBoxLayout(self)   # create the layout
        self.list_widget = QListWidget()   # create the widget list
        panel_layout.addWidget(self.list_widget)  # add the widget list to the layout


    def add_diagnostic_widgets_from_status(self, address:str, status: dict):
        log.info(f'Adding diag widget from status {status}')

    def add_diagnostic_widget(self, address: str, name: str, plottables: dict):
        new_widget = DiagnosticControlWidget(address=address, name=name, plottables= plottables)

        
        self.diagnostic_widgets.setdefault(address, {})[name] = new_widget
        item = QListWidgetItem(self.list_widget)          # create a new list item
        item.setSizeHint(new_widget.sizeHint())           # set the size of the item
        self.list_widget.addItem(item)                    # add the new item in the list
        self.list_widget.setItemWidget(item, new_widget)  # assign the new widget to the item


    def update_diagnostic_widget(self, address: str, status: dict) -> None:
        log.info(f'Status at address {address} is {status}')

    def update_diagnostic_unavailable(self, address):
        diagnostic_widgets = self.diagnostic_widgets.get(address)
        log.debug(f'Diagnostic widgets: {diagnostic_widgets}')
        for widget in diagnostic_widgets.values():
            widget.update_status_available(False)

    def actions(self):
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = DiagnosticsPanel()
    
    diagnostics = {'tcp://147.250.140.85:5555': ['name1', 'name2', 'name3'], 
            'tcp://147.250.140.86:5555': ['name4', 'name5', 'name6'],
            'tcp://147.250.140.87:5555': ['name', 'name_', 'name+']}

    for address, name_list in diagnostics.items():
        for name in name_list :
            window.add_diagnostic_widget(address, name)
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())