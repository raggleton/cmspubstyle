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
         re_pattern=re.compile(r"\b(\w+)[\s.,]+\1[\s.,]+", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=" .the THE "),
    TestRule(rule=rules[-1], text=" ,the THE, "),
    TestRule(rule=rules[-1], text=" the. THE "),
    TestRule(rule=rules[-1], text=" the  THE "),
    TestRule(rule=rules[-1], text=" the  THE,"),
    TestRule(rule=rules[-1], text=" however, however "),
    TestRule(rule=rules[-1], text=" the. Then ", should_pass=True),
])

# rules.append(
#     Rule(description="Missing space at end of sentence",
#          re_pattern=re.compile(r"\.[A-Z]+"),
#          where=ALL())
# )
# tests.extend([
#     TestRule(rule=rules[-1], text="blah.Blah"),
#     TestRule(rule=rules[-1], text="v2.How"),
#     TestRule(rule=rules[-1], text="v2.3", should_pass=True),
# ])

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
         re_pattern=re.compile(r",\s+\\etal"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="Josie, \\etal"),
    TestRule(rule=rules[-1], text="Mark  \\etal", should_pass=True),
])

##############################################################################
# HYPHENATION
##############################################################################
# UNHYPHENATED, 2 WORDS
rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-jet"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-jet"),
    TestRule(rule=rules[-1], text=r"\cPQb-jet"),
    TestRule(rule=rules[-1], text=r"b jet", should_pass=True),
    TestRule(rule=rules[-1], text=r"\cPQb jet", should_pass=True),
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

rules.append(
    Rule(description="Unnecessary hyphenation",
         re_pattern=re.compile(r"\w-tagging"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="b-tagging"),
    TestRule(rule=rules[-1], text=r"b tagging", should_pass=True),
    TestRule(rule=rules[-1], text=r"{\PW} tagging", should_pass=True),
])

# UNHYPHENATED SINGLE WORDS

# SHOULD BE HYPHENATED
rules.append(
    Rule(description="Missing hyphenation",
         re_pattern=re.compile(r" \w tagged", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=" b tagged"),
    TestRule(rule=rules[-1], text=r"Higgs-tagged", should_pass=True),
    TestRule(rule=rules[-1], text="the tagged", should_pass=True),
])


##############################################################################
# COMMON GRAMMATICAL MISTAKES
##############################################################################
rules.append(
    Rule(description="Wrong indefinite article, SM requires 'an'",
         re_pattern=re.compile(r"a SM", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="a SM"),
    TestRule(rule=rules[-1], text=r"an SM", should_pass=True),
])

rules.append(
    Rule(description="Wrong indefinite article, SUSY requires 'a'",
         re_pattern=re.compile(r"\ban SUSY", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="an SUSY"),
    TestRule(rule=rules[-1], text=r"a SUSY", should_pass=True),
])

rules.append(
    Rule(description="'due to' or 'because of'?",
         re_pattern=re.compile(r"\bdue\b\s+\bto", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="due to"),
    TestRule(rule=rules[-1], text=r"subdue to", should_pass=True),
])

rules.append(
    Rule(description="'evidence' takes no plural",
         re_pattern=re.compile(r"\bevidences", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=".Evidences"),
    TestRule(rule=rules[-1], text="Evidences"),
    TestRule(rule=rules[-1], text=r". Evidence for", should_pass=True),
])

rules.append(
    Rule(description="'which' or 'that'?",
         re_pattern=re.compile(r"(?<!in)(?<!,) +\bwhich", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="background which"),
    TestRule(rule=rules[-1], text="in which", should_pass=True),
    TestRule(rule=rules[-1], text=r"background, which", should_pass=True),
])

rules.append(
    Rule(description="Do not use \"it's\"",
         re_pattern=re.compile(r"\bit's", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="it's"),
    TestRule(rule=rules[-1], text="bit's", should_pass=True),
    TestRule(rule=rules[-1], text=r"nits", should_pass=True),
])

##############################################################################
# ACRONYMS
##############################################################################

rules.append(
    Rule(description="Do not capitalise first letters",
         re_pattern=re.compile(r"Standard\b\s+\bModel"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="Standard Model"),
    TestRule(rule=rules[-1], text="standard model", should_pass=True),
])

rules.append(
    Rule(description="Do not capitalise first letters",
         re_pattern=re.compile(r"Quantum\b\s+\bChromodynamics"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="Quantum Chromodynamics"),
    TestRule(rule=rules[-1], text="quantum chromodynamics", should_pass=True),
])

