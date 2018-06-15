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
# ABSTRACT ONLY
##############################################################################
rules.append(
    Rule(description='Missing "LHC" in abstract',
         re_pattern=re.compile(r"^(?!.*LHC).*$"),
         where=COMMAND("abstract"))
)
tests.extend([
    TestRule(rule=rules[-1], text="Some cool physics at ATLAS."),
    TestRule(rule=rules[-1], text="Other physics at LHC. My cool result.", should_pass=True),
])

rules.append(
    Rule(description='Missing "CMS" in abstract',
         re_pattern=re.compile(r"^(?!.*CMS).*$"),
         where=COMMAND("abstract"))
)
tests.extend([
    TestRule(rule=rules[-1], text="Some cool physics at ATLAS."),
    TestRule(rule=rules[-1], text="Other physics at CMS. My cool result.", should_pass=True),
])

rules.append(
    Rule(description='Missing Collaboration/experiment/detector after "CMS" in abstract',
         re_pattern=re.compile(r"CMS ((?!collaboration)(?!experiment))\w+", re.IGNORECASE),
         where=COMMAND("abstract"))
)
tests.extend([
    TestRule(rule=rules[-1], text="Our CMS result"),
    TestRule(rule=rules[-1], text="The CMS collaboration", should_pass=True),
])

rules.append(
    Rule(description="Missing data year in abstract",
         re_pattern=re.compile(r"^(?!.*201[0-9]).*$",),
         where=COMMAND("abstract"))
)
tests.extend([
    TestRule(rule=rules[-1], text="Our CMS result"),
    TestRule(rule=rules[-1], text="Data taken in 2016", should_pass=True),
    TestRule(rule=rules[-1], text="Data taken in 2016/2017", should_pass=True),
])

##############################################################################
# COMMAS
##############################################################################

rules.append(
    Rule(description="No comma before et al",
         re_pattern=re.compile(r", +\\etal"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="Josie, \\etal"),
    TestRule(rule=rules[-1], text="Mark  \\etal", should_pass=True),
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
    TestRule(rule=rules[-1], text=r"Higgs-tagged", should_pass=True),
])

rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-quark"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-quark"),
    TestRule(rule=rules[-1], text=r"\cPQb-quark"),
    TestRule(rule=rules[-1], text=r"b quark", should_pass=True),
    TestRule(rule=rules[-1], text=r"\cPQb quark", should_pass=True),
])

rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-tag(?!ged)"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-tag"),
    TestRule(rule=rules[-1], text=r"b tag", should_pass=True),
    TestRule(rule=rules[-1], text=r"{\PW} tag", should_pass=True),
    TestRule(rule=rules[-1], text=r"b-tagged", should_pass=True),
    TestRule(rule=rules[-1], text=r"b-tagged", should_pass=True),
])

