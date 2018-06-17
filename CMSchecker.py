#!/usr/bin/env python

"""Check your CMS document against PubComm guidelines.

References:
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionPrep
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionFormat

"""

from __future__ import print_function
import os
import re
import sys
import argparse
from itertools import chain
from collections import OrderedDict

from rules import normal_text
from rules import latex
from rules.classes import ALL, ENVIRONMENT, INLINE, COMMAND, Text, TextLine, RuleBroken, Rule, TestRule


class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def join_textlines(strings):
    return ''.join([x.text.rstrip('\n') for x in strings])


def create_arg_parser():
    """Create an ArgumentParser"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input",
                        help="Main paper/PAS/AN tex file. Will also check every file included with \\input.")
    return parser


def check_args(args):
    """Check all user arguments are sane, otherwise raise errors"""
    if not args.input.endswith(".tex"):
        raise RuntimeError("Your input file must be a .tex")

    if not os.path.isfile(args.input):
        raise IOError("Input file does not exist")


def extract_input_files(tex_file):
    """Return dict of included files in main tex file, split by category."""
    files_dict = OrderedDict()
    # the main tex file with abstract, title
    files_dict['root'] = tex_file
    # included bibliography
    files_dict['bib'] = os.path.splitext(tex_file)[0] + ".bib"

    # included files with main contents
    files_dict['contents'] = []
    input_pattern = re.compile(r"\\input\s*{(.+)}")
    with open(tex_file) as f:
        for line in f:
            if line.strip().startswith("%"):
                continue
            input_res = input_pattern.search(line)
            if not input_res:
                continue
            filename = input_res.group(1) + ".tex"
            filename = os.path.join(os.path.dirname(tex_file), filename)
            files_dict['contents'].append(filename)

    return files_dict


def report_error(broken_rule, color=bcolors.RED):
    """Print broken rule message on screen, highlight violating part & rule"""
    # print(broken_rule)
    
    line_num_str = str(broken_rule.lines[0].line_num)
    if len(broken_rule.lines) > 1:
        line_num_str += " - " + str(broken_rule.lines[-1].line_num)
    
    match = broken_rule.match
    
    start_ind = match.start() - broken_rule.lines[0].char_num_start + 1
    end_ind = match.end() - broken_rule.lines[0].char_num_start
    
    lines = ''.join([l.text for l in broken_rule.lines])
    
    error_str = lines[:start_ind].lstrip()
    error_str += color + bcolors.UNDERLINE + bcolors.BOLD + match.group(0) + bcolors.ENDC
    error_str += lines[end_ind+1:]
    error_str = error_str.rstrip('\n')
    
    print("    L"+line_num_str + ":", error_str, "  [", broken_rule.rule.description, "]")


def check_text(text):
    """Method to check any piece of main text (not bib)"""
    # locations = list(set([rule.where for rule in chain(normal_text.rules, latex.rules)]))
    # for l in locations:
    #     print(l)
    
    # for x in text.text_contents:
        # print(x)
    # print(text.text_as_one_line)

    for rule in chain(normal_text.rules, latex.rules):
        if isinstance(rule.where, ALL):
            # print(rule.re_pattern)

            for match, lines in text.find_iter(rule.re_pattern):
                yield RuleBroken(rule=rule, match=match, lines=lines)
    
        # elif isinstance(rule.where, COMMAND):
        #     print('doing', rule.where)
        #     for this_cmd_text in text.iter_command(rule.where.opt):
        #         print(this_cmd_text)
        #         for match, lines in this_cmd_text.iter_command(rule.re_pattern):
        #             yield RuleBroken(rule=rule, match=match, lines=lines)


def check_and_report_errors(text):
    """Check text for all errors, and print them out"""
    problems = []
    for broken_rule in check_text(text):
        report_error(broken_rule)
        problems.append(broken_rule)


def print_filename_header(filename):
    """Print header for filename"""
    separator = "-"*80
    print(separator)
    print(bcolors.BLUE + filename + bcolors.ENDC)
    print(separator)


def check_root_file(filename):
    """Check elements of the main TeX file"""
    with open(filename) as f:
        root_text = Text(f.readlines())

    abstract_text = list(root_text.iter_command("abstract"))[0]
    print_filename_header(filename + " (ABSTRACT)")
    abstract_problems = check_and_report_errors(abstract_text)

    # title_text_lines = Text(list(root_text.iter_command("title"))[0])
    # print_filename_header(filename + " (TITLE)")
    # title_problems = check_and_report_errors(title_text)

    # return abstract_results + title_results


def check_content_files(filenames):
    """Iterate through normal latex files and check each"""
    for filename in filenames:
        with open(filename) as f:
            text = Text(f.readlines())
        print_filename_header(filename)
        check_and_report_errors(text)


def check_bib_files(filenames):
    return True


def main(in_args):
    parser = create_arg_parser()
    args = parser.parse_args(in_args)
    check_args(args)

    files_dict = extract_input_files(args.input)
    print("files_dict", files_dict)
    root_results = check_root_file(files_dict['root'])
    content_results = check_content_files(files_dict['contents'])
    # content_results = check_content_files(files_dict['root'])
    bib_results = check_bib_files(files_dict['bib'])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