rules.append(
    Rule(description="Do capitalise first letters",
         re_pattern=re.compile(r"monte\b\s+\bcarlo"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="monte carlo"),
    TestRule(rule=rules[-1], text="Monte Carlo", should_pass=True),
])

rules.append(
    Rule(description="Do not use d.o.f for degrees of freedom (use dof or n_d)",
         re_pattern=re.compile(r"d\.o\.f"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="d.o.f"),
    TestRule(rule=rules[-1], text="dof", should_pass=True),
])

rules.append(
    Rule(description="Do not use d.o.f for degrees of freedom (use dof or n_d)",
         re_pattern=re.compile(r"d\.o\.f"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text="d.o.f"),
    TestRule(rule=rules[-1], text="dof", should_pass=True),
])

rules.append(
    Rule(description="Do not start sentence with an acronym",
         re_pattern=re.compile(r"\.\s+\b[A-Z]{2,}\b"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r". VLQ"),
    TestRule(rule=rules[-1], text=".   VLQ"),
    TestRule(rule=rules[-1], text=r"a QLZ", should_pass=True),
])

##############################################################################
# SYMBOLS
##############################################################################

rules.append(
    Rule(description="Do not start sentence with a symbol",
         re_pattern=re.compile(r"\.\s+[\$\\](?!section)(?!ref)(?!subsection)(?!item)(?!begin)(?!end)"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r". \Zp"),
    TestRule(rule=rules[-1], text=".   $N_d$"),
    TestRule(rule=rules[-1], text=r"a \QLZ", should_pass=True),
])

rules.append(
    Rule(description="Use 'transverse momentum', not 'transverse energy'",
         re_pattern=re.compile(r"transverse\b\s+\benergy", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"transverse  energy"),
    TestRule(rule=rules[-1], text=r"transverse  momentum", should_pass=True),
])

##############################################################################
# WORD USE AND JARGON
##############################################################################

rules.append(
    Rule(description="Avoid 'actual', prefer 'current'/'existing'",
         re_pattern=re.compile(r"\bactual\b", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the actual setup"),
    TestRule(rule=rules[-1], text=r"factual", should_pass=True),
])

rules.append(
    Rule(description="Use 'X antiquark', not 'antiX quark'",
         re_pattern=re.compile(r"\banti-?[\w]+\b\s+quark", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the antitop quark "),
    TestRule(rule=rules[-1], text=r"the antibottom quark "),
    TestRule(rule=rules[-1], text=r"the antitop quark's "),
    TestRule(rule=rules[-1], text=r"the anti-top quark "),
    TestRule(rule=rules[-1], text=r"the top antiquark", should_pass=True),
])

rules.append(
    Rule(description="jargon: beamspot",
         re_pattern=re.compile(r"\bbeamspot'?s?\b", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the beamspot is"),
    TestRule(rule=rules[-1], text=r"the beamspot's is"),
    TestRule(rule=rules[-1], text=r"the beamspots is"),
])

rules.append(
    Rule(description="Use 'charged particle track' instead of 'charged track'",
         re_pattern=re.compile(r"\bcharged\b\s+\btrack\b", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the charged track is"),
    TestRule(rule=rules[-1], text=r"the charged   track."),
    TestRule(rule=rules[-1], text=r"the charged tracking", should_pass=True), # why?
])

rules.append(
    Rule(description="ATLAS & CMS Collaboration(s) have capital C",
         re_pattern=re.compile(r"(ATLAS|CMS)\b\s+\bcollaboration"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the CMS collaboration"),
    TestRule(rule=rules[-1], text=r"the ATLAS  collaboration."),
    TestRule(rule=rules[-1], text=r"the ATLAS & CMS collaborations."),
    TestRule(rule=rules[-1], text=r"the ATLAS and CMS Collaborations", should_pass=True),
])

rules.append(
    Rule(description="Tevatron collaborations have lower case c",
         re_pattern=re.compile(r"Tevatron\b\s+\bCollaborations"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the Tevatron Collaborations"),
    TestRule(rule=rules[-1], text=r"the Tevatron collaborations", should_pass=True),
])

rules.append(
    Rule(description="D0 Collaboration has capital c",
         re_pattern=re.compile(r"D0\b\s+\bcollaboration"),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"the D0 collaboration"),
    TestRule(rule=rules[-1], text=r"the D0 Collaboration", should_pass=True),
])

rules.append(
    Rule(description="Colloquial expression",
         re_pattern=re.compile(r"\bget\b\s+\brid\b\s+\bof", re.IGNORECASE),
         where=ALL())
)
tests.extend([
    TestRule(rule=rules[-1], text=r"we get rid of background"),
    TestRule(rule=rules[-1], text=r"forget riding off", should_pass=True),
])

