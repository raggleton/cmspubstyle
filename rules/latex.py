"""
For rules concerning latex, like doing _{T}

"""

import re
from rules.classes import *


# TODO check which of standard + new newcommands can be used e.g. \fbinv

rules, tests = [], []

rules.append(
    Rule(description="Use roman subscript in maths",
        # ignore if \mathrm or \text in subscript, but pickup other things
         re_pattern=re.compile(r"^includegraphics[\w{}_\\=\[\].]*?_\{?(?!\\mathrm)(?!\\text)[\w\\]+\}?", re.IGNORECASE),
         # re_pattern=re.compile(r"_\{?(?!\\mathrm)(?!\\text)[\w\\]+\}?", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="$p_T$"),
    TestRule(rule=rules[-1], text="$p_{V}$"),
    TestRule(rule=rules[-1], text="$p_{J2}$"),
    TestRule(rule=rules[-1], text="$p_{rec}$"),
    TestRule(rule=rules[-1], text="$p_{VLQ}$"),
    TestRule(rule=rules[-1], text=r"$p_{\Zp}$", should_pass=True),  # user macro
    TestRule(rule=rules[-1], text=r"$p_{\mathrm{T}}$", should_pass=True),
    TestRule(rule=rules[-1], text=r"$p_{\mathrm{T}}$", should_pass=True),
    TestRule(rule=rules[-1], text=r"$p_{\mathrm{rec}}$", should_pass=True),
])

rules.append(
    Rule(description="Use \\ie macro",
         re_pattern=re.compile(r"i\.e\."),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="i.e."),
    TestRule(rule=rules[-1], text="\\ie", should_pass=True),
])

rules.append(
    Rule(description="Use \\eg macro",
         re_pattern=re.compile(r"e\.g\."),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="e.g."),
    TestRule(rule=rules[-1], text="\\eg, he's a pain", should_pass=True),
])

rules.append(
    Rule(description="Use \\etal macro",
         re_pattern=re.compile(r" et al"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="Ram et al"),
    TestRule(rule=rules[-1], text="Dave \\etal", should_pass=True),
])

# DASHES
# rules.append(
#     Rule(description="Use en dash -- for numerical range",
#          # re_pattern=re.compile(r"\d+\s*?(-|---)\s*?\d+"),
#          re_pattern=re.compile(r"(?<!cite)[\w{-]*?\d+\s*?(-|---)\s*?\d+"),
#          where=ALL())
# )
# tests.extend([
#     TestRule(rule=rules[-1], text="6-7"),
#     TestRule(rule=rules[-1], text="6 - 7"),
#     TestRule(rule=rules[-1], text="6---7"),
#     TestRule(rule=rules[-1], text="6 -- 7", should_pass=True),
#     TestRule(rule=rules[-1], text="6--7", should_pass=True),
# ])

# rules.append(
#     Rule(description="Use en dash -- for two people",
#          re_pattern=re.compile(r"^((?!cite).)*?[A-Z][a-z]*\s*?(-|---)\s*?[A-Z][a-z]*"),
#          where=ALL())
# )
# tests.extend([
#     TestRule(rule=rules[-1], text="Randall-Sundrum"),
#     TestRule(rule=rules[-1], text="Randall - Sundrum"),
#     TestRule(rule=rules[-1], text="Randall---Sundrum"),
#     TestRule(rule=rules[-1], text="Randall -- Sundrum", should_pass=True),
#     TestRule(rule=rules[-1], text="Randall--Sundrum", should_pass=True),
# ])
