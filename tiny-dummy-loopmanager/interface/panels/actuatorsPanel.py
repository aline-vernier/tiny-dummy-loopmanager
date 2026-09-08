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
from ..widgets.actuator_control_widget import ActuatorControlWidget


class ActuatorsPanel(QGroupBox):

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

    def update_actuator_widget(self, address: str, status: dict) -> None:
        for motor in status['motors']:
                    name = motor['name']
                    position = motor['position']
                    try : 
                        actuator_widgets = self.actuator_widgets[address]
                    except Exception as e :
                        log.error(f'self.actuator_widgets[address] could not be accessed {e}')
                        return
                    try : 
                        widget = actuator_widgets[name]
                    except Exception as e: 
                        log.error(f'actuator_widgets[name] could not be accessed {e}')
                        return
                    try : 
                        widget.update_position(position)
                    except Exception as e:
                        log.error(f'Could not update position: {e}')
                    

    def add_actuator_widgets_from_status(self, address: str, status: dict) -> None:
        for motor in status['motors']:
            name = motor['name']
            position = motor['position']
            self.add_actuator_widget(address, name, position)
            

    def add_actuator_widget(self, address: str, name: str, position: float):
        new_widget = ActuatorControlWidget(address=address, name=name)

        self.actuator_widgets.setdefault(address, {})[name] = new_widget
        item = QListWidgetItem(self.list_widget)          # create a new list item
        item.setSizeHint(new_widget.sizeHint())           # set the size of the item
        self.list_widget.addItem(item)                    # add the new item in the list
        self.list_widget.setItemWidget(item, new_widget)  # assign the new widget to the item
        try: 
            self.actuator_widgets[address][name].update_position(position)
        except Exception as e:
            log.error(f'Could not update position {e}')

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