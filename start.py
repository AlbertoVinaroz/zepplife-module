import argparse
import json
import os
import sys
import logging
from ZL_std import Standalone

from utils import Utils

def start(args):
    Utils.setup_custom_logger()
    Utils.setup_case()
    
    logging.info("Starting Mifit analysis...")

    # Analysis logic

    standalone = Standalone(args.path, args.output, args.start, args.end, args.gps)
    standalone.analyse()
    standalone.report()
    logging.info("Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MiFit Analyzer')
    parser.add_argument('-p', '--path', help='Dump app data', required=True)
    parser.add_argument('-o', '--output', help='Report output path folder', required=False, default="report.json")
    parser.add_argument('-s', '--start', help='Forensic artifacts start date (dd-mm-yyyy)', required=False)
    parser.add_argument('-e', '--end', help='Forensic artifacts end date (dd-mm-yyyy)', required=False)
    parser.add_argument('-g', '--gps', help='Generate KML file (if available)', required=False)
    args = parser.parse_args()
    
    start(args)