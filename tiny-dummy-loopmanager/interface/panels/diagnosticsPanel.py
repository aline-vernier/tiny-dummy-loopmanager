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


class DiagnosticPanel(QGroupBox):

    def __init__(self):        
        super().__init__("Actuators (motors, gas, etc.)")

        self.actuator_widgets = dict({})
        self.set_up()  # build the elements
        self.actions() # defines the panel actions

    def set_up(self) -> None:
        '''
        Build the panel widgets.
        '''
        panel_layout = QVBoxLayout(self)   # create the layout
        self.list_widget = QListWidget()   # create the widget list
        panel_layout.addWidget(self.list_widget)  # add the widget list to the layout

    def add_actuator_dict_widget(self, actuators_dict: dict):
        '''
        actuators_dict must have format :
        {'address':[name list], ...}
        '''
        for address, name_list in actuators_dict.items():
            for name in name_list :
                self.add_actuator_widget(address, name)


    def add_actuator_widget(self, address: str, name: str):
        new_widget = DiagnosticControlWidget(address=address, name=name)

        self.actuator_widgets[address]={name : new_widget}
        item = QListWidgetItem(self.list_widget)          # create a new list item
        item.setSizeHint(new_widget.sizeHint())           # set the size of the item
        self.list_widget.addItem(item)                    # add the new item in the list
        self.list_widget.setItemWidget(item, new_widget)  # assign the new widget to the item

    def actions(self):
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ActuatorsPanel()
    
    actuators = {'tcp://147.250.140.85:5555': ['name1', 'name2', 'name3'], 
            'tcp://147.250.140.86:5555': ['name4', 'name5', 'name6'],
            'tcp://147.250.140.87:5555': ['name', 'name_', 'name+']}

    for address, name_list in actuators.items():
        for name in name_list :
            window.add_actuator_widget(address, name)
    window.resize(350, 150)
    window.show()

    sys.exit(app.exec())