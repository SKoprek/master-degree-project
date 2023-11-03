import tkinter as tk
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from utils import tempered_scale as tem_scale
from functools import partial


class GUI:
    def __init__(self, settings):

        self.gui_settings: dict = settings['GUI']
        self.audio_settings: dict = settings['Audio']

        # TEMP
        self.threshold_max_valueFFT: float = 0
        self.threshold_average_valueWINDOW: float = 0

        self.selected_freq = []
        self.freq_lines = []
        self.line_colors = ["blue", "brown", "orange", "cyan", "magenta", "purple"]
        self.threshold_freq = (2 ** (1 / 24))
        self.peaks_points: list = []
        self.peaks_points_plot: list = []
        self.threshold_main: int = int(self.audio_settings['Threshold_MAIN'])

        self.threshold_area: list = []
        self.freq_lines: list = []

        self.root = tk.Tk()

        self.root.title(self.gui_settings['GUI_TITLE'])
        self.root.geometry(self.gui_settings['GUI_GEOMETRY'])
        self.root.rowconfigure(0, weight=1)

        self.frame_duration = int(self.audio_settings['Input_CHUNK']) / int(self.audio_settings['Input_RATE'])
        self.fr = np.array(range(0, int(self.audio_settings['Input_CHUNK']))) / self.frame_duration

        # Dodawanie elementów interfejsu użytkownika
        self.fig, self.ax = plt.subplots(nrows=3, ncols=1)
        bar1 = FigureCanvasTkAgg(self.fig, self.root)
        bar1.get_tk_widget().grid(row=8, columnspan=14, rowspan=15)
        x = np.arange(10000)
        y = np.random.randn(10000)
        # RAW plot
        self.li, = self.ax[0].plot(x, y)
        self.ax[0].set_xlim(0, self.frame_duration)
        self.ax[0].set_ylim(-1, 1)
        self.ax[0].set_title("Wykres amplitudy")
        self.ax[0].set_xlabel("Czas [s]")
        self.ax[0].set_ylabel("Amplituda")
        # FFT PLOT
        self.li2, = self.ax[1].plot(x, y)
        self.ax[1].set_xlim(20, 1400)
        self.ax[1].set_ylim(1, 5000000)
        self.ax[1].set_title("FFT")  # FFT
        self.ax[1].set_xlabel("Frequency (Hz)")
        self.ax[1].set_ylabel("Amplituda")
        # FFT PLOT WINDOW
        self.li3, = self.ax[2].plot(x, y)
        self.ax[2].set_xlim(-1400, 1400)
        self.ax[2].set_ylim(-250, 250)
        self.ax[2].set_title("Wykres FFT w skali dB z oknem Hamming")
        self.ax[2].set_xlabel("Częstotliwość (Hz)")
        self.ax[2].set_ylabel("Amplituda (dB)")

    def run(self, ploter):
        ani = animation.FuncAnimation(self.fig, ploter, interval=100)
        self.set_gui()
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()

    def set_gui(self):
        self.set_buttons_menu()
        self.selected_buttons(self.line_colors, self.selected_freq)
        self.freq_detect(self.peaks_points, self.selected_freq)
        # --INPUT INFO--
        titleThreshold = tk.Label(self.root, text="--INPUT INFO--", borderwidth=2, relief="solid")
        titleThreshold.grid(row=9, column=24, columnspan=4, sticky='nsew')
        # FORMAT (sampling size and format )
        titleThreshold = tk.Label(self.root, text="Format: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=10, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=" Int 16 ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=10, column=26, columnspan=2, sticky='nsew')
        # CHANNELS (number of channels)
        titleThreshold = tk.Label(self.root, text="Channels: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=11, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=(str(int(self.audio_settings['Input_CHANNELS'])) + " "),
                                  borderwidth=2,
                                  relief="solid")
        titleThreshold.grid(row=11, column=26, columnspan=2, sticky='nsew')
        # RATE (Sampling rate)
        titleThreshold = tk.Label(self.root, text="Sampling rate: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=12, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=(self.audio_settings['Input_RATE'] + " Hz"), borderwidth=2,
                                  relief="solid")
        titleThreshold.grid(row=12, column=26, columnspan=2, sticky='nsew')
        # CHUNK (Specifies the number of frames per buffer)
        titleThreshold = tk.Label(self.root, text="Frames per buffer: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=13, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=(self.audio_settings['Input_CHUNK'] + " "), borderwidth=2,
                                  relief="solid")
        titleThreshold.grid(row=13, column=26, columnspan=2, sticky='nsew')
        # Sample duration
        titleThreshold = tk.Label(self.root, text="Frame duration: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=14, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=(str(round(self.frame_duration, 2)) + " in seconds "), borderwidth=2,
                                  relief="solid")
        titleThreshold.grid(row=14, column=26, columnspan=2, sticky='nsew')
        # -- Threshold INFO --
        titleThreshold = tk.Label(self.root, text="-- Threshold INFO --", borderwidth=2, relief="solid")
        titleThreshold.grid(row=18, column=24, columnspan=4, sticky='nsew')
        titleThreshold = tk.Label(self.root, text="Threshold: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=19, column=24, columnspan=2, sticky='nsew')
        titleThreshold = tk.Label(self.root, text=self.threshold_main, borderwidth=2, relief="solid")
        titleThreshold.grid(row=19, column=26, columnspan=2, sticky='nsew')

        titleSelected = tk.Label(self.root, text="Selected freq", borderwidth=2, relief="solid")
        titleSelected.grid(row=8, column=14, columnspan=5, sticky='nsew')

        titleThreshold = tk.Label(self.root, text="Threshold Max FFT: ", borderwidth=2, relief="solid")
        titleThreshold.grid(row=9, column=20, columnspan=2, sticky='nsew')

        titleThreshold = tk.Label(self.root, text="Threshold windowed:", borderwidth=2, relief="solid")
        titleThreshold.grid(row=10, column=20, columnspan=2, sticky='nsew')

    def set_buttons_menu(self):
        string_list = tem_scale.string_names
        myLabelFreq = tk.Label(self.root, text="Guitar frequency")
        myLabelFreq.grid(row=0, column=0, columnspan=3, sticky='nsew')
        for index_0 in range(0, 26):
            if index_0 == 0:
                label = tk.Label(self.root, text="   ", bg="black")
                label.grid(row=1, column=1)
            else:
                label = tk.Label(self.root, text=(index_0 - 1), font=('Helvetica', 18, 'bold'))
                label.grid(row=1, column=index_0 + 1)
        for index, name in enumerate(string_list):
            string_data = tem_scale.return_string()[index]
            label = tk.Label(self.root, text=name, font=('Helvetica', 18, 'bold'))
            label.grid(row=index + 2, column=1)
            for fretboard, fretboard_index, frequencies in string_data:
                freqValue = round(frequencies, 2)
                row = index + 2
                column = fretboard_index + 2
                b_value = [fretboard, fretboard_index, freqValue, row, column]
                myButton = tk.Button(self.root, text=(round(frequencies, 2)),
                                     command=partial(self.click_button, b_value), bg="white")
                myButton.grid(row=b_value[3], column=b_value[4], sticky='nsew')

    def selected_buttons(self, line_colors, selected_freq):
        for index_0, color in enumerate(line_colors):
            rowLab1 = tk.Label(self.root, text="-", bg=line_colors[index_0], borderwidth=2, relief="solid")
            rowLab1.grid(row=9 + index_0, column=14, columnspan=2, sticky='nsew')
            rowLab1 = tk.Label(self.root, text="-", bg=line_colors[index_0])
            rowLab1.grid(row=9 + index_0, column=14 + 2, columnspan=3, sticky='nsew')
        for index_0, selected in enumerate(selected_freq):
            rowLab0 = tk.Label(self.root, text=(str(selected[0]) + str(selected[1])), bg=line_colors[index_0],
                               borderwidth=2,
                               relief="solid")
            rowLab0.grid(row=9 + index_0, column=14, columnspan=2, sticky='nsew')
            rowLab1 = tk.Label(self.root, text=str(selected[2]), bg=line_colors[index_0])
            rowLab1.grid(row=9 + index_0, column=14 + 2, columnspan=3, sticky='nsew')

    def click_button(self, button_v):
        if not self.selected_freq:
            self.selected_freq.append(button_v)
            myButton = tk.Button(self.root, text=(button_v[2]), command=partial(self.click_button, button_v),
                                 bg="green")
            myButton.grid(row=button_v[3], column=button_v[4], sticky='nsew')
        else:
            for index_0, selected in enumerate(self.selected_freq):
                if (selected == button_v) or (selected[3] == button_v[3]):
                    myButton = tk.Button(self.root, text=(button_v[2]), command=partial(self.click_button, button_v),
                                         bg="white")
                    myButton.grid(row=button_v[3], column=button_v[4], sticky='nsew')
                    self.selected_freq.pop(index_0)
                    self.selected_buttons(self.line_colors, self.selected_freq)
                    if selected != button_v:
                        self.selected_freq.append(button_v)
                        myButton = tk.Button(self.root, text=(selected[2]),
                                             command=partial(self.click_button, selected), bg="white")
                        myButton.grid(row=selected[3], column=selected[4], sticky='nsew')
                        myButton = tk.Button(self.root, text=(button_v[2]),
                                             command=partial(self.click_button, button_v), bg="green")
                        myButton.grid(row=button_v[3], column=button_v[4], sticky='nsew')
                        self.selected_buttons(self.line_colors, self.selected_freq)
                    return
            self.selected_freq.append(button_v)
            myButton = tk.Button(self.root, text=(button_v[2]), command=partial(self.click_button, button_v),
                                 bg="green")
            myButton.grid(row=button_v[3], column=button_v[4], sticky='nsew')
        self.selected_buttons(self.line_colors, self.selected_freq)

    def freq_detect(self, peaks, select_freq):
        color_x = ["gray", "gray", "gray", "gray", "gray", "gray"]
        if len(peaks) > 0:
            if (len(peaks[0]) > 0) and len(peaks[1]) > 0 and (len(select_freq) > 0):
                for index_freq, freq in enumerate(select_freq):
                    for index_peak, peak in enumerate(peaks[0]):
                        if (freq[2] * self.threshold_freq > (peaks[0][index_peak])) and (
                                freq[2] / self.threshold_freq < (peaks[0][index_peak])) and (
                                peaks[1][index_peak] > self.threshold_freq):
                            color_x[index_freq] = "green"
        for index, color in enumerate(color_x):
            ttt = tk.Label(self.root, borderwidth=2, bg=color, relief="solid")
            ttt.grid(row=(9 + index), column=19, sticky='nsew')

    def set_li(self, data_to_plot):
        self.li.set_xdata(data_to_plot[0])
        self.li.set_ydata(data_to_plot[1])

    def set_li2(self, data_to_plot):
        self.li2.set_xdata(data_to_plot[0])
        self.li2.set_ydata(data_to_plot[1])

    def set_li3(self, data_to_plot):
        self.li3.set_xdata(data_to_plot[0])
        self.li3.set_ydata(data_to_plot[1])

    def set_li_plots(self, data_to_plot):
        self.set_li(data_to_plot[0])
        self.set_li2(data_to_plot[1])
        self.set_li3(data_to_plot[2])

    def set_max_valueFFT(self, threshold_max_valueFFT):
        titleThreshold = tk.Label(self.root, text=threshold_max_valueFFT, borderwidth=2, relief="solid")
        titleThreshold.grid(row=9, column=22, columnspan=2, sticky='nsew')

    def set_max_valueWindow(self, threshold_average_valueWINDOW):
        titleThreshold = tk.Label(self.root, text=threshold_average_valueWINDOW, borderwidth=2, relief="solid")
        titleThreshold.grid(row=10, column=22, columnspan=2, sticky='nsew')

    def points_threshold(self):
        while len(self.threshold_area) > 0:
            self.threshold_area[0].remove()
            self.threshold_area.pop(0)
        while len(self.freq_lines) > 0:
            self.freq_lines[0].remove()
            self.freq_lines.pop(0)
        if len(self.selected_freq) != 0:
            for index, selected in enumerate(self.selected_freq):
                # FFT
                self.threshold_area.append(
                    self.ax[1].fill_between(
                        x=[(selected[2] / self.threshold_freq), (selected[2] * self.threshold_freq)],
                        y1=self.threshold_main, y2=5000000,
                        color="yellow"))
                self.freq_lines.append(
                    self.ax[1].axvline(x=selected[2], color=self.line_colors[index], linestyle='dashed'))
                self.freq_lines.append(
                    self.ax[1].axvline(x=selected[2] * 2, color=self.line_colors[index], linestyle='dashed'))
                self.freq_lines.append(
                    self.ax[1].axvline(x=selected[2] * 3, color=self.line_colors[index], linestyle='dashed'))
                self.freq_lines.append(
                    self.ax[1].axvline(x=selected[2] * 4, color=self.line_colors[index], linestyle='dashed'))
                # Windowed
                # self.threshold_area.append(
                #     self.ax[2].fill_between(x=[(selected[2] - 5), (selected[2] + 5)], y1=self.threshold_main,
                #                             y2=(10 ** 10),
                #                             color="yellow"))
                # self.freq_lines.append(
                #     self.ax[2].axvline(x=selected[2], color=self.line_colors[index], linestyle='dashed'))
                # self.freq_lines.append(
                #     self.ax[2].axvline(x=selected[2] * 2, color=self.line_colors[index], linestyle='dashed'))
                # self.freq_lines.append(
                #     self.ax[2].axvline(x=selected[2] * 3, color=self.line_colors[index], linestyle='dashed'))
                # self.freq_lines.append(
                #     self.ax[2].axvline(x=selected[2] * 4, color=self.line_colors[index], linestyle='dashed'))

        self.freq_detect(self.peaks_points, self.selected_freq)

    def peaks_marks(self, peaks_data):
        self.peaks_points.clear()
        self.peaks_points.append(peaks_data[0])
        self.peaks_points.append(peaks_data[1])
        while len(self.peaks_points_plot) > 0:
            self.peaks_points_plot[0][0].remove()
            self.peaks_points_plot.pop(0)
        if len(peaks_data[0]) != 0:
            self.peaks_points_plot.append(self.ax[1].plot(peaks_data[0], peaks_data[1], "x", color="red"))
