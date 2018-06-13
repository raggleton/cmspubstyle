#!/usr/bin/env python

"""Check your CMS document against PubComm guidelines.

References:
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionPrep
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionFormat


I bear no responsiblity if this code misses errors - I was once told
"even if I think you have the needed skills.
You are seemingly lacking the needed concentration..."
"""

from __future__ import print_function
import os
import re
import sys
import argparse
from itertools import chain
from collections import OrderedDict
from bisect import bisect_left

from rules import normal_text
from rules import latex
from rules.classes import ALL, ENVIRONMENT, INLINE, COMMAND, Text, TextLine, RuleBroken, Rule, TestRule


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


def report_error(broken_rule):
    """Tell the user they broke a rule"""
    print(broken_rule.match, broken_rule.match.group(), "  [", broken_rule.rule.description, "]")


def check_text(text):
    """Method to check any piece of main text (not bib)"""
    # print("Checking", text.text_contents)
    for rule in chain(normal_text.rules, latex.rules):
        if isinstance(rule.where, ALL):
            for match, lines in text.find_iter(rule.re_pattern):
                yield RuleBroken(rule=rule, match=match, lines=lines)


def check_and_report_errors(text):
    """"""
    problems = []
    for broken_rule in check_text(text):
        report_error(broken_rule)
        problems.append(broken_rule)


def check_root_file(filename):
    """Check elements of the main TeX file"""
    with open(filename) as f:
        text = f.readlines()

    root_text = Text(text)

    abstract_text = Text(list(root_text.iter_command("abstract"))[0])
    print("-"*80)
    print(filename, "(ABSTRACT):")
    print("-"*80)
    abstract_problems = check_and_report_errors(abstract_text)

    # title_text_lines = Text(list(root_text.iter_command("title"))[0])
    # print("-"*80)
    # print(filename, "(TITLE):")
    # print("-"*80)
    # title_problems = check_and_report_errors(title_text)

    # for c in root_text.iter_command("HERWIG"):
    #     print(c)

    # for c in root_text.iter_command("caption"):
    #     print(c)

    # for c in root_text.iter_command("drums"):
    #     print(c)

    # for m in root_text.iter_inline_delim("$"):
    #     print(m)

    # for m in root_text.iter_inline_delim("$$"):
    #     print(m)

    # for a in root_text.iter_environment("figure"):
    #     print(join_textlines(a))

    # for c in root_text.find_iter(re.compile(r"[\s.](\w+)[\s.]+\1", re.IGNORECASE)):
    #     print(c)

    # return abstract_results + title_results


def check_content_files(filenames):
    for f in filenames:
        pass


def check_bib_files(filenames):
    pass


def main(in_args):
    parser = create_arg_parser()
    args = parser.parse_args(in_args)
    check_args(args)

    files_dict = extract_input_files(args.input)


    root_results = check_root_file(files_dict['root'])
    content_results = check_content_files(files_dict['contents'])
    bib_results = check_bib_files(files_dict['bib'])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
