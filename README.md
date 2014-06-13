DS9 interface with Catalog
==========================

# Aim

Facilitate teh interaction with catalog and FITS image

# Basic Functions:

1. Load Region file

2. Select subsample based on given catalog

# Configure file

*ps9.cfg*

## Input

Specify the FITS image file name pattern (not crucial), default region file path, and catalog path (must-have).

## Output

Specify the region output, and catalog output

## Extra

Extra command to execute.

For instance

    import test as ds9

will replace the pyds9 to an pseudo ds9 connector.

# Prerequisite

+ pyds9
+ Tkinter
+ numpy
+ matplotlib
+ XPA

# Usage

    python psControl
