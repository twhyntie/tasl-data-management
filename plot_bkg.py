#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 MoEDAL and CERN@school - Plotting BKG information.

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

# The BKG wrapper class.
from wrappers.bkg import BKG

if __name__ == "__main__":

    print("*")
    print("*==================================================*")
    print("* MoEDAL and CERN@school: Plotting BKG information *")
    print("*==================================================*")
    print("*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("dataPath",        help="Path to the input dataset.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The root data path.
    data_path = args.dataPath

    # Check if the input file exists. If it doesn't, quit.
    if not os.path.exists(data_path):
        raise IOError("* ERROR: '%s' input file does not exist!" % (data_path))

    ## The number of blobs data path.
    bkg_path = os.path.join(data_path, "BKG")
    if not os.path.isdir(bkg_path):
        raise IOError("* ERROR: '%s' does not exist - no input data!" % (bkg_path))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join('./.', 'log_plot_bkg.log'), filemode='w', level=level)

    lg.info(" *")
    lg.info(" *==================================================*")
    lg.info(" * MoEDAL and CERN@school: Plotting BKG information *")
    lg.info(" *==================================================*")
    lg.info(" *")
    lg.info(" * Plotting background assessment information in : '%s'" % (bkg_path))
    lg.info(" *")

    # Loop over the found blob information.
    for i, bkg_csv_path in enumerate(sorted(glob.glob(os.path.join(bkg_path, "*.csv")))):

        ## The subject ID.
        sub_id = os.path.basename(bkg_csv_path)[:-4]

        ## The BKG wrapper object.
        bkg = BKG(bkg_csv_path)

        ## The path of the plot image.
        bkg_plot_image_path = os.path.join(bkg_path, "%s.png" % (sub_id))

        # Make the plot.
        bkg.make_frequency_histogram(bkg_plot_image_path)
