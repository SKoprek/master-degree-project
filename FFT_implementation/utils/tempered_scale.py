import numpy as np

string_names = ["E-", "A-", "D-", "G-", "B-", "e-"]
freq_array_base = []
guitar_fretboard_frequencies_array = []

BASE_FREQ_A = 440.000
tempered_scale = (2 ** (1 / 12))

temp_freq_E6 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(5, 30)))
freq_array_base.append(np.ndarray.tolist(temp_freq_E6))
temp_freq_A5 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(0, 25)))
freq_array_base.append(np.ndarray.tolist(temp_freq_A5))
temp_freq_D4 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(-5, 20)))
freq_array_base.append(np.ndarray.tolist(temp_freq_D4))
temp_freq_G3 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(-10, 15)))
freq_array_base.append(np.ndarray.tolist(temp_freq_G3))
temp_freq_B2 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(-14, 11)))
freq_array_base.append(np.ndarray.tolist(temp_freq_B2))
temp_freq_e1 = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(-19, 6)))
freq_array_base.append(np.ndarray.tolist(temp_freq_e1))


def all_freq():
    all_temp_freq = np.flip(BASE_FREQ_A / (tempered_scale ** np.arange(-19, 30)))
    return all_temp_freq


def set_table(temp_freq, string_name):
    table = []
    for index0, temp_freq in enumerate(temp_freq):
        new_table = [string_name, index0, temp_freq]
        table.append(new_table)
        pass
    return table


def return_string():
    for index, string in enumerate(string_names):
        in_table = set_table(freq_array_base[index], string_names[index])
        guitar_fretboard_frequencies_array.append(in_table)
        pass
    return guitar_fretboard_frequencies_array
