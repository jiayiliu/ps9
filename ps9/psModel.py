__author__ = 'jiayiliu'

import numpy as np
from sparameter import *


class XpaModel(ds9.ds9):
    """
    DS9 communication module
    """
    def __init__(self):
        ds9.ds9.__init__(self, start=False, wait=0)
        self.set("crosshair {0:s}".format(self.get("crosshair")))

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
        self.match_id = None
        self.pos = [0, 0]
        self.cat = None

    def clean_region(self):
        """
        clean region in DS9 image, and empty selection list
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
        content = ["{0:f} {1:f}".format(i[1],i[2]) for i in self.selection]
        return "R.A. Dec.\n"+"\n".join(content)

    def get_cat(self, filename):
        """
        get the catalog
        """
        self.cat = np.loadtxt(filename)

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
        if self.cat is None:
            return
        self.match_id = np.argmin(distance2(self.cat[:,0], self.cat[:,1], self.pos[0], self.pos[1]))
        self.pos = (self.cat[self.match_id,0], self.cat[self.match_id,1])
        self.xpa.set("crosshair {0:f} {1:f} wcs".format(self.pos[0], self.pos[1]))

    def popout(self):
        """
        remove the last selection
        """
        if len(self.selection) > 0:
            self.selection.pop()

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
        self.selection.append((self.match_id, self.pos[0], self.pos[1]))


def distance2(ra, dec, x0, y0):
    """
    Calculate the rough distance between two object on sky
    """
    return ((ra-x0)*np.cos(np.deg2rad(y0)))**2 + (dec - y0)**2
