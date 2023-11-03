from utils import configuration as config
from gui.gui import GUI
from audio_data.audio_data import AudioData
import sys


gui = GUI(config.settings)
audio = AudioData(config.settings)


def load_data_from_buffer(i):
    data_to_plot = audio.load_plot_data()
    gui.set_li_plots(data_to_plot)

    peaks = audio.peaks_finder(data_to_plot[1][1])
    gui.peaks_marks(peaks)

    if gui.threshold_max_valueFFT <= max(data_to_plot[1][1]):
        gui.threshold_max_valueFFT = max(data_to_plot[1][1])
        gui.set_max_valueFFT(gui.threshold_max_valueFFT)
    if gui.threshold_average_valueWINDOW <= max(data_to_plot[2][1]):
        gui.threshold_average_valueWINDOW = max(data_to_plot[2][1])
        gui.set_max_valueWindow(gui.threshold_average_valueWINDOW)
    gui.points_threshold()


if __name__ == '__main__':

    try:
        gui.run(load_data_from_buffer)
        gui.set_gui()
    except KeyboardInterrupt:
        audio.quit()
        gui.destroy()
        sys.exit()
