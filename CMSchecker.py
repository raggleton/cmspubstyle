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
from collections import OrderedDict, namedtuple
from bisect import bisect_left


def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError


TextLine = namedtuple("TextLine", ["line_num", "char_num_start", "text"])


def join_textlines(strings):
    return ''.join([x.text.rstrip('\n') for x in strings])


class Text(object):
    """Class to aid storage & finding in lines of latex"""

    def __init__(self, text, line_num_start=1):
        self.text_contents = []
        for ind, line in enumerate(text, line_num_start):
            # don't include the newline (which python counts as 1 char) since
            # we remove it when searching, and it would screw up looking for
            # relevant line(s)
            char_num_start = sum([len(l.text.rstrip('\n')) for l in self.text_contents]) + 1
            this_line = TextLine(line_num=ind, char_num_start=char_num_start, text=line)
            self.text_contents.append(this_line)
        self.create_one_str_from_contents()

    def create_one_str_from_contents(self):
        """Store text as one long line to make searching across lines easier"""
        self.text_as_one_line = ''.join([x.text.rstrip("\n") for x in self.text_contents])

    def find_line_with_char_num(self, char_num):
        """Select relevant line, based on which characters are involved"""
        # TODO: use bisect?
        for ind, line in enumerate(self.text_contents):
            if (line.char_num_start <= char_num and
                (ind == len(self.text_contents)-1 or
                 self.text_contents[ind+1].char_num_start > char_num)):
                return line

    def find_lines_with_char_num_range(self, char_num_start, char_num_end):
        # Select relevant lines, based on which characters are involved
        lines = []
        found_start = False
        for ind, x in enumerate(self.text_contents):
            if found_start:
                if x.char_num_start > char_num_end:
                    break
                lines.append(x)
            elif (char_num_start >= x.char_num_start and
                  self.text_contents[ind+1].char_num_start > char_num_start):
                # TODO: use bisect?
                lines.append(x)
                found_start = True
        return lines

    def iter_environment(self, environment):
        """Return contents of environments"""
        start_env = "\\begin{"+environment
        end_env = "\\end{"+environment
        if start_env not in self.text_as_one_line:
            yield None
            return
        # FIXME: this assumes everything on own lines,
        # no pre/post extra bits we dont want - issue?
        start_ind, end_ind = None, None
        for ind, line in enumerate(self.text_contents):
            if start_env in line.text:
                start_ind = ind
            if end_env in line.text:
                end_ind = ind
                if not (start_ind and end_ind):
                    raise RuntimeError("Found end of environment but not beginning: %s" % line)
                these_lines = self.text_contents[start_ind+1:end_ind]
                start_ind, end_ind = None, None
                yield these_lines

    def iter_inline_maths(self, delim="$"):
        """"""
        lines = []
        matches = list(re.finditer(r"\%s" % delim, self.text_as_one_line))
        for m1, m2 in zip(matches[:-1:2], matches[1::2]):
            # Assumes all contents on one TextLine!
            l = self.find_line_with_char_num(m1.start()+1)
            l2 = self.find_line_with_char_num(m2.end())
            if l2.line_num != l.line_num:
                raise RuntimeError("Your inline maths spans 2 lines - I don't knwo how to handle that")
            this_text = self.text_as_one_line[m1.start()+1:m2.start()]
            # FIXME: what should char_num_start be doing?
            new_line = TextLine(line_num=l.line_num, char_num_start=m1.start()+1, text=this_text)
            lines.append(new_line)
        return lines

    def iter_command(self, command):
        char_ind_pairs = []
        stack = []

        for m in re.finditer(r"\\"+command.lstrip("\\")+"{", self.text_as_one_line):
            stack.append(m.end()-1)
            for c_ind, c in enumerate(self.text_as_one_line[m.end():], m.end()):
                if c == "{":
                    stack.append(c_ind)
                elif c == "}":
                    if len(stack) == 1:
                        char_ind_pairs.append((stack.pop()+1, c_ind))
                        break
                    else:
                        stack.pop()

        lines = []

        # Handle the relevant line(s), chopping the text appropriately
        for s, e in char_ind_pairs:
            these_lines = self.find_lines_with_char_num_range(s, e-1)

            first_line_char_num = these_lines[0].char_num_start
            offset_start = s - first_line_char_num + 1
            these_lines[0] = TextLine(line_num=these_lines[0].line_num,
                                      char_num_start=s+1,
                                      text=these_lines[0].text[offset_start:])

            last_line_char_num = these_lines[-1].char_num_start
            offset_end = e - last_line_char_num + 1
            these_lines[-1] = TextLine(line_num=these_lines[-1].line_num,
                                       char_num_start=s,
                                       text=these_lines[-1].text[:offset_end])

            lines.append(these_lines)

        return lines

    def find_iter(self, pattern):
        results = []
        for m in pattern.finditer(self.text_as_one_line):
            # TODO what if >1 group?
            matching_text = m.groups()

            lines = []

            # need the +1 on .start() as re uses 0-indexing, whilst .end() alread has +1
            start, end = m.start() + 1, m.end()
            print(start, end)

            # Select relevant lines, based on which characters are involved
            found_start = False
            for ind, x in enumerate(self.text_contents):
                if found_start:
                    if x.char_num_start > m.end():
                        break
                    lines.append(x)
                elif (start >= x.char_num_start and
                      self.text_contents[ind+1].char_num_start > start):
                    # Look for first line that contains one of our chars
                    # TODO: use bisect?
                    print(x)
                    lines.append(x)
                    found_start = True

            print(lines)
            results.append((m, lines))
        return results


