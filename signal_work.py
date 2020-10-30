import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.simpledialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import pickle
import pathlib
from ds1054z import DS1054Z
class Profile:
    def __init__(self, show_ch=[1,0,0,0], ch1=[0,1,0], ch2=[0,1,0], ch3=[0,1,0], ch4=[0,1,0], y_offset=0, time_div=0, res=1, current_ch=0, ip='192.168.1.1', dev=0, listdata=[]):
        self.show_ch = show_ch          #[1,1,1,1] channel 1-4
        self.ch1 = ch1                  #[voltdiv, probeoff, x_off]
        self.ch2 = ch2
        self.ch3 = ch3
        self.ch4 = ch4
        self.y_offset = y_offset
        self.time_div = time_div
        self.res = res
        self.current_ch = current_ch            #current ch setting
        self.ip = ip                            #ip
        self.dev = dev

class Application:
    def __init__(self, root):
        self.root =root
        self.root.title = 'DS1054Z GUI'

        self.profile1 = Profile()
        self.profile2 = Profile()
        self.profile3 = Profile()
        self.profile4 = Profile()
        self.temp_profile = Profile()
        self.profile_list = [self.profile1, self.profile2, self.profile3, self.profile4, self.temp_profile]
        self.current_profile = self.temp_profile
        self.probe_range = [1,2,5,10]
        self.ch_range = ['ch1', 'ch2', 'ch3', 'ch4']
        self.volt_div_range = [10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01,0.005,0.002,0.001]
        self.time_div_range = [50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 500E-6, 200E-6,
                          100E-6, 50E-6, 20E-6, 10E-6, 5E-6, 2E-6, 1E-6, 500E-9, 200E-9, 100E-9, 50E-9, 20E-9, 10E-9,
                          5E-9]
        self.volt_div_text = ['10V', '5V', '2V', '1V', '500mV', '200mV', '100mV', '50mV', '20mV', '10mV', '5mV', '2mV', '1mV']
        self.time_div_text = ['50s', '20s', '10s', '5s', '2s', '1s', '500ms', '200ms', '100ms', '50ms', '20ms', '10ms',
                         '5ms', '2ms', '1ms', '500μs', '200μs', '100μs', '50μs', '20μs', '10μs', '5μs', '2μs', '1μs',
                         '500ns', '200ns', '100ns', '50ns', '20ns', '10ns', '5ns']
        self.user_interface()

    """
    File Menubar section
    - new_user is resetting all profile to default by calling reset_profile method (also show warning msgbox)
    - reset_profile is reset method
    - load_file ,save as is just like their name
    - save is avaliable after you loaded or save as a psk file first
    - _active save is method for enable save command in menubar
    """
    def new_user(self):
        MsgBox = tkinter.messagebox.askquestion('Reset Profile', 'Are you sure you want reset all current settings',
                                           icon='warning')
        if MsgBox:
            self.reset_profile(5)
        else:pass
    def reset_profile(self, index=5):
        if index == 5:
            for profile in self.profile_list:
                profile = Profile()
        else:
            index -=1
            self.profile_list[index] = Profile()
    def load_file(self):
        self.file_path = tkinter.filedialog.askopenfilename(initialdir=pathlib.Path(__file__).parent.absolute(), title='Open File',
                                                       filetypes = (("Pickle File", "*.pkl"),("all files","*.*")))
        file = open(self.file_path, 'rb')
        self.profile1 = pickle.load(file)
        self.profile2 = pickle.load(file)
        self.profile3 = pickle.load(file)
        self.profile4 = pickle.load(file)
        self.temp_profile = pickle.load(file)
        file.close()
        self._active_save()
    def save_as(self):
        self.file_path = tkinter.filedialog.asksaveasfilename(initialdir=pathlib.Path(__file__).parent.absolute(), title='Save File',
                                                         filetypes = (("Pickle File", "*.pkl"),("all files","*.*"))) + '.pkl'
        file = open(self.file_path, 'wb')
        pickle.dump(self.profile1, file)
        pickle.dump(self.profile2, file)
        pickle.dump(self.profile3, file)
        pickle.dump(self.profile4, file)
        pickle.dump(self.temp_profile, file)
        file.close()
        self._active_save()
    def save(self):
        file = open(self.file_path, 'wb')
        pickle.dump(self.profile1, file)
        pickle.dump(self.profile2, file)
        pickle.dump(self.profile3, file)
        pickle.dump(self.profile4, file)
        pickle.dump(self.temp_profile, file)
        file.close()
    def _active_save(self):
    # Cant find a convenient way to active/disable menubar item so just delete and add these
        self.filemenu.delete(3)
        self.filemenu.delete(3)
        self.filemenu.delete(3)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)

    """
    Profile Menubar Section
    *calling these method by using 1-4 (as channel 1-4) but list index is 0-3 so every method have to minus index by 1
    """
    def select_profile(self, index):
        index -= 1
        self.temp_profile = self.profile_list[index]

        self._update_ui()
    def save_profile(self, index):
        index -= 1                      #profile 1-4 but index is 0-3
        self.profile_list[index] = self.temp_profile
    def reset_profile(self):
        profile_index -= 1  # profile 1-4 but index is 0-3
        self.profile_list[profile_index] = Profile()
        self._update_ui()

    #Info Menubar
    def show_info(self):
        tkinter.messagebox.showinfo("Thank for using", "This Application is Mini project of subject\n"
                                                       "010123106 Signal and System class KMUTNB\n"
                                                       "\nMade by \n-Mr.Isara Kunudomchhaiwat 6001012610097 \n"
                                                       "-Mr.Phichet Eaktrakul 6001012630071 \n"
                                                       "-Mr.Saksit Wilainuch6001012630144\n"
                                                       "\ngithub.com/isarafx/Signal-Final-Project")

    """
    update ipbox, channel_show, channel, volt-div, time-div, probe-offset, x-offset, y-offset,sampling resolution
    """
    def _update_ui(self):
        self.temp_profile = self.pr
    #ui section seperate to make this code look cleaner
    def user_interface(self):

        #menubar section
        menubar = tkinter.Menu(root)

        # create a pulldown menu, and add it to the menu bar
        self.filemenu = tkinter.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_user)
        self.filemenu.add_command(label="Open", command=self.load_file)
        self.filemenu.add_command(label="Save as", command=self.save_as)
        self.filemenu.add_command(label="Save", command=self.save, state='disabled')
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=self.filemenu)

        # create more pulldown menus
        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_radiobutton(label="Profile1")
        editmenu.add_radiobutton(label="Profile2")
        editmenu.add_radiobutton(label="Profile3")
        editmenu.add_radiobutton(label="Profile4")
        editmenu.add_separator()
        editmenu.add_command(label="Save", state='disabled')
        editmenu.add_command(label="Reset", state='disabled')
        menubar.add_cascade(label="Profile", menu=editmenu)

        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_info)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        root.config(menu=menubar)

        """
        using only pack layout all of item are declared first then pack
        to make sure everything is configurable
        to understand how frame layed out check in github
        """
        self.ip_frame = tkinter.LabelFrame(self.root, text='enter your ip')
        self.ip_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        useless_var=tkinter.StringVar()
        self.ip_box = tkinter.Entry(self.ip_frame, textvariable=useless_var)
        self.ip_box.pack(side=tkinter.LEFT)
        useless_var.set('169.254.1.5')
        self.ip_button = tkinter.Button(self.ip_frame, text='enter')
        self.ip_button.pack(side=tkinter.LEFT)
        self.status = tkinter.Label(self.ip_frame, text='please enter ip address first')
        self.status.pack(side=tkinter.LEFT)

        self.second_frame = tkinter.Frame(self.root)
        self.second_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        self.left_frame = tkinter.Frame(self.second_frame)
        self.left_frame.pack(side=tkinter.LEFT)
        self.right_frame = tkinter.Frame(self.second_frame)
        self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)
        self.chdiv_frame = tkinter.LabelFrame(self.right_frame, text='Volt-div,  Time-div')
        self.chdiv_frame.pack(side=tkinter.TOP)
        self.voltdiv = tkinter.ttk.Combobox(self.chdiv_frame, state="readonly", values=self.volt_div_text)
        self.voltdiv.pack(side=tkinter.LEFT)
        self.voltdiv.current(1)
        # self.voltdiv.bind("<<ComboboxSelected>>", self._setvoltdiv)
        self.probe_offset = tkinter.ttk.Combobox(self.chdiv_frame, state="readonly", values=self.probe_range)
        self.probe_offset.pack(side=tkinter.LEFT)
        self.probe_offset.current(1)
        # self.voltdiv.bind("<<ComboboxSelected>>", self._setvoltdiv)
        self.chdiv2_frame = tkinter.Frame(self.right_frame)
        self.chdiv2_frame.pack(side=tkinter.TOP)
        self.select_ch = tkinter.ttk.Combobox(self.chdiv2_frame, state="readonly", values=self.ch_range)
        self.select_ch.pack(side=tkinter.LEFT)
        self.select_ch.current(1)
        self.timediv = tkinter.ttk.Combobox(self.chdiv2_frame, state="readonly", values=self.time_div_text)
        self.timediv.pack(side=tkinter.TOP)
        self.timediv.current(1)
        # self.timediv.bind("<<ComboboxSelected>>", self._settimediv)
        self.x_offframe = tkinter.LabelFrame(self.right_frame, text="X-Offset")
        self.x_offframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.x_offset = tkinter.Scale(self.x_offframe, orient=tkinter.HORIZONTAL, from_=-100, to=100)
        self.x_offset.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        # self.x_offset.bind("<ButtonRelease-1>", self._offset_x_change)
        self.y_offframe = tkinter.LabelFrame(self.right_frame, text="Y-Offset")
        self.y_offframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.y_offset = tkinter.Scale(self.y_offframe, orient=tkinter.HORIZONTAL, from_=-100, to=100)
        self.y_offset.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        # self.y_offset.bind("<ButtonRelease-1>", self._offset_y_change)
        self.sampling_res_frame = tkinter.LabelFrame(self.right_frame, text="Sampling_Resolution")
        self.sampling_res_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.sampling_offset = tkinter.Scale(self.sampling_res_frame, orient=tkinter.HORIZONTAL, from_=1, to=15)
        self.sampling_offset.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        # self.sampling_offset.bind("<ButtonRelease-1>", self._sampling_change)

        self.run_button_frame = tkinter.Frame(self.right_frame)
        self.run_button_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.run_button = tkinter.Button(self.run_button_frame, text='RUN')
        self.run_button.pack(side=tkinter.LEFT, expand=1, fill=tkinter.X)
        self.stop_button = tkinter.Button(self.run_button_frame, text='STOP')
        self.stop_button.pack(side=tkinter.LEFT, expand=1, fill=tkinter.X)
        self.auto_button = tkinter.Button(self.run_button_frame, text='AUTO')
        self.auto_button.pack(side=tkinter.LEFT, expand=1, fill=tkinter.X)
        self.report = tkinter.Label(self.root, text='some nonsense detail for nerd')
        self.report.pack(side=tkinter.TOP)

        #
        t = np.arange(0, 12, .01)
        signal = [-0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.06, -0.06, 0.136, 0.132, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.064, 0.056, -0.136, -0.128, -0.148, -0.14, -0.148, -0.14, -0.148, -0.148, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.148, -0.064, -0.06, 0.136, 0.132, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.064, 0.06, -0.136, -0.132, -0.148, -0.14, -0.148, -0.148, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.148, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14400000000000002, -0.14, -0.14400000000000002, -0.14, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.14, -0.148, -0.148, -0.14, -0.14, -0.148, -0.14, -0.148, -0.148, -0.064, -0.06, 0.14, 0.136, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.14400000000000002, 0.152, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002, 0.152, 0.14400000000000002]
        self.fig = Figure(figsize=(8, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(t, signal, 'r-')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.channel_frame = tkinter.Frame(self.left_frame)
        self.channel_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.chv1 = tkinter.IntVar()
        self.chv2 = tkinter.IntVar()
        self.chv3 = tkinter.IntVar()
        self.chv4 = tkinter.IntVar()
        self.ch1 = tkinter.Checkbutton(self.channel_frame, text='ch1', variable=self.chv1)
        self.ch2 = tkinter.Checkbutton(self.channel_frame, text='ch2', variable=self.chv2)
        self.ch3 = tkinter.Checkbutton(self.channel_frame, text='ch3', variable=self.chv3)
        self.ch4 = tkinter.Checkbutton(self.channel_frame, text='ch4', variable=self.chv4)
        self.ch1.pack(side=tkinter.LEFT, expand=1)
        self.ch2.pack(side=tkinter.LEFT, expand=1)
        self.ch3.pack(side=tkinter.LEFT, expand=1)
        self.ch4.pack(side=tkinter.LEFT, expand=1)

        self.ui_item = [self.voltdiv, self.timediv, self.x_offset, self.y_offset, self.sampling_offset,
                         self.ch1, self.ch2, self.ch3, self.ch4,
                        self.run_button, self.stop_button, self.auto_button]




root = tkinter.Tk()
gui = Application(root)
root.mainloop()