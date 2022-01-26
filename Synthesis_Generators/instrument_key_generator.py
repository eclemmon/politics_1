
def generate_instrument_dict(instrument_names):
    instrument_dict = {}
    for count, name in enumerate(instrument_names):
        key = 'sound{}'.format(count + 1)
        instrument_dict[key] = name
    return instrument_dict
