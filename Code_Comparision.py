# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:35:53 2022

@author: gowrishankar.p
"""
import difflib
import os

filename = 'DCOMMINS.txt'
exp_code_dir = 'D:\gowrishankar.p\Accelerate Task\Cobol_Sample_data_listing\PROD__exp'
tlistings_dir = 'D:\gowrishankar.p\Accelerate Task\Cobol_Sample_data_listing\Listing_trimmed'
reports_dir = 'D:\gowrishankar.p\Python Script'

def main():
    rep_file, match_ratio = compare_listing(filename, exp_code_dir, tlistings_dir, reports_dir)

# Core comparison process
def compare_listing(filename, exp_code_dir, tlistings_dir, reports_dir):
    fromfile = os.path.join(exp_code_dir, filename)
    tofile = os.path.join(tlistings_dir, filename)
    repfile = os.path.join(reports_dir, filename.rstrip(".txt")+".html")

    with open(fromfile) as f:
        fromlines = f.readlines()

    with open(tofile) as f:
        tolines = f.readlines()

    diff_html = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile, tofile)
    s = difflib.SequenceMatcher(None, fromlines, tolines)
    with open(repfile, "a") as f:
        f.write(diff_html)

    return repfile, s.ratio()

if __name__ == "__main__":
    main()