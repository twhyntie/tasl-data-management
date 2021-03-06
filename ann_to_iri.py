#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 MoEDAL and CERN@school - ANN -> IRI.

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for handling the annotation JSON information.
import json

# The annotation file wrapper class.
from wrappers.ann import ANN

if __name__ == "__main__":

    print("*")
    print("*====================================*")
    print("* MoEDAL and CERN@school: ANN -> IRI *")
    print("*====================================*")
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

    ## The annotations path.
    ann_path = os.path.join(data_path, "ANN")
    if not os.path.isdir(ann_path):
        raise IOError("* ERROR: '%s' does not exist - no annotation data!" % (ann_path))

    ## The inner ring information data path.
    iri_path = os.path.join(data_path, "IRI")
    if not os.path.isdir(iri_path):
        os.mkdir(iri_path)

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join('./.', 'log_ann_to_iri.log'), filemode='w', level=level)

    lg.info(" *")
    lg.info(" *====================================*")
    lg.info(" * MoEDAL and CERN@school: ANN -> IRI *")
    lg.info(" *====================================*")
    lg.info(" *")
    lg.info(" * Looking for annotations in        : '%s'" % (ann_path))
    lg.info(" * Writing inner ring information in : '%s'" % (iri_path))
    lg.info(" *")

    # Loop over the found annotations.
    for i, ann_csv_path in enumerate(sorted(glob.glob(os.path.join(ann_path, "*.csv")))):

        ## The subject ID.
        sub_id = os.path.basename(ann_csv_path)[:-4]

        ## The annotations found for the subject.
        annotations = ANN(ann_csv_path)

        inner_ring_list = []

        # Loop over the annotations found in the subject.
        for anno_id, anno in annotations.get_annotations().iteritems():

            ## The annotation data
            d = json.loads(anno)

            # Loop over the task answers for this annotation.
            for entry in d:

                if entry["task"] == "T1":

                    # Get the inner ring information from the annotation.
                    inner_ring_info = entry["value"]

                    # Add an inner ring for each found.
                    for inner_ring_i in inner_ring_info:
                        x = inner_ring_i["x"]
                        y = inner_ring_i["y"]
                        r = inner_ring_i["r"]
                        inner_ring_list.append("%s,%.1f,%.1f,%.1f" % (anno_id,x,y,r))

        # Write out the IRI CSV file.
        ## The IRI CSV filename (and path).
        iri_csv_path = os.path.join(iri_path, "%s.csv" % (sub_id))
        #
        ## The CSV file string to write out.
        iri_csv_s = "annotation_id,x,y,r\n"
        #
        # Loop over the inner rings.
        for i, inner_ring_string in enumerate(inner_ring_list):
            iri_csv_s += inner_ring_string
            if i < len(inner_ring_list): iri_csv_s += "\n"
        #
        # Write out the CSV file.
        with open(iri_csv_path, "w") as nf:
            nf.write(iri_csv_s)

        lg.info(" * Subject '%s' found in '%s': % 6d annotations." % (sub_id, ann_csv_path, annotations.get_number_of_annotations()))

        print("* Converted '%s' -> '%s' (%d annotations)." % (ann_csv_path, iri_csv_path, annotations.get_number_of_annotations()))

    lg.info(" *")
    print("*")
