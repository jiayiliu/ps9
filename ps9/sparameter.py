__author__ = 'jiayiliu'

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read("./ps9.cfg")

################# Input Section ###################
#: Pattern of all FITS files
FITS_PATTERN = config.get("Input", "FITS_pattern")

#: Region file input path
DEFAULT_REGION_INPUT = config.get("Input", "Default_Region_Input")

#: Catalog input path
DEFAULT_CAT_INPUT_PATTERN = config.get("Input", "Default_Catalog_Input_Pattern")

################# Output Section ###################
#: Region file output path
DEFAULT_REGION_OUTPUT_PATTERN = config.get("Output", "Default_Region_output_pattern")

#: Catalog output path
DEFAULT_CAT_OUTPUT_PATTERN = config.get("Output", "Default_Catalog_Output_Pattern")

#:
DEFAULT_IMG_OUTPUT_PATTERN = config.get("Output", "Default_Img_Output_Pattern")
############# Extra loading of code ################
n = config.getint("Extra", "N")
for i in range(n):
    exec(config.get("Extra", "E{0:d}".format(i)))


