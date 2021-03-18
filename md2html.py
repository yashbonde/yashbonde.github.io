#!/usr/local/bin/python3

import re
import sys


no_data = False
try:
    in_file = sys.argv[1]
    out_file = sys.argv[2]
except:
    no_data = True

if sys.argv[1] == "--help" or no_data == True:
    print('''Tool to help convert any markdown file to HTML output.
Usage: md2html <in_file> <out_file>''')
    exit()

with open(in_file, "r") as f:
    lines = f.readlines()

##### parsing method #####
html = ""  # complete HTML string to put in the <body> </body>
curr_para = "<p>\n"
para_on = False
for l in lines:
    if not l and para_on:
        # this is new para if there is already a paragraph running
        curr_para += "</p>"
        html += curr_para
        curr_para = "<p>"
    
    elif l[0] == "#":
        # this is sub heading
        if len(re.findall("#", l)) > 3:
            # h3 heading
            html += f"<h3>"




