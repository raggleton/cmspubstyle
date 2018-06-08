#!/usr/bin/env python

"""Check your CMS document against PubComm guidelines.

References:
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionPrep
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionFormat
"""


import os
import sys
import argparse
from collections import OrderedDict
import re


def create_arg_parser():
    """Create an ArgumentParser"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Main paper/PAS/AN tex file. Will also check every file included with \\input.")
    parser.add_argument("--forSubmission", help="Extra checks for when paper is to be submitted. See https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionPrep", action='store_true')
    return parser


def check_args(args):
    """Check all user arguments are sane, otherwise raise errors"""
    print (args)

    if not args.input.endswith(".tex"):
        raise RuntimeError("Your input file must be a .tex")

    if not os.path.isfile(args.input):
        raise IOError("Input file does not exist")


def find_input_files(tex_file):
    """Return dict of included files in main tex file, split by category."""
    files_dict = OrderedDict()
    # the main tex file with abstract, title
    files_dict['root'] = tex_file
    # included files with definitions
    files_dict['defs'] = []
    # included files with main contents
    files_dict['contents'] = []
    # included bibliography
    files_dict['bib'] = os.path.splitext(tex_file)[0] + ".bib"

    input_pattern = re.compile(r"\\input{(.+)}")
    with open(tex_file) as f:
        for line in f:
            input_res = input_pattern.search(line)
            if not input_res:
                continue
            filename = input_res.group(1) + ".tex"
            filename = os.path.join(os.path.dirname(tex_file), filename)
            files_dict['contents'].append(filename)

    return files_dict


def find_command_text(filename, command):
    """Pull the text inside a command from the file"""
    command = command.lstrip("\\")

    with open(filename) as f:
        text = f.readlines()

    # Much easier to convert to one line of text than worrying about linebreaks
    text = ''.join([t.strip('\n') for t in text])

    latex_cmd = "\\"+command+"{"
    if latex_cmd not in text:
        return None

    # Start inside command, and count opening/closing brackets. Then we can
    # determine properly which is the right closing bracket.
    this_text = text.split(latex_cmd)[1]
    bracket_counter = 1
    command_text = []
    for c in this_text:
        if c == "{":
            bracket_counter += 1
        elif c == "}":
            bracket_counter -= 1
        if bracket_counter == 0:
            break
        command_text.append(c)

    return ("".join(command_text)).strip()


def check_text(text):
    """Method to check any piece of main text (not bib)"""
    pass


def check_root_file(filename):
    abstract_text = find_command_text(filename, "abstract")
    title_text = find_command_text(filename, "title")
    print(abstract_text)
    print(title_text)


def check_defs_files(filename):
    bad_cmd = r"\def"
    pass


def check_content_files(filename):
    pass


def check_bib_files(filename):
    pass


def main(in_args):
    parser = create_arg_parser()
    args = parser.parse_args(in_args)
    check_args(args)

    files_dict = find_input_files(args.input)
    print(files_dict)

    root_results = check_root_file(files_dict['root'])
    defs_results = check_defs_files(files_dict['defs'])
    content_results = check_content_files(files_dict['contents'])
    bib_results = check_bib_files(files_dict['bib'])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
