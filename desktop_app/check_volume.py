

def check_volume(config, input_from_interface):
    configuration_volume = 0
    input_volume = 0
    for values in config.occupied_space.values():
        configuration_volume += len(values)
    # Numarul de piese e pe pozitia 1 in tupla, de schimbat daca se trimite numarul pe pozitia 2 si culoarea pe pozitia 1
    for i in input_from_interface:
        input_volume += len(config.db_brick_info.get(i[0])[3]) * i[1]
    if configuration_volume > input_volume:
        return False
    return True

