
def format_plottable_data_dict(data: dict) -> dict:
    plottable_data_dict = {}

    for address_dictionary in data.values():
        name = address_dictionary['name']

        for key, value in address_dictionary['data'].items():
            if type(value) is float:
                plottable_data_dict[key] = value

    return plottable_data_dict


if __name__ == "__main__":
    dictionary =  {'tcp://147.250.140.85:5556': 
                   {'name': 'dummy_camera', 'data': 
                    {'shot_number': 8, 'motor': [0.0, 0.0], 'electron_charge': 1.0028798580169678, 'electron_energy_mean': 0.9999077916145325, 'time': '16:39:20'}}}
    print(f'Plottables: {format_plottable_data_dict(dictionary)}')
