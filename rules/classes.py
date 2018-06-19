"""Classes to handle rules and test"""


import re
from bisect import bisect_left, bisect_right
from collections import namedtuple


def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError


TextLine = namedtuple("TextLine", ["line_num", "char_num_start", "text"])


class Text(object):
    """Class to aid storage & finding in lines of latex"""

    def __init__(self, text, line_num_start=1):
        self.text_contents = []
        if len(text) > 0:
            # Creation from list of str
            if type(text[0]) == str:
                for ind, line in enumerate(text, line_num_start):
                    # don't include the newline (which python counts as 1 char) since
                    # we remove it when searching, and it would screw up looking for
                    # relevant line(s)
                    char_num_start = sum([len(l.text.rstrip('\n')) for l in self.text_contents]) + 1
                    this_line = TextLine(line_num=ind, char_num_start=char_num_start, text=line)
                    self.text_contents.append(this_line)
            # Creation from list of TextLine e.g. from output of another Text
            elif type(text[0]) == TextLine:
                for line in text:
                    # reset char_num_start
                    char_num_start = sum([len(l.text.rstrip('\n')) for l in self.text_contents]) + 1
                    this_line = TextLine(line_num=line.line_num, char_num_start=char_num_start, text=line.text)
                    self.text_contents.append(this_line)
            else:
                raise RuntimeError("Unknown type %s for text arg for Text class - should be list[str] or list[TextLine]" % type(text[0]))
            
            self.text_as_one_line = ""
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
        char_num_starts = [x.char_num_start for x in self.text_contents]
        start_ind = bisect_right(char_num_starts, char_num_start)-1
        end_ind = bisect_left(char_num_starts, char_num_end)
        lines = self.text_contents[start_ind : end_ind]
        return lines

    def iter_environment(self, environment):
        r"""Return contents of environments, i.e. \begin{<environment>}...\end{<environment>}

        Returns list of TextLine for each occurence of \begin{<environment>}...\end{<environment>}
        """
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
                yield Text(these_lines)

    def iter_inline_delim(self, delim="$"):
        """Iterate over text inside matching delim, e.g. $...$

        Returns TextLine for each occurence of <delim>...<delim>
        """
        matches = list(re.finditer("\\" + delim, self.text_as_one_line))
        print(matches)
        for m1, m2 in zip(matches[:-1:2], matches[1::2]):
            # Assumes all contents on one TextLine!
            l = self.find_line_with_char_num(m1.start()+1)
            l2 = self.find_line_with_char_num(m2.end())
            # if l2.line_num != l.line_num:
            #     raise RuntimeError("Your inline maths spans 2 lines - I don't knwo how to handle that")
            this_text = self.text_as_one_line[m1.start()+1:m2.start()]
            # FIXME: what should char_num_start be doing?
            new_line = TextLine(line_num=l.line_num, char_num_start=m1.start()+1, text=this_text)
            yield Text([new_line])

    def iter_command(self, command):
        """Iterate over sections of text inside a \<command>{...}

        Returns list of TextLine for each occurence of \<command>
        """
        stack = []

        for m in re.finditer(r"\\"+command.lstrip("\\")+"{", self.text_as_one_line):
            # Use stack method to look for matching closing bracket
            # - could be more {} inside
            stack.append(m.end()-1)
            for c_ind, c in enumerate(self.text_as_one_line[m.end():], m.end()):
                if c == "{":
                    stack.append(c_ind)
                elif c == "}":
                    if len(stack) == 1:
                        s, e = stack.pop()+1, c_ind
                        # Handle the relevant line(s), chopping the text appropriately
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
                        yield Text(these_lines)
                        break
                    else:
                        stack.pop()

    def find_iter(self, pattern):
        """Iterate over search results"""
        for m in pattern.finditer(self.text_as_one_line):
            # TODO what if >1 group?
            matching_text = m.groups()

            # need the +1 on .start() as re uses 0-indexing, whilst .end() alread has +1
            start, end = m.start() + 1, m.end()
            lines = self.find_lines_with_char_num_range(start, end)
            yield (m, lines)


# Classes to handle sections/types of text to be searched
class Location(object):

    def __init__(self, opt=None):
        self.opt = opt

    def __hash__(self):
        return hash(self.opt)

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return self.opt == other.opt

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def to_str(self):
        opt = "" if self.opt is None else self.opt
        return self.__class__.__name__+'('+opt+')'

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()


class ALL(Location):
    def __init__(self, *args, **kwargs):
        super(ALL, self).__init__(*args, **kwargs)


class ENVIRONMENT(Location):
    def __init__(self, *args, **kwargs):
        super(ENVIRONMENT, self).__init__(*args, **kwargs)


class INLINE(Location):
    def __init__(self, *args, **kwargs):
        super(INLINE, self).__init__(*args, **kwargs)


class COMMAND(Location):
    def __init__(self, *args, **kwargs):
        super(COMMAND, self).__init__(*args, **kwargs)


# Classes to handle the actual grammar rules & their tests
class Rule(object):

    def __init__(self, description, re_pattern, where):
        self.description = description
        self.re_pattern = re_pattern
        self.where = where

    def __repr__(self):
        return "Rule("+str(self.re_pattern)+")"


class TestRule(object):
    """Class to define a test for a Rule, and whether it should pass or not"""

    def __init__(self, rule, text, should_pass=False):
        self.rule = rule
        if isinstance(text, str):
            self.text = Text([text])
        else:
            self.text = Text(text)
        self.should_pass = should_pass

    def __str__(self):
        return "TestRule(rule=%s, text=%s, should_pass=%s)" % (self.rule, self.text.text_as_one_line, self.should_pass)

    def __repr__(self):
        return "TestRule(rule=%s, text=%s, should_pass=%s)" % (self.rule, self.text.text_as_one_line, self.should_pass)

    def test():
        result = True
        return result

# Handle a specific case of a rule being broken, the pure regex result, and the offending line(s)
RuleBroken = namedtuple("RuleBroken", ["rule", "match", "lines"])
