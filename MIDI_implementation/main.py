import sys

import pygame.midi

DEVICE_NAME: str = 'LPK25'
DETAILS: bool = True


def print_devices():
    """
    Wyświetla listę dostępnych urządzeń.
    """
    print("|Dostępne urządzenia|")
    for n in range(pygame.midi.get_count()):
        print(n, pygame.midi.get_device_info(n))


def get_device_by_id(f_device_name):
    """
    Funkcja ustala id poszukiwanego urządzenia przy pomocy jego nazwy.
    :param f_device_name: nazwa urządzenia,
    :return: id urządzenia.
    """
    f_device_id: int = -1
    for n in range(pygame.midi.get_count()):
        if f_device_name in str(pygame.midi.get_device_info(n)[1]) and 1 == pygame.midi.get_device_info(n)[2]:
            f_device_id = n
            print(f"Odnaleziono urządzenie wejścia {f_device_name} pod indeksem {n}.")
            break
    return f_device_id


def readInput(input_device, details):
    """
    Funkcja wyświetla dane, które zostają wysłane przez urządzenie MIDI przy pomocy jego id.
    Zwraca tablicę elementów oraz opcjonalne informacje dodatkowe.
    :param input_device: id urządzenia,
    :param details: czy zwrócić informacje dodatkowe.
    """
    while True:
        if input_device.poll():
            event = input_device.read(1)
            print(event)
            if details:
                MIDI_message = event[0][0]
                MIDI_message_status = MIDI_message[0]
                MIDI_message_data1 = MIDI_message[1]
                MIDI_message_data2 = MIDI_message[2]
                MIDI_message_data3 = MIDI_message[3]
                timestamp = event[0][1]
                print(f"Otrzymano wiadomość {event[0]}.")
                print(
                    f"Czas: {timestamp} oraz wiadomość MIDI: Status: {MIDI_message_status}, Data1: {MIDI_message_data1}, Data2: {MIDI_message_data2}, Data3:{MIDI_message_data3}")
                print(
                    f"Prezentacja wiadomości w formie binarnej, bloki zostały podzielone znakiem | :{midi_to_bin(MIDI_message_status)}|{midi_to_bin(MIDI_message_data1)}|{midi_to_bin(MIDI_message_data2)}|{midi_to_bin(MIDI_message_data3)}")


def midi_to_bin(input_number):
    """
    Funkcja przetwarza liczbę wejściową i uzupełnia puste bity w 8-bitowym bloku, aby zaprezentować pełny blok danych.
    :param input_number: liczba wejściowa,
    :return: 8-bitowy blok w formie tekstowej.
    """
    input_message = bin(input_number)[2:]
    temp_message = ''
    for index in range(8 - len(input_message)):
        temp_message += str("0")
    return f"{temp_message}{input_message}"


if __name__ == '__main__':
    print("MIDI:")
    pygame.midi.init()  # inicjuje moduł MIDI
    print_devices()  # wyświetlenie wszystkich dostępnych urządzeń MIDI
    device_id = get_device_by_id(DEVICE_NAME)  # ustala id poszukiwanego urządzenia.
    if device_id == -1:  # jeżeli urządzenie nie zostanie znalezione kończy działanie programu
        print(f"Urządzenie {DEVICE_NAME} nie zostało odnalezione!")
        sys.exit()
    else:
        print(f"Urządzenie {DEVICE_NAME} gotowe do komunikacji.")
        my_input = pygame.midi.Input(device_id)  # ustala połączenie z urządzeniem MIDI
        readInput(my_input, DETAILS)  # interpretuje informacje wejściowe MIDI
