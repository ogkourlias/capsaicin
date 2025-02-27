#!/usr/bin/env python3

"""
    usage:
        python3 orfeas_gkourlias_deelopdracht01.py
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.1"

# IMPORTS
import sys
import pandas as pd
import glob
import argparse
import os

# FUNCTIONS
def translate(sample_count):
    """ Desc """
    for barcode in range(1,100):
        sample = (barcode - 1) % sample_count + 1
        print(barcode, "sample", sample)
    return 0

def merge_report(reports):
    """ Desc """
    reports = [pd.read_csv(report, sep="\t",
                            names=["fragment_perc", "fragments_downstream", "fragments_taxon", "rank", "taxid", "tax"], usecols=["tax", "fragments_downstream", "fragments_taxon"])
                              for report in reports]
    merged = pd.concat(reports).groupby(['tax']).sum().reset_index()
    merged = merged.reindex(index=merged.index[::-1])
    merged = merged.sort_values("tax")
    merged.to_csv("test.csv")
    return 0

def merge_mpa(barcode, path, out, size_sort = 0):
    """ Desc """
    barcode = f"{str(barcode).zfill(2)}"
    reports = []
    for file in list(os.scandir(path)):
        if barcode in file.name and "-kraken2" in file.name:
            reports.append(file.path)
            #print(file.path)
    reports = [pd.read_csv(report, sep="\t",
                            names=["tax", "fragments"])
                              for report in reports]
    merged = pd.concat(reports).groupby(["tax"]).sum()
    merged = merged.reset_index()
    merged = merged[~merged["tax"].str.contains("Mammalia")]
    # merged = merged.reindex(index=merged.index[::-1])
    merged = merged.sort_values("tax")
    merged["ratio"] = (
        round(merged["fragments"] / max(merged["fragments"]), 10))
    if size_sort:
        merged = merged.sort_values("ratio", ascending=0)
    merged.to_csv(f"{out.rstrip("/")}/{barcode}.tsv", sep="\t")
    return 0

def input_list(fastq_dir):
    fastq_files = []
    for i in range(1, 21):
        barcode = f"barcode{str(i).zfill(2)}"
        if i < 11:
            fastq_files.extend(glob.glob(f"{fastq_dir}/chili1/*/fastq_pass/{barcode}/*.fastq.gz", recursive=True))
        else:
            fastq_files.extend(glob.glob(f"{fastq_dir}/chili2/*/fastq_pass/{barcode}/*.fastq.gz", recursive=True))

    # Writing input file names for logging purposes
    with open("input-files.txt", "w+") as input_log:
        for name in fastq_files:
            input_log.write(name + "\n")

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--barcode', type=str, required=False)
    parser.add_argument('--path', type=str, required=False)
    parser.add_argument('--out', type=str, required=False)
    args = parser.parse_args()
    return args

# MAIN
def main(args):
    """ Main function """
    # translate(4)
    # merge_mpa(["/commons/dsls/spicy/test_files/kraken2/test1-report.txt", "/commons/dsls/spicy/test_files/kraken2/test2-report.txt"], size_sort=1)
    args = parse()
    merge_mpa(args.barcode, args.path, args.out)
    # FINISH
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
