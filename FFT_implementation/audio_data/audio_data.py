import pyaudio
import numpy as np
from scipy.signal import find_peaks


class AudioData:
    def __init__(self, settings):
        self.gui_settings: dict = settings['GUI']
        self.audio_settings: dict = settings['Audio']
        self.FORMAT: int = pyaudio.paInt16
        self.MAX_INPUT_SIGNAL_VALUE: int = 32768  # for 16 bits = 32768
        self.CHANNELS: int = int(self.audio_settings['Input_CHANNELS'])
        self.RATE: int = int(self.audio_settings['Input_RATE'])
        self.CHUNK: int = int(self.audio_settings['Input_CHUNK'])

        self.frame_duration = self.CHUNK / self.RATE
        self.fr = np.array(range(0, self.CHUNK)) / self.frame_duration
        self.threshold_main: int = int(self.audio_settings['Threshold_MAIN'])

        self.audio = pyaudio.PyAudio()
        p = pyaudio.PyAudio()
        info_input_device = p.get_default_input_device_info()
        print(info_input_device)
        self.stream = self.audio.open(format=self.FORMAT,
                                      output_device_index=None,
                                      channels=int(self.CHANNELS),
                                      rate=int(self.RATE),
                                      input=True)
    def quit(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def load_data_from_buffer(self):
        return np.frombuffer(self.stream.read(self.CHUNK), np.int16)

    def load_raw_data(self, data_from_buffer):
        return [np.arange(len(data_from_buffer)) / self.RATE, data_from_buffer / self.MAX_INPUT_SIGNAL_VALUE]

    def load_fft_data(self, data_from_buffer):
        fft = np.fft.fft(data_from_buffer)
        fft_abs = np.abs(fft)
        return [self.fr, fft_abs]

    def load_fft_data2(self, data_from_buffer):
        window = np.hamming(len(data_from_buffer))
        data_windowed = data_from_buffer * window
        fft_data = np.abs(np.fft.fft(data_windowed))
        fft_data_db = 20 * np.log10(fft_data)
        freq_axis = np.fft.fftfreq(len(fft_data_db), 1.0 / self.RATE)
        return [freq_axis, fft_data_db]

    def load_plot_data(self):
        data_from_buffer = self.load_data_from_buffer()
        plot_data: list = [self.load_raw_data(data_from_buffer),
                           self.load_fft_data(data_from_buffer),
                           self.load_fft_data2(data_from_buffer)]
        return plot_data

    def peaks_finder(self, fft_abs):
        peaks = find_peaks(fft_abs, height=self.threshold_main)
        peak_ps = self.fr[peaks[0]]
        height = peaks[1]['peak_heights']
        return [peak_ps, height]
