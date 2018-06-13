"""
For rules concerning normal text, like duplicate words, missing spaces.

"""

import re
from rules.classes import *


rules, tests = [], []

##############################################################################
# GENERAL
##############################################################################
rules.append(
    Rule(description="Duplicate words",
         re_pattern=re.compile(r"[\s.](\w+)[\s.]+\1", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=" .the THE "),
    TestRule(rule=rules[-1], text=" the. THE "),
    TestRule(rule=rules[-1], text=" the  THE "),
])

rules.append(
    Rule(description="Missing space at end of sentence",
         re_pattern=re.compile(r"\.[A-Z]+"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="blah.Blah"),
    TestRule(rule=rules[-1], text="v2.How"),
    TestRule(rule=rules[-1], text="v2.3", should_pass=True),
])


##############################################################################
# HYPHENATION
##############################################################################
rules.append(
    Rule(description="Missing hyphenation",
         re_pattern=re.compile(r"\w tagged"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b tagged"),
    TestRule(rule=rules[-1], text=r"\\cPt-tagged", should_pass=True),
])

rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-quark"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-quark"),
    TestRule(rule=rules[-1], text=r"b quark", should_pass=True),
])

rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-tag(?!ged)"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-tag"),
    TestRule(rule=rules[-1], text=r"b tag", should_pass=True),
    TestRule(rule=rules[-1], text=r"b-tagged", should_pass=True),
])

