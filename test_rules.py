import pytest
from itertools import chain

from rules import normal_text
from rules import latex


ALL_TESTS = normal_text.tests + latex.tests


@pytest.mark.parametrize("test", ALL_TESTS, ids=[x.rule.description for x in ALL_TESTS])
def test_a_rule(test):
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


def run_all_rule_tests():
    for test in ALL_TESTS:
        test_a_rule(test)


if __name__ == "__main__":
    run_all_rule_tests()