class Error(object):

    def __init__(self, description, re_pattern, where):
        self.description = description
        self.re_pattern = re_pattern
        self.where = where


def create_arg_parser():
    """Create an ArgumentParser"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input",
                        help="Main paper/PAS/AN tex file. Will also check every file included with \\input.")
    return parser


def check_args(args):
    """Check all user arguments are sane, otherwise raise errors"""
    print(args)

    if not args.input.endswith(".tex"):
        raise RuntimeError("Your input file must be a .tex")

    if not os.path.isfile(args.input):
        raise IOError("Input file does not exist")


def find_input_files(tex_file):
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


def extract_command_text(text, command):
    """Pull the text inside a command from the file"""
    command = command.lstrip("\\")

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


def extract_environment_text(filename, environment):
    with open(filename) as f:
        text = f.read()

    if "\\begin{"+environment not in text or "\\end{"+environment not in text:
        return None


def check_text(text):
    """Method to check any piece of main text (not bib)"""
    # TODO check which of standard + new newcommands can be used e.g. \fbinv
    checks = [
        Error(description="Duplicate words",
              re_pattern=re.compile(r"[\s.](\w+)[\s.]+\1", re.IGNORECASE),
              where=None),
    ]
    return True


def check_root_file(filename):
    """Check elements of the main TeX file"""
    with open(filename) as f:
        text = f.readlines()

    root_text = Text(text)

    abstract_text = root_text.iter_command("abstract")
    title_text = root_text.iter_command("title")

    # abstract_text = extract_command_text(text, "abstract")
    # title_text = extract_command_text(text, "title")
    # print(abstract_text)
    # print(title_text)
    # abstract_results = check_text(abstract_text)
    # title_results = check_text(title_text)

    for c in root_text.iter_command("HERWIG"):
        print(c)

    for c in root_text.iter_command("caption"):
        print(c)

    for c in root_text.iter_command("drums"):
        print(c)

    # for m in root_text.iter_inline_maths("$"):
    #     print(m)

    # for a in root_text.iter_environment("figure"):
    #     print(join_textlines(a))

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

    files_dict = find_input_files(args.input)
    # print(files_dict)

    root_results = check_root_file(files_dict['root'])
    content_results = check_content_files(files_dict['contents'])
    bib_results = check_bib_files(files_dict['bib'])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
