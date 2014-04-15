__author__ = 'jiayiliu'

import numpy as np
from sparameter import *


class XpaModel(ds9.ds9):
    """
    DS9 communication module
    """
    def __init__(self):
        ds9.ds9.__init__(self, start=False, wait=0)

    def get_pos(self):
        """
        get the crosshair position in wcs [RA/Dec]

        :return: [R.A., Dec.]
        """
        return [float(i) for i in self.get("crosshair wcs").split(" ")]

    def load_region(self, filename):
        """
        load region file

        :param filename: filename
        """
        self.set("regions file {0:s}".format(filename))


class Ds9Model():
    """
    DS9 connection model
    """
    def __init__(self):
        self.xpa = None
        self.selection = list()
        self.show_selection = list()
        self.match_id = None
        self.pos = [0, 0]
        self.cat = None

        self.all_pos = list()
        self.all_match_id = list()

    def clean_region(self):
        """
        clean region in DS9 image, and empty selection list

        ! the selection is still available !
        """
        self.xpa.set("regions deleteall")

    def create_xpa(self):
        """
        create xpa access point to DS9
        """
        if self.xpa is not None:
            del self.xpa
        self.xpa = XpaModel()

    def display_selection(self):
        """
        return selection list

        :return: ra,dec str to display
        """
        #content = ["{0:f} {1:f}".format(i[1],i[2]) for i in self.selection]
        content = ["{0:f} {1:f}".format(i[1],i[2]) for i in self.show_selection]
        return "Total Selection: %d\nR.A. Dec.\n"%len(self.selection)+"\n".join(content)

    def get_cat(self, filename):
        """
        get the catalog
        also refresh selection and show_selection

        :param filename: catalog to load
        """
        self.selection = list()
        self.show_selection = list()
        self.cat = np.loadtxt(filename)
        self.display_selection()

    def get_all_pos(self):
        """
        get all positions
        """
        all_pos = self.xpa.get("regions list -format xy -sky fk5 -system wcs -coordformat degree")
        if len(all_pos) == 0:
            self.all_pos = None
            return
        all_pos = all_pos.splitlines()
        all_pos = [pos.strip().split(" ") for pos in all_pos]
        self.all_pos = [(float(pos[0]),float(pos[1])) for pos in all_pos]
        self.match_all_cat()

    def get_pos(self):
        """
        get crosshair position
        """
        self.pos = self.xpa.get_pos()
        self.match_cat()

    def load_region_files(self, files):
        """
        load region files

        :param files: filename list
        """
        for i in files:
            self.xpa.load_region(i)

    def match_cat(self):
        """
        match to the catalog and update the position
        """
        self.match_id = np.argmin(distance2(self.cat[:,0], self.cat[:,1], self.pos[0], self.pos[1]))
        self.pos = (self.cat[self.match_id,0], self.cat[self.match_id,1])
        self.xpa.set("crosshair {0:f} {1:f} wcs".format(self.pos[0], self.pos[1]))

    def match_all_cat(self):
        """
        match all pos to catalog
        """
        self.all_match_id = list()
        if self.all_pos is None:
            self.all_match_id = None
            return
        for pos in self.all_pos:
            self.all_match_id.append(np.argmin(distance2(self.cat[:,0], self.cat[:,1], pos[0], pos[1])))

    def popout(self):
        """
        remove the last selection
        """
        if len(self.show_selection) > 0:
            self.show_selection.pop()

    def save_image(self, filename):
        """
        save DS9 image
        
        :param filename: file name to save
        """
        self.xpa.set("saveimage {0:s}".format(filename))

    def save_list(self, filename):
        """
        save catalog list

        :param filename: catalog file to save
        """
        with open(filename, "w") as f:
            for i in self.selection:
                for j in self.cat[i[0], :]:
                    f.write("{0:f} ".format(j))
                f.write("\n")

    def save_region(self, filename):
        """
        Save selection to region file

        :param filename: region file to save
        """
        with open(filename, "w") as f:
            f.write("fk5;\n")
            for i in self.selection:
                f.write("Circle {0:f} {1:f} 1\" \n".format(i[1], i[2]))

    def select_pos(self):
        """
        attach current match to selection list
        """
        self.show_selection.append((self.match_id, self.pos[0], self.pos[1]))

    def select_all_pos(self):
        """
        attach all match id to selection list
        """
        self.selection = list()
        unique_id = list()
        if self.all_match_id is None: # no region marked
            return
        for i in self.all_match_id:
            if i not in unique_id:
                unique_id.append(i)
                self.selection.append((i, self.cat[i,0], self.cat[i,1]))
        self.save_region("temp.reg")
        self.clean_region()
        self.load_region_files(["temp.reg"])

def distance2(ra, dec, x0, y0):
    """
    Calculate the rough distance between two object on sky
    """
    return ((ra-x0)*np.cos(np.deg2rad(y0)))**2 + (dec - y0)**2
