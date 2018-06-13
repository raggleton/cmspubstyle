from itertools import chain

from rules import normal_text
from rules import latex


def test_all_rules():

    for test in chain(normal_text.tests, latex.tests):
        rule = test.rule
        pattern = rule.re_pattern
        text = test.text.text_as_one_line
        should_pass = test.should_pass
        expect_word = "OK" if should_pass else "not OK"
        print("Testing", rule.description, "on:", text, "(expect:", expect_word, ")")
        match = pattern.search(text)
        found = match is not None
        if found == should_pass:
            print("Failing test:", pattern, "on", text, "with result:", match)
        assert(found != should_pass)


if __name__ == "__main__":
    test_all_rules()
