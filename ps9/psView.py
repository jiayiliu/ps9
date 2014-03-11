__author__ = 'jiayiliu'


import Tkinter as Tk


def display_rgb(rgb_files,
                min=0, max=3000,
                zoom=0.4, width=800, height=800):
    """
    Display FITS data in RGB format

    :param rgb_files: rgb file name list [r,g,b]
    :param min: min in zscale
    :param max: max in zscale
    :param zoom: zoom of image
    :param width: width of image
    :param height: height of image
    """
    from os import system
    command = "ds9 -zoom {0:f} -width {1:d} -height {2:d} -rgb ".format(zoom, width, height)
    for i, j in zip(rgb_files, ['red', 'green', 'blue']):
        command += "-{0:s} {1:s} -log -z1 {2:f} -z2 {3:f} ".format(j, i, min, max)
    command += "-colorbar no &"
    print  command
    #system(command)


class Ds9Viewer(Tk.Toplevel):
    def __init__(self, master):
        Tk.Toplevel.__init__(self, master)
        self.title("DS9 communicator")
        # Cluster information
        frame_cluster = Tk.Frame(self)
        frame_cluster.grid(row=0, column=0)
        Tk.Label(frame_cluster, text="Cluster ID:").grid(row=0, column=0)
        self.entry_cluster_id = Tk.Entry(frame_cluster)
        self.entry_cluster_id.grid(row=0, column=1)
        self.button_get_cat = Tk.Button(frame_cluster, text="Load Catalog")
        self.button_get_cat.grid(row=0,column=2)
        # DS9 Communication
        frame_ds9 = Tk.Frame(self)
        frame_ds9.grid(row=1, column=0)
        self.button_xpa = Tk.Button(frame_ds9, text="Set up")
        self.button_xpa.grid(row=0, column=0)
        self.button_load_region = Tk.Button(frame_ds9, text="Load Region", state=Tk.DISABLED)
        self.button_load_region.grid(row=0, column=1)
        self.button_clean_region = Tk.Button(frame_ds9, text="Clean Region", state=Tk.DISABLED)
        self.button_clean_region.grid(row=0, column=2)
        self.button_load_region_again = Tk.Button(frame_ds9, text="Load again", state=Tk.DISABLED)
        self.button_load_region_again.grid(row=0, column=3)
        self.button_get_pos = Tk.Button(frame_ds9, text="Get Position (g)", state=Tk.DISABLED)
        self.button_get_pos.grid(row=1, column=0)
        self.button_select_pos = Tk.Button(frame_ds9, text="Select Position (s)", state=Tk.DISABLED)
        self.button_select_pos.grid(row=1, column=1)
        self.button_pop_pos = Tk.Button(frame_ds9, text="Remove", state=Tk.DISABLED)
        self.button_pop_pos.grid(row=1, column=2)
        # Record Keeping
        frame_record = Tk.Frame(self)
        frame_record.grid()
        self.button_save_reg = Tk.Button(frame_record, text="Save Region", state=Tk.DISABLED)
        self.button_save_reg.grid(row=0, column=0)
        self.button_save_list = Tk.Button(frame_record, text="Save List", state=Tk.DISABLED)
        self.button_save_list.grid(row=0, column=1)
        self.button_save_img = Tk.Button(frame_record, text="Save Image", state=Tk.DISABLED)
        self.button_save_img.grid(row=0, column=2)
        frame_selection = Tk.Frame(self, bd=2, relief=Tk.SUNKEN)
        frame_selection.grid()
        self.text_region = Tk.Text(frame_selection, wrap=Tk.NONE, bd=0, state=Tk.DISABLED)
        self.text_region.grid(row=0, column=0, sticky=Tk.N+Tk.S+Tk.E+Tk.W)
        y_scrollbar = Tk.Scrollbar(frame_selection, command=self.text_region.yview)
        y_scrollbar.grid(row=1, column=1, sticky=Tk.N+Tk.S)
        self.text_region.config(yscrollcommand=y_scrollbar.set)

