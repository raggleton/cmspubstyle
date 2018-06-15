# cms-grammar-checker

Check your PAS/PAPER/AN against the CMS PubComm guildelines.
Aims to make language review less embarassing, since no one can remember several TWikis worth of somewhat arbitrary rules.

## Install


## Running


## Add new rule

A rule is added via the `Rule` class.
Each rule is designed to look for **bad** words/patterns.
A rule has a `description`, which is presented to the user when an infraction occurs; therefore it should be concise and precise.
The matching pattern is implemented by a regular expression (in the form of a `re` pattern), passed in via the `re_pattern` arg.
Finally, the `where` arg specifies in what context to apply the rule: 

- `ALL()` for everywhere
- `ENVIRONMENT(xxx)` for sections inside `\begin{xxx}...\end{xxx}` (e.g. `ENVIRONMENT('figure')`)
- `INLINE(xxx)` for sections inside `xxx...xxx` (e.g. `INLINE('$')` for inline maths)
- `COMMAND(xxx)` for sections inside `\xxx{...}` (e.g. `COMMAND('abstract')` for the abstract)

A rule should have **at least 2** test cases: one case in which it fails the rule, and one case in which it passes the rule.
Tests for rules are implemente by instances of the `TestRule` class.
Each instance must have the `Rule` object which it is testing, the sample text string it is testing against, and whether or not the string should pass the rule (set via the `should_pass` arg).

The more test cases the better!

You should think about: what is the usual user error, what are edge cases, and which correct texts might trigger the rule accidentally.

## Running tests

To run the tests, you will need the `pytest` package.

If you do not already have it, install it with `pip install pytest`.

Then, just do `pytest`, and it will automatically run all tests.

## References

https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionPrep
https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PaperSubmissionFormat
