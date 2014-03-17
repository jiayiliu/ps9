__author__ = 'jiayiliu'

import Tkinter as Tk
import tkFileDialog
from psView import *
from psModel import *
from sparameter import *


class Ds9Controller():
    """
    Python-DS9 Controller

    :param master: the master window, Tk.Tk() or others
    """
    def __init__(self, master=None):
        if master is None:
            master = Tk.Tk()
            master.withdraw()
            master_flag = True
        else:
            master_flag = False
        self.viewer = Ds9Viewer(master)
        self.model = Ds9Model()
        self.reg_files_to_load = list()
        self.cluster_id = 0
        # detail setup
        self.viewer.button_load_region.config(command=self.load_region)
        self.viewer.button_load_region_again.config(
            command=lambda: self.model.load_region_files(self.reg_files_to_load))
        self.viewer.button_get_cat.config(command=self.get_cat)
        self.select_ok = [False, False]
        # DS9 communication
        self.viewer.button_xpa.config(command=self.create_xpa)
        # output
        self.viewer.button_save_list.config(command=self.save_list)
        self.viewer.button_save_reg.config(command=self.save_reg)
        self.viewer.button_save_img.config(command=self.save_img)
        if master_flag:
            self.viewer.protocol("WM_DELETE_WINDOW", master.destroy)
            master.mainloop()

    def clean_region(self):
        """
        Clean all regions in DS9
        """
        self.model.clean_region()

    def create_xpa(self):
        """
        create model xpa connection when DS9 image is ready
        """
        self.model.create_xpa()
        self.viewer.focus_set()
        self.select_ok[1] = True
        if self.select_ok[0]:
            self.viewer.button_select_pos.config(state=Tk.NORMAL, command=self.get_all_pos)
            self.viewer.bind_all("<KeyPress-s>", lambda e: self.get_all_pos())
            self.viewer.button_select_one.config(state=Tk.NORMAL, command=self.get_pos)
            self.viewer.button_remove_one.config(state=Tk.NORMAL, command=self.popout)
        self.viewer.button_load_region.config(state=Tk.NORMAL)
        self.viewer.button_clean_region.config(state=Tk.NORMAL, command=self.model.clean_region)
        self.viewer.button_save_img.config(state=Tk.NORMAL)

    def get_pos(self):
        """
        get one position and print out
        """
        self.model.xpa.set("crosshair {0:s}".format(self.model.xpa.get("crosshair")))
        self.model.get_pos()
        self.select_pos()
        self.viewer.update_list(self.model.display_selection())

    def get_all_pos(self):
        """
        get all positions
        """
        self.model.get_all_pos()
        self.model.select_all_pos()
        self.viewer.update_list(self.model.display_selection())

    def get_cat(self):
        """
        load cluster catalog according to the cluster_id
        """
        self.cluster_id = int(self.viewer.entry_cluster_id.get())
        filename = DEFAULT_CAT_INPUT_PATTERN.format(self.cluster_id)
        self.model.get_cat(filename)
        self.select_ok[0] = True
        if self.select_ok[1]:
            self.viewer.button_select_pos.config(state=Tk.NORMAL)
            self.viewer.bind_all("<KeyPress-s>", lambda e: self.model.select_pos())
        self.viewer.button_save_list.config(state=Tk.NORMAL)
        self.viewer.button_save_reg.config(state=Tk.NORMAL)

    def load_region(self):
        """
        Load regions files into DS9 image
        """
        self.reg_files_to_load = \
            tkFileDialog.askopenfilenames(filetypes=[("all file", ".*"), ("region file", ".reg")],
                                          initialdir=DEFAULT_REGION_INPUT)
        if len(self.reg_files_to_load) > 0:
            self.model.load_region_files(self.reg_files_to_load)
            self.viewer.button_load_region_again.config(state=Tk.NORMAL)
        else:
            self.viewer.button_load_region_again.config(state=Tk.DISABLED)

    def popout(self):
        """
        pop out one selection in text field
        """
        self.model.popout()
        self.viewer.update_list(self.model.display_selection())


    def save_list(self):
        """
        save selected catalog into new place
        """
        self.model.save_list(DEFAULT_CAT_OUTPUT_PATTERN.format(self.cluster_id))

    def save_reg(self):
        """
        save region file
        """
        self.model.save_region(DEFAULT_REGION_OUTPUT_PATTERN.format(self.cluster_id))

    def save_img(self):
        """
        save image file
        """
        self.model.save_image(DEFAULT_IMG_OUTPUT_PATTERN.format(self.cluster_id))

    def select_pos(self):
        """
        Match the current position to closest catalog position
        """
        self.model.select_pos()


if __name__ == "__main__":
    rfile = FITS_PATTERN.format(216, 'i')
    gfile = FITS_PATTERN.format(216, 'r')
    bfile = FITS_PATTERN.format(216, 'g')
    #display_rgb([rfile, gfile, bfile])

    Ds9Controller()

