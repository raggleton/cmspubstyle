import pytest
from itertools import chain

from cmspubstyle.rules import normal_text
from cmspubstyle.rules import latex


ALL_TESTS = normal_text.TESTS + latex.TESTS


@pytest.mark.parametrize("test", ALL_TESTS, ids=[x.rule.description for x in ALL_TESTS])
def test_a_rule(test):
    """Test one Rule via a TestRule"""
    rule = test.rule
    pattern = rule.re_pattern
    text = test.text.text_as_one_line
    should_pass = test.should_pass
    expect_word = "pass" if should_pass else "not pass"
    print("Testing", rule.description, "on: '"+text+"' (expect:", expect_word, ")")
    match = pattern.search(text)
    found = match is not None
    if found == should_pass:
        print("Failing test:", pattern, "on: '"+text+"' with match:", match)
    assert(found != should_pass)


def run_all_rule_tests():
    for test in ALL_TESTS:
        test_a_rule(test)


if __name__ == "__main__":
    run_all_rule_tests()
